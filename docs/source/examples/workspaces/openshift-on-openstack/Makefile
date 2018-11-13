credentials/clouds.yaml:
	@echo "No clouds.yml found! Please configure and try again"
	exit 1

hooks/ansible/openshift-ansible:
	pushd hooks/ansible && \
		git clone -b release-3.9 https://github.com/openshift/openshift-ansible

openshift-on-openstack: hooks/ansible/openshift-ansible credentials/clouds.yaml
	CREDS_PATH=./credentials linchpin -v \
		   --template-data "{\"ansible_ssh_user\": \"centos\"}" \
		   up openshift-on-openstack

destroy-openshift-on-openstack: credentials/clouds.yaml
	CREDS_PATH=./credentials linchpin -v \
                   --template-data "{\"ansible_ssh_user\": \"centos\"}" \
                   destroy openshift-on-openstack
