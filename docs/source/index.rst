LinchPin documentation
=======================

About LinchPin
^^^^^^^^^^^^^^^

Welcome to the LinchPin documentation!

LinchPin is a hybrid cloud orchestration tool. Its intended purpose is managing cloud resources across multiple infrastructures. These resources can be provisioned, decommissioned, and configured all using a topology file and a simple command-line interface.

Additionally, LinchPin provides a Python API (and soon a RESTful API) for managing resources. The cloud management component is backed by `Ansible <https://ansible.com>`. The front-end API manages the interface between the command line (or other interfaces) and calls to the Ansible API.

This documentation covers the current released version of LinchPin (|version|). For recent features, we attempt to note in each section the version of LinchPin where the feature was added.


.. toctree::
   :maxdepth: 2

   intro
   installation
   getting_started
   configuration
   topologies
   community
   libdocs
   releases
   roadmap
   glossary


.. configuration
   linchpincli
   community

.. Using this as a guide (thanks Ansible)
   Introduction
   Quickstart
   Topologies
   Inventory Layouts
   CommandLine
   CommandLine: Advanced Options
   Detailed Guides
   Developer Information
   LinchPin API
   Community Information & Contributing
   Testing Strategies
   Frequently Asked Questions
   Glossary
   Python 3 Support


.. autosummary::
   :toctree: _autosummary


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

