[![Build Status](https://travis-ci.com/oasis-roles/aws.svg?branch=master)](https://travis-ci.com/oasis-roles/aws)

aws
===========

AWS role for LinchPin

Requirements
------------

Ansible 2.7 or higher

Red Hat Enterprise Linux 7, CentOS 7, Fedora 30 or highter

Valid Red Hat Subscriptions (if using RHEL)

Role Variables
--------------

Currently the following variables are supported:

### General

* `res_defs` - The resource definitions for the target

Dependencies
------------

None

Example Playbook
----------------

```yaml
- hosts: aws-servers
  roles:
    - role: oasis_roles.aws
```

License
-------

GPLv3

Author Information
------------------

Ryan Cole <rycole@redhat.com>
