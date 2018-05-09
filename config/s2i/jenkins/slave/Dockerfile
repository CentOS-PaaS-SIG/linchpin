FROM openshift/jenkins-slave-base-centos7:v3.7
RUN yum install -y epel-release
# add ruby for ghi
RUN yum install -y python-pip python-setuptools python-wheel python-twine
RUN yum install -y gcc libyaml-devel ansible jq ruby
RUN pip install -U pip setuptools wheel twine
