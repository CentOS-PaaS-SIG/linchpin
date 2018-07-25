FROM openshift/jenkins-slave-base-centos7:v3.6
##
## ------------------------------------->  ^^ this is needed
## since the centosCI openshift cluster
## is running 3.6 and the slave needs the
## correct 'oc' binary to work properly
## This should be updated when the cluster
## is upgraded.
##

RUN curl -L -o /etc/yum.repos.d/herlo-linchpin-epel7.repo \
https://copr.fedorainfracloud.org/coprs/herlo/linchpin-epel7/repo/epel-7/herlo-linchpin-epel7-epel-7.repo; \
yum install -y epel-release; \
yum install -y gcc python-devel libyaml-devel buildah \
python-pip python-setuptools python-wheel python-twine \
ansible jq ruby && yum clean all && rm -rf /var/cache/yum; \
pip install -U pip setuptools wheel twine
