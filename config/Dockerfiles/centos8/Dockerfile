FROM centos:8
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Centos8"

ENV HOME=/root
WORKDIR $HOME

RUN dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
RUN dnf -y install python3 platform-python-pip \
    && dnf -y install python3 platform-python-pip curl gcc python3-devel openssl-devel \
                      libvirt-daemon-driver-* libvirt-daemon libvirt-daemon-kvm \
                      qemu-kvm libvirt-daemon-config-network libvirt-python3 \
                      libvirt-devel virt-install file openssh mkisofs \
                      libvirt-client net-tools git make \
                      python3-lxml krb5-workstation krb5-devel \
                      python3-requests jq buildah git which \
    && pip3 install -U pip \
    && pip3 install -U setuptools \
    && pip3 install -U pygithub \
    && pip3 install -U openstackclient boto>=2.49.0 \
    && pip3 install ansible; \
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

#RUN curl -o /etc/yum.repos.d/beaker-client.repo \
#            https://beaker-project.org/yum/beaker-client-CentOS.repo; \
#    dnf -y install beaker-client \
RUN dnf clean all && rm -rf /var/cache/dnf;

RUN mkdir -p $HOME/.config

# /wordir should include the source code of linchpin
VOLUME [ "/workdir" , "/sys/fs/cgroup"]
CMD ["/usr/sbin/init"]
