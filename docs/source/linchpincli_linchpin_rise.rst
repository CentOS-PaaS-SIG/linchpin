Rise
====

command : linchpin rise

This command initiate the provisioning activity using contents of PinFile and current working directory files.
By default it provisions all the targets in the PinFile.


Options :
Options:
  --pf           option to specify PinFIle to use
  --target TEXT  target to provision
  --help         help 

=========
Examples:
=========

+-------------------------------------+--------------------------------------------------------------------+
| Usage                               | Action                                                             |
+-------------------------------------+--------------------------------------------------------------------+
| linchpin rise                       | Provisions all targets in the PinFile of current working directory |
+-------------------------------------+--------------------------------------------------------------------+
| linchpin rise --target <targetname> | Initiates provisioning of specific target                          |
+-------------------------------------+--------------------------------------------------------------------+
