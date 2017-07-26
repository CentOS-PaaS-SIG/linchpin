#!/usr/bin/env python

import os
import sys
import click
from distutils import dir_util

from linchpin.api import LinchpinAPI


class LinchpinCli(LinchpinAPI):

    def __init__(self, ctx):
        """
        Set some variables, pass to parent class
        """

        LinchpinAPI.__init__(self, ctx)


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
                if not click.confirm(
                    '{0} already exists, overwrite it?'.format(pf_w_path),
                    default=False):
                    sys.exit(0)

            dir_util.copy_tree(src_w_path, self.workspace, verbose=1)
            os.rename(src_pf, pf_w_path)

            self.ctx.log_state('{0} and file structure created at {1}'.format(
                self.pinfile, self.workspace))
        except Exception as e:
            self.ctx.log_state('Error: {0}'.format(e))
            sys.exit(1)
