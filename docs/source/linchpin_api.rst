Linchpin API ( until 1.7.5 )
============================

LinchPin can be used to provision resources by invoking linchpin python API. 

Provisioning example using a Pinfile
------------------------------------

While provisioning with a Pinfile as a dictionary we have to set various config parameters and workspaces as follows.

.. code::

    from linchpin import LinchpinAPI
    from linchpin.context import LinchpinContext
 
    context = LinchpinContext()
    context.setup_logging()
    context.load_config()
    context.load_global_evars()
    context.set_cfg('lp', 'workspace', '.')
    context.set_evar('workspace', '.')
    context.set_evar('debug_mode', True)
    linchpin_api = LinchpinAPI(context)
    pindict = {
      "simple": {
        "layout": {
          "inventory_layout": {
            "hosts": {
              "example-node": {
                "count": 1,
                "host_groups": [
                  "example"
                ]
              }
            },
            "vars": {
              "hostname": "__IP__",
              "ansible_ssh_private_key_file": "~/.ssh/id_rsa"
            }
           }
        },
        "topology": {
           "topology_name": "simple",
          "resource_groups": [
            {
              "resource_group_name": "os-server-new",
              "resource_definitions": [
                {
                  "count": 1,
                  "name": "database",
                  "image": "CentOS-7-x86_64-GenericCloud-1612",
                  "keypair": "ci-factory",
                  "role": "os_server",
                  "fip_pool": "10.8.240.0",
                  "flavor": "m1.small",
                  "networks": [
                    "QE-test"
                  ]
                }
              ],
              "resource_group_type": "openstack",
              "credentials": {
                "filename": "clouds.yaml",
                "profile": "default"
              }
            }
          ]
        }
      }
    }

    # credentials alternatives: file vs environment variables
    linchpin_api.do_action(pindict, action='up')
    # inorder to destroy the pinfile we need to pass action parameter as destroy
    # linchpin_api.do_action(pindict, action='destroy')



Linchpin revised API (Preview in 1.7.6)
=======================================

In linchpin new api restructure linchpin provides two classes Pinfile, Workspace to provision resources

This feature is currently in Preview state for 1.7.6 will be available from version 2.0

Examples for provisioning using linchpin api Pinfile and workspace are as follows

.. code::

    import json
    import linchpin
    from linchpin.api import Pinfile
    from linchpin.api import Workspace
    
    # workspace requires workspace path
    wksp = Workspace(path="/tmp/tmp3BAAhC/")
    wksp.up()
    #prints the inventory generated after provisioning
    wksp.get_inventory(inv_format="json")
    wksp.destroy()

    # Provisioning with Pinfile structure

    pinfile="""
    dummy-test:
      topology:
        topology_name: "dummy_cluster" # topology name
        resource_groups:
        - resource_group_name: "dummy"
          resource_group_type: "dummy"
          resource_definitions:
          - name: "web"
            role: "dummy_node"
            count: 3
          - name: "test"
            role: "dummy_node"
            count: 1
      layout:
        inventory_layout:
          vars:
            hostname: __IP__
          hosts:
            example-node:
              count: 3
              host_groups:
              - example
            test-node:
              count: 1
              host_groups:
              - test
          host_groups:
            all:
              vars:
                ansible_user: root
    """
    import yaml
    pinfile = yaml.load(pinfile)
    pf = Pinfile(pinfile=pinfile)
    print(pf.validate())
    #pf.up()
    #pf.destroy()

  # workspace with external credential path
    wsp = Workspace(path="/home/srallaba/workspace/lp_ws_backup/lp_ws/ex_hooks/testw/dummy-creds-vault")
    print(wsp.validate())
    wsp.set_creds_path("/home/srallaba/workspace/lp_ws_backup/lp_ws/ex_hooks/testw/dummy-creds-vault/credentials/")
    wsp.set_evar("vault_password","testval")
    wsp.up()
    wsp.get_inventory()
    wsp.destroy()


.. note:: The both examples provided are backward compatible in nature. Introduction of new API does not change functionality the existing API

Refer the API reference section here :doc:`libbase` for more documentation on specific functions 
