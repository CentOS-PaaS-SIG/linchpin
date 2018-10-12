import os
import sys
import ansible
from collections import namedtuple
from contextlib import contextmanager

ansible24 = float(ansible.__version__[0:3]) >= 2.4
ansible_version = float(ansible.__version__[0:3])


# CentOS 6 EPEL provides an alternate Jinja2 package
# used by the imports below - Ansible uses Jinja2 here

try:
    from .callbacks import PlaybookCallback
    from ansible.parsing.dataloader import DataLoader
    from ansible.executor.playbook_executor import PlaybookExecutor
except ImportError:
    sys.path.insert(0, '/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg')
    from .callbacks import PlaybookCallback
    from ansible.parsing.dataloader import DataLoader
    from ansible.executor.playbook_executor import PlaybookExecutor

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
                      extra_vars,
                      options=None,
                      inventory_src='localhost',
                      console=True):

    variable_manager = VariableManager()
    loader = DataLoader()
    variable_manager.extra_vars = extra_vars
    inventory = Inventory(loader=loader,
                          variable_manager=variable_manager,
                          host_list=inventory_src)
    passwords = {}
    pbex = PlaybookExecutor([playbook_path],
                            inventory,
                            variable_manager,
                            loader,
                            options,
                            passwords)

    return pbex



def ansible_runner_24x(playbook_path,
                       extra_vars,
                       options=None,
                       inventory_src='localhost',
                       console=True):

    loader = DataLoader()
    variable_manager = VariableManager(loader=loader)
    variable_manager.extra_vars = extra_vars
    inventory = Inventory(loader=loader, sources=[inventory_src])
    variable_manager.set_inventory(inventory)
    passwords = {}

    pbex = PlaybookExecutor([playbook_path],
                            inventory,
                            variable_manager,
                            loader,
                            options,
                            passwords)
    return pbex


def ansible_runner(playbook_path,
                   module_path,
                   extra_vars,
                   inventory_src='localhost',
                   verbosity=1,
                   console=True):
    """
    Uses the Ansible API code to invoke the specified linchpin playbook
    :param playbook: Which ansible playbook to run (default: 'up')
    :param console: Whether to display the ansible console (default: True)
    """

    # note: It may be advantageous to put the options into the context and pass
    # that onto this method down the road. The verbosity flag would just live
    # in options and we could set the defaults.

    # module path cannot accept list in ansible 2.3.x versions
    if ansible_version <= 2.3:
        module_path = ":".join(module_path)

    connect_type = 'ssh'
    if 'localhost' in inventory_src:
        extra_vars["ansible_python_interpreter"] = sys.executable
        connect_type = 'local'

    Options = namedtuple('Options', ['connection',
                                     'module_path',
                                     'forks',
                                     'become',
                                     'become_method',
                                     'become_user',
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
                                     'check',
                                     'diff',
                                     ])

    options = Options(connection=connect_type,
                      module_path=module_path,
                      forks=100,
                      become=False,
                      become_method='sudo',
                      become_user='root',
                      listhosts=False,
                      listtasks=False,
                      listtags=False,
                      syntax=False,
                      remote_user=None,
                      private_key_file=None,
                      ssh_common_args=None,
                      ssh_extra_args=None,
                      sftp_extra_args=None,
                      scp_extra_args=None,
                      verbosity=verbosity,
                      check=False,
                      diff=False
                      )

    if ansible24:
        pbex = ansible_runner_24x(playbook_path,
                                  extra_vars,
                                  options,
                                  inventory_src=inventory_src,
                                  console=console)
    else:
        pbex = ansible_runner_2x(playbook_path,
                                 extra_vars,
                                 options,
                                 inventory_src=inventory_src,
                                 console=console)
    if ansible_version >= 2.5:
        cb = PlaybookCallback(options=options, ansible_version=ansible_version)
    else:
        cb = PlaybookCallback(options=options)

    if not console:
        results = {}
        return_code = 0
        with suppress_stdout():
            pbex._tqm._stdout_callback = cb
        return_code = pbex.run()
        results = cb.results
        return return_code, results
    else:
        # the console only returns a return_code
        pbex._tqm._stdout_callback = None
        return_code = pbex.run()
        return return_code, None
