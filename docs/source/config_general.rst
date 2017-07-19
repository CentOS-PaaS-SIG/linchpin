General Configuration
=====================

Managing LinchPin requires a few configuration files. Beyond `linchpin.conf`, 
there are a few other configurations that need to be created. When running linchpin, 
four different locations are checked for linchpin.conf files. 
Files are checked in the following order:

1. linchpin/library/path/linchpin.conf
2. /etc/linchpin.conf
3. ~/.config/linchpin/linchpin.conf
4. path/to/workspace/linchpin.conf

The linchpin configuration parser supports overriding and extension of
configurations. Therefore, after the files are checked for existence, the
existing configuration files are read and if linchpin finds two or more
different configuration files to contain the same configuration section header,
the header that was parsed more recently will provide the configuration for that
section. Therefore, if the user wants to add their own configurations to their
linchpin workpace, the the user should add their configurations to a
linchpin.conf file in the root of their workspace. This way, their file will be
parsed last and their configurations will take precedence over all other
configurations.

To add your own configurations, simply create a linchpin.conf file in the root
of your workspace using your preferred text editor and write configuration in a
`.ini` style. Here's an example:

::
    [Section Header]
    key1 = value1
    key2 = value2


.. contents:: Topics

Workspace
`````````

.. include:: includes/workspace.rst

Initialization
``````````````

.. include:: includes/initialization.rst

PinFile
```````

.. include:: includes/pinfile.rst

Topologies
``````````

.. include:: includes/topologies.rst

Inventory Layouts
`````````````````

.. include:: includes/layouts.rst

