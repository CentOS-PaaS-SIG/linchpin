import os
import sys
import ansible
from collections import namedtuple
from contextlib import contextmanager
from callbacks import PlaybookCallback
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor

ansible24 = float(ansible.__version__[0:3]) >= 2.4

if ansible24:
    from ansible.vars.manager import VariableManager
    from ansible.inventory.manager import InventoryManager as Inventory
else:
    from ansible.inventory import Inventory
    from ansible.vars import VariableManager


@contextmanager
def suppress_stdout():
    """
    This context manager provides tooling to make Ansible's Display class
    not output anything when used
    """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


def ansible_runner_2x(playbook_path,
                      module_path,
                      extra_vars,
                      inventory_src='localhost',
                      console=True):

    variable_manager = VariableManager()
    loader = DataLoader()
    variable_manager.extra_vars = extra_vars
    inventory = Inventory(loader=loader,
                          variable_manager=variable_manager,
                          host_list=inventory_src)
    passwords = {}
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
                      verbosity=0,
                      check=False)

    pbex = PlaybookExecutor(playbooks=[playbook_path],
                            inventory=inventory,
                            variable_manager=variable_manager,
                            loader=loader,
                            options=options,
                            passwords=passwords)

    return pbex



def ansible_runner_24x(playbook_path,
                       module_path,
                       extra_vars,
                       inventory_src,
                       console=True):

    loader = DataLoader()
    variable_manager = VariableManager(loader=loader)
    variable_manager.extra_vars = extra_vars
    inventory = Inventory(loader=loader, sources=[inventory_src])
    variable_manager.set_inventory(inventory)
    passwords = {}
    Options = namedtuple('Options', ['connection',
                                     'module_path',
                                     'forks',
                                     'become',
                                     'become_method',
                                     'become_user',
                                     'check',
                                     'diff',
                                     'listhosts',
                                     'listtasks',
                                     'listtags',
                                     'syntax',
                                     'remote_user',
                                     'private_key_file',
                                     'ssh_common_args',
                                     'ssh_extra_args',
                                     'sftp_extra_args',
                                     'scp_extra_args',
                                     'verbosity',
                                     ])
    options = Options(listtags=False,
                      listtasks=False,
                      listhosts=False,
                      syntax=False,
                      connection='local',
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
                      verbosity=4,
                      diff=False,
                      check=False)

    pbex = PlaybookExecutor(playbooks=[playbook_path],
                            inventory=inventory,
                            variable_manager=variable_manager,
                            loader=loader,
                            options=options,
                            passwords=passwords)
    return pbex


def ansible_runner(playbook_path,
                   module_path,
                   extra_vars,
                   inventory_src='localhost',
                   console=True):
        """
        Uses the Ansible API code to invoke the specified linchpin playbook
        :param playbook: Which ansible playbook to run (default: 'up')
        :param console: Whether to display the ansible console (default: True)
        """

        extra_vars["ansible_python_interpreter"] = sys.executable

        if ansible24:
            pbex = ansible_runner_24x(playbook_path,
                                      module_path,
                                      extra_vars,
                                      inventory_src,
                                      console)
        else:
            pbex = ansible_runner_2x(playbook_path,
                                     module_path,
                                     extra_vars,
                                     inventory_src,
                                     console)

        if not console:
            results = {}
            return_code = 0
            cb = PlaybookCallback()
            with suppress_stdout():
                pbex._tqm._stdout_callback = cb
            return_code = pbex.run()
            results = cb.results
            return return_code, results
        else:
            # the console only returns a return_code
            return_code = pbex.run()
            return return_code, None
