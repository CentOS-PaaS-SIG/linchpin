#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import ast
import json

from ansible.module_utils.basic import AnsibleModule

from linchpin.rundb.basedb import BaseDB
from linchpin.rundb.drivers import DB_DRIVERS


# ---- Documentation Start ----------------#
DOCUMENTATION = '''
---
version_added: "0.1"
module: rundb
short_description: A run database for linchpin, though it
                   could be used for anything transactional
                   really.
description:
  - This module allows a user to store and retrive values.
options:
  db_type:
    description:
      Type of Database used
    required: false
    default: TinyRunDB
  conn_str:
    description:
      Connection string to the database, can be file or url
    required: true
  db_schema:
    description:
      Database schema to use when running operations.
      The schema is required for an 'init' operation.
    required: false
  operation:
    description:
      Operation being performed on the database
      Available operations: init, update, purge, search
    required: true
    default: update
  run_id:
    description:
      The run_id value describes the current transaction.
      The run_id is returned for an 'init' operation.
      The run_id is required for an 'update' operation.
    required: false
    default: None
  table: (aka target in linchpin)
    description:
      Name of the table to update in the database
    required: true
  action:
    description:
      Action being performed, up/destroy
    required: false
    default: up
  key:
    description:
      key for the db record
    required: true (except for init and purge operations)
  value:
    description:
      value for the db record. Must be a dictionary of values.
    required: true (except for init and purge operations)

example


requirements: [TinyDB (or your own database)]
author: Clint Savage - herlo@redhat.com
'''


def main():

    module = AnsibleModule(
        argument_spec=dict(
            db_type=dict(type='str', required=False, default='TinyRunDB'),
            conn_str=dict(type='str', required=True),
            operation=dict(choices=['init',
                                    'update',
                                    'purge',
                                    'get'],
                           default='update'),
            run_id=dict(type='int', required=False),
            table=dict(type='str', required=True),
            action=dict(type='str', required=False, default='up'),
            key=dict(type='str', required=False),
            value=dict(type='str', required=False),
        ),
    )
    db_type = module.params['db_type']
    conn_str = os.path.expanduser(module.params['conn_str'])
    table = module.params['table']
    action = module.params['action']
    op = module.params['operation']
    key = module.params['key']
    value = module.params['value']
    run_id = module.params['run_id']

    is_changed = False
    output = None
    try:
        rundb = BaseDB(DB_DRIVERS[db_type], conn_str=conn_str)

        val = value
        # if value looks like a dict it is a dict!
        if value and (value.startswith("{") or value.startswith("[")):
            try:
                val = json.loads(value)
            except Exception as e:
                try:
                    val = ast.literal_eval(value)
                except Exception as e:
                    module.fail_json(msg=e)

        if op in ['init', 'purge']:
            if op == "init":
                if val:
                    rundb.schema = val
                    output = rundb.init_table(table)
                else:
                    msg = ("'table' and 'value' required for init operation")
                    module.fail_json(msg=msg)
            if op == "purge":
                output = rundb.purge(table=table)

        elif op in ['update', 'get']:
            if op == "update":
                # idempotent update
                if run_id and key and val:
                    # get the record first
                    runid = int(run_id)
                    out = rundb.get_record(table,
                                           action=action,
                                           run_id=runid)
                    existing_val = out[0].get(key, "")
                    if existing_val == value:
                        is_changed = False
                    else:
                        output = rundb.update_record(table, runid, key, val)[0]
                else:
                    msg = ("'table', 'run_id, 'key', and 'value' required"
                           " for update operation")
                    module.fail_json(msg=msg)

            if op == "get":
                if key:
                    runid = None
                    if run_id:
                        runid = int(run_id)
                    if key == 'run_id':
                        output = rundb.get_record(table,
                                                  action=action,
                                                  run_id=runid)[1]

                    else:
                        record = rundb.get_record(table,
                                                  action=action,
                                                  run_id=runid)[0]

                        if key in record:
                            output = record.get(key)
                        else:
                            msg = "key '{0}' was not found in"
                            " record".format(key)
                            module.fail_json(msg=msg)
                else:
                    msg = "The 'key' value must be passed"
                    module.fail_json(msg=msg)

        else:
            msg = "Module 'action' required"
            module.fail_json(msg=msg)

        if output:
            is_changed = True

        module.exit_json(output=output, changed=is_changed)

    except Exception as e:
        module.fail_json(msg=str(e))


#
#            module.exit_json(output=output, changed=output)
#        except Exception as e:
#            module.fail_json(msg=str(e))
# ---- Import Ansible Utilities (Ansible Framework) -------------------#
main()
