The following settings are in the ``[evars]`` section of the linchpin.conf

LinchPin sets several :term:`extra_vars` values, which are passed to the provisioning playbooks.


.. note:: Default paths in playbooks exist.
   lp_path = <src_dir>/linchpin
   determined in the load_config method of linchpin.cli.LinchpinCliContext
   if either of these change, the value in linchpin/templates must also change

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

LinchPin supports the Ansible `async mode <http://docs.ansible.com/ansible/latest/playbooks_async.html>`_
for certain :doc:`../providers`. Setting ``async = True`` here enables the feature.

.. code-block:: cfg

    _async = False

async_timeout
~~~~~~~~~~~~~

Works in conjunction with the `async` setting, defaulting
the async wait time to ``{{ async_timeout }}`` in provider playbooks

.. code-block:: cfg

    async_timeout = 1000

enable_uhash
~~~~~~~~~~~~

In older versions of Linchpin, the uhash value was not used. If set to true,
the unique-ish hash (uhash) will be appended to instances (for providers who
support naming) and the `inventory_path`.

.. code-block:: cfg

    enable_uhash = False

generate_resources
~~~~~~~~~~~~~~~~~~

In older versions of linchpin (<v1.0.4), a `resources` folder exists, which
dumped the data that is now stored in the RunDB. 

.. code-block:: cfg

    generate_resources = True

output
~~~~~~

Deprecated in version 1.2.0
Removed in version 1.5.0

Horribly named variable, no longer used

.. code-block:: cfg

    output = True


layouts_folder
~~~~~~~~~~~~~~

Used in lookup for a specific :term:`layout` within a workspace. The PinFile
specifies the layout without a path, this is the relative location.

Also used in combination with `default_layouts_path <conf_def_layout_path>`,
which isn't generally used.

.. code-block:: cfg

    layouts_folder = layouts

topologies_folder
~~~~~~~~~~~~~~~~~

Used in lookup for a specific :term:`topology` within a workspace. The PinFile
specifies the topology without a path, this is the relative location.

Also used in combination with `default_topologies_path<conf_def_topo_path>`,
which isn't generally used.

.. code-block:: cfg

    topologies_folder = topologies

roles_folder
~~~~~~~~~~~~

New in version 1.5.0

Used in combination with `default_roles_path <conf_def_roles_path>` for
external provider roles

.. code-block:: cfg

    roles_folder = roles

inventories_folder
~~~~~~~~~~~~~~~~~~

Relative location where inventories will be written. Usually combined with the
`default_inventories_path`, but could be relative tothe workspace.


.. code-block:: cfg

    _check_mode = False

inventories_folder = inventories

hooks_folder
~~~~~~~~~~~~

Relative location within the workspace where hooks data is stored

.. code-block:: cfg

    hooks_folder = hooks

resources_folder
~~~~~~~~~~~~~~~~

Deprecated in version 1.5.0

Relative location of the resources destination path. Generally combined with
the `default_resource_path`

.. code-block:: cfg

    resources_folder = resources

schemas_folder
~~~~~~~~~~~~~~

Deprecated in version 1.2.0

Relative location of the schemas within the LinchPin codebase

.. code-block:: cfg

    schemas_folder = schemas

playbooks_folder
~~~~~~~~~~~~~~~~

Relative location of the Ansible playbooks and roles within the LinchPin codebase

.. code-block:: cfg

    playbooks_folder = provision

default_schemas_path
~~~~~~~~~~~~~~~~~~~~

Deprecated in version 1.5.0

Used to locate default schemas, usually `schema_v4` or
`schema_v3`

.. code-block:: cfg

    default_schemas_path = {{ lp_path }}/defaults/%(schemas_folder)s

.. _conf_def_topo_path:

default_topologies_path
~~~~~~~~~~~~~~~~~~~~~~~

Deprecated in version 1.2.0

Default location for topologies in cases where :term:`topology` or
:term:`topology_file` is not set.

.. code-block:: cfg

    default_topologies_path = {{ lp_path }}/defaults/%(topologies_folder)s

.. _conf_def_layout_path:

default_layouts_path
~~~~~~~~~~~~~~~~~~~~

Deprecated in version 1.2.0

When inventories are processed, layouts are looked up here if :term:`layout_file` is not set

.. code-block:: cfg

    default_layouts_path = {{ lp_path }}/defaults/%(layouts_folder)s

.. _conf_def_inv_path:

default_inventories_path
~~~~~~~~~~~~~~~~~~~~~~~~

Deprecated in version 1.2.0

When writing out inventories, this path is used if :term:`inventory_file` is not set

.. code-block:: cfg

    default_inventories_path = {{ lp_path }}/defaults/%(inventories_folder)s

default_resources_path
~~~~~~~~~~~~~~~~~~~~~~

Deprecated in version 1.2.0

When writing out resources files, this path is used if :term:`inventory_file` is not set

.. code-block:: cfg

    default_inventories_path = {{ lp_path }}/defaults/%(inventories_folder)s

.. _conf_def_roles_path:

default_roles_path
~~~~~~~~~~~~~~~~~~

When using an external provider, this path points back to some of the core
roles needed in the provider's playbook.

.. code-block:: cfg

    default_roles_path = {{ lp_path }}/%(playbooks_folder)s/%(roles_folder)s

default_roles_path = {{ lp_path }}/%(playbooks_folder)s/%(roles_folder)s

.. _conf_schema_v3:

schema_v3
~~~~~~~~~

Deprecated in v1.5.0

Full path to the location of the ``schema_v3.json`` file, which is
used to perform validation of the topology.

.. code-block:: cfg

    _check_mode = False

schema_v3 = %(default_schemas_path)s/schema_v3.json

.. _conf_schema_v4:

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
set, use this location to look up credentials files defined in a topology.

.. code-block:: cfg

    default_credentials_path = %(default_config_path)s

inventory_path
~~~~~~~~~~~~~~

New in version 1.5.0

The `inventory_path` is used to set the value of the resulting inventory
file which is generated by LinchPin. This value is dynamically generated by
default.

.. note:: This should not be confused with the `inventory_file` which is an
   input to the LinchPin ansible playbooks.

.. code-block:: cfg

    #inventory_path = {{ workspace }}/{{inventories_folder}}/happy.inventory

default_ssh_key_path
~~~~~~~~~~~~~~~~~~~~

New in version 1.2.0

Used solely in the `libvirt provider <prov_libvirt>`. Could be used to set a
default location for ssh keys that might be passed via a cloud-config setup.

.. code-block:: cfg

    default_ssh_key_path = ~/.ssh

libvirt_image_path
~~~~~~~~~~~~~~~~~~

Where to store the libvirt images for copying/booting instances. This can be
adjusted to a user accessible location if permissions are an issue.

.. note:: Ensure the `libvirt_user` and `libvirt_become` options below are also
   adjusted according to proper permissions.

.. code-block:: cfg

    libvirt_image_path = /var/lib/libvirt/images/

libvirt_user
~~~~~~~~~~~~

What user to use to access the libvirt services.

.. note:: Specifying `root` means that linchpin will attempt to access the
   libvirt service as the `root` user. If the linchpin user is not root, sudo
   without password must be setup.

.. code-block:: cfg

    libvirt_user = root

libvirt_become
~~~~~~~~~~~~~~

When using root or any privileged user, this must be set to yes.

.. note:: If the linchpin user is not root, sudo without password must also be setup.

.. code-block:: cfg

    libvirt_become = yes
