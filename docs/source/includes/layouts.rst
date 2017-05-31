The :term:`inventory_layout <layout>` or :term:`layout` mean the same thing, a YAML definition for providing an Ansible static inventory file, based upon the provided topology. A YAML :term:`layout` is stored in a :term:`layout_file`.

.. code-block:: yaml

    ---
    inventory_layout:
      vars:
        hostname: __IP__
      hosts:
        example-node:
          count: 3
          host_groups:
            - example
      host_groups:
        example:
          vars:
            test: one

The above YAML allows for interpolation of the ip address, or hostname as a component of a generated inventory. A host group called `example` will be added to the Ansible static inventory, along with a section called `example:vars` containing `test = one`. The resulting static Ansible inventory is shown here.

.. code-block:: cfg

    [example:vars]
    test = one

    [example]
    web-2.example.net hostname=web-2.example.net
    web-1.example.net hostname=web-1.example.net
    web-0.example.net hostname=web-0.example.net

    [all]
    web-2.example.net hostname=web-2.example.net
    web-1.example.net hostname=web-1.example.net
    web-0.example.net hostname=web-0.example.net
