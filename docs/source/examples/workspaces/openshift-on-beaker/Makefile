credentials/beaker.conf:
	@echo "No beaker.conf found! Please configure and try again"
	exit 1

hooks/ansible/openshift-ansible:
	pushd hooks/ansible && \
		git clone -b release-3.9 https://github.com/openshift/openshift-ansible

openshift-on-beaker: hooks/ansible/openshift-ansible credentials/beaker.conf
	BEAKER_CONF=$(PWD)/credentials/beaker.conf linchpin -v up openshift-on-beaker

destroy-openshift-on-beaker: credentials/beaker.conf
	BEAKER_CONF=$(PWD)/credentials/beaker.conf linchpin -v \
                   destroy openshift-on-beaker
