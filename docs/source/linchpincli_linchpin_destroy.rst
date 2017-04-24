linchpin destroy
================

Usage: ``linchpin destroy [OPTIONS] TARGET``

Destroys nodes from the given target(s) in the given PinFile.

**Arguments**

``TARGET ...``
	Destroy ONLY the listed target(s). If omitted, ALL targets in the appropriate PinFile are destroyed.

**Options**

``-p, --pinfile TEXT``
	Use a different PinFile than the one in the current workspace.
``-h, --help``
    Print the help text for this command.

Examples
--------

+--------------------------------------------------+--------------------------------------------------------------------------+
| Usage                                            | Action                                                                   |
+==================================================+==========================================================================+
| linchpin destroy                                 | Destroy all targets in the PinFile in the current working directory      |
+--------------------------------------------------+--------------------------------------------------------------------------+
| linchpin destroy <targetname> [<targetname> ...] | Destroy specific targets in the PinFile in the current working directory |
+--------------------------------------------------+--------------------------------------------------------------------------+
| linchpin destroy -p <pinfile>                    | Destroy specific targets in the PinFile specific with ``-p``             |
+--------------------------------------------------+--------------------------------------------------------------------------+

.. seealso::
    * :doc:`linchpincli`
    * :doc:`linchpincli_linchpin_init`
    * :doc:`linchpincli_linchpin_up`
