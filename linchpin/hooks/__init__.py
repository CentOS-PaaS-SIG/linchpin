"""
example Pinfile for reference::
---
openstack:
  topology: ex_os_server.yml
  layout: openshift-3node-cluster.yml
  hooks:
    postup:              # sub-state is specified
        - name: do_something
          type: shell
          actions:
            - samvaran
        - name: manipulate_inventory
          type: shell
          path: /tmp/shellscripts
          actions:
            - thisisshell.sh
        - name: post_up
          type: ansible
          actions:
            - playbook: test_playbook.yaml
              vars: test_var.yaml
              extra_vars: { "testvar": "world"}
    preup:              # sub-state is specified
        - name: do_something
          type: shell
          actions:
            - echo " this is post up operation Hello hai how r u ?"
        - name: build_openshift_cluster
          type: ansible
          actions:
            - playbook: test_playbook.yaml
              vars: test_var.yaml
              extra_vars: { "testvar": "world"}
    postdown:
        - name: do_something
          type: shell
          actions:
            - echo " this is post up operation Hello hai how r u ?"
        - name: postdown_task
          type: ansible
          actions:
            - playbook: test_playbook.yaml
              vars: test_var.yaml
              extra_vars: { "testvar": "world"}

"""

import pprint
import ast
import sys
from linchpin.hooks.action_managers import ACTION_MANAGERS
from linchpin.exceptions import ActionManagerError

class ActionBlockRouter(object):

    def __init__(self, name, *args, **kwargs):

        self.__implementation = self.__get_implementation(name)(name, *args, **kwargs)

    def __getattr__(self, name):

        return getattr(self.__implementation, name)

    def __get_implementation(self, class_name):

        action_class = ACTION_MANAGERS.get(class_name, None)
        if action_class == None:
            raise ActionManagerError("Action Class %s not found " % (class_name))
        return action_class

class LinchpinHooks(object):

    def __init__(self, api):

        self.api = api
        self.api.bind_to_state(self.run_hooks)

    def run_hooks(self, state, is_global=False):

        self.api.ctx.log("State change triggered in linchpin API")
        self.api.ctx.log("Observed State in LinchpinHooks :: "+str(state))
        hooks_data = self.api.current_target_data.get("hooks", None)
        if hooks_data == None:
            self.api.ctx.log("No hooks found for current target")
            return
        # fetches all the state_data , ie., all the action blocks inside
        # state of the target
        state_data = hooks_data.get(str(state), None)

        # Print out error message if the hooks are not found
        if state_data == None:
            self.api.ctx.log(str(state)+" State hook not found in PinFile")
            return

        # current target data extravars are fetched
        target_data = self.api.current_target_data.get("extra_vars", None)
        self.run_actions(state_data, target_data)

    def run_actions(self, action_blocks, target_data, is_global=False):

        """
        arguments
        action_blocks: list of action_blocks each block constitues
                       to a type of hook
        target_data: data specific to target , which can be dict of topology , layout, outputs , inventory.
        is_global: scope of the hook.
        example: action_block: 
        - name: do_something
          type: shell
          actions:
            - echo " this is post up operation Hello hai how r u ?"
        """

        if is_global:
            raise NotImplementedError("Run Hooks is not implemented \
                                       for global scoped hooks")
        else:
            # a_b -> abbr for action_block
            for a_b in action_blocks:
                action_type = a_b["type"]
                ctx = a_b['context'] if a_b.has_key('context') else True
                if not a_b.has_key("path"):
                    # if the path is not defined it defaults to
                    # workspace/hooks/typeofhook/name
                    a_b["path"] = "{0}/hooks/{1}/{2}/".format(
                                                            self.api.ctx.workspace,
                                                            a_b["type"],
                                                            a_b["name"]
                                                           )
                if a_b.has_key("action_manager"):
                    # fetches the action object from the path
                    # add path to python path
                    sys.path.append(a_b["path"])
                    # get the module path
                    module_path = "{0}/{1}".format(a_b["path"],
                                                   a_b["action_manager"])
                    # get module src
                    module_src = open(module_path, "r").read()
                    # strip .py ext from module path 
                    module_path = module_path.strip(".py")
                    # strip .py ext from action_manager
                    a_b["action_manager"] = a_b["action_manager"].strip(".py")
                    # parse the module
                    module_src = ast.parse(module_src)
                    # get all classes inside the class
                    classes = [node.name for node in ast.walk(module_src) if isinstance(node, ast.ClassDef)]
                    # choose the first name as the class name
                    class_name = classes[0]
                    # import the module with class name, it should work coz python path is appended
                    module = __import__(a_b["action_manager"])
                    # get the class
                    class_ = getattr(module, class_name)
                    # a_b_obj is action_block_object
                    a_b_obj = class_(action_type, a_b, target_data, context=ctx)
                else:
                    a_b_obj = ActionBlockRouter(action_type, a_b, target_data, context=ctx)
                # validates the class object
                a_b_obj.validate()
                # executes the hook
                a_b_obj.execute()
