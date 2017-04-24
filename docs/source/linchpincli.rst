Linchpin CLI
============

Linchpin's command line interface is availble with the "linchpin" command,
and comes installed with Linchpin automatically. The linchpin command has
subcommands, like linchpin up, linchpin destroy, etc., listed below.

Usage: ``linchpin [OPTIONS] COMMAND [ARGS]...``

**Options**

``-c, --config PATH``
    Path to config file
``-w, --workspace PATH``
    Use the specified workspace if the familiar Jenkins $WORKSPACE environment variable is not set
``-v, --verbose``
    Enable verbose output
``--version``
    Prints the version and exits
``-h, --help``
    Print the help text for this command.

**Arguments**

``COMMAND``
    One of the linchpin commands listed below.

.. toctree::
   :maxdepth: 1

   linchpincli_linchpin_init
   linchpincli_linchpin_up
   linchpincli_linchpin_destroy
   linchpincli_linchpin_invgen
   linchpincli_linchpin_layout
   linchpincli_linchpin_topology
   linchpincli_linchpin_validate
   linchpincli_linchpin_rise
   linchpincli_linchpin_drop

The ``linchpin config`` command has been removed with the release of 1.0.0.
