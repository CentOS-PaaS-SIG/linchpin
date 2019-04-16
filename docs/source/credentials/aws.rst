One method to provide AWS credentials that can be loaded by LinchPin is to use
the INI format that the `AWS CLI tool <https://docs.aws.amazon.com/cli/latest/userguide/cli-config-files.html>`_
uses.

Credentials File
~~~~~~~~~~~~~~~~

An example credentials file may look like this for :ref:`aws`.

.. code-block:: cfg

    $ cat aws.key
    [default]
    aws_access_key_id=ARYA4IS3THE3NO7FACEB
    aws_secret_access_key=0Hy3x899u93G3xXRkeZK444MITtfl668Bobbygls

    [herlo_aws1_herlo]
    aws_access_key_id=JON6SNOW8HAS7A3WOLF8
    aws_secret_access_key=Te4cUl24FtBELL4blowSx9odd0eFp2Aq30+7tHx9

.. seealso:: :doc:`providers` for provider-specific credentials examples.

To use these credentials, the user must tell LinchPin two things. The first
is which credentials to use. The second is where to find the credentials data.

Using Credentials
~~~~~~~~~~~~~~~~~

In the topology, a user can specific credentials. The credentials are
described by specifying the file, then the profile. As shown above, the
filename is 'aws.key'. The user could pick either profile in that file.

.. code-block:: yaml

    ---
    topology_name: ec2-new
    resource_groups:
      - resource_group_name: "aws"
        resource_group_type: "aws"
        resource_definitions:
          - name: demo-day
            flavor: m1.small
            role: aws_ec2
            region: us-east-1
            image: ami-984189e2
            count: 1
        credentials:
          filename: aws.key
          profile: default

The important part in the above topology is the `credentials` section. Adding
credentials like this will look up, and use the credentials provided.

Credentials Location
~~~~~~~~~~~~~~~~~~~~

By default, credential files are stored in the `default_credentials_path`, which is
``~/.config/linchpin``.

.. hint:: The `default_credentials_path` value uses the interpolated
   :dirs1.5:`default_config_path <workspace/linchpin.conf#L22>` value, and
   can be overridden in the :docs1.5:`linchpin.conf`.

The credentials path (or ``creds_path``) can be overridden in two ways.

It can be passed in when running the linchpin command.

.. code-block:: bash

    $ linchpin -vvv --creds-path /dir/to/creds up aws-ec2-new

.. note:: The ``aws.key`` file could be placed in the
   :doc:`default_credentials_path <conf/evars>`. In that case passing
   ``--creds-path`` would be redundant.

Or it can be set as an environment variable.

.. code-block:: bash

    $ export CREDS_PATH=/dir/to/creds
    $ linchpin -v up aws-ec2-new





