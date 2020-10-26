# The ansible_runner file contains all of the functions used to call ansible
# playbooks.  The runner can call playbooks via the Ansible API or the CLI,
# and supports the three most recent versions of Ansible (just as the Ansible
# team itself does)

from __future__ import absolute_import
import os
import sys
import json
import ansible
import subprocess
import tempfile
from contextlib import contextmanager
from .utils import ansible_version_recognizer as avr

ansible_ver_firstdigit = int(ansible.__version__.split('.')[:2][0])
ansible_ver_seconddigit = int(ansible.__version__.split('.')[:2][1])
ansible24 = avr.ansibleverisgreaterthan(2.3)
ansible_version = [ansible_ver_firstdigit, ansible_ver_seconddigit]

# CentOS 6 EPEL provides an alternate Jinja2 package
# used by the imports below - Ansible uses Jinja2 here

try:
    from .callbacks import PlaybookCallback
    from ansible.parsing.dataloader import DataLoader
    from ansible.executor.playbook_executor import PlaybookExecutor
except ImportError:
    from .callbacks import PlaybookCallback
    from ansible.parsing.dataloader import DataLoader
    from ansible.executor.playbook_executor import PlaybookExecutor

if ansible24:
    from ansible.vars.manager import VariableManager
    from ansible.inventory.manager import InventoryManager as Inventory
else:
    from ansible.inventory import Inventory
    from ansible.vars import VariableManager

if avr.ansibleverisgreaterthan(2.8):
    from ansible import context


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


def subprocess_runner(cmd, shell=False):
    """
    Runs subprocess commands
    param: cmd in a list
    param: shell to print stdout, stderr or not

    """
    os.environ['PYTHONUNBUFFERED'] = "1"
    os.environ['ANSIBLE_FORCE_COLOR'] = '1'
    my_env = os.environ.copy()
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            env=my_env
                            )
    stdout = []
    stderr = []
    while proc.poll() is None:
        std_out_line = proc.stdout.read()
        std_err_line = proc.stderr.read()
        if shell:
            print(std_out_line)
            print(std_err_line)
        else:
            stdout.append(std_out_line)
            stderr.append(std_err_line)
    return proc.returncode, stdout, stderr


def ansible_runner_24x(playbook_path,
                       extra_vars,
                       options,
                       inventory_src='localhost',
                       console=True):

    loader = DataLoader()
    variable_manager = VariableManager(loader=loader)
    variable_manager._extra_vars = extra_vars
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


def ansible_runner_28x(playbook_path,
                       extra_vars,
                       options,
                       inventory_src='localhost',
                       console=True):

    loader = DataLoader()
    variable_manager = VariableManager(loader=loader)
    variable_manager._extra_vars = extra_vars
    inventory = Inventory(loader=loader, sources=[inventory_src])
    variable_manager.set_inventory(inventory)
    passwords = {}
    context._init_global_context(options)

    pbex = PlaybookExecutor([playbook_path],
                            inventory,
                            variable_manager,
                            loader,
                            passwords)
    return pbex


def set_environment_vars(env_vars):
    """
    Sets environment variables passed
    : param env_vars: list of tuples
    """
    for tup in env_vars:
        os.environ[tup[0]] = tup[1]
    return True


