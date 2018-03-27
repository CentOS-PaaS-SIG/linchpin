FROM centos:6
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Centos6"

ENV HOME=/root
WORKDIR $HOME

# Per https://github.com/ansible/ansible/issues/276#issuecomment-54228436
# to fix the error:
# AttributeError: 'module' object has no attribute 'HAVE_DECL_MPZ_POWM_SEC'

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm; \
    yum -y install python-pip ansible curl gcc python-devel openssl-devel \
                   libxml2-devel libxslt-devel file openssh \
                   python-jinja2-26 libffi-devel \
                   libvirt libvirt-devel libvirt-client libvirt-python \
                   qemu-kvm virt-install net-tools qemu-kvm libvirt-python \
                   mkisofs libvirt-client libguestfs-tools \
                   policycoreutils-python bridge-utils python-krbV; \
    echo "options kvm-intel nested=1" > /etc/modprobe.d/kvm-intel.conf; \
    pip install -U pip; \
    pip install -U setuptools; \
    pip uninstall -y pycrypto; \
    yum -y remove python-crypto; \
    yum -y install python-crypto python-paramiko; \
    yum -y remove python-six python-requests python-urllib3; \
    yum -y install cloud-init; \
    pip install six requests urllib3 PyOpenSSL --force --upgrade; \
    yum clean all

RUN curl -o /etc/yum.repos.d/beaker-client.repo \
            https://beaker-project.org/yum/beaker-client-CentOS.repo; \
    yum install beaker-client; \
    yum clean all

COPY centos6/start_libvirtd.sh $HOME/

# /workdir should include the source code of linchpin
VOLUME [ "/workdir" ]
CMD ["/root/start_libvirtd.sh"]
