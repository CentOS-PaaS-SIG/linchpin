FROM fedora:28
LABEL name="contrainfra/linchpin-executor" \
      maintainer="https://github.com/CentOS-PaaS-SIG/linchpin" \
      version="0.0.6" \
      description="LinchPin executable container running Fedora 28"

ENV APP_ROOT=/linchpin/
ENV PATH=${APP_ROOT}/bin:${PATH} HOME=${APP_ROOT}

COPY conf/ansible.cfg /etc/ansible/ansible.cfg
COPY conf/linchpin.conf /etc/linchpin.conf
COPY bin/ ${APP_ROOT}/bin/

RUN curl -L -o /etc/yum.repos.d/beaker-client.repo \
    https://beaker-project.org/yum/beaker-client-Fedora.repo; \
    dnf install -y beaker-client \
        python-pip \
        ansible \
        curl \
        python-devel \
        python2-shade \
        openssl-devel \
        redhat-rpm-config file \
        net-tools \
        python-krbV \
        libxslt-python \
        libxml2-python \
        krb5-workstation \
        libselinux-python \
        && dnf clean all; \
        pip install -U pip; \
        pip install -U setuptools; \
        pip install INSTALL_LOCATION; \
        pip install INSTALL_LOCATION[beaker]; \
        mkdir -p ${APP_ROOT} && \
        chmod -R u+x ${APP_ROOT}/bin && \
        chgrp -R 0 ${APP_ROOT} && \
        chmod -R g=u ${APP_ROOT} /etc/passwd; \
        (cd /lib/systemd/system/sysinit.target.wants/; for i in *; \
        do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
        rm -f /lib/systemd/system/multi-user.target.wants/*; \
        rm -f /etc/systemd/system/*.wants/*; \
        rm -f /lib/systemd/system/local-fs.target.wants/*; \
        rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
        rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
        rm -f /lib/systemd/system/basic.target.wants/*; \
        rm -f /lib/systemd/system/anaconda.target.wants/*;

### Containers should NOT run as root as a good practice
USER 1000
WORKDIR ${APP_ROOT}

### user name recognition at runtime w/ an arbitrary uid - for OpenShift deployments
ENTRYPOINT [ "uid_entrypoint" ]

CMD run
