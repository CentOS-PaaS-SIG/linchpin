Invgen
======

command : linchpin invgen

This command generates inventory based on inventory output file and layout file.

Options : 
--invtype       inventory type
--invout        inventory output file  [required]
--layout        layout file usually found in layout folder  [required]
--topoout       topology output file  [required]


=========
Examples:
=========

+------------------------------------------------------------+-------------------------------------------+
| Usage                                                      | Action                                    |
+------------------------------------------------------------+-------------------------------------------+
+ linchpin invgen --invtype <file_path> --invout <file_path> + Generates inventory from the topology     +
|  --layout <file_path> --topoout <file_path>                | output files based on inventype attribute |
+------------------------------------------------------------+-------------------------------------------+
