PinFile
-------

A :term:`PinFile` takes a :term:`topology` and an optional :term:`layout`, among other options, as a combined set of configurations as a resource for provisioning. An example :term:`Pinfile` is shown.

The *simple* PinFile is shown below

.. code-block:: yaml

    ---
    simple:
      topology:
        topology_name: simple
        resource_groups:
          - resource_group_name: simple
            resource_group_type: dummy
            resource_definitions:
              - name: web
                role: dummy_node
                count: 2


The :term:`PinFile` collects the given :term:`topology` and :term:`layout` into one place. It's grouped together in a :term:`target`. 

Target
``````

In this :term:`PinFile`, the `target` is the first line *simple*, just like the name of the workspace. The target is what LinchPin performs actions upon. For instance, typing `linchpin up` causes the PinFile to be read, and all targets evaluated. The *simple* target would be found, and then the resources listed would be provisioned.

A `target` will have subcomponents, which tell `linchpin` what it should do and how. Currently, those are :term:`topology`, :term:`layout`, and :term:`hooks`. For now, we will just cover the topology and its components.

Topology
++++++++




.. note:: More detail about the PinFile can be found in the :ref:`res_pinfiles` document.

.. note:: Additional PinFile examples can be found in :dirs1.5:`the source code <workspaces>`


