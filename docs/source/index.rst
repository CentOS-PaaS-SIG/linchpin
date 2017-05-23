LinchPin documentation
=======================

About LinchPin
^^^^^^^^^^^^^^^

Welcome to the LinchPin documentation!

LinchPin is a hybrid cloud orchestration tool. Its intended purpose is managing cloud resources across multiple infrastructures. These resources can be provisioned, decommissioned, and configured all using a topology file and a simple command-line interface.

Additionally, LinchPin provides an python API (and soon a RESTful API) for managing the resources. The cloud provisioning component is backed by `Ansible <https://ansible.com>`. The front-end API manages the interface between the command line (or other interfaces) and callse to the Ansible API.

This documentation covers the current released version of LinchPin (|version|). For recent features, we attempt to note in each section the version of LinchPin where the feature was added.


.. toctree::
   :maxdepth: 1

   intro
   config
   topologies
   linchpincli
   libdocs

.. autosummary::
   :toctree: _autosummary


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

