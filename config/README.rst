Automated Testing of LinchPin
-----------------------------

LinchPin has automated testing from PR's (Pull Requests) in GitHub.  Whenever a PR is updated or
the trigger phrase '[test]' is included in the comment a set of tests will be kicked off.  These tests are orchestrated via jenkins in the `Centos CI openshift environment <https://jenkins-continuous-infra.apps.ci.centos.org/>`_.

The point of these tests is to verify that LinchPin works correctly in a variety of different environments.
We currently exercise current releases of both Centos and Fedora.  On those distros we test the following providers: dummy, duffy, aws, libvirt, openstack, and beaker.  We are continuing to expand this.

These distros are provided as containers which are deployed inside the openshift environment.

Typical workflow
++++++++++++++++

A typical workflow would be creating a PR in github under https://github.com/CentOS-PaaS-SIG/linchpin/pulls
This will automatically cause a build to be created and will test your changes.  If for some reason the build
fails for a reason other than your change you can trigger it again by commenting in the PR with '[test]'.

If you make changes and push another commit to the same PR it will automatically test those changes again.

When your changes are verified both by the automated testing and have been reviewed you can issue a merge
by commenting in the PR with '[merge]'.  It is important to do merges this way since any changes to containers
will be promoted to 'stable' at this time.

Details of the orchestration
++++++++++++++++++++++++++++

* config/Dockerfiles/<DISTRO>/Dockerfile
* config/Dockerfiles/Jenkinsfile
* config/Dockerfiles/JenkinsfileContainer
* config/Dockerfiles/JenkinsfileStageTrigger
* config/Dockerfiles/JenkinsfileStageMerge
* config/s2i
* config/Dockerfiles/linchpin-install.sh
* config/Dockerfiles/linchpin-tests.sh
* config/Dockerfiles/tests.d/

config/Dockerfiles/<DISTRO>/Dockerfile
++++++++++++++++++++++++++++++++++++++

Each distro will have a Dockerfile which will start with a FROM entry that matches the
distro.  All rpm dependencies that LinchPin relies on should be installed.  One of the
points of the container is to be stable and show us if we have accidentally pulled
in a new dependency.  If the libvirt target is going to be tested in this distro
you will need to make sure that libvirt is installed and configured to run inside
the container.

config/Dockerfiles/Jenkinsfile
++++++++++++++++++++++++++++++

This is a scripted pipeline file that tells jenkins how to setup the containers
needed for the testing and how to execute the tests.  When adding a new distro
you will need the following (replace <DISTRO> with the actual container name):

* <DISTRO>_TAG environment variable which defaults to 'stable'
* string parameter <DISTRO>_tag which defaults to 'stable'
* containerTemplate describing how to bring up <DISTRO>
* Install stage which executes the linchpin-install.sh script
* Test stage which defines env.PROVIDERS stating which providers should be tested for this <DISTRO> and execute the linchpin-tests.sh script.  The list of providers to test can be overridden by setting a global environment variable in jenkins called LINCHPIN_PROVIDERS.  Any Targets that require authentication can be handled by creating a credential file in jenkins.  The id of the key should be named <PROVIDER>-key.  For example duffy-key.  In this example a duffy.key will be copied to keys/duffy/duffy.key.  When the target is executed CREDS_PATH will be exported to this path.

config/s2i
++++++++++

s2i stands for Source to Image. We are actually using Dockerfiles for the
distros. When adding a new distro, a build template yaml file will be needed.
This describes how to build that distro. The create-containers.sh script
will also need to be updated to reference this template.

config/Dockerfiles/linchpin-install.sh
++++++++++++++++++++++++++++++++++++++

This is the script that is executed from the <DISTRO>-INSTALL stage of jenkins.
When jenkins executes this script it runs from the git checkout of the PR under test.
If any other files are needed to test certain targets like authentication keys they should
be installed at this time.

config/Dockerfiles/linchpin-tests.sh
++++++++++++++++++++++++++++++++++++

This is the script that is executed from the <DISTRO>-TEST stage of jenkins.
Based on the values from the environment variable PROVIDERS it will execute
linchpin-test.sh for each PROVIDER in series.

config/Dockerfiles/tests.d/
+++++++++++++++++++++++++++++++++++

Tests are stored in directories within this structure. The structure includes
specific distro folders, and more generic directories which may be used by
multiple distros and/or providers. This tree structure shows several tests,
along with some directories which do not have tests::

    $ cd config/Dockerfiles/tests.d/ && tree
    .
    ├── aws
    ├── beaker
    ├── dummy
    │   ├── 01_dummy-template-data
    │   └── 02_dummy-template-data-file
    ├── general
    │   └── 01_general
    ├── inventory
    │   └── 01_template_inventory
    ├── libvirt
    └── openstack
        ├── 01_os-server-new
        ├── 02_os-server-template
        ├── 03_os-server-template-file
        ├── 04_os-sg-new
        └── 05_os-vol-new

The empty directories are just placeholders, and `linchpin-tests.sh` will find
no tests inside and move to the next directory.

Each test contains a small header which details the distros and providers that
would run a particular test. Here is the header for `dummy/01_dummy-template-data`::

    $ cat dummy/01_dummy-template-data
    #!/bin/bash -xe

    # Verify dummy provisioning using inline template data
    # distros.exclude: none
    # providers.include: dummy
    # providers.exclude: none
    .. snip ..

This shows an example that will run for any distro passed into the script. The
only provider that will use this script is dummy.

.. note:: These lines are intentionally commented and must start at the left margin.

.. note:: If both `providers.include` and `providers.exclude` are set, the
   script only reads `providers.include` line. The `providers.include` line
   must be set to 'none' for `providers.exclude` to be used.

Below these lines, the script is freeform, and can use whatever language desired.
The only two items passed in are 'distro' and 'provider' in that order. Another
more complex example of the header may be helpful here, for clarity::

    # Verify template-based provisioning using complex template data file
    # distros.exclude: fedora26 fedora27
    # providers.include: none
    # providers.exclude: dummy openstack beaker duffy aws

This is the header for `inventory/01_template_inventory`. It excludes both
fedora26 and fedora27 from being tested. Additionally, it excludes providers
dummy, openstack, beaker, duffy, and aws. Essentially, as of this writing,
this test would run only on the centos7 distro, for libvirt.

.. note:: The distro and provider are determined in the JenkinsfileContainer
   script.

config/Dockerfiles/JenkinsfileStageTrigger
++++++++++++++++++++++++++++++++++++++++++

This is a declarative pipeline script that watches LinchPin's github repo for
any PR's that need testing.  If the changeset includes changes to a distro's
Dockerfile it will rebuild the container and use that version of the container
for testing.  If you add a new distro you will also need to update the tagmap
like so::

    tagMap['<DISTRO>'] = STABLE_LABEL

replace <DISTRO> with the actual distro name.

config/Dockerfiles/JenkinsfileStageMerge
++++++++++++++++++++++++++++++++++++++++

This is a declarative pipeline script that watches LinchPin's github repo for
any PR's that have the comment '[merge]'.  If found it will look for any
containers that have a tag from this PR and promote them to stable.  Finally it will
merge the PR.  No need to modify this file when a new distro is added.
