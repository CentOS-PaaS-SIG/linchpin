The :term:`topology` is declarative, written in YAML or JSON (v1.5+), and defines how the provisioned systems should look after executing the ``linchpin up`` command. A simple **dummy** topology is shown here.

.. code-block:: yaml

    ---
    topology_name: "dummy_cluster" # topology name
    resource_groups:
      - resource_group_name: "dummy"
        resource_group_type: "dummy"
        resource_definitions:
          - name: "web"
            role: "dummy_node"
            count: 1

This topology describes a single dummy system that will be provisioned when `linchpin up` is executed. Once provisioned, the resources outputs are stored for reference and later lookup. Additional topology examples can be found in :dirs1.5:`the source code <workspace/topologies>`.

.. FIXME: Update/Remove topologies. One per provider.

