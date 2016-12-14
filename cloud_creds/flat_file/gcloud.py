import utils
import json
from defaults import *


class GCloud:
    def __init__(self):
        pass

    def get_creds(self, path, name, profile=None):
        # resolves by file name
        for file_path in utils.list_files(path):
            if name == file_path.split("/")[-1].split(".")[0]:
                creds = open(file_path, "r").read()
                creds = json.loads(creds)
                creds["file_path"] = file_path
                return creds

    def get_default_creds(self):
        pass
