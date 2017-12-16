Configuration File
==================

.. toctree::
   :maxdepth: 1

.. contents:: Topics

Below is full coverage of each of the sections of the values available in `linchpin.conf <https://raw.githubusercontent.com/CentOS-PaaS-SIG/linchpin/develop/linchpin/linchpin.conf>`_

General Configuration
---------------------

Managing LinchPin requires a few configuration files. Beyond
:docs1.5:`linchpin.conf`, there are a few other configurations that are
checked . When running linchpin, four different locations are checked for
linchpin.conf files. Files are checked in the following order:

1. linchpin/library/path/linchpin.conf
2. /etc/linchpin.conf
3. ~/.config/linchpin/linchpin.conf
4. path/to/workspace/linchpin.conf

The linchpin configuration parser supports overriding and extension of
configurations. Therefore, the existing configuration files are read.
If linchpin finds the same configuration section header in more than one file,
the header that was parsed more recently will provide the configuration for that
section. In this way user can override the general configurations. Commonly,
this is done by placing a `linchpin.conf` in the root of the :term:`workspace`.

Getting the most current configuration
--------------------------------------

If you are installing LinchPin from a package manager (pip or RPM), the latest linchpin.conf is already included in the library.

An `example linchpin.conf is available on Github <https://raw.githubusercontent.com/CentOS-PaaS-SIG/linchpin/develop/linchpin/linchpin.conf>`_

.. FIXME: The above link should point to an example in the docs, even if it's a symlink.

For in-depth details of all the options, see the :doc:`Configuration Reference <configuration>` document.

Environmental Variables
-----------------------

LinchPin allows configuration adjustments via environment variables in some cases. If these environment variables are set, they will take precedence over any settings in the configuration file.

A full listing of available environment variables, see the :doc:`Configuration Reference <configuration>` document.

Command Line Options
--------------------

Some configuration options are also present in the command line. Settings passed via the command line will override those passed through the configuration file and the environment.

The full list of options is covered in the :doc:`cli` document.

Values by Section
-----------------

The configuration file is broken into sections. Each section controls a specific functionality in LinchPin.

General Defaults
````````````````

.. include:: conf/defaults.rst
.. include:: conf/lp.rst

Extra Vars
``````````

LinchPin sets several :term:`extra_vars` values, which are passed to the provisioning playbooks.

.. include:: conf/evars.rst

..   conf_init
..   conf_logger
..   conf_console
..   conf_hookstates
..   conf_extensions
..   conf_ansible
..   conf_states
..   conf_repository_control
..   conf_fetch_types
..   conf_fetch_aliases


.. seealso::

    `User Mailing List <https://www.redhat.com/mailman/listinfo/linchpin>`_
        Subscribe and participate. A great place for Q&A
    `irc.freenode.net <http://irc.freenode.net>`_
        #linchpin IRC chat channel
