Gcloud Topologies
==================

.. contents:: Topics

.. _gcloud_topologies:

Google Cloud Topologies
```````````````````````

.. code-block:: yaml
   
   ---
    topology_name: "ex_gcloud_topo1"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "gcloud"
        res_defs:
          - 
            res_name: "testresource"
            flavor: "n1-standard-1"
            res_type: "gcloud_gce"
            region: "us-central1-a"
            image: "centos-7"
            count: 1
        assoc_creds: "gcloudsk"
      - 
        resource_group_name: "testgroup2"
        res_group_type: "gcloud"
        res_defs:
          - 
            res_name: "testresource2"
            flavor: "n1-standard-1"
            res_type: "gcloud_gce"
            region: "us-central1-a"
            image: "centos-7"
            count: 2
        assoc_creds: "gcloudsk"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        Name: "TestInstanceGroup1"
        test_var1: "test_var1 msg is grp1 hello"
        test_var2: "test_var2 msg is grp1 hello"
        test_var3: "test_var3 msg is grp1 hello"
      - 
        resource_group_name : "testgroup2"
        Name: "TestInstanceGroup2"
        test_var1: "test_var1 msg is grp2 hello"
        test_var2: "test_var2 msg is grp2 hello"
        test_var3: "test_var3 msg is grp3 hello"


.. note::

  Source of the above mentioned examples can be found at `Example Topologies <https://github.com/CentOS-PaaS-SIG/linch-pin/tree/master/ex_topo>`_

