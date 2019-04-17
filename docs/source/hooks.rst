Linchpin Hooks
==============

Description:
************


Every resource provisioned by linchpin goes through multiple states. Each state has its own context. Depending upon the state Linchpin provides a feature to trigger single or multiple events. In Linchpin terminology, each event can initiate execution of a script/scripts or Ansible playbooks called hooks. Hooks are used to configure or interact with resources provisioned or about to be provisioned. The trigger to the hooks is determined by the state in which it is defined.

Different states linchpin provisioning undertakes are as follows:

* preup: State before provisioning the topology resources
* postup: State after provisioning the topology resources, and generating the optional inventory
* predestroy: State before teardown of the topology resources
* postdestroy: State after teardown of the topology resources

Depending upon the state section in which it is defined the hooks are triggered.


In linchpin, there are a set of python interfaces called ActionManagers which are responsible for the execution of a hook. Based on the runtime they use to execute hook there are multiple types of Action managers exists. Here's a list of built-in Action Managers:

* shell: Allows either inline shell commands or an executable shell script
* python: Executes a Python script
* ansible: Executes an Ansible playbook, allowing passing of a vars_file and extra_vars represented as a Python dict
* nodejs: Executes a Node.js script
* ruby: Executes a Ruby script

In addition to the above action managers, User can define their custom action manager. Refer Action managers documentation for more details.

A hook is bound to a specific target and must be re-stated for each target used.

Based on how they are packaged linchpin hooks are classified into two types:


* User defined hooks: These hooks are written following specific syntax and folder structure within the workspace. These are triggered based upon the section in which it is declared.

  User-defined hooks are to be declared within a linchpin workspace folder named "hooks" by default. However, this path can be configured by variable hooks_folder in [evars] section of linchpin.conf.

.. code:: yaml

  [evars]
  ...
  hooks_folder = /path/to/hooks_folder


* Built-in hooks (in development): These hooks are pre-packaged with linchpin and they do not need any file structure to be declared in workspaces to work. They can be directly referenced within the Pinfile.

**************************
User defined hook example:
**************************

Let us consider a user-defined hook for example.

Each hook follows a strict folder structure. If not followed the hooks execution will result in failure.
The following is an example workspace which has a user-defined ansible hook named example_hook. The following would be the directory tree structure of the workspace.

::

  .
  ├── credentials
  ├── hooks
  │   └── ansible
  │       ├── example_hook
  │       │   ├── test_hook1.yaml
  │       │   ├── test_hook2.yaml
  │       ├── example_hook2
  │       │   ├── test_ex.yaml
  ├── inventories
  ├── layouts
  │   └── dummy-layout.yml
  ├── linchpin.conf
  ├── linchpin.log
  ├── PinFile
  ├── resources
  └── topologies
    └── dummy-topology.yml

Every hook with respect to their type is declared in their respective folder ie., ansible hooks go inside ansible folder, python hooks are declared in python folder etc.,
The current example illustrates the folder structure of ansible based hooks. 
For more examples folder structures of other hooks refer `Hooks examples`. Further, the name of the folder should be the name of the hook that will be referred to within a PinFile. Since Ansible relies on the playbooks. All the playbooks are to be defined within the folder.

The following is how a user-defined hook looks like when referenced in a Pinfile dummy provider.

.. code:: yaml

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
      - name: example_hook    # name of the hook
        type: ansible      # type of the hook ie., the type of action manager being used.
        context: True      # whether to pass the linchpin context variables or not.
        actions:
          - playbook: test_hook1.yaml  # file name of the playbook to be run
          - playbook: test_hook2.yaml
      - name: example_hook2    # name of the hook
        type: ansible      # type of the hook ie., the type of action manager being used.
        context: True      # whether to pass the linchpin context variables or not.
        actions:
          - playbook: test_ex.yaml  # file name of the playbook to be run
      

As mentioned previously, depending upon the state where the user would like to execute hooks can be triggered at preup, postup, predestroy, postdestroy states. Within Pinfile these states are defined as separate sections. Every hook declared within a section is executed in a top-down approach. Thus, according to the above example, example_hook would be executed first after that execution is successful, example hook2 would be executed.

Parameters of  user-defined hooks:
----------------------------------

  - name: Name of the hook that is defined. Further, it should match the name of the folder inside the hooks_folder configured
  - type: Type of the action manager that is to be used can be any one of ansible, shell, python, ruby, and nodejs. 
  - Context: while declaring hooks provide an option called as context. When the context variable is set to True some of the linchpin context variables are passed as runtime parameters to the playbooks/scripts executed. This is feature is very helpful when end-user would like to run addition configuration playbooks on provisioned instances.
  - actions: Actions are the list of commands, scripts or playbooks which will be run. There can be multiple actions with the same hook file referenced. If it is an ansible type hook, The elements in action should have a playbook, extra_vars(Optional) parameters instead of directly referencing the file path. For more examples refer Linchpin Hooks examples section.

Action manager specific parameters:
-----------------------------------

The following are examples for different types of hooks using multiple action_managers 

