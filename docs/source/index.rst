LinchPin documentation
=======================

Welcome to the LinchPin documentation!

LinchPin is a simple and flexible hybrid cloud orchestration tool. Its intended purpose is managing cloud resources across multiple infrastructures. These resources can be provisioned, decommissioned, and configured all using declarative data and a simple command-line interface.

Additionally, LinchPin provides a Python API for managing resources. The cloud management component is backed by `Ansible <https://ansible.com>`_. The front-end API manages the interface between the command line (or other interfaces) and calls to the Ansible API.

This documentation covers the current released version of LinchPin (|release|). For recent features, we attempt to note in each section the version of LinchPin where the feature was added.


.. toctree::
   :maxdepth: 1

   intro
   cli
   managing_resources
   providers
   configuration
   advanced_topics
   developer_info
   faq
   community
   glossary

.. autosummary::
   :toctree: _autosummary

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: includes/footer.rst
