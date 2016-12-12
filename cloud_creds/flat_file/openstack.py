import utils
import yaml
from defaults import *

class Openstack:
    def __init__(self):
        pass

    def get_creds(self, path, name, profile=None):
        # resolves by name
        cred = {}
        for file_path in utils.list_files(path):
            if name == file_path.split("/")[-1].strip(".yaml").strip(".yml"):
                creds = open(file_path,"r").read()
                creds = yaml.load(creds)
                if profile in creds["clouds"]:
                    cred = creds["clouds"][profile]
        return cred

        #for file_path in utils.list_files(path):
        #    if name == file_path.split("/")[-1].strip(".yml").strip(".yaml"):
        #        return file_path
        # if not found by name searches each profile in the file
 
    def get_default_creds(self):
        #export OS_USERNAME=username
        #export OS_PASSWORD=password
        #export OS_TENANT_NAME=projectName
        #export OS_AUTH_URL=https://identityHost:portNumber/v2.0
        ENV_VARS = ["OS_USERNAME", "OS_PASSWORD", "OS_TENANT_NAME", "OS_AUTH_URL"]
        creds = { }
        for var in ENV_VARS:
            creds[var] = os.getenv(key,False)
        if False in creds.values():
            return None
        return creds
