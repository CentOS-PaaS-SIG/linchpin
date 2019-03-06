Provisioning OpenStack Server with linchpin
=================================================

LinchPin can be used to provision compute instances on OpenStack.  If you need to familiarize yourself with OpenStack Server, `read this`_. Now let's step through the process of creating a new workspace for provisioning OpenStack

.. _read this: https://developer.openstack.org/api-guide/compute/server_concepts.html

Fetch
-----

It is possible that you want to access a workspace that already exists.  If that workspace exists online, :code:`linchpin fetch` can be used to clone the repository. For example, the OpenShift on OpenStack example from release 1.7.2 in the linchpin repository can be cloned as follows:

.. code:: bash

	$ linchpin fetch --root docs/source/examples/workspaces openshift-on-openstack --branch 1.7.2 --dest ./fetch-example https://github.com/CentOS-PaaS-SIG/linchpin

You can even choose to fetch only a certain component of the workspace.  For example, if you only wish to fetch the topologies you can add :code:`--type topologies`.  If you were able to fetch a complete workspace, you can skip to `Up`_

Initialization
--------------

Assuming you are creating a workspace from scratch, you can run :code:`linchpin init` to initialize a workspace.  The following line of code will create a linchpin.conf, dummy PinFile, and README.rst in a directory called "simple"

.. code:: bash

	$ linchpin init simple

The PinFile contains a single target, called simple, which contains a topology but no layout.  A group of related provisioning tasks is called a target.  Each target has a topology, which can contain many resource groups, and an optional layout.  We'll explain what each of those means later on in further detail

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

After provisioning the hosts, LinchPin will iterate through each host type in the inventory_layout, pop :code:`count` hosts off of the list, and add them to the relevant host groups.  The :code:`host_groups` section of the layout is used to set environment variables for each of the hosts in a given host group

Credentials
-----------

Finally, we need to add credentials to the resource group.  OpenStack provides several ways to provide credentials. LinchPin supports some of these methods for passing credentials for use with OpenStack resources.

Environment Variables
`````````````````````

LinchPin honors the OpenStack environment variables such as ``$OS_USERNAME``,
``$OS_PROJECT_NAME``, etc.

See `the OpenStack documentation cli documentation 
<https://docs.openstack.org/python-openstackclient/pike/cli/man/openstack.html#manpage>`_
for details.

.. note:: No credentials files are needed for this method. When LinchPin calls
   the OpenStack provider, the environment variables are automatically picked
   up by the OpenStack Ansible modules, and passed to OpenStack for
   authentication.

Using OpenStack Credentials
```````````````````````````

OpenStack provides a simple file structure using a file called
`clouds.yaml <https://docs.openstack.org/os-client-config/latest/user/configuration.html>`_,
to provide authentication to a particular tenant. A single clouds.yaml file might contain several entries.

.. code-block:: yaml

    clouds:
      devstack:
        auth:
          auth_url: http://192.168.122.10:35357/
          project_name: demo
          username: demo
          password: 0penstack
        region_name: RegionOne
      trystack:
        auth:
          auth_url: http://auth.trystack.com:8080/
          project_name: trystack
          username: herlo-trystack-3855e889
          password: thepasswordissecrte

Using this mechanism requires that credentials data be passed into LinchPin.

An OpenStack topology can have a ``credentials`` section for each
:term:`resource_group`, which requires the filename, and the profile name.

It's worth noting that we can't give you credentials to use, so you'll have to provide
your own filename and profile here.  By default, LinchPin searches for the filename in
{{ workspace }}/credentials but can be made to search other places by setting the
:code:`evars.default_credentials_path` variable in your linchpin.conf.  The credentials
path can also be overridden by using the :code:`--creds-path` flag.

.. code-block:: yaml

    ---
    topology_name: topo
    resource_groups:
      - resource_group_name: openstack
        resource_group_type: openstack
        resource_definitions:

          .. snip ..

        credentials:
          filename: clouds.yaml
          profile: devstack


Up
--

Once the resources have been defined, LinchPin can be run as follows:

.. code:: bash

	$ linchpin --workspace . -vv up simple

The :code:`--workspace` flag references the relevant workspace.  By default, the workspace is
the current working directory.  If the PinFile has a name (or path) other than {{workspace}}/PinFile,
the :code:`--pinfile` flag can override that.  Finally, :code:`-vv` sets a verbosity level of 2.  As
with Ansible, the verbosity can be set between 0 and 4.

If the provisioning was successful, you should see some output at the bottom that looks something like this:

.. code:: bash

	ID: 122
	Action: up

	Target              	Run ID	uHash	Exit Code 
	-------------------------------------------------
	simple              	   1	3a0c59	        0

You can use that uhash value to get the inventory generated according to the layout we discussed above.  The file will be titled :code:`inventories/${target}-${uhash}` but you can change this naming schema by editing the :code:`inventory_file` field in the :code:`inventory_layout` section of the layout.  When :code:`linchpin up` is run, each target will generate its own inventory layout.  The inventories folder and inventory_path can also be set in the :term:`evars` section of linchpin.conf


Destroy
-------

At some point you'll no longer need the machines you provisioned.  You can destroy the provisioned machines with :code:`linchpin destroy`.  However, you may not want to remove every single target from your last provision.  For example, lets say you ran the simple provision above, then ran a few others.  You could use the :term:`transaction ID`, labeled "ID" above, to do so.

.. code:: bash

	$ linchpin -vv destroy -t 122

You may also have provisioned multiple targets at once.  If you only want to destroy one of them, you can do so with the name of the target and the :term:`run ID`.

.. code:: bash

	$ linchpin -vv destroy -r 1 simple

Journal
-------

Each time you provision or destroy resources with LinchPin, information about the run is stored in the Run Database, or RunDB.  Data from the RunDB can be printed using :code:`linchpin journal`.  This allows you to keep track of which resources you have provisioned but haven't destroyed and gather the transaction and run IDs for those resources.  To list each resource by target, simply run:

.. code:: bash

	$ linchpin journal

	Target: simple
	run_id	    action	     uhash	        rc	
	--------------------------------------------------
	2      	  destroy	   bb8064	        0	
	1      	       up	   bb8064	        0	

	Target: beaker-openstack
	run_id	    action	     uhash	        rc	
	--------------------------------------------------
	2      	  destroy	   b1e364	        2	
	1      	       up	   b1e364	        2	

	Target: os-subnet
	run_id	    action	     uhash	        rc	
	--------------------------------------------------
	3      	  destroy	   c619ac	        0	
	2      	       up	   c619ac	        0	
	1      	  destroy	   ab9d81	        0	

As you can see, linchpin printed out the run data for the :code:`simple` target that we provisioned and destroyed above, but also printed out information for a number of other targets which had been provisioned recently.  You can provide a target as an argument to only print out the given target.  You can also group by transaction id with the flag :code:`--view tx`.  `Click here to read more about linchpin journal`_

.. _Click here to read more about linchpin journal: ../linchpin_journal.rst
