The following settings are in the ``[DEFAULT]`` section of the linchpin.conf

.. warning:: The configurations in this section should NOT be changed unless you know what you are doing.

pkg
~~~

This defines the package name. Many components base paths and other
information from this setting.

.. code-block:: cfg

    pkg = linchpin

default_config_path
~~~~~~~~~~~~~~~~~~~

New in version 1.2.0

Where configuration files might land, such as the workspaces.conf,
or credentials. Generally used in combination with other configurations.

.. code-block:: cfg

    default_config_path = ~/.config/linchpin

external_providers_path
~~~~~~~~~~~~~~~~~~~~~~~

New in version 1.5.0

Developers can provide additional provider playbooks and schemas.
This configuration is used to set the path(s) to look for additional providers.

.. code-block:: cfg

    external_providers_path = %(default_config_path)s/linchpin-x


The following settings are in the ``[init]`` section of the linchpin.conf

source
~~~~~~

Source path of files provided for the ``linchpin init`` command.

.. code-block:: cfg

    source = templates/

pinfile
~~~~~~~

Formal name of the PinFile. Can be changed as desired.

.. code-block:: cfg

    pinfile = PinFile

.. FIXME: consider adjusting init.pinfile to use this one somehow
