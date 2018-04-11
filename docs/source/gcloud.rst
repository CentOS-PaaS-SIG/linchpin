Google Cloud Platform
=====================

The Google Cloud Platform (gcloud) provider manages one resource, ``gcloud_gce``.

gcloud_gce
----------

Google Compute Engine (gce) instances are provisioned using this resource.

* :docs1.5:`Topology Example <workspace/topologies/gce-new.yml>`
* `Ansible module <http://docs.ansible.com/ansible/latest/gce_module.html>`_

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

