Drop
====

command : linchpin drop

This command initiates the teardown activity using contents of PinFile and current working directory.
By default it teardowns all the targets in the PinFile.


Options:
  --target    Name of the target
  --pf        Option to specify the PinFile to use.
  --help      Help

=========
Examples:
=========

+-------------------------------------+--------------------------------------------------------------------+
| Usage                               | Action                                                             |
+-------------------------------------+--------------------------------------------------------------------+
| linchpin drop                       | Teardown  all targets in the PinFile of current working directory. |
+-------------------------------------+--------------------------------------------------------------------+
| linchpin drop --target <targetname> | Initiates provisioning of specific target.                         |
+----------------------------+-----------------------------------------------------------------------------+
