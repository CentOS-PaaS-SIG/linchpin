The following settings are in the ``[states]`` section of the linchpin.conf.

These settings define the state names, which are useful in :doc:`hooks`.

preup
~~~~~

Define the name of the so called `preup` state. This state is set and
executed prior to the 'up' action being called, but after the PinFile
data is loaded.

.. code-block:: cfg

    preup = preup

predestroy
~~~~~~~~~~

Define the name of the so called `predestroy` state. This state is set and
executed prior to the 'destroy' action being called, but after the PinFile
data is loaded.

.. code-block:: cfg

    predestroy = predestroy

postup
~~~~~~

Define the name of the so called `postup` state. This state is set and
executed after to the 'up' action is completed, and after the `postinv`
state is executed.

.. code-block:: cfg

    postup = postup

postdestroy = postdestroy
~~

Define the name of the so called `postdestroy` state. This state is set and
executed after to the 'destroy' action is completed.

.. code-block:: cfg

    postdestroy = postdestroy

postinv
~~~~~~~

Define the name of the so called `postinv` state. This state is set and
executed after to the 'up' action is completed, and before the `postup`
state is executed. This is eventually going to be the inventory generation
hook.

.. code-block:: cfg

    postinv = inventory

The following settings are in the ``[hookstates]`` section of the linchpin.conf.

These settings define the 'STATES' each action uses in :doc:`hooks`.

up
~~

For the 'up' action, types of hook states are available for execution

.. code-block:: cfg

    up = pre,post,inv


destroy
~~~~~~~

For the 'destroy' action, types of hook states are available for execution

.. code-block:: cfg

    destroy = pre,post

inv
~~~

New in version 1.2.0

For the inventory generation, which only happens on an 'up' state. 

.. note:: The `postinv` state currently doesn't do anything. In the future,
   it will provide a way to generate inventories besides the standard Ansible
   static inventory.

.. code-block:: cfg

    inv = post

