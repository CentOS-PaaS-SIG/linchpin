LinchPin documentation
=======================

Welcome to the LinchPin documentation!

LinchPin is a simple and flexible hybrid cloud orchestration tool. Its intended purpose is managing cloud resources across multiple infrastructures. These resources can be provisioned, decommissioned, and configured all using declarative data and a simple command-line interface.

Additionally, LinchPin provides a Python API for managing resources. The cloud management component is backed by `Ansible <https://ansible.com>`_. The front-end API manages the interface between the command line (or other interfaces) and calls to the Ansible API.

This documentation covers LinchPin version (|release|). For recent features, see the updated |link-pre|\ |version|\ |link-post|.

.. note:: Releases are formatted using `semanting versioning <https://semver.org>`_. If the release shown above is a pre-release version, the content listed may not be supported. Use `latest </en/latest>`_ for the most up-to-date documentation.

.. |link-pre| raw:: html

    <a href="https://github.com/CentOS-PaaS-SIG/linchpin/releases/tag/v

.. |link-post| raw:: html

    ">release notes</a>


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
