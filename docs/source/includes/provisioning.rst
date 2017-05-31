Once a :term:`PinFile`, :term:`topology`, and optionally a :term:`layout` are in place, provisioning can happen.

.. note:: For this section, the dummy tooling will be used as it is much
    simpler and doesn't require anything extra to be configured. The dummy
    provider creates a temporary file, which represents provisioned hosts.
    If the temporary file does not have any data, hosts have not been
    provisioned, or they have been recently destroyed.

The dummy :term:`topology`, :term:`layout`, and :term:`PinFile` are shown above in the appropriate sections. The tree would be very simple.

.. code-block:: bash

    $ tree
    .
    ├── inventories
    ├── layouts
    │   └── dummy-layout.yml
    ├── PinFile
    ├── resources
    └── topologies
        └── dummy-cluster.yml

Performing the command ``linchpin up`` should generate :term:`resources` and :term:`inventory` files based upon the :term:`topology_name` value. In this case, is ``dummy_cluster``.

.. code-block:: bash

    $ linchpin up
    target: dummy1, action: up

    $ ls {resources,inventories}/dummy*
    inventories/dummy_cluster.inventory  resources/dummy_cluster.output

To verify resources with the dummy cluster, check ``/tmp/dummy.hosts``

.. code-block:: bash

    $ cat /tmp/dummy.hosts
    web-0.example.net
    web-1.example.net
    web-2.example.net

This is reflected in both the :term:`resources` (not shown) and :term:`inventory` files.

.. code-block:: cfg

    [example:vars]
    test = one

    [example]
    web-2.example.net hostname=web-2.example.net
    web-1.example.net hostname=web-1.example.net
    web-0.example.net hostname=web-0.example.net

    [all]
    web-2.example.net hostname=web-2.example.net
    web-1.example.net hostname=web-1.example.net
    web-0.example.net hostname=web-0.example.net

