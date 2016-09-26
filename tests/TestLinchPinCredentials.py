import os
import sys
import json
import jsonschema
import yaml
from jsonschema import validate
import pdb
from a import A
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises
from nose import with_setup 
from collections import namedtuple

def get_cred_schema(cred_type):
    aws_cred_schema = {
        "type" : "object",
        "properties" : {
           "aws_access_key_id" : {"type" : "string"},
           "aws_secret_access_key" : {"type" : "string"},
        },
        "required": [ "aws_access_key_id", "aws_secret_access_key" ]
    }
    os_cred_schema = {
        "type" : "object",
        "properties" : {
           "endpoint" : {"type" : "string"},
           "project" : {"type" : "string"},
           "username" : {"type" : "string"},
           "password" : {"type" : "string"},
        },
        "required": [ "endpoint", "project","username","password"]
    }
    gcloud_cred_schema = {
        "type" : "object",
        "properties" : {
           "aws_access_key_id" : {"type" : "string"},
           "aws_secret_access_key" : {"type" : "string"},
        },
    }
    duffy_cred_schema = {
        "type" : "object",
        "properties" : {
           "key_path" : {"type" : "string"},
           "url_base" : {"type" : "string"},
        },
    }
    rx_cred_schema = {
        "type" : "object",
        "properties" : {
           "username" : {"type" : "string"},
           "api_key" : {"type" : "string"},
        },
    }
    cred_schemas = {
       "aws": aws_cred_schema,
       "os": os_cred_schema,
       "gcloud": gcloud_cred_schema,
       "duffy": duffy_cred_schema,
       "rax": rx_cred_schema
    }
    return cred_schemas[cred_type]

def validate_creds(cred_path, cred_type):
    schema = get_cred_schema(cred_type)
    cred_str = open(cred_path).read()
    cred_json = yaml.load(cred_str)
    try:
        validate(cred_json,schema)
        return True
    except:
        return False

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
        creds_path = "/".join(creds_path.split("/")[0:-2])+"/provision/roles/aws/vars"
        aws_creds = []
        creds_path = os.walk(creds_path)
        for path,_,creds in creds_path:
            for f in creds:
                aws_creds.append(path+"/"+f)
                output = validate_creds(path+"/"+f,"aws")
                assert_equal(output,True)

    def test_linchpin_os_creds(self):
        creds_path = os.path.realpath(__file__)
        creds_path = "/".join(creds_path.split("/")[0:-2])+"/provision/roles/openstack/vars"
        aws_creds = []
        output = True
        creds_path = os.walk(creds_path)
        for path,_,creds in creds_path:
            for f in creds:
                aws_creds.append(path+"/"+f)
                output = validate_creds(path+"/"+f,"os")
                assert_equal(output,True)

    def test_linchpin_gcloud_creds(self):
        creds_path = os.path.realpath(__file__)
        creds_path = "/".join(creds_path.split("/")[0:-2])+"/provision/roles/openstack/vars"
        gcloud_creds = []
        output = True
        creds_path = os.walk(creds_path)
        for path,_,creds in creds_path:
            for f in creds:
                if f.split(".")[-1] == "yml" or  f.split(".")[-1] == "yaml":
                    gcloud_creds.append(path+"/"+f)
                    output = validate_creds(path+"/"+f,"gcloud")
                    assert_equal(output,True)
        assert_equal(output,True)
   
    def test_linchpin_duffy_creds(self):
        creds_path = os.path.realpath(__file__)
        creds_path = "/".join(creds_path.split("/")[0:-2])+"/provision/roles/duffy/vars"
        duffy_creds = []
        output = True
        creds_path = os.walk(creds_path)
        for path,_,creds in creds_path:
            for f in creds:
                if f.split(".")[-1] == "yml" or  f.split(".")[-1] == "yaml":
                    duffy_creds.append(path+"/"+f)
                    output = validate_creds(path+"/"+f,"gcloud")
                    assert_equal(output,True)
        assert_equal(output,True)

    def test_linchpin_rax_creds(self):
        creds_path = os.path.realpath(__file__)
        creds_path = "/".join(creds_path.split("/")[0:-2])+"/provision/roles/rackspace/vars"
        rax_creds = []
        output = True
        creds_path = os.walk(creds_path)
        for path,_,creds in creds_path:
            for f in creds:
                if f.split(".")[-1] == "yml" or  f.split(".")[-1] == "yaml":
                    rax_creds.append(path+"/"+f)
                    output = validate_creds(path+"/"+f,"rax")
                    assert_equal(output,True)
        assert_equal(output,True)
