FROM centos:7
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under centos7"

ENV HOME=/root
WORKDIR $HOME

ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8

# install python 3 dependencies
#RUN  yum install -y epel-release
RUN  yum update -y \
     && yum install -y python3 python3-pip python3-devel python3-setuptools 

RUN yum -y install  ansible libvirt-daemon-driver-* libvirt-daemon libvirt-daemon-kvm \
                    qemu-kvm libvirt-daemon-config-network libvirt-python \
                    libvirt-devel virt-install file openssh mkisofs \
                    python-libvirt python3-libvirt python2-lxml python3-lxml \
                    libvirt-client net-tools git python-krbV make \
                    krb5-workstation \
                    python-requests jq buildah git which; 
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; \
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
