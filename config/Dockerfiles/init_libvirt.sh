#!/usr/bin/sh

/usr/bin/mkdir -p /var/run/libvirt
/usr/bin/chmod 666 /dev/kvm

/usr/sbin/libvirtd &
/usr/bin/sleep 5
/usr/sbin/virtlogd
