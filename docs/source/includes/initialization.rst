Running ``linchpin init`` will generate the :term:`workspace` directory structure, along with an example :term:`PinFile`, :term:`topology`, and :term:`layout` files. Performing the following tasks will generate a simple dummy folder with All in one PinFile which includes topology, and layout structure.

.. code-block:: bash

    $ pwd
    /tmp/workspace
    $ linchpin init
    Created destination workspace <path>
    $ tree

    ├── dummy
    │   ├── PinFile
    │   ├── PinFile.json
    │   └── README.rst
    └── linchpin.log
