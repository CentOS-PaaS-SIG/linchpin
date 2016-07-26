# linch-pin
Linch-pin provides a collection of Ansible playbooks for provisioning and managing resources across multiple infrastructures.
Where multiple Infrastructure resource types can be defined with a single topology file.

## Directory Structure
```
.
|-- bin # binaries needed
|-- docs # documentation
|-- ex_schemas # example Schema definitions
|-- ex_topo # example topologies
|-- group_vars # variables applicable for groups
|-- hosts # inventory hosts file
|-- inventory # dynamic inventory scripts
|-- library # custom modules library
|-- plugins # custom plugins
|-- README.md
|-- roles # roles handling resource specific provisioning
|-- site.yml # top level Ansible playbook
`-- tests # tests cases
```

## Installation

### System Dependencies
Python 2.7.x  or higher

#### Centos
```
sudo yum install python-setuptools
sudo pip install ansible
```

#### Fedora 23 and above
```
sudo dnf install python-setuptools
sudo pip install ansible
git clone https://github.com/CentOS-PaaS-SIG/linch-pin
```

# Example Credential file formats:
Each Infra type should be maintaining a credential file in yaml format inside their respective vars folder,
which will be referred by the topology file.

Example formats of the credential files are as follows:
### Openstack credential file format: 
#### path: roles/openstack/vars/ex_os_creds.yml
```
--- # openstack credentials example
endpoint: http://example.com:5000/v2.0/
project: example
username: example
password: example
```
### AWS credential file format:
#### path: roles/aws/vars/ex_aws_creds.yml
```
--- # AWS credentials example
aws_access_key_id: XXXXXXXXXXXXXXXXXXXXXX
aws_secret_access_key: XXXXXXXXXXXXXXXXXXXXXX
```
### GCE credential file format:
#### path: roles/openstack/vars/ex_gce_creds.yml
```
--- # gcloud credentials example
service_account_email: "XXXXXXXXXXXXXXX.iam.gserviceaccount.com" 
project_id: "XXXXXXXXXXXXXX" 
credentials_file: "absolute_path_to_json_file"
```
### Note:
For GCE the absolute path of the service account json file should be provided

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
            res_name: "ha_inst3"
            flavor: "t2.micro"
            res_type: "aws_ec2"
            region: "us-east-1"
            image: "ami-fce3c696"
            count: 2
            keypair: "ex_keypair_name"
        assoc_creds: "ex_aws_creds"
    - 
        resource_group_name: "testgroup4"
        res_group_type: "gcloud"
        res_defs:
          - 
            res_name: "testvmgce"  # note gce resource names should not contain '_' characters 
            flavor: "n1-standard-1"
            res_type: "gcloud_gce"
            region: "us-central1-a"
            image: "debian-7"
            count: 2
        assoc_creds: "ex_gcloud_creds" 
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
    -
      resource_group_name : "testgroup4"
      test_var1: "test_var1 msg is grp4 hello"
      test_var2: "test_var2 msg is grp4 hello"
      test_var3: "test_var3 msg is grp4 hello"

```
## Usage
### Provision a topology
```
command: ansible-playbook -vvv site.yml -e "{'data':'path_to_topology_file', 'schema':'path_to_schema_file', 'state':'present', 'topology_output_file':'path_to_output_file'}"

example: ansible-playbook -vvv site.yml -e "{'data':'ex_topo/ex_data.yml', 'schema':'ex_schemas/schema_v2.json', 'state':'present', 'topology_output_file':'/tmp/ex_data_output.yaml'}"
```

### De-Provision a topology
```
command: ansible-playbook -vvv site.yml -e "{'data':'path_to_topolgy_file', 'schema':'path_to_schema_file', 'state':'absent', 'topology_output_file':'path_to_output_file'}"
example: ansible-playbook -vvv site.yml -e "{'data':'ex_topo/ex_data.yml', 'schema':'ex_schemas/schema_v2.json', 'state':'absent', 'topology_output_file':'/tmp/ex_data_output.yaml'}"
```
```
note: In both Provision/Deprovision commands the topology_output_file should be specified.
```
