GLOBAL_HOOKS = {
    "res_check": {
        "name": "res_check",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "res_check.yml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "ocp_container_boot_log": {
        "name": "ocp_container_boot_log",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "boot_log.yml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "ec2_boot_log": {
        "name": "ec2_boot_log",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "boot_log.yml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "beaker_log": {
        "name": "beaker_log",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "boot_log.yml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "os_server_boot_log": {
        "name": "os_server_boot_log",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "boot_log.yml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "check_ssh": {
        "name": "check_ssh",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "check_ssh.yaml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "ping": {
        "name": "ping",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "ping.yaml",
                "extra_vars": {
                    "ansible_ssh_user": "",
                    "ansible_ssh_private_key": ""
                }
            }
        ]
    },
    "port_up": {
        "name": "port_up",
        "context": True,
        "type": "ansible",
        "actions": [
            {
                "playbook": "port_up.yaml",
                "extra_vars": {
                    "port": 22,
                }
            }
        ]
    }
}
