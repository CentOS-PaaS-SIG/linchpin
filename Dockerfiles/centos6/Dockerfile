FROM centos:6
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Centos6"

ENV HOME=/root
WORKDIR $HOME

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
RUN yum -y install python-pip ansible curl gcc python-devel openssl-devel \
                   libvirt-daemon-driver-* libvirt-daemon libvirt-daemon-kvm \
                   qemu-kvm libvirt-daemon-config-network libvirt-python \
                   libvirt-devel libxml2-devel libxslt-devel file openssh \
                   mkisofs libvirt-client virt-install net-tools && yum clean all
RUN pip install -U pip
RUN pip install -U setuptools

COPY linchpin-install.sh $HOME/
COPY linchpin-test.sh $HOME/
COPY pip_install.sh $HOME/
COPY centos6/start_libvirtd.sh $HOME/

RUN $HOME/pip_install.sh
RUN mkdir -p $HOME/.config

# /wordir should include the source code of linchpin
VOLUME [ "/workdir" ]
CMD ["/root/start_libvirtd.sh"]
