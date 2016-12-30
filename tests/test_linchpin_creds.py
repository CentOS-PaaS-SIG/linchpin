import os
import sys
import json
import jsonschema
import yaml
import pdb
from a import A
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from nose import with_setup
from collections import namedtuple
from linchpin_utils import cred_utils
from jsonschema import validate


class TestLinchPinCredentials(object):
    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""

    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""
        pass

    def setUp(self):
        """This method is run once before _each_ test method is executed"""
        pass

    def test_linchpin_aws_creds(self):
        creds_path = os.path.realpath(__file__)
        path = "/provision/roles/aws/vars"
        creds_path = "/".join(creds_path.split("/")[0:-2]) + path
        aws_creds = []
        creds_path = os.walk(creds_path)
        for path, _, creds in creds_path:
            for f in creds:
                aws_creds.append(path+"/"+f)
                output = cred_utils.validate_creds(path+"/" + f, "aws")
                assert_equal(output, True)

    def test_linchpin_os_creds(self):
        creds_path = os.path.realpath(__file__)
        path = "/provision/roles/openstack/vars"
        creds_path = "/".join(creds_path.split("/")[0:-2]) + path
        aws_creds = []
        output = True
        creds_path = os.walk(creds_path)
        for path, _, creds in creds_path:
            for f in creds:
                aws_creds.append(path+"/"+f)
                output = cred_utils.validate_creds(path+"/" + f, "os")
                assert_equal(output, True)

    def test_linchpin_gcloud_creds(self):
        creds_path = os.path.realpath(__file__)
        path = "/provision/roles/gcloud/vars"
        creds_path = "/".join(creds_path.split("/")[0:-2]) + path
        gcloud_creds = []
        output = True
        creds_path = os.walk(creds_path)
        for path, _, creds in creds_path:
            for f in creds:
                if f.split(".")[-1] == "yml" or f.split(".")[-1] == "yaml":
                    gcloud_creds.append(path+"/"+f)
                    output = cred_utils.validate_creds(path+"/" + f, "gcloud")
                    assert_equal(output, True)
        assert_equal(output, True)

    def test_linchpin_duffy_creds(self):
        creds_path = os.path.realpath(__file__)
        path = "/provision/roles/duffy/vars"
        creds_path = "/".join(creds_path.split("/")[0:-2]) + path
        duffy_creds = []
        output = True
        creds_path = os.walk(creds_path)
        for path, _, creds in creds_path:
            for f in creds:
                if f.split(".")[-1] == "yml" or f.split(".")[-1] == "yaml":
                    duffy_creds.append(path+"/"+f)
                    output = cred_utils.validate_creds(path+"/" + f, "duffy")
                    assert_equal(output, True)
        assert_equal(output, True)

    def test_linchpin_rax_creds(self):
        creds_path = os.path.realpath(__file__)
        path = "/provision/roles/rackspace/vars"
        creds_path = "/".join(creds_path.split("/")[0:-2]) + path
        rax_creds = []
        output = True
        creds_path = os.walk(creds_path)
        for path, _, creds in creds_path:
            for f in creds:
                if f.split(".")[-1] == "yml" or f.split(".")[-1] == "yaml":
                    rax_creds.append(path+"/"+f)
                    output = cred_utils.validate_creds(path+"/" + f, "rax")
                    assert_equal(output, True)
        assert_equal(output, True)
