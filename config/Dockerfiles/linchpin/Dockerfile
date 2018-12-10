FROM fedora:28
LABEL name="contrainfra/linchpin" \
      maintainer="https://github.com/CentOS-PaaS-SIG/linchpin" \
      version="1.6.5" \
      description="LinchPin executable container running the latest Fedora release"

ARG install_location='linchpin'
ARG git_project='https://github.com/CentOS-PaaS-SIG/linchpin'
ARG git_branch='develop'

ENV UID=10001
ENV HOME=/linchpin/
ENV PATH=${HOME}/bin:${PATH}

COPY conf/ansible.cfg /etc/ansible/ansible.cfg
COPY conf/linchpin.conf /etc/linchpin.conf
COPY bin/ ${HOME}/bin/

RUN curl -L -o /etc/yum.repos.d/beaker-client.repo \
    https://beaker-project.org/yum/beaker-client-Fedora.repo; \
    dnf install -y git beaker-client \
        python-pip \
        ansible \
        curl gcc \
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
    if [ "${install_location}" == "." ]; then \
        git clone -b ${git_branch} --single-branch ${git_project} lp; \
        pushd lp; \
    fi; \
        pip install -U pip; \
        pip install -U setuptools; \
        pip install ${install_location}; \
        pip install ${install_location}[beaker]; \
        mkdir -p ${HOME}/bin/ && \
        chmod -R u+x ${HOME}/bin && \
        chown -R ${UID}.0 ${HOME} && \
        chmod -R g=u ${HOME} /etc/passwd; \
        (cd /lib/systemd/system/sysinit.target.wants/; for i in *; \
        do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
        rm -f /lib/systemd/system/multi-user.target.wants/*; \
        rm -f /etc/systemd/system/*.wants/*; \
        rm -f /lib/systemd/system/local-fs.target.wants/*; \
        rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
        rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
        rm -f /lib/systemd/system/basic.target.wants/*; \
        rm -f /lib/systemd/system/anaconda.target.wants/*; \
    if [ "install_location" == "." ]; then \
        popd; \
        rm -rf lp; \
    fi;

### Containers should NOT run as root as a good practice
USER ${UID}
WORKDIR ${HOME}

### user name recognition at runtime w/ an arbitrary uid - for OpenShift deployments
ENTRYPOINT [ "uid_entrypoint" ]

CMD [ "run" ]
