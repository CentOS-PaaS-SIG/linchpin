A :term:`PinFile` takes a :term:`topology` and an optional :term:`layout`, among other options, as a combined set of configurations as a resource for provisioning. An example :term:`Pinfile` is shown.

.. code-block:: yaml

    dummy1:
      topology: dummy-cluster.yml
      layout: dummy-layout.yml

The :term:`PinFile` collects the given :term:`topology` and :term:`layout` into one place. Many :term:`targets <target>` can be referenced in a single :term:`PinFile`.

The :term:`target` above is named `dummy1`. This :term:`target` is the reference to the :term:`topology` named `dummy-cluster.yml` and :term:`layout` named `dummy-layout.yml`. The :term:`PinFile` can also contain definitions of :term:`hooks <hook>` that can be executed at certain pre-defined states.

.. _running_linchpin:
