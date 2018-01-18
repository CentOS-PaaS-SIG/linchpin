FROM centos:6
LABEL maintainer "https://github.com/CentOS-PaaS-SIG/linchpin"
LABEL description "This container will verify linchpin works under Centos6"

ENV HOME=/root
WORKDIR $HOME

RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

RUN yum -y install python-pip ansible curl gcc python-devel openssl-devel \
                   libxml2-devel libxslt-devel file openssh \
                   python-jinja2-26 libffi-devel

# install Libvirt deps
RUN yum -y install libvirt libvirt-devel libvirt-client libvirt-python \
                   qemu-kvm virt-install net-tools qemu-kvm libvirt-python \
                   mkisofs libvirt-client libguestfs-tools \
                   policycoreutils-python bridge-utils

RUN echo "options kvm-intel nested=1" > /etc/modprobe.d/kvm-intel.conf

RUN pip install -U pip
RUN pip install -U setuptools

# Per https://github.com/ansible/ansible/issues/276#issuecomment-54228436
# to fix the error:
# AttributeError: 'module' object has no attribute 'HAVE_DECL_MPZ_POWM_SEC'
RUN pip uninstall -y pycrypto
RUN yum -y remove python-crypto
RUN yum -y install python-crypto python-paramiko

# fix python-six missing
RUN yum -y remove python-six python-requests python-urllib3
RUN yum -y install cloud-init
RUN pip install six requests urllib3 PyOpenSSL --force --upgrade

RUN yum clean all

COPY linchpin-install.sh $HOME/
COPY linchpin-test.sh $HOME/
COPY linchpin-tests.sh $HOME/
COPY pip_install.sh $HOME/
COPY centos6/start_libvirtd.sh $HOME/

RUN $HOME/pip_install.sh


# /wordir should include the source code of linchpin
VOLUME [ "/workdir" ]
CMD ["/root/start_libvirtd.sh"]
