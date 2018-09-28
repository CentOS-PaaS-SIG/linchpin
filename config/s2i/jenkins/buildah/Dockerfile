FROM fedora:28
LABEL name="contrainfra/buildah" \
      maintainer="herlo@redhat.com" \
      version="0.0.1" \
      description="Container to build and release docker images used by contra-infra tools"

RUN curl -L -o /etc/yum.repos.d/herlo-linchpin-epel7.repo \
https://copr.fedorainfracloud.org/coprs/herlo/linchpin-epel7/repo/epel-7/herlo-linchpin-epel7-epel-7.repo; \
yum install -y epel-release; \
yum install -y gcc python-devel libyaml-devel buildah \
python-pip python-setuptools python-wheel python-twine \
ansible jq ruby && yum clean all && rm -rf /var/cache/yum; \
pip install -U pip setuptools wheel twine
