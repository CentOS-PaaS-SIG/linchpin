Linchpin Hooks: Examples
========================


Following document has most common examples of linchpin hooks

Example1: Running ansible based hooks on Openstack based instances

- Refer: `Workspace <https://github.com/samvarankashyap/linchpin_hooks_openstack_ws>`


- Pinfile:

::

  ---
  os-server-addl-vols:
    topology:
      topology_name: os-server-inst
      resource_groups:
        - resource_group_name: os-server-addl-vols
          resource_group_type: openstack
          resource_definitions:
          - name: "database"
            role: os_server
            flavor: m1.small
            image: CentOS-7-x86_64-GenericCloud-1612
            count: 1
            keypair: testkeypair_sk
            fip_pool: 10.8.240.0
            networks:
            - e2e-openstack
          credentials:
            filename: clouds.yaml
            profile: ci-rhos
    layout:
      inventory_layout:
        vars:
          hostname: __IP__
        hosts:
          addl-vols-node:
            count: 1
            host_groups:
              - hello
    hooks:
      postup:
          actions:
          - name: osoos
            type: ansible
            context: True
            actions:
          - playbook: install_packages.yaml
            extra_vars:
              ansible_ssh_private_key_file: "testkeypair_sk.key"
              ansible_ssh_user: centos
          - playbook: git_clone.yaml
            extra_vars:
              ansible_ssh_private_key_file: "testkeypair_sk.key"
              ansible_ssh_user: centos


Example: Running Global hook ping, check_ssh, port_up on Openstack based resources

::

  ---
  os-server-addl-vols:
    topology:
      topology_name: os-server-inst
      resource_groups:
      - resource_group_name: os-server-addl-vols
        resource_group_type: openstack
        resource_definitions:
          - name: "database"
            role: os_server
            flavor: m1.small
            image: CentOS-7-x86_64-GenericCloud-1612
            count: 1
            keypair: test_keypairsk2
            fip_pool: 10.8.240.0
            networks:
              - e2e-openstack
        credentials:
          filename: clouds.yaml
          profile: ci-rhos
    layout:
      inventory_layout:
        vars:
          hostname: __IP__
        hosts:
          addl-vols-node:
            count: 1
            host_groups:
            - hello
    hooks:
      postup:
        # check_ssh, ping and port_up are builtin hooks
        # note builtin hooks follow different structure when compared to localhooks
        - name: check_ssh
          extra_vars:
            # since checking ssh depends on logging into machine pem file, ssh_user are must
            ansible_ssh_private_key_file:  /home/srallaba/.ssh/test_keypairsk2.key
            ansible_ssh_user: centos
            ansible_ssh_common_args: "'-o StrictHostKeyChecking=no'"
            ansible_python_interpreter: "/usr/bin/python"
        - name: ping


Example3: Running python based hook on dummy workspace

* Workspace tree:
  
  ::

  .
  ├── credentials
  ├── hooks
  │   └── python
  │       └── test_python
  │           └── test.py
  ├── inventories
  ├── layouts
  │   └── dummy-layout.yml
  ├── linchpin.conf
  ├── PinFile
  ├── resources
  └── topologies


* Pinfile:

  ::

  ---
  dummy_target:
    topology:
      topology_name: "dummy"
      resource_groups:
      - resource_group_name: "dummy"
        resource_group_type: "dummy"
        resource_definitions:
        - role: "dummy_node"
          name: "web"
          count: 1
    layout:
      inventory_layout:
        vars:
          hostname: __IP__
        hosts:
          example-node:
            count: 1
            host_groups:
              - example
    hooks:
      preup:
        - name: test_python
          type: python
          context: False
          actions:
          - test.py hello hi  # hello hi will be command line parameters parameters passed to script test.py
