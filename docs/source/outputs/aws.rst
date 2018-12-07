AWS Sample Output
=================

.. code-block:: json

    {
       "kernel": null,
       "root_device_type": "ebs",
       "private_dns_name": "",
       "public_ip": "",
       "private_ip": "",
       "id": "i-01cc0455abe8465b8",
       "ebs_optimized": false,
       "state": "running",
       "virtualization_type": "hvm",
       "root_device_name": "/dev/sda1",
       "ramdisk": null,
       "block_device_mapping": {
         "/dev/sdb": {
           "status": "attached",
           "delete_on_termination": true,
           "volume_id": "vol-0f3311851115c8241"
         },
         "/dev/sda1": {
           "status": "attached",
           "delete_on_termination": true,
           "volume_id": "vol-00f6f149c57ac152c"
         }
       },
       "key_name": null,
       "image_id": "ami-984189e2",
       "tenancy": "default",
       "groups": {
         "sg-eae64983": "default",
         "sg-8a1d78e3": "public"
       },
       "public_dns_name": "",
       "state_code": 16,
       "tags": {
         "color": "blue",
         "resource_group_name": "aws",
         "shape": "oval",
         "name": "demo-day"
       },
       "placement": "us-east-1c",
       "ami_launch_index": "0",
       "dns_name": "",
       "region": "us-east-1",
       "launch_time": "2018-10-01T17:19:23.000Z",
       "instance_type": "m1.small",
       "architecture": "x86_64",
       "hypervisor": "xen"
    }
