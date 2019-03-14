FROM centos:7
# trigger 2.0 release 
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Centos7"

ENV HOME=/root
WORKDIR $HOME

COPY centos7/centos7-pike.repo /etc/yum.repos.d/centos7-pike.repo
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y install python-pip \
    && pip install -U pip \
    && pip install -U setuptools \
    && yum -y install curl \
    && curl -o /etc/yum.repos.d/herlo-linchpin-epel7.repo \
    https://copr.fedorainfracloud.org/coprs/herlo/linchpin-epel7/repo/epel-7/herlo-linchpin-epel7-epel-7.repo; \
    yum -y install gcc python-devel openssl-devel ansible \
                    libvirt-daemon-driver-* libvirt-daemon libvirt-daemon-kvm \
                    qemu-kvm libvirt-daemon-config-network libvirt-python \
                    libvirt-devel virt-install file openssh mkisofs \
                    libvirt-client net-tools git python-krbV make \
                    libxslt-python krb5-workstation PyYAML python-ipaddress \
                    python-requests jq; \
    (cd /lib/systemd/system/sysinit.target.wants/; for i in *; \
     do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
    rm -f /lib/systemd/system/multi-user.target.wants/*;\
    rm -f /etc/systemd/system/*.wants/*;\
    rm -f /lib/systemd/system/local-fs.target.wants/*; \
    rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
    rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
    rm -f /lib/systemd/system/basic.target.wants/*;\
    rm -f /lib/systemd/system/anaconda.target.wants/*; \
    rm -f /usr/sbin/vgs; \
    rm -f /usr/sbin/lvs; \
    rm -f /usr/sbin/pvs; \
    systemctl enable libvirtd; \
    systemctl enable virtlockd
RUN sed -i "/Service/a ExecStartPost=\/bin\/chmod 666 /dev/kvm" /usr/lib/systemd/system/libvirtd.service

RUN curl -o /etc/yum.repos.d/beaker-client.repo \
            https://beaker-project.org/yum/beaker-client-CentOS.repo; \
    yum -y install beaker-client \
    && yum clean all && rm -rf /var/cache/yum;

COPY centos7/default.xml /etc/libvirt/qemu/networks/

RUN mkdir -p $HOME/.config

# /wordir should include the source code of linchpin
VOLUME [ "/workdir" , "/sys/fs/cgroup"]
CMD ["/usr/sbin/init"]
