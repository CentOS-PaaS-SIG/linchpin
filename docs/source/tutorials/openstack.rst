Provisioning OpenStack Server with LinchPin
=================================================

LinchPin can be used to provision compute instances on OpenStack.  If you need to familiarize yourself with OpenStack Server, `read this`_. Now let's step through the process of creating a new workspace for provisioning OpenStack

.. _read this: https://developer.openstack.org/api-guide/compute/server_concepts.html

.. include:: templates/fetch.rst

.. include:: templates/initialization.rst

Creating a Topology
-------------------

Now that we have a PinFile, its time to add the code for an OpenStack server.  Edit your PinFile so it looks like the one below.

.. code:: yaml

    simple:
      topology:
        topology_name: simple
        resource_groups:
          - resource_group_name: os_simple
            resource_group_type: openstack
            resource_definitions:
              - name: simple_keypair
                role: os_keypair
              - name: simple_server
                role: os_server
                flavor: m1.small
                keypair: simple_keypair
                count: 1

There are a number of other fields available for these two roles.  Information about those fields as well as the other OpenStack roles can be found on the `OpenStack provider page`_.

A :term:`resource group` is a group of resources related to a single provider.  In this example we have an openstack resource group that defines two different types of openstack resources.  We could also define an AWS resource group below it that provisions a handful of EC2 nodes.  A single resource group can contain many :term:`resource definitions`. A resource definition details the requirements for a specific resource.  Multiple resources can be provisioned from a single resource definition by editing the :code:`count` field, but all non-unique properties of the resources will be identical.

.. _openstack provider page: ../openstack.rst

Credentials
-----------

Finally, we need to add credentials to the resource group.  OpenStack provides several ways to provide credentials. LinchPin supports some of these methods for passing credentials for use with OpenStack resources.

.. include:: ../credentials/openstack.rst

.. include:: templates/layout.rst

.. include:: templates/up.rst

.. include:: templates/destroy.rst

.. include:: templates/journal.rst
