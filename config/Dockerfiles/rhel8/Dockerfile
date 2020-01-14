FROM registry.redhat.io/ubi8/ubi
LABEL mantainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under RHEL 8"

ENV HOME=/root
WORKDIR $HOME

RUN subscription-manager register --username rcyoalne@gmail.com --password ******* --auto-attach; \
    dnf install -y python3 gcc platform-python-devel openssl-devel libvirt-daemon-driver-* libvirt-daemon libvirt-daemon-kvm qemu-kvm libvirt-daemon-config-network libvirt-devel virt-install file openssh mkisofs libvirt-client net-tools git make python3-lxml krb5-workstation python3-requests jq buildah git which python3-libselinux \
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
    rm -f /usr/sbin/pvs;
    # systemctl enable libvirtd; these can be re-enabled once systemd is working on rhel
    # systemctl enable virtlockd

RUN export GIT_PYTHON_GIT_EXECUTABLE=/usr/bin/git

RUN curl -o /etc/yum.repos.d/beaker-client.repo \
            https://beaker-project.org/yum/beaker-client-Fedora.repo; \
    dnf -y install beaker-client; \
    dnf clean all

COPY init_libvirt.sh $HOME/

RUN python3 -m pip install -U pip; \
    python3 -m pip install -U setuptools; \
    python3 -m pip install -U pygithub; \
    sed -i "/Service/a ExecStartPost=\/bin\/chmod 666 /dev/kvm" \
      /usr/lib/systemd/system/libvirtd.service

RUN echo "namespaces = []" >> /etc/libvirt/qemu.conf

# /workdir should include the source code of linchpin
VOLUME [ "/workdir" ]
CMD ["/usr/sbin/init"]
