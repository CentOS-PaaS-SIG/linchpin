FROM openshift/jenkins-slave-base-centos7:v3.7
RUN yum install -y epel-release
# add ruby for ghi
RUN yum install -y python-pip python-setuptools ansible jq ruby
RUN pip install -U pip setuptools
