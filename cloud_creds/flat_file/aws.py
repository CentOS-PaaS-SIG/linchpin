import utils
import os
from defaults import *

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser


class AWS:
    def __init__(self):
        pass

    def get_creds(self, path, name, profile=None):
        # resolves by name
        cred = {}
        for file_path in utils.list_files(path):
            if name == file_path.split("/")[-1].strip(".ini"):
                parser = ConfigParser()
                parser.read(file_path)
                secs = parser.sections()
                confdict = {section: dict(parser.items(sec)) for sec in secs}
                if (profile is None) and ("default" in confdict):
                    cred = confdict["default"]
                if profile in confdict:
                    cred = confdict[profile]
        return cred

    def get_default_creds(self):
        # /etc/boto.cfg - for site-wide settings
        # that all users on this machine will use
        # (if profile is given) ~/.aws/credentials -
        #    for credentials shared between SDKs
        # (if profile is given) ~/.boto - for user-specific settings
        # ~/.aws/credentials - for credentials shared between SDKs
        # ~/.boto - for user-specific settings
        cred_paths = ["~/.boto", "~/.aws/credentials", "/etc/boto.cfg"]
        for path in AWS_DEFAULT_PATHS:
            if os.path.exists(path):
                parser = ConfigParser()
                parser.read(file_path)
                secs = parser.sections()
                confdict = {section: dict(parser.items(sec)) for sec in secs}
                return confdict
        # AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY or EC2_ACCESS_KEY
        # AWS_SECRET_ACCESS_KEY, AWS_SECRET_KEY, or EC2_SECRET_KEY
        access_key_defaults = ["AWS_ACCESS_KEY_ID",
                               "AWS_ACCESS_KEY",
                               "EC2_ACCESS_KEY"]
        secret_defaults = ["AWS_SECRET_ACCESS_KEY",
                           "AWS_SECRET_KEY",
                           "EC2_SECRET_KEY"]
        access_id = ""
        secret = ""
        for key in access_key_defaults:
            accessid = os.getenv(key, False)
            if access_id:
                break
        for key in secret_defaults:
            secret = os.getenv(key, False)
            if secret:
                break
        creds = {
                  "aws_access_key_id": access_id,
                  "aws_secret_access_key": secret
                }
        return creds
