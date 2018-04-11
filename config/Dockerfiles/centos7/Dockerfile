FROM centos:7
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Centos7"

ENV HOME=/root
WORKDIR $HOME

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y install python-pip ansible curl gcc python-devel openssl-devel \
                   libvirt-daemon-driver-* libvirt-daemon libvirt-daemon-kvm \
                   qemu-kvm libvirt-daemon-config-network libvirt-python \
                   libvirt-devel file openssh mkisofs libvirt-client \ 
                   net-tools git python-krbV make intltool libosinfo \
                   libxslt-python krb5-workstation gtk-update-icon-cache \
    && yum clean all; \
    (cd /lib/systemd/system/sysinit.target.wants/; for i in *; \
     do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
    rm -f /lib/systemd/system/multi-user.target.wants/*;\
    rm -f /etc/systemd/system/*.wants/*;\
    rm -f /lib/systemd/system/local-fs.target.wants/*; \
    rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
    rm -f /lib/systemd/system/basic.target.wants/*;\
    rm -f /lib/systemd/system/anaconda.target.wants/*; \
    systemctl enable libvirtd; \
    systemctl enable virtlockd

RUN yum -y remove PyYAML python-requests python-ipaddress && yum -y clean all

RUN pip install -U pip; \
    pip install -U setuptools; \
    pip install 'requests>=2.14.2'; \
    pip install 'ipaddress>=1.0.17'; \
    pip install 'PyYAML>=3.12'; \
    pip install ipaddr

RUN curl -Lo /root/virt-manager-1.5.0.tar.gz \
    https://github.com/virt-manager/virt-manager/archive/v1.5.0.tar.gz; \
    tar xvf /root/virt-manager-1.5.0.tar.gz; \
    pushd virt-manager-1.5.0; \
    ./setup.py install; \
    popd

#RUN yum -y install virt-install

RUN sed -i "/Service/a ExecStartPost=\/bin\/chmod 666 /dev/kvm" /usr/lib/systemd/system/libvirtd.service

RUN curl -o /etc/yum.repos.d/beaker-client.repo \
            https://beaker-project.org/yum/beaker-client-CentOS.repo; \
    yum install beaker-client; \
    yum clean all

COPY centos7/default.xml /etc/libvirt/qemu/networks/

RUN mkdir -p $HOME/.config

# /wordir should include the source code of linchpin
VOLUME [ "/workdir" , "/sys/fs/cgroup"]
CMD ["/usr/sbin/init"]
