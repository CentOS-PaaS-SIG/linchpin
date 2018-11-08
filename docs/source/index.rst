Introduction to LinchPin
========================

Welcome to the LinchPin documentation!

LinchPin is a simple and flexible hybrid cloud orchestration tool. Its intended purpose is managing cloud resources across multiple infrastructures. These resources can be provisioned, decommissioned, and configured all using declarative data and a simple command-line interface.

Additionally, LinchPin provides a Python API for managing resources. The cloud management component is backed by `Ansible <https://ansible.com>`_. The front-end API manages the interface between the command line (or other interfaces) and calls to the Ansible API.

This documentation covers LinchPin version (|release|). For recent features, see the updated |link-pre|\ |version|\ |link-post|.


.. _index-why-linchpin:

Why LinchPin?
=============

LinchPin provides a simple, declarative interface to a repeatable set of resources on cloud providers such as Amazon Web Services, Openstack, and Google Cloud Platform to help improve productivity and performance for you and your team. It's built on top of other proven resources, including Ansible and Python. LinchPin is built with a focus on Continuous Integration and Continuous Delivery tooling, in which its workflow excels.

LinchPin has some very useful features, including inventory generation, hooks, and more. Using these, specific cloud resources can be spun up for testing applications. By creating a single :ref:`PinFile` with your targets in an environment, you can simply run `linchpin up` and have your environment up and configured, ready for you to do your work with very little effort.

.. toctree::
   :maxdepth: 1

   getting_started
   docs
   developer_info
   faq
   community
   glossary

.. note:: Releases are formatted using `semanting versioning <https://semver.org>`_. If the release shown above is a pre-release version, the content listed may not be supported. Use `latest </en/latest>`_ for the most up-to-date documentation.

.. |link-pre| raw:: html

    <a href="https://github.com/CentOS-PaaS-SIG/linchpin/releases/tag/v

.. |link-post| raw:: html

    ">release notes</a>



.. autosummary::
   :toctree: _autosummary

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. include:: includes/footer.rst
