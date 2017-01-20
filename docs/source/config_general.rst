General Configuration
=====================

.. contents:: Topics

Initialization
``````````````

Linchpin configuration requires multiple files to specify all the values. Fortunately,
there is an easy way to setup the files in the proper location. Linchpin offers a
handy `linchpin init` to create a skeleton configuration. Go ahead and issue that command
inside of a clean directory and take a look at the files that it creates.

PinFile
```````

The first file to configure is the PinFile. A PinFile can be configured with multiple
sets of infrastructure that should be provisioned or torn down. This file has two entries
prefilled that should be left as is.

``
topology_upstream: https://github.com/CentOS-PaaS-SIG/linch-pin/
layout_upstream: https://github.com/CentOS-PaaS-SIG/linch-pin/
``

These values should be left as is.

The remaining values in this file are named object hashes. Each object hash has two
properties. `topology` is is the name of the toplogy file to be used with that group.
`layout` is the name of the layout file that will be placed  Both topology and layout
files will be discussed in more detail in the upcoming pages.

inventory
`````````

This is a folder where output from linchpin will be placed following a successful run
of the command. Specifically, when so configured, inventory files suitable for consumption
by Ansible will be placed here. These files will point towards the resources requested
in your topology, tagged into groups with variables as specified by your layout.

layouts
```````

This directory is provided to place layout files. Paths to the layout files mentioned
in the PinFile are relative to this folder. An example file is provided, named
openshift-3node-cluster.yml. There is also an empty file named my_layout.yml where
you could place your own values.

A layout is a specification that provides input variables and group assignments
which will be included in the Ansbile inventory compatible output files from
linchpin. Layouts will be discussed in more detail later in this documentation.

topologies
``````````

This folder is for storing the topology files your project will use. Topology files
hold the basic information about which resources to provision and in which environments
they should be provisioned. More information about each supported environment will
be discussed later. For present, a sample file that will provision three resources in
a Duffy environment is provided in the topologies folder.

Topologies will be discussed in more detail and more examples will be given later
in these documents.
