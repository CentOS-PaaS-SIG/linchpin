# linch-pin
Linch-pin provides a collection of Ansible playbooks for provisioning and
managing resources across multiple infrastructures. Where multiple
infrastructure resource types can be defined with a single topology file.

Linch-pin can also generate inventory files for use with additional ansible
playbooks. These are applied using an inventory layout file (work in progress).

## Directory Structure
```
.
├── provision # provisioning of infrastructures occurs here
│   ├── roles # ansible roles used to perform provisioning
│   ├── filter_plugins # inventory layout filter plugins
│   ├── site.yml # default provisioning playbook
│   └── invfilter.yml # playbook for tooling inventory filters
├── configure # additional configurations for jenkins jobs and the like
│   └── site.yml # configuration playbook
├── docs # documentation
├── README.md # this file
├── ex_schemas # example schemas (includes default schema: schema_v2.json)
├── ex_topo # example topologies and related components
├── keystore # location of ssh keys, etc to provide to provisioned systems
├── credential_store # location of cloud credentials
├── library # ansible modules for linch-pin (written in python)
├── inventory # default location of inventories provided by linch-pin
└── outputs # default location of outputs
```

## Installation

### System Dependencies
Python 2.7.x  or higher
Ansible 2.1.x or higher
Python virtualenv is highly recommended

#### CentOS 7

```
sudo yum install python-setuptools
sudo yum install python-virtualenv
sudo yum install python-virtualenvwrapper
source /usr/bin/virtualenvwrapper.sh
mkvirtualenv linchpin-test
pip install --upgrade ansible>=2.1.0
pip install jsonschema functools32
git clone https://github.com/CentOS-PaaS-SIG/linch-pin
```

#### Fedora 23 and above
```
sudo dnf install python-setuptools
sudo dnf install python-virtualenv
sudo dnf install python-virtualenvwrapper
sudo dnf install ansible
source /usr/bin/virtualenvwrapper.sh
mkvirtualenv linchpin-test
pip install jsonschema functools32
git clone https://github.com/CentOS-PaaS-SIG/linch-pin
```

# Example Credential file formats:
Each Infra type should be maintaining a credential file in yaml format inside their respective credential_store folder,
which will be referred by the topology file.

Example formats of the credential files are as follows:
### Openstack credential file format:
#### path: credential_store/openstack/ex_os_creds.yml
Openstack credentials follow clouds.yaml syntax.
```
--- # openstack credentials example
clouds:
  devstack:
    auth:
      auth_url: http://192.168.122.10:35357/
      project_name: demo
      username: demo
      password: 0penstack
    region_name: RegionOne
  ds-admin:
    auth:
      auth_url: http://192.168.122.10:35357/
      project_name: admin
      username: admin
      password: 0penstack
    region_name: RegionOne
```
### AWS credential file format:
#### path: credential_store/aws/ex_aws_creds.ini
AWS credentials follow standard botoconfig.ini format
```
[default]
aws_access_key_id = XXXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXX

[test]
aws_access_key_id = XXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXX

[test2]
aws_access_key_id = XXXXXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXX

```
### GCE credential file format:
#### path: credential_store/gcloud/ex_gcloud_creds.json
Copy the service account json creds to gcloud format

Example service account json:
```
{
  "type": "service_account",
  "project_id": "xxxxxxxxxxxxx",
  "private_key_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "private_key": "-----BEGIN PRIVATE KEY-----xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n-----END PRIVATE KEY-----\n",
  "client_email": "xxxxxxxxxxxxxxxx@xxxxxxxxxxxxx.iam.gserviceaccount.com",
  "client_id": "xxxxxxxxxxxxxxxxxxxxx",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/xxxxxxxxxxxxxxxc%40xxxxxxxxxxxxx.iam.gserviceaccount.com"
}
```

### Duffy credentials file
#### path: roles/duffy/vars/duffy_cred.yml
```
---
key_path: ~/duffy.key
url_base: http://admin.ci.centos.org:8080
```

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
      assoc_creds: "ex_os_creds" # name of the credential file 
      profile: "devstack" # profile listed in credential file
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
        assoc_creds: "ex_aws_creds" # name of the credential file
        profile: "test" # profile listed in credential file
    -
        resource_group_name: "testgroup4"
        res_group_type: "gcloud"
        res_defs:
          -
            res_name: "testvmgce"  # note gce resource names should not contain '_' characters 
            flavor: "n1-standard-1"
            res_type: "gcloud_gce"
            region: "us-central1-a" # name of credential_file
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

## Example Inventory Layout (openshift 3 node cluster)
```
---
inventory_layout:
  vars:
    openshift_hostname: __IP__
    openshift_public_hostname: __IP__
  hosts:
    openshift-master:
      host_groups:
        - masters
        - nodes
        - OSEv3
    openshift-node:
      count: 1
      host_groups:
        - nodes
        - OSEv3
    openshift-repo-host:
      host_groups:
        - nodes
        - OSEv3
        - repo_host
  host_groups:
    OSEv3:
      vars:
        openshift_docker_additional_registries: |
            "registry.example.com"
        openshift_docker_insecure_registries: |
            "registry.example.com"
        debug_level: 2
        ansible_sudo: False
        ansible_ssh_user: root
        openshift_override_hostname_check: True
        openshift_set_hostname: True
      children:
        - masters
        - nodes

```
## CLI Examples
### Provision a topology

```
$ ansible-playbook -vvv provision/site.yml -e "topology='/path/to/topology_file'" \
-e 'state=present'
```

### Teardown a topology
```
$ ansible-playbook -vvv provision/site.yml -e "topology='/path/to/topology_file'" \
-e 'state=absent'
```
### Note:
In both Provision/Teardown commands, certain values are available beyond
'data' and 'state'. Here's a few possible other values:

* topology_output_file: default determined by topology_name variable
  (provided in topology file)
* inventory_output_path: where generated inventory files will land
* inventory_playbooks: a list of playbooks which generate the ansible
  inventories for each infrastructure
* inventory_layout_file: the mapping file used to generate ansible inventories
  used for additional work with a provisioned cluster



