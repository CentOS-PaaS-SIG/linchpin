Command-Line Reference
=======================

Linchpin's command line interface is availble with the ``linchpin`` command,
and comes installed with LinchPin automatically. The command has
subcommands, ``up``, ``destroy``, etc., listed below.

Usage: ``linchpin [OPTIONS] COMMAND [ARGS]...``

**Options**

``-c, --config PATH``
    Path to config file
``-w, --workspace PATH``
    Use the specified workspace if the familiar Jenkins
    $WORKSPACE environment variable is not set
``-v, --verbose``
    Enable verbose output
``--version``
    Prints the version and exits
``-h, --help``
    Show this message and exit.

**Commands**

``init``
    Initializes a linchpin project

``up``
    Provisions nodes from the given target(s) in the given PinFile.

``destroy``
    Destroys nodes from the given target(s) in the given PinFile

