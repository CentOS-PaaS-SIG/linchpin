Duffy Topologies
==============

.. contents:: Topics

.. _duffy_topologies:


Simple Duffy Cluster
`````````````````````````

.. code-block:: yaml

    ---
    topology_name: "duffy_3node_cluster"
    resource_groups:
      -
        resource_group_name: "3node"
        res_group_type: "duffy"
        res_defs:
          -
            res_name: "duffy_nodes"
            res_type: "duffy"
            version: 7
            arch: "x86_64"
            count: 3
        assoc_creds: "duffy_creds"

.. note:: the reference to ``duffy_creds`` defaults to using an assumed file
    in the user's home directory called ``duffy.key``, and points to an
    internal service at http://admin.ci.centos.org:8080. The credentials
    themselves are held in the ``duffy.key`` file.
