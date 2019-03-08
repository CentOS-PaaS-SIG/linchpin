Environment Variables
`````````````````````

LinchPin honors the OpenStack environment variables such as ``$OS_USERNAME``,
``$OS_PROJECT_NAME``, etc.

See `the OpenStack documentation cli documentation 
<https://docs.openstack.org/python-openstackclient/pike/cli/man/openstack.html#manpage>`_
for details.

.. note:: No credentials files are needed for this method. When LinchPin calls
   the OpenStack provider, the environment variables are automatically picked
   up by the OpenStack Ansible modules, and passed to OpenStack for
   authentication.

Using OpenStack Credentials
```````````````````````````

OpenStack provides a simple file structure using a file called
`clouds.yaml <https://docs.openstack.org/os-client-config/latest/user/configuration.html>`_,
to provide authentication to a particular tenant. A single clouds.yaml file might contain several entries.

.. code-block:: yaml

    clouds:
      devstack:
        auth:
          auth_url: http://192.168.122.10:35357/
          project_name: demo
          username: demo
          password: 0penstack
        region_name: RegionOne
      trystack:
        auth:
          auth_url: http://auth.trystack.com:8080/
          project_name: trystack
          username: herlo-trystack-3855e889
          password: thepasswordissecrte

Using this mechanism requires that credentials data be passed into LinchPin.

An OpenStack topology can have a ``credentials`` section for each
:term:`resource_group`, which requires the filename, and the profile name.

It's worth noting that we can't give you credentials to use, so you'll have to provide
your own filename and profile here.  By default, LinchPin searches for the filename in
{{ workspace}}/credentials but can be made to search other places by setting the
:code:`evars.default_credentials_path` variable in your linchpin.conf.  The credentials
path can also be overridden by using the :code:`--creds-path` flag.

.. code-block:: yaml

    ---
    topology_name: topo
    resource_groups:
      - resource_group_name: openstack
        resource_group_type: openstack
        resource_definitions:

          .. snip ..

        credentials:
          filename: clouds.yaml
          profile: devstack

