FROM registry.access.redhat.com/ubi8/ubi
USER root
LABEL maintainer="linchpin"
RUN dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm -y
RUN dnf install -y python3-pip curl gcc python3-devel openssl-devel redhat-rpm-config file \
                   openssh net-tools make libxslt krb5-workstation libselinux-python3 git \
                   libxslt-devel libxslt

# Disable RHSM
RUN sed -i -e  's/^\(enabled\).*/\1=0/g' /etc/yum/pluginconf.d/subscription-manager.conf
# Start bash
ENTRYPOINT ["/usr/bin/tail -f /dev/null"]
