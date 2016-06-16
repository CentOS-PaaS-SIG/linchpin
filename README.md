# linch-pin
Linch-pin provides a collection of Ansible playbooks for provisioning , managing resources accross multiple infrastructures.
Where , multiple Infrastructure resource types can be defined with a single topology file.

## Directory Structure 
```
.
|-- bin # binaries needed 
|-- docs # documentation 
|-- ex_schemas # example Schema definitions
|   `-- os_server_roles.json
|-- ex_topo # example topologies
|   |-- ex_data_os_server.yml
|-- group_vars # variables applicable for groups
|   `-- all
|-- hosts # inventory hosts file
|-- inventory # dynamic inventory scripts
|-- library # custom modules library
|   `-- schema_check
|       `-- schema_check.py
|-- plugins # custom plugins
|-- README.md
|-- roles # roles handling resource specific provisioning
|   |-- aws
|   |   |-- handlers
|   |   |   `-- main.yml
|   |   |-- tasks
|   |   |   `-- main.yml
|   |   `-- templates
|   |-- common 
|   |   |-- handlers
|   |   |   `-- main.yml
|   |   |-- tasks
|   |   |   `-- main.yml
|   |   `-- templates
|   `-- openstack
|       |-- handlers
|       |   `-- main.yml
|       |-- tasks
|       |   |-- main.yml
|       |   `-- provision_resource_group.yml 
|       |   `-- provision_res_defs.yml
|       |-- templates
|       `-- vars #contains openstack credential files
|           |-- examplecreds.yml
|-- site.yml
`-- tests # tests cases
```

## Installation

### System Dependencies
Python 2.7.x  or higher
#### Centos
sudo yum install ansible  

#### Fedore 23 and above
sudo dnf install ansible 

git clone https://github.com/CentOS-PaaS-SIG/linch-pin
cd linch-pin/library
### append the linch-pin/library path to library variable in ansible.cfg 

## Example Topology file 
```
---
  topology_name: "example_topo" # topology name
  credentials: # list of credentials
    - "ex_os_creds" 
    - "ex_aws_creds" 
  resource_groups: 
    - 
      resource_group_name: "testgroup1"
      res_group_type: "openstack"
      res_defs: 
        - 
          res_name: "ha_inst" 
          flavor: "m1.small"
          res_type: "os_server"
          image: "rhel-6.5_jeos"
          count: 1
          keypair: "ex_keypair_os"
          networks:
            - "ex_network1"
        - 
          res_name: "web_inst"
          flavor: "m1.small"
          res_type: "os_server"
          image: "rhel-6.5_jeos"
          count: 2
          keypair: "ex_keypair_os"
          networks:
            - "ex_network2"
    - 
      resource_group_name: "testgroup2"
      res_group_type: "openstack"
      res_defs:
        - res_name: "test_inst"
          flavor: "m1.small"
          res_type: "os_server"
          image: "rhel-6.5_jeos"
          count: 1
          keypair: "ex_keypair_os"
          networks:
            - "ex_network3"
      assoc_creds: "ex_os_creds"
    - 
      resource_group_name: "testgroup3"
      res_group_type: "aws"
      res_defs:
        - 
          ex_prop: "m1.small"
          res_type: "aws_ec2"
          keypair: "ex_keypair_awsec2"
      assoc_creds: "ex_aws_creds"
  resource_group_vars:
    - 
      resource_group_name : "testgroup1"
      test_var1: "test_var1 msg is grp1 hello "
      test_var2: "test_var2 msg is grp1 hello "
      test_var3: "test_var3 msg is grp1 hello "
    -
      resource_group_name : "testgroup2"
      test_var1: "test_var1 msg is grp2 hello"
      test_var2: "test_var2 msg is grp2 hello"
      test_var3: "test_var3 msg is grp2 hello"
    -
      resource_group_name : "testgroup3"
      test_var1: "test_var1 msg is grp3 hello"
      test_var2: "test_var2 msg is grp3 hello"
      test_var3: "test_var3 msg is grp3 hello"

```

## Usage
### Provision a topology
```
command: ansible-playbook -vvv site.yml -e "{'data':'path_to_topolgy_file', 'schema':'path_to_schema_file', 'state':'present'}"

example: ansible-playbook -vvv site.yml -e "{'data':'ex_topo/ex_data.yml', 'schema':'ex_schemas/schema_v2.json', 'state':'present'}"
```

### De-Provision a topology
```
command: ansible-playbook -vvv site.yml -e "{'data':'path_to_topolgy_file', 'schema':'path_to_schema_file', 'state':'absent'}"
example: ansible-playbook -vvv site.yml -e "{'data':'ex_topo/ex_data.yml', 'schema':'ex_schemas/schema_v2.json', 'state':'absent'}"
```
