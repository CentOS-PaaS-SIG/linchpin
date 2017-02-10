AWS Topologies
==============

.. contents:: Topics

.. _aws_topologies:


AWS EC2 Multiple Accounts
`````````````````````````

.. code-block:: yaml

    ---
    topology_name: "ex_aws_topo"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "aws"
        res_defs:
          - 
            res_name: "ha_inst"
            flavor: "t1.micro"
            res_type: "aws_ec2"
            region: "us-west-2"
            image: "ami-014cb561"
            count: 1
            keypair: "libra"
        assoc_creds: "master_aws_creds"
      - 
        resource_group_name: "testgroup2"
        res_group_type: "aws"
        res_defs:
          - 
            res_name: "ha_inst2"
            flavor: "t1.micro"
            res_type: "aws_ec2"
            region: "us-east-1"
            image: "ami-00a7636d"
            count: 2
            keypair: "libra"
        assoc_creds: "master_aws_creds"
      - 
        resource_group_name: "testgroup3"
        res_group_type: "aws"
        res_defs:
          - 
            res_name: "ha_inst2"
            flavor: "t1.micro"
            res_type: "aws_ec2"
            region: "us-east-1"
            image: "ami-00a7636d"
            count: 1
            keypair: "libra"
        assoc_creds: "sk_aws_creds"
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
      - 
        resource_group_name : "testgroup3"
        Name: "TestInstanceGroup3"
        test_var1: "test_var1 msg is grp3 hello"
        test_var2: "test_var2 msg is grp3 hello"
        test_var3: "test_var3 msg is grp3 hello"
      - 
        resource_group_name : "testgroup4"
        Name: "TestInstanceGroup4"
        test_var1: "test_var1 msg is grp4 hello"
        test_var2: "test_var2 msg is grp4 hello"
        test_var3: "test_var3 msg is grp4 hello"

AWS EC2 Keypair
```````````````

.. code-block:: yaml
   
    ---
    topology_name: "ex_aws_keypair_topo"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "aws"
        res_defs:
          - res_name: "ex_keypair_sk"
            res_type: "aws_ec2_key"
            region: "us-west-2"
        assoc_creds: "sk_aws_personal"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        Name: "TestInstanceGroup1"
        test_var1: "test_var1 msg is grp1 hello"
        test_var2: "test_var2 msg is grp1 hello"
        test_var3: "test_var3 msg is grp1 hello"

AWS CFN EXAMPLE1
````````````````

.. code-block:: yaml
   
    ---
    topology_name: "ex_cfn_topo"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "aws"
        res_defs:
          - 
            res_name: "cfnsimplestackaws"
            res_type: "aws_cfn"
            region: "us-east-1"
            template_path: "/path/to/cfn_template"
        assoc_creds: "sk_aws_personal"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        Name: "TestInstanceGroup1"
        cfn_params:
          KeyName: "sk_key"
          InstanceType: "t2.micro"


AWS CFN EXAMPLE2
`````````````````

.. code-block:: yaml
       
    ---
    topology_name: "ex_cfn_topo2"
    site: "qeos"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "aws"
        res_defs:
          - 
            res_name: "cfnsimplestackaws"
            res_type: "aws_cfn"
            region: "us-east-1"
            template_path: "/path/to/ec2_sample_cfn.template"
        assoc_creds: "sk_aws_personal"
      - 
        resource_group_name: "testgroup2"
        res_group_type: "aws"
        res_defs:
          - 
            res_name: "ha_inst2"
            flavor: "t2.micro"
            res_type: "aws_ec2"
            region: "us-east-1"
            image: "ami-fce3c696"
            count: 2
            keypair: "sk_key"
        assoc_creds: "sk_aws_personal"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        Name: "TestInstanceGroup1"
        cfn_params:
          KeyName: "sk_key"
          InstanceType: "t2.micro"
      - 
        resource_group_name : "testgroup2"
        Name: "TestInstanceGroup2"
        test_var1: "test_var1 msg is grp2 hello"
        test_var2: "test_var2 msg is grp2 hello"
        test_var3: "test_var3 msg is grp2 hello"


AWS FULLSTACK EXAMPLE
`````````````````````

.. code-block:: yaml
 
    ---
    topology_name: "ex_aws_full_stack"
    site: "testsite"
    resource_groups:
      - 
        resource_group_name: "testgroup1"
        res_group_type: "aws"
        res_defs:
          - 
            res_name: "ha_inst2"
            flavor: "t2.micro"
            res_type: "aws_ec2"
            region: "us-east-1"
            image: "ami-fce3c696"
            count: 1
            keypair: "sk_key"
          - 
            res_name: "samvaranbucktest"
            res_type: "aws_s3"
            region: "us-west-2"
          - 
            res_name: "ex_keypair_sk"
            res_type: "aws_ec2_key"
            region: "us-west-2"
        assoc_creds: "sk_aws_personal"
      - 
        resource_group_name: "testgroup2"
        res_group_type: "aws"
        res_defs:
          - 
            res_name: "cfnsimplestackaws"
            res_type: "aws_cfn"
            region: "us-east-1"
            template_path: "/path/to/ec2_sample_cfn.template"
        assoc_creds: "sk_aws_personal"
    resource_group_vars:
      - 
        resource_group_name : "testgroup1"
        Name: "TestInstanceGroup1"
        test_var1: "test_var1 msg is grp1 hello"
        test_var2: "test_var2 msg is grp1 hello"
        test_var3: "test_var3 msg is grp1 hello"
      - 
        resource_group_name : "testgroup2"
        Name: "TestInstanceGroup1"
        cfn_params:
          KeyName: "sk_key"
          InstanceType: "t2.micro"


.. note::

  Source of the above mentioned examples can be found at `Example Topologies <https://github.com/CentOS-PaaS-SIG/linch-pin/tree/master/ex_topo>`_

AWS EC2 Security Groups EXAMPLE
````````````````````````````````

.. code-block:: yaml

    ---
    topology_name: "aws_sg_topology"
    resource_groups:
      -
        resource_group_name: "awssgtest"
        res_group_type: "aws"
        res_defs:
          -
            res_name: "aws_test_sg"
            res_type: "aws_sg"
            description: "AWS Security Group with ssh access"
            region: "us-east-1"
            rules:
           -
             rule_type: "inbound"
             from_port: 8 # type 8 is ICMP echo request
             to_port: -1
             proto: "icmp"
             cidr_ip: "0.0.0.0/0"
           -
             rule_type: "inbound"
             from_port: 22
             to_port: 22
             proto: "tcp"
             cidr_ip: "0.0.0.0/0"
           -
             rule_type: "outbound"
             from_port: "all"
             to_port: "all"
             proto: "all"
             cidr_ip: "0.0.0.0/0"
        assoc_creds: "aws_creds"
    resource_group_vars:
      -
        resource_group_name : "awssgtest"
        test_var1: "test_var1 msg is grp1 hello"

.. note::

  Source of the above AWS EC2 Security Groups example can be found at `Example Topologies <https://github.com/CentOS-PaaS-SIG/linch-pin/tree/master/examples/topology>`_

