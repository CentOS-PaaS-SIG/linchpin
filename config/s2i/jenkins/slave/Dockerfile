FROM openshift/jenkins-slave-base-centos7:v3.7
RUN yum install -y epel-release
RUN yum install -y gcc python-devel libyaml-devel
RUN yum install -y python-pip python-setuptools python-wheel python-twine
# add ruby for ghi
RUN yum install -y ansible jq ruby
RUN pip install -U pip setuptools wheel twine
