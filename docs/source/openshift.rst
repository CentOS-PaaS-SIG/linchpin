Openshift
=========

The openshift provider manages two resources, ``openshift_inline``, and ``openshift_external``.

openshift_inline
----------------

Openshift instances can be provisioned using this resource. Resources are
detail inline.

* :docs1.5:`Topology Example <workspace/topologies/openshift-new.yml>`

The ansible module for openshift is written and bundled as part of LinchPin.

* :code1.5:`openshift.py <linchpin/provision/library/openshift.py>`

.. note:: The `oc <https://docs.ansible.com/ansible/2.4/oc_module.html`_ module
   was included into ansible after the above openshift module was created and
   included with LinchPin. The future may see the oc module used.

openshift_external
------------------

Openshift instances can be provisioned using this resource. Resources are
detail in an external file.

Additional Dependencies
-----------------------

There are no known additional dependencies for using the openshift provider
for LinchPin.

Credentials Management
----------------------

An openshift topology can have a ``credentials`` section for each
:term:`resource_group`, which requires the `api_endpoint`, and the `api_token`
values.
Further, Openshift also honours --creds-path in linchpin. The credential file
passed needs to be formatted as follows

.. code-block:: yaml

   ---
   testprofile:
       api_endpoint: example.com:8443/
       api_token: mytokentextrighthere
   default:
       api_endpoint: testexample.com:8443/
       api_token: someothertoken


.. code-block:: yaml

    ---
    topology_name: topo
    resource_groups:
      - resource_group_name: openshift
        resource_group_type: openshift
        resource_definitions:
          - name: openshift
            role: openshift_inline
            data:

          .. snip ..

        credentials:
          api_endpoint: example.com:8443/
          api_token: mytokentextrighthere
          # filename: name_of_credsfile.yaml  --> when --creds-path is provided
          # profile: name_of_profile --> defaults to 'default' profile in cred_file
