The ``linchpin`` command also allows combinining of general options with subcommand options. A good example of these might be to use the verbose (``-v``) option. This is very helpful in both the ``up`` and ``destroy`` subcommands.

.. code-block:: bash

    $ linchpin -v up dummy-new -r 72
    using data from run_id: 72
    rundb_id: 73
    uhash: a48d
    calling: preup
    hook preup initiated

    PLAY [schema check and Pre Provisioning Activities on topology_file] ********

    TASK [Gathering Facts] ******************************************************
    ok: [localhost]

    TASK [common : use linchpin_config if provided] *****************************

What can be immediately observed, is that the ``-v`` option provides more verbose output of a particular task. This can be useful for troubleshooiting or giving more detail about a specitic task. The ``-v`` option is placed **before** the subcommand. The ``-r`` option, since it applies directly to the ``up`` subcommand, it is placed **afterward**. Investigating the ``linchpin -help`` and ``linchpin up --help`` can help differentiate if there's confusion.

