.. This is the template for the fetch section of a provider tutorial
.. In the majority of cases, this file can be included directly.  If non-provider-specific changes must be
.. made, make them here instead of modifying the provider you're working on

Fetch
-----

It is possible that you want to access a workspace that already exists.  If that workspace exists online, :code:`linchpin fetch` can be used to clone the repository. For example, the OpenShift on OpenStack example from release 1.7.2 in the linchpin repository can be cloned as follows:

.. code:: bash

	$ linchpin fetch --root docs/source/examples/workspaces openshift-on-openstack --branch 1.7.2 --dest ./fetch-example https://github.com/CentOS-PaaS-SIG/linchpin

You can even choose to fetch only a certain component of the workspace.  For example, if you only wish to fetch the topologies you can add :code:`--type topologies`.  If you were able to fetch a complete workspace, you can skip to `Up`_
