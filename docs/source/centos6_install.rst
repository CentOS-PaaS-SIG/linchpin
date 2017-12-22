Installing LinchPin on CentOS 6
===============================

Installing LinchPin on CentOS 6 is a bit of a special snowflake. Because
of the age of the distribution, and the newness of the libraries used by
LinchPin, system packages and python packages will conflict.

.. note:: It's possible this document could be used to install RHEL6 packages
   as well. Please consult the Red Hat documentation.

Follow this document very carefully, completing each section in order. It's
imperative to a working LinchPin installation.

System Packages
---------------

Install the EPEL RPM.

.. code-block:: bash

    $ sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

Follow this up with the LinchPin dependencies. This shouldn't differ from the
standard :doc:`installation`.

.. code-block:: bash

    $ sudo yum install python-pip python-virtualenv libffi-devel \
    openssl-devel libyaml-devel gmp-devel libselinux-python make \
    gcc redhat-rpm-config libxml2-python libxslt-python

Next install some additional dependencies used for installing LinchPin via the
python pip package manager.

.. code-block:: bash

    $ sudo yum install gcc python-devel libxslt-devel \
    python-jinja2-26 libffi-devel

Pip Packages
------------

Because pip and setuptools from RPM are too old, update them.

.. note:: Using ``--force`` is required because otherwise other tools depend
   on a newer setuptools

.. code-block:: bash

    $ pip install pip setuptools --force --upgrade

So far this has been rather simple. This next part is critical. To address
`AttributeError: 'module' object has no attribute 'HAVE_DECL_MPZ_POWM_SEC
<https://github.com/ansible/ansible/issues/276#issuecomment-54228436>`_,
perform the following tasks in order.

.. code-block:: bash

    $ sudo pip uninstall pycrypto
    $ sudo yum install python-crypto python-paramiko

This removes the python-crypto RPM and pycrypto pip package, then puts the
older python-crypto RPM back. In a minute, we'll update that to a newer version.

When removing the above packages, it removed a few other dependencies. Add them
back here.

.. code-block:: bash

    $ sudo yum remove python-six python-requests python-urllib3
    $ sudo pip uninstall -y urllib3
    $ sudo yum install cloud-init
    $ sudo pip install six requests urllib3 PyOpenSSL --force --upgrade

Installing LinchPin
-------------------

Now it is time to install LinchPin.

.. code-block:: bash

    $ sudo pip install linchpin

Alternatively install from source.

.. code-block:: bash

    $ sudo yum install git
    $ git clone git://github.com/CentOS-PaaS-SIG/linchpin.git
    $ cd linchpin
    $ sudo pip install .

At this point, the ``linchpin`` command should work.

.. code-block:: bash

    $ linchpin --version
    linchpin version 1.5.0

Installation Script
-------------------

To make this easier, a script has been written which implements the above
steps. In can be run from the scripts directory in a linchpin git checkout.

:code1.5:`centos6_install.sh <scripts/centos6_install.sh>`

.. seealso::

    :doc:`providers`

