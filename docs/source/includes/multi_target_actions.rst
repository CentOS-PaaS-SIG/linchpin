LinchPin can :term:`provision` or :term:`teardown` any number of :term:`resources`. If a :term:`PinFile` has multiple :term:`targets <target>`, and is called without a target name, all targets will be executed. Given this PinFile.

.. code-block:: yaml

    example:
      topology: example-topology.yml
      layout: example-layout.yml

    example2:
      topology: example2-topology.yml
      layout: example2-layout.yml

    dummy1:
      topology: dummy-cluster.yml
      layout: dummy-layout.yml

A call to ``linchpin up`` would :term:`provision` and generate an Ansible static :term:`inventory` for each :term:`target`.

.. code-block:: bash

    $ linchpin up
    target: dummy1, action: up

    target: example2, action: up

    target: example, action: up

