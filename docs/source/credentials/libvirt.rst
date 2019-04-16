Libvirt doesn't require credentials via LinchPin. Multiple options are
available for authenticating against a Libvirt daemon (libvirtd). Most methods
are detailed `here <https://libvirt.org/auth.html>`_.  If desired, the uri for
the resource can be set using one of these mechanisms.

By default, however, libvirt requires sudo access to use.  To allow users
without sudo access to provision libvirt instances, run the following commands
on the target machine:

#. Create the libvirt group if it does not exist

   .. code-block:: bash

      $ getent group | grep libvirt
      $ groupadd -g 7777 libvirt

#. Add user account to libvirt group

   .. code-block:: bash

      $ usermod -aG libvirt <user>

#. Edit libvirtd configuration to add group

   .. code-block:: bash

      $ cat <<EOF >>/etc/libvirt/libvirtd.conf
      unix_sock_group = "libvirt"
      unix_sock_rw_perms = "0770"
      EOF

#. Restart the libvirtd daemon

   .. code-block:: bash

      $ systemctl restart libvirtd

The next time the user logs in, they will be able to provision libvirt disks
without sudo access


