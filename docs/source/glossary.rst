Glossary
========

The following is a list of terms used throughout the LinchPin documentation.


.. glossary::

    _async
        *(boolean, default: False)*

        Used to enable asynchronous provisioning/teardown. Sets the Ansible `async` magic_var.

    async_timeout
        *(int, default: 1000)*

        How long the resouce collection (formerly outputs_writer) process should wait

    _check_mode/check_mode
        *(boolean, default: no)*

        This option does nothing at this time, though it may eventually be used for dry-run
        functionality based upon the provider

    default_schemas_path
        *(file_path, default: <lp_path>/defaults/<schemas_folder>)*

        default path to schemas, absolute path. Can be overridden by passing schema / schema_file.

    default_playbooks_path
        *(file_path, default: <lp_path>/defaults/playbooks_folder>)*

        default path to playbooks location, only useful to the linchpin API and CLI

    default_layouts_path
        *(file_path, default: <lp_path>/defaults/<layouts_folder>)*

        default path to inventory layout files

    default_topologies_path
        *(file_path, default: <lp_path>/defaults/<topologies_folder>)*

        default path to topology files

    default_resources_path
        *(file_path, default: <lp_path>/defaults/<resources_folder>, formerly: outputs)*

        default landing location for resources output data

    default_inventories_path
        *(file_path, default: <lp_path>/defaults/<inventories_folder>)*

        default landing location for inventory outputs

    evars
    extra_vars
        Variables that can be passed into Ansible playbooks from external
        sources. Used in linchpin via the linchpin.conf `[evars]` section.

    hook
        Certain scripts can be called when a particular :term:`hook` has been
        referenced in the :term:`PinFile`. The currently available hooks are
        `preup`, `postup`, `predestroy`, and `postdestroy`.

    inventory
    inventory_file
        If layout is provided, this will be the location of the resulting ansible
        inventory

    inventories_folder
        A configuration entry in :docs1.5:`linchpin.conf <workspace/linchpin.conf>`
        which stores the relative location where inventories are stored.

    linchpin_config
    lpconfig
        if passed on the command line with ``-c/--config``, should be
        an ini-style config file with linchpin default configurations (see
        BUILT-INS below for more information)

    layout
    layout_file
    inventory_layout
        Definition for providing an Ansible (currently) static inventory file, based upon the provided
        topology

    layouts_folder
        *(file_path, default: layouts)*

        relative path to layouts

    lp_path
        base path for linchpin playbooks and python api

    output
        *(boolean, default: True, previous: no_output)*

        Controls whether resources will be written to the resources_file

    PinFile
    pinfile
        A YAML file consisting of a :term:`topology` and an optional
        :term:`layout`, among other options. This file is used by the
        ``linchpin`` command-line, or Python API to determine what resources
        are needed for the current action.

    playbooks_folder
        *(file_path, default: provision)*

        relative path to playbooks, only useful to the linchpin API and CLI

    provider
        A set of platform actions grouped together, which is provided by an
        external Ansible module. `openstack` would be a provider.

    provision
    up
        An action taken when resources are to be made available on a
        particular provider platform. Usually corresponds with the
        ``linchpin up`` command.

    resource_definitions
        In a topology, a resource_definition describes what the resources
        look like when provisioned. This example shows two different
        dummy_node resources, the resource named `web` will get 3 nodes, while
        and the resource named `test` will get 1 resource.

        .. code-block:: yaml

            resource_definitions:
              - name: "web"
                type: "dummy_node"
                count: 3
              - name: "test"
                type: "dummy_node"
                count: 1

    resource_group_type
        For each resource group, the type is defined by this value. It's used by
        the LinchPin API to determine which provider playbook to run.

    resources
    resources_file
        File with the resource outputs in a JSON formatted file. Useful for
        teardown (destroy,down) actions depending on the provider.

    run_id
    run-id
        An integer identifier assigned to each task.

        * The run_id can be passed to ``linchpin up`` for idempotent provisioning
        * The run_id can be passed to ``linchpin destroy`` to destroy any 
          previously provisioned resources.

    rundb
    RunDB
        A simple json database, used to store the :term:`uhash` and other
        useful data, including the :term:`run_id` and output data.

    schema
        JSON description of the format for the topology.

    target
        Specified in the :term:`PinFile`, the :term:`target` references a
        :term:`topology` and optional :term:`layout` to be acted upon from the
        command-line utility, or Python API.

    teardown
    destroy
        An action taken when resources are to be made unavailable on a
        particular provider platform. Usually corresponds with the
        ``linchpin destroy`` command.

    topologies_folder
        *(file_path, default: topologies)*

        relative path to topologies

    topology
    topology_file
        A set of rules, written in YAML, that define the way the provisioned
        systems should look after executing linchpin.

        Generally, the `topology` and `topology_file` values are
        interchangeable, except after the file has been processed.

    topology_name
        Within a :term:`topology_file`, the `topology_name` provides a way to
        identify the set of resources being acted upon.

    uhash
    uHash
        Unique-ish hash associated with resources on a provider basis. Provides
        unique resource names and data if desired. The uhash must be enabled
        in linchpin.conf if desired.

    workspace
        If provided, the above variables will be adjusted
        and mapped according to this value. Each path will use the following
        variables::

            topology / topology_file = /<topologies_folder>
            layout / layout_file = /<layouts_folder>
            resources / resources_file = /resources_folder>
            inventory / inventory_file = /<inventories_folder>


        If the ``WORKSPACE`` environment variable is set, it will be used here. If it
        is not, this variable can be set on the command line with ``-w/--workspace``, and defaults
        to the location of the PinFile bring provisioned.

        .. note:: schema is not affected by this pathing


.. seealso::

    `Source Code <https://github.com/CentOS-PaaS-SIG/linchpin>`_
        LinchPin Source Code
