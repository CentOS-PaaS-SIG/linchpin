oVirt
=====

The ovirt provider manages a single resource, ``ovirt_vms``.

ovirt_vms
---------

oVirt Domains/VMs can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/ovirt-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/ovirt_module.html>`_

Additional Dependencies
-----------------------

There are no known additional dependencies for using the oVirt provider
for LinchPin.

Credentials Management
----------------------

An oVirt topology can have a ``credentials`` section for each
:term:`resource_group`, which requires the filename, and the profile name.

Consider the following file, named ``ovirt_creds.yml``.

.. code-block:: yaml

    clouds:
      ge2:
        auth:
          ovirt_url: http://192.168.122.10/
          ovirt_username: demo
          ovirt_password: demo

An oVirt topology can have a ``credentials`` section for each
:term:`resource_group`, which requires the filename and profile name.


.. code-block:: yaml

    ---
    topology_name: topo
    resource_groups:
      - resource_group_name: ovirt
        resource_group_type: ovirt
        resource_definitions:

          .. snip ..

        credentials:
          filename: ovirt_creds.yml
          profile: ge2

Provisioning
````````````

Provisioning with credentials uses the ``--creds-path`` option. Assuming
the credentials file was placed in ``~/.config/ovirt``, and the
topology described above, a provision task could occur.

.. code-block:: bash

   $ linchpin -v --creds-path ~/.config/ovirt up

Alternatively, the credentials path can be set as an environment variable,

.. code-block:: bash

   $ export CREDS_PATH="~/.config/ovirt"
   $ linchpin -v up

