LinchPin 1.1.x ROADMAP - July 31, 2017?
*******************************

More Unit Tests #257
---------------------
- coverage
- flake8
- cli fail testing
- api fail testing
- linchpin-lib pass/fail testing

Integration Testing #247
-------------------------
testing of each provider set in core (openstack, ec2, gce, libvirt)

Regression Testing
-------------------------
More research needed

Cloud-Init functionality #111 #148
-----------------------------
- Libvirt
- openstack userdata tooling
- aws userdata??
- gce userdata??

State Logging 
-------------------
- Report transitioning between states
  - (prehooks -> up -> posthooks -> resources -> postreshooks? -> inventory_generation -> postgenhooks)

Output / Exception Handling
-----------------------------------

Investigate dependency pinning
----------------------------------------

Investigate reducing dependencies (separate packages??)
--------------------------------------------

Upgrade to Ansible 2.3
-------------------------------
- Handle new magic_vars
- Verify/Adapt any API changes work in LinchPin

Python 3 conversion
---------------------------
Separate core and contributed providers in packaging (we've already got some of this, but it's not clean)
