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

