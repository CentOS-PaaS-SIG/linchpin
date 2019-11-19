FROM fedora:31
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Fedora-30"

ENV HOME=/root
WORKDIR $HOME

RUN dnf -y install python2
RUN dnf -y install python-pip ansible curl gcc python-devel \
                   openssl-devel redhat-rpm-config file \
                   openssh \
                   python-krbV make libxslt-python krb5-workstation jq buildah \
                   git \
    && dnf clean all;

RUN pip install -U setuptools; \
    pip install -U pygithub;

RUN export GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

RUN curl -o /etc/yum.repos.d/beaker-client.repo \
            https://beaker-project.org/yum/beaker-client-Fedora.repo; \
    dnf -y install beaker-client; \
    dnf clean all

# /workdir should include the source code of linchpin
VOLUME [ "/workdir" ]
ENTRYPOINT ["tail", "-f", "/dev/null"]
