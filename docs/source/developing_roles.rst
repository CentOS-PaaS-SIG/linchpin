Developing Your Own LinchPin Roles
==================================

LinchPin currently supports a large number of providers, but we cannot guarantee that we can support all of them.  Often, a team or organization requesting the role can provide a better test infrastructure than the LinchPin team.  Because of this, LinchPin supports pulling roles from Ansible Galaxy.

Getting Started
----------------
LinchPin uses `molecule`_ to test roles.  The testing infrastructure is based on Red Hat's Open Ansible Systems Integration Solutions (OASIS) guidelines.  To initialize an OASIS role, first clone the OASIS roles meta skeleton. Then initialize the role using ansible galaxy

.. code-block:: bash

    $ git clone git@github.com:oasis-roles/meta_skeleton.git
    $ ansible-galaxy init --role-skeleton=meta_skeleton $YOUR_ROLE_NAME

You can also initialize the role with molecule

.. code-block:: bash

    $ git clone git@github.com:oasis-roles/meta_skeleton.git
    $ molecule init role --role-name $YOUR_ROLE_NAME --template meta_skeleton

Where do the roles go?
``````````````````````
Push your role to GitHub.  Then import it into Ansible Galaxy.  The role will be called `<your github username>.<github repo name>`.

Inputs
------
LinchPin passes a few variables to a role, which are described in more detail below

state
`````
The `state` variable should be either `present` or `absent`, corresponding with `linchpin up` or `linchpin destroy`.

resources
`````````
The `resources` variable corresponds with a single `resource group`_ in a PinFile.


Schema
-------
The first file required for use with linchpin is a `schema.json`.  The schema validates each resource definition.  LinchPin uses `cerberus`_ for validation.  This is an example of a schema:

.. code-block:: json

    {
        "res_defs": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                   "role": {
                       "type": "string",
                       "required": true,
                       "allowed": ["dummy_node"]
                   },
                   "name": { "type": "string", "required": true },
                   "domain": { "type": "string", "required": false },
                   "count": { "type": "integer", "required": false }
                }
            }
        }   
    }


This resource definition would be valid under the schema:

.. code-block:: yaml

    - name: "master-node"
      role: "dummy_node"
      count: 3


The following one, however, would not.  Notice how "count" is a string here.  To learn more about cerberus, visit the link above.

.. code-block:: yaml

    - name: "master-node"
      role: "dummy_node"
      count: "3"

Inventory
----------
The second file required by linchpin is an `inventory.py`.  This file allows LinchPin to generate inventories such as the one below.  To read more about inventories, visit the page on :ref:`layouts <inv_layouts>`.

In order to pass data from your role to LinchPin for inventory generation, first register the data returned by your provisioning task.  Then append that to the `topology outputs` variable.  `topology outputs` is a variable that linchpin uses to collect data from each resource definition.  The registered output must also be appended with two variables:  The resource group name and the role.  This helps LinchPin determine how to generate the inventory.  LinchPin has a filter called `add_res_data()` to make this step easy.  Below is an example from LinchPin's AWS role in which the data is collected from the provisioning task and assigned to `topology_outputs`.

.. code-block:: yaml

    - name: "Provisioning AWS_EC2 Resource"
      ec2:
        aws_access_key: "{{ auth_var['aws_access_key_id'] }}"
        aws_secret_key: "{{  auth_var['aws_secret_access_key'] }}"
        key_name: "{{ res_def['keypair'] }}"
        instance_type: "{{ res_def['flavor'] }}"
        image: "{{ res_def['image'] }}"
        region: "{{ res_def['region'] }}"
        wait: yes
        wait_timeout: "{{ res_def['wait_timeout'] }}"
        group: "{{ res_def['security_group'] }}"
        count: "{{ res_def['count'] }}"
        vpc_subnet_id: "{{ res_def['vpc_subnet_id'] }}"
        assign_public_ip: "{{ res_def['assign_public_ip'] }}"
        instance_tags: "{{ instance_tags }}"
     register: res_def_output

    - name: "Add type to resource"
      set_fact:
      topology_outputs: "{{ topology_outputs }} + {{ res_def_output | add_res_data(lookup('vars', 'role_name'), res_def['role']) }}"


