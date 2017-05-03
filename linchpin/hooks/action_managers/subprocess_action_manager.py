import os
import sys
import subprocess
from action_manager import ActionManager
from cerberus import Validator

from linchpin.exceptions import HookError


class SubprocessActionManager(ActionManager):

    def __init__(self, name, action_data, target_data, **kwargs):

        self.name = name
        self.action_data = action_data
        self.target_data = target_data
        self.context = kwargs.get('context', True)
        self.kwargs = kwargs

    def validate(self):

        """
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

        # set os.environpath if exists
        if self.action_data.has_key("path"):
            os.environ["PATH"] += ":"+self.action_data["path"]

    def add_context_params(self, action):

        command = action
        for key in self.target_data:
            command += " %s=%s " %(key, self.target_data[key])
        return command

    def execute(self):

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
