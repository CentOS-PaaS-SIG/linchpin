Provisioning
------------

Following is a list of provisioners supported by LinchPin. Please read the section below to see any requirements.


Dummy
=====

Test provider. Creates a /tmp/dummy.hosts file with data from the provision.

Libvirt
=======

Provisions systems a local or remote image, creating a virtual machine on a system running libvirt. See https://libvirt.org/ for more detail on how libvirt works.

Reference::

* http://docs.ansible.com/ansible/latest/list_of_cloud_modules.html#misc

Openstack
=========

Provisions instances on an openstack server. Additionally supports security groups, objects, and volumes without teardown support. See https://openstack.org for more detail about how openstack works.

Reference::

* http://docs.ansible.com/ansible/latest/list_of_cloud_modules.html#openstack

Amazon Web Services (aws)
=========================

Provisions Elastic Compute Cloud (ec2) instances on amazon web services. Additionally supports security groups, and ssh_key management without teardown support. See https://aws.amazon.com/ for more detail on how AWS works.

Reference::

* http://docs.ansible.com/ansible/latest/list_of_cloud_modules.html#amazon

Google Cloud (gcloud)
=====================

Provisions instances in the Google Compute Engine (gce) on Google Cloud Platform. Additionally supports security groups, and ssh_key management without teardown support. See https://cloud.google.com/ for more detail on how gce works.

Reference::

* http://docs.ansible.com/ansible/latest/list_of_cloud_modules.html#amazon

Beaker
======

Provisions specific types of systems from an available catalog. See https://beaker-project.org/ for more detail about how Beaker works.

Reference::

* https://github.com/herlo/linchpin-x/blob/master/library/bkr_server.py
* https://github.com/herlo/linchpin-x/blob/master/library/bkr_info.py


Duffy
=====

Provisions preallocated CentOS 6 & 7 systems for Continuous Integration purposes.

Reference: https://wiki.centos.org/QaWiki/CI/Duffy

Requires: https://github.com/herlo/duffy-ansible-module added to the library path

Openshift
=========

Provisions containers from an Openshift endpoint. See https://docs.openshift.com/ for more detail about how Openshift works.

Reference: https://docs.ansible.com/ansible/2.4/oc_module.html

oVirt
=====

Provisions virtual machines using a web interface (or API) via the libvirtd daemon. See https://ovirt.org/ for more detail about how oVirt works.

Reference: http://docs.ansible.com/ansible/latest/list_of_cloud_modules.html#ovirt

Rackspace
=========

Rackspace is a specialized Openstack instance with commercial support. See https://www.rackspace.com/en-us/cloud for more detail about how Rackspace works.

Reference: http://docs.ansible.com/ansible/latest/list_of_cloud_modules.html#rackspace
