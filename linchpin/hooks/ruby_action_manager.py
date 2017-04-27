from action_manager import ActionManager
from Naked.toolshed.shell import run_rb
from cerberus import Validator


class RubyActionManager(ActionManager):

    def __init__(self, name, action_data, target_data, **kwargs):

        self.name = name
        self.action_data = action_data
        self.target_data = target_data
        self.context = kwargs.get('context', True)
        self.kwargs = kwargs

    def validate(self):

        schema= {
        'name': {'type': 'string', 'required': True },
        'type': { 'type': 'string', 'allowed': ['ruby']},
        'path': {'type': 'string', 'required': False},
        'context': {'type': 'boolean', 'required': False},
        'actions': {
                     'type': 'list',
                     'schema': {'type':'string'},
                     'required': True
                   }
        }
        v = Validator(schema)
        status = v.validate(self.action_data)
        if not status:
            raise Exception("Invalid syntax: LinchpinHook:"+str((v.errors)))
        else:
            return status
        pass

    def add_ctx_params(self, file_path, context=True):
        if not context:
            return file_path
        params = file_path
        for key in self.target_data:
            params += " %s=%s " %(key, self.target_data[key])
        return "{0} {1}".format(file_path,
                                    params)

    def execute(self):

        for action in self.action_data["actions"]:
            context = self.action_data.get("context", True)
            path = self.action_data["path"]
            file_path = "{0}/{1}".format(
                        path,
                        action
                        )
            command = self.add_ctx_params(file_path, context)
            success = run_rb(command)
            return success
