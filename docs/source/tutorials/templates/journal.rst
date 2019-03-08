.. This is the template for the journal section of a provider tutorial
.. In the majority of cases, this file can be included directly.  If non-provider-specific changes must be
.. made, make them here instead of modifying the provider you're working on

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
