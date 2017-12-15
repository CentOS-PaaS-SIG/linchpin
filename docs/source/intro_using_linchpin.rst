Using LinchPin
==============

Almost all interactions with LinchPin are done through the command-line interface.

The interface is through the ``linchpin`` command. There are many subcommands available, and are covered :doc:`here <linchpin_cli>`. The most common are ``linchpin up`` and ``linchpin destroy``. If you run ``linchpin`` by itself, a help page will be displayed showing the available subcommands. Additionally, each subcommand has its own help by passing a ``-h``.

.. toctree::
   :tocdepth: 1

.. contents:: Topics

.. _help:

Getting Help
------------

.. include:: includes/cli_help.rst

.. _basic_usage:

Basic Usage
-----------

.. include:: includes/cli_basic_usage.rst

.. _options:

Options and Arguments
---------------------

.. include:: includes/cli_opts_args.rst

.. _combining_options:

Combining Options
-----------------

.. include:: includes/cli_combine_opts.rst

.. _common_usage:

Common Usage
------------

Here are some common use cases for the linchpin command-line.

.. include:: includes/cli_common_usage.rst

.. _topology:

Topologies
----------

.. include:: includes/topologies.rst

.. _layout:

Inventory Layouts
-----------------

.. include:: includes/layouts.rst

.. _pinfile:

PinFile
-------

.. include:: includes/pinfile.rst

.. _provisioning:

Provisioning (up)
-----------------

.. include:: includes/provisioning.rst

.. _teardown:

Teardown (destroy)
------------------

.. include:: includes/teardown_destroy.rst