.. note:: Be sure to APPEND the data! If you simply assign the output to `topology_outputs`,
          you will overwrite the results of all previous resource definitions.
:


The inventory script should contain a class called `Inventory` that inherits from LinchPin's `InventoryFilter` class.  Children of this class must contain a method called `get_host_data()` that takes two arguments: the provisioned resources and the :ref:`configs <pinfile_cfgs>`.  It returns a dict whose keys are hostnames for the provisioned resources and whose values are a dict of key/value pairs representing data described in the `cfgs` and `layout`.  Below is an example `get_host_data()` method, also from LinchPin's built-in AWS role

.. code:: python

        def get_host_data(self, res, cfgs):
            """
            Returns a dict of hostnames or IP addresses for use in an Ansible
            inventory file, based on available data. Only a single hostname or IP
            address will be returned per instance, so as to avoid duplicate runs of
            Ansible on the same host via the generated inventory file.
            Each hostname contains mappings of any variable that was defined in the
            cfgs section of the PinFile (e.g. __IP__) to the value in the field that
            corresponds with that variable in the cfgs.
            If an instance has a public IP attached, its hostname in DNS will be
            returned if available, and if not the public IP address will be used.
            For instances which have a private IP address for VPC use cases, the
            private IP address will be returned since private EC2 hostnames (e.g.
            ip-10-0-0-1.ec2.internal) will not typically be resolvable outside of
            AWS. For instances with both a public and private IP address, the
            public address is always returned instead of the private address.
            :param topo:
                linchpin AWS EC2 resource data
            :param cfgs:
                map of config options from PinFile
            """
    
            host_data = OrderedDict()
            if res['resource_group'] != 'aws' or res['role'] != 'aws_ec2':
                return host_data
            var_data = cfgs.get('aws', {})
            if var_data is None:
                var_data = {}
            for instance in res['instances']:
                host = self.get_hostname(instance, var_data,
                                         self.DEFAULT_HOSTNAMES)
                hostname_var = host[0]
                hostname = host[1]
                if '__IP__' not in list(var_data.keys()):
                    var_data['__IP__'] = hostname_var
                host_data[hostname] = {}
                self.set_config_values(host_data[hostname], instance, var_data)
            return host_data

There are a few functions and variables here which may not be familiar.  The first is the `get_hostname()` method.  Hosts in LinchPin inventories list a hostname and all of the corresponding variables.  To determine the hostname, the `get_hostname()` method takes the data for the instance, the cfgs data, and a list of default hostname variables.  For AWS, these variables are: `['public_dns_name', 'public_ip', 'private_ip']`.  If `__IP__` is not listed in `cfgs`, LinchPin will search for each of the default hostnames.  When one is encountered, it returns a tuple with the hostname variable and the hostname itself.

The second function which may not be familiar is the `set_config_values()` function.  This function takes the dict corresponding with a given host (generally empty at this point), the provisioning data for that host, and the variable data for the resource group (from `cfgs`) an populates the dict with the corresponding values.


Testing
-------
LinchPin's built-in roles take advantage of the `molecule`_ test framework, and we recommend that you do the same.  These are the tests which we run on our roles

yamllint
````````
yamllint is a linter to check syntax and do basic style enforcement.

ansible-lint
````````````
Ansible-lint 

testinfra
`````````
Testinfra is a testing framework used to verify the state of your servers after provisioning.

.. code:: bash

    Code example should probably go here





.. _molecule: https://molecule.readthedocs.io/en/stable/
.. _cerberus: https://docs.python-cerberus.org/en/stable/
.. _configs: :ref:`pinfile_cfgs`
