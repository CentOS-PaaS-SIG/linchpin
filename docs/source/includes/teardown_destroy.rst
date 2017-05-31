As expected, LinchPin can also perform :term:`teardown` of :term:`resources`.  A teardown action generally expects that resources have been :term:`provisioned <provision>`. However, because Ansible is idempotent, ``linchpin destroy`` will only check to make sure the resources are up.  Only if the resources are already up will the teardown happen.

The command ``linchpin destroy`` will either use :term:`resources` and/or :term:`topology` files to determine the proper :term:`teardown` procedure. The `dummy` Ansible role does not use the resources, only the topology during teardown.

.. code-block:: bash

    $ linchpin destroy
    target: dummy1, action: destroy

    $ cat /tmp/dummy.hosts
    -- EMPTY FILE --

.. note:: The teardown functionality is slightly more limited around ephemeral
    resources, like networking, storage, etc. It is possible that a network
    resource could be used with multiple cloud instances. In this way,
    performing a ``linchpin destroy`` does not teardown certain resources. This
    is dependent on each providers implementation.

    See specific implementations for each of the `providers
    <https://github.com/CentOS-PaaS-SIG/linch-pin/tree/develop/linchpin/provision/roles>`_.
