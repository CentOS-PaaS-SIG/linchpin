A :term:`PinFile` takes a :term:`topology` and an optional :term:`layout`, among other options, as a combined set of configurations as a resource for provisioning. An example :term:`Pinfile` is shown.

.. code-block:: yaml

    dummy_cluster:
      topology: dummy-topology.yml
      layout: dummy-layout.yml

The :term:`PinFile` collects the given :term:`topology` and :term:`layout` into one place. Many :term:`targets <target>` can be referenced in a single :term:`PinFile`.

JSON PinFile
~~~~~~~~~~~~

New in version 1.5.0

The :term:`PinFile` can also use JSON.

.. code-block:: json

    {
        "dummy": {
            "topology": "dummy-topology.yml",
            "layout:": "dummy-layout.yml"
        }
    }



Additionally, both the topology, and layout can be included inline.

.. code-block:: json

    {
        "dummy": {
            "topology": {
                "resource_groups": [
                    {
                        "resource_definitions": [
                            {
                                "count": 3,
                                "name": "web",
                                "role": "dummy_node"
                            }
                        ],
                        "resource_group_name": "dummy",
                        "resource_group_type": "dummy"
                    }
                ],
                "topology_name": "dummy_cluster"
            },
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
            }
        }
    }


Generated PinFile
~~~~~~~~~~~~~~~~~

New in version 1.5.0

Jinja2 Templates
++++++++++++++++

A PinFile can also be generated via `Jinja2 <http://jinja.pocoo.org/docs/2.10/>`_ templates. Consider this template named ``PinFile.libvirt-mi.template``.

.. code-block:: none

    ---
    libvirt-mi:
      topology:
        topology_name: "libvirt-multi"
        resource_groups:
          - resource_group_name: "libvirt-mi"
            resource_group_type: "libvirt"
            res_defs:
            {% for instance in instances %}
              - role: libvirt_node
                name: {{ instance.name }}
                image_src: {{ instance.src }}
                memory: 1024
                vcpus: 1
                arch: {{ instance.arch | default('x86_64') }}
                networks:
                  - name: default
            {% endfor %}


In the same workspace is this file, named ``Data.libvirt-my.yml``.

.. code-block:: yaml

    ---
    instances:
      - name: centos71
        src: http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1608.qcow2.xz
      - name: centos66
        src: http://cloud.centos.org/centos/6.6/images/CentOS-6-x86_64-GenericCloud-1711.qcow2.xz

Execute the linchpin command, passing these two files.

.. code-block:: bash

    linchpin -vp PinFile.libvirt-mi.template --template-data Data.libvirt-my.yml up

Would yield output that would be provisionable.

.. code-block:: json

    {
        "libvirt-mi": {
            "topology": {
                "topology_name": "libvirt-multi",
                "resource_groups": [
                    {
                        "resource_group_name": "libvirt-mi",
                        "resource_group_type": "libvirt",
                        "res_defs": [
                            {
                                "name": "centos71",
                                "networks": [
                                    {
                                        "name": "default"
                                    }
                                ], 
                                "vcpus": 1,
                                "role": "libvirt_node",
                                "memory": 1024,
                                "arch": "x86_64",
                                "image_src": "http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1608.qcow2.xz"
                            }, 
                            {
                                "name": "centos66",
                                "networks": [
                                    {
                                        "name": "default"
                                    }
                                ], 
                                "vcpus": 1,
                                "role": "libvirt_node",
                                "memory": 1024,
                                "arch": "x86_64",
                                "image_src": "http://cloud.centos.org/centos/6.6/images/CentOS-6-x86_64-GenericCloud-1711.qcow2.xz"
                            }
                        ]
                    }
                ]
            }
        }
    }

.. note:: Output data can also be saved, if desired, by adding the ``--output-pinfile /path/to/PinFile.libvirt-mi.generated``.


Additional PinFile examples can be found in :dirs1.5:`the source code <workspace>`.

.. FIXME: Update PinFiles. Provide expanded examples in both YAML and JSON.

