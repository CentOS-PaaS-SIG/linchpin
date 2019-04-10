Linchpin Custom Action Managers
===============================

Linchpin custom action managers:

In linchpin, ActionManagers are set of python interfaces responsible for execution of linchpin hook based on their type. There are two types of ActionManagers builtins and custom. 

Here's a list of built-in Action Managers:

* shell: Allows either inline shell commands or an executable shell script
* python: Executes a Python script
* ansible: Executes an Ansible playbook, allowing passing of a vars_file and extra_vars represented as a Python dict
* nodejs: Executes a Node.js script
* ruby: Executes a Ruby script

In addition to the above action managers, User can define their custom action manager. custom/userdefined action managers are helpful when there is a specific runtime end user would like to make use of for executing a hook.

For example, if linchpin end user would like to use a “xyz” language based runtime or a custom command to be run when certain paramters are passed to a hook. They can do it with help of hook based on custom_action_manager.

Consider the following dummy workspace example for custom_action_manager:

::

  .
  ├── credentials
  ├── hooks
  │   ├── custom
  │   │   └── somecustomhook
  │   │       ├── custom_action_manager.py
  │   │       ├── custom_action_manager.pyc
  │   │       └── test_custom.py
  ├── inventories
  ├── layouts
  ├── linchpin.conf
  ├── linchpin.log
  ├── localhost
  ├── PinFile
  ├── resources
  └── topologies
    └── dummy-topology.yml


::

  ---
  dummy_target:
    topology: 
      topology_name: "dummy"
      resource_groups:
      - resource_group_name: "dummy"
        resource_group_type: "dummy"
        resource_definitions:
        - role: "dummy_node"
          name: "web"
          count: 1
    layout:
      inventory_layout:
        vars:
          hostname: __IP__
        hosts:
          example-node:
            count: 1
            host_groups:
              - example
    hooks:
      postup:
        - name: somecustomhook
          type: custom
          action_manager: custom_action_manager.py
          # action_manager: /path/to/manager
          # if not absolute path 
          # linchpin searches in hooks folder configured 
          context: True
          actions:
            - script: some_script.go




As you can see in the above structure the custom hook follows the same structure of a userdefined hook. However, we also need to add python interface custom_action_manager.py (which can be named any) within thehooks folder or the absolute path to the python file is to be mentioned in the Pinfile

In order to write a custom_action_manager one has to implement builtin linchpin ActionManager class overriding the following functions:


* validate: (optional): validate schema for hook designed

* load: How to load the context parameters

* execute: Responsible for executing the files based on the parameters

Once the above functions are implemented the class file can be included in Pinfile.

Following is an example for the python interface implemented:


::

  import os
  import yaml
  import json
  
  from cerberus import Validator

  from linchpin.exceptions import HookError
  from linchpin.hooks.action_managers.action_manager import ActionManager


  class CustomActionManager(ActionManager):
  
      def __init__(self, name, action_data, target_data, **kwargs):

          """
          The following is an example for CustomActionManager
          AnsibleActionManager constructor
          :param name: Name of Action Manager , ( ie., ansible)
          :param action_data: dictionary of action_block
          consists of set of actions
          example:
          - name: nameofthehook
            type: custom
            actions:
              - script: test_playbook.yaml
          :param target_data: Target specific data defined in PinFile
          :param kwargs: anyother keyword args passed as metadata
          """

          self.name = name
          self.action_data = action_data
          self.target_data = target_data
          self.context = kwargs.get("context", True)
          self.kwargs = kwargs


      def validate(self):

          """
          Validates the action_block based on the cerberus schema
          example:: ansible_action_block::::
          - name: nameofthehook
            type: customhook
            actions:
              - script: test_playbook.yaml
          """
          """
          schema = {
              'name': {'type': 'string', 'required': True},
              'type': {'type': 'string', 'allowed': ['custom']},
              'path': {'type': 'string', 'required': False},
              'context': {'type': 'boolean', 'required': False},
              'actions': {
                  'type': 'list',
                  'schema': {
                      'type': 'dict',
                      'schema': {
                          'script': {'type': 'string', 'required': True}
                      }
                  },
                  'required': True
              }
          }

          v = Validator(schema)
          status = v.validate(self.action_data)
  
          if not status:
              raise HookError("Invalid syntax: {0}".format((v.errors)))
          else:
              return status


      def load(self):
  
          """
          Loads the ansible specific managers and loaders
          """
          return True

      def get_ctx_params(self):

          """
          Reformats the ansible specific context variables
          """

          ctx_params = {}
          ctx_params["resource_file"] = (
              self.target_data.get("resource_file", None))
          ctx_params["layout_file"] = self.target_data.get("layout_file", None)
          ctx_params["inventory_file"] = (
              self.target_data.get("inventory_file", None))

          return ctx_params


      def execute(self):

          """
          Executes the action_block in the PinFile
          The following logic just prints out path of the script being used
          """

          self.load()
          extra_vars = {}
          runners = []

          print("This is the custom hook that runs custom logic")

          for action in self.action_data["actions"]:
              path = self.action_data["path"]
              script = action.get("script")
              print(script)
              print(path)

