Docker
======

The docker provider manages a ``docker_container`` resource.

* :docs1.5:`Topology Example <workspaces/docker/topologies/docker-new.yml>`

docker_container
----------------

The ``docker_container`` resource provides the ability to provision a Docker
container. It is implemented as a wrapper around the Ansible's `docker_container <https://docs.ansible.com/ansible/latest/modules/docker_container_module.html>`
module so that same requirements, parameters, and behavior are expected.

Topology Schema
~~~~~~~~~~~~~~

Within Linchpin, the :term:`docker_container` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`docker_container`
definition, the same options of the Ansible `docker_container` module are available. The :term: name :term: option is required.

See the `docker_container parameters <https://docs.ansible.com/ansible/latest/modules/docker_container_module.html#parameters>` for the complete list and defaults.

Additional Dependencies
-----------------------

The docker resource group requires the same dependencies of the Ansible docker_container module. See the `docker_container requirements <https://docs.ansible.com/ansible/latest/modules/docker_container_module.html#requirements>` documentation for the complete list of dependencies and any further detail.

