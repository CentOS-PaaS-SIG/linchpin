FROM centos:7
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Centos7"

ENV HOME=/root
ENV LC_ALL=en_US.utf8
ENV LANG=en_US.utf8
WORKDIR $HOME

COPY centos7/centos7-pike.repo /etc/yum.repos.d/centos7-pike.repo
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN yum -y install python3-pip
RUN curl -o /etc/yum.repos.d/herlo-linchpin-epel7.repo \
    https://copr.fedorainfracloud.org/coprs/herlo/linchpin-epel7/repo/epel-7/herlo-linchpin-epel7-epel-7.repo
RUN yum -y install gcc python3-devel openssl-devel ansible \
                    libvirt-daemon-driver-* libvirt-daemon libvirt-daemon-kvm \
                    qemu-kvm libvirt-daemon-config-network libvirt-python3 \
                    libvirt-devel virt-install file openssh mkisofs \
                    libvirt-client net-tools git python3-krbV make \
                    libxslt-python3 python3-libselinux krb5-workstation \
                    python3-requests jq buildah git which; \
    pip3 install -U pip \
    && pip3 install -U setuptools \
    && pip3 install -U pygithub \
    && pip3 install -U openstackclient boto>=2.49.0 \
    && pip3 install -U curl; \
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
