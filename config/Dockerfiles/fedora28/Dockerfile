FROM fedora:28
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Fedora28"

ENV HOME=/root
WORKDIR $HOME

RUN dnf -y install python-pip ansible curl gcc python-devel python2-shade \
                   openssl-devel libvirt-daemon-driver-* libvirt-daemon \
                   libvirt-daemon-kvm qemu-kvm libvirt-daemon-config-network \
                   libvirt-python libvirt-devel redhat-rpm-config file \
                   openssh mkisofs libvirt-client virt-install net-tools \
                   python-krbV make libxslt-python krb5-workstation jq \
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

RUN curl -o /etc/yum.repos.d/beaker-client.repo \
            https://beaker-project.org/yum/beaker-client-Fedora.repo; \
    yum install beaker-client; \
    yum clean all

COPY init_libvirt.sh $HOME/

RUN pip install -U pip; \
    pip install -U setuptools; \
    sed -i "/Service/a ExecStartPost=\/bin\/chmod 666 /dev/kvm" \
      /usr/lib/systemd/system/libvirtd.service

RUN echo "namespaces = []" >> /etc/libvirt/qemu.conf

# /workdir should include the source code of linchpin
VOLUME [ "/workdir" ]
CMD ["/usr/sbin/init"]
