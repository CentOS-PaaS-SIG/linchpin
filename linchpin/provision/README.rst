Provisioning
------------

To provide further provisioning beyond the core modules included in this directory. See https://github.com/herlo/linchpin-x (hopefully soon to be https://github.com/CentOS-PaaS-SIG/linchpin-x).

Essentially, the `linchpin-x` repository can be cloned here, or set as a sub-module, which will then provide provisioning for these additional providers.

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
