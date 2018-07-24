Duffy
=====

Duffy is a tool for managing pre-provisioned systems in CentOS' CI environment.
The Duffy provider manages a single resource, ``duffy_node``.

duffy_node
----------

The ``duffy_node`` resource provides the ability to provision using the
`duffy api  <https://wiki.centos.org/QaWiki/CI/Duffy>`_.

* :docs1.5:`Topology Example <workspace/topologies/duffy-new.yml>`

The ansible module for duffy exists in its own
`repository <https://github.com/CentOS-PaaS-SIG/duffy-ansible-module>`_.

Using Duffy
-----------

Duffy can only be run within the CentOS CI environment. To get access, follow
`this guide <https://wiki.centos.org/QaWiki/CI/GettingStarted>`_. Once access
is granted, the duffy ansible module can be used.

Additional Dependencies
-----------------------

Duffy doesn't require any additional dependencies, but does need to be included
in the Ansible library path to work properly. See the `ansible documentation
<http://docs.ansible.com/ansible/latest/intro_configuration.html#library>`_ for
help addding a library path.

Credentials Management
----------------------

Duffy uses a single file, generally found in the user's home directory, to
provide credentials. It contains a single line, which has the API key which is
passed to duffy via the API.

For LinchPin to provision, ``duffy.key`` must exist.

A duffy topology can have a ``credentials`` section for each
:term:`resource_group`, which requires a filename.

.. code-block:: yaml

    ---
    topology_name: topo
    resource_groups:
      - resource_group_name: duffy
        resource_group_type: duffy
        resource_definitions:

          .. snip ..

        credentials: duffy.key

By default, the location searched for the ``duffy.key`` is the user's home
directory, as stated above. However, the credentials path can be set using
``--creds-path`` option.  Assuming the ``duffy.key`` file was placed in
``~/.config/duffy``, using the topology described above, a provisioning task
could occur.

.. code-block:: bash

   $ linchpin -v --creds-path ~/.config/duffy up

Alternatively, the credentials path can be set as an environment variable,

.. code-block:: bash

   $ export CREDS_PATH="~/.config/duffy"
   $ linchpin -v up

