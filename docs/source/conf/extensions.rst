The following settings are in the ``[extensions]`` section of the linchpin.conf.

These settings define the file extensions certain files have..


resource
~~~~~~~~

Deprecated in version 1.2.0

Removed in version 1.5.0

When generating resource output files, append this extension

.. code-block:: cfg

    resource = .output

inventory
~~~~~~~~~

When generating Ansible static inventory files, append this extension

.. code-block:: cfg

    inventory = .inventory

playbooks
~~~~~~~~~

New in version 1.5.0

Since playbooks fundamentially changed between v1.2.0 and v1.5.0, this
option was added for looking up a provider playbook. It's unlikely this
value will change.

.. code-block:: cfg

    playbooks = .yml

