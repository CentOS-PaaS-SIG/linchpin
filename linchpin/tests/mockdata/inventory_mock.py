import json
import os
import yaml


dir_path = os.path.dirname(os.path.realpath(__file__))


def get_mock_topo_output():
    return json.loads(open(dir_path+"/ex_all_output.json", "r").read())

def get_mock_layout():
    return json.loads(open(dir_path+"/test_layout.json", "r").read())

def get_mock_pf():
    return yaml.load(open(dir_path+"/PinFile", "r").read())

def get_mock_pf_path():
    return dir_path+"/PinFile"

def get_mock_outputfile():
    return dir_path+"/ex_all_output.json"

def get_mock_layoutfile():
    return dir_path+"/openshift-3node-cluster.yml"
