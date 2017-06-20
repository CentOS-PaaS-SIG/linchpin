Beaker Topologies
=================

.. contents:: Topics

.. _beaker_topologies:


Beaker Server
`````````````

.. code-block:: yaml

    ---
    topology_name: beaker
    resource_groups:
      - resource_group_name: test1
        res_group_type: beaker
        job_group: your-beaker-group
        whiteboard: Arbitrary Job whiteboard string
        recipesets:
          - distro: RHEL-6.5
            arch: x86_64
            keyvalue:
              - MEMORY>1000
              - DISKSPACE>20000
            hostrequires:
              - tag: processors
                op: ">="
                value: 4
              - tag: device
                op: "="
                type: "network"
            count: 1

.. note::

  Source of the above Beaker example can be found at `Example Topologies <https://github.com/CentOS-PaaS-SIG/linch-pin/tree/master/examples/topology>`_

Requiring Specific Hosts
````````````````````````

By default, any host available to your beaker user can be selected for use in a given job.
If a specific host, or hosts, is desired, ``hostrequires`` filters can be used to refine the hosts
selected for use in a given job.

Force a Specific Host
^^^^^^^^^^^^^^^^^^^^^

The reservation of a specific hostname can be done with the ``force`` keyword nested within a
recipeset's ``hostrequires`` mapping. Additional filtering,
such as a ``keyvalue`` or ``hostrequires`` filter, is silently ignored by beaker when the hostname
to reserve is forced. Because of this, using the ``force`` argument is mutually exclusive to using
any other filters.

For example::

    hostrequires:
      force: beaker.machine.hostname

Select from a named System Pool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Beaker also supports provisioning from a named system pool::

    hostrequires:
      - tag: pool
        op: "="
        value: system-pool-name

This filter will automatically select a system from the named system pool, but unlike the ``force``
keyword additional filters will also be applied.

.. note::

    The "op" keyword of a hostrequires filter should be quoted when the operator contains symbols,
    such as "==", "!=", or ">=".
