#!/usr/bin/env python

import os
import re
import ast
import sys
import json
import click

from distutils import dir_util
from collections import OrderedDict

from linchpin import LinchpinAPI
from linchpin.fetch import FETCH_CLASS
from linchpin.exceptions import ActionError
from linchpin.exceptions import LinchpinError
from linchpin.exceptions import TopologyError
from linchpin.utils.dataparser import DataParser


class LinchpinCli(LinchpinAPI):

    def __init__(self, ctx):
        """
        Set some variables, pass to parent class
        """

        LinchpinAPI.__init__(self, ctx)
        self.parser = DataParser()


    @property
    def pinfile(self):
        """
        getter function for pinfile name
        """

        return self.ctx.pinfile


    @pinfile.setter
    def pinfile(self, pinfile):
        """
        setter for pinfile name
        """

        self.ctx.pinfile = pinfile


    @property
    def pf_data(self):
        """
        getter for pinfile template data
        """

        return self.ctx.pf_data


    @pf_data.setter
    def pf_data(self, pf_data):
        """
        setter for pinfile template data
        """

        self.ctx.pf_data = pf_data


    @property
    def workspace(self):
        """
        getter function for context workspace
        """

        return self.ctx.workspace


    @workspace.setter
    def workspace(self, workspace):
        """
        setter for context workspace
        """

        self.ctx.workspace = workspace
        self.ctx.set_evar('workspace', workspace)


    def lp_init(self, providers=['libvirt']):
        """
        Initializes a linchpin project. Creates the necessary directory
        structure, includes PinFile, topologies and layouts for the given
        provider. (Default: Dummy. Other providers not yet implemented.)

        :param providers: A list of providers for which templates
        (and a target) will be provided into the workspace.
        NOT YET IMPLEMENTED
        """

        src = self.get_cfg('init', 'source', 'templates/')
        src_w_path = os.path.realpath('{0}/{1}'.format(self.ctx.lib_path, src))

        pf_w_path = self._get_pinfile_path(exists=False)

        # appending .lp_example so we know which PinFile is which
        src_pf = os.path.realpath('{0}.lp_example'.format(pf_w_path))

        try:
            if os.path.exists(pf_w_path):
                if not click.confirm('{0} already exists,'
                                     'overwrite it?'.format(pf_w_path),
                                     default=False):
                    sys.exit(0)

            dir_util.copy_tree(src_w_path, self.workspace, verbose=1)
            os.rename(src_pf, pf_w_path)

            self.ctx.log_state('{0} and file structure created at {1}'.format(
                self.pinfile, self.workspace))
        except Exception as e:
            self.ctx.log_state('Error: {0}'.format(e))
            sys.exit(1)

    def _get_pinfile_path(self, exists=True):
        """
        This function finds the self.pinfile. If the file is a full path,
        it is expanded and used. If not found, the lp.default_pinfile
        configuration value is used for the pinfile, the workspace is
        prepended and returned.

        :param exists:
            Whether the pinfile is supposed to already exist (default: True)
        """

        if not self.pinfile:
            self.pinfile = self.get_cfg('lp',
                                        'default_pinfile',
                                        default='PinFile')

        pf_w_path = os.path.realpath(os.path.expanduser(self.pinfile))

        # Ensure a PinFile path will exist
        if not os.path.exists(pf_w_path) and exists:
            pf_w_path = '{0}/{1}'.format(self.workspace, self.pinfile)

        # If the PinFile doesn't exist, raise an error
        if not os.path.exists(pf_w_path) and exists:
            raise LinchpinError('{0} not found. Please check that it'
                                ' exists and try again'.format(pf_w_path))

        return pf_w_path


    def _get_data_path(self):
        """
        This function finds the template data path, or returns the data.
        If the file is a full path, it is expanded and used.
        If not found, the workspace is prepended. If still not found, it
        is assumed what is passed in is data and returned to the caller.

        :param data_path:
            Consists of either a absolute path, relative path, or the actual
            template data.
        """

        if not self.pf_data or not self.pf_data.startswith('@'):
            return None
        else:
            pf_data_path = self.pf_data[1:]
            data_w_path = os.path.abspath(os.path.expanduser(pf_data_path))

            if not os.path.exists(data_w_path):
                data_w_path = '{0}/{1}'.format(self.workspace, pf_data_path)
                if not os.path.exists(data_w_path):
                    error_txt = "Template-data (-d) file was not found. Check"
                    error_txt += " the template path and try again."
                    raise TopologyError(error_txt)

            return data_w_path


    def _write_distilled_context(self, run_data):
        """
        This method takes all of the provided run_data, loops through the
        distiller section of the linchpin.constants and writes out the
        linchpin.context (name TBD) to the 'resources' directory.
        """

        dist_roles = self.get_cfg('distiller')

        resources_path = self.get_evar('resources_folder')
        context_path = '{0}/{1}'.format(self.workspace, resources_path)
        if not os.path.exists(context_path):
            os.makedirs(context_path)
        context_file = '{0}/{1}'.format(context_path, 'linchpin.distilled')

        roles = []
        dist_data = {}
        # get roles used
        for target, data in run_data.iteritems():
            inputs = data.get('inputs')
            topo = inputs.get('topology_data')
            res_grps = topo.get('resource_groups')

            for group in res_grps:
                res_defs = group.get('resource_definitions')
                for rd in res_defs:
                    roles.append(rd.get('role'))

            fields = {}
            outputs = data.get('outputs', {})
            resources = outputs.get('resources', [])

            for dist_role, flds in dist_roles.iteritems():
                if dist_role in roles:
                    for f in flds.split(','):
                        if '.' not in f:
                            fld = fields.get('single', [])
                            fields[f] = None
                        else:
                            k, v = f.split('.')
                            fld = fields.get(k, [])
                            if ':' in v:
                                subfields = {}
                                k2, val = v.split(':')
                                subfld = subfields.get(k2, [])
                                subfld.append(val)
                                subfields[k2] = subfld
                                fld.append(subfields)
                                fields[k] = fld
                            else:
                                fld.append(v)
                                fields[k] = fld

            try:
                for res in resources:
                    res_data = []
                    for k, v in fields.iteritems():
                        if not v:
                            res_dict = {}
                            res_dict[k] = res.get(k)
                            res_data.append(res_dict)
                        else:
                            for rsrc in res.get(k, []):
                                res_dict = {}
                                for value in v:
                                    if isinstance(value, dict):
                                        for key, vals in value.iteritems():
                                            subrsc = rsrc.get(key)
                                            for val in vals:
                                                res_dict[val] = subrsc.get(val)
                                    else:
                                        res_dict[value] = rsrc.get(value)
                                res_data.append(res_dict)

                    if target not in dist_data.keys():
                        dist_data[target] = []

                    if len(res_data) and res_data not in dist_data[target]:
                        dist_data[target].extend(res_data)
            except Exception as e:
                self.ctx.log_info('Error recording distilled context'
                                  ' ({0})'.format(e))
        with open(context_file, 'w+') as f:
            f.write(json.dumps(dist_data))


    def lp_down(self, pinfile, targets=(), run_id=None):
        """
        This function takes a list of targets, and performs a shutdown on
        nodes in the target's topology. Only providers which support shutdown
        from their API (Ansible) will support this option.

        CURRENTLY UNIMPLEMENTED

        .. seealso:: lp_destroy

        :param pinfile:
            Provided PinFile, with available targets,

        :param targets:
            A tuple of targets to provision.
        """

        pass


    def lp_up(self, targets=(), run_id=None, tx_id=None):
        """
        This function takes a list of targets, and provisions them according
        to their topology.

        :param targets:
            A tuple of targets to provision

        :param run_id:
            An optional run_id if the task is idempotent

        :param tx_id:
            An optional tx_id if the task is idempotent
        """

        # Prep input data

        # Execute prepped data
        return_code, return_data = self._execute_action('up',
                                                        targets,
                                                        run_id=run_id,
                                                        tx_id=tx_id)

        # Distill data
        new_tx_id = return_data.keys()[0]

        # This is what the API allows.
        # run_data = self.get_run_data(new_tx_id, ('outputs', 'inputs',
        #                                          'action', 'cfgs', 'start',
        #                                          'end', 'rc', 'uhash'))

        run_data = self.get_run_data(new_tx_id, ('inputs', 'outputs'))

        # Export distilled data in useful ways
        # # Write out run_data to a file for now
        distill_data = self.get_cfg('lp', 'distill_data')
        gen_resources = self.get_evar('generate_resources')

        if ast.literal_eval(distill_data.title()) and not gen_resources:
            if return_code:
                distill_on_error = self.get_cfg('lp',
                                                'distill_on_error',
                                                default='False')
                if ast.literal_eval(distill_on_error.title()):
                    self._write_distilled_context(run_data)
            else:
                    self._write_distilled_context(run_data)

        # Show success and errors, with data
        return (return_code, return_data)



    def lp_destroy(self, targets=(), run_id=None, tx_id=None):

        """
        This function takes a list of targets, and performs a destructive
        teardown, including undefining nodes, according to the target(s).

        .. seealso:: lp_down - currently unimplemented

        :param targets:
            A tuple of targets to destroy.

        :param run_id:
            An optional run_id to use

        :param tx_id:
            An optional tx_id to use
        """

        # prep inputs


        return self._execute_action('destroy',
                                    targets,
                                    run_id=run_id,
                                    tx_id=tx_id)


    def _execute_action(self, action, targets=(), run_id=None, tx_id=None):
        """
        This function takes a list of targets, and performs a destructive
        teardown, including undefining nodes, according to the target(s).

        .. seealso:: lp_down - currently unimplemented

        :param targets:
            A tuple of targets to perform action upon.

        :param run_id:
            An optional run_id to use

        :param tx_id:
            An optional tx_id to use
        """

        use_pinfile = True
        pf = None
        pf_data = None

        return_data = OrderedDict()
        return_code = 0

        urfa = self.get_cfg('lp', 'use_rundb_for_actions')
        use_rundb_for_actions = ast.literal_eval(urfa.title())

        # The UI should catch this, but just in case.
        if run_id and tx_id:
            raise ActionError("'run_id' and 'tx_id' are mutually exclusive")

        if use_rundb_for_actions:
            if run_id and not tx_id:
                if not len(targets) == 1:
                    raise ActionError("'use_rundb_for_actions' is enabled."
                                      " A single target required when"
                                      " passing --run_id.")
                run_id = int(run_id)
                use_pinfile = False
            elif not run_id and tx_id:
                use_pinfile = False

        if use_pinfile:
            pf_w_path = self._get_pinfile_path()
            pf_data_path = self._get_data_path()
            if not pf_data_path:
                pf = self.parser.process(pf_w_path, data=self.pf_data)
            else:
                pf = self.parser.process(pf_w_path,
                                         data='@{0}'.format(pf_data_path))

            if pf:
                provision_data = self._build(pf, pf_data)

            return_code, return_data = self._execute(provision_data,
                                                     targets,
                                                     action=action,
                                                     run_id=run_id)
        else:
            # get the pinfile data from the run_id or the tx_id
            provision_data = self.get_pf_data_from_rundb(targets,
                                                         run_id=run_id,
                                                         tx_id=tx_id)

            if provision_data:
                return_code, return_data = self._execute(provision_data,
                                                         targets,
                                                         action=action,
                                                         run_id=run_id,
                                                         tx_id=tx_id)

            else:
                return (99, {})

        return (return_code, return_data)


    def find_include(self, filename, ftype='topology'):
        """
        Find the included file to be acted upon.

        :param filename:
            name of file from to be loaded

        :param ftype:
            the file type to locate: topology, layout
            (default: topology)

        """

        folder = self.get_evar('topologies_folder', 'topologies')
        if ftype == 'layout':
            folder = self.get_evar('layouts_folder', 'layouts')

        path = os.path.realpath('{0}/{1}'.format(self.workspace, folder))
        files = os.listdir(path)

        if filename in files:
            return os.path.realpath('{0}/{1}'.format(path, filename))

        raise LinchpinError('{0} not found in'
                            ' workspace'.format(filename))


    def _make_layout_integers(self, data):

        inv_layout = data.get('inventory_layout')

        if inv_layout:
            hosts = inv_layout.get('hosts')
            for k in hosts:
                count = int(hosts[k].get("count"))
                hosts[k]["count"] = count
            inv_layout["hosts"] = hosts
            data["inventory_layout"] = inv_layout

        return data


    def _build(self, pf, pf_data=None):
        """
        This function constructs the provision_data from the pinfile inputs

        :param pf:
            Provided PinFile dict, with all targets

        """

        provision_data = {}

        for target in pf.keys():

            provision_data[target] = {}

            if not isinstance(pf[target]['topology'], dict):
                topology_path = self.find_include(pf[target]["topology"])
                topology_data = self.parser.process(topology_path,
                                                    data=self.pf_data)
            else:
                topology_data = pf[target]['topology']

            provision_data[target]['topology'] = topology_data

            layout_data = None

            if 'layout' in pf[target]:
                if not isinstance(pf[target]['layout'], dict):
                    layout_path = self.find_include(pf[target]["layout"],
                                                    ftype='layout')

                    layout_data = self.parser.process(layout_path,
                                                      data=self.pf_data)
                    layout_data = self._make_layout_integers(layout_data)
                    provision_data[target]['layout'] = layout_data
                else:
                    layout_data = pf[target]['layout']
                    provision_data[target]['layout'] = layout_data

            if 'hooks' in pf[target]:
                provision_data[target]['hooks'] = pf[target]['hooks']
            # grab target specific vars
            if 'cfgs' in pf[target]:
                provision_data[target]['cfgs'] = pf[target]['cfgs']

        return provision_data


    def _execute(self, provision_data, targets,
                 action='up', run_id=None, tx_id=None):
        """
        This function takes a list of targets, constructs a dictionary of tasks
        and passes it to the LinchpinAPI.do_action method for processing.

        :param provision_data:
            Provided PinFile json data, with available targets

        :param targets:
            A tuple of targets to provision

        :param action:
            Specific action to perform on the provided target(s)

        :param run_id:
            An optional run_id if the task is idempotent or a destroy action
        """

        prov_data = OrderedDict()

        if len(targets):
            for target in targets:
                prov_data[target] = provision_data.get(target)
        else:
            prov_data = provision_data

        return self.do_action(prov_data,
                              action=action,
                              run_id=run_id,
                              tx_id=tx_id)


    def lp_fetch(self, src, root=None, fetch_type='workspace'):
        if root is not None:
            root = list(filter(None, root.split(',')))

        dest = self.workspace
        if not os.path.exists(dest):
            raise LinchpinError(dest + " does not exist")

        fetch_aliases = {
            "topologies": self.get_evar("topologies_folder"),
            "layouts": self.get_evar("layouts_folder"),
            "resources": self.get_evar("resources_folder"),
            "hooks": self.get_evar("hooks_folder"),
            "workspace": "workspace"
        }

        fetch_dir = fetch_aliases.get(fetch_type, "workspace")


        cache_path = os.path.abspath(os.path.join(os.path.expanduser('~'),
                                                  '.cache/linchpin'))
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        protocol_regex = OrderedDict([
            ('((git|ssh|http(s)?)|(git@[\w\.]+))'
                '(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?',
                'FetchGit'),
            ('^(http|https)://', 'FetchHttp'),
            ('^(file)://', 'FetchLocal')
        ])
        fetch_protocol = None
        for regex, obj in protocol_regex.items():
            if re.match(regex, src):
                fetch_protocol = obj
                break
        if fetch_protocol is None:
            raise LinchpinError("The protocol speficied is not supported")


        fetch_class = FETCH_CLASS[fetch_protocol](self.ctx, fetch_dir, src,
                                                  dest, cache_path, root)
        fetch_class.fetch_files()
        fetch_class.copy_files()
