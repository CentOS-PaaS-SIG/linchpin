Openstack-libvirt 
=================

This workspace contains set of hooks and Pinfile to provision and openstack instance

and run libvirt tests remotely using the remote hooks. 

In order to run these tests one has to be inside cloned linchpin repository and run 

./config/Dockerfiles/tests.d/openstack/10_openstack_libvirt

Further, you set the CREDS_PATH environment variable before running the script. 
