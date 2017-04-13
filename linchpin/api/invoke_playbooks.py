import os
import pprint
import jsonschema as jsch
from tabulate import tabulate

import ansible
from ansible import utils
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from callbacks import PlaybookCallback

from collections import namedtuple


#PLAYBOOKS = {
#           "PROVISION": "site.yml",
#           "TEARDOWN": "site.yml",
#           "SCHEMA_CHECK": "schemacheck.yml",
#           "INVGEN": "invgen.yml",
#           "TEST": "test.yml",
#}



def invoke_linchpin(ctx, lp_path, e_vars, playbook='provision', console=True):

    """
    Invokes linchpin playbook
    """

    pb_path = '{0}/{1}'.format(lp_path, ctx.cfgs['lp']['playbooks_folder'])
    module_path = '{0}/{1}'.format(pb_path, ctx.cfgs['lp']['module_folder'])
    playbook_path = '{0}/{1}'.format(pb_path, ctx.cfgs['playbooks'][playbook])

    loader = DataLoader()
    variable_manager = VariableManager()
    variable_manager.extra_vars = e_vars
    inventory = Inventory(loader=loader,
                          variable_manager=variable_manager,
                          host_list=[])
    passwords = {}
    utils.VERBOSITY = 4

    Options = namedtuple('Options', ['listtags',
                                     'listtasks',
                                     'listhosts',
                                     'syntax',
                                     'connection',
                                     'module_path',
                                     'forks',
                                     'remote_user',
                                     'private_key_file',
                                     'ssh_common_args',
                                     'ssh_extra_args',
                                     'sftp_extra_args',
                                     'scp_extra_args',
                                     'become',
                                     'become_method',
                                     'become_user',
                                     'verbosity',
                                     'check'])

    options = Options(listtags=False,
                      listtasks=False,
                      listhosts=False,
                      syntax=False,
                      connection='ssh',
                      module_path=module_path,
                      forks=100,
                      remote_user='test',
                      private_key_file=None,
                      ssh_common_args=None,
                      ssh_extra_args=None,
                      sftp_extra_args=None,
                      scp_extra_args=None,
                      become=False,
                      become_method='sudo',
                      become_user='root',
                      verbosity=utils.VERBOSITY,
                      check=False)

    pbex = PlaybookExecutor(playbooks=[playbook_path],
                            inventory=inventory,
                            variable_manager=variable_manager,
                            loader=loader,
                            options=options,
                            passwords=passwords)

    if not console:
        cb = PlaybookCallback()
        pbex._tqm._stdout_callback = cb
        return_code = pbex.run()
        results = cb.results
    else:
        results = pbex.run()
    return results
