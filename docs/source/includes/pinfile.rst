A :term:`PinFile` takes a :term:`topology` and an optional :term:`layout`, among other options, as a combined set of configurations as a resource for provisioning. An example :term:`Pinfile` is shown.

.. code-block:: yaml

    dummy_cluster:
      topology: dummy-topology.yml
      layout: dummy-layout.yml

The :term:`PinFile` collects the given :term:`topology` and :term:`layout` into one place. Many :term:`targets <target>` can be referenced in a single :term:`PinFile`.

Starting in v1.5+, the :term:`PinFile` can also use JSON.

.. code-block:: json

    {
        "dummy": {
            "topology": "dummy-topology.yml",
            "layout:": "dummy-layout.yml"
        }
    }



Additionally, both the topology, and layout can be included inline.

.. code-block:: json

    {
        "dummy": {
            "topology": {
                "resource_groups": [
                    {
                        "resource_definitions": [
                            {
                                "count": 3,
                                "name": "web",
                                "role": "dummy_node"
                            }
                        ],
                        "resource_group_name": "dummy",
                        "resource_group_type": "dummy"
                    }
                ],
                "topology_name": "dummy_cluster"
            },
            "layout": {
                "inventory_layout": {
                    "hosts": {
                        "example-node": {
                            "count": 3, 
                            "host_groups": [
                                "example"
                            ]
                        }
                    },
                    "vars": {
                        "hostname": "__IP__"
                    }
                }
            }
        }
    }



