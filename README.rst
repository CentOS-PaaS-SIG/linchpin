linch-pin
----------

Linch-pin provides a collection of Ansible playbooks for provisioning and
managing resources across multiple infrastructures. Where multiple
infrastructure resource types can be defined with a single topology file.

Linch-pin can also generate inventory files for use with additional ansible
playbooks. These are applied using an inventory layout file (work in progress).

Directory Structure
++++++++++++++++++++

.. code-block:: bash
    .
    ├── provision # provisioning of infrastructures occurs here
    │   ├── roles # ansible roles used to perform provisioning
    │   ├── filter_plugins # inventory layout filter plugins
    │   ├── site.yml # default provisioning playbook
    │   └── invfilter.yml # playbook for tooling inventory filters
    ├── configure # additional configurations for jenkins jobs and the like
    │   └── site.yml # configuration playbook
    ├── docs # documentation
    ├── README.md # this file
    ├── schemas # example schemas (includes default schema: schema_v2.json)
    ├── ex_topo # example topologies and related components
    ├── keystore # location of ssh keys, etc to provide to provisioned systems
    ├── library # ansible modules for linch-pin (written in python)
    ├── inventory # default location of inventories provided by linch-pin
    └── outputs # default location of outputs

Installation
++++++++++++

`Installation documentation <http://linch-pin.readthedocs.io/en/latest/intro_installation.html>`_

General Configuration
+++++++++++++++++++++

`General Configuration documentation <http://linch-pin.readthedocs.io/en/latest/config_general.html>`_

Credentials
++++++++++++

* `Openstack credentials examples <https://github.com/herlo/linch-pin/tree/master/linchpin/provision/roles/openstack/vars>`_
* `AWS credential examples <https://github.com/herlo/linch-pin/tree/master/linchpin/provision/roles/aws/vars>`_
* `GCE credentials examples <https://github.com/herlo/linch-pin/tree/master/linchpin/provision/roles/gcloud/vars>`_

Example Topology
+++++++++++++++++++++

`Example Topologies <http://linch-pin.readthedocs.io/en/latest/topologies.html>`_

Example Inventory Layout (openshift 3 node cluster)
+++++++++++++++++++++++++++++++++++++++++++++++++++

`Example Layouts <http://linch-pin.readthedocs.io/en/latest/config_layout.html>`_

Using Linch-Pin
+++++++++++++++

Probably the best way to see linch-pin in action, is to watch the
presentation given at
`DevConf 2017 <https://www.youtube.com/watch?v=Tb7Zti5Xao8>`_


