Running ``linchpin init`` will generate the :term:`workspace` directory structure, along with an example :term:`PinFile`, :term:`topology`, and :term:`layout` files. Performing the following tasks will generate a simple dummy PinFile, topology, and layout structure.

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