* Ansible:

  :: 

    - name: example_hook2    # name of the hook
      type: ansible      # type of the hook ie., the type of action manager being used.
      context: True      # whether to pass the linchpin context variables or not.
        path: /path/to/scripts # optional , by default path would be configured hooks_folder
        actions:
        - playbook: test_ex.yaml  # file name of the playbook to be run
          extra_vars:
            testvar: testval # extravars are optional

* Python:

  ::
 
    - name: example_hook2    # name of the hook
      type: python      # type of the hook ie., the type of action manager being used.
      context: True      # whether to pass the linchpin context variables or not.
      path: /path/to/scripts # optional , by default path would be configured hooks_folder
      actions:
        - script.py  #file name of the playbook to be run

* shell:

  ::
 
    - name: example_hook3    # name of the hook
      type: shell      # type of the hook ie., the type of action manager being used.
      context: True      # whether to pass the linchpin context variables or not.
      path: /path/to/scripts # optional , by default path would be configured hooks_folder
      actions:
      # make sure the script file has execute permissions and shebang header included.
        - script.sh  #file name of the playbook to be run




* Ruby:

  ::

    - name: example_ruby   # name of the hook
      type: ruby      # type of the hook ie., the type of action manager being used.
      context: True      # whether to pass the linchpin context variables or not.
      path: /path/to/scripts # optional , by default path would be configured hooks_folder
      actions:
        - script.rb  #file name of the playbook to be run

* Nodejs:

  ::

    - name: example_nodejs    # name of the hook
      type: nodejs      # type of the hook ie., the type of action manager being used.
      context: True      # whether to pass the linchpin context variables or not.
      path: /path/to/scripts # optional , by default path would be configured hooks_folder
      actions:
        - script.js  #file name of the playbook to be run

Note: For both ruby and nodejs the runtime interpreters should be pre-installed in the host machine.


* linchpin global hooks or builtins:
Linchpin also provides a prepackaged set of built-in hooks which can be referenced within Pinfile without creating a hooks folder structure. These built-ins are ansible based hooks each having different parameters. Currently, There are three builtin linchpin hooks available to end user. They are:

* ping: Simple ICMP ping to check the host provisioned in inventory is up or not
* check_ssh: linchpin tries to check the ssh server is up and running by logging into the machines provisioned using a ssh key
* port_up: Checks whether the list of network ports are up or down.

All the builtin hooks are context-aware, Thus, every built-in hook is run against the inventory file generated during the linchpin provisioning process.


Builtin hooks Example:

:: 

  ---
  os-server-target:
    topology:
      topology_name: os-server-inst
      resource_groups:
        - resource_group_name: os-server-addl-vols
          resource_group_type: openstack
          resource_definitions:
          - name: "database"
            role: os_server
            flavor: m1.small
            image: CentOS-7-x86_64-GenericCloud-1612
            count: 1
            keypair: test_keypairsk2
            fip_pool: 10.8.240.0
            networks:
              - e2e-openstack
          credentials:
            filename: clouds.yaml
            profile: ci-rhos
    layout:
      inventory_layout:
        vars:
          hostname: __IP__
        hosts:
          addl-vols-node:
            count: 1
            host_groups:
            - hello
  hooks:
    postup:
      # check_ssh, ping and port_up are builtin hooks
      # note builtin hooks follow different structure when compared to localhooks
      - name: check_ssh
        extra_vars:
          # since checking ssh depends on logging into machine pem file, ssh_user are must
          ansible_ssh_private_key_file:  test_keypairsk2.key
          ansible_ssh_user: centos
          ansible_ssh_common_args: "'-o StrictHostKeyChecking=no'"
          ansible_python_interpreter: "/usr/bin/python"
      - name: ping
      - name: port_up
        ports:
          - 22
          - 8080

**************************
Hook Communication:
**************************

Hooks can read data from other hooks run in the same target.  Hook data is not shared between a provisioning and corresponding teardown task, but is shared between pre- and post- provisioning as well as between action managers.

With the exception of the Ansible action manager, hook data is passed as the last argument to the hook.  The data is formatted as a JSON array.  Each item in the array is an object with three fields: :term:`return_code`. :term:`data`, and :term:`state` (e.g. preup).  In order for a hook to share data, it should output it as json to stderr.  This will be saved to the :term:`data` field of the hook data object.  If the stderr output is not valid json, it will be ignored.

The ansible action manager handles data somewhat differently.  The results array is passed as a variable called :term:`hook_results` to Ansible's extra vars.  Data from Ansible will be sent back to LinchPin using the :term:`PlaybookCallback` class.



Note: For more examples please refer hooks examples section.

.. toctree::
   :maxdepth: 1
   :hidden:

   installation
   init_workspace
   simple_workspace
   simple_pinfile
   simple_up
   hooks
   hooks_cli_options
   hooks_examples
   custom_action_managers
   inventory
   destroy
   tutorials




.. seealso::

    :doc:`cli`
        Linchpin Command-Line Interface
    :doc:`workflow`
        Common LinchPin Workflows
    :doc:`managing_resources`
        Managing Resources
    :doc:`providers`
        Providers in Detail
