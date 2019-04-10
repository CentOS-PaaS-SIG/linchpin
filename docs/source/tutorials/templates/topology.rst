.. This is the template for the topology section of a provider tutorial
.. You can't include this verbatim as you could with templates/fetch.rst, but you can use it as a starting point

Creating a Topology
-------------------

Now that we have a PinFile, its time to add the code for an OpenStack server.  Edit your PinFile so it looks like the one below.

.. code:: yaml

	simple:
	  topology:
		{{ topology data }}

There are a number of other fields available for these two roles.  Information about those fields as well as the other OpenStack roles can be found on the `{{ provider }} provider page`_.

A :term:`resource group` is a group of resources related to a single provider.  In this example we have an {{ provider }} resource group that defines two different types of {{ provider }} resources.  We could also define an AWS resource group below it that provisions a handful of EC2 nodes.  A single resource group can contain many :term:`resource definitions`. A resource definition details the requirements for a specific resource.  Multiple resources can be provisioned from a single resource definition by editing the :code:`count` field, but all non-unique properties of the resources will be identical.

.. _{{ provider }} provider page: ../{{ provider }}.rst
