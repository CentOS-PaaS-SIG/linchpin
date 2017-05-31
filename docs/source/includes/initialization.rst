Running ``linchpin init`` will generate the directory structure needed, along with an example :term:`PinFile`, :term:`topology`, and :term:`layout` files. One important option here, is the :term:`--workspace <workspace>`. When passing this option, the system will use this as the location for the structure. The default is the current directory.

.. code-block:: bash

    $ export WORKSPACE=/tmp/workspace
    $ linchpin init
    PinFile and file structure created at /tmp/workspace
    $ cd /tmp/workspace/
    $ tree
    .
    ├── credentials
    ├── hooks
    ├── inventories
    ├── layouts
    │   └── example-layout.yml
    ├── PinFile
    ├── resources
    └── topologies
        └── example-topology.yml

At this point, one could execute ``linchpin up`` and provision a single libvirt virtual machine, with a network named `linchpin-centos71`. An inventory would be generated and placed in ``inventories/libvirt.inventory``. This can be known by reading the ``topologies/example-topology.yml`` and gleaning out the `topology_name` value.

