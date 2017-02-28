Beaker Topologies
=================

.. contents:: Topics

.. _beaker_topologies:


Simple Beaker Topology
`````````````````````````

.. code-block:: yaml

    ---
    topology_name: beaker
    resource_groups:
      - resource_group_name: test1
        res_group_type: beaker
        job_group: ci-ops-central
        recipesets:
          - distro: RHEL-6.5
            arch: x86_64
            arches:
              - X86_64
              - X86_64
            keyvalue:
              - MEMORY>1000
              - DISKSPACE>20000
            hostrequire:
              - arch=X86_64
            count: 1

.. note:: For more details about beaker and its components, please visit the
    `documentation <https://beaker-project.org/docs/>`_.
