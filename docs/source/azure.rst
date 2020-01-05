Azure
=====

The Azure provider manages multiple types of resources.

.. NOTE::
   The dependencies is perfectly working for the latest version of Ansible, 
   if you are not using the latest version, may not work.

azure_vm
--------

Azure VM Instances can be provisioned using this resource.

* Example_
* `azure_vm module`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_vm` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`azure_vm`
definition, the following options are available.

+----------------------+----------+--------+-----------------------+--------------------+
| Parameter            | required | type   | ansible value         | comments           |
+======================+==========+========+=======================+====================+
| role                 | true     | string | N/A                   |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| vm_name              | true     | string | name                  | It can't include   |
|                      |          |        |                       | '_' and other      |
|                      |          |        |                       | special char       |
+----------------------+----------+--------+-----------------------+--------------------+
| private_image        | false    | string | image                 | This takes         |
|                      |          |        |                       | private images     |
|                      |          |        |                       |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| virtual_network_name | false    | string | virtual_network_name  |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| vm_username          | false    | string | image                 |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| vm_password          | false    | string | image                 |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| count                | false    | int    |                       |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| resource_group       | true     | string | resource_group        |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| vm_size              | false    | string | vm_size               |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| public_image         | false    | dict   | image                 | This para takes    |
|                      |          |        |                       | public images      |
|                      |          |        |                       |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| vm_username          | false    | string | admin_username        |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| vm_password          | false    | string | admin_password        |                    |
+----------------------+----------+--------+-----------------------+--------------------+
| public_key           | false    | string |                       | Copy you key here  |
+----------------------+----------+--------+-----------------------+--------------------+
| delete_all_attached  | false    | string | remove_on_absent      |                    |
+----------------------+----------+--------+-----------------------+--------------------+

* If you declare both public and private image, only the private will be taken

azure_api
---------

Any Azure resources can be provisioned using this role, it supported by the Azure Api

* Example_
* `azure_api module`_
* `Azure API`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`azure_api` :term:`resource_definition` has more
options than what is shown in the examples above. For each :term:`azure_api`
definition, the following options are available.

+-----------------+----------+--------+----------------+----------------------+
| Parameter       | required | type   | ansible value  | comments             |
+=================+==========+========+================+======================+
|  role           | true     | string | N/A            |                      |
+-----------------+----------+--------+----------------+----------------------+
|  resource_group | true     | String | resource_group |                      |
+-----------------+----------+--------+----------------+----------------------+
|  resource_type  | true     | String | resource_type  |                      |
+-----------------+----------+--------+----------------+----------------------+
|  resource_name  | true     | string | resource_name  |                      |
+-----------------+----------+--------+----------------+----------------------+
|  api_version    | true     | string | api_version    |                      |
+-----------------+----------+--------+----------------+----------------------+
|  body_path      | true     | string |                | Path to request body |
+-----------------+----------+--------+----------------+----------------------+
|  url            | true     | string | url            |                      |
+-----------------+----------+--------+----------------+----------------------+

Credentials Management
----------------------
Linchpin supports `Ansible authentication options`_:

* Active Directory
* Service Principal

Active Directory
~~~~~~~~~~~~~~~~

The following keys are required in the credentials file for AD authentication:

user
   The user name, you can verify it manually in `Azure portal`_.

password
   The password, you can verify it manually in `Azure portal`_ and change_ it.

subscription_id
   The subscription id to use, you can check what subscriptions_ available and
   what permission you have in `Azure portal`_.

tenant
   Is the Active Directory ID, and it is required if the user is member of
   multiple directories. You can find tenant ID in `Azure portal`_ at
   `Azure Active Directory`_

Example of credentials file with Azure Active directory:

::

  [default]
  user: linchpin@redhat.com
  password: MySecretPassword
  subscription_id: 2q3d2d-ad3adw-adwa3d-dwade-awedawee
  tenant: 3rfawca-awd3daw-d3cc33-ASCEA-CAEESA-caceace


Service Principal
~~~~~~~~~~~~~~~~~

The following keys are required in the credentials file for SP authentication:

.. glossary::

   client_id
      The client ID is the application ID.

   secret
      The application secret token, can be generated in `Azure portal`_ 

   subscription_id
      The subscription id to use, you can check what subscriptions_ available and
      what permission you have in `Azure portal`_.

   tenant
      Is the Active Directory ID, and it is required if the user is member of
      multiple directories. You can find tenant ID in `Azure portal`_ at
      `Azure Active Directory`_

Example of credentials file with Azure Service Principal:

::

  [default]
  client_id: 2q3d2d-ad3adw-adwa3d-dwade-awedawee
  secret: 2q3d2d-ad3adw-adwa3d-dwade-awedawee
  subscription_id: 2q3d2d-ad3adw-adwa3d-dwade-awedawee
  tenant: 3rfawca-awd3daw-d3cc33-ASCEA-CAEESA-caceace


How to create new Service Principal in Azure portal
```````````````````````````````````````````````````

1. Go to `Azure Active Directory`_ in `Azure portal`_
2. Go to *App registration* on the left bar
3. Create a new app
4. The Application ID is :term:`client_id`
5. The Directory ID is :term:`tenant`
6. Go to *Certificates and secrets* on left bar
7. Upload or create a new key, that is the :term:`secret`
8. Go to the *Access Control* of you resource group or subscription
9. Click on *Add* button to add new role assignment
10. Assign the role of *Contributor* to the application you just created
11. Go to *Subscription* to find out its ID for :term:`subscription id`

How to create new Service Principal using Azure command line client
```````````````````````````````````````````````````````````````````

.. code-block::

   accountname@Azure:~$ az ad sp create-for-rbac --name ServicePrincipalName
   Changing "ServicePrincipalName" to a valid URI of "http://ServicePrincipalName", which is the required format used for service principal names
   Creating a role assignment under the scope of "/subscriptions/dcc74c29-4db6-4c49-9a0f-ac0ee03fa17e"
     Retrying role assignment creation: 1/36
     Retrying role assignment creation: 2/36
     Retrying role assignment creation: 3/36
     Retrying role assignment creation: 4/36
   {
     "appId": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
     "displayName": "ServicePrincipalName",
     "name": "http://ServicePrincipalName",
     "password": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxx",
     "tenant": "xxxxx-xxxxx-xxxx-xxxx-xxxxxxxxxxxx"
   }

.. _Example: workspaces/azure/Pinfile
.. _Azure API: https://docs.microsoft.com/en-us/rest/api/?view=Azure
.. _Azure portal: https://portal.azure.com/
.. _change: https://account.activedirectory.windowsazure.com/ChangePassword.aspx
.. _subscriptions: https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade
.. _Ansible authentication options: https://docs.ansible.com/ansible/latest/scenario_guides/guide_azure.html#authenticating-with-azure
.. _Azure Active Directory: https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/Overview
.. _azure_vm module: https://docs.ansible.com/ansible/latest/modules/azure_rm_virtualmachine_module.html
.. _azure_api module: https://docs.ansible.com/ansible/latest/modules/azure_rm_resource_module.html#azure-rm-resource-module
