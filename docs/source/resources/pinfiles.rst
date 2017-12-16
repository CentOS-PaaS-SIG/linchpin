These PinFiles represent many combinations of complexity and providers.

PinFiles are processed top to bottom.

YAML
````
PinFiles written using YAML format:

  * :docs1.5:`PinFile.dummy.yml <workspace/PinFile.dummy.yml>`
  * :docs1.5:`PinFile.openstack.yml <workspace/PinFile.openstack.yml>`
  * :docs1.5:`PinFile.complex.yml <workspace/PinFile.complex.yml>`

The combined format is only available in v1.5.0+

  * :docs1.5:`PinFile.combined.yml <workspace/PinFile.combined.yml>`

JSON
````

New in version 1.5.0

PinFiles written using JSON format.

  * :docs1.5:`PinFile.dummy.json <workspace/PinFile.dummy.json>`
  * :docs1.5:`PinFile.aws.json <workspace/PinFile.aws.json>`
  * :docs1.5:`PinFile.duffy.json <workspace/PinFile.duffy.json>`
  * :docs1.5:`PinFile.combined.json <workspace/PinFile.combined.json>`
  * :docs1.5:`PinFile.complex.json <workspace/PinFile.complex.json>`

Jinja2
``````

New in version 1.5.0

These PinFiles are examples of what can be done with templating using Jinja2.

Beaker Template
~~~~~~~~~~~~~~~

This template would be processed with a dictionary containing a key named `arches`.

  * :docs1.5:`PinFile.beaker.template <workspace/PinFile.beaker.template>`

.. code-block:: bash

    $ linchpin -p PinFile.beaker.template \
        --template-data '{ "arches": [ "x86_64", "ppc64le", "s390x" ]}' up

Libvirt Template and Data
~~~~~~~~~~~~~~~~~~~~~~~~~

This template and data can be processed together.

  * :docs1.5:`PinFile.libvirt-mi.template <workspace/PinFile.libvirt-mi.template>`
  * :docs1.5:`Data.libvirt-mi.yml <workspace/Data.libvirt-mi.yml>`

.. code-block:: bash

    $ linchpin -vp PinFile.libvirt-mi.template \
        --template-data Data.libvirt-mi.yml up

Scripts
```````

New in version 1.5.0

Scripts that generate valid JSON output to STDOUT can be processed and used.

  * :docs1.5:`generate_dummy.sh <workspace/scripts/generate_dummy.sh>`

.. code-block:: bash

    $ linchpin -vp ./scripts/generate_dummy.sh up

.. FIXME: change docs1.5 to example1.5

Output PinFile
``````````````

New in version 1.5.0

An output file can be created on an up/destroy action. Simply pass
the ``--output-pinfile`` option with a path to a writable file location.

.. code-block:: bash

    $ linchpin --output-pinfile /tmp/Pinfile.out -vp ./scripts/generate_dummy.sh up
    ..snip..
    $ cat /tmp/Pinfile.out
    {
        "dummy": {
            "layout": {
                "inventory_layout": {
                    "hosts": {
                        "example-node": {
                            "count": 3, 
                            "host_groups": [
                                "example"
                            ]
                        }
                    },
                    "vars": {
                        "hostname": "__IP__"
                    }
                }
            },
            "topology": {
                "topology_name": "dummy_cluster",
                "resource_groups": [
                    {
                        "resource_group_name": "dummy",
                        "resource_definitions": [
                            {
                                "count": 3,
                                "type": "dummy_node",
                                "name": "web"
                            },
                            {
                                "count": 1,
                                "type": "dummy_node",
                                "name": "test"
                            }
                        ],
                        "resource_group_type": "dummy"
                    }
                ]
            }
        }
    }

