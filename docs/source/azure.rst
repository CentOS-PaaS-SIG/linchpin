Azure VM
===================

The Azure provider manages multiple types of resources.

azure_vm
-------

Azure VM Instances can be provisioned using this resource.

* Example <workspaces/azure/Pinfile>`
* azure_vm module <https://docs.ansible.com/ansible/latest/modules/azure_rm_virtualmachine_module.html#id4>_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_vm` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`azure_vm`
definition, the following options are available.

+------------------+------------+---------------+-------------------+-----------------+
| Parameter        | required   | type          | ansible value     | comments        |
+==================+============+===============+===================+=================+
| role             | true       | string        | N/A               |                 |
+------------------+------------+---------------+-------------------+-----------------+
| vm_name          | true       | string        | name              |It can't include |
|                  |            |               |                   | _ and other     |
|                  |            |               |                   |special char     |
+------------------+------------+---------------+-------------------+-----------------+
| image            | true       | string        | image             |                 |
+------------------+------------+---------------+-------------------+-----------------+

Azure Inventory Generation
~~~~~~~~~~~~~~~~~~~~~~~~

If an instance has a public IP attached, its hostname in public DNS, if
available, will be provided in the generated Ansible inventory file, and if not
the public IP address will be provided.


Additional Dependencies
-----------------------
Run "sudo pip install ansible[azure]"

Credentials Management
----------------------
 Support IAM user
 example: docs/source/example/workspaces/azure/azure.key



.. include:: credentials/aws.rst

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

LinchPin honors the Azure environment variables

Provisioning
~~~~~~~~~~~~

Provisioning with credentials uses the ``--creds-path`` option.

.. code-block:: bash

   $ linchpin -v --creds-path ~/.config/aws up

Alternatively, the credentials path can be set as an environment variable,

.. code-block:: bash

   $ export CREDS_PATH="~/.config/aws"
   $ linchpin -v up

