from linchpin import LinchpinAPI
from linchpin.context import LinchpinContext
import yaml
import json
import os
import tempfile
import shutil


class Workspace:

    def __init__(self,
                 path=None):

        self.workspace_path = path
        self.context = LinchpinContext()
        self.context.setup_logging()
        self.context.load_config(workspace=path)
        self.context.load_global_evars()
        self.pindict = {}
        # check where the workspace is being created
        self.context.set_cfg('lp', 'workspace', self.workspace_path)
        self.context.set_evar('workspace', self.workspace_path)
        self.context.set_evar('debug_mode', True)

    def load_data(self, path):

        self.pindict = yaml.load(open(path).read())
        return self.pindict

    def validate(self):

        linchpin_api = LinchpinAPI(self.context)
        self.load_data(self.find_pinfile())
        output = linchpin_api.do_validation(self.pindict)
        return output

    def find_pinfile(self):

        PF_NAMES = ["Pinfile", "PinFile", "PinFile.json"]
        for name in PF_NAMES:
            if os.path.isfile(self.workspace_path+"/"+name):
                return self.workspace_path+"/"+name
        return False

    def set_workspace(self, path):

        self.workspace_path = path
        self.context.set_cfg('lp', 'workspace', self.workspace_path )
        self.context.set_evar('workspace', self.workspace_path)
        return self.workspace_path

    def get_workspace(self):

        return self.workspace_path

    def set_evar(self, key, value):

        self.context.set_evar(key, value)
        return key,value

    def get_evar(self, key):

        return self.context.get_evar(key)

    def set_credentials_path(self, creds_path):

        if os.path.isdir(creds_path):
            return self.context.set_evar("default_credentials_path",
                                         creds_path)
        raise LinchpinError("Incorrect file path, path should be a directory")

    def get_credentials_path(self):

        return self.context.get_evar("default_credentials_path")

    def set_vault_encryption(self, vault_enc):

        if isinstance(vault_enc, bool):
            return self.context.set_evar("vault_encryption",vault_enc)
        raise LinchpinError("Incorrect datatype please use boolean")

    def get_vault_encryption(self):

        return self.context.get_evar("vault_encryption")

    def set_flag_no_hooks(self, flag):

        if isinstance(flag, bool):
            return self.context.set_cfg("hookflags", "no_hooks", flag)
        raise LinchpinError("Incorrect datatype please use boolean")

    def get_flag_no_hooks(self):

        return self.context.get_cfg("hookflags", "no_hooks")

    def set_flag_ignore_failed_hooks(self, flag):

        if isinstance(flag, bool):
            return self.context.set_cfg("hookflags", "ignore_failed_hooks", flag)
        raise LinchpinError("Incorrect datatype please use boolean")

    def get_flag_ignore_failed_hooks(self):

        return self.context.get_cfg("hookflags", "ignore_failed_hooks")

    def set_vault_pass(self, vault_pass):

        return self.context.set_evar("vault_password",vault_pass)

    def get_vault_pass(self):

        return self.context.get_evar("vault_password")    

    def get_inventory(self, inv_format="json"):

        lapi = LinchpinAPI(self.context)
        latest_run_data = lapi._get_run_data_by_txid()
        inventory_data = lapi._write_to_inventory(inv_format=inv_format)
        return inventory_data

    def get_latest_run(self):

        lapi = LinchpinAPI(self.context)
        latest_run_data = lapi._get_run_data_by_txid()
        return latest_run_data

    def set_cfg(self, section, key, value):

        return self.context.set_cfg(section, key, value)

    def get_cfg(self, section, key):

        return self.context.set_cfg(section, key)

    def up(self):

        lapi = LinchpinAPI(self.context)
        file_path = self.find_pinfile()
        self.load_data(file_path)
        output = lapi.do_action(self.pindict, action='up')
        return output

    def destroy(self):

        lapi = LinchpinAPI(self.context)
        self.load_data(self.find_pinfile())
        output = lapi.do_action(self.pindict, action='destroy')
        return output


class Pinfile(Workspace):

    def __init__(self,
                 pinfile={},
                 config="linchpin.conf",
                 workspace_path=None):
        # check where the linchpin.conf is written
        # check the data_type of the content if its
        # file_path load it 
        
        # if workspace is not provided
        if workspace_path:
            self.workspace_path= workspace_path
        else:
            self.workspace_path= tempfile.mkdtemp()
        # generate a workspace name based on Pinfile_contents
        # write contents to workspace
        open(self.workspace_path+"/PinFile","w").write(json.dumps(pinfile))
        self.pinfile = pinfile
        self.config = config
        self.context = LinchpinContext()
        self.context.setup_logging()
        self.context.load_config(workspace=self.workspace_path)
        self.context.load_global_evars()
        # check where the workspace is being created
        self.context.set_cfg('lp', 'workspace', self.workspace_path)
        self.context.set_evar('workspace', self.workspace_path)
        self.context.set_evar('debug_mode', True)

    def up(self):
        lapi = LinchpinAPI(self.context)
        output = lapi.do_action(self.pinfile, action='up')
        return output

    def destroy(self):
        lapi = LinchpinAPI(self.context)
        output = lapi.do_action(self.pinfile, action='destroy')
        return output
