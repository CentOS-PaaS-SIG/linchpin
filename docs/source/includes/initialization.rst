Running ``linchpin init`` will generate the directory structure needed, along with an example :term:`PinFile`, :term:`topology`, and :term:`layout` files. Performing the following tasks will generate a simple dummy PinFile, topology, and layout structure.

.. code-block:: bash

    $ pwd
    /tmp/workspace
    $ linchpin init
    PinFile and file structure created at /tmp/workspace
    $ tree
    .
    ├── credentials
    ├── hooks
    ├── inventories
    ├── layouts
    │   └── dummy-layout.yml
    ├── PinFile
    └── topologies
        └── dummy-topology.yml



One important option here, is the :term:`workspace`. When passing this option, the system will use this as the location for the structure. The default is the current directory.

The next sections cover the Topology, Layout, and PinFile in a bit more detail.


