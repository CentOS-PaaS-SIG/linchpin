# Openstack simple single instance deployment

Deployment of a single instance in Openstack with minimal set of settings.
The example is [configurable] using the following arguments:

 - `os_simple_name` - instance name, default is 'database'
 - `os_simple_flavor` - [Openstack flavor], default is 'm1.small'
 - `os_simple_image` - [Openstak image], default is CentOS image
 - `os_simple_keypair` - [Key-pair in Openstack] to put into instance
 - `os_simple_fip_pool` - [Openstack floating IP pool] to get public IP from
 - `os_simple_networks` - Openstack network to get private IP from
 - `os_simple_keypath` - Path to private key on local system

To run with different configuration, you add `--template-data` option with path
to file or inline, for example:

    linchpin --template-data '{ "os_simple_name": "my_system" }' up

From file:

    linchpin --template-data '@settings.json' up

Short version:

    linchpin -d '@settings.json' up

[configurable]: https://linchpin.readthedocs.io/en/latest/managing_resources.html
[Openstack flavor]: https://docs.openstack.org/nova/rocky/user/flavors.html
[Openstage image]: https://docs.openstack.org/ocata/admin-guide/compute-images-instances.html
[Key-pair in Openstack]: https://docs.openstack.org/horizon/latest/user/configure-access-and-security-for-instances.html
[Openstack floating IP pool]: https://docs.openstack.org/ocata/user-guide/cli-manage-ip-addresses.html
