General Configuration
---------------------

Managing LinchPin requires a few configuration files. Most configurations are
stored in the :code1.5:`linchpin configuration <linchpin/linchpin.constants>` file.

.. note:: in versions before 1.5.1, the file was called linchpin.conf. This
   changed in 1.5.1 due to backward compatibility requirements, and the need
   to load configuration defaults. The linchpin.conf continues to work as
   expected.

The settings in this file are loaded automatically as defaults.

However, it's possible to override any setting in linchpin. For the
command line shell, three different locations are checked for linchpin.conf
files. Files are checked in the following order:

#. :file:`/etc/linchpin.conf`
#. :file:`~/.config/linchpin/linchpin.conf`
#. :file:`/path/to/workspace/linchpin.conf`

The LinchPin configuration parser supports overriding and extending
configurations. If linchpin finds the same section and setting in more than
one file, the header that was parsed more recently will provide the
configuration. In this way user can override default configurations. Commonly,
this is done by placing a `linchpin.conf` in the root of the :term:`workspace`.

Adding/Overriding a Section
```````````````````````````

New in version 1.2.0

Adding a section to the configuration is simple. The best approach is to
create a linchpin.conf in the appropriate location from the locations above.

Once created, add a section. The section can be a new section, or it can
overwrite an existing section.

 .. code-block:: cfg

    [lp]
    # move the rundb_connection to a global scope
    rundb_conn = %(default_config_path)s/rundb/rundb-::mac::.json

    module_folder = library
    rundb_conn = ~/.config/linchpin/rundb-::mac::.json

    rundb_type = TinyRunDB
    rundb_conn_type = file
    rundb_schema = {"action": "",
                    "inputs": [],
                    "outputs": [],
                    "start": "",
                    "end": "",
                    "rc": 0,
                    "uhash": ""}
    rundb_hash = sha256

    dateformat = %%m/%%d/%%Y %%I:%%M:%%S %%p
    default_pinfile = PinFile

.. warning:: For version 1.5.0 and earlier, if overwriting a section, all
   entries from the entire section must be updated.


Overriding a configuration item
```````````````````````````````

New in version 1.5.1

Each item within a section can be a new setting,
or override a default setting, as shown.

.. code-block:: cfg

    [lp]
    # move the rundb_connection to a global scope
    rundb_conn = ~/.config/linchpin/rundb-::mac::.json


As can be plainly seen, the configuration has been updated to use a different
path to the ``rundb_conn``. This section now uses a user-based RunDB, which
can be useful in some scenarios.

.. _config_useful_configs:

Useful Configuration Options
````````````````````````````

These are some configuration options that may be useful to adjust for your
needs. Each configuration option listed here is in a format of
``section.option``.

.. note:: For clarity, this would appear in a configuration file where the
   section is in brackets (eg. ``[section]``) and the option would have a
   ``option = value`` set within the section.

lp.external_providers_path
    New in version 1.5.0

    Default value: ``%(default_config_path)s/linchpin-x``

    Providers playbooks can be created outside of the core of linchpin,
    if desired. When using these external providers, linchpin will use
    the `external_providers_path` to lookup the playbooks and attempt to
    run them.

    See :doc:`providers` for more information.

lp.rundb_conn
    New in version 1.2.0

    Default value:
        * v1.2.0: ``/home/user/.config/linchpin/rundb-<macaddress>.json``
        * v1.2.2+: ``/path/to/workspace/.rundb/rundb.json``

    The RunDB is a single json file, which records each transaction involving
    resources. A :term:`run_id` and :term:`uHash` are assigned, along with
    other useful information. The `lp.rundb_conn` describes the location to
    store the RunDB so data can be retrieved during execution.

evars._async
    Updated in version 1.2.0

    Default value: ``False``

    Previous key name: evars.async

    Some providers (eg. openstack, aws, ovirt) support asynchronous
    provisioning. This means that a topology containing many resources
    would provision or destroy all at once. LinchPin then waits for responses
    from these asynchronous tasks, and returns the success or failure.  If the
    amount of resources is large, asynchronous tasks reduce the wait time
    immensely.

    Reason for change: Avoiding conflict with existing Ansible variable.

    Starting in Ansible 2.4.x, the `async` variable could not be set internally.
    The `_async` value is now passed in and sets the Ansible `async` variable
    to its value.

evars.default_credentials_path
    Default value: ``%(default_config_path)s``

    Storing credentials for multiple providers can be useful. It also may
    be useful to change the default here to point to a given location.

    .. note:: The ``--creds-path`` option, or ``$CREDS_PATH`` environment
              variable overrides this option

evars.inventory_file
    Default value: ``None``

    If the unique-hash feature is turned on, the default inventory_file
    value is built up by combining the :term:`workspace` path,
    :term:`inventories_folder` :term:`topology_name`, the :term:`uhash`,
    and the `extensions.inventory` configuration value. The resulting file
    might look like this:

    .. code-block:: bash

        /path/to/workspace/inventories/dummy_cluster-049e.inventory

    It may be desired to store the inventory without the uhash, or
    define a completely different structure altogether.

ansible.console
    Default value: ``False``

    This configuration option controls whether the output from the Ansible
    console is printed. In the ``linchpin`` CLI tool, it's the equivalent of
    the ``-v (--verbose)`` option.