def ansible_runner_shell(playbook_path,
                         module_path,
                         extra_vars,
                         vault_password_file=None,
                         inventory_src='localhost',
                         verbosity=1,
                         console=True,
                         env_vars=(),
                         check=False):
    # set verbosity to >=2
    # since -v in subprocess command fails
    if verbosity >= 2:
        verbosity = verbosity
    else:
        verbosity = 2

    # set the base command
    base_command = ["ansible-playbook"]
    # convert verbosity to -v
    verbosity = "v" * verbosity
    verbosity = "-" + verbosity

    # append inventory option to command
    # FIX ME ansible considers localhost as another machine
    if os.path.isfile(inventory_src) and\
       inventory_src.split("/")[-1] != 'localhost':
        base_command.append("--inventory")
        base_command.append(inventory_src)

    # Load vault password file
    if vault_password_file and os.path.isfile(vault_password_file):
        base_command.append("--vault-password-file")
        base_command.append(vault_password_file)

    # ask for a sudo password
    if extra_vars.get('ask_sudo_pass', None):
        base_command.append("--ask-become-pass")

    # enable checkmode if check mode is mentioned
    if check:
        base_command.append("-C")


    # extravars to be passed into ansible.

    if extra_vars:

        fd, tmp_file_path = tempfile.mkstemp()
        with os.fdopen(fd, 'w') as tmp:
            # write files to temp file
            tmp.write(json.dumps(extra_vars))
        # Clean up the temporary file yourself
        base_command.append("-e")
        base_command.append("@" + tmp_file_path)

    base_command.append(verbosity)
    base_command.append(playbook_path)
    return_code, stdout, stderr = subprocess_runner(base_command,
                                                    shell=console)
    return return_code, stdout, stderr


def ansible_runner(playbook_path,
                   module_path,
                   extra_vars,
                   vault_password_file,
                   inventory_src='localhost',
                   verbosity=2,
                   console=True,
                   env_vars=(),
                   use_shell=False):
    """
    Uses the Ansible API code to invoke the specified linchpin playbook
    :param playbook: Which ansible playbook to run (default: 'up')
    :param console: Whether to display the ansible console (default: True)
    """

    # sets environment variables for subsequent processes
    if env_vars:
        set_environment_vars(env_vars)

    # note: It may be advantageous to put the options into the context and pass
    # that onto this method down the road. The verbosity flag would just live
    # in options and we could set the defaults.

    if not use_shell:

        connect_type = 'ssh'
        if 'localhost' in inventory_src:
            extra_vars["ansible_python_interpreter"] = sys.executable
            connect_type = 'local'

        options = Options(connect_type, module_path, 100, False, 'sudo', 'root',
                          False, False, False, False, None, None, None, None,
                          None, None, None, verbosity, False, False,
                          [vault_password_file])

        if avr.ansibleverisgreaterthan(2.7):
            pbex = ansible_runner_28x(playbook_path,
                                      extra_vars,
                                      options,
                                      inventory_src=inventory_src,
                                      console=console)
        elif not avr.ansibleverisgreaterthan(2.8):
            pbex = ansible_runner_24x(playbook_path,
                                      extra_vars,
                                      options,
                                      inventory_src=inventory_src,
                                      console=console)

        # ansible should be >=2.6 to run this statement
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
    else:
        rc, stdout, stderr = ansible_runner_shell(playbook_path,
                                                  module_path,
                                                  extra_vars,
                                                  vault_password_file,
                                                  inventory_src=inventory_src,
                                                  verbosity=verbosity,
                                                  console=console)
        results = stdout
        return rc, results


# This is just a temporary class because python 2.7.5, the CentOS7 default,
# does not support the __dict__ keyword.  Once CentOS7 updates to a new version
# of python or we move to support CentOS8, we can delete this and move back to
# the (less messy) namedtuple or switch to the 3.7 DataClasses
class Options():
    def __init__(self, connection,
                 module_path,
                 forks, become, become_method, become_user, listhosts,
                 listtasks, listtags, syntax, remote_user, private_key_file,
                 ssh_common_args, ssh_extra_args, sftp_extra_args,
                 scp_extra_args, start_at_task, verbosity, check, diff,
                 vault_password_files):
        self.connection = connection
        self.module_path = module_path
        self.forks = forks
        self.become = become
        self.become_method = become_method
        self.become_user = become_user
        self.listhosts = listhosts
        self.listtasks = listtasks
        self.listtags = listtags
        self.syntax = syntax
        self.remote_user = remote_user
        self.private_key_file = private_key_file
        self.ssh_common_args = ssh_common_args
        self.ssh_extra_args = ssh_extra_args
        self.sftp_extra_args = sftp_extra_args
        self.scp_extra_args = scp_extra_args
        self.start_at_task = start_at_task
        self. verbosity = verbosity
        self.check = check
        self.diff = diff
        self.vault_password_files = vault_password_files
