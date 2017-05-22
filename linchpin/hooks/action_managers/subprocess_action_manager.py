import os
import sys
import subprocess
from action_manager import ActionManager
from cerberus import Validator

from linchpin.exceptions import HookError


class SubprocessActionManager(ActionManager):

    def __init__(self, name, action_data, target_data, **kwargs):

        """
        SubprocessActionManager constructor
        :param name: Name of Action Manager , ( ie., shell)
        :param action_data: dictionary of action_block consists of set of actions
        example:
        - name: hookname
          type: shell
          actions:
            - echo " this is post down operation Hello hai how r u ?"
            - test.sh
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
        example:
        action_block :: sample ::
        - name: manipulate_inventory
          type: shell
          path: /tmp/shellscripts
          actions:
            - thisisshell.sh
        """
        schema= { 'name': { 
                           'type':'string',
                           'required': True
                          },
                  'type': { 
                           'type': 'string',
                           'allowed': ['shell', 'subprocess']
                          },
                  'path': {
                           'type': 'string',
                           'required': False
                          },
                  'context': {
                           'type': 'boolean',
                           'required': False
                           },
                  'actions': { 
                               'type': 'list',
                               'schema': {
                                          'type': 'string'
                                         },
                               'required': True
                             }
        }
        v = Validator(schema)
        status = v.validate(self.action_data)
        if not status:
            raise HookError("Invalid syntax: LinchpinHook:"+str((v.errors)))
        else:
            return status

    def load(self):
        
        """
        Adds the shell script to the os path if mentioned
        """

        # set os.environpath if exists
        if self.action_data.has_key("path"):
            os.environ["PATH"] += ":"+self.action_data["path"]

    def add_context_params(self, action):
        
        """
        Adds ctx params to the action_block run when context is true
        :param file_path: path to the script
        :param context: whether the context params are to be included or not
        """

        command = action
        for key in self.target_data:
            command += " %s=%s " %(key, self.target_data[key])
        return command

    def execute(self):
        
        """
        Executes the action_block in the PinFile
        """

        self.load()
        for action in self.action_data["actions"]:
            if self.context:
                command = self.add_context_params(action)
            else:
                command = action
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            proc.wait()
            for line in proc.stdout:
                print(line)
