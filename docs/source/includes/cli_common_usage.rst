Verbose Output
~~~~~~~~~~~~~~

.. code-block:: bash

    $ linchpin -v up dummy-new

Specify an Alternate PinFile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ linchpin -vp Pinfile.alt up

Specify an Alternate Workspace
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ export WORKSPACE=/tmp/my_workspace
    $ linchpin up libvirt

or

.. code-block:: bash

    $ linchpin -vw /path/to/workspace destroy openshift

Provide Credentials
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ export CREDS_PATH=/tmp/my_workspace
    $ linchpin -v up libvirt

or

.. code-block:: bash

    $ linchpin -v --creds-path /credentials/path up openstack

.. note:: The value provided to the ``--creds-path`` option is a directory,
          NOT a file. This is generally due to the topology containing the
          filename where the credentials are stored.

