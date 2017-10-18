Openstack Topologies
====================

.. contents:: Topics

.. _openstack_topologies:

Openstack Server
````````````````

.. code-block:: yaml

   ---
    topology_name: "example_topo"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "openstack"
        res_defs:
          - 
            res_name: "ha_inst"
            flavor: "m1.small"
            res_type: "os_server"
            image: "rhel-6.5_jeos"
            count: 1
            keypair: "ci-factory"
            networks:
              - "e2e-openstack"
          - 
            res_name: "web_inst"
            flavor: "m1.small"
            res_type: "os_server"
            image: "rhel-6.5_jeos"
            count: 1
            keypair: "ci-factory"
            networks:
              - "e2e-openstack"
        assoc_creds: "cios_e2e-openstack"
      - 
        resource_group_name: "testgroup2"
        res_group_type: "openstack"
        res_defs:
          - res_name: "ano_inst"
            flavor: "m1.small"
            res_type: "os_server"
            image: "rhel-6.5_jeos"
            count: 1
            keypair: "ci-factory"
            networks:
              - "e2e-openstack"
        assoc_creds: "cios_e2e-openstack"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        test_var1: "test_var1 msg is grp1 hello "
        test_var2: "test_var2 msg is grp1 hello "
        test_var3: "test_var3 msg is grp1 hello "
      -
        resource_group_name : "testgroup2"
        test_var1: "test_var1 msg is grp2 hello"
        test_var2: "test_var2 msg is grp2 hello"
        test_var3: "test_var3 msg is grp2 hello"
      -
        resource_group_name : "testgroup3"
        test_var1: "test_var1 msg is grp3 hello"
        test_var2: "test_var2 msg is grp3 hello"
        test_var3: "test_var3 msg is grp3 hello"

Openstack Keypair
`````````````````
.. code-block:: yaml

   ---
    topology_name: "ex_os_keypair"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "openstack"
        res_defs:
          - res_name: "ex_keypair_sk"
            res_type: "os_keypair"
        assoc_creds: "cios_e2e-openstack"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        Name: "TestInstanceGroup1"
        test_var1: "test_var1 msg is grp1 hello"
        test_var2: "test_var2 msg is grp1 hello"
        test_var3: "test_var3 msg is grp1 hello"

Openstack Cinder Volume
```````````````````````

.. code-block:: yaml

   ---
    topology_name: "ex_os_vol"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "openstack"
        res_defs:
          - res_name: "test_volume_sk"
            res_type: "os_volume"
            size: 1
            count: 3
        assoc_creds: "cios_e2e-openstack"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        Name: "TestInstanceGroup1"
        test_var1: "test_var1 msg is grp1 hello"
        test_var2: "test_var2 msg is grp1 hello"
        test_var3: "test_var3 msg is grp1 hello"

Openstack Swift Container
`````````````````````````

.. code-block:: yaml

   ---
    topology_name: "ex_os_obj"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "openstack"
        res_defs:
          - res_name: "testcontainer_sk"
            res_type: "os_object"
            access: "public"
            count: 2
        assoc_creds: "cios_e2e-openstack"
      - 
        resource_group_name: "testgroup2"
        res_group_type: "openstack"
        res_defs:
          - res_name: "testit_sk"
            res_type: "os_object"
            access: "private"
            count: 2
        assoc_creds: "cios_e2e-openstack"
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
        test_var3: "test_var3 msg is grp2 hello"

Openstack Container & Volume
````````````````````````````

.. code-block:: yaml

   ---
    topology_name: "ex_os_obj_vol"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "openstack"
        res_defs:
          - res_name: "test_volume_sk"
            res_type: "os_volume"
            size: 2
            count: 3
          - res_name: "testcontainer_sk"
            res_type: "os_object"
            access: "public"
            count: 3
        assoc_creds: "cios_e2e-openstack"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        Name: "TestInstanceGroup1"
        test_var1: "test_var1 msg is grp1 hello"
        test_var2: "test_var2 msg is grp1 hello"
        test_var3: "test_var3 msg is grp1 hello"

Openstack Full Stack 
````````````````````

.. code-block:: yaml

   ---
    topology_name: "ex_os_heat_topo"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "openstack"
        res_defs:
          - 
            res_name: "ex_keypair_sk"
            res_type: "os_keypair"
          - 
            res_name: "os_heat_template_sample"
            res_type: "os_heat"
            template_path: "/path/to/hot_template_sample2.yaml"
          - res_name: "ano_inst"
            flavor: "m1.small"
            res_type: "os_server"
            image: "rhel-6.5_jeos"
            count: 2
            keypair: "ci-factory"
            networks:
              - "e2e-openstack"
        assoc_creds: "cios_e2e-openstack"
      - 
        resource_group_name: "testgroup2"
        res_group_type: "openstack"
        res_defs:
          - res_name: "test_volume_sk"
            res_type: "os_volume"
            size: 2
            count: 3
          - res_name: "testcontainer_sk"
            res_type: "os_object"
            access: "public"
            count: 3
        assoc_creds: "cios_e2e-openstack"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        Name: "TestInstanceGroup1"
        heat_params:
          key_name: "ci-factory"
          image_id: "rhel-6.5_jeos"
          instance_type: "m1.small"
          network_name: "e2e-openstack"
      - 
        resource_group_name : "testgroup2"
        Name: "TestInstanceGroup2"
        test_var1: "test_var1 msg is grp2 hello"
        test_var2: "test_var2 msg is grp2 hello"
        test_var3: "test_var3 msg is grp2 hello"


Credentials
```````````
* save openstack credentials in standard ``clouds.yml`` file using below
  format and save the directory path containing clouds.yml in environment variable ``CREDS_PATH``.

.. code-block:: yaml

   
   ---
    clouds: 
      devstack:
        auth:
          username: "admin"
          password: "Secret123"
          project_name: "my-tenant"
          auth_url: "http://192.168.122.33:5000/v2.0"
          
Topology
````````
* create topology file under ``$WORKSPACE/topologies/openstack_topology.yml``
  as show below:

.. code-block:: yaml

   ---
    topology_name: "osp-test"
    resource_groups:
      -
        resource_group_name: "lp-test"
        resource_group_type: "openstack"
        resource_definitions:
          - name: "test1"
            type: "os_server"
            flavor: "m1.small"
            image: "rhel-6.5_jeos"
            count: 1
            keypair: "ci-factory"
            networks:
              - "e2e-openstack"
            fip_pool: "192.168.122.1/24"
        credentials:
            filename: "clouds.yml"
            profile: "devstack"

Provision
`````````

* provision the above topology
      
.. code-block:: bash
   
   $ cd $WORKSPACE
   $ export CREDS_PATH="/path/to/credential_dir/"
   $ linchpin -v up 

 
* Alternatively one could pass credentials path as an argument to linchpin

.. code-block:: bash

   $ cd $WORKSPACE
   $ linchpin -v --creds-path /path/to/dir_containing_clouds.yml/ up
