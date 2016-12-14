import os
import sys
import json
import tempfile
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
from linchpin_utils.module_utils import run_module
from linchpin_utils.module_utils import boilerplate_module


class TestLinchPinModuleOutputParser(object):
    @classmethod
    def setup(self):
        """This method is run once before _each_ test method is executed"""
        self.options = {}
        filepath = os.path.realpath(__file__)
        filepath = "/".join(filepath.split("/")[0:-2])
        self.options["module_path"] = filepath + "/library/output_parser.py"
        self.options["module_args"] = '{}'
        self.options["interpretor"] = 'python={0}'.format(sys.executable)
        self.options["check"] = None
        self.options["filename"] = '~/.ansible_module_generated'

    @classmethod
    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    @with_setup(setup)
    def test_module_empty_params(self):
        """
        tests module with no parameters
        """
        invalid_params = {}
        self.options["module_args"] = json.dumps(invalid_params)
        results = run_module(self.options)
        msg = "missing required arguments"
        output = results['failed'] and msg in results["msg"]
        assert_equal(output, True)

    @with_setup(setup)
    def test_module_unsupported_params(self):
        """
        tests module with unsupported parameters
        """
        invalid_params = {"test": "params"}
        self.options["module_args"] = json.dumps(invalid_params)
        results = run_module(self.options)
        msg = "unsupported parameter for module"
        output = results['failed'] and msg in results["msg"]
        assert_equal(output, True)

    @with_setup(setup)
    def test_module_dir_params(self):
        """
        tests module with dir params
        """
        dir_name = tempfile.mkdtemp()
        invalid_params = {"output_file": dir_name}
        self.options["module_args"] = json.dumps(invalid_params)
        results = run_module(self.options)
        msg = "Recursive directory not supported"
        output = results['failed'] and msg in results["msg"]
        os.removedirs(dir_name)
        assert_equal(output, True)

    @with_setup(setup)
    def test_module_empty_file(self):
        """
        tests module with empty file
        """
        tf = tempfile.NamedTemporaryFile(delete=False)
        invalid_params = {"output_file": tf.name}
        self.options["module_args"] = json.dumps(invalid_params)
        results = run_module(self.options)
        output = results['failed'] and results["msg"]["content"] is None
        tf.close()
        os.unlink(tf.name)
        assert_equal(output, True)

    @with_setup(setup)
    def test_module_yaml_file(self):
        """
        tests module with yaml file
        """
        tf = tempfile.NamedTemporaryFile(delete=False)
        tf.write("testkey: testval")
        tf_name = tf.name
        tf.close()
        invalid_params = {"output_file": tf_name}
        self.options["module_args"] = json.dumps(invalid_params)
        results = run_module(self.options)
        output = results['changed']
        os.remove(tf_name)
        assert_equal(output, True)
