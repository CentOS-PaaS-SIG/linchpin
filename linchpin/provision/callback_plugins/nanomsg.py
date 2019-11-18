from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: nanomsg
    type: notification
    requirements:
      - nanomsg
    short_description: push to massage bus play events
    version_added: 1.9
    description:
      - This plugin will use nanomsg to push play events.
'''

from ansible.plugins.callback import CallbackBase
from nanomsg import Socket, PAIR, NanoMsgAPIError, BUS
from time import sleep


class CallbackModule(CallbackBase):
    """
    makes Ansible much more exciting.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'nanomsg'
    CALLBACK_NEEDS_WHITELIST = False

    def __init__(self):

        super(CallbackModule, self).__init__()
        self.socket = Socket(BUS)
        self.socket.connect("ipc:///tmp/linchpin.ipc")

    def push(self, msg):
        try:
            self.socket.send(str(msg).encode('utf-8'))
        except NanoMsgAPIError as nn_error:
            pass # FIXME: what to do if messages failed to send?
        except Exception as e:
            pass # FIXME: any other error?

    def v2_playbook_on_task_start(self, task, is_conditional):
        #self.push(task.name)
        pass

    def v2_runner_on_ok(self, result):
        #self.push(str(result._result))
        pass

    def playbook_on_stats(self, name):
        self.push('{"playbook": "done"}')
