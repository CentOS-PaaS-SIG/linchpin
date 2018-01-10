The following settings are in the ``[lp]`` section of the linchpin.conf

module_folder
~~~~~~~~~~~~~

Load custom ansible modules from this directory

.. code-block:: cfg

    module_folder = library

.. FIXME: RunDB values should probably have their own section.

rundb_type
~~~~~~~~~~

New in version 1.2.0

RunDB supports additional drivers, currently the only driver is
TinyRunDB, based upon tinydb.

.. code-block:: cfg

    rundb_type = TinyRunDB

rundb_conn
~~~~~~~~~~

New in version 1.2.0

The resource path to the RunDB connection. The TinyRunDB version (default)
is a file.

Default: ``{{ workspace }}/.rundb/rundb.json``

The configuration file has this option commented out. Uncommenting it could
enable a system-central rundb, if desired.

.. code-block:: cfg

    #rundb_conn = %(default_config_path)s/rundb/rundb-::mac::.json

rundb_conn_type
~~~~~~~~~~~~~~~

New in version 1.2.0

Set this value if the RunDB resource is anything but a file. This setting
is linked to the ``rundb_conn`` configuration.

.. code-block:: cfg

    rundb_conn_type = file

rundb_conn_schema
~~~~~~~~~~~~~~~~~

New in version 1.2.0

The schema used to store records in the TinyRunDb. Many other databases
will likely not use this value, but must honor the configuration item.

.. code-block:: cfg

    rundb_schema = {"action": "",
                    "inputs": [],
                    "outputs": [],
                    "start": "",
                    "end": "",
                    "rc": 0,
                    "uhash": ""}

rundb_hash
~~~~~~~~~~

New in version 1.2.0

Hashing algorithm used to create the uHash.

.. code-block:: cfg

    rundb_hash = sha256

dateformat
~~~~~~~~~~

New in version 1.2.0

The dateformat to use when writing out start and end times to the RunDB.

.. code-block:: cfg

    dateformat = %%m/%%d/%%Y %%I:%%M:%%S %%p

.. FIXME: update the logging dateformat and this one to inherit somehow

default_pinfile
~~~~~~~~~~~~~~~

New in version 1.2.0

The dateformat to use when writing out start and end times to the RunDB.

.. code-block:: cfg

    default_pinfile = PinFile

.. FIXME: consider adjusting init.pinfile to use this one somehow

