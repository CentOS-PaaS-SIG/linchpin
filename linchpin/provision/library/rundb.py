#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import ast
import json
from ansible.module_utils.basic import AnsibleModule
from abc import ABCMeta, abstractmethod
import six
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.operations import add
from tinydb.operations import set as tinySet
from tinydb.middlewares import CachingMiddleware
from six.moves import range


class RunDB(six.with_metaclass(ABCMeta, object)):

    @abstractmethod
    def init_table(self, table):
        return self.driver.init_table(table)

    @abstractmethod
    def update_record(self, table, run_id, key, value):
        return self.driver.update_record(table, run_id, key, value)

    @abstractmethod
    def get_tx_record(self, tx_id):
        return self.driver.get_tx_record(tx_id)

    def get_tx_records(self, tx_ids):
        return self.driver.get_tx_records(tx_ids)

    @abstractmethod
    def get_run_id(self, table, action='up'):
        return self.driver.get_run_id(table, action=action)

    @abstractmethod
    def get_record(self, table, action='up', run_id=None):
        return self.driver.get_record(table, action=action, run_id=run_id)

    @abstractmethod
    def get_records(self, table=[], count=10):
        return self.driver.get_records(table=table, count=count)

    @abstractmethod
    def get_tables(self):
        return self.driver.get_tables()

    @abstractmethod
    def remove_record(self, table, key, value):
        return self.driver.remove_record(table, key, value)

    @abstractmethod
    def search(self, table, key):
        return self.driver.search(table, key)

    @abstractmethod
    def query(self, table, query_info):
        return self.driver.query(table, query_info)

    @abstractmethod
    def purge(self, table=None):
        return self.driver.purge(table)


class BaseDB(RunDB):

    def __init__(self, driver, conn_str):

        self.name = 'BaseDB'
        self.conn_str = conn_str
        self.driver = driver(conn_str)

    def __str__(self):
        return self.driver.__str__()

    @property
    def schema(self):
        return self.driver.schema

    @schema.setter
    def schema(self, schema):
        self.driver.schema = schema

    def init_table(self, table):
        return self.driver.init_table(table)

    def update_record(self, table, run_id, key, value):
        return self.driver.update_record(table, run_id, key, value)

    def get_tx_record(self, tx_id):
        return self.driver.get_tx_record(tx_id)

    def get_tx_records(self, tx_ids):
        return self.driver.get_tx_records(tx_ids)

    def get_run_id(self, table, action='up'):
        return self.driver.get_run_id(table, action=action)

    def get_record(self, table, action='up', run_id=None):
        return self.driver.get_record(table, action=action, run_id=run_id)

    def get_records(self, table=[], count=10):
        return self.driver.get_records(table=table, count=count)

    def get_tables(self):
        return self.driver.get_tables()

    def remove_record(self, table, key, value):
        return self.driver.remove_record(table, key, value)

    def search(self, table, key):
        return self.driver.search(table, key)

    def query(self, table, query_info):
        return self.driver.query(table, query_info)

    def purge(self, table=None):
        return self.driver.purge(table)



def usedb(func):
    def func_wrapper(*args, **kwargs):
        args[0]._opendb()
        x = func(*args, **kwargs)
        args[0]._closedb()
        return x
    return func_wrapper


class TinyRunDB(BaseDB):

    def __init__(self, conn_str):
        self.name = 'TinyRunDB'
        self.conn_str = conn_str
        self.default_table = 'linchpin'


    def _opendb(self):
        self.middleware = CachingMiddleware(JSONStorage)
        self.middleware.WRITE_CACHE_SIZE = 500
        self.db = TinyDB(self.conn_str, storage=self.middleware,
                         default_table=self.default_table)


    def __str__(self):
        if self.conn_str:
            return "{0} at {2}".format(self.name, self.conn_str)
        return "{0} at {1}".format(self.name, 'None')


    @property
    def schema(self):
        return self._schema


    @schema.setter
    def schema(self, schema):
        self._schema = dict()
        self._schema.update(schema)


    @usedb
    def init_table(self, table):
        t = self.db.table(name=table)
        return t.insert(self.schema)


    @usedb
    def update_record(self, table, run_id, key, value):
        t = self.db.table(name=table)
        # get transaction record
        tx_rec = t.get(doc_id=run_id).get("outputs", [])
        if len(tx_rec) > 0 and isinstance(value, list):
            # fetch the resources dict, index
            # by filtering them from outputs list
            res_list = [(idx, x) for idx, x in enumerate(tx_rec)
                        if "resources" in x]
            if len(res_list) != 0:
                res_idx = res_list[0][0]
                resources = res_list[0][1]
                if "resources" in list(value[0].keys()):
                    de = resources["resources"]
                    for i in value[0]["resources"]:
                        de.append(i)
                    de = {"resources": de}
                    tx_rec[res_idx] = de
                    res = t.update(tinySet(key, [de]), doc_ids=[run_id])
                    return res
        return t.update(add(key, value), doc_ids=[run_id])


    @usedb
    def get_tx_record(self, tx_id):

        t = self.db.table(name='linchpin')
        return t.get(doc_id=tx_id)


    @usedb
    def get_tx_records(self, tx_ids):

        txs = {}
        t = self.db.table(name='linchpin')
        for tx_id in tx_ids:
            txs[tx_id] = t.get(doc_id=tx_id)

        return txs


    @usedb
    def get_run_id(self, table, action='up'):
        """
        gets the run_id associated with the most recent instance of `action`
        if there is no instance of action, returns the most recent run_id
        """
        t = self.db.table(name=table)
        run_id = len(t.all())

        for rid in range(int(run_id), 0, -1):
            record = t.get(eid=int(rid))
            if record and record['action'] == action:
                return rid
        return run_id


    @usedb
    def get_record(self, table, action='up', run_id=None):

        t = self.db.table(name=table)
        if not run_id:
            run_id = self.get_run_id(table, action)
            if not run_id:
                return (None, 0)
            record = t.get(eid=int(run_id))
            if record and record['action'] == action:
                return (record, int(run_id))
        else:
            record = t.get(eid=int(run_id))
            if record:
                return(record, int(run_id))

        return (None, 0)


    @usedb
    def get_records(self, table, count=10):
        records = {}
        if table in self.db.tables():
            t = self.db.table(name=table)
            if len(t.all()):
                start = len(t)
                if count == 'all':
                    end = 0
                else:
                    end = start - count
                for i in range(start, end, -1):
                    records[i] = t.get(doc_id=i)
        return records


    @usedb
    def get_tables(self):

        tables = self.db.tables()
        tables.remove(self.default_table)

        return tables


    def remove_record(self, table, key, value):
        pass


    def search(self, table, key=None):
        t = self.db.table(name=table)
        if key:
            return t.search(key)
        return t.all()


    def query(self, table, query):
        pass


    def purge(self, table=None):
        if table:
            return self.db.purge_table(table)
        return self.db.purge_tables()


    def _closedb(self):
        self.db.close()


DB_DRIVERS = {
    "TinyRunDB": TinyRunDB,
}


def get_all_drivers():
    return DB_DRIVERS

# ---- Documentation Start ----------------#


DOCUMENTATION = """
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
"""


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
            except Exception:
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


main()
