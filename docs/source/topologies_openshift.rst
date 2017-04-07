OpenShift Topologies
====================

.. contents:: Topics

.. _openshift_topologies:

Inventory Generation
--------------------

It is important to note that OpenShift resources do not follow the normal rules
of most other providers. When you provision a resource in OpenShift, there is
no easy way for Linchpin to introspect any information about the resources you
have spun up. Accessing individual containers and pods directly is a violation
of how most people expect OpenShift and container technologies in general to
operate. Therefore, no output will be given into the generated Ansible
inventory file for an OpenShift provisioning. OpenShift does not even expose a
method to address an individual container and create or destroy one. It only
exposes the pod level and above for creation, making entering into a particular
container impossible.

Additionally, it is possible to use Linchpin to spin up resources in OpenShift
that are not even containers, as any item other than an Event which may be
created through the API can be created through the OpenShift provider layer
in Linchpin. Thus, even if proper destination IP addresses could be
introspected from the results, there is no guarantee that what is being created
even has such a destination.

Accessing OpenShift Resources
-----------------------------

Furthermore, individual containers will typically not expose SSH access to the
process space. Such introspection of the containers needs to be done through
native OpenShift methods such as the command line client "oc" and its sub
commands like "exec" and "rsh". Information on how to access running pods and
containers can be found in the external documentation for OpenShift, along with
specific information from your cluster's administrator.

Note About Teardown
-------------------

Again, OpenShift shows its special nature in the teardown step of
infrastructure management. Most use cases, as is the case with the example
below, will create what is known as a "replication controller". This is an
object with the job of monitoring and maintaining multiple copies of a pod
running across the cluster. The replication controller provides a very simple
way to increase or decrease the quantity of running pods. If it detects that
ond of its pods has stopped for any reason, it will attempt to recreate the
pod again. This is good, as it gives a layer of automated infrastructure
monitoring to ensure the required number of copies are running across the
cluster.

However, this configuration creates a difficulty with teardown. If a topology
file creates a replication controller with more than 0 pods (the example below
creates a ReplicationController with 7 copies of the Jenkins slave pod running)
that RC will work to keep the pods up, but it will not teardown those pods when
the RC is deleted. Those pods will remain running until they are either killed
manually or until their base process crashes. Thus, running "linchpin rise"
followed by "linchpin drop" on this ReplicationController will leave seven
orphaned pods running in the cluster unless they are cleaned up manually.

One way to avoid this is to "scale down" the RC by setting its number of
active pods to 0 before deleting it. This will leave no orphaned pods behind.
Alternatively, the pods could be deleted manually after deletion of the RC.
Linchpin does not attempt to do the scaling automatically, as there are a vast
number of possible scenarios for leaving orphaned items behind in a cluster.
Pods are only referenced here as the most likely possibility, and are a clear
example of something that could be orphaned on a cluster.

Example Topologies
------------------

Each of these topologies has two places where authentication data will need to
be inserted. The first is the field named "api_endpoint". This needs to be,
minimally, the hostname and port serving the OpenShift cluster API. If the
API is behind an additional path element instead of living at the root of the
host, this portion can be continued on just as if this is part of a URL
fragment.

Secondly, the "api_token" field needs to filled in. This field is time
dependent for most users, so it might need to be regenerated on a regular
basis. This can be done by executing "oc whoami --token" after an "oc login"
command.

OpenShift Instance (Inline)
```````````````````````````

In this example, the data for a ReplicationController is inserted directly
into the topology file. The value under "inline_data" is exactly the same
as the data that would be passed into the "oc" command through a file.

.. code-block:: yaml

   ---
    topology_name: openshift
    resource_groups:
      - resource_group_name: test1
        res_group_type: openshift
        api_endpoint: example.com:8443
        api_token: someapitoken
        resources:
          - inline_data:
              apiVersion: v1
              kind: ReplicationController
              metadata:
                name: jenkins-slave
                namespace: central-ci-test-ghelling
              spec:
                replicas: 7
                selector:
                  name: jenkins-slave
                template:
                  metadata:
                    labels:
                      name: jenkins-slave
                  spec:
                    containers:
                      - image: redhatqecinch/jenkins_slave:latest
                        name: jenkins-slave
                        env:
                          - name: JENKINS_MASTER_URL
                            value: http://10.8.172.6/
                          - name: JSLAVE_NAME
                            value: mynode
                    restartPolicy: Always
                    securityPolicy:
                      runAsUser: 1000090000

OpenShift Instance (external)
`````````````````````````````

In this example, the data is not placed into the topology file but a reference
to an external yaml file is provided. That file will be read in by Linchpin
and uploaded to the OpenShift cluster just as if it had been passed into the
"oc" client.

.. code-block:: yaml

   ---
    topology_name: openshift_external
    resource_groups:
      - resource_group_name: test-external
        res_group_type: openshift
        api_endpoint: example.com:8443
        api_token: someapitoken
        resources:
          - file_reference: /home/user/openshift/external/resource/file.yaml
          - file_reference: /home/user/openshift/external/resource/cluster.yaml
