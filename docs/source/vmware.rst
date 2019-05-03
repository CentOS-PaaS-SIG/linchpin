VMware
======

The VMware provider manages a single resource, ``vmware_guest``.

vmware_guest
------------

VMware VMs can be provisioned using this resource

* :docs1.7: `Topology Example <workspace/topologies/vmware.yml>`
* `Ansible module https://docs.ansible.com/ansible/latest/modules/vmware_guest_module.html`


Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`vmware_guest` supports all the Ansible module
options with the same schema structure. All the limitation of the module apply
too.

Additional Dependencies
-----------------------

The vmware resources group requires additional dependency, the following must be
installed:

* PyVmomi

.. code-block:: bash

   $ pip install linchpin[vmware]

Credentials Management
----------------------

.. include:: credentials/vmware.rst
