Init
====

command : linchpin init

This command initialises the directory structure to facilitate linchpin rise and linchpin drop commands
The directory structure generated is as follows:
|  .
|  ├── configure
|  ├── docs
|  ├── inventories
|  ├── layouts
|  │ └── my_layout.yml 
|  ├── PinFile
|  └── topologies
|    └── duffy-3node-cluster.yml

Options:
  --path PATH  path for initialisation
  --help       Help

=========
Examples:
=========

+------------------------+---------------------------------------------------------+
| Usage                  | Action                                                  |
+========================+=========================================================+
| linchpin init          |  initialises the directory structure for rise & drop    |
+------------------------+---------------------------------------------------------+
