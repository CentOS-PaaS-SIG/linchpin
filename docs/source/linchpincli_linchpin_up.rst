linchpin up
===========

Usage: ``linchpin up [OPTIONS] TARGET``

Provisions nodes from the given target(s) in the given PinFile.

**Arguments**

``TARGET ...``
	Provision ONLY the listed target(s). If omitted, ALL targets in the appropriate PinFile are provisioned.

**Options**

``-p, --pinfile TEXT``
	Use a different PinFile than the one in the current workspace.
``-h, --help``
    Print the help text for this command.

Examples
--------

+---------------------------------------------+--------------------------------------------------------------------+
| Usage                                       | Action                                                             |
+=============================================+====================================================================+
| linchpin up                                 | Provision all targets in the PinFile in the current workspace      |
+---------------------------------------------+--------------------------------------------------------------------+
| linchpin up <targetname> [<targetname> ...] | Provision specific targets in the PinFile in the current workspace |
+---------------------------------------------+--------------------------------------------------------------------+
| linchpin up -p <pinfile>                    | Provision specific targets in the PinFile specified with ``-p``    |
+---------------------------------------------+--------------------------------------------------------------------+

.. seealso::
    * :doc:`linchpincli`
    * :doc:`linchpincli_linchpin_init`
    * :doc:`linchpincli_linchpin_destroy`
