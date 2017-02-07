import os
import sys
import json
import pdb
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


class TestLinchPinInventoryGen(object):
    @classmethod
    def setup(self):
        """This method is run once before _each_ test method is executed"""
        # contains all the intialisation required for linchpin
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.inventory = Inventory(loader=self.loader,
                                   variable_manager=self.variable_manager,
                                   host_list=['localhost'])
        base_path = os.path.realpath(__file__)
        base_path = "/".join(base_path.split("/")[0:-2])
        playbook_path = base_path+"/tests/playbooks/test_inventory.yml"
        self.playbook_path = playbook_path
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
        self.options = self.Options(listtags=False,
                                    listtasks=False,
                                    listhosts=False,
                                    syntax=False,
                                    connection='ssh',
                                    module_path=None,
                                    forks=100, remote_user='root',
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
        filepath = os.path.realpath(__file__)
        filepath = "/".join(filepath.split("/")[0:-2]) + "/filter_plugins"
        sys.path.append(filepath)

    @classmethod
    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    @with_setup(setup)
    def test_inventory_aws(self):
        """
        generates inventory for aws on testdata
        """
        self.variable_manager.extra_vars = {'inventory_type': 'aws'}
        pbex = PlaybookExecutor(playbooks=[self.playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords={})
        results = pbex.run()
        assert_equal(results, 0)

    @with_setup(setup)
    def test_inventory_gcloud(self):
        """
        generates inventory for gcloud on testdata
        """
        self.variable_manager.extra_vars = {'inventory_type': 'gcloud'}
        pbex = PlaybookExecutor(playbooks=[self.playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords={})
        results = pbex.run()
        assert_equal(results, 0)
    """
    # unit test needs to be updated
    @with_setup(setup)
    def test_inventory_os(self):
        self.variable_manager.extra_vars = {'inventory_type': 'os'}
        pbex = PlaybookExecutor(playbooks=[self.playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords={})
        results = pbex.run()
        assert_equal(results, 0)
    """
    """
    #unit test needs to be updated 
    @with_setup(setup)
    def test_inventory_generic(self):
        self.variable_manager.extra_vars = {'inventory_type': 'generic'}
        pbex = PlaybookExecutor(playbooks=[self.playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords={})
        results = pbex.run()
        assert_equal(results, 0)
    """
    @with_setup(setup)
    def test_inventory_duffy(self):
        """
        generates inventory for duffy type on testdata
        """
        self.variable_manager.extra_vars = {'inventory_type': 'duffy'}
        pbex = PlaybookExecutor(playbooks=[self.playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords={})
        results = pbex.run()
        assert_equal(results, 2)

    @with_setup(setup)
    def test_inventory_other(self):
        """
        generates inventory for not supported type on testdata
        """
        self.variable_manager.extra_vars = {'inventory_type': 'dummy'}
        pbex = PlaybookExecutor(playbooks=[self.playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords={})
        results = pbex.run()
        assert_equal(results, 2)
