Layouts
=======

A layout file is the current mechanism to define mappings between the resources provisioned
out of the topology and the Ansible inventory groups that are output.

.. contents:: Topics

Structure
`````````

As with a topology file, a layout file is a YAML file or a JSON file with a single
root object hash. There is one top-level entry in the hash, named `inventory_layout`.
The `inventory_layout` value is itself an object that has a few fields inside of it.

Hosts
-----

The first hash value is `hosts`, which contains an object hash as a value. The keys of
that hash are the names of hosts that have been provisioned out of the topology. Each
host has two properties, `count` and `host_groups`.

The `count` property says how many of the topology hosts are to share this inventory
hostname. For instance, if the host is "webserver" and `count` is 2, then this will
generate hosts in the output inventory named "webserver-1" and "webserver-2". This
value is optional and defaults to 1 when it's not present.

The `host_groups` field contains an array of Ansible inventory groups into which all
the hosts under this hash will get placed. This value is optional and will default to
an empty list when not filled. In that case, the host will be named into the inventory
with its host vars, but it will not 

As an example, assume you provisioned three hosts and you wanted one database and
two applicaiton hosts. Your goal is to get to an Ansible inventory that looks like this::

    [backend]
    database

    [frontend]
    webhost-1
    webhost-2

    [ldap]
    database
    webhost-1
    webhost-2

    [security_updates]
    database

Then your hosts object would look like this::

    hosts:
      database:
        count: 1
        host_groups:
          - backend
          - ldap
          - security_updates
      webhost:
        count: 2
        host_groups:
          - ldap
