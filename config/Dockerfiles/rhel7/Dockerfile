FROM registry.access.redhat.com/ubi7:latest

ENV SUMMARY="Base image which allows using of source-to-image."	\
    DESCRIPTION="The s2i-core image provides any images layered on top of it \
with all the tools needed to use source-to-image functionality while keeping \
the image size as small as possible."

RUN echo $'[centos]\n\
name=CentOS-7\n\
baseurl=http://ftp.heanet.ie/pub/centos/7/os/x86_64/\n\
enabled=1\n\
gpgcheck=1\n\
gpgkey=http://ftp.heanet.ie/pub/centos/7/os/x86_64/RPM-GPG-KEY-CentOS-7\n'\
> /etc/yum.repos.d/centos7.repo

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

RUN yum update -y && \
    yum -y install python3-pip python3-devel gcc curl mlocate openssl-devel ansible \
    qemu-kvm libvirt-daemon-config-network libvirt-python libvirt-devel virt-install \
    file openssh mkisofs libvirt-client net-tools git python-krbV make libxslt-python \
    krb5-workstation python-requests jq buildah git which;
RUN mkdir -p $HOME/.config;
RUN mkdir -p $HOME/.ssh;

# /wordir should include the source code of linchpin
VOLUME [ "/workdir" , "/sys/fs/cgroup"]
CMD ["/usr/sbin/init"] 
