Openshift
=========

The openshift provider manages two resources, ``openshift_inline``, and ``openshift_external``.
However, both of the resource types are managed by module k8s Ansible module. Usage of either one
will result in redirection to k8s module with different parameters.

Prior to linchpin 1.6.5,
The Ansible module for openshift is written and bundled as part of LinchPin.
* :code1.5:`openshift.py <linchpin/provision/library/openshift.py>`

After 1.6.5 bundled ansible module is being replaced by upstream ansible kubernetes module.
Refer: `K8s module <https://docs.ansible.com/ansible/2.6/modules/k8s_module.html>`_.
Linchpin supports all the attributes mentioned in k8s module.

openshift_inline 
----------------
Openshift instances can be provisioned using this resource. Resources are
detail inline.
* :docs1.5:`Topology Example <workspace/topologies/openshift-new.yml>`

Example PinFile:
````````````````

.. code-block:: yaml
  openshift-new:
    topology:
      topology_name: openshift
      resource_groups:
        - resource_group_name: test1
          resource_group_type: openshift
          resource_definitions:
            - name: hellopod
              role: openshift_inline
              namespace: continuous-infra # pre provisioned namespace
              definition:
                kind: Pod
                apiVersion: v1
                metadata:
                  name: hello-openshift
                  labels:
                    name: hello-openshift
                spec:
                  containers:
                  - name: hello-openshift
                    image: openshift/hello-openshift
                    ports:
                    - containerPort: 8080
                      protocol: TCP
                    resources: {}
                    volumeMounts:
                    - name: tmp
                      mountPath: /tmp
                    terminationMessagePath: /dev/termination-log
                    imagePullPolicy: IfNotPresent
                    capabilities: {}
                    securityContext:
                      capabilities: {}
                      privileged: false
                  volumes:
                  - name: tmp
                    emptyDir: {}
                  restartPolicy: Always
                  dnsPolicy: ClusterFirst
                  serviceAccount: ''
                  status: {}

 
openshift_external 
------------------

Openshift instances can be provisioned using this resource. Resources are
 detail in an external file.

Example PinFile:

.. code-block:: yaml
  openshift-new:
    topology:
      topology_name: openshift
      resource_groups:
        - resource_group_name: test1
          resource_group_type: openshift
          resource_definitions:
            - name: testing  # creates namespaces
              role: openshift
              kind: Namespace
            - name: anotesting
              role: openshift
              kind: Namespace
            - name: hellopod
              role: openshift
              namespace: continuous-infra
              src: /abosolute_path/to/templatefile
          credentials:
            filename: open  # fetched from --creds-path is provided
            profile: default
 
Topology Schema:
----------------

openshift_inline and opeshift_external resource definitions in linchpin
follow the schema identical to ansible k8s module. 
The following parameters are allowed in a linchpin topology:

+------------------+------------+----------+-------------------+----------------------------------------------------+
| Parameter        | required   | type     | ansible value     | comments                                           |
+==================+============+==========+===================+====================================================+
| name             | true       | string   | name              |                                                    |
+------------------+------------+----------+-------------------+----------------------------------------------------+
| namespace        | true       | string   | namespace         |                                                    |
+------------------+------------+----------+-------------------+----------------------------------------------------+
| definition       | false      | string   | deinition         | not needed when src is used                        |
+------------------+------------+----------+-------------------+----------------------------------------------------+
| src              | false      | string   | src               | exclusive with defintion attribute                 |
+------------------+------------+----------+-------------------+----------------------------------------------------+
| kind             | false      | string   | kind              | needed when definition/src atrribute are mentioned |
+------------------+------------+----------+-------------------+----------------------------------------------------+
| force            | false      | boolean  | force             | Recreates resources when force is true             |                                      |
+------------------+------------+----------+-------------------+----------------------------------------------------+

Additional Dependencies
-----------------------

There are no known additional dependencies for using the openshift provider
for LinchPin. Since openshift client dependecy is included as part of linchpin's
core requirements.

 
Credentials Management
----------------------

An openshift topology can have a ``credentials`` section for each
:term:`resource_group`, which requires the `api_endpoint`, and the `api_token`
values.
Openshift honors --creds-path in linchpin. The credential file
passed needs to be formatted as follows.
Further, it also honors all the evironment variables that are supported by 
ansible k8s module.
Refer: `K8s module <https://docs.ansible.com/ansible/2.6/modules/k8s_module.html>`_.
Linchpin defaults to environment variables if the credentials section is ommited 
or the --creds-path does not contain the openshift credential file.

.. code-block:: yaml

  ---
  default:
    api_endpoint: https://192.168.42.115:8443
    api_token: 4_6A86rcZqdVBIbPwJQnsz33mO35O_PnSH2okk8_190
  # optional parameters
  # api_version: v1  # defaults to version 1 
  # cert_file: /path/to/cert_file
  # context: contextname 
  # key_file: /path/to/key_file
  # kube_config: /path/to/kube_config
  # ssl_ca_cert: /path/to/ssl_ca_cert
  # username: username # not needed when api_token is used
  # password: ******** # not needed when api_token is used
  # verify_ssl: no #defaults to no. Needs to be set to yes when ssl_ca_cert is used

  test:
    api_endpoint: https://192.168.42.115:8443
    api_token: 4_6A86rcZqdVBIbPwJQnsz33mO35O_PnSH2okk8_190

.. code-block:: yaml

    ---
    topology_name: topo
    resource_groups:
      - resource_group_name: openshift
        resource_group_type: openshift
        resource_definitions:
          - name: openshift
            role: openshift_inline
            definition:

          .. snip ..

        credentials:
          filename: name_of_credsfile.yaml  # fetched from --creds-path is provided
          profile: name_of_profile # defaults to 'default' profile in cred_file
  
Tid bits :
----------

How to get to know API_ENDPOINT and API_TOKEN:
`````````````````````````````````````````````

Once the openshift cluster is up and running try logging into openshift using the following command

.. code-block:: bash

   oc login

After login run following command to get the API_ENDPOINT: 

.. code-block:: bash

   oc version | grep Server | awk '{print $2}'

Run the following command to get API_TOKEN

.. code-block:: bash

   oc whomai -t

Make sure your openshift user has permissions to create resources: 
``````````````````````````````````````````````````````````````````

Openshift by default imposes many restrictions on users when it comes to 
creation . One can always manage roles to get appropriate roles. 
if its just a development environment please use following command to give
admin user privileges to user
.. code-block::
   oc adm policy add-cluster-role-to-user cluster-admin <username> --as=system:admin
       
Refer: `Openshift role management <https://docs.openshift.com/container-platform/3.3/admin_solutions/user_role_mgmt.html>`_.
