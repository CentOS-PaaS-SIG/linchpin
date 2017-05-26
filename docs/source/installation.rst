Installation
============

.. contents:: Topics

.. _minimum_requirements:

.. note::

    If your operating system package manager has linchpin available for direct installation, you can skip this entire document
    and install directly from that source. If you are only looking to use the software and not develop it, this is the recommended
    approach. If your OS does not have a package available, or you plan to develop the software, then this document is for you

Minimum Requirements
````````````````````

Currently Linchpin can be run from any machine with Python 2.6 or 2.7, and Ansible 2.1.0  installed ( Windows isn't supported ).

This includes Red Hat, Debian, CentOS, OS X, any of the BSDs, and so on.

Refer to your specific operating system for directions on the best method to install Python, if it is not already installed. Many
modern operating systems will have Python already installed. This is typically the case in all versions of Linux and OS X, but
the version present might be older than the version needed for use with Ansible. You can check the version by typing
``python --version``.

Even if the system installed version of Python is older than 2.6, many systems will provide a method to install updated versions
of Python in parallel to the system version.

.. note::

    Ansible does not currently support Python 3. If your system has a version greater than 3.0, you will need to install
    Python 2.6 or 2.7.


.. _getting_ansible:

Prerequisite software packages
``````````````````````````````

There are several system packages that must be installed on a system prior to being able to install Ansible and linchpin. These
are necessary to get Ansible working properly. In CentOS or Fedora, the following command will install the necessary development
files on your system. A similar set of packages should be available on Mac OS X through Homebrew or Ubuntu through apt

* python-virtualenv
* libffi-devel
* openssl-devel
* libyaml-devel
* gmp-devel
* libselinux-python
* make

Install the necessary packages in Fedora with this command::

    sudo dnf install python-virtualenv libffi-devel openssl-devel libyaml-devel gmp-devel libselinux-python make

Install the necessary packages in CentOS with this command::

    sudo yum install python-virtualenv libffi-devel openssl-devel libyaml-devel gmp-devel libselinux-python make

If your intended usage includes connecting to any instance using Kerberos authentication - such as Beaker - then
install the necessary tools to handle Kerberos authentication::

    sudo dnf install krb5-workstation

Or on CentOS::

    sudo yum install krb5-workstation

You will need to configure Kerberos as required for your environment if you intend to use it as such.

.. note::
    A functioning C compiler is necessary to install some of the Python package dependencies. If your system does not have a
    compiler already avaliable, you will need to install one before moving on to the next step

.. _getting_linchpin:

Getting Linchpin
````````````````

If linchpin is available as a direct install package for your operating system, then using your OS's native installation tools
is encouraged for end users of the product who are not interested in or able to commit back changes to the source. Only stable,
reelased versions of linchpin should be available from your package manager of choice.

If linchpin is not avialble natively for your operating system, then you are encouraged to install the software
using a Python virtualenv. If you are unfamiliar with the usage of a virtualenv,
it is highly recommended that you stop at this point and go read about them. Such an introduction is beyond the scope of this
document, but is good background reading.

Create a virtualenv to install the package using the following sequence of commands::

    # Create a virtualenv in your uesr's home directory
    virtualenv ~/linchpin
    # Activate the virtualenv you just created - (Bash-style scripts)
    source ~/linchpin/bin/activate

Uesr Installation
-----------------

If you are interested in linchpin as a user, then it is not necessary to install the application from raw sources. Thus, after
activating a virtualenv, the following commands should suffice to create a working linchpin environment::

    # Fetch the source from github
    git clone https://github.com/CentOS-PaaS-SIG/linch-pin --recursive
    # Install linchpin - modify for version desired
    cd linch-pin
    pip install .


Developer Installation
----------------------

Developers, and those wishing to test pre-release versions of the software, will need to install linchpin from its source repository.
Once a virtualenv has been created and activated, the source can be downloaded and installed with the following commands::

    pip install git+https://github.com/CentOS-PaaS-SIG/linch-pin.git
