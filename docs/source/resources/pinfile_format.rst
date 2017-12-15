A PinFile can be in YAML format as above. In v1.5, JSON formatting was introduced.

.. code-block:: json

    {
        "dummy": {
            "topology": "dummy.yml",
            "layout": "dummy.yml"
        }
    }


Additionally in v1.5, an all-in-one PinFile option was introduced. Consider the following ``topology``, ``layout`` and ``PinFile``.

.. code-block:: yaml

    $ cat topologies/dummy-topology.yml
    ---
    topology_name: "dummy_cluster" # topology name
    resource_groups:
      - resource_group_name: "dummy"
        resource_group_type: "dummy"
        resource_definitions:
          - name: "web"
            role: "dummy_node"
            count: 1

.. code-block:: yaml

    $ cat layouts/dummy-layout.yml
    ---
    inventory_layout:
      vars:
        hostname: __IP__
      hosts:
        example-node:
          count: 1
          host_groups:
            - example

.. code-block:: yaml

    dummy_cluster:
      topology: dummy-topology.yml
      layout: dummy-layout.yml

The result of combining a `topology` and `layout` into one file is possibly cleaner.

.. code-block:: yaml

    dummy_cluster:
        topology:
            topology_name: "dummy_cluster" # topology name
            resource_groups:
              - resource_group_name: "dummy"
                resource_group_type: "dummy"
                resource_definitions:
                  - name: "web"
                    role: "dummy_node"
                    count: 1
        layout:
            inventory_layout:
              vars:
                hostname: __IP__
              hosts:
                example-node:
                  count: 1
                  host_groups:
                    - example

As previously mentioned, starting in v1.5, the :term:`PinFile`, :term:`topology`,
and :term:`layout` can be represented in JSON. A combined JSON file is also possible.

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
                            "count": 1,
                            "host_groups": [
                                "example"
                            ]
                        }
                    }
                }
            }
        }
    }

