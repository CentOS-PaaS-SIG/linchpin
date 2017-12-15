Once a :term:`PinFile`, :term:`topology`, and optional :term:`layout` are in place, provisioning can happen. Performing the command ``linchpin up`` should provision the :term:`resources` and :term:`inventory` files based upon the :term:`topology_name` value. In this case, is ``dummy_cluster``.

.. code-block:: bash

    $ linchpin up
    target: dummy_cluster, action: up
    Action 'up' on Target 'dummy_cluster' is complete

    Target              Run ID  uHash       Exit Code
    -------------------------------------------------
    dummy_cluster       70      0446                0

As you can see, the generated inventory file has the right data. This can be used in many ways, which will be covered elsewhere in the documentation.

.. code-block:: bash

    $ cat inventories/dummy_cluster-0446.inventory
    [example]
    web-0446-0.example.net hostname=web-0446-0.example.net

    [all]
    web-0446-0.example.net hostname=web-0446-0.example.net

To verify resources with the dummy cluster, check ``/tmp/dummy.hosts``

.. code-block:: bash

    $ cat /tmp/dummy.hosts
    web-0446-0.example.net
    test-0446-0.example.net


