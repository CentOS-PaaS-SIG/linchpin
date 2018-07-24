Getting help from the command line is very simple. Running either ``linchpin``
or ``linchpin --help`` will yield the command line help page.

.. code-block:: bash

    $ linchpin --help
    Usage: linchpin [OPTIONS] COMMAND [ARGS]...

      linchpin: hybrid cloud orchestration

    Options:
      -c, --config PATH               Path to config file
      -p, --pinfile PINFILE           Use a name for the PinFile different from
                                      the configuration.
      -d, --template-data TEMPLATE_DATA
                                      Template data passed to PinFile template
      -o, --output-pinfile OUTPUT_PINFILE
                                      Write out PinFile to provided location
      -w, --workspace PATH            Use the specified workspace. Also works if
                                      the familiar Jenkins WORKSPACE environment
                                      variable is set
      -v, --verbose                   Enable verbose output
      --version                       Prints the version and exits
      --creds-path PATH               Use the specified credentials path. Also
                                      works if CREDS_PATH environment variable is
                                      set
      -h, --help                      Show this message and exit.

    Commands:
      init     Initializes a linchpin project.
      up       Provisions nodes from the given target(s) in...
      destroy  Destroys nodes from the given target(s) in...
      fetch    Fetches a specified linchpin workspace or...
      journal  Display information stored in Run Database...

For subcommands, like ``linchpin up``, passing the ``--help`` or ``-h`` option produces help related to the provided subcommand.

.. code-block:: bash

    $ linchpin up -h
    Usage: linchpin up [OPTIONS] TARGETS

      Provisions nodes from the given target(s) in the given PinFile.

      targets:    Provision ONLY the listed target(s). If omitted, ALL targets
      in the appropriate PinFile will be provisioned.

      run-id:     Use the data from the provided run_id value

    Options:
      -r, --run-id run_id  Idempotently provision using `run-id` data
      -h, --help           Show this message and exit.

As can easily be seen, ``linchpin up`` has additional arguments and options.

