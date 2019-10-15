Azure VM
===================

The Azure provider manages multiple types of resources.

azure_vm
-------

Azure VM Instances can be provisioned using this resource.

* Example <workspaces/azure/Pinfile>`
* azure_vm module <https://docs.ansible.com/ansible/latest/modules/azure_rm_virtualmachine_module.html#id4>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_vm` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`azure_vm`
definition, the following options are available.

+----------------------+------------+---------------+-----------------------+--------------------+
| Parameter            | required   | type          | ansible value         | comments           |
+======================+============+===============+=======================+====================+
| role                 | true       | string        | N/A                   |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_name              | true       | string        | name                  | It can't include   |
|                      |            |               |                       | '_' and other      |
|                      |            |               |                       | special char       |
+----------------------+------------+---------------+-----------------------+--------------------+
| private_image        | false      | string        | image                 | This takes         |
|                      |            |               |                       | private images     |
|                      |            |               |                       |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| virtual_network_name | false      | string        | virtual_network_name  |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_username          | false      | string        | image                 |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_password          | false      | string        | image                 |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| resource_group       | true       | string        | resource_group        |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_size              | false      | string        | vm_size               |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| public_image         | false      | dict          | image                 | This para takes    |
|                      |            |               |                       | public images      |
|                      |            |               |                       |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_username          | false      | string        | admin_username        |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| vm_password          | false      | string        | admin_password        |                    |
+----------------------+------------+---------------+-----------------------+--------------------+
| delete_all_attached  |false       | string        | remove_on_absent      |                    |
+----------------------+------------+---------------+-----------------------+--------------------+

⚫ If you declare both public and private image, only the private will be taken

Credentials Management
----------------------
 Support IAM user (instruction below)         
 example: docs/source/example/workspaces/azure/azure.key

IAM Instruction
---------------------
1. Go to Azure Active Directory
2. Go to app registration on the left bar
3. Create a new app
4. Take notes of Application (client) ID (this is client_id)
5. Take notes of Directory (tenant) ID (this is tenant)
6. Go to Certificates & secrets on left bar 
7. Upload or create a new key and take note of it  (this is secret)
8. Go to the ACESS CONTROL of you resource group or subscription
9. Click Add button to add new role assignment
10. Assign the role of Contributor to the App you just created
11. Go to subscription find out the subscription id (this is subscription_id)
11. Fill out the form below and put it into your workplace
client_id:
tenant:
secret: 
subscription_id:
