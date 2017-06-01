LinchPin 1.2.x ROADMAP - October 1, 2017??
******************************

Authentication Driver for Libvirt and others
-----------------------------------------
- Libvirt -- PolicyKit/SSH/tcp integration/sudo (become) methods


Reworking Schema
-------------------------
- Use cerberus on a driver by driver basis to validate schemas

Zuul Integration
---------------------
Sean Myers is working on this

New providers
-------------------
- Azure
- RHEV RHEL
- Foreman

Rework on Roles
-----------------------
- Small playbooks that do provision/teardown per provider
- Create a plugin model for ephemeral services

Split out Linchpin API/REST API from cli
------------------------------------------------------
- API becomes linchpin pkg (libraries and playbooks)
- CLI becomes linchpin-cli pkg (just cli tooling)

Hooks
--------

- Built-in Hooks
  - inventory generator
  - resource outputter
  - schema validation
- Global hooks functionality

- State tracking:
  - on_success/on_failure flags for hooks and actions
  - Implement retry in hooks on failure

REST Service
-------------------
- simple rest service interface
