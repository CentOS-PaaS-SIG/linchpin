Automated Testing of Linchpin
-----------------------------

Linchpin has automated testing from PR's (Pull Requests) in GitHub.  Whenever a PR is updated or
the trigger phrase '[test]' is included in the comment a set of tests will be kicked off.  These tests are orchestrated via jenkins in the `Centos CI openshift environment <https://jenkins-continuous-infra.apps.ci.centos.org/>`_.

The point of these tests is to verify that linchpin works correctly in a variety of different environments.
We currently exercise current releases of both Centos and Fedora.  On those distros we test the following targets: dummy, duffy, aws and libvirt.  We are continuing to expand this.

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
* config/s2i
* config/Dockerfiles/linchpin-install.sh
* config/Dockerfiles/linchpin-tests.sh
* config/Dockerfiles/linchpin-test.sh
* config/Dockerfiles/JenkinsfileStageTrigger
* config/Dockerfiles/JenkinsfileStageMerge

config/Dockerfiles/<DISTRO>/Dockerfile
++++++++++++++++++++++++++++++++++++++

Each distro will have a Dockerfile which will start with a FROM entry that matches the
distro.  All rpm dependencies that linchpin relies on should be installed.  One of the
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
* Test stage which defines env.TARGETS stating which targets should be tested for this <DISTRO> and execute the linchpin-tests.sh script.  The list of targets to test can be overridden by setting a global environment variable in jenkins called LINCHPIN_TARGETS.  Any Targets that require authentication can be handled by creating a credential file in jenkins.  The id of the key should be named <TARGET>-key.  For example duffy-key.  In this example a duffy.key will be copied to keys/duffy/duffy.key.  When the target is executed CREDS_PATH will be exported to this path.

config/s2i
++++++++++

s2i stands for Source to Image.  But we are actually using Dockerfiles for the
distros.  When adding a new distro, a build template yaml file will be needed.
This describes how to build that distro.  The create-containers.sh script
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
Based on the values from the environment variable TARGETS it will execute
linchpin-test.sh for each TARGET in series.

config/Dockerfiles/linchpin-test.sh
+++++++++++++++++++++++++++++++++++

This script is called from linchpin-tests.sh and simply does a linchpin up on
the name of the target passed in.  A linchpin destroy is called to clean up
any resources used.

config/Dockerfiles/JenkinsfileStageTrigger
++++++++++++++++++++++++++++++++++++++++++

This is a declarative pipeline script that watches linchpin's github repo for
any PR's that need testing.  If the changeset includes changes to a distro's 
Dockerfile it will rebuild the container and use that version of the container
for testing.  If you add a new distro you will also need to update the tagmap
like so::

    tagMap['<DISTRO>'] = STABLE_LABEL

replace <DISTRO> with the actual distro name.

config/Dockerfiles/JenkinsfileStageMerge
++++++++++++++++++++++++++++++++++++++++

This is a declarative pipeline script that watches linchpin's github repo for
any PR's that have the comment '[merge]'.  If found it will look for any 
containers that have a tag from this PR and promote them to stable.  Finally it will
merge the PR.  No need to modify this file when a new distro is added.
