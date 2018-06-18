FROM openshift/jenkins-slave-base-centos7:v3.6
##
## ------------------------------------->  ^^ this is needed
## since the centosCI openshift cluster
## is running 3.6 and the slave needs the
## correct 'oc' binary to work properly
## This should be updated when the cluster
## is upgraded.
##

# Install dependencies for JenkinsfileRelease
# add ruby for ghi
RUN yum install -y epel-release; \
yum install -y gcc python-devel libyaml-devel \
python-pip python-setuptools python-wheel python-twine \
ansible jq ruby && yum clean all && rm -rf /var/cache/yum; \
pip install -U pip setuptools wheel twine
