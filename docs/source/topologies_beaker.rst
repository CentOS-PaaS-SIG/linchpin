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
        job_group: ci-ops-central
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

By default, any host available to the named ``job_group`` can be selected for use in a given job.
If a specific host, or hosts, is desired, ``hostrequires`` filters can be used to refine the hosts
selected for use in a given job.

The reservation of a specific hostname can be done with the ``force`` keyword nested within a
recipeset's ``hostrequires`` mapping. Additional filtering,
such as a ``keyvalue`` or ``hostrequires`` filter, is silently ignored by beaker when the hostname
to reserve is forced. Because of this, using the ``force`` argument is mutually exclusive to using
any other filters.

For example::

    hostrequires:
      - force: beaker.machine.hostname

Beaker supports globbing via the "like" operator::

    hostrequires:
      - tag: hostname
        op: like
        value: beaker-%.machine.hostname

This glob will match hostnames like ``beaker-01.machine.hostname``, allowing you to select from
a subset of machines available in the given job group. This acts like any other "hostrequires"
filter, so it can be combined with those filters to futher ensure that only nodes with required
cababilities are selected for a job (unlike when ``force`` is used).

.. note::

    The "op" keyword of a hostrequires filter should be quoted when the operator contains symbols,
    such as "==", "!=", or ">=".
