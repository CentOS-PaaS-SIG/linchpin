.. This is the template for the up section of a provider tutorial
.. In the majority of cases, this file can be included directly.  If non-provider-specific changes must be
.. made, make them here instead of modifying the provider you're working on

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

