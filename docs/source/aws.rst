Amazon Web Services
===================

The Amazon Web Services (AWS) provider manages multiple types of resources.

aws_ec2
-------

AWS Instances can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/aws-ec2-new.yml>`
* :docs1.5:`Topology Example w/ VPC <workspace/topologies/aws-ec2-vpc.yml>`
* `aws_ec2 module <http://docs.ansible.com/ansible/latest/ec2_module.html>`_

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`aws_ec2` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`aws_ec2`
definition, the following options are available.

+------------------+------------+---------------+-------------------+-----------------+
| Parameter        | required   | type          | ansible value     | comments        |
+==================+============+===============+===================+=================+
| role             | true       | string        | N/A               |                 |
+------------------+------------+---------------+-------------------+-----------------+
| name             | true       | string        | instance_tags     | name is set as  |
|                  |            |               |                   | an instance_tag |
|                  |            |               |                   | value.          |
+------------------+------------+---------------+-------------------+-----------------+
| flavor           | true       | string        | instance_type     |                 |
+------------------+------------+---------------+-------------------+-----------------+
| image            | true       | string        | image             |                 |
+------------------+------------+---------------+-------------------+-----------------+
| region           | false      | string        | region            |                 |
+------------------+------------+---------------+-------------------+-----------------+
| count            | false      | integer       | count             |                 |
+------------------+------------+---------------+-------------------+-----------------+
| keypair          | false      | string        | key_name          |                 |
+------------------+------------+---------------+-------------------+-----------------+
| security_group   | false      | string / list | group             |                 |
+------------------+------------+---------------+-------------------+-----------------+
| vpc_subnet_id    | false      | string        | vpc_subnet_id     |                 |
+------------------+------------+---------------+-------------------+-----------------+
| assign_public_ip | false      | string        | assign_public_ip  |                 |
+------------------+------------+---------------+-------------------+-----------------+

EC2 Inventory Generation
~~~~~~~~~~~~~~~~~~~~~~~~

If an instance has a public IP attached, its hostname in public DNS, if
available, will be provided in the generated Ansible inventory file, and if not
the public IP address will be provided.

For instances which have a private IP address for VPC usage, the private IP
address will be provided since private EC2 DNS hostnames (e.g.
**ip-10-0-0-1.ec2.internal**) will not typically be resolvable outside of AWS.

For instances with both a public and private IP address, the public address is
always provided instead of the private address, so as to avoid duplicate runs
of Ansible on the same host via the generated inventory file.
 
aws_ec2_key
-----------

AWS SSH keys can be added using this resource.

* :docs1.5:`Topology Example <workspace/topologies/aws-ec2-key-new.yml>`
* `ec2_key module <http://docs.ansible.com/ansible/latest/ec2_key_module.html>`_

.. note:: This resource will not be torn down during a :term:`destroy`
   action. This is because other resources may depend on the now existing
   resource.
 
aws_s3 
------

AWS Simple Storage Service buckets can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/aws-s3-new.yml>`
* `aws_s3 module <http://docs.ansible.com/ansible/latest/aws_s3_module.html>`_

.. note:: This resource will not be torn down during a :term:`destroy`
   action. This is because other resources may depend on the now existing
   resource.
 
aws_sg
------

AWS Security Groups can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/aws-sg-new.yml>`
* `ec2_group module <http://docs.ansible.com/ansible/latest/ec2_group_module.html>`

.. note:: This resource will not be torn down during a :term:`destroy`
   action. This is because other resources may depend on the now existing
   resource.
  
aws_ec2_eip
-----------

AWS EC2 elastic ips can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/aws-ec2-eip.yml>`
* `ec2_eip module <http://docs.ansible.com/ansible/latest/ec2_eip_module.html>`

aws_ec2_vpc_net
---------------

AWS VPC networks can be provisioned using this resource.

* :docs1.5:`Topology Example <workspaces/topologies/aws-ec2-vpc-net.yml>`
* `ec2_vpc_net module <http://docs.ansible.com/ansible/latest/ec2_vpc_net.html
>`_


aws_ec2_vpc_net
---------------

AWS VPC networks can be provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/aws-ec2-vpc-net.yml>`
* `ec2_vpc_net module <http://docs.ansible.com/ansible/latest/ec2_vpc_net.html>`_


aws_ec2_vpc_subnet
------------------

AWS VPC subnets can be provisioned using this resource.
* :docs1.5:`Topology Example <workspace/topologies/aws-ec2-vpc-subnet.yml>`
* `ec2_vpc_subnet module <http://docs.ansible.com/ansible/latest/ec2_vpc_subnet.html>`_

aws_ec2_vpc_routetable
----------------------

AWS VPC routetable can be provisioned using this resource.
* :docs1.5:`Topology Example <workspace/topologies/aws-ec2-vpc-routetable.yml>`
* `ec2_vpc_route_table module <https://docs.ansible.com/ansible/latest/modules/ec2_vpc_route_table_module.html#ec2-vpc-route-table-module>`_

aws_ec2_vpc_endpoint
--------------------

AWS VPC endpoint can be provisioned using this resource.
* :docs1.5:`Topology Example <workspace/topologies/aws-ec2-vpc-endpoint.yml>`
* `ec2_vpc_endpoint module <https://docs.ansible.com/ansible/latest/modules/ec2_vpc_endpoint_module.html>`_

aws_ec2_elb_lb
--------------

AWS EC2 elb lb load balancer can be provisioned using this resource.
* :docs1.5:`Topology Example <workspace/topologies/aws-ec2-elb-lb.yml>`
* `ec2_vpc_endpoint module <https://docs.ansible.com/ansible/latest/modules/ec2_elb_module.html>`_

Additional Dependencies
-----------------------

No additional dependencies are required for the AWS Provider.

Credentials Management
----------------------

AWS provides several ways to provide credentials. LinchPin supports
some of these methods for passing credentials for use with AWS resources.



.. include:: credentials/aws.rst

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

LinchPin honors the AWS environment variables
 
Provisioning
~~~~~~~~~~~~

Provisioning with credentials uses the ``--creds-path`` option.

.. code-block:: bash

   $ linchpin -v --creds-path ~/.config/aws up

Alternatively, the credentials path can be set as an environment variable,

.. code-block:: bash

   $ export CREDS_PATH="~/.config/aws"
   $ linchpin -v up

