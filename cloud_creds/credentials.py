import flat_file
import pdb

from flat_file import aws, openstack, gcloud, example

cred_functions = {
    "aws" : aws.AWS,
    "openstack" : openstack.Openstack,
    "gcloud" : gcloud.GCloud,
    "example" : example.Example,
}

def get_creds(cred_type, cred_store, cred_name, profile=None):
    #cred = cred_functions[cred_type](cred_store, cred_name)
    cred = cred_functions[cred_type]().get_creds(cred_store+"/"+cred_type, cred_name, profile)
    #return {"hello":"this is nothing"}
    return cred

def get_default_creds(cred_type, cred_store, cred_name):
    cred = cred_functions[cred_type](cred_store, cred_name, True)
