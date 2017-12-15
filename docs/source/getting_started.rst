Getting Started
===============

.. contents:: Topics

.. _foreword:

This guide will walk you through the basics of using LinchPin. LinchPin is a command-line utility, a Python API, and Ansible playbooks. As this guide is intentionally quite brief to get you started, a more complete version can be found in the documentation links found in the :doc:`index <index>`.

.. _terminology:


Running the ``linchpin`` command
--------------------------------

.. include:: includes/linchpin_cli.rst

Initialization (init)
---------------------

.. include:: includes/initialization.rst

The Workspace
`````````````

.. include:: includes/workspace.rst


Resources
---------

With LinchPin, resources are king. Defining, managing and output are all declarative. Resources are managed via the :term:`PinFile`. The PinFile can hold two additional files, the :term:`topology`, and :term:`layout`. Linchpin also supports :doc:`hooks`.


Topology
````````

.. include:: includes/topologies.rst

Inventory Layout
````````````````

.. include:: includes/layouts.rst


PinFile
```````

.. include:: includes/pinfile.rst


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

    :doc:`linchpin_cli`
        Linchpin Command-Line Interface
    :doc:`managing_resources`
        Managing Resources
    :doc:`providers`
        Available Providers
