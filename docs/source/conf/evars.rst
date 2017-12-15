The following settings are in the ``[evars]`` section of the linchpin.conf

_check_mode
~~~~~~~~~~~

Enables the Ansible
`check_mode <http://docs.ansible.com/ansible/latest/playbooks_checkmode.html>`_,
or Dry Run functionality. Most provisioners currently DO NOT support this
option

.. code-block:: cfg

    _check_mode = False

_async
~~~~~~


.. code-block:: cfg

    _check_mode = False
_async = False

_async
~~~~~~

.. code-block:: cfg

    _check_mode = False

async_timeout = 1000


_async
~~~~~~

.. code-block:: cfg

    _check_mode = False

output = True

_async
~~~~~~

.. code-block:: cfg

    _check_mode = False

_async
~~~~~~

default_ssh_key_path = ~/.ssh

.. code-block:: cfg

    _check_mode = False

# default paths in playbooks
#
# lp_path = <src_dir>/linchpin
# determined in the load_config method of # linchpin.cli.LinchpinCliContext
#

# if either of these change, the value in linchpin/templates must also change

_async
~~~~~~

.. code-block:: cfg

    _check_mode = False


layouts_folder = layouts

_async
~~~~~~

.. code-block:: cfg

    _check_mode = False

topologies_folder = topologies

_async
~~~~~~

.. code-block:: cfg

    _check_mode = False


hooks_folder = hooks
_async
~~~~~~
.. code-block:: cfg

    _check_mode = False

roles_folder = roles
_async
~~~~~~
.. code-block:: cfg

    _check_mode = False

inventories_folder = inventories
_async
~~~~~~
.. code-block:: cfg

    _check_mode = False

resources_folder = resources
_async
~~~~~~
.. code-block:: cfg

    _check_mode = False

schemas_folder = schemas
_async
~~~~~~
.. code-block:: cfg

    _check_mode = False


# used in the API/CLI only
playbooks_folder = provision

# inputs
_async
~~~~~~
.. code-block:: cfg

    _check_mode = False

default_schemas_path = {{ lp_path }}/defaults/%(schemas_folder)s
_async
~~~~~~
.. code-block:: cfg

    _check_mode = False

default_topologies_path = {{ lp_path }}/defaults/%(topologies_folder)s
_async
~~~~~~
.. code-block:: cfg

    _check_mode = False

default_layouts_path = {{ lp_path }}/defaults/%(layouts_folder)s
_async
~~~~~~
.. code-block:: cfg

    _check_mode = False

default_inventories_path = {{ lp_path }}/defaults/%(inventories_folder)s

default_roles_path
~~~~~~~~~~~~~~~~~~

When using the :ref:`external_providers_path`

.. code-block:: cfg

    _check_mode = False

default_roles_path = {{ lp_path }}/%(playbooks_folder)s/%(roles_folder)s

schema_v3
~~~~~~~~~

Deprecated in v1.5.0

Full path to the location of the ``schema_v3.json`` file, which is
used to perform validation of the topology.

.. code-block:: cfg

    _check_mode = False

schema_v3 = %(default_schemas_path)s/schema_v3.json

schema_v4
~~~~~~~~~

Deprecated in v1.5.0

Full path to the location of the ``schema_v4.json`` file, which is
used to perform validation of the topology.

.. code-block:: cfg

    schema_v4 = %(default_schemas_path)s/schema_v4.json

default_credentials_path
~~~~~~~~~~~~~~~~~~~~~~~~

If the ``--creds-path`` option or ``$CREDS_PATH`` environment variable are not
set, use this location to look up credentials files defined in the topology.

.. code-block:: cfg

    default_credentials_path = %(default_config_path)s

inventory_file
~~~~~~~~~~~~~~

New in v1.2.0

This configuration changes the default ``inventory_file`` value.
The default is determined in code by concatenating several evars together.

.. code-block:: cfg

    #inventory_file = {{ workspace }}/{{ inventories_folder }}/{{ topology_name }}-{{ uhash }}.inventory
