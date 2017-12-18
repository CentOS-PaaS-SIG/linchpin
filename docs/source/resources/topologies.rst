These topologies represent many combinations of complexity and providers.
Topologies process :term:`resource_definitions` top to bottom according to the file.

Topologies have evolved a little and have a slightly different format between
versions. However, older versions still work on v1.5.0+ (until otherwise noted).

The difference is quite minor, except in two providers, beaker and openshift.

Topology Format Pre v1.5.0
``````````````````````````

.. code-block:: yaml

    ---
    topology_name: "dummy_cluster" # topology name
    resource_groups:
      - resource_group_name: "dummy"
        resource_group_type: "dummy"
        resource_definitions:
          - name: "web"
            type: "dummy_node" <-- this is called 'type`
            count: 1

v1.5.0+ Topology Format
```````````````````````

.. code-block:: yaml

    ---
    topology_name: "dummy_cluster" # topology name
    resource_groups:
      - resource_group_name: "dummy"
        resource_group_type: "dummy"
        resource_definitions:
          - name: "web"
            role: "dummy_node" <-- this is called 'role`
            count: 1

The subtle difference is in the `resource_definitions` section. In the pre-v1.5.0 topology,
the key was `type`, in v1.5.0+, the key is `role`.

.. note:: Pay attention to the callout in the code blocks above.

For details about the differences in beaker and openshift,
see :doc:`../topology_incompatibilities`.

YAML
````
New in version 1.5.0

Topologies written using YAML format:

  * :docs1.5:`os-server-new.yml <workspace/topologies/os-server-new.yml>`
  * :docs1.5:`libvirt-new.yml <workspace/topologies/libvirt-new.yml>`
  * :docs1.5:`bkr-new.yml <workspace/topologies/bkr-new.yml>`

Older topologies, supported in v1.5.0+

  * :docs1.5:`os-server.yml <workspace/topologies/os-server.yml>`
  * :docs1.5:`libvirt.yml <workspace/topologies/libvirt.yml>`
  * :docs1.5:`bkr.yml <workspace/topologies/bkr.yml>`

JSON
````

New in version 1.5.0

Topologies can be written using JSON format.

  * :docs1.5:`dummy.json <workspace/topologies/dummy.json>`

Jinja2
``````

New in version 1.5.0

Topologies can be processed as templates using Jinja2.

Jenkins-Slave Template
~~~~~~~~~~~~~~~~~~~~~~

This topology template would be processed with a dictionary containing one key named `arch`.

  * :docs1.5:`jenkins-slave.j2 <workspace/topologies/jenkins-slave.j2>`

The PinFile.jenkins.yml contains the reference to the `jenkins-slave` topology.

.. code-block:: yaml

    jenkins-slave:
      topology: jenkins-slave.yml
      layout: jenkins-slave.yml


.. seealso:: :docs1.5:`Pinfile.jenkins.j2 <workspace/PinFile.jenkins.j2>`

.. code-block:: bash

    $ linchpin -p PinFile.jenkins --template-data '{ "arch": "x86_64" }' up


