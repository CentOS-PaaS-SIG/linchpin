from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
from nanomsg import Socket, PAIR, NanoMsgAPIError, BUS
from time import sleep

socket = Socket(BUS)
socket.connect("ipc:///tmp/linchpin.ipc")


class ActionModule(ActionBase):
    ''' Send events to Nanomsg '''

    TRANSFERS_FILES = False
    # _VALID_ARGS = frozenset(('nanomsg',))

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()
        name = "{}({})".format(
                self._task.args['name'],
                self._task.args['count'])
        msg = dict(status=dict(target=name, state='Provisioning'), bar=50)
        socket.send(str(msg).encode('utf-8'))

        result = super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()
        module_return = self._execute_module(module_name='dummy',
                                             module_args=module_args,
                                             task_vars=task_vars, tmp=tmp)
        del tmp  # tmp no longer has any effect
        sleep(2)

        msg = dict(status=dict(target=name, state='Done'), bar=50)
        socket.send(str(msg).encode('utf-8'))
        sleep(2)

        return module_return
