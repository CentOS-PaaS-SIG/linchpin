Getting Started
===============

.. toctree::
   :maxdepth: 1

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

Topology
~~~~~~~~

.. include:: includes/topologies.rst

Inventory Layout
~~~~~~~~~~~~~~~~

.. include:: includes/layouts.rst

PinFile
~~~~~~~

.. include:: getting_started/pinfile.rst

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
