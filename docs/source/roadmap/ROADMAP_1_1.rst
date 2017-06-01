LinchPin 1.1.x ROADMAP - July 31, 2017?
***************************************

More Unit Tests #257
---------------------
- coverage
- flake8
- cli fail testing
- api fail testing
- linchpin-lib pass/fail testing

Integration Testing #247
-------------------------

- testing of each provider set in core (openstack, ec2, gce, libvirt)

Regression Testing
-------------------------

- More research needed

Bug Fixes from 1.0.0 release
----------------------------

It's inevitable, there will be many bugs to fix. :)

Cloud-Init functionality #111 #148
-----------------------------

- Libvirt
- openstack userdata tooling
- aws userdata??
- gce userdata??

State Logging
--------------

- Report transitioning between states
  - (prehooks -> up -> posthooks -> resources -> postreshooks? -> inventory_generation -> postgenhooks)

Output / Exception Handling
---------------------------

- The basic exception handling is in place. CLI output works, but isn't perfect.
- Refine the API to return messages, let the interface handle how to display them.

Investigate dependency pinning/Investigate reducing dependencies (separate packages??)
--------------------------------------------------------------------------------------

- There are a lot of packages that can probably be removed
- Break out drivers to a separate package (core pkgs may become linchpin-drivers-core or somesuch)
- Create packages for linchpin library and linchpin-cli
  - Already have some of this, but it's not clean)

Upgrade to Ansible 2.3
-------------------------------

- Handle new magic_vars
- Verify/Adapt any API changes work in LinchPin

Python 3 conversion
---------------------------

Ansible is ready (pretty much), so should we be.
