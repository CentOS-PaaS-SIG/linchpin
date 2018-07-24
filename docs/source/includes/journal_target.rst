The default view, 'target', is displayed using the target. The data displayed to the screen shows the last three (3) tasks per target, along with some useful information.

.. code-block:: bash

    $ linchpin journal --view=target dummy-new

    Target: dummy-new
    run_id       action       uhash         rc
    ------------------------------------------
    5              up         0658          0
    4         destroy         cf22          0
    3              up         cf22          0

.. note:: The 'target' view is the default, making the --view optional.

The target view can show more data as well. Fields (``-f, --fields``) and
count (``-c, --count``) are useful options.

.. code-block:: bash

    $ linchpin journal dummy-new -f action,uhash,end -c 5

    Target: dummy-new
    run_id      action       uhash         end
    ------------------------------------------
    6              up        cd00   12/15/2017 05:12:52 PM
    5              up        0658   12/15/2017 05:10:52 PM
    4         destroy        cf22   12/15/2017 05:10:29 PM
    3              up        cf22   12/15/2017 05:10:17 PM
    2         destroy        6d82   12/15/2017 05:10:06 PM
    1              up        6d82   12/15/2017 05:09:52 PM

It is simple to see that the output now has five (5) records, each containing the run_id, action, uhash, and end date.

The data here can be used to perform idempotent (repetitive) tasks, like running the :term:`up` action on `run_id: 5` again.

.. code-block:: bash

    $ linchpin up dummy-new -r 6
    Action 'up' on Target 'dummy-new' is complete

    Target                  Run ID  uHash   Exit Code
    -------------------------------------------------
    dummy-new                    7   cd00           0

What might not be immediately obvious, is that the :term:`uhash` on Run ID: 7 is identical to the run_id: 6 shown in the previous ``linchpin journal`` output. Essentially, the same task was run again.

.. note:: If LinchPin is configured with the unique-hash feature, and the provider supports naming, resources can have unique names. These features are turned off by default.

The :term:`destroy` action will automatically look up the last task with an `up` action and destroy it. If other resources are needed to be destroyed, a `run_id` should be passed to the task.

.. code-block:: bash

    $ linchpin destroy dummy-new -r 5
    Action 'destroy' on Target 'dummy-new' is complete

    Target                  Run ID  uHash   Exit Code
    -------------------------------------------------
    dummy-new                    8   0658           0

