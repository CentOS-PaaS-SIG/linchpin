A :term:`PinFile` takes a :term:`topology` and an optional :term:`layout`, among other options, as a combined set of configurations as a resource for provisioning. An example :term:`Pinfile` is shown.

.. code-block:: yaml

    dummy_cluster:
      topology: dummy-topology.yml
      layout: dummy-layout.yml

The :term:`PinFile` collects the given :term:`topology` and :term:`layout` into one place. Many :term:`targets <target>` can be referenced in a single :term:`PinFile`.

More detail about the PinFile can be found in the :ref:`res_pinfiles` document.

Additional PinFile examples can be found in :docs1.5:`the source code <workspace>`


