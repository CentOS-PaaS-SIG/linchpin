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
        # contains all the module arguments
        module_args = self._task.args.copy()
        # task vars.keys() contains all the variable  required
        # when passed a extra_var as key value pair task_vars
        # would return mocked output of the named module.
        # print(task_vars['vars'].keys())
        # print(task_vars['vars'].get('linchpin_mock', False))
        linchpin_mock = task_vars['vars'].get('linchpin_mock',
                                              False)
        task_name = "_".join(self._task.get_name().split())
        print(task_name)
        if linchpin_mock:
            if task_name.startswith("libvirt_:_DIS"):
                return mock_utils.get_mock_data(module_args,
                                                "get_url_DIS")

        module_return = self._execute_module(module_args=module_args,
                                             task_vars=task_vars, tmp=tmp)
        return module_return
