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
|                  |            |               |                   | '_' and other   |
|                  |            |               |                   |special char     |
+------------------+------------+---------------+-------------------+-----------------+
| private_image    | false      | string        | image             |This para takes  |
|                  |            |               |                   | private images  |
|                  |            |               |                   |                 |
+------------------+------------+---------------+-------------------+-----------------+
| resource_group   | true       | string        | resource_group    |                 |
+------------------+------------+---------------+-------------------+-----------------+
| vm_size          | true       | string        | vm_size           |                 |
+------------------+------------+---------------+-------------------+-----------------+
| public_image     | false      | dict          | image             |This para takes  |
|                  |            |               |                   | public images   |
|                  |            |               |                   |                 |
+------------------+------------+---------------+-------------------+-----------------+
|virtual_network_name| true     | string        |virtual_network_name|                 |
+------------------+------------+---------------+-------------------+-----------------+
| vm_username      | true       | string        | image             |                 |
+------------------+------------+---------------+-------------------+-----------------+
| vm_password      | true       | string        | image             |                 |
+------------------+------------+---------------+-------------------+-----------------+

#If you declare both public and private image, only the private will be taken

Credentials Management
----------------------
 Support IAM user
 example: docs/source/example/workspaces/azure/azure.key
