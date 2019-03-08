.. This is the template for the destroy section of a provider tutorial
.. In the majority of cases, this file can be included directly.  If non-provider-specific changes must be
.. made, make them here instead of modifying the provider you're working on

Destroy
-------

At some point you'll no longer need the machines you provisioned.  You can destroy the provisioned machines with :code:`linchpin destroy`.  However, you may not want to remove every single target from your last provision.  For example, lets say you ran the simple provision above, then ran a few others.  You could use the :term:`transaction ID`, labeled "ID" above, to do so.

.. code:: bash

	$ linchpin -vv destroy -t 122

You may also have provisioned multiple targets at once.  If you only want to destroy one of them, you can do so with the name of the target and the :term:`run ID`.

.. code:: bash

	$ linchpin -vv destroy -r 1 simple
