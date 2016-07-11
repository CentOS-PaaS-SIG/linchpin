Getting Started
===============

.. contents:: Topics

.. _foreword:

Foreword
````````

Now that linch-pin is installed according to the steps given in :doc:`intro_installation` its time to understand the directory file structure and terminology of used in linchpin.



.. _directory_structure:

The current directory structure of linchpin should look lika as follows::
    
    .
    ├── docs
    │   ├── make.bat
    │   ├── Makefile
    │   └── source
    │       ├── conf.py
    │       ├── index.rst
    │       ├── installation.rst
    │       ├── intro_getting_started.rst
    │       ├── intro_installation.rst
    │       ├── intro.rst
    │       └── license.rst
    ├── ex_schemas
    │   ├── os_server_roles.json
    │   └── schema_v2.json
    ├── ex_topo
    │   └── ex_data.yml
    ├── group_vars
    │   └── all
    ├── hosts
    ├── library
    │   ├── output_parser
    │   │   └── output_parser.py
    │   └── schema_check
    │       └── schema_check.py
    ├── README.md
    ├── requirements.txt
    ├── roles
    │   ├── aws
    │   │   ├── handlers
    │   │   │   └── main.yml
    │   │   ├── tasks
    │   │   │   ├── deprovision_res_defs.yml
    │   │   │   ├── deprovision_resource_group.yml
    │   │   │   ├── main.yml
    │   │   │   ├── provision_res_defs.yml
    │   │   │   └── provision_resource_group.yml
    │   │   ├── templates
    │   │   │   └── output_formatter.j2
    │   │   └── vars
    │   │       └── ex_aws_creds.yml
    │   ├── common
    │   │   ├── handlers
    │   │   │   └── main.yml
    │   │   └── tasks
    │   │       └── main.yml
    │   ├── duffy
    │   │   ├── tasks
    │   │   │   ├── main.yml
    │   │   │   ├── provision_res_defs.yml
    │   │   │   ├── provision_resource_group.yml
    │   │   │   ├── teardown_res_defs.yml
    │   │   │   └── teardown_resource_group.yml
    │   │   └── vars
    │   │       └── ex_duffy_creds.yml
    │   ├── gcloud
    │   │   ├── handlers
    │   │   │   └── main.yml
    │   │   ├── tasks
    │   │   │   ├── main.yml
    │   │   │   ├── provision_res_defs.yml
    │   │   │   └── provision_resource_group.yml
    │   │   └── vars
    │   │       └── ex_gcloud_creds.yml
    │   ├── openstack
    │   │   ├── handlers
    │   │   │   └── main.yml
    │   │   ├── tasks
    │   │   │   ├── main.yml
    │   │   │   ├── provision_os_server.yml
    │   │   │   ├── provision_res_defs.yml
    │   │   │   └── provision_resource_group.yml
    │   │   └── vars
    │   │       └── ex_os_creds.yml
    │   └── output_writer
    │       ├── handlers
    │       │   └── main.yml
    │       ├── tasks
    │       │   └── main.yml
    │       └── templates
    │           └── output_formatter.j2
    └── site.yml

.. _understanding_directory_structure:

Understanding Directory_structure
`````````````````````````````````

.. _understanding_terminology:

Terminology
```````````

.. _example_topology_file:

Example Topology
````````````````

