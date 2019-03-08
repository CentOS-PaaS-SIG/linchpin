Provisioning AWS EC2 with LinchPin
=================================================

LinchPin can be used to provision compute instances on Amazon Web Services.  If you need to familiarize yourself with EC2, `read this`_. Now let's step through the process of creating a new workspace for provisioning EC2

.. _read this: https://docs.aws.amazon.com/ec2/index.html#lang/en_us

.. include:: templates/fetch.rst

.. include:: templates/initialization.rst

Creating a Topology
-------------------

Now that we have a PinFile, its time to add the code for an AWS EC2 instance.  Edit your PinFile so it looks like the one below.

.. code:: yaml

    simple:
      topology:
        topology_name: simple
        resource_groups:
          - resource_group_name: aws_simple
            resource_group_type: aws
            resource_definitions:
              - name: simple_ec2
                role: aws_ec2
                flavor: m1.small
                count: 1

There are a number of other fields available for these two roles.  Information about those fields as well as the other AWS roles can be found on the `AWS provider page`_.

A :term:`resource group` is a group of resources related to a single provider.  In this example we have an AWS resource group that defines one type of AWS resources.  We could also define an OpenStack resource group below it that provisions a handful of OpenStack Server nodes.  A single resource group can contain many :term:`resource definitions`. A resource definition details the requirements for a specific resource.  We could add another resource definition to this topology to create a security group for our EC2 nodes.  Multiple resources can be provisioned from a single resource definition by editing the :code:`count` field, but all non-unique properties of the resources will be identical.  So the flavor will be the same, but each node will have a unique name.  The name will be {{ name }}_0, {{ name }}_1, etc. from 0 to count.

.. _AWS provider page: ../aws.rst

Credentials
-----------

Finally, we need to add credentials to the resource group.  AWS provides several ways to provide credentials. LinchPin supports some of these methods for passing credentials for use with AWS resources.

.. include:: ../credentials/aws.rst

.. include:: templates/layout.rst

.. include:: templates/up.rst

.. include:: templates/destroy.rst

.. include:: templates/journal.rst
