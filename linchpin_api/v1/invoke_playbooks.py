import os
import yaml
import os.path
import click
import shutil
import errno
import sys
import json
import inspect
import pdb
import ansible
import pprint
import jsonschema as jsch
from tabulate import tabulate
from ansible import utils
from jinja2 import Environment, PackageLoader
from collections import namedtuple
from ansible import utils
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from callbacks import PlaybookCallback


PLAYBOOKS = {
           "PROVISION": "site.yml",
           "TEARDOWN": "site.yml",
           "SCHEMA_CHECK": "schemacheck.yml",
           "INVGEN": "invgen.yml",
           "TEST": "test.yml",
}


def get_evars(pf):
    """ creates a group of extra vars on basis on linchpin file """
    e_vars = []
    for group in pf:
        topology = pf[group].get("topology")
        layout = pf[group].get("layout")
        e_var_grp = {}
        e_var_grp["topology"] = search_path(topology, os.getcwd())
        e_var_grp["layout"] = search_path(layout, os.getcwd())
        if None in e_var_grp.values():
            display("ERROR:003")
        e_vars.append(e_var_grp)
    return e_vars


def invoke_linchpin(base_path, e_vars, playbook="PROVISION", console=True):
    """ Invokes linchpin playbook """
    module_path = base_path+"/library"
    print("debug:: module path ::"+module_path)
    playbook_path = base_path+"/provision/"+PLAYBOOKS[playbook]
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
