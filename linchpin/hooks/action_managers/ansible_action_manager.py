import os
import yaml
import json

from cerberus import Validator

from linchpin.ansible_runner import ansible_runner
from linchpin.exceptions import HookError
from linchpin.hooks.action_managers.action_manager import ActionManager


class AnsibleActionManager(ActionManager):

    def __init__(self, name, action_data, target_data, **kwargs):

        """
        AnsibleActionManager constructor
        :param name: Name of Action Manager , ( ie., ansible)
        :param action_data: dictionary of action_block
        consists of set of actions
        example:
        - name: nameofthehook
          type: ansible
          actions:
            - playbook: test_playbook.yaml
              vars: test_var.yaml
              extra_vars: { "test_var": "postdowntask"}
        :param target_data: Target specific data defined in PinFile
        :param kwargs: anyother keyword args passed as metadata
        """

        self.name = name
        self.action_data = action_data
        self.target_data = target_data
        self.context = kwargs.get("context", True)
        self.kwargs = kwargs


    def validate(self):

        """
        Validates the action_block based on the cerberus schema
        example:: ansible_action_block::::
        - name: build_openshift_cluster
          type: ansible
          actions:
            - playbook: test_playbook.yaml
              vars: test_var.yaml
              extra_vars: { "testvar": "world"}
        """

        schema = {
            'name': {'type': 'string', 'required': True},
            'type': {'type': 'string', 'allowed': ['ansible']},
            'path': {'type': 'string', 'required': False},
            'context': {'type': 'boolean', 'required': False},
            'actions': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'playbook': {'type': 'string', 'required': True},
                        'vars': {'type': 'string', 'required': False},
                        'extra_vars': {'type': 'dict', 'required': False}
                    }
                },
                'required': True
            }
        }

        v = Validator(schema)
        status = v.validate(self.action_data)

        if not status:
            raise HookError("Invalid syntax: {0}".format((v.errors)))
        else:
            return status


    def load(self):

        """
        Loads the ansible specific managers and loaders
        """

    def get_ctx_params(self):

        """
        Reformats the ansible specific variables
        """

        ctx_params = {}
        ctx_params["resource_file"] = (
            self.target_data.get("resource_file", None))
        ctx_params["layout_file"] = self.target_data.get("layout_file", None)
        ctx_params["inventory_file"] = (
            self.target_data.get("inventory_file", None))

        return ctx_params


    def execute(self):

        """
        Executes the action_block in the PinFile
        """

        self.load()
        extra_vars = {}
        runners = []

        for action in self.action_data["actions"]:
            path = self.action_data["path"]
            playbook = action.get("playbook")

            if not(os.path.isfile(playbook)):
                playbook = "{0}/{1}".format(path, playbook)

            if "vars" in action:
                var_file = "{0}/{1}".format(path, action.get("vars"))
                ext = var_file.split(".")[-1]
                extra_vars = open(var_file, "r").read()

                if ("yaml" in ext) or ("yml" in ext):
                    extra_vars = yaml.load(extra_vars)
                else:
                    extra_vars = json.loads(extra_vars)

            e_vars = action.get("extra_vars", {})
            extra_vars.update(e_vars)
            verbosity = self.kwargs.get('verbosity', 1)

            if self.context:
                extra_vars.update(self.get_ctx_params())
            if 'inventory_file' in self.target_data and self.context:
                inv_file = self.target_data["inventory_file"]
                runners.append(ansible_runner(playbook,
                                              "",
                                              extra_vars,
                                              inventory_src=inv_file,
                                              verbosity=verbosity))
            else:
                runners.append(ansible_runner(playbook,
                                              "",
                                              extra_vars,
                                              inventory_src="localhost",
                                              verbosity=verbosity))
        return runners
