Provisioning Beaker Server with LinchPin
=================================================

LinchPin can be used to provision compute instances on Beaker.  If you need to familiarize yourself with Beaker Server, `read this`_. Now let's step through the process of creating a new workspace for provisioning Beaker

.. _read this: https://beaker-project.org/docs/server-api/

.. include:: templates/fetch.rst

.. include:: templates/initialization.rst

Creating a Topology
-------------------

Now that we have a PinFile, its time to add the code for a Beaker server.  Edit your PinFile so it looks like the one below.

.. code:: yaml

    simple:
      topology:
        topology_name: simple
        resource_groups:
          - resource_group_name: bkr_simple
            resource_group_type: beaker
            resource_definitions:
              - role: bkr_server
				recipesets:
				  - distro: RHEL-7.5
					name: rhelsimple
					arch: x86_64
					variant: Server
					count: 1
					hostrequires:
					  - rawxml: '<key_value key="model" op="=" value="KVM"/>'

There are a number of other fields available for these two roles.  Information about those fields as well as the other Beaker roles can be found on the `Beaker provider page`_.

A :term:`resource group` is a group of resources related to a single provider.  In this example we have a Beaker resource group that defines two different types of Beaker resources.  We could also define an AWS resource group below it that provisions a handful of EC2 nodes.  A single resource group can contain many :term:`resource definitions`. A resource definition details the requirements for a specific resource. Multiple resources can be provisioned from a single resource definition by editing the count field, but all non-unique properties of the resources will be identical. So the distro will be the same, but each node will have a unique name. The name will be {{ name }}_0, {{ name }}_1, etc. from 0 to count.

.. _Beaker provider page: ../beaker.rst

Credentials
-----------

Finally, we need to add credentials to the resource group.

.. include:: ../credentials/beaker.rst

.. include:: templates/layout.rst

.. include:: templates/up.rst

.. include:: templates/destroy.rst

.. include:: templates/journal.rst
