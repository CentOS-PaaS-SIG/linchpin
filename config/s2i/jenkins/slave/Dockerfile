FROM openshift/jenkins-slave-base-centos7:v3.7

# Install dependencies for JenkinsfileRelease
# add ruby for ghi
RUN yum install -y epel-release
RUN yum install -y gcc python-devel libyaml-devel \
python-pip python-setuptools python-wheel python-twine \
ansible jq ruby && yum clean all && rm -rf /var/cache/yum

RUN pip install -U pip setuptools wheel twine
