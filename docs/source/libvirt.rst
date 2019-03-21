Libvirt
=======

The libvirt provider manages two types of resources.

.. _libvirt_node:

libvirt_node
------------

Libvirt Domains (or nodes) can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/libvirt-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/virt_module.html>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`libvirt_node` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`libvirt_node`
definition, the following options are available.

+--------------------+-------+----------+---------------+---------------------+------------+
| Parameter          | req'd | type     | where used    | default             | comments   |
+====================+=======+==========+===============+=====================+============+
| role               | true  | string   | role          |                     |            |
+--------------------+-------+----------+---------------+---------------------+------------+
| name               | true  | string   | module: name  |                     |            |
+--------------------+-------+----------+---------------+---------------------+------------+
| vcpus              | true  | string   | xml: vcpus    |                     |            |
+--------------------+-------+----------+---------------+---------------------+            +
| memory             | true  | string   | xml: memory   | 1024                |            |
+--------------------+-------+----------+---------------+---------------------+            +
| driver             | false | string   | xml: driver   | kvm                 |            |
|                    |       |          | (kvm, qemu)   |                     |            |
+--------------------+-------+----------+---------------+---------------------+            +
| arch               | false | string   | xml: arch     | x86_64              |            |
+--------------------+-------+----------+---------------+---------------------+            +
| boot_dev           | false | string   | xml: boot_dev | hd                  |            |
+--------------------+-------+----------+---------------+---------------------+------------+
| networks           | false | list     | xml: networks | Assigns the domain to a network  |
|                    |       |          |               | by name. Each device is named    |
|                    |       |          | * name (req)  | with an incremented value (eth0) |
|                    |       |          | * ip          |                                  |
|                    |       |          | * mac         | .. note:: Network must exist     |
|                    |       |          |               |                                  |
+--------------------+-------+----------+---------------+---------------------+------------+
| image_src          | false | string   | virt-install  |                     |            |
+--------------------+-------+----------+---------------+---------------------+------------+
| network_bridge     | false | string   | virt-install  | virbr0              |            |
+--------------------+-------+----------+---------------+---------------------+------------+
| ssh_key            | false | string   | role          | resource_group_name |            |
+--------------------+-------+----------+---------------+---------------------+------------+
| remote_user        | false | string   | role          | ansible_user_id     |            |
+--------------------+-------+----------+---------------+---------------------+------------+
| cloud_config       | false | list     | role          | http://cloudinit.readthedocs.io  |
|                    |       |          |               | is used here                     |
+--------------------+-------+----------+---------------+---------------------+------------+
| additional_storage | false | string   | role          | 1G                  |            |
+--------------------+-------+----------+---------------+---------------------+------------+
| uri                | false | string   | module: uri   | qemu:///system      |            |
+--------------------+-------+----------+---------------+---------------------+------------+
| count              | false | string   | N/A           |                     |            |
+--------------------+-------+----------+---------------+---------------------+------------+

libvirt_network
---------------

Libvirt networks can be provisioned. If a :ref:`libvirt_network` is to be used
with a :ref:`libvirt_node`, it must precede it.

* :docs1.5:`Topology Example <workspace/topologies/libvirt-el7net.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/virt_net_module.html>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`libvirt_network` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`libvirt_network`
definition, the following options are available.

+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| Parameter          | req'd | type     | where used      | default             | comments                         |
+====================+=======+==========+=================+=====================+==================================+
| role               | true  | string   | role            |                     |                                  |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| name               | true  | string   | module: name    |                     |                                  |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| uri                | false | string   | module: name    |  qemu:///system     |                                  |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| ip                 | true  | string   | xml: ip         |                     |                                  |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| dhcp_start         | false | string   | xml: dhcp_start |                     |                                  |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| dhcp_end           | false | string   | xml: dhcp_end   |                     |                                  |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| domain             | false | string   | xml: domain     |                     | Automated DNS for guests         |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| forward_mode       | false | string   | xml: forward    | nat                 |                                  |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| forward_dev        | false | string   | xml: forward    |                     |                                  |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| bridge             | false | string   | xml: bridge     |                     |                                  |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+
| delete_on_destroy  | false | boolean  | N/A             | False               | If true, libvirt destroy will    |
|                    |       |          |                 |                     | destroy and undefine the network |
+--------------------+-------+----------+-----------------+---------------------+----------------------------------+

.. note:: This resource will not be torn down during a :term:`destroy` action.
   This is because other resources may depend on the now existing resource.

Additional Dependencies
-----------------------

The libvirt resource group requires several additional dependencies. The
following must be installed.

* libvirt-devel
* libguestfs-tools
* python-libguestfs
* libvirt-python
* python-lxml

For a Fedora 26 machine, the dependencies would be installed using dnf.

.. code-block:: bash

  $ sudo dnf install libvirt-devel libguestfs-tools python-libguestfs
  $ pip install linchpin[libvirt]

Additionally, because libvirt downloads images, certain SELinux libraries must
exist.

* libselinux-python

For a Fedora 26 machine, the dependencies would be installed using dnf.

.. code-block:: bash

  $ sudo dnf install libselinux-python

If using a python virtual environment, the selinux libraries must be symlinked. Assuming
a virtualenv of ``~/venv``, symlink the libraries.

.. code-block:: bash

  $ export LIBSELINUX_PATH=/usr/lib64/python2.7/site-packages
  $ ln -s ${LIBSELINUX_PATH}/selinux ~/venv/lib/python2.7/site-packages
  $ ln -s ${LIBSELINUX_PATH}/_selinux.so ~/venv/lib/python2.7/site-packages

Copying Images
--------------

New in version 1.5.1

By default, LinchPin manages the libvirt images in a directory that is accessible
only by the root user. However, adjustments can be made to allow an unprivileged
user to manage Libvirt via LinchPin. These settings can be modified in the
:docs1.5:`linchpin.conf <workspace/linchpin.conf>`

This configuration adjustment of `linchpin.conf` may work for the unprivileged
user `herlo`.

.. code-block:: cfg

    [evars]
    libvirt_image_path = ~/libvirt/images/
    libvirt_user = herlo
    libvirt_become = no

The directory will be created automatically by LinchPin. However, the user may
need additional rights, like group membership to access Libvirt. Please see
https://libvirt.org for any additional configurations.


Credentials Management
----------------------

.. include:: credentials/libvirt.rst
