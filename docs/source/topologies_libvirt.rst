Libvirt Topologies
==================

.. contents:: Topics

.. _libvirt_topologies:


Simple Libvirt Topology
`````````````````````````

.. code-block:: yaml

   ---
    topology_name: "libvirt_simple"
    resource_groups:
      -
        resource_group_name: "simple"
        res_group_type: "libvirt"
        res_defs:

          - res_name: "centos72"
            res_type: "libvirt_node"
            driver: 'qemu'
            uri: 'qemu:///system'
            image_src: 'file:///tmp/linchpin_centos71.img'
            count: 2
            memory: 2048
            vcpus: 2
            networks:
              - name: linchpin-centos72

          - res_name: "centos71"
            res_type: "libvirt_node"
            uri: 'qemu:///system'
            count: 1
            image_src: 'http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1608.qcow2.xz'
            memory: 2048
            vcpus: 2
            arch: x86_64
            networks:
              - name: linchpin-centos71

.. note:: Each set of nodes can only be assigned one network at this time.

.. note:: The above topology assumes both networks exist and are running at
    provision time. If they are not, or do not exist, they will not be created
    and will fail.

Complete Libvirt Topology
`````````````````````````

.. code-block:: yaml

    ---
    topology_name: "libvirt_test"
    resource_groups:
      -
        resource_group_name: "libvirt1"
        res_group_type: "libvirt"
        res_defs:

          - res_name: "linchpin-centos72"
            res_type: "libvirt_network"
            ip: 192.168.77.100
            dhcp_start: 192.168.77.101
            dhcp_end: 192.168.77.112

          - res_name: "linchpin-centos74"
            res_type: "libvirt_network"

          - res_name: "centos72"
            res_type: "libvirt_node"
            uri: 'qemu:///system'
            count: 2
            memory: 2048
            vcpus: 2
            networks:
              - name: linchpin-centos72

          - res_name: "centos74"
            res_type: "libvirt_node"
            uri: 'qemu://libvirt.example.com/system'
            memory: 1024
            vcpus: 1
            networks:
              - name: linchpin-centos74

.. note:: as compared with the ``simple`` topology above, this topology
    defines and enables the network(s) with the res_type of libvirt_network.

.. note:: The ``linchpin-centos72`` network will support dhcp, with a defined pool.

.. note:: The ``linchpin-centos74`` is providing only the network definition.
    Each defined node would need to manually configure its own ip address.

.. note:: Libvirt provisioning does not yet support ``assoc_creds`` as simple
    adjustments can be made to a hypervisor to accommodate authentication.
