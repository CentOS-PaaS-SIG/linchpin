.. _installation:

Installation
============

LinchPin can be run either as a container or as a bare-metal application

.. _docker_installation:

Docker Installation
-------------------

The LinchPin container is built using the latest Fedora image.  The image exists in the docker hub as contrainfra/linchpin and is updated with each release.  The image can also be build manually.

From within the config/Dockerfiles/linchpin directory:

.. code::

   $ sudo buildah bud -t linchpin .

Finally, to run the linchpin container:

.. code::

   $ sudo buildah run linchpin -v /path/to/workspace:/workdir -- linchpin -w /wordir up
   $ sudo buildah run linchpin -v /path/to/workspace:/workdir -- linchpin -w /workdir -vv destroy

.. note::
   Setting the CREDS_PATH environment variable pointing the /workdir is recommended.
   AWS credentials can also be passed as evironment variables when the container is run, named  AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID

.. note::
   Beaker uses kinit, which is installed in the container but must be run within the container after it starts
   The default /etc/krb5.conf for kerberos requires privilege escalation.  The linchpin Dockerfile replaces it with a version that eliminates this need


.. bare_metal_installation

Bare Metal Installation
-----------------------
Currently, LinchPin can be run from any machine with Python 2.6+ (Python 3.x is currently experimental), and requires Ansible 2.7.1 or newer.

.. note:: Some providers have additional dependencies. Additional software requirements can be found in the :doc:`providers` documentation.

Refer to your specific operating system for directions on the best method to install Python, if it is not already installed. Many modern operating systems will have Python already installed. This is typically the case in all versions of Linux and OS X, but the version present might be older than the version needed for use with Ansible. You can check the version by typing ``python --version``.

If the system installed version of Python is older than 2.6, many systems will provide a method to install updated versions of Python in parallel to the system version (eg. virtualenv).

.. _minimal_reqs:

Minimal Software Requirements
-----------------------------

As LinchPin is heavily dependent on Ansible 2.3.1 or newer, this is a core requirement. Beyond installing Ansible, there are several packages that need to be installed::

* libffi-devel
* openssl-devel
* libyaml-devel
* gmp-devel
* libselinux-python
* make
* gcc
* redhat-rpm-config
* libxml2-python
* libxslt-python

For CentOS or RHEL the following packages should be installed:

.. code-block:: bash

    $ sudo yum install python-pip python-virtualenv libffi-devel \
    openssl-devel libyaml-devel gmp-devel libselinux-python make \
    gcc redhat-rpm-config libxml2-python libxslt-python

.. attention:: CentOS 6 (and likely RHEL 6) require special care during installation. See :doc:`centos6_install` for more detail.

For Fedora 26+ the following packages should be installed:

.. code-block:: bash

    $ sudo dnf install python-virtualenv libffi-devel \
    openssl-devel libyaml-devel gmp-devel libselinux-python make \
    gcc redhat-rpm-config libxml2-python libxslt-python

.. _installing_linchpin:

Installing LinchPin
-------------------

.. note:: Currently, linchpin is not packaged for any major Operating System. If you'd like to contribute your time to create a package, please contact the `linchpin mailing list <mailto:linchpin@redhat.com>`_.

Create a virtualenv to install the package using the following sequence of commands (requires virtualenvwrapper)

.. code-block:: bash

    $ mkvirtualenv linchpin
    ..snip..
    (linchpin) $ pip install linchpin
    ..snip..

Using mkvirtualenv with Python 3 (now default on some Linux systems) will attempt to link to the `python3` binary. LinchPin isn't fully compatible with Python 3 yet. However, mkvirtualenv provides the ``-p`` option for specifying the `python2` binary.

.. code-block:: bash

    $ mkvirtualenv linchpin -p $(which python2)
    ..snip..
    (linchpin) $ pip install linchpin
    ..snip..

.. note:: mkvirtualenv is optional dependency you can install from `here <http://virtualenvwrapper.readthedocs.io/en/latest/install.html>`_. An alternative, virtualenv, also exists. Please refer to the `virtualenv documentation <https://virtualenv.pypa.io/en/stable/>`_ for more details.


To deactivate the virtualenv

.. code-block:: bash

    (linchpin) $ deactivate
    $

Then reactivate the virtualenv

.. code-block:: bash

    $ workon linchpin
    (linchpin) $

If testing or docs is desired, additional steps are required

.. code-block:: bash

    (linchpin) $ pip install linchpin[docs]
    (linchpin) $ pip install linchpin[tests]

Virtual Environments and SELinux
````````````````````````````````

When using a virtualenv with SELinux enabled, LinchPin may fail due to an error related to with the libselinux-python libraries. This is because the libselinux-python binary needs to be enabled in the Virtual Environment. Because this library affects the filesystem, it isn't provided as a standard python module via pip. The RPM must be installed, then a symlink must occur.

