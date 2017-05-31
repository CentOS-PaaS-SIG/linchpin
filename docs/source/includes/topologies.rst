The :term:`topology` is a set of rules, written in YAML, that define the way the provisioned systems should look after executing linchpin. Generally, the :term:`topology` and :term:`topology_file <topology>` values are interchangeable, except where the YAML is specifically indicated. A simple **dummy** topology is shown here.

.. code-block:: yaml

    ---
    topology_name: "dummy_cluster" # topology name
    resource_groups:
      -
        resource_group_name: "dummy"
        resource_group_type: "dummy"
        resource_definitions:
          -
            name: "web"
            type: "dummy_node"
            count: 3

This topology describes a set of three (3) dummy systems that will be provisioned when `linchpin up` is executed. The names of the systems will be 'web_#.example.net', where ``#`` indicates the count (usually `0`, `1`, and `2`). Once provisioned, the resources will be output and stored for reference. The output :term:`resources` data can then be used to generated an inventory, or passed as part of a `linchpin destroy` action.


