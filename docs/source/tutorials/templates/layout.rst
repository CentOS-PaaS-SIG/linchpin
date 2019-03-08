.. This is the template for the layouts section of a provider tutorial
.. In the majority of cases, this file can be included directly.  If non-provider-specific changes must be
.. made, make them here instead of modifying the provider you're working on

Creating a Layout
-----------------

LinchPin can use layouts to describe what an Ansible inventory might look like after provisioning.  Layouts can include information such as IP addresses, zones, and FQDNs.  Under the simple key, put the following data:

.. code:: yaml

	layout:
	  inventory_layout:
		vars:
		  hostname: __IP__
	  	hosts:
		  server:
			count: 1
			host_groups:
			  - frontent
	  host_groups:
		all:
		  vars:
			ansible_user: root
		frontend:
		  vars:

After provisioning the hosts, LinchPin will through each host type in the inventory_layout, pop :code:`count` hosts off of the list, and add them to the relevant host groups.  The :code:`host_groups` section of the layout is used to set environment variables for each of the hosts in a given host group
