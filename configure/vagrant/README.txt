Each subfolder here contains, minimally, a Vagrantfile and a hosts file that
can be orchestratred together for development and testing, or just for trying
the playbooks in a non-destructive and low-maintenance setting.

You can choose to manually invoke "vagrant up" if you have options you would
like to pass to Vagrant. Alternatively, ./full_cycle.sh will destroy any 
currently running VMs from that machine, spin up fresh ones, and run the
playbooks.

If you opt to manually spin up through "vagrant up" you can then invoke the
configure.sh script in each directory to run the Ansible playbook against the
included hosts file. Of course it's possible to run that Ansible command by
yourself as well, by just passing in the provided hosts file and pointing to
the site.yml file in the parent of this directory.

A brief list of the available systems with some of their notable features

master:
- CentOS 7
- All default options from the playbook
- Guaranteed to work out-of-the-box (if you can spin up Vagrant VMs)
- Please report bugs if this one does not spin up without modification
- Access through http://192.168.8.2/ after spin up

master_rhel7:
- RHEL 7
- Requires minimally configuring a rhel_base url to point to a valid RHEL
  mirror infrastructure
- Will not work without RHEL mirrors, but should spin up just fine with
- Access through http://192.168.8.2/ after spin up
