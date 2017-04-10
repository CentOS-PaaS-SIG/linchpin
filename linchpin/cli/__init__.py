#!/usr/bin/env python

from linchpin.api import LinchpinAPI


class LinchpinCli(LinchpinAPI):

    def __init__(self, ctx):
        LinchpinAPI.__init__(self, ctx)



#import os
#
#from linchpin.api import LinchpinAPI
#from linchpin.api.invoke_playbooks import invoke_linchpin
#from linchpin.cli.utils import find_topology
#from linchpin.api import LinchpinError
#from linchpin.api.utils import yaml2json
#
#
#class LinchpinCli(LinchpinAPI):
#
#    def __init__(self, ctx):
#        LinchpinAPI.__init__(self)
#        self.ctx = ctx
#
#
#    def lp_rise(self, pf, targets='all'):
#        """
#        DEPRECATED
#
#        An alias for lp_up. Used only for backward compatibility.
#        """
#
#        self.lp_up(pf, targets)
#
#
#    def lp_up(self, pinfile, targets='all'):
#        """
#        This function takes a list of targets, and provisions them according
#        to their topology. If an layout argument is provided, an inventory
#        will be generated for the provisioned nodes.
#
#        \b
#        pf:
#            Provided PinFile, with available targets,
#
#        \b
#        targets:
#            A tuple of targets to provision.
#        """
#
#        pf = yaml2json(pinfile)
#
#        e_vars = {}
#        e_vars['outputfolder_path'] = self.ctx.cfgs['lp']['outputs_folder']
#        e_vars['inventory_outputs_path'] = (
#                self.ctx.cfgs['lp']['inventories_folder'])
#        e_vars['state'] = "present"
#
#        if targets == "all":
#            for key in set(pf.keys()).difference(self.excludes):
#                e_vars['topology'] = find_topology(ctx, pf[key]["topology"])
#                if e_vars['topology'] is None:
#                    raise LinchpinError('Topology for target: {0} not found '
#                            '!!'.format(key))
#
#                if pf[key].has_key('layout'):
#                    layout_path = self.find_layout(pf[key]["layout"], pf)
#                    e_vars['inventory_layout_file'] = layout_path
#                    if e_vars['inventory_layout_file'] is None:
#                        print("Layout not found !!")
#                        break
#                    print(e_vars)
#                output = invoke_linchpin(self.base_path,
#                                         e_vars,
#                                         "PROVISION",
#                                         console=True)
#        else:
#            if pf.get(target, False):
#                topology_path = self.find_topology(pf[target]["topology"],
#                                                   pf)
#                e_vars['topology'] = topology_path
#                if e_vars['topology'] is None:
#                    print("Topology not found !!")
#                if pf[key].has_key('layout'):
#                    layout_path = self.find_layout(pf[target]["layout"], pf)
#                    e_vars['inventory_layout_file'] = layout_path
#                    if e_vars['inventory_layout_file'] is None:
#                        print("Layout not found !!")
#                    print(e_vars)
#                output = invoke_linchpin(self.base_path,
#                                         e_vars,
#                                         "PROVISION",
#                                         console=True)
#            else:
#                raise KeyError('Target not found in PinFile')
#
#
#
