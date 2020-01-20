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
        if linchpin_mock:
            return mock_utils.get_mock_data(module_args,
                                            "ec2_vpc_subnet_facts")

        module_return = self._execute_module(module_args=module_args,
                                             task_vars=task_vars, tmp=tmp)
        return module_return
