openstack sample output
=======================

.. code-block:: json

    {
        "OS-DCF:diskConfig": "MANUAL",
        "OS-EXT-AZ:availability_zone": "nova",
        "OS-EXT-STS:power_state": 1,
        "OS-EXT-STS:task_state": null,
        "OS-EXT-STS:vm_state": "active",
        "OS-SRV-USG:launched_at": "2018-09-19T14:53:12.000000",
        "OS-SRV-USG:terminated_at": null,
        "accessIPv4": "",
        "accessIPv6": "",
        "addresses": {
            "e2e-openstack": [
                {
                    "OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:a1:c0:6b",
                    "OS-EXT-IPS:type": "fixed",
                    "addr": "",
                    "version": 4
                }
            ]
        },
        "adminPass": "",
        "az": "nova",
        "cloud": "defaults",
        "config_drive": "",
        "created": "2018-09-19T14:46:51Z",
        "created_at": "2018-09-19T14:46:51Z",
        "disk_config": "MANUAL",
        "flavor": {
            "id": "2",
            "name": "m1.small"
        },
        "has_config_drive": false,
        "hostId": "190ddf5e439d5fa9a5e767485c44e8fdbfa206166eaf5aa6ed100fc0",
        "host_id": "190ddf5e439d5fa9a5e767485c44e8fdbfa206166eaf5aa6ed100fc0",
        "id": "83e2d9d3-7823-45f3-8a58-52452acddaa8",
        "image": {
            "id": "11b72b11-59e8-4919-a918-265c1566bd45",
            "name": "CentOS-7-x86_64-GenericCloud-1612"
        },
        "interface_ip": "",
        "key_name": "ci-factory",
        "launched_at": "2018-09-19T14:53:12.000000",
        "location": {
            "cloud": "defaults",
            "project": {
                "domain_id": null,
                "domain_name": null,
                "id": "f53391f4d50643f283af5d59fc450e09",
                "name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
            },
            "region_name": "",
            "zone": "nova"
        },
        "metadata": {},
        "name": "596-master-d7b60a-1",
        "networks": {},
        "os-extended-volumes:volumes_attached": [],
        "power_state": 1,
        "private_v4": "",
        "progress": 0,
        "project_id": "f53391f4d50643f283af5d59fc450e09",
        "properties": {
            "OS-DCF:diskConfig": "MANUAL",
            "OS-EXT-AZ:availability_zone": "nova",
            "OS-EXT-STS:power_state": 1,
            "OS-EXT-STS:task_state": null,
            "OS-EXT-STS:vm_state": "active",
            "OS-SRV-USG:launched_at": "2018-09-19T14:53:12.000000",
            "OS-SRV-USG:terminated_at": null,
            "os-extended-volumes:volumes_attached": []
        },
        "public_v4": "",
        "public_v6": "",
        "region": "",
        "security_groups": [
            {
                "description": "Default security group",
                "id": "f48c6b12-497b-4301-97f5-0c8749815089",
                "location": {
                    "cloud": "defaults",
                    "project": {
                        "domain_id": null,
                        "domain_name": null,
                        "id": "f53391f4d50643f283af5d59fc450e09",
                        "name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                    },
                    "region_name": "",
                    "zone": null
                },
                "name": "default",
                "project_id": "f53391f4d50643f283af5d59fc450e09",
                "properties": {},
                "security_group_rules": [
                    {
                        "direction": "ingress",
                        "ethertype": "IPv4",
                        "group": {},
                        "id": "1b315474-5730-483e-a9b7-712530c17b19",
                        "location": {
                            "cloud": "defaults",
                            "project": {
                                "domain_id": null,
                                "domain_name": null,
                                "id": "f53391f4d50643f283af5d59fc450e09",
                                "name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                            },
                            "region_name": "",
                            "zone": null
                        },
                        "port_range_max": 22,
                        "port_range_min": 22,
                        "project_id": "",
                        "properties": {
                            "group": {}
                        },
                        "protocol": "tcp",
                        "remote_group_id": null,
                        "remote_ip_prefix": "0.0.0.0/0",
                        "security_group_id": "f48c6b12-497b-4301-97f5-0c8749815089",
                        "tenant_id": ""
                    },
                    {
                        "direction": "ingress",
                        "ethertype": "IPv4",
                        "group": {
                            "name": "default",
                            "tenant_id": "f53391f4d50643f283af5d59fc450e09"
                        },
                        "id": "2e45cfff-370d-460f-a88f-f3042b4a25d8",
                        "location": {
                            "cloud": "defaults",
                            "project": {
                                "domain_id": null,
                                "domain_name": null,
                                "id": "f53391f4d50643f283af5d59fc450e09",
                                "name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                            },
                            "region_name": "",
                            "zone": null
                        },
                        "port_range_max": null,
                        "port_range_min": null,
                        "project_id": "",
                        "properties": {
                            "group": {
                                "name": "default",
                                "tenant_id": "f53391f4d50643f283af5d59fc450e09"
                            }
                        },
                        "protocol": null,
                        "remote_group_id": null,
                        "remote_ip_prefix": null,
                        "security_group_id": "f48c6b12-497b-4301-97f5-0c8749815089",
                        "tenant_id": ""
                    },
                    {
                        "direction": "ingress",
                        "ethertype": "IPv4",
                        "group": {},
                        "id": "33078914-a857-45c4-8ed2-d4ba9d7b41be",
                        "location": {
                            "cloud": "defaults",
                            "project": {
                                "domain_id": null,
                                "domain_name": null,
                                "id": "f53391f4d50643f283af5d59fc450e09",
                                "name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                            },
                            "region_name": "",
                            "zone": null
                        },
                        "port_range_max": null,
                        "port_range_min": null,
                        "project_id": "",
                        "properties": {
                            "group": {}
                        },
                        "protocol": "icmp",
                        "remote_group_id": null,
                        "remote_ip_prefix": "0.0.0.0/0",
                        "security_group_id": "f48c6b12-497b-4301-97f5-0c8749815089",
                        "tenant_id": ""
                    },
                    {
                        "direction": "ingress",
                        "ethertype": "IPv4",
                        "group": {
                            "name": "default",
                            "tenant_id": "f53391f4d50643f283af5d59fc450e09"
                        },
                        "id": "b801bf97-f470-476b-9d63-b692de45ec67",
                        "location": {
                            "cloud": "defaults",
                            "project": {
                                "domain_id": null,
                                "domain_name": null,
                                "id": "f53391f4d50643f283af5d59fc450e09",
                                "name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                            },
                            "region_name": "",
                            "zone": null
                        },
                        "port_range_max": null,
                        "port_range_min": null,
                        "project_id": "",
                        "properties": {
                            "group": {
                                "name": "default",
                                "tenant_id": "f53391f4d50643f283af5d59fc450e09"
                            }
                        },
                        "protocol": null,
                        "remote_group_id": null,
                        "remote_ip_prefix": null,
                        "security_group_id": "f48c6b12-497b-4301-97f5-0c8749815089",
                        "tenant_id": ""
                    }
                ],
                "tenant_id": "f53391f4d50643f283af5d59fc450e09"
            }
        ],
        "status": "ACTIVE",
        "task_state": null,
        "tenant_id": "f53391f4d50643f283af5d59fc450e09",
        "terminated_at": null,
        "updated": "2018-09-19T14:53:12Z",
        "user_id": "e32798f55da74cffa90d629e50939582",
        "vm_state": "active",
        "volumes": []
    }