.. code-block:: bash

    (linchpin) $ sudo dnf install libselinux-python
    .. snip ..
    (linchpin) $ echo ${VIRTUAL_ENV}
    /path/to/virtualenvs/linchpin
    (linchpin) $ export VENV_LIB_PATH=lib/python2.7/site-packages
    (linchpin) $ export LIBSELINUX_PATH=/usr/lib64/python2.7/site-packages # make sure to verify this location
    (linchpin) $ ln -s ${LIBSELINUX_PATH}/selinux ${VIRTUAL_ENV}/${VENV_LIB_PATH}
    (linchpin) $ ln -s ${LIBSELINUX_PATH}/_selinux.so ${VIRTUAL_ENV}/${VENV_LIB_PATH}

.. note:: A script is provided to do this work at :code1.5:`scripts/install_selinux_venv.sh`

Installing on Fedora 26
-----------------------

Install RPM pre-reqs

.. code-block:: bash

    $ sudo dnf -y install python-virtualenv libffi-devel openssl-devel libyaml-devel gmp-devel libselinux-python make gcc redhat-rpm-config libxml2-python


Create a working-directory

.. code-block:: bash

    $ mkdir mywork
    $ cd mywork

Create linchpin directory, make a virtual environment, activate the virtual environment

.. code-block:: bash

    $ mkvirtualenv linchpin
    ..snip..
    (linchpin) $ pip install linchpin

Make a workspace, and initialize it to prove that linchpin itself works

.. code-block:: bash

    (linchpin) $ mkdir workspace
    (linchpin) $ cd workspace
    (linchpin) $ linchpin init
    PinFile and file structure created at /home/user/workspace

.. note:: The default workspace is $PWD, but can be set using the $WORKSPACE variable.

Installing on RHEL 7.4
----------------------

Tested on RHEL 7.4 Server VM which was kickstarted and pre-installed with the following YUM package-groups and RPMs::

* @core
* @base
* vim-enhanced
* bash-completion
* scl-utils
* wget

For RHEL 7, it is assumed that you have access to normal RHEL7 YUM repos via RHSM or by pointing at your own http YUM repos, specifically the following repos or their equivalents::

* rhel-7-server-rpms
* rhel-7-server-optional-rpms

Install pre-req RPMs via YUM:

.. code-block:: bash

    $ sudo yum install -y libffi-devel openssl-devel libyaml-devel gmp-devel libselinux-python make gcc redhat-rpm-config libxml2-devel libxslt-devel libxslt-python libxslt-python

To get a working python 2.7 pip and virtualenv either use EPEL

.. code-block:: bash

    $ sudo rpm -ivh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

Install python pip and virtualenv:

.. code-block:: bash

    $ sudo yum install -y python2-pip python-virtualenv

Create a working-directory

.. code-block:: bash

    $ mkdir mywork
    $ cd mywork

Create linchpin directory, make a virtual environment, activate the virtual environment

.. code-block:: bash

    $ mkvirtualenv linchpin
    ..snip..
    (linchpin) $ pip install linchpin

Inside the virtualenv, upgrade pip and setuptools because the EPEL versions are too old.

.. code-block:: bash

    (linchpin) $ pip install -U pip
    (linchpin) $ pip install -U setuptools

Install linchpin

.. code-block:: bash

    (linchpin) $ pip install linchpin

Make a workspace, and initialize it to prove that linchpin itself works

.. code-block:: bash

    (linchpin) $ mkdir workspace
    (linchpin) $ cd workspace
    (linchpin) $ linchpin init
    PinFile and file structure created at /home/user/workspace

Source Installation
-------------------

As an alternative, LinchPin can be installed via github. This may be done in order to fix a bug, or contribute to the project.

.. code-block:: bash

    $ git clone git://github.com/CentOS-PaaS-SIG/linchpin
    ..snip..
    $ cd linchpin
    $ mkvirtualenv linchpin
    ..snip..
    (linchpin) $ pip install file://$PWD/linchpin

linchpin setup : Automatic Dependency installation:
---------------------------------------------------
From version 1.6.5 linchpin includes linchpin setup commandline option to automate installations of linchpin dependencies. 
linchpin setup uses built in ansible-playbooks to carryout the installations. 

Install all the dependencies:

.. code-block:: bash

    $ linchpin setup

To install only a subset of dependencies, pass as arguments list:

.. code-block:: bash

    $ linchpin setup beaker docs

It also supports ask-sudo-pass parameter when installing dnf related dependencies:

.. code-block:: bash

   $ linchpin setup libvirt --ask-sudo-pass
