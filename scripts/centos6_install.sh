#!/bin/bash

DISTRO=$(cat /etc/redhat-release | cut -f1 -d' ')

if [ "${DISTRO}" == "CentOS" ] || [ "${DISTRO}" == "Red Hat" ]; then
    if [ "${DISTRO}" == "CentOS" ]; then
        VER=$(rpm -q --queryformat '%{VERSION}' centos-release)
    else
        VER=$(rpm -q --queryformat '%{RELEASE}' redhat-release-server | awk -F. '{print $1}')
    fi

    if [ "${VER}" != "6" ]; then
        echo "Can only be run on CentOS 6 or Red Hat 6 systems"
        exit 1
    fi
else
    echo "Can only be run on CentOS 6 or Red Hat 6 systems"
    exit 1
fi

SUDO=''

if [ "$USER" != "root" ]; then
    SUDO=$(which sudo)
    echo "User is not root, using ${SUDO}"
fi

# Install the EPEL RPM.

EPEL_PKG="epel-release"
rpm -q ${EPEL_PKG} >  /dev/null
RES=${?}
if [ "${RES}" != "0" ]; then
    ${SUDO} yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
    if [ "${?}" != 0 ]; then
        exit 1
    fi
fi

# Follow this up with the LinchPin dependencies.
LP_PKGS="python-pip python-virtualenv libffi-devel openssl-devel libyaml-devel gmp-devel libselinux-python make gcc redhat-rpm-config libxml2-python libxslt-python"

for pkg in ${LP_PKGS}; do
    rpm -q ${pkg} > /dev/null
    RES=${?}
    if [ "${RES}" != "0" ]; then
        ${SUDO} yum install -y ${pkg}
        if [ "${?}" != 0 ]; then
            exit 1
        fi
    fi
done


# install some additional dependencies used for installing LinchPin via the
# python pip package manager.
DEP_PKGS="gcc python-devel libxslt-devel python-jinja2-26 libffi-devel"

for pkg in ${DEP_PKGS}; do
    rpm -q ${pkg} > /dev/null
    RES=${?}
    if [ "${RES}" != "0" ]; then
        ${SUDO} yum install -y ${pkg}
        if [ "${?}" != 0 ]; then
            exit 2
        fi
    fi
done

# Because pip and setuptools from RPM are too old, update them.
# use --force because otherwise setuptools won't update
${SUDO} pip install pip setuptools --force --upgrade

# To address `AttributeError: 'module' object has no attribute 'HAVE_DECL_MPZ_POWM_SEC
# <https://github.com/ansible/ansible/issues/276#issuecomment-54228436>`_,
${SUDO} pip uninstall -y pycrypto

CRYPTO_PKGS="python-crypto python-paramiko"

for pkg in ${CRYPTO_PKGS}; do
    rpm -q ${pkg} > /dev/null
    RES=${?}
    if [ "${RES}" != "0" ]; then
        ${SUDO} yum install -y ${pkg}
        if [ "${?}" != 0 ]; then
            exit 3
        fi
    fi
done

# When removing the above packages, it removed a few other dependencies.
# Add them back here.
URL_PKGS="python-urllib3 python-six python-requests"

for pkg in ${URL_PKGS}; do
    rpm -q ${pkg} > /dev/null
    RES=${?}
    if [ "${RES}" == "0" ]; then
        ${SUDO} yum remove -y ${pkg}
        if [ "${?}" != 0 ]; then
            exit 5
        fi
    fi
done

${SUDO} pip uninstall -y urllib3 six requests

CLOUD_PKGS="cloud-init"
for pkg in ${CLOUD_PKGS}; do
    rpm -q ${pkg} > /dev/null
    RES=${?}
    if [ "${RES}" != "0" ]; then
        ${SUDO} yum install -y ${pkg}
        if [ "${?}" != 0 ]; then
            exit 7
        fi
    fi
done

${SUDO} pip install six requests urllib3 PyOpenSSL --force --upgrade
if [ "${?}" != 0 ]; then
    exit 8
fi

echo
echo
echo "Dependencies installed. Install linchpin."
echo "From pypi, run:"
echo
echo "sudo pip install linchpin"
echo
echo "or from source run:"
echo
echo "$ sudo yum install git"
echo "$ git clone git://github.com/CentOS-PaaS-SIG/linchpin.git"
echo "$ cd linchpin"
echo "$ sudo pip install ."
echo
echo "Test it by running:"
echo
echo "linchpin --version"
echo
echo "The output should be something like:"
echo
echo "linchpin version 1.5.0"
echo
echo
echo "Have a great day!"






