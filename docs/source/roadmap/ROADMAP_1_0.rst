****************************
LinchPin 1.0.0 ROADMAP
****************************

Enhancements
------------

- Better python package
  - Reduce noise by containing the library under the ``linchpin`` namespace

- Beaker provisioner

- Convert from lincnpin_config.yml to linchpin.conf
  - Add tooling to load configurations from linchpin.conf

- LinchPin Context to manage environment

- Unit Tests
  - Testing of python libraries, including API, Context, CLI, etc.
  - Created dummy provisining provider to perform testing

- Hooks
  - `pre` / `post` hooks for both `up` and `destroy` actions

- Direct credential management
  - All core cloud providers (gce, ec2, openstack) can authenticate using their traditional method
  - An override can be passed via the CLI/API using the variable ``creds_path``

- Customizable workspace in the CLI/API
  - LinchPin now provides a workspace option. The PinFile, topology, layout and hooks live here.

- Context provides logging to a centralized log file, console (stdout/stderr), or both

- OpenShift provisioning provider

- 

Documentation Improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^

- Beaker topology
- Inline API documentation now on readthedocs


Bug Fixes
----------

- #177 Missing dependency for python-krbV

While this bug indicated wontfix and was closed, the improvement was instead to add functionality to the ``setup.py``. This created the ability to ship extra dependencies by simply performing a `pip install linchpin[krbV]`.

- #202 linchpin-config.yml inconsistencies

This lead to the rework of the configuration into ``linchpin.conf``, and the ``Context`` objects

- #225 Linchpin multiple targets no longer work

When running ``linchpin up/destroy`` actions, if no target(s) are passed, all targets are acted upon. This failed after reworking the ``linchpin.conf`` and adding the ``Context`` object.

- #226 Returned results from API calls (up and destroy) when console set to False does not contain failures

This bug prevented certain users of the LinchPin API from gathering results from the Ansible runs. To that end, the _invoke_playbook method was reworked to return the results in a list of TaskResult objects.

