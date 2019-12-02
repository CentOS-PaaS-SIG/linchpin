#!/bin/sh
set -x # verbose output
set -e # fail the whole script if some command fails
mkdir -p results
resultdir=$(readlink -f results)
org=CentOS-PaaS-SIG
branch=master
repo=https://github.com/$org/linchpin
release_repo=https://github.com/CentOS-PaaS-SIG/linchpin

pip install --user rpmvenv

mkdir -p linchpin
git init linchpin
git -C linchpin pull --depth 1 $repo $branch
cd linchpin
python2 setup.py sdist -d "$resultdir"

version="$(cat linchpin/version.py | awk -F "'" '{print $2}' | head -n1)"
rpmvenv linchpin.json --core_version="${version}" --verbose --spec > "${resultdir}/linchpin.spec"
sed -i -e "s#^Requires: .*#Requires: git, beaker-client, nanomsg#g" \
       -e '/^# Blocks/i %{?fc30:Requires: python2-lxml, python2-libvirt}' \
       -e '/^# Blocks/i %{?rhel:Requires: python-lxml, libvirt-python}' \
       -e '/^# Blocks/i BuildRequires: python2-pip, python2-devel, gcc' \
       -e "s#^cd %{SOURCE0}#cd %{_builddir}/linchpin-${version}/#g" \
       -e "s#^Source0: .*#Source0: ${release_repo}/archive/v${version}.tar.gz#g" \
       -e "s#%{SOURCE0}#%{_builddir}/linchpin-${version}#g" \
       -e '/^%prep/a %setup -q' \
       -e '/^%prep/a touch %{_builddir}/linchpin.sh' \
       -e '/^%prep/a chmod +x %{_builddir}/linchpin.sh' \
       -e '/^%prep/a cat << EOF > %{_builddir}/linchpin.sh\n#!/bin/bash\nPYTHONPATH="/usr/lib/python2.7/site-packages:/usr/lib64/python2.7/site-packages" /opt/linchpin/bin/linchpin \\$\@\nEOF' \
       -e '/^%prep/a pip2 install --user rpmvenv virtualenv==16.1.0' \
       -e "/^%install/a cp %{_builddir}/linchpin.sh  %{_builddir}/linchpin-${version}/linchpin.sh" \
       -e '/^%install/a export PATH=$PATH:~/.local/bin' \
       -e '/^%post/i find %{buildroot} -name "*.pyc" -exec rm -rf {} \\\;' \
       -e '/^%post/i find %{buildroot} -type f -print0 | xargs -0 sed -i "s|${RPM_BUILD_ROOT}||g"' \
       -e '/^# Macros/i %undefine __brp_mangle_shebangs' \
       -e '/^# Macros/i %global _build_id_links none' \
       -e '/^%post/i unlink %{buildroot}/opt/linchpin/lib64 || true' \
       -e '/^%post/i ln -s /opt/linchpin/lib %{buildroot}/opt/linchpin/lib64 || true' \
 "${resultdir}/linchpin.spec"
