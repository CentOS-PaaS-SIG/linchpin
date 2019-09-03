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


Credentials Management
----------------------
 Support IAM user
 example: docs/source/example/workspaces/azure/azure.key
