FROM centos:8
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Centos8"

ENV HOME=/root
WORKDIR $HOME
RUN yum -y update
RUN yum -y install epel-release
RUN yum -y update && \
    yum -y install python3-pip && \
    pip3 install -U setuptools && \
    yum install -y python3-devel gcc openssl-devel ansible libvirt-daemon-driver-* \
                   libvirt-daemon libvirt-daemon-kvm qemu-kvm libvirt-daemon-config-network \
                   python3-libvirt curl python3-devel openssl-devel ansible \
                   libvirt-daemon-driver-* libvirt-daemon libvirt-daemon-kvm \
                   qemu-kvm libvirt-daemon-config-network \
                   libvirt-devel virt-install file openssh mkisofs \
                   libvirt-client net-tools git make \
                   python3-lxml libxslt-devel libxslt krb5-workstation \
                   python3-requests jq buildah git which; \
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
    systemctl enable virtlockd;
RUN sed -i "/Service/a ExecStartPost=\/bin\/chmod 666 /dev/kvm" /usr/lib/systemd/system/libvirtd.service

RUN curl -o /etc/yum.repos.d/beaker-client.repo \
            https://beaker-project.org/yum/beaker-client-CentOS.repo; \
    yum -y install beaker-client \
    && yum clean all && rm -rf /var/cache/yum;

RUN mkdir -p $HOME/.config

# /wordir should include the source code of linchpin
VOLUME [ "/workdir" , "/sys/fs/cgroup"]
CMD ["/usr/sbin/init"]
