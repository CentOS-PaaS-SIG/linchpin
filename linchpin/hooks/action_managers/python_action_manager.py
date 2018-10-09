from .action_manager import ActionManager
import sys
import subprocess
from cerberus import Validator

from linchpin.exceptions import HookError


class PythonActionManager(ActionManager):

    def __init__(self, name, action_data, target_data, **kwargs):

        """
        PythonActionManager constructor
        :param name: Name of Action Manager , ( ie., python)
        :param action_data: dictionary of action_block
        consists of set of actions
        example:
        - name: nameofhook
          type: python
          context: true
          actions:
            - test.py
        :param target_data: Target specific data defined in PinFile
        :param kwargs: anyother keyword args passed as metadata
        """

        self.name = name
        self.action_data = action_data
        self.target_data = target_data
        self.context = kwargs.get('context', True)
        self.kwargs = kwargs


    def validate(self):

        """
        Validates the action_block based on the cerberus schema
        """

        schema = {
            'name': {'type': 'string', 'required': True},
            'type': {'type': 'string', 'allowed': ['python']},
            'path': {'type': 'string', 'required': False},
            'context': {'type': 'boolean', 'required': False},
            'actions': {
                'type': 'list',
                'schema': {'type': 'string'},
                'required': True
            }
        }
        v = Validator(schema)
        status = v.validate(self.action_data)
        if not status:
            raise HookError("Invalid syntax: {0}".format(+str((v.errors))))
        else:
            return status


    def add_ctx_params(self, file_path, context=True):

        """
        Adds ctx params to the action_block run when context is true
        :param file_path: path to the script
        :param context: whether the context params are to be included or not
        """

        if not context:
            return "{0} {1}".format(sys.executable,
                                    file_path)
        params = ""
        for key in self.target_data:
            params += " {0}={1} ".format(key, self.target_data[key])
        return "{0} {1} {2}".format(sys.executable,
                                    file_path,
                                    params)


    def execute(self):

        """
        Executes the action_block in the PinFile
        """

        for action in self.action_data["actions"]:
            context = self.action_data.get("context", True)
            path = self.action_data["path"]
            file_path = "{0}/{1}".format(path, action)
            command = self.add_ctx_params(file_path, context)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            proc.wait()

            for line in proc.stdout:
                print(line)
