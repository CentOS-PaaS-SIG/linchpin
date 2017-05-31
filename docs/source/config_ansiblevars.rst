Ansible Variables
=================

.. contents:: Topics


Inputs
``````

The following variables can be set using ansible extra_vars, including in the ``[evars]`` section
of linchpin.conf, to alter linchpin's default behavior.

.. glossary::

    topology
    topology_file
        A set of rules, written in YAML, that define the way the provisioned
        systems should look after executing linchpin.

        Generally, the `topology` and `topology_file` values are
        interchangeable, except after the file has been processed.

    schema
    schema_file
        JSON description of the format for the topology.
        *(schema_v3, schema_v4 are still available)*

    layout
    layout_file
        YAML definition for providing an ansible (currently) static inventory file, based upon the provided
        topology.

    inventory
    inventory_file
        If layout / layout_file is provided, this will be the location of the resulting ansible inventory.

    linchpin_config
        if passed on the command line with ``-c/--config``, should be
        an ini-style config file with linchpin default configurations (see
        BUILT-INS below for more information)

    resources
    resources_file
        File with the resource outputs in a JSON formatted file. Useful for teardown (destroy,down) actions
        depending on the provider.

    workspace
        If provided, the above variables will be adjusted
        and mapped according to this value. Each path will use the following
        variables::

            topology / topology_file = /<topologies_folder>
            layout / layout_file = /<layouts_folder>
            resources / resources_file = /resources_folder>
            inventory / inventory_file = /<inventories_folder>

            .. note:: schema is not affected by this pathing

        If the ``WORKSPACE`` environment variable is set, it will be used here. If it
        is not, this variable can be set on the command line with ``-w/--workspace``, and defaults
        to the location of the PinFile bring provisioned.


Built-ins
`````````

These variables **SHOULD NOT** be changed!

.. glossary::

    lp_path
        base path for linchpin playbooks and python api

    lpconfig
        ``<lp_path>/linchpin.conf``, unless overridden by :term:`linchpin_config`


Defaults
````````

While the variables here can also be passed as extra-vars, the values are the defaults and it is
recommended not to change them. These values are defined in ``<lp_path>/linchpin.conf`` by default.

.. glossary::

    async
        *(boolean, default: False)*

        Used to enable asynchronous provisioning/teardown

    async_timeout
        *(int, default: 1000)*

        How long the resouce collection (formerly outputs_writer) process should wait

    output
        *(boolean, default: True, previous: no_output)*

        Controls whether resources will be written to the resources_file

    check_mode
        *(boolean, default: no)*

        This option does nothing at this time, though it may eventually be used for dry-run
        functionality based upon the provider

    schemas_folder
        *(file_path, default: schemas)*

        relative path to schemas

    playbooks_folder
        *(file_path, default: provision)*

        relative path to playbooks, only useful to the linchpin API and CLI

    layouts_folder
        *(file_path, default: layouts)*

        relative path to layouts

    topologies_folder
        *(file_path, default: topologies)*

        relative path to topologies

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

        landing location for resources output data

    default_inventories_path
        *(file_path, default: <lp_path>/defaults/<inventories_folder>)*

        landing location for inventory outputs

.. seealso::

    :doc:`glossary`
        Glossary
