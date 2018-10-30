PinFile
-------

A :term:`PinFile` takes a :term:`topology` and an optional :term:`layout`, among other options, as a combined set of configurations as a resource for provisioning. An example :term:`Pinfile` is shown.

The PinFile in the *simple* workspace is shown below.

.. code-block:: yaml

    1   ---
    2   simple:
    3       topology:
    4         topology_name: simple
    5         resource_groups:
    6           - resource_group_name: simple
    7             resource_group_type: dummy
    8             resource_definitions:
    9               - name: web
    10                role: dummy_node
    11                count: 2


The :term:`PinFile` collects the given :term:`topology` and :term:`layout` into one place. It's grouped together in a :term:`target`.

.. note:: Each of the lines of this PinFile are numbered to help identify lines discussed throughout this section. Each will be denoted with a superscript\ :sup:`1` next to its description.

Target
``````

In this :term:`PinFile`, the target\ :sup:`2` is the first line *simple*, just like the name of the workspace. The target is what LinchPin performs actions upon. For instance, typing ``linchpin up`` causes the PinFile to be read, and all targets evaluated. The *simple* target would be found, and then the resources listed would be provisioned.

A target will have subcomponents, which tell `linchpin` what it should do and how. Currently, those are :term:`topology`, :term:`layout`, and :term:`hooks`. For now, we will just cover the topology and its components.

Topology
++++++++

A topology\ :sup:`3`\  consists of several items. First and foremost is the topology_name\ :sup:`4`\, followed by one or more resource_groups\ :sup:`5`\. In this PinFile, there is only one resource group.

Resource Group
++++++++++++++

A resource group contains several items, minimally, it will have a resource_group_name\ :sup:`6`\, and a resource_group_type\ :sup:`7`\. The main component of a resource group, it its resource_definitions\ :sup:`8` section.

Resource Definitions
++++++++++++++++++++

Within a resource group, multiple resource definitions can exist. In many cases, there are desires for two different resources to be provisioned within a resource group. In this example, there is only one. Each provider has its own constraints for what is required. There are some common fields, however. In the example above, there is name\ :sup:`9`\, role\ :sup:`10`\, and count\ :sup:`11`\.

.. note:: The role relates to the ansible role used to perform provisioning. In this case, that's the *dummy_node* role. But many providers have multiple roles.

Definitions help, but lets see it in :doc:`action <simple_up>`.

.. note:: More detail about the PinFile can be found in the :ref:`res_pinfiles` document.



