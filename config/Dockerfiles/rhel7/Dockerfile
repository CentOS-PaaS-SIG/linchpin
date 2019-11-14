FROM registry.access.redhat.com/ubi7/ubi
USER root
LABEL maintainer="linchpin"
# Disable RHSM
RUN sed -i -e  's/^\(enabled\).*/\1=0/g' /etc/yum/pluginconf.d/subscription-manager.conf

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y install python-pip \
    && pip install -U pip \
    && yum -y install curl \
    yum -y install gcc python-devel openssl-devel ansible file openssh \
                    net-tools git make \
                    krb5-workstation \
                    python-requests jq git which; \
RUN sed -i "/Service/a ExecStartPost=\/bin\/chmod 666 /dev/kvm" /usr/lib/systemd/system/libvirtd.service

RUN curl -o /etc/yum.repos.d/beaker-client.repo \
            https://beaker-project.org/yum/beaker-client-CentOS.repo; \
    yum -y install beaker-client \
    && yum clean all && rm -rf /var/cache/yum;

# Start bash
ENTRYPOINT ["/usr/bin/tail -f /dev/null"]
