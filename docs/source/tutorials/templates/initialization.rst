.. This is the template for the initialization section of a provider tutorial
.. In the majority of cases, this file can be included directly.  If non-provider-specific changes must be
.. made, make them here instead of modifying the provider you're working on

Initialization
--------------

Assuming you are creating a workspace from scratch, you can run :code:`linchpin init` to initialize a workspace.  The following line of code will create a linchpin.conf, dummy PinFile, and README.rst in a directory called "simple"

.. code:: bash

	$ linchpin init simple

The PinFile contains a single target, called simple, which contains a topology but no layout.  A group of related provisioning tasks is called a target.  Each target has a topology, which can contain many resource groups, and an optional layout.  We'll explain what each of those means later on in further detail
