Up
--

It's time to provision your first LinchPin resources.

.. code-block:: bash

    1   [/tmp/simple]$ linchpin up
    2    [WARNING]: Unable to parse /tmp/simple/localhost as an inventory source

    3    [WARNING]: No inventory was parsed, only implicit localhost is available

    4   Action 'up' on Target 'simple' is complete

    5   ID: 10
    6   Action: up

    7   Target              	Run ID	uHash	Exit Code
        -------------------------------------------------
    8   simple              	     2	3a4038	        0

In just a few seconds, the command will finish. Because the *simple* target provides only the *dummy_node* resource, no actual instances are provisioned. However, a representation can be found at ``/tmp/dummy.hosts``

.. code-block:: bash

    $ cat /tmp/dummy.hosts
    web-3a4038-0.example.net
    web-3a4038-1.example.net

More importantly, there are several other things to note. First off, The ``linchpin`` command has two basic actions, *up* and *destroy*. Each should be pretty self-explanatory.

Summary
```````
Upon completion of every action, there is a summary that is provided. This summary provides details which can be used to repeat the process, or for further reporting with ``linchpin journal``. Let's cover the process in detail.

uHash
+++++

The Unique-ish Hash, or uHash\ :sup:`8` provides a way for each instance to be unique within a set of resources. The uHash is used throughout LinchPin with reporting, idempotency, inventories, etc. The uHash is configurable, but defaults to a sha256 hash of some unique data, trimmed to 6 characters.

Run ID
++++++

The Run ID\ :sup:`8` can be used for idempotency. The Run ID is used for a specific target. Passing ``-r <run-id>`` to ``linchpin up`` or ``linchpin destroy`` along with the target will provide an idempotent up or destroy action.

.. code-block:: bash

    $ linchpin up --run-id 2 simple

    .. snip ..

    Action 'up' on Target 'simple' is complete

    ID: 11
    Action: up

    Target              	Run ID	uHash	Exit Code
    -------------------------------------------------
    simple              	     3	3a4038	        0

The thing to notice here is that the uHash is the same here as in the original *up* action above. This provides idempotency when provisioning.

ID
++

Similar to the Run ID explained above, the Transaction ID, or ID\ :sup:`5`\, is provided for idempotency. If desired, the entire transaction can be repeated using this value. Unlike the Run ID, however, the Transaction ID can be used to repeat the entire transaction (multiple targets). As with Run ID, passing ``-t <tx-id>`` will provide idempotent an idempotent up or destroy action.

.. code-block:: bash

    $ linchpin up --tx-id 10

    .. snip ..

    ID: 12
    Action: up

    Target              	Run ID	uHash	Exit Code
    -------------------------------------------------
    simple              	     4	3a4038	        0

.. note:: All targets are executed when using ``-t/--tx-id``. This differs from ``-r/--run-id`` where only one target can be supplied per Run ID. This is useful when multiple targets are executed from the PinFile.


Exit Code
+++++++++

A common desire is to check the exit code\ :sup:`7`\. This is provided as an indicator of the action's success or failure. Commonly, post actions are performed upon resources (eg. configure the system, adding logins, setting up security, etc.)


Destroy
-------

To destroy the previously provisioned resources, use ``linchpin destroy``.

.. code-block:: bash

    $ linchpin destroy
     [WARNING]: Unable to parse /tmp/simple/localhost as an inventory source

     [WARNING]: No inventory was parsed, only implicit localhost is available

    Action 'destroy' on Target 'simple' is complete

    ID: 13
    Action: destroy

    Target              	Run ID	uHash	Exit Code
    -------------------------------------------------
    simple              	     5	3a4038	        0

As with ``linchpin up``, destroy provides a summary of the action taken. In this case, however, the resources have been terminated and cleaned up. With the *dummy_node* role, the resources are remove from the file.

.. code-block:: bash

    $ cat /tmp/dummy.hosts
    $ wc -l /tmp/dummy.hosts
    0 /tmp/dummy.hosts

This concludes the introduction of the LinchPin getting started tutorial. For more information, see :doc:`providers`.
