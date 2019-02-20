A :term:`PinFile` takes a :term:`topology` and an optional :term:`layout`, among other options, as a combined set of configurations as a resource for provisioning. An example :term:`Pinfile` is shown.

.. code-block:: yaml
    
    # Example 1
    dummy_cluster:
      topology: dummy-topology.yml
      layout: dummy-layout.yml

    # Example 2
    dummy-topo:
      topology:
        topology_name: "dummy_cluster" # topology name
        resource_groups:
        - resource_group_name: "dummy"
          resource_group_type: "dummy"
          resource_definitions:
          - name: "{{ distro | default('') }}web"
            role: "dummy_node"
            count: 3
          - name: "{{ distro | default('') }}test"
            role: "dummy_node"
            count: 1
      layout:
        inventory_layout:
          vars:
            hostname: __IP__
          hosts:
            example-node:
              count: 3
              host_groups:
              - example
            test-node:
              count: 1
              host_groups:
              - test

The :term:`PinFile` collects the given :term:`topology` and :term:`layout` into one place. Many :term:`targets <target>` can be referenced in a single :term:`PinFile`.

More detail about the PinFile can be found in the :ref:`res_pinfiles` document.

Additional PinFile examples can be found in :dirs1.5:`the source code <workspace>`


