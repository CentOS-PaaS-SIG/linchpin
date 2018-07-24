The most common argument available in ``linchpin`` is the :term:`TARGET <target>`. Generally, the :term:`PinFile` will have many targets available, but only one or two will be requested.

.. code-block:: bash

    $ linchpin up dummy-new libvirt-new
    Action 'up' on Target 'dummy' is complete
    Action 'up' on Target 'libvirt' is complete

    Target              Run ID     uHash    Exit Code
    -------------------------------------------------
    dummy                   77      73b1            0
    libvirt                 39      dc2c            0


In some cases, you may wish to use a different :term:`PinFile`.

.. code-block:: bash

    $ linchpin -p PinFile.json up
    Action 'up' on Target 'dummy-new' is complete

    Target              Run ID      uHash   Exit Code
    -------------------------------------------------
    dummy-new           29          c70a            0

As you can see, this PinFile had a :term:`target` called ``dummy-new``, and it was the only target listed.

Other common options include:

  * ``--verbose`` (``-v``) to get more output
  * ``--config`` (``-c``) to specify an alternate configuration file
  * ``--workspace`` (``-w``) to specify an alternate workspace
