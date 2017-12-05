#!/usr/bin/env python

import os
import re
import sys
import click

from distutils import dir_util
from collections import OrderedDict

from linchpin import LinchpinAPI
from linchpin.utils import yaml2json
from linchpin.fetch import FETCH_CLASS
from linchpin.exceptions import LinchpinError


class LinchpinCli(LinchpinAPI):

    def __init__(self, ctx):
        """
        Set some variables, pass to parent class
        """

        LinchpinAPI.__init__(self, ctx)


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


    def lp_init(self, pf_w_path, providers=['libvirt']):
        """
        Initializes a linchpin project. Creates the necessary directory
        structure, includes PinFile, topologies and layouts for the given
        provider. (Default: Libvirt. Other providers not yet implemented.)

        :param pf_w_path: Path to where the PinFile might exist. Gets created
        if it doesn't exist.

        :param providers: A list of providers for which templates
        (and a target) will be provided into the workspace.
        NOT YET IMPLEMENTED
        """

        src = self.get_cfg('init', 'source', 'templates/')
        src_w_path = os.path.realpath('{0}/{1}'.format(self.ctx.lib_path, src))

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


    def lp_up(self, pinfile, targets='all', run_id=None):
        """
        This function takes a list of targets, and provisions them according
        to their topology.

        :param pinfile:
            Provided PinFile, with available targets

        :param targets:
            A tuple of targets to provision

        :param run_id:
            An optional run_id if the task is idempotent or a destroy action
        """

        return self._build_and_execute(pinfile,
                                       targets=targets,
                                       action='up',
                                       run_id=run_id)


    def lp_destroy(self, pinfile, targets='all', run_id=None):
        """
        This function takes a list of targets, and performs a destructive
        teardown, including undefining nodes, according to the target(s).

        .. seealso:: lp_down - currently unimplemented

        :param pinfile:
            Provided PinFile, with available targets,

        :param targets:
            A tuple of targets to destroy.
        """

        return self._build_and_execute(pinfile,
                                       targets,
                                       action="destroy",
                                       run_id=run_id)


    def lp_down(self, pinfile, targets='all'):
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


    def find_topology(self, topology):
        """
        Find the topology to be acted upon. This could be pulled from a
        registry.

        :param topology:
            name of topology from PinFile to be loaded

        """

        topo_path = os.path.realpath('{0}/{1}'.format(
                                     self.ctx.workspace,
                                     self.get_evar('topologies_folder',
                                                   'topologies')))

        topos = os.listdir(topo_path)

        if topology in topos:
            return os.path.realpath('{0}/{1}'.format(topo_path, topology))

        raise LinchpinError('Topology {0} not found in'
                            ' workspace'.format(topology))


    def _build_and_execute(self, pinfile, targets='all',
                           action='up', run_id=None):
        """
        This function takes a list of targets, constructs a dictionary of tasks
        and passes it to the LinchpinAPI.do_action method for processing.

        :param pinfile:
            Provided PinFile, with available targets

        :param targets:
            A tuple of targets to provision

        :param action:
            Specific action to perform on the provided target(s)

        :param run_id:
            An optional run_id if the task is idempotent or a destroy action
        """

        pf = yaml2json(pinfile)

        # determine what targets is equal to
        if (set(targets) ==
                set(pf.keys()).intersection(targets) and len(targets) > 0):
            pass
        elif len(targets) == 0:
            targets = set(pf.keys()).difference()
        else:
            raise LinchpinError("One or more invalid targets found")

        ws = self.ctx.workspace

        provision_data = {}

        for target in targets:

            provision_data[target] = {}

            topology_data = yaml2json(self.find_topology(pf[target]["topology"]))  # noqa: E501

            provision_data[target]['topology'] = topology_data
            layout_data = None

            if 'layout' in pf[target]:
                self.set_evar('layout_file',
                              '{0}/{1}/{2}'.format(self.ctx.workspace,
                                                   self.get_evar(
                                                       'layouts_folder'),
                                                   pf[target]["layout"]))

                ws = self.ctx.workspace
                layout_folder = self.get_evar("layouts_folder",
                                              default='layouts')
                layout_file = pf[target]['layout']
                layout_path = '{0}/{1}/{2}'.format(ws,
                                                   layout_folder,
                                                   layout_file)
                layout_data = yaml2json(layout_path)

                provision_data[target]['layout'] = layout_data

        return self.do_action(provision_data, action=action, run_id=run_id)


    def lp_fetch(self, src, fetch_type, root):
        if root is not None:
            root = list(filter(None, root.split(',')))

        dest = self.ctx.workspace
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
            os.mkdir(cache_path)

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
