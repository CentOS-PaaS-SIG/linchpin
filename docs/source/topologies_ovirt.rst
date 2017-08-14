oVirt Topologies
================

.. contents:: Topics

.. _ovirt_topologies:

oVirt Virtual Machines
``````````````````````

.. code-block:: yaml

    ---
    topology_name: "oVirt_vms_example_topology"
    resource_groups:
      -
        resource_group_name: "golden_env_mixed"
        resource_group_type: "ovirt"
        resource_definitions:
          -
            res_name: "virtio_1_0"
            res_type: "ovirt_vms"
            template: "golden_mixed_virtio_template"
            cluster: "golden_env_mixed_1"
          -
            res_name: "virtio_1_1"
            res_type: "ovirt_vms"
            template: "golden_mixed_virtio_template"
            cluster: "golden_env_mixed_1"
    
        credentials:
          filename: "ex_ovirt_creds.yml"
          profile: "ge2"

   
.. note::

  Source of the above mentioned examples can be found at `Example Topologies <https://github.com/CentOS-PaaS-SIG/linch-pin/tree/master/ex_topo>`_
