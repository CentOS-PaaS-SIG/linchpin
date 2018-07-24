Context Distiller
-----------------

New in version 1.5.2

The purpose of the Context Distiller is to take outputs from provisioned
resources and provide them to a user as a json file.

The distiller currently supports the following roles::

  * os_server
  * aws_ec2
  * bkr_server
  * dummy_node (for testing)

For each :term:`role`, the distiller collects specific fields from the
resource data.

.. note:: Please be aware that this feature is planned to integrated with
   other tooling to make extracting resource data more flexible in the future.

Enabling the Distiller
``````````````````````

To enable the Context Distiller, the following must be set in the
:dirs1.5:`linchpin.conf <workspace/linchpin.conf>`.

.. code:: cfg

  [lp]
  distill_data = True

  # disable generating the resources file
  [evars]
  generate_resources = False

.. note:: Other settings may already be in these sections. If that is the case,
   just add these settings to the proper section.

.. hint:: It may not be immediately obvious, as LinchPin uses the :term:`RunDB`
   data to return resource data from a run. In this way, the resource data can
   be stored somewhere and retrieved at any time by future tooling. Because of
   this, the resources file is disabled. In this way, the resource data is
   stored solely in the RunDB for easy retrieval.

Fields to Retreive
++++++++++++++++++

.. warning:: Modifying the distilled fields can cause unexpected results.
   MODIFY THIS DATA AT YOUR OWN RISK!

Within the :code1.5:`linchpin.constants <linchpin/linchpin.constants>` file,
the `[distiller`] section exists. Described within this section is how each
role gathers the applicable data to distill.

.. code-block:: cfg

    [distiller]
    bkr_server = id,url,system
    dummy_node: hosts
    aws_ec2 = instances.id,instances.public_ip,instances.private_ip,instances.public_dns_name,instances.private_dns_name,instances.tags:name
    os_server = servers.id,servers.interface_ip,servers.name,servers.private_v4,servers.public_v4

If the distiller is enabled, the `bkr_server` role will distill the id, url,
and system values for each instance provisioned during the transaction.

Output
``````

The distiller creates one file, placed in
``<workspace>/resources/linchpin.distilled``. Each time an 'up' transaction
is performed, the distilled data is overwritten.

If no output is recorded, it's likely that the provisioning didn't complete
successfully, or an error occurred during data collection. The data is still
available in the RunDB.

This is the output for the `aws_ec2` role, using the `aws-ec2-new` target,
which provisioned two instances.

.. code:: json

    {
        "aws-ec2-new": [
            {
                "id": "i-0d8616a3d08a67f38",
                "name": "demo-day",
                "private_dns_name": "ip-172-31-18-177.us-west-2.compute.internal",
                "private_ip": "172.31.18.177",
                "public_dns_name": "ec2-54-202-80-27.us-west-2.compute.amazonaws.com",
                "public_ip": "54.202.80.27"
            },
            {
                "id": "i-01112909e184530fc",
                "name": "demo-night",
                "private_dns_name": "ip-172-31-20-190.us-west-2.compute.internal",
                "private_ip": "172.31.20.190",
                "public_dns_name": "ec2-54-187-172-80.us-west-2.compute.amazonaws.com",
                "public_ip": "54.187.172.80"
            }
        ]
    }

