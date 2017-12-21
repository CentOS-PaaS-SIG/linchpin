Topology Incompatibilities
==========================

While writing the new API updates, some inconsistencies were discovered in
the beaker, and openshift topologies. These topologies did not contain the
:term:`resource_definitions` section. This inconsistency affected the way
the LinchPin API processed the schema, and in turn, validated the data to
be acted upon.

The purpose of the rewrite was to enable Dynamic inputs, and topology templating.
Part of which meant having a consistent, standardized topology. The
:term:`resource_definitions` section was being validated against the new `schema.json`
found in each provider's ``roles/files``.

The API was rewritten in such a way, that only dictionaries were passed to the
``do_action`` method. The linchpin shell and cli packages converted input from
YAML, JSON, Templating, and Scripts into the ``provision_data`` dictionary. Once
converted, validation happened, and the API called the appropriate ansible
playbook for the particular provider.

This enabled the linchpin API to call a playbook named for the `resource_group_type`
(eg. openstack), which contained the necessary items to provision using Ansible.

Because the openshift and beaker topologies didn't contain the needed section,
they were updated to the newer structure.

Updated Beaker Topology
-----------------------

.. code-block:: yaml

    ---
    topology_name: "bkr-new"
    resource_groups:
      - resource_group_name: "bkr-new"
        resource_group_type: beaker
        resource_definitions:
          - role: bkr_server
            whiteboard: Provisioned with linchpin
            job_group: ci-ops-central
            recipesets:
              - distro: RHEL-6.5
                arch: x86_64
                hostrequires:
                  - tag: processors
                    op: ">="
                    value: 4
                  - tag: device
                    op: "="
                    type: "network"
                count: 1
          - role: bkr_server
            whiteboard: Provisioned with linchpin
            job_group: ci-ops-central
            recipesets:
              - distro: RHEL-6.5
                arch: x86_64
                hostrequires:
                  - tag: processors
                    op: ">="
                    value: 1
                count: 1

.. note:: Due to the change, the beaker playbooks were improved. Previously, multiple
   data sets could not be submitted at the same time. However, with the new
   `resource_definitions` section in place, each set of resources was provisioned
   at the same time. The fetching of data was also looking for multiple job data,
   instead of one. This did not affect the recipesets functionality.

Updated Openshift Topology
--------------------------

.. code-block:: yaml

    ---
    topology_name: openshift
    resource_groups:
      - resource_group_name: test1
        resource_group_type: openshift
        resource_definitions:
          - name: openshift
            role: openshift_inline
            data:
              - apiVersion: v1
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
        credentials:
          api_endpoint: example.com:8443/
          api_token: mytokentextrighthere

