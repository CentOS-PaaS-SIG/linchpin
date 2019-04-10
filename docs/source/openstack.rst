OpenStack
=========

The OpenStack provider manages multiple types of resources.

os_server
---------

OpenStack instances can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/os-server-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/os_server_module.html>`_

.. note:: Currently, the ansible module used is bundled with LinchPin. However,
   the variables used are identical to the Ansible os_server module, except for
   adding a ``count`` option.

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`os_server` :term:`resource_definition` has more options
than what is shown in the examples above. For each :term:`os_server` definition, the
following options are available.

+------------------+------------+----------+-------------------+----------------------------------+
| Parameter        | required   | type     | ansible value     | comments                         |
+==================+============+==========+===================+==================================+
| name             | true       | string   | name              | Name of the instance             |
+------------------+------------+----------+-------------------+----------------------------------+
| flavor           | true       | string   | flavor            | Defines the compute, memory,     |
|                  |            |          |                   | and storage capacity of the node |
+------------------+------------+----------+-------------------+----------------------------------+
| image            | true       | string   | image             | The disk image used to provision |
|                  |            |          |                   | the server instances             |
+------------------+------------+----------+-------------------+----------------------------------+
| region           | false      | string   | region            |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| count            | false      | integer  | count             |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| keypair          | false      | string   | key_name          | Public key of an OpenSSH keypair |
|                  |            |          |                   | to be used for access to created |
|                  |            |          |                   | servers                          |
+------------------+------------+----------+-------------------+----------------------------------+
| security_groups  | false      | string   | security_groups   |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| fip_pool         | false      | string   | floating_ip_pools |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| networks         | false      | string   | networks          |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| userdata         | false      | string   | userdata          |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| volumes          | false      | list     | volumes           |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| boot_from_volume | false      | string   | boot_from_volume  |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| terminate_volume | false      | string   | terminate_volume  |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| volume_size      | false      | string   | volume_size       |                                  |
+------------------+------------+----------+-------------------+----------------------------------+
| boot_volume      | false      | string   | boot_volume       |                                  |
+------------------+------------+----------+-------------------+----------------------------------+

os_obj
------

OpenStack Object Storage can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/os-obj-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/os_object_module.html>`_

os_vol
------

OpenStack Cinder Volumes can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/os-vol-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/os_volume_module.html>`_

os_sg
-----

OpenStack Security Groups can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/os-sg-new.yml>`
* `Ansible Security Group module <http://docs.ansible.com/ansible/latest/os_security_group_module.html>`_
* `Ansible Security Group Rule module <http://docs.ansible.com/ansible/latest/os_security_group_rule_module.html>`_

os_network
----------

OpenStack networks can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/os-network.yml>`
* `Ansible os_network module <https://docs.ansible.com/ansible/2.5/modules/os_network_module.html>`_

os_router
---------

OpenStack routers can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/os-router.yml>`
* `Ansible os_router module <https://docs.ansible.com/ansible/latest/modules/os_router_module.html>`_

os_subnet
---------

OpenStack subnets can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/os-subnet.yml>`
* `Ansible os_router module <https://docs.ansible.com/ansible/latest/modules/os_subnet_module.html>`_


Additional Dependencies
-----------------------

No additional dependencies are required for the OpenStack Provider.

Credentials Management
----------------------

OpenStack provides several ways to provide credentials. LinchPin supports
some of these methods for passing credentials for use with OpenStack resources.

Environment Variables
`````````````````````

LinchPin honors the OpenStack environment variables such as ``$OS_USERNAME``,
``$OS_PROJECT_NAME``, etc.

See `the OpenStack documentation cli documentation 
<https://docs.openstack.org/python-openstackclient/pike/cli/man/openstack.html#manpage>`_
for details.

.. note:: No credentials files are needed for this method. When LinchPin calls
   the OpenStack provider, the environment variables are automatically picked
   up by the OpenStack Ansible modules, and passed to OpenStack for
   authentication.

Using OpenStack Credentials
```````````````````````````

OpenStack provides a simple file structure using a file called
`clouds.yaml <https://docs.openstack.org/os-client-config/latest/user/configuration.html>`_,
to provide authentication to a particular tenant. A single clouds.yaml file
might contain several entries.

.. code-block:: yaml

    clouds:
      devstack:
        auth:
          auth_url: http://192.168.122.10:35357/
          project_name: demo
          username: demo
          password: 0penstack
        region_name: RegionOne
      trystack:
        auth:
          auth_url: http://auth.trystack.com:8080/
          project_name: trystack
          username: herlo-trystack-3855e889
          password: thepasswordissecrte

Using this mechanism requires that credentials data be passed into LinchPin.

An OpenStack topology can have a ``credentials`` section for each
:term:`resource_group`, which requires the filename, and the profile name.

.. code-block:: yaml

    ---
    topology_name: topo
    resource_groups:
      - resource_group_name: openstack
        resource_group_type: openstack
        resource_definitions:

          .. snip ..

        credentials:
          filename: clouds.yaml
          profile: devstack

Provisioning
````````````

Provisioning with credentials uses the ``--creds-path`` option. Assuming
the ``clouds.yaml`` file was placed in ``~/.config/OpenStack``, and the
topology described above, a provisioning task could occur.

.. code-block:: bash

   $ linchpin -v --creds-path ~/.config/openstack up

.. note:: The ``clouds.yaml`` could be placed in the
   :doc:`default_credentials_path <conf/evars>`. In that case passing
   ``--creds-path`` would be redundant.

Alternatively, the credentials path can be set as an environment variable,

.. code-block:: bash

   $ export CREDS_PATH="/path/to/credential_dir/"
   $ linchpin -v up
