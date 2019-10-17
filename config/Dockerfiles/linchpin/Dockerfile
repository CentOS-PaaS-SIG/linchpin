FROM fedora:30
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
        python3-pip \
        ansible \
        curl gcc \
        python3-devel \
        openssl-devel \
        redhat-rpm-config file \
        net-tools \
        python-krbV \
        libxml2-python \
        krb5-workstation \
        libselinux-python \
        && dnf clean all; \
    if [ "${install_location}" == "." ]; then \
        if [[ ${git_branch} == PR-* ]]; then \
            git clone ${git_project} lp; \
            pushd lp; \
            PRNUM="$(cut -d'-' -f2 <<<${git_branch})"; \
            git fetch origin pull/${PRNUM}/head:pr_branch; \
            git checkout pr_branch; \
        else \
            git clone -b ${git_branch} --single-branch ${git_project} lp; \
            pushd lp; \
        fi; \
    fi; \
        pip3 install -U pip; \
        pip3 install -U setuptools; \
        pip3 install -U shade; \
        pip3 install ${install_location}; \
        pip3 install ${install_location}[beaker]; \
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
