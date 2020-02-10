FROM fedora:30
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Fedora-30"

ENV HOME=/root
WORKDIR $HOME


RUN dnf -y install python3-pip ansible curl gcc python3-devel \
                   openssl-devel libvirt-daemon-driver-* libvirt-daemon \
                   libvirt-daemon-kvm qemu-kvm libvirt-daemon-config-network \
                   python3-libvirt libvirt-devel redhat-rpm-config file \
                   openssh genisoimage libvirt-client virt-install net-tools \
                   make libxslt-python krb5-workstation jq buildah \
                   python3-libselinux git \
    && dnf clean all; \
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

RUN export GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

RUN curl -o /etc/yum.repos.d/beaker-client.repo \
            https://beaker-project.org/yum/beaker-client-Fedora.repo; \
    dnf -y install beaker-client; \
    dnf clean all

COPY init_libvirt.sh $HOME/

RUN pip install -U pip; \
    pip install -U setuptools; \
    pip install -U pygithub; \
    pip install -U pyaml; \
    sed -i "/Service/a ExecStartPost=\/bin\/chmod 666 /dev/kvm" \
      /usr/lib/systemd/system/libvirtd.service

RUN echo "namespaces = []" >> /etc/libvirt/qemu.conf

# /workdir should include the source code of linchpin
VOLUME [ "/workdir" ]
CMD ["/usr/sbin/init"]
