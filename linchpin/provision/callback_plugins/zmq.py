from __future__ import (absolute_import, division, print_function)
from ansible.plugins.callback import CallbackBase
__metaclass__ = type
import zmq

DOCUMENTATION = '''
    callback: zmq
    type: notification
    requirements:
      - zmq
    short_description: push to massage bus play events
    version_added: 1.9
    description:
      - This plugin will use zmq to push play events.
'''


class CallbackModule(CallbackBase):
    """
    makes Ansible much more exciting.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'zmq'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self):

        super(CallbackModule, self).__init__()
        self.socket = None

    def push(self, msg):
        try:
            self.socket.send(str(msg).encode('utf-8'))
        except Exception:
            # FIXME: any other error
            pass

    def v2_playbook_on_play_start(self, playbook):
        vm = playbook.get_variable_manager()
        extra_vars = vm.extra_vars
        no_monitor = extra_vars.get('no_monitor', '')
        if no_monitor:
            self.disabled = True
        else:
            context = zmq.Context()
            self.socket = context.socket(zmq.REQ)
            self.socket.connect("tcp://localhost:5599")

    def v2_playbook_on_task_start(self, task, is_conditional):
        pass

    def v2_runner_on_ok(self, result):
        pass

    def playbook_on_stats(self, name):
        self.push('{"playbook": "done"}')
