GLOBAL_HOOKS = {
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
