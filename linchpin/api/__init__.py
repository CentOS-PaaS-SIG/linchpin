from linchpin import LinchpinAPI
from linchpin.context import LinchpinContext
from linchpin.exceptions import LinchpinError
import yaml
import json
import os
import tempfile


class Workspace(object):

    def __init__(self,
                 path=None):

        """
        Linchpin api workspace constructor

        :param path: path to workspace directory
        """

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
        self.context.set_evar('auth_debug', True)

    def load_data(self, path):
        """
        load_data function to load from workspace path

        :param path: path to workspace directory
        """

        self.pindict = yaml.load(open(path).read())
        return self.pindict

    def validate(self):
        """
        validate function to validate loaded workspace/pinfile

        """

        linchpin_api = LinchpinAPI(self.context)
        self.load_data(self.find_pinfile())
        output = linchpin_api.do_validation(self.pindict)
        return output

    def find_pinfile(self):
        """
        find_pinfile function to search pinfiles in workspace path
        returns pinfile path if found

        """

        PF_NAMES = ["Pinfile", "PinFile", "PinFile.json"]
        for name in PF_NAMES:
            if os.path.isfile(self.workspace_path + "/" + name):
                return self.workspace_path + "/" + name
        return False

    def set_workspace(self, path):
        """
        set_workspace function sets workspace path

        :param path: path to workspace directory

        returns workspace path if set
        """

        self.workspace_path = path
        self.context.set_cfg('lp', 'workspace', self.workspace_path)
        self.context.set_evar('workspace', self.workspace_path)
        return self.workspace_path

    def get_workspace(self):
        """
        get_workspace function gets current workspace path

        :param path: path to workspace directory

        returns workspace path if set
        """


        return self.workspace_path

    def set_evar(self, key, value):
        """
        set_evar function sets extra vars in current run

        :param key: string
        :param value: string


        returns key,value tuple
        """

        self.context.set_evar(key, value)
        return key, value

    def get_evar(self, key):
        """
        get_evar function sets extra vars in current run

        :param key: string


        returns value for corresponding key
        """

        return self.context.get_evar(key)

    def set_credentials_path(self, creds_path):
        """
        set_credentials_path function set credentials path

        :param creds_path: path to credential directory

        returns True/False
        """

        if os.path.isdir(creds_path):
            return self.context.set_evar("default_credentials_path",
                                         creds_path)
        raise LinchpinError("Incorrect file path, path should be a directory")

    def get_credentials_path(self):
        """
        get_credentials_path function gets current credentials path

        returns path to credential file
        """

        return self.context.get_evar("default_credentials_path")

    def set_vault_encryption(self, vault_enc):
        """
        set_vault_encryption sets vault_encryption flag
        if credentials are encrypted in vault current credentials path

        param: vault_enc: boolean

        returns boolean
        """

        if isinstance(vault_enc, bool):
            return self.context.set_evar("vault_encryption", vault_enc)
        raise LinchpinError("Incorrect datatype please use boolean")

    def get_vault_encryption(self):
        """
        get_vault_encryption gets current vault_encryption flag value

        returns boolean
        """

        return self.context.get_evar("vault_encryption")

    def set_flag_no_hooks(self, flag):
        """
        set_flag_no_hooks sets no_hooks flag

        param: flag: boolean

        returns boolean
        """

        if isinstance(flag, bool):
            return self.context.set_cfg("hookflags", "no_hooks", flag)
        raise LinchpinError("Incorrect datatype please use boolean")

    def get_flag_no_hooks(self):
        """
        get_flag_no_hooks gets current vault_encryption flag value

        returns boolean
        """

        return self.context.get_cfg("hookflags", "no_hooks")

    def set_flag_ignore_failed_hooks(self, flag):
        """
        set_flag_ignore_failed_hooks sets current ignore_failed_hooks flag value

        param: flag: boolean

        """

        if isinstance(flag, bool):
            return self.context.set_cfg("hookflags",
                                        "ignore_failed_hooks",
                                        flag)
        raise LinchpinError("Incorrect datatype please use boolean")

    def get_flag_ignore_failed_hooks(self):
        """
        get_flag_ignore_failed_hooks get current ignore_failed_hooks flag value

        returns boolean

        """

        return self.context.get_cfg("hookflags", "ignore_failed_hooks")

    def set_vault_pass(self, vault_pass):
        """
        set_vault_pass set current vault_pass value

        param: vault_pass: string
        returns boolean

        """

        return self.context.set_evar("vault_password", vault_pass)

    def get_vault_pass(self):
        """
        get_valut_pass get current valut_password set

        returns boolean

        """

        return self.context.get_evar("vault_password")

    def get_inventory(self, inv_format="json"):
        """
        get_inventory gets inventory of latest run

        param: inv_format: string json/ini

        returns dict/string

        """

        lapi = LinchpinAPI(self.context)
        inventory_data = lapi._write_to_inventory(inv_format=inv_format)
        return inventory_data

    def get_latest_run(self):
        """
        get_latest_run get latest resources provisioned

        returns dict

        """

        lapi = LinchpinAPI(self.context)
        latest_run_data = lapi._get_run_data_by_txid()
        return latest_run_data

    def set_cfg(self, section, key, value):
        """
        get_flag_ignore_failed_hooks get current ignore_failed_hooks flag value

        returns boolean

        """

        return self.context.set_cfg(section, key, value)

    def get_cfg(self, section, key):
        """
        get_cfg gets current linchpin.conf values based on section, key

        returns string

        """

        return self.context.set_cfg(section, key)

    def up(self):
        """
        provisions workspace resources constructed through the workspace object

        returns output dictionary

        """

        lapi = LinchpinAPI(self.context)
        file_path = self.find_pinfile()
        self.load_data(file_path)
        output = lapi.do_action(self.pindict, action='up')
        return output

    def destroy(self):
        """
        Destroys workspace resources constructed through the workspace object

        returns output dictionary

        """

        lapi = LinchpinAPI(self.context)
        self.load_data(self.find_pinfile())
        output = lapi.do_action(self.pindict, action='destroy')
        return output


class Pinfile(Workspace):

    def __init__(self,
                 pinfile={},
                 config="linchpin.conf",
                 workspace_path=None):

        """
        Linchpin api Pinfile constructor

        :param pinfile: dictionary object of pinfile
        :param config: configuration path to linchpin.conf, defaults to
                       current working directory
        :param workspace_path: path to workspace directory. if not provided
                               workspace would be generated in /tmp/
        """

        # if workspace is not provided
        if workspace_path:
            self.workspace_path = workspace_path
        else:
            self.workspace_path = tempfile.mkdtemp()
        # generate a workspace name based on Pinfile_contents
        # write contents to workspace
        open(self.workspace_path + "/PinFile", "w").write(json.dumps(pinfile))
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
        self.context.set_evar('auth_debug', True)

    def up(self):
        """
        provsions pinfile resources constructed through the Pinfile object

        returns output dictionary
        """
        lapi = LinchpinAPI(self.context)
        output = lapi.do_action(self.pinfile, action='up')
        return output

    def destroy(self):
        """
        Destroys pinfile resources constructed through the Pinfile object

        returns output dictionary

        """

        lapi = LinchpinAPI(self.context)
        output = lapi.do_action(self.pinfile, action='destroy')
        return output
