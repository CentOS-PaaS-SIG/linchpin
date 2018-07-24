The RunDB Explained
-------------------

.. attention:: Much of the information below began in v1.2.0 and later.
   However, much of the data did not exist until later on, generally in
   version 1.5.0 or later. Some cases, where noted, the data is only planned,
   and does not yet exist.

The RunDB is the central database which stores transactions and target-based
runs each time any LinchPin action is performed. The RunDB stores detailed
data, including inputs like topology, inventory layout, hooks; and outputs
like resource return data, ansible inventory filename and data, etc.

RunDB Storage
`````````````

The RunDB is stored using a JSON format by default. `TinyDB
<http://tinydb.readthedocs.io/en/latest/>`_ currently provides the backend.
It is a NOSQL database, which writes out transactional records to a single
file. Other databases could provide a backend, as long as a driver is written and
included.

TinyDB is included in a class called `TinyRunDB
<https://github.com/CentOS-PaaS-SIG/linchpin/blob/develop/linchpin/rundb/tinyrundb.py>`_.
TinyRunDB is an implementation of a parent class, called BaseDB, which in turn
is a subclass of the abstract RunDB class.

Records are the main way for items to be stored in the RunDB. There are two
types of records stored in the RunDB, target, and transaction.

Transaction Records
```````````````````

Each time any action (eg. ``linchpin up``) occurs using linchpin, a
transaction record is stored. The transaction records are stored in the
'linchpin' table. The main constraint to this is that a target called
`linchpin` cannot be used.

Transaction Records consist of a Transaction ID `(tx_id)`, the action and
a target information for each target acted upon during the specified
transaction. A single record could have multiple targets listed.

.. code-block:: json

    "136": {
        "action": "up",
        "targets": [
            {
                "dummy-new": {
                    "290": {
                        "rc": 0,
                        "uhash": "27e1"
                    }
                },
                "libvirt-new": {
                    "225": {
                        "rc": 0,
                        "uhash": "d88c"
                    }
                }
            }
        ]
    },


In every case, the target data included is the name, run-id, return code (rc),
and uhash. The ``linchpin journal`` provides a transaction view to show this
data in human readable format.

.. code-block:: bash

    $ linchpin journal --view tx -t 136

    ID: 136			Action: up

    Target              Run ID	uHash	Exit Code 
    ---------------------------------------------
    dummy-new              290	 27e1	        0
    libvirt-new            225	 d88c	        0

    =============================================


Target Records
``````````````

Target Records are much more detailed. Generally, the target records
correspond to a specific Run ID (`run_id`). These can also be referenced via
the ``linchpin journal`` command, using the target (default) view.

.. code-block:: bash

    $ linchpin journal dummy-new --view target

    Target: dummy-new
    run_id	    action	     uhash       rc
    -----------------------------------------------
    225    	       up	     f9e5        0
    224    	  destroy	     89ea        0
    223    	       up	     89ea        0

The target record data is where the detail lies. Each record contains several
sections, followed by possibly several sub-sections. A complete target record
is very large. Let's have a look at record 225 for the 'dummy-new' target.

.. code-block:: json

    "225": {
        "action": "up",
        "end": "03/27/2018 12:18:21 PM",
        "inputs": [
            {
                "topology_data": {
                    "resource_groups": [
                        {
                            "resource_definitions": [
                                {
                                    "count": 3,
                                    "name": "web",
                                    "role": "dummy_node"
                                },
                                {
                                    "count": 1,
                                    "name": "test",
                                    "role": "dummy_node"
                                }
                            ],
                            "resource_group_name": "dummy",
                            "resource_group_type": "dummy"
                        }
                    ],
                    "topology_name": "dummy_cluster"
                }
            },
            {
                "layout_data": {
                    "inventory_layout": {
                        "hosts": {
                            "example-node": {
                                "count": 3,
                                "host_groups": [
                                    "example"
                                ]
                            },
                            "test-node": {
                                "count": 1,
                                "host_groups": [
                                    "test"
                                ]
                            }
                        },
                        "inventory_file": "{{ workspace }}/inventories/dummy-new-{{ uhash }}.inventory",
                        "vars": {
                            "hostname": "__IP__"
                        }
                    }
                }
            },
            {
                "hooks_data": {
                    "postup": [
                        {
                            "actions": [
                                "echo hello"
                            ],
                            "name": "hello",
                            "type": "shell"
                        }
                    ]
                }
            }
        ],
        "outputs": [
            {
                "resources": [
                    {
                        "changed": true,
                        "dummy_file": "/tmp/dummy.hosts",
                        "failed": false,
                        "hosts": [
                            "web-f9e5-0.example.net",
                            "web-f9e5-1.example.net",
                            "web-f9e5-2.example.net"
                        ]
                    },
                    {
                        "changed": true,
                        "dummy_file": "/tmp/dummy.hosts",
                        "failed": false,
                        "hosts": [
                            "test-f9e5-0.example.net"
                        ]
                    }
                ]
            }
        ],
        "rc": 0,
        "start": "03/27/2018 12:18:02 PM",
        "uhash": "f9e5",
        "cfgs": [
            {
                "evars": []
            },
            {
                "magics": []
            },
            {
                "user": []
            }
        ]
    },

As might be gleaned from looking at the JSON, there are a few main sections.
Some of these sections, have subsections. The main sections include::

  * action
  * start
  * end
  * uhash
  * rc
  * inputs
  * outputs
  * cfgs

Most of these sections are self-explanatory, or can be easily determined.
However, there are three that may need further explanation.

Inputs
~~~~~~

The RunDB stored all inputs in the "inputs" section.

.. code-block:: json

    "inputs": [
        {
            "topology_data": {
                "resource_groups": [
                    {
                        "resource_definitions": [
                            {
                                "count": 3,
                                "name": "web",
                                "role": "dummy_node"
                            },
                            {
                                "count": 1,
                                "name": "test",
                                "role": "dummy_node"
                            }
                        ],
                        "resource_group_name": "dummy",
                        "resource_group_type": "dummy"
                    }
                ],
                "topology_name": "dummy_cluster"
            }
        },
        {
            "layout_data": {
                "inventory_layout": {
                    "hosts": {
                        "example-node": {
                            "count": 3,
                            "host_groups": [
                                "example"
                            ]
                        },
                        "test-node": {
                            "count": 1,
                            "host_groups": [
                                "test"
                            ]
                        }
                    },
                    "inventory_file": "{{ workspace }}/inventories/dummy-new-{{ uhash }}.inventory",
                    "vars": {
                        "hostname": "__IP__"
                    }
                }
            }
        },
        {
            "hooks_data": {
                "postup": [
                    {
                        "actions": [
                            "echo hello"
                        ],
                        "name": "hello",
                        "type": "shell"
                    }
                ]
            }
        }
    ],

Currently, the `inputs` section has three sub-sections, `topology_data`,
`layout_data`, and `hooks_data`. These three sub-sections hold
relevant data. The use of this data is generally for record-keeping, and more
recently to allow for reuse of the data with linchpin up/destroy actions.

Additionally, some of this data is used to create the outputs, which are
stored in the `outputs` section.

Outputs
~~~~~~~

Going forward, the `outputs` section will contain much more data than is
displayed below. Items like `ansible_inventory`, and `user_data` will also
appear in the database. These will be provided in future development.

.. code-block:: json

    "outputs": [
        {
            "resources": [
                {
                    "changed": true,
                    "dummy_file": "/tmp/dummy.hosts",
                    "failed": false,
                    "hosts": [
                        "web-f9e5-0.example.net",
                        "web-f9e5-1.example.net",
                        "web-f9e5-2.example.net"
                    ]
                },
                {
                    "changed": true,
                    "dummy_file": "/tmp/dummy.hosts",
                    "failed": false,
                    "hosts": [
                        "test-f9e5-0.example.net"
                    ]
                }
            ]
        }
    ],

The lone sub-section is `resources`. For the `dummy-new` target,
the data provided is simplistic. However, for providers like openstack or aws,
the resources become quite large and extensive. Here is a snippet of an
openstack resources sub-section.

.. code-block:: json

    "resources": [
         {
             "changed": true,
             "failed": false,
             "ids": [
                 "fc96e134-4a68-4aaa-a053-7f53cae21369"
             ],
             "openstack": [
                 {
                     "OS-DCF:diskConfig": "MANUAL",
                     "OS-EXT-AZ:availability_zone": "nova",
                     "OS-EXT-STS:power_state": 1,
                     "OS-EXT-STS:task_state": null,
                     "OS-EXT-STS:vm_state": "active",
                     "OS-SRV-USG:launched_at": "2017-11-27T19:43:54.000000",
                     "OS-SRV-USG:terminated_at": null,
                     "accessIPv4": "10.8.245.175",
                     "accessIPv6": "",
                     "addresses": {
                         "atomic-e2e-jenkins-test": [
                             {
                                 "OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:ba:0e:5e",
                                 "OS-EXT-IPS:type": "fixed",
                                 "addr": "172.16.171.15",
                                 "version": 4
                             },
                             {
                                 "OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:ba:0e:5e",
                                 "OS-EXT-IPS:type": "floating",
                                 "addr": "10.8.245.175",
                                 "version": 4
                             }
                         ]
                     },
                     "adminPass": "<REDACTED>",
                     "az": "nova",
                     "cloud": "",
                     "config_drive": "",
                     "created": "2017-11-27T19:43:47Z",
                     "disk_config": "MANUAL",
                     "flavor": {
                         "id": "2",
                         "name": "m1.small"
                     },
                     "has_config_drive": false,
                     "hostId": "20a84eb5691c546defeac6b2a5b4586234aed69419641215e0870a64",
                     "host_id": "20a84eb5691c546defeac6b2a5b4586234aed69419641215e0870a64",
                     "id": "fc96e134-4a68-4aaa-a053-7f53cae21369",
                    "image": {
                         "id": "eae92800-4b49-4e81-b876-1cc61350bf73",
                         "name": "CentOS-7-x86_64-GenericCloud-1612"
                     },
                     "interface_ip": "10.8.245.175",
                     "key_name": "ci-factory",
                     "launched_at": "2017-11-27T19:43:54.000000",
                     "location": {
                         "cloud": "",
                         "project": {
                             "domain_id": null,
                             "domain_name": null,
                             "id": "6e65fbc3161648e78fde849c7abbd30f",
                             "name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                         },
                         "region_name": "",
                         "zone": "nova"
                     },
                     "metadata": {},
                     "name": "database-44ee-1",
                     "networks": {},
                     "os-extended-volumes:volumes_attached": [],
                     "power_state": 1,
                     "private_v4": "172.16.171.15",
                     "progress": 0,
                     "project_id": "6e65fbc3161648e78fde849c7abbd30f",
                     "properties": {
                         "OS-DCF:diskConfig": "MANUAL",
                         "OS-EXT-AZ:availability_zone": "nova",
                         "OS-EXT-STS:power_state": 1,
                         "OS-EXT-STS:task_state": null,
                         "OS-EXT-STS:vm_state": "active",
                         "OS-SRV-USG:launched_at": "2017-11-27T19:43:54.000000",
                         "OS-SRV-USG:terminated_at": null,
                         "os-extended-volumes:volumes_attached": []
                     },
                     "public_v4": "10.8.245.175",
                     "public_v6": "",
                     "region": "",
                     "security_groups": [
                         {
                             "description": "Default security group",
                             "id": "1da85eb2-3c51-4729-afc4-240e187a30ce",
                             "location": {
                                 "cloud": "",
                                 "project": {
                                     "domain_id": null,
                                     "domain_name": null,
                                     "id": "6e65fbc3161648e78fde849c7abbd30f",
                                     "name": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER"
                                 },
                    .. snip ..

.. note:: The data above continues for several more pages, and would take up
   too much space to document. A savvy user might cat the rundb file and pipe
   it to the python 'json.tool' module.

Each provider returns a large structure like this as results of the
provisioning (up) process. For the teardown, the data can be large, but is
generally more succinct.

..
..  Configurations (cfgs)
..  ~~~~~~~~~~~~~~~~~~~~~

..  .. attention:: This section is currently only a placeholder and doesn't yet
..     exist in the RunDB as shown below.
  
  When a LinchPin transaction occurs, there are many configurations which are
  passed in and used. Some are generated by LinchPin, these are referred to as
  'magic' configs. Others are presets provided by the :term:`linchpin.constants`
  file. Each section is used to configure linchpin, some are passed to ansible
  (evars). Additionally, user specific configs can be passed from the PinFile.
  In each case, these items have a sub-section within the cfgs section in the
  RunDB.
  
  .. code-block:: json
  
      "cfgs": [
          {
              "magics": {
                  "uhash": "f935"
                  "run_id": "225"
                  .. snip ..
              }
          },
          {
              "lp": {
                  "module_folder": "library",
                  "rundb_conn": "{{ workspace }}/.rundb/rundb-::mac::.json",
                  "rundb_type": "TinyRunDB",
                  "rundb_conn_type": "file",
                  "rundb_schema": {"action": "", "inputs": [], "outputs": [], "cfgs": [], "start": "", "end": "", "rc": 0, "uhash": ""},
                  "rundb_hash": "sha256",
                  "dateformat": "%m/%d/%Y %I:%M:%S %p",
                  "default_pinfile": "PinFile",
                  "external_providers_path": "%(default_config_path)s/linchpin-x",
                  "use_rundb_for_actions": "False",
                  .. snip ..
              }
          },
          {
              "evars": {
                  "inventory_file": "/home/herlo/lp-workspace/inventories/dummy-new-f935.inventory"
                  .. snip ..
              }
          },
          {
              "user": {
                  "x": "y"
              }
          }
      ]
  
  The purpose of the `magics` and `evars` sections is fairly clear. The `user`
  sub-section is less clear at this time, but will likely allow overriding of
  items in the `evars`.
  
  .. note:: A user can now add a 'vars' section to a target within the PinFile.
     However, data is currently only stored in the RunDB, and not used elsewhere
     at this point.
  
  .. code-block:: yaml
  
      dummy-new:
        topology: dummy-new.yml
        layout: dummy-new.yml
        cfgs:
          'x': 'y'
