Docker
======

The docker provider manages ``docker_container`` and ``docker_image`` resources.

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

docker_image
------------

The ``docker_image`` resource provides the ability to manage a Docker image. It is implemented as a wrapper around the Ansible's `docker_image <https://docs.ansible.com/ansible/latest/modules/docker_image_module.html>` module so that same requirements, parameters, and behavior are expected.

Topology Schema
~~~~~~~~~~~~~~~

Within Linchpin, the :term:`docker_image` :term:`resource_definition` has more
options than what are shown in the examples above. For each :term:`docker_image`
definition, the same options of the Ansible `docker_image` module are available. The :term: name :term: option is required.

See the `docker_image parameters <https://docs.ansible.com/ansible/latest/modules/docker_image_module.html#parameters>` for the complete list and defaults.

.. note:: The provider assume that the ``cacert_path``, ``cert_path``, ``path``, and ``load_path`` parameter value are relative to the workspace path, unless its value is absolute (e.g. /path/to/cert) or relative (e.g. ./path/to/cert) to the OS filesystem.

Additional Dependencies
-----------------------

The docker resource group requires the same dependencies of the Ansible docker_container module. See the `docker_container requirements <https://docs.ansible.com/ansible/latest/modules/docker_container_module.html#requirements>` documentation for the complete list of dependencies and any further detail.

