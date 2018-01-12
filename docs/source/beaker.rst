beaker
======

The Beaker (bkr) provider manages a single resource, ``bkr_server``.

bkr_server
----------

Beaker instances are provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/bkr-new.yml>`

The ansible modules for beaker are written and bundled as part of LinchPin.

* :code1.5:`bkr_server.py <linchpin/provisoin/library/bkr_server.py>`
* :code1.5:`bkr_info.py <linchpin/provisoin/library/bkr_info.py>`

Additional Dependencies
-----------------------

The beaker resource group requires several additional dependencies. The
following must be installed.

* beaker-client>=23.3

It is also recommended to install the python bindings for kerberos.

* python-krbV

For a Fedora 26 machine, the dependencies could be installed using dnf.

.. code-block:: bash

  $ sudo dnf install python-krbV
  $ wget https://beaker-project.org/yum/beaker-server-Fedora.repo
  $ sudo mv beaker-server-Fedora.repo /etc/yum.repos.d/
  $ sudo dnf install beaker-client

Alternatively, with pip, possibly within a virtual environment.

.. code-block:: bash

  $ pip install linchpin[beaker]


Credentials Management
----------------------

Beaker provides several ways to authenticate. LinchPin supports these methods.

* Kerberos
* OAuth2

.. note:: LinchPin doesn't support the username/password authentication
   mechanism. It's also not recommended by the Beaker Project, except for
   initial setup.

