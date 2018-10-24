LinchPin Initialization
-----------------------

.. code-block:: bash

    $ linchpin init simple
    Created destination workspace: /tmp/simple
    $ cd /tmp/simple
    $ linchpin up

    .. snip ..

    Action 'up' on Target 'simple' is complete

    ID: 1
    Action: up

    Target              	Run ID	uHash	Exit Code
    -------------------------------------------------
    simple              	     1	7735aa	        0

After running the commands above, LinchPin should be able to provision for you. We'll use `linchpin init` and `linchpin fetch` throughout this tutorial to get you familiar with its inner workings.

It's a minimal setup, using the `dummy` provider. We'll get more into those in the upcoming parts of this tutorial.

Now that `LinchPin` is working, the simple workspace is in place, let's learn more about :doc:`simple_workspace`.

.. note:: If you were unable to get LinchPin successfully installed and/or working, please see the :ref:`troubleshooting` documentation.

