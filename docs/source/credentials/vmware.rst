Environment Variables
---------------------

Linchpin honors the following environment variables:

+----------------------+----------------------+--------------------------------+
| Environment variable | Credentials variable | Description                    |
+======================+======================+================================+
| VMWARE_PASSWORD      | password             | The password of the vSphere    |
|                      |                      | vCenter or ESXi server         |
+----------------------+----------------------+--------------------------------+
| VMWARE_USER          | username             | The username of the vSphere    |
|		       |		      | vCenter or ESXi server.	       |
+----------------------+----------------------+--------------------------------+
| VMWARE_HOST	       | hostname	      | The hostname or IP address of  |
|		       |		      | the vSphere vCenter or ESXi    |
|		       |		      | server.                        |
+----------------------+----------------------+--------------------------------+
| VMWARE_PORT	       | port                 | The port number of the vSphere |
|		       |		      | vCenter or ESXi server.        |
+----------------------+----------------------+--------------------------------+
| VMWARE_VALIDATE_CERTS| validate_certs       | Allows connection when SSL     |
|		       |		      | certificates are not valid.    |
+----------------------+----------------------+--------------------------------+

Credentials File
~~~~~~~~~~~~~~~~

An example credentials file may look like this for :ref:`vmware`.

.. code-block:: cfg

    $ cat vmware.key
      [default]
      username=root
      password=VMware1!
      hostname=192.168.122.125
      validate_certs=false

.. seealso:: :doc:`providers` for provider-specific credentials examples.

To use these credentials, the user must tell LinchPin two things. The first
is which credentials to use. The second is where to find the credentials data.

Using Credentials
~~~~~~~~~~~~~~~~~

In the topology, a user can specific credentials. The credentials are
described by specifying the file, then the profile. As shown above, the
filename is 'vmware.key'. The user could pick either profile in that file.

.. code-block:: yaml

    ---
    topology_name: vmware-new
    resource_groups:
      - resource_group_name: vmware-new
        resource_group_type: vmware
        resource_definitions:
          - role: vmware_guest
            name: vmware-node
            cdrom:
              type: iso
              iso_path: "[ha-datacenter] tc_vmware4.iso"
            folder: /
            datastore: ha-datacenter
            disk:
              - size_mb: 10
                type: thin
            hardware:
              num_cpus: 1
              memory_mb: 256
            networks:
              - name: VM Network
            wait_for_ip_address: yes
        credentials:
          filename: vmware.key
          profile: default

The important part in the above topology is the `credentials` section. Adding
credentials like this will look up, and use the credentials provided.

Credentials Location
~~~~~~~~~~~~~~~~~~~~

By default, credential files are stored in the `default_credentials_path`, which is
``~/.config/linchpin``.

.. hint:: The `default_credentials_path` value uses the interpolated
   :dirs1.5:`default_config_path <workspace/linchpin.conf#L22>` value, and
   can be overridden in the :docs1.5:`linchpin.conf`.

The credentials path (or ``creds_path``) can be overridden in two ways.

It can be passed in when running the linchpin command.

.. code-block:: bash

    $ linchpin -vvv --creds-path /dir/to/creds up vmware-new

.. note:: The ``vmware.key`` file could be placed in the
   :doc:`default_credentials_path <conf/evars>`. In that case passing
   ``--creds-path`` would be redundant.

Or it can be set as an environment variable.

.. code-block:: bash

    $ export CREDS_PATH=/dir/to/creds
    $ linchpin -v up vmware-new


