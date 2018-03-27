Inventory Layouts
-----------------

When generating an inventory, LinchPin provides some very flexible options. From the simple :ref:`res_layouts` to much more complex options, detailed here.

inventory_file
``````````````
New in version 1.5.2

When an :term:`layout` is provided in the PinFile, LinchPin automatically generates
a static inventory for Ansible. The inventory filename is dynamically generated based
upon a few factors. However, the value can be overridden simply by adding the
``inventory_file`` option.

.. code-block:: bash

    ---
    inventory_layout:
      inventory_file: /path/to/dummy.inventory
      vars:
      .. snip ..

Using LinchPin or Ansible variables
```````````````````````````````````

New in version 1.5.2

It's likely that the inventory file is based upon specific Linchpin
(or Ansible) variables. In this case, the values need to be wrapped as
raw values. This allows LinchPin to read the string in unparsed and
pass it to the Ansible parser.

.. code-block:: bash

    inventory_layout:
      inventory_file: "{% raw -%}{{ workspace }}/inventories/dummy-new-{{ uhash }}.inventory{%- endraw %}"

Using Environment variables
```````````````````````````

Additionally, using environment variables requires the raw values.

.. code-block:: bash

  host_groups:
    all:
      vars:
        ansible_user: root
        ansible_private_key_file: |
            "{% raw -%}{{ lookup('env', 'TESTLP') | default('/tmp', true) }}/CSS/keystore/css-central{%- endraw %}"

