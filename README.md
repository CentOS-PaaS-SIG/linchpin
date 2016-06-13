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
|       |   `-- provision_os_server.yml
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
#append the linch-pin/library path to library variable in ansible.cfg 

## Example Topology file 
```
---
  topology_name: "example_topo" # topology name
  infra_type: "openstack" # type of infrastructure 
  site: "site_name" # site where the infra is provisioned
  credentials: # list of credentials
    - "ex_creds1"
    - "ex_creds2"
  resources: # list of resources of different resource types
    - 
      resource_name: "test_res" #name of the resource
      res_type: "os_server" # resource type Ex: os_server , aws_ec2 etc.,
      count: 2 # number of instances to be provisioned
      res_def:
        flavor: "m1.small" # flavor type 
        image: "rhel-6.5_jeos"
        keypair: "keypair_name" # the keypair to be used if its os_server type
        networks:
          - "ex_network_name" # network name 
        tags: # optional metadata 
          - "this"
          - "tags"
          - "attribute"
          - "is optional"
        assoc_creds:  "ex_creds1" # credentials associated with this resource creds needs to be declared in the respective roles/role_name/vars ex: roles/openstack/vars/ex_creds1.yml
    - 
      resource_name: "testvm_web"
      res_type: "os_server"
      count: 4
      res_def:
        flavor: "m1.small"
        count: 1
        image: "centos_image"
        keypair: "ex_keypair"
        networks:
          - "ex_network"
        tags:
          - "this"
          - "tags"
          - "attribute"
          - "is not required"
        assoc_creds:  "ex_creds2"
```

## Usage
### Provision a topology
```
command: ansible-playbook -vvv site.yml -e "{'data':'path_to_topolgy_file', 'schema':'path_to_schema_file', 'state':'present'}"

example: ansible-playbook -vvv site.yml -e "{'data':'ex_topo/ex_data_os_server.yml', 'schema':'ex_schemas/os_server_roles.json', 'state':'present'}"
```

### De-Provision a topology
```
command: ansible-playbook -vvv site.yml -e "{'data':'path_to_topolgy_file', 'schema':'path_to_schema_file', 'state':'present'}"
example: ansible-playbook -vvv site.yml -e "{'data':'ex_topo/ex_data_os_server.yml', 'schema':'ex_schemas/os_server_roles.json', 'state':'absent'}"
```


