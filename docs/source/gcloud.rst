Google Cloud Platform
=====================

The Google Cloud Platform (gcloud) provider manages one resource, ``gcloud_gce``.

gcloud_gce
----------

Google Compute Engine (gce) instances are provisioned using this resource.

* :docs1.5:`Topology Example <workspaces/topologies/gce-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/gce_module.html>`_

gcloud_gce_eip
--------------

Google Compute enginer external IP (gce_eip) are provisioned using this resource.

* :docs1.5:`Topology Example <workspaces/topologies/gce-eip.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/gce_eip_module.html>`

gcloud_gce_net
--------------

Google compute engine network (gce_net) are provisioned using this resource.

* :docs1.5:`Topology Example <workspaces/topologies/gce-net.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/gce_net_module.html>`

gcloud_gcdns_zone
-----------------

Google DNS zone (gcdns_zone) are provisioned using this resource.

* :docs1.5:`Topology Example <workspaces/topologies/gcdns-zone.yml>`
* `Ansible module <https://docs.ansible.com/ansible/latest/modules/gcdns_zone_module.html>`

gcloud_gcdns_record
-------------------

Google DNS zone records (gcdns_record) are provisioned using this resource.

* :docs1.5:`Topology Example <workspaces/topologies/gcdns-record.yml>`
* `Ansible module <https://docs.ansible.com/ansible/latest/modules/gcdns_record_module.html>`

gcloud_gcp_compute_network
--------------------------

Google cloud compute networks are provisioned using this resource.

* :docs1.5:`Topology Example <workspaces/topologies/gcp-compute-network.yml>`
* `Ansible module <https://docs.ansible.com/ansible/latest/modules/gcp_compute_network_module.html>`

gcloud_gcp_compute_router
-------------------------

Google cloud compute routers are provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/gcp-compute-router.yml>`
* `Ansible module <https://docs.ansible.com/ansible/latest/modules/gcp_compute_router_module.html>`

Additional Dependencies
-----------------------

No additional dependencies are required for the Google Cloud (gcloud) Provider.

Credentials Management
----------------------

Google Compute Engine provides several ways to provide credentials. LinchPin supports
some of these methods for passing credentials for use with openstack resources.

Environment Variables
`````````````````````

LinchPin honors the gcloud environment variables.

Configuration Files
```````````````````

Google Cloud Platform provides tooling for authentication. See
https://cloud.google.com/appengine/docs/standard/python/oauth/ for options.
