Topology Generation
===================

Broadly, a topology is a specification of which resources from which environments
are being requested from a linchpin run. Since each environment has different sets
of requirements, the exact values and structure of a topology file will vary based
on where resources are to be provisioned. In this document some broad discussion of
topologies will be addressed. More extensive examples pertaining to specific environments
will be given in a separate section of the documentation.

.. contents:: Topics

Topology
````````

Broadly speaking, a linchpin topology file is a list of resources to be provisioned from
each environment. It is possible and a very common use case to list multiple resources,
even multiple types of resources, in a single topology file. A less common use case, but
still supported, is to provision multiple resources across multiple environments.

The topology file does not designate the format of the output, nor map the particular
resources that get provisioned into output inventory groups. That is the work of the
layouts file.

Structure
`````````

A topology is a YAML file or a JSON file formatted with a single top-level object.

There are two top level keys in a topology.

The first key is named `topology_name` and is a relatively free-form string that identifies
the user-friendly name for this particular topology. For best practices, this should
resemble the file name and possibly the name of the key from the PinFile.

The second key is the `resource_groups` key. This key is an array of objects.

Resource Group
--------------

Each entry in the `resource_group` key array is itself an object hash with three
object keys.

The first key is `resource_group_name`, and is a user-friendly name for the
resources that will be provisioned from this group definition.

The second key is `res_group_type` and must be a string of a limited set. This set
must match to the particular environment. Some environments can define different types
of valid values. As an example, the value `duffy` will define a resource type to
be provisioned in a Duffy architecture, whereas the value `beaker` will contain definitions
of a set of servers to be provisioned in a Beaker environment.

The third key is `res_defs`. This key defines an array of objects. Each of these objects'
exact form will be dictated by the value of `res_group_type`. To see more information on
the structure of these values, check the example topologies section of this documentation.
