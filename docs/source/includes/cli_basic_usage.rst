The most basic usage of ``linchpin`` might be to perform an `up` action. This simple command assumes a :term:`PinFile` in the workspace (current directory by default), with one target `dummy`.

.. code-block:: bash

    $ linchpin up
    Action 'up' on Target 'dummy' is complete

    Target              Run ID      uHash   Exit Code
    -------------------------------------------------
    dummy                   75       79b9           0

Upon completion, the systems defined in the `dummy` target will be provisioned. An equally basic usage of ``linchpin`` is the `destroy` action. This command is peformed using the same PinFile and target.

.. code-block:: bash

    $ linchpin destroy
    Action 'destroy' on Target 'dummy' is complete

    Target              Run ID      uHash   Exit Code
    -------------------------------------------------
    dummy                   76       79b9           0

Upon completion, the systems which were provisioned, are destroyed (or torn down).

Preview Feature: 

linchpin up and destroy includes --use-shell parameter which makes linchpin run as a subprocess rather than ansible api call
usefull when we would like to overwrite environment varibles

.. code-block:: bash

    $ linchpin -vvvv up --use-shell --env-vars TESTENV testenv value

