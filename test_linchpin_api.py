import json
import linchpin
from linchpin.api import Pinfile
from linchpin.api import Workspace

wksp = Workspace(path="/tmp/tmp3BAAhC/")
wksp.up()
wksp.destroy()

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
print(pinfile)
"""
#pf = Pinfile("/home/srallaba/workspace/lp_ws_backup/lp_ws/ex_hooks/testw/dummy")
wsp = Workspace(path="/home/srallaba/workspace/lp_ws_backup/lp_ws/ex_hooks/testw/dummy")
print(wsp.validate())
wsp.up()
#wsp.set_evar()
#wsp.set_cfg()
#wsp.get_cfg()
print(wsp.get_inventory())
wsp.destroy()
"""
"""
# workspace with credential management
wsp = Workspace(path="/home/srallaba/workspace/lp_ws_backup/lp_ws/ex_hooks/testw/dummy-creds-vault")
print(wsp.validate())
wsp.set_evar("default_credentials_path", "/home/srallaba/workspace/lp_ws_backup/lp_ws/ex_hooks/testw/dummy-creds-vault/credentials/")
wsp.set_evar("vault_password","testval")
wsp.up()
print(wsp.get_inventory())
"""


pf = Pinfile(pinfile=pinfile)
print(pf.validate())
#pf.up()
#pf.destroy()
