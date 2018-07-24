An :term:`inventory_layout` (or :term:`layout`) is written in YAML or JSON (v1.5+), and defines how the provisioned resources should look in an Ansible static inventory file. The inventory is generated from the resources provisioned by the topology and the layout data. A layout is shown here.

.. code-block:: yaml

    ---
    inventory_layout:
      vars:
        hostname: __IP__
      hosts:
        example-node:
          count: 1
          host_groups:
            - example

The above YAML allows for interpolation of the ip address, or hostname as a component of a generated inventory. A host group called `example` will be added to the Ansible static inventory. The `all` group always exists, and includes all provisioned hosts.

.. code-block:: bash

    $ cat inventories/dummy_cluster-0446.inventory
    [example]
    web-0446-0.example.net hostname=web-0446-0.example.net

    [all]
    web-0446-0.example.net hostname=web-0446-0.example.net

.. note:: A keen observer might notice the filename and hostname are appended with ``-0446``. This value is called the :term:`uhash` or unique-ish hash. Most providers allow for unique identifiers to be assigned automatically to each hostname as well as the inventory name. This provides a flexible way to repeat the process, but manage multiple resource sets at the same time.

Advanced layout examples can be found by reading :ref:`ra_inventory_layouts`.

.. note:: Additional layout examples can be found in :dirs1.5:`the source code <workspace/layouts>`.

