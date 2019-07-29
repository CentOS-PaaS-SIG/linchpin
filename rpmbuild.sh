#!/bin/sh
set -x # verbose output
set -e # fail the whole script if some command fails
mkdir -p results
resultdir=$(readlink -f results)
repo=https://github.com/CentOS-PaaS-SIG/linchpin

pip install --user rpmvenv

git clone --single-branch --branch master --depth 1 $repo
cd linchpin
python2 setup.py sdist -d "$resultdir"

version="$(cat linchpin/version.py | awk -F "'" '{print $2}' | head -n1)"
rpmvenv linchpin.json --core_version="${version}" --verbose --spec > "${resultdir}/linchpin.spec"
sed -i '/^# Blocks/i BuildRequires: python2-pip' "${resultdir}/linchpin.spec"
sed -i '/^# Blocks/i BuildRequires: python2-devel' "${resultdir}/linchpin.spec"
sed -i "s#^cd %{SOURCE0}#cd %{_builddir}/linchpin-${version}/#g" "${resultdir}/linchpin.spec"
sed -i "s#^Source0: .*#Source0: ${repo}/archive/v${version}.tar.gz#g" "${resultdir}/linchpin.spec"
sed -i "s#%{SOURCE0}#%{_builddir}/linchpin-${version}#g" "${resultdir}/linchpin.spec"
sed -i '/^%prep/a %setup -q' "${resultdir}/linchpin.spec"
sed -i '/^%prep/a chmod +x %{_builddir}/linchpin.sh' "${resultdir}/linchpin.spec"
sed -i '/^%prep/a cat << EOF > %{_builddir}/linchpin.sh\n#!/bin/bash\nPYTHONPATH=/usr/lib/python2.7/site-packages /opt/linchpin/bin/linchpin \\$\@\nEOF' "${resultdir}/linchpin.spec"
sed -i '/^%prep/a pip2 install --user rpmvenv virtualenv==16.1.0' "${resultdir}/linchpin.spec"
sed -i "/^%install/a cp %{_builddir}/linchpin.sh  %{_builddir}/linchpin-${version}/linchpin.sh" "${resultdir}/linchpin.spec"
sed -i '/^%install/a export PATH=$PATH:~/.local/bin' "${resultdir}/linchpin.spec"
sed -i '/^%post/i find %{buildroot} -name "*.pyc" -exec rm -rf {} \\\;' "${resultdir}/linchpin.spec"
sed -i '/^%post/i find %{buildroot} -type f -print0 | xargs -0 sed -i "s|${RPM_BUILD_ROOT}||g"' "${resultdir}/linchpin.spec"
sed -i '/^# Macros/i %undefine __brp_mangle_shebangs' "${resultdir}/linchpin.spec"
sed -i '/^# Macros/i %global _build_id_links none' "${resultdir}/linchpin.spec"
sed -i '/^%post/i unlink %{buildroot}/opt/linchpin/lib64 || true' "${resultdir}/linchpin.spec"
sed -i '/^%post/i ln -s /opt/linchpin/lib %{buildroot}/opt/linchpin/lib64 || true' "${resultdir}/linchpin.spec"
