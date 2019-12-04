[![Build Status](https://travis-ci.com/oasis-roles/oasis-dummy.svg?branch=master)](https://travis-ci.com/oasis-roles/oasis-dummy)

oasis-dummy
===========

Basic description for oasis-dummy

Requirements
------------

Ansible 2.4 or higher

Red Hat Enterprise Linux 7 or equivalent

Valid Red Hat Subscriptions

Role Variables
--------------

Currently the following variables are supported:

### General

* `oasis-dummy_become` - Default: true. If this role needs administrator
  privileges, then use the Ansible become functionality (based off sudo).
* `oasis-dummy_become_user` - Default: root. If the role uses the become
  functionality for privilege escalation, then this is the name of the target
  user to change to.

Dependencies
------------

None

Example Playbook
----------------

```yaml
- hosts: oasis-dummy-servers
  roles:
    - role: oasis_roles.oasis-dummy
```

License
-------

GPLv3

Author Information
------------------

Author Name <authoremail@domain.net>