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
    |-- bin # binaries needed 
    |-- docs # documentation 
    |-- ex_schemas # example Schema definitions
    |   `-- os_server_roles.json
    |-- ex_topo # example topologies
    |   |-- ex_data_os_server.yml
    |-- group_vars # variables applicable for groups
    |   `-- all
    |-- hosts # inventory hosts file
    |-- inventory # dynamic inventory scripts
    |-- library # custom modules library
    |   `-- schema_check
    |       `-- schema_check.py
    |-- plugins # custom plugins
    |-- README.md
    |-- roles # roles handling resource specific provisioning
    |   |-- aws
    |   |   |-- handlers
    |   |   |   `-- main.yml
    |   |   |-- tasks
    |   |   |   `-- main.yml
    |   |   `-- templates
    |   |-- common 
    |   |   |-- handlers
    |   |   |   `-- main.yml
    |   |   |-- tasks
    |   |   |   `-- main.yml
    |   |   `-- templates
    |   `-- openstack
    |       |-- handlers
    |       |   `-- main.yml
    |       |-- tasks
    |       |   |-- main.yml
    |       |   `-- provision_resource_group.yml 
    |       |   `-- provision_res_defs.yml
    |       |-- templates
    |       `-- vars #contains openstack credential files
    |           |-- examplecreds.yml
    |-- site.yml
    `-- tests # tests cases

.. _understanding_directory_structure:

Understanding Directory_structure
`````````````````````````````````

