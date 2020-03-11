from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.action import ActionBase
import linchpin.MockUtils.MockUtils as mock_utils


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        """
        Simple action plugin that returns the mocked output
        when linchpin_mock is True
        """
        super(ActionModule, self).run(tmp, task_vars)
        module_args = self._task.args.copy()
        linchpin_mock = task_vars['vars'].get('linchpin_mock',
                                              False)

        up = task_vars['vars'].get('state', 'present') == 'present'
        if up and linchpin_mock:
            return mock_utils.get_mock_data(module_args,
                                            "azure_loadbalancer.present")
        elif not up and linchpin_mock:
            return mock_utils.get_mock_data(module_args,
                                            "azure_loadbalancer.absent")

        module_return = self._execute_module(module_args=module_args,
                                             task_vars=task_vars, tmp=tmp)
        return module_return
