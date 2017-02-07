import os
import sys
import json
import pdb
from a import A
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from nose import with_setup
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

# patch for sys.exit
sys.exit = lambda *x: None

class TestLinchPinInvocation(object):
    @classmethod
    def setup(self):
        """This method is run once before _each_ test method is executed"""
        # contains all the intialisation required for linchpin
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.inventory = Inventory(loader=self.loader,
                                   variable_manager=self.variable_manager,
                                   host_list=['localhost'])
        self.playbook_path = 'playbooks/test_playbook.yml'
        self.Options = namedtuple('Options',
                                  ['listtags',
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

    @classmethod
    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    @with_setup(setup)
    def test_linchpin_invocation_without_param(self):
        """
        runs linchpin playbooks without any parameters
        """
        #ansible_path = "/".join(os.path.realpath(__file__).split("/")[0:-1])
        ansible_path = "/".join(os.path.realpath(__file__).split("/")[0:-2])
        #ansible_path = ansible_path + "/mockdata/ansible.cfg"
        #os.environ["ANSIBLE_CFG"] = ansible_path
        os.environ["ANSIBLE_LIBRARY"] = ansible_path
        path = os.path.realpath(__file__).split("/")[0:-2]
        path = "/".join(path)

        playbook_path = path + '/provision/site.yml'
        options = self.Options(listtags=False,
                               listtasks=False,
                               listhosts=False,
                               syntax=False,
                               connection='ssh',
                               module_path=None,
                               forks=100,
                               remote_user='root',
                               private_key_file=None,
                               ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None,
                               scp_extra_args=None,
                               become=True,
                               become_method=None,
                               become_user='root',
                               verbosity=3,
                               check=False)
        self.variable_manager.extra_vars = {'test_var': 'test_val'}
        pbex = PlaybookExecutor(playbooks=[playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=options,
                                passwords={})
        results = pbex.run()
        #del os.environ["ANSIBLE_CFG"]
        del os.environ["ANSIBLE_LIBRARY"]
        assert_equal(results, 2)
