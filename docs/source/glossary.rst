Glossary
========

The following is a list of terms used throughout the LinchPin documentation.


.. glossary::

   _ async/async
        *(boolean, default: False)*

        Used to enable asynchronous provisioning/teardown

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

    hook
        Certan scripts can be called when a particular :term:`hook` has been
        referenced in the :term:`PinFile`. The currently available hooks are
        `preup`, `postup`, `predestroy`, and `postdestroy`.

    inventory
    inventory_file
        If layout / layout_file is provided, this will be the location of the resulting ansible inventory.

    linchpin_config
        if passed on the command line with ``-c/--config``, should be
        an ini-style config file with linchpin default configurations (see
        BUILT-INS below for more information)

    layout
    layout_file
        YAML definition for providing an ansible (currently) static inventory file, based upon the provided
        topology.

    layouts_folder
        *(file_path, default: layouts)*

        relative path to layouts

    lp_path
        base path for linchpin playbooks and python api

    lpconfig
        ``<lp_path>/linchpin.conf``, unless overridden by :term:`linchpin_config`

    output
        *(boolean, default: True, previous: no_output)*

        Controls whether resources will be written to the resources_file

    PinFile
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
        An action taken when resources are to be made available on a
        particular provider platform. Usually corresponds with the
        ``linchpin up`` command.

    resources
    resources_file
        File with the resource outputs in a JSON formatted file. Useful for
        teardown (destroy,down) actions depending on the provider.

    schema
        JSON description of the format for the topology.

        *(schema_v3, schema_v4 are still available)*

    schemas_folder
        *(file_path, default: schemas)*

        relative path to schemas

    target
        Specified in the :term:`PinFile`, the :term:`target` references a
        :term:`topology` and optional :term:`layout` to be acted upon from the
        command-line utility, or Python API.

    teardown
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

    :doc:`config_ansiblevars`
        Ansible Variables
    `Source Code <https://github.com/CentOS-PaaS-SIG/linchpin>`_
        LinchPin Source Code
    `User Mailing List <https://www.redhat.com/mailman/listinfo/linchpin>`_
        Subscribe and participate. A great place for Q&A 
    `irc.freenode.net <http://irc.freenode.net>`_
        #linchpin IRC chat channel
