Validate Command
-----------------

The purpose of the validate command is to determine whether topologies and layouts are syntactically valid.  If not, it will provide a list of errors that occured during validation

The command `linchpin validate` looks at the topology and layout files for each target in a given PinFile. If the topology is not valid under the current schema, it will attempt to convert the topology to an older schema and try again. If the topology is still invalid, the command will report the topology and a list of errors found.

Invalid Topologies
++++++++++++++++++

Here is a simple PinFile and topology file. The topology file has some errors and will not validate.

.. code-block:: yaml

   ---
   libvirt-new:
      topology: libvirt-new.yml
      layout: libvirt.yml

   libvirt:
      topology: libvirt.yml
      layout: libvirt.yml

   libvirt-network:
      topology: libvirt-network.yml


.. code-block:: yaml

   ---
   topology_name: libvirt-new
   resource_groups:
     - resource_group_name: libvirt-new
       resource_group_type: libvirt
       resource_definitions:
         - role: libvirt_node
           uri: qemu:///system
           count: "1"
           image_src: http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1608.qcow2.xz
           memory: 2048
           vcpus: 1
           arch: x86_64
           ssh_key: libvirt
           networks:
             - name: default
               additional_storage: 10G
           cloud_config:
             users:
               - name: herlo
                 gecos: Clint Savage
                 groups: wheel
                 sudo: ALL=(ALL) NOPASSWD:ALL
                 ssh-import-id: gh:herlo
                 lock_passwd: true

.. code-block:: bash

   $ linchpin validate
   topology for target 'libvirt-network' is valid

   Topology for target 'libvirt-new' does not validate
   topology: 'OrderedDict([('topology_name', 'libvirt-new'), ('resource_groups', [OrderedDict([('resource_group_name', 'libvirt-new'), ('resource_group_type', 'libvirt'), ('resource_definitions', [OrderedDict([('role', 'libvirt_node'), ('uri', 'qemu:///system'), ('image_src', 'http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1608.qcow2.xz'), ('memory', 2048), ('vcpus', '1'), ('arch', 'x86_64'), ('ssh_key', 'libvirt'), ('networks', [OrderedDict([('name', 'default'), ('hello', 'world')])]), ('additional_storage', '10G'), ('cloud_config', OrderedDict([('users', [OrderedDict([('name', 'herlo'), ('gecos', 'Clint Savage'), ('groups', 'wheel'), ('sudo', 'ALL=(ALL) NOPASSWD:ALL'), ('ssh-import-id', 'gh:herlo'), ('lock_passwd', True)])])])), ('count', 1)])])])])])'
   errors:
         res_defs[0][count]: value for field 'count' must be of type 'integer'
         res_defs[0][networks][0][additional_storage]: field 'additional_storage' could not be recognized within the schema provided
         res_defs[0][name]: field 'name' is required

   topology for target 'libvirt' is valid under old schema
   topology for target 'libvirt-network' is valid


The `linchpin validate` command can also provide a list of errors against the old schema with the `--old-schema` flag

.. code-block:: bash

   $ linchpin validate --old-schema
   
   Topology for target 'libvirt-new' does not validate
   topology: 'OrderedDict([('topology_name', 'libvirt-new'), ('resource_groups', [OrderedDict([('resource_group_name', 'libvirt-new'), ('resource_group_type', 'libvirt'), ('resource_definitions', [OrderedDict([('role', 'libvirt_node'), ('uri', 'qemu:///system'), ('image_src', 'http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1608.qcow2.xz'), ('memory', 2048), ('vcpus', '1'), ('arch', 'x86_64'), ('ssh_key', 'libvirt'), ('networks', [OrderedDict([('name', 'default'), ('hello', 'world')])]), ('additional_storage', '10G'), ('cloud_config', OrderedDict([('users', [OrderedDict([('name', 'herlo'), ('gecos', 'Clint Savage'), ('groups', 'wheel'), ('sudo', 'ALL=(ALL) NOPASSWD:ALL'), ('ssh-import-id', 'gh:herlo'), ('lock_passwd', True)])])])), ('count', 1)])])])])])'
   errors:
         res_defs[0][networks][0][additional_storage]: field 'additional_storage' could not be recognized within the schema provided
         res_defs[0][name]: field 'name' is required

   topology for target 'libvirt' is valid under old schema
   topology for target 'libvirt-network' is valid

As you can see, validation under both schemas result in an error stating that the field `additional_storage` could not be recognized.  In this case, there is simply an indentation error. `additional_storage` is a recognized field within `resource_definitions` but not within the `networks` sub-schema. Other times this unrecognized field may be a spelling error.  Both fields also flag the missing "name" field, which is required.  Both of these errors must be fixed in order for the topology file to validate.  Because making `count` a string only results in an error when validating against the old schema, this field does not have to be changed in order for the topology file to pass validation. However, it is best to change it anyway and keep your topology as up-to-date as possible.

Valid Topologies
++++++++++++++++

The topology below has been fixed so that it will validate under the current schema.

.. code-block:: yaml

   ---
   topology_name: libvirt-new
   resource_groups:
     - resource_group_name: libvirt-new
       resource_group_type: libvirt
       resource_definitions:
         - role: libvirt_node
           name: centos71
           uri: qemu:///system
           count: 1
           image_src: http://cloud.centos.org/centos/7/images/CentOS-7-x86_64-GenericCloud-1608.qcow2.xz
           memory: 2048
           vcpus: 1
           arch: x86_64
           ssh_key: libvirt
           networks:
             - name: default
           additional_storage: 10G
           cloud_config:
             users:
               - name: herlo
                 gecos: Clint Savage
                 groups: wheel
                 sudo: ALL=(ALL) NOPASSWD:ALL
                 ssh-import-id: gh:herlo
                 lock_passwd: true

If `linchpin validate` is run on a PinFile containing the topology above, this will be the output:

.. code-block:: bash

   $ linchpin validate
   topology for target 'libvirt-new' is valid
   topology for target 'libvirt' is valid under old schema
   topology for target 'libvirt-network' is valid
