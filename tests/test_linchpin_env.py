import os
import sys
import json
import pdb
import ansible
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


class TestLinchPinEnv(object):
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
        pass

    @with_setup(setup)
    def test_ansible_version(self):
        """
        Checks for the version of ansible installed
        """
        version = float(ansible.__version__[0:3]) >= 2.1
        assert_equal(version, True)

    @with_setup(setup)
    def test_libcloud_version(self):
        """
        Checks for the version of libcloud installed
        """
        import libcloud
        version = float(libcloud.__version__[0:3]) >= 0.20
        assert_equal(version, True)

    @with_setup(setup)
    def test_jsonschema_version(self):
        """
        Checks for the version of json installed
        """
        import jsonschema
        version = float(jsonschema.__version__[0:3]) >= 2.5
        assert_equal(version, True)

    @with_setup(setup)
    def test_boto_version(self):
        """
        Checks for the version of boto installed
        """
        import boto
        version = float(boto.__version__[0:3]) >= 2.4
        assert_equal(version, True)

    @with_setup(setup)
    def test_init(self):
        """
        Initialises and runs sample echo playbook for testing
        """
        path = os.path.realpath(__file__).split("/")[0:-1]
        path = "/".join(path)
        playbook_path = path+'/playbooks/test_playbook.yml'
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
        self.variable_manager.extra_vars = {'hosts': 'mywebserver'}
        passwords = {}
        pbex = PlaybookExecutor(playbooks=[playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=options,
                                passwords=passwords)
        results = pbex.run()
        assert_equal(results, 0)
