This folder contains an Ansible playbook for standing up and configuring
Jenkins masters and slaves. There are roles specifically for the creation of
those configurations, as well as several other roles which can be leveraged
for configuring and standing up resources of other types helpful in the
process of running continuous integration. Some of these roles are documented
here, along with information on how to leverage them and configure them.

For full documentation on the configuration options of each role, see the
default vars YAML file in the particular role. Any of the values in that file
are intended to be overridden by the user.

As a qiuck start, you can copy one of the folders in the "inventory" folder to
a new name "local" and modify the hosts file and any group_vars files to point
to the options you want.

If you are looking to just mess around with either development or take it for
a spin, you can jump into the vagrant/master folder and muuter ./full_cycle.sh
to get a local VM up and going and configured to run Jenkins master with all
of the default options from this playbook. If you have access to extra RHEL7
licenses, you can run from the vagrant/master_rhel folder, instead, but you
will need to pass through at least an additional option that points the system
to your RHEL repository mirror infrastructure.

Some notable defaults for Jenkins masters currently enabled are
- Java 8
- Jenkins LTS 1.651.3
- an extensive list of plugins found in files/jenkins-plugin-lists/default.txt
- SSL disabled, but Jenkins served off of port 80

Primary supported operating systems are
- RHEL 7
- CentOS 7
