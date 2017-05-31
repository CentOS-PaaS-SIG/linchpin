Getting Started
===============

.. toctree::
   :maxdepth: 1
   :tocdepth: 1

.. contents:: Topics

.. _foreword:

Foreword
````````

Now that LinchPin is installed according to :doc:`installation`, it is time to see how it works. This guide is essentially a quick start guide to getting up and running with LinchPin.

LinchPin is a command-line utility, a Python API, and Ansible playbooks. This document focuses on the command-line interface.

.. _terminology:

Terminology
```````````

LinchPin, while it attempts to be a simple tool for provisioning resources, still does have some complexity. To that end, this section attempts to define the minimal bits of terminology needed to understand how to use the ``linchpin`` command-line utility.

Topology
--------

.. include:: includes/topologies.rst

Inventory Layout
----------------

.. include:: includes/layouts.rst

PinFile
-------

.. include:: includes/pinfile.rst

Running ``linchpin``
````````````````````

As stated above, this guide is about using the command-line utility, ``linchpin``. First off, simply execute ``linchpin`` to see some options.

.. code-block:: bash

    $ linchpin
    Usage: linchpin [OPTIONS] COMMAND [ARGS]...

      linchpin: hybrid cloud orchestration

    Options:
      -c, --config PATH       Path to config file
      -w, --workspace PATH    Use the specified workspace if the familiar Jenkins
                              $WORKSPACE environment variable is not set
      -v, --verbose           Enable verbose output
      --version               Prints the version and exits
      --creds-path PATH       Use the specified credentials path if WORKSPACE
                              environment variable is not set
      -h, --help              Show this message and exit.

    Commands:
      init     Initializes a linchpin project.
      up       Provisions nodes from the given target(s) in...
      destroy  Destroys nodes from the given target(s) in...

What can be seen immediately is a simple description, along with options and arguments that can be passed to the command. The three commands found near the bottom of this help are where the focus will be for this document.

Initialization (init)
---------------------

.. include:: includes/initialization.rst

Provisioning (up)
------------------

.. include:: includes/provisioning.rst

Teardown (destroy)
------------------

.. include:: includes/teardown_destroy.rst

Multi-Target Actions
--------------------

.. include:: includes/multi_target_actions.rst

.. seealso::

    :doc:`linchpincli`
        Linchpin Command-Line Interface
    `User Mailing List <https://www.redhat.com/mailman/listinfo/linchpin>`_
        Subscribe and participate. A great place for Q&A
    `irc.freenode.net <http://irc.freenode.net>`_
        #linchpin IRC chat channel
