#!/bin/sh

chmod 666 /dev/kvm

/usr/sbin/libvirtd&
/usr/sbin/virtlogd&

tail -f /dev/null
