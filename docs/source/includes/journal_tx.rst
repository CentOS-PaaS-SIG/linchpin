The transaction view, provides data based upon each transaction.

.. code-block:: bash

    $ linchpin journal --view tx --count 1

    ID: 130         Action: up

    Target                  Run ID  uHash   Exit Code
    -------------------------------------------------
    dummy-new                  279   920c           0
    libvirt                    121   ef96           0

    =================================================

In the future, the transaction view will also provide output for these items.
