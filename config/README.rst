Automated Testing of Linchpin
-----------------------------

Linchpin has automated testing from PR's (Pull Requests) in GitHub.  Whenever a PR is updated or
the trigger phrase '[test]' is included in the comment a set of tests will be kicked off.  These tests are orchestrated via jenkins in the `Centos CI openshift environment <https://jenkins-continuous-infra.apps.ci.centos.org/>`_.

The point of these tests is to verify that linchpin works correctly in a variety of different environments.
We currently exercise current releases of both Centos and Fedora.  On those targets only the dummy and
libvirt driver are currently tested but there are plans to expand this.

These targets are provided as containers which are deployed inside the openshift environment.

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

* config/Dockerfiles/<TARGET>/Dockerfile
* config/Dockerfiles/Jenkinsfile
* config/s2i
* config/Dockerfiles/linchpin-install.sh
* config/Dockerfiles/linchpin-tests.sh
* config/Dockerfiles/linchpin-test.sh
* config/Dockerfiles/JenkinsfileStageTrigger
* config/Dockerfiles/JenkinsfileStageMerge

config/Dockerfiles/<TARGET>/Dockerfile
++++++++++++++++++++++++++++++++++++++

Each target will have a Dockerfile which will start with a FROM entry that matches the
target.  All rpm dependencies that linchpin relies on should be installed.  One of the
points of the container is to be stable and show us if we have accidentally pulled
in a new dependency.  If the libvirt driver is going to be tested in this target
you will need to make sure that libvirt is installed and configured to run inside
the container.

config/Dockerfiles/Jenkinsfile
++++++++++++++++++++++++++++++

This is a scripted pipeline file that tells jenkins how to setup the containers
needed for the testing and how to execute the tests.  When adding a new target 
you will need the following (replace <TARGET> with the actual container name):

* <TARGET>_TAG environment variable which defaults to 'stable'
* string parameter <TARGET>_tag which defaults to 'stable'
* containerTemplate describing how to bring up <TARGET>
* Install stage which executes the linchpin-install.sh script
* Test stage which defines env.DRIVERS stating which drivers should be tested for this <TARGET> and execute the linchpin-tests.sh script.

config/s2i
++++++++++

s2i stands for Source to Image.  But we are actually using Dockerfiles for the
distros.  When adding a new target, a build template yaml file will be needed.
This describes how to build that target.  The create-containers.sh script
will also need to be updated to reference this template.

config/Dockerfiles/linchpin-install.sh
++++++++++++++++++++++++++++++++++++++

This is the script that is executed from the <TARGET>-INSTALL stage of jenkins.
When jenkins executes this script it runs from the git checkout of the PR under test.
If any other files are needed to test certain drivers like authentication keys they should
be installed at this time.

config/Dockerfiles/linchpin-tests.sh
++++++++++++++++++++++++++++++++++++

This is the script that is executed from the <TARGET>-TEST stage of jenkins.
Based on the values from the environment variable DRIVERS it will execute
linchpin-test.sh for each DRIVER in series.

config/Dockerfiles/linchpin-test.sh
+++++++++++++++++++++++++++++++++++

This script is called from linchpin-tests.sh and simply does a linchpin up on
the name of the driver passed in.  A linchpin destroy is called to clean up
any resources used.

config/Dockerfiles/JenkinsfileStageTrigger
++++++++++++++++++++++++++++++++++++++++++

This is a declarative pipeline script that watches linchpin's github repo for
any PR's that need testing.  If the changeset includes changes to a target's 
Dockerfile it will rebuild the container and use that version of the container
for testing.  If you add a new target you will also need to update the tagmap
like so::

    tagMap['<TARGET>'] = STABLE_LABEL

replace <TARGET> with the actual target name.

config/Dockerfiles/JenkinsfileStageMerge
++++++++++++++++++++++++++++++++++++++++

This is a declarative pipeline script that watches linchpin's github repo for
any PR's that have the comment '[merge]'.  If found it will look for any 
containers that have a tag from this PR and promote them to stable.  Finally it will
merge the PR.  No need to modify this file when a new target is added.
