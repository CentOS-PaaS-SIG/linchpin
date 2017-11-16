FROM fedora:25
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Fedora25"

ENV HOME=/root
WORKDIR $HOME

RUN dnf -y install python-pip ansible curl gcc python-devel python2-shade \
                   openssl-devel libvirt-daemon-driver-* libvirt-daemon \
                   libvirt-daemon-kvm qemu-kvm libvirt-daemon-config-network \
                   libvirt-python libvirt-devel redhat-rpm-config \
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

RUN pip install -U pip
RUN pip install -U setuptools
RUN sed -i "/Service/a ExecStartPost=\/bin\/chmod 666 /dev/kvm" /usr/lib/systemd/system/libvirtd.service

COPY linchpin-install.sh $HOME/
COPY linchpin-test.sh $HOME/
COPY pip_install.sh $HOME/

RUN $HOME/pip_install.sh
RUN mkdir -p $HOME/.config

# /wordir should include the source code of linchpin
VOLUME [ "/workdir" , "/sys/fs/cgroup"]
CMD ["/usr/sbin/init"]
