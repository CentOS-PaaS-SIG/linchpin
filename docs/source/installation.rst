Installation
============

.. contents:: Topics

Currently, LinchPin can be run from any machine with Python 2.6+ (Python 3.x is currently experimental), and requires Ansible 2.2.1. There are many other dependencies, depending on the provider. The core providers are `OpenStack`, `Amazon EC2`, and `Google Compute Cloud`. If enabled on the host system, `Libvirt` can also be used out of the box.

Refer to your specific operating system for directions on the best method to install Python, if it is not already installed. Many modern operating systems will have Python already installed. This is typically the case in all versions of Linux and OS X, but the version present might be older than the version needed for use with Ansible. You can check the version by typing ``python --version``.

If the system installed version of Python is older than 2.6, many systems will provide a method to install updated versions of Python in parallel to the system version (eg. virtualenv).

.. _minimal_reqs:

Minimal Software Requirements
``````````````````````````````

As LinchPin is heavily dependent on Ansible, this is a core requirement. Beyond installing Ansible, there are several packages that need to be installed::

* libffi-devel
* openssl-devel
* libyaml-devel
* gmp-devel
* libselinux-python
* make

For Fedora/CentOS/RHEL the necessary packages should be installed.

.. code-block:: bash

    $ sudo yum install python-virtualenv libffi-devel \
    openssl-devel libyaml-devel gmp-devel libselinux-python make

.. note:: Fedora will present an output suggesting the use of `dnf` as a replacement for yum.


.. _installing_linchpin:

Installing LinchPin
````````````````````

.. note:: Currently, linchpin is not packaged for any major Operating System. If you'd like to contribute your time to create a package, please contact the `linchpin mailing list <mailto:linchpin@redhat.com>`_.

Create a virtualenv to install the package using the following sequence of commands (requires virtualenvwrapper).

.. code-block:: bash

    $ mkvirtualenv linchpin
    ..snip..
    (linchpin) $ pip install linchpin
    ..snip..

To deactivate the virtualenv.

.. code-block:: bash

    (linchpin) $ deactivate
    $

Then reactivate the virtualenv.

.. code-block:: bash

    $ workon linchpin
    (linchpin) $

If testing or docs is desired, additional steps are required.

.. code-block:: bash

    (linchpin) $ pip install linchpin[docs]
    (linchpin) $ pip install linchpin[tests]

Source Installation
-------------------

As an alternative, LinchPin can be installed via github. This may be done in order to fix a bug, or contribute to the project.

.. code-block:: bash

    (linchpin) $ git clone git://github.com/CentOS-PaaS-SIG/linch-pin
    ..snip..
    (linchpin) $ pip install ./linch-pin


.. seealso::

    `User Mailing List <https://www.redhat.com/mailman/listinfo/linchpin>`_
        Subscribe and participate. A great place for Q&A
    `irc.freenode.net <http://irc.freenode.net>`_
        #linchpin IRC chat channel
