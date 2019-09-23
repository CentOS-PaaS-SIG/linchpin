from __future__ import absolute_import
import json
from .action_manager import ActionManager
from Naked.toolshed.shell import run_rb
from cerberus import Validator

from linchpin.exceptions import HookError


class RubyActionManager(ActionManager):

    def __init__(self, name, action_data, target_data, state, **kwargs):

        """
        RubyActionManager constructor
        :param name: Name of Action Manager , ( ie., ruby)
        :param action_data: dictionary of action_block consists of
        a set of actions
        example:
        - name: nameofhook
          type: ruby
          context: true
          actions:
            - test.js
        :param target_data: Target specific data defined in PinFile
        :param kwargs: anyother keyword args passed as metadata
        """

        self.name = name
        self.action_data = action_data
        self.target_data = target_data
        self.context = kwargs.get('context', True)
        self.state = state
        self.kwargs = kwargs


    def validate(self):

        """
        Validates the action_block based on the cerberus schema
        """

        schema = {
            'name': {'type': 'string', 'required': True},
            'type': {'type': 'string', 'allowed': ['ruby']},
            'path': {'type': 'string', 'required': False},
            'context': {'type': 'boolean', 'required': False},
            'vault_password_file': {'type': 'string', 'required': False},
            'src': {
                'type': 'dict',
                'schema': {
                    'type': {'type': 'string', 'required': True},
                    'url': {'type': 'string', 'required': True}
                }
            },
            'actions': {
                'type': 'list',
                'schema': {'type': 'string'},
                'required': True
            }
        }

        v = Validator(schema)
        status = v.validate(self.action_data)

        if not status:
            raise HookError("Invalid syntax: {0}".format(str((v.errors))))
        else:
            return status


    def add_ctx_params(self, file_path, context=True):

        """
        Adds ctx params to the action_block run when context is true
        :param file_path: path to the script
        :param context: whether the context params are to be included or not
        """

        if not context:
            return file_path

        params = file_path
        for key in self.target_data:
            params += " {0}={1} ".format(key, self.target_data[key])

        return "{0} {1}".format(file_path, params)


    def execute(self, results):

        """
        Executes the action_block in the PinFile
        """

        for action in self.action_data["actions"]:
            result = {}

            res_str = json.dumps(results, separators=(',', ':'))
            context = self.action_data.get("context", True)
            path = self.action_data["path"]
            file_path = "{0}/{1}".format(
                        path,
                        action
            )

            command = self.add_ctx_params(file_path, context)
            run_data = run_rb(command, arguments=res_str)

            print(run_data.stdout)

            data = run_data.stderr
            try:
                if data:
                    result['data'] = json.loads(data)
            except ValueError:
                print("Warning: '{0}' is not a valid JSON object.  "
                      "Data from this hook will be discarded".format(data))

            result['return_code'] = run_data.exitcode
            result['state'] = str(self.state)
            results.append(result)

        return results
