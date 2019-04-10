#!/usr/bin/env python

import os
import ast
import sys
import json
import click
import hashlib

from random import randint
from distutils import dir_util
from collections import OrderedDict

from linchpin import LinchpinAPI
from linchpin.fetch import FETCH_CLASS
from linchpin.exceptions import ActionError
from linchpin.exceptions import LinchpinError
from linchpin.exceptions import TopologyError
from linchpin.exceptions import ValidationError
from linchpin.utils.dataparser import DataParser



class LinchpinCli(LinchpinAPI):

    def __init__(self, ctx):
        """
        Set some variables, pass to parent class
        """

        LinchpinAPI.__init__(self, ctx)
        self.__meta__ = "CLI"
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

    def _write_to_inventory(self, tx_id=None, inv_path=None, inv_format="cfg"):
        latest_run_data = self._get_run_data_by_txid()
        if tx_id:
            latest_run_data = self._get_run_data_by_txid(tx_id)
        all_inventories = {}
        try:
            for t_id in latest_run_data:
                targets = latest_run_data[t_id]["targets"][0]
                # if there are multiple targets mentioned in pinfile
                # the multiple inventory files are being generated
                inv_file_count = 0 if len(targets) > 1 else False
                for name in targets:
                    if "layout_data" in targets[name]["inputs"]:
                        lt_data = targets[name]["inputs"]["layout_data"]
                        t_data = targets[name]["inputs"]["topology_data"]
                        c_data = {}
                        if "cfgs" in targets[name].keys():
                            c_data = targets[name]["cfgs"]["user"]
                        i_path = targets[name]["outputs"]["inventory_path"][0]
                        layout = lt_data["inventory_layout"]
                        # check whether inventory_file is mentioned in layout

                        if not os.path.exists(os.path.dirname(i_path)):
                            os.makedirs(os.path.dirname(i_path))
                        if inv_path and inv_file_count is not False:
                            i_path = inv_path + str(inv_file_count)
                        # r_o -> resources_outputs
                        r_o = targets[name]["outputs"]["resources"]
                        # TODO: in the future we should render templates in
                        # layout and cfgs here so that we can use data from the
                        # most recent run
                        inv = self.generate_inventory(r_o,
                                                      layout,
                                                      inv_format=inv_format,
                                                      topology_data=t_data,
                                                      config_data=c_data)
                        # if inv_path is explicitly mentioned it is used
                        if inv_path:
                            i_path = inv_path
                        # if there are multiple targets based on
                        # number of targets multiple files are
                        # generated with suffixes
                        if inv_path and isinstance(inv_file_count, int):
                            i_path = inv_path + "." + str(name)
                            with open(i_path, 'w') as the_file:
                                the_file.write(inv)
                            inv_file_count += 1
                        else:
                            with open(i_path, 'w') as the_file:
                                the_file.write(inv)
                        all_inventories[name] = inv
            return all_inventories

        except Exception as e:
            self.ctx.log_state('Error: {0}'.format(e))
            sys.exit(1)
        return True


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
        if self.workspace:
            pf_w_path = '{0}/{1}'.format(self.workspace, self.pinfile)

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

        resources_folder = self.get_evar('resources_folder',
                                         default='resources')
        context_path = '{0}/{1}'.format(self.workspace, resources_folder)

        resources_path = os.path.expanduser(
            self.get_evar('default_resources_path'))

        if (os.path.isabs(resources_path)):
                context_path = resources_path
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

    def _write_latest_run(self):
        latest_run_data = self._get_run_data_by_txid()
        resources_path = self.get_evar('resources_folder')
        context_path = '{0}/{1}'.format(self.workspace, resources_path)
        if not os.path.exists(context_path):
            os.makedirs(context_path)
        context_file = '{0}/{1}'.format(context_path, 'linchpin.latest')
        with open(context_file, 'w+') as f:
            f.write(json.dumps(latest_run_data))


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


    def lp_up(self, targets=(), run_id=None, tx_id=None, inv_f="cfg"):
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
        self._write_latest_run()
        self._write_to_inventory(inv_format=inv_f)

        if (('post' in self.pb_hooks) and
                (self.__meta__ == "CLI") and
                not self.get_cfg('hook_flags', 'no_hooks')):
            self.hook_state = '{0}{1}'.format('post', 'up')

        # Show success and errors, with data
        return (return_code, return_data)


    def lp_validate(self, targets=(), old_schema=False):
        """
        This function takes a list of targets, and validates their topology.

        :param targets:
            A tuple of targets to provision

        :param old_schema
            Denotes whether schema should be validated with the old schema
            rather than the new one!/usr/bin/env python
        """

        # Prep input data

        pf_w_path = self._get_pinfile_path()
        pf_data_path = self._get_data_path()
        if not pf_data_path:
            pf = self.parser.process(pf_w_path, data=self.pf_data)
        else:
            pf = self.parser.process(pf_w_path,
                                     data='@{0}'.format(pf_data_path))

        if pf:
            provision_data = self._build(pf, pf_data=self.pf_data)

            pf_outfile = self.get_cfg('tmp', 'outfile')
            if pf_outfile:
                self.parser.write_json(provision_data, pf_outfile)

        prov_data = OrderedDict()

        if len(targets):
            for target in targets:
                prov_data[target] = provision_data.get(target)
        else:
            prov_data = provision_data

        return self.do_validation(prov_data, old_schema=old_schema)


    def lp_setup(self, providers=("all")):
        """
        This function takes a list of providers, and setsup the dependencies
        :param providers:
            A tuple of providers to install dependencies
        """
        if self.ctx.get_evar("ask_sudo_pass"):
            output = self._invoke_playbooks(providers=providers,
                                            action="ask_sudo_setup")
        else:
            output = self._invoke_playbooks(providers=providers,
                                            action="setup")

        return output




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


        outputs = self._execute_action('destroy',
                                       targets,
                                       run_id=run_id,
                                       tx_id=tx_id)
        if (('post' in self.pb_hooks) and
            (self.__meta__ == "CLI") and not self.get_cfg('hook_flags',
                                                          'no_hooks')):
            self.hook_state = '{0}{1}'.format('post', 'destroy')
        return outputs


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
                provision_data = self._build(pf, pf_data=self.pf_data)

                pf_outfile = self.get_cfg('tmp', 'outfile')
                if pf_outfile:
                    self.parser.write_json(provision_data, pf_outfile)


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
        elif ftype == 'hooks':
            folder = self.get_evar('hooks_folder', 'hooks')

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

    def _render_template(self, template, data):
        if data is None:
            return template

        if data.startswith('@'):
            with open(data[1:], 'r') as strm:
                data = strm.read()

        try:
            template = json.dumps(template)
            render = self.parser.render(template, data)
        except TypeError:
            error_txt = "Error attempting to parse PinFile data file."
            error_txt += "\nTemplate-data files require a prepended '@'"
            error_txt += " (eg. '@/path/to/template-data.yml')"
            error_txt += "\nPerhaps the path to the PinFile or"
            error_txt += " template-data is missing or the incorrect path?."
            raise ValidationError(error_txt)

        return json.JSONDecoder(object_pairs_hook=OrderedDict).decode(render)


    def _build(self, pf, pf_data=None):
        """
        This function constructs the provision_data from the pinfile inputs

        :param pf:
            Provided PinFile dict, with all targets

        """

        provision_data = OrderedDict()

        for target in pf.keys():
            if target == 'cfgs':
                provision_data['cfgs'] = pf['cfgs']
                continue

            provision_data[target] = OrderedDict()

            if isinstance(pf[target]['topology'], str):
                topology_path = self.find_include(pf[target]["topology"])
                topology_data = self.parser.process(topology_path,
                                                    data=self.pf_data)
                topology_data = self._render_template(topology_data,
                                                      self.pf_data)
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
                    layout_data = self._render_template(layout_data,
                                                        self.pf_data)
                    layout_data = self._make_layout_integers(layout_data)
                else:
                    layout_data = pf[target]['layout']
                provision_data[target]['layout'] = layout_data


            if 'hooks' in pf[target]:
                if isinstance(pf[target]['hooks'], str):
                    hook_path = self.find_include(pf[target]['hooks'],
                                                  ftype='hooks')
                    hook_data = self.parser.process(hook_path,
                                                    data=self.pf_data)
                    provision_data[target]['hooks'] = hook_data
                else:
                    hook_data = pf[target]['hooks']
                    provision_data[target]['hooks'] = hook_data
            # grab target specific vars

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


    def lp_fetch(self, src, root='', fetch_type='workspace',
                 fetch_protocol='FetchGit', fetch_ref=None, dest_ws=None,
                 nocache=False):
        """
        Fetch a workspace from git, http(s), or a local directory, and
        generate a provided workspace

        :param src:         The URL or URI of the remote directory

        :param root:        Used to specify the location of the workspace
                            within the remote. If root is not set, the root
                            of the given remote will be used.

        :param fetch_type:  Specifies which component(s) of a workspace the
                            user wants to fetch. Types include: topology,
                            layout, resources, hooks, workspace.
                            (default: workspace)

        :param fetch_protocol:  The protocol to use to fetch the workspace.
                                (default: git)

        :param fetch_ref:   Specify the git branch. Used only with git protocol
                            (eg. master). If not used, the default branch will
                            be used.

        :param dest_ws: Workspaces destination, the workspace will be relative
                        to this location.

                        If `dest_ws` is not provided and `-r/--root` is
                        provided, the basename will be the name of the
                        workspace within the destination. If no root is
                        provided, a random workspace name will be generated.
                        The destination can also be explicitly set by using
                        -w (see linchpin --help).

        :param nocache: If true, don't copy from the cache dir, unless it's
                        longer than the configured fetch.cache_days (1 day)
                        (default: False)
        """

        root_ws = ''
        if dest_ws and dest_ws != '.':
            if root:
                abs_root = os.path.expanduser(os.path.realpath(root))
                root_ws = os.path.basename(abs_root.rstrip(os.path.sep))
            else:
                # generate a unique value for the root
                hash_string = '{0}{1}'.format(src, dest_ws)
                uroot = hashlib.sha256(hash_string)
                uroot = uroot.hexdigest()[:8]

                # generate a random location to put an underscore
                min_under = randint(1, 7)
                max_under = min_under + 1
                root_ws = uroot[:min_under] + '_' + uroot[max_under:]
        else:
            dest_ws = self.workspace
            if root:
                abs_root = os.path.expanduser(os.path.realpath(root))
                root_ws = os.path.basename(abs_root.rstrip(os.path.sep))
#                else:
#                    pass  # dest = self.workspace (set at the top)

        dest = '{0}/{1}'.format(dest_ws, root_ws)

        output_txt = 'destination workspace: {0}'.format(dest)
        if not os.path.exists(dest):
            os.makedirs(dest)
            output_txt = 'Created {0}'.format(output_txt)

        self.ctx.log_state(output_txt)

        fetch_aliases = {
            "topologies": self.get_evar("topologies_folder"),
            "layouts": self.get_evar("layouts_folder"),
            "resources": self.get_evar("resources_folder"),
            "hooks": self.get_evar("hooks_folder"),
            "workspace": "workspace"
        }

        fetch_type = fetch_aliases.get(fetch_type, 'workspaces')

        cache_path = os.path.abspath(os.path.join(os.path.expanduser('~'),
                                                  '.cache/linchpin'))
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

        fetch_class = FETCH_CLASS[fetch_protocol](self.ctx, fetch_type, src,
                                                  dest, cache_path, root=root,
                                                  root_ws=root_ws,
                                                  ref=fetch_ref)
        fetch_class.fetch_files()

        if nocache:
            self.set_cfg('fetch', 'cache_ws', 'False')

        fetch_class.copy_files()
