#!/usr/bin/env python

from __future__ import absolute_import
import sys

from . import usedb
from .basedb import BaseDB

if sys.version_info[0] == 3:
    from pymongo import MongoClient, DESCENDING



class MongoDB(BaseDB):

    def __init__(self, conn_str):
        self.name = 'MongoDB'
        self.conn_str = conn_str
        self.default_table = 'linchpin'


    def _opendb(self):
        self.client = MongoClient(self.conn_str)
        self.db = self.client['linchpin']

    def _closedb(self):
        # also flush the stored data to mongodb
        pass

    @property
    def schema(self):
        return self._schema


    @schema.setter
    def schema(self, schema):
        self._schema = dict()
        self._schema.update(schema)


    @usedb
    def init_table(self, table):
        table = self.db[table]
        prev_run = table.find_one(sort=[('_id', DESCENDING)])
        if prev_run:
            return prev_run['_id'] + 1
        return 1


    @usedb
    def update_record(self, table, run_id, key, value):
        collection = self.db[table]

        result = None
        if key == 'outputs' and 'resources' in value[0].keys():
            result = self._update_outputs(collection, run_id, key, value)
            if result:
                return result
        if type(self._schema[key]) == list:
            if isinstance(value, list):
                result = collection.find_one_and_update({'_id': run_id},
                                                        {'$addToSet':
                                                            {key: {'$each':
                                                                   value}}},
                                                        upsert=True)
            else:
                result = collection.find_one_and_update({'_id': run_id},
                                                        {'$addToSet': {key:
                                                                       value}},
                                                        upsert=True)
        else:
            result = collection.find_one_and_update({'_id': run_id},
                                                    {'$set': {key: value}},
                                                    upsert=True)

        # find_one_and_update() returns the document before the update
        # if the value is the same, we return None (to signify no change)
        # else we return the document
        if result and result.get(key, None) == value:
            return None
        return result


    def _update_outputs(self, collection, run_id, key, value):
        val = []
        for v in value:
            if type(v['resources']) == list:
                val.extend(v['resources'])
            else:
                val.append(v['resources'])
        return collection.find_one_and_update({'_id': run_id,
                                              'outputs.resources':
                                                  {'$exists': True}},
                                              {'$push': {"outputs.$.resources":
                                                         {'$each': val}}})



    @usedb
    def get_tx_record(self, table, tx_id):
        table = self.db[table]

        return table.find_one({'_id': tx_id})


    @usedb
    def get_tx_records(self, table, tx_ids):
        table = self.db[table]

        txs = {}
        for tx_id in tx_ids:
            txs[tx_id] = table.find_one({'_id': tx_id})

        return txs


    @usedb
    def get_run_id(self, table, action='up'):
        table = self.db[table]

        record = table.find_one({'action': action}, sort=[('_id', DESCENDING)])
        if record:
            return record['_id']


    @usedb
    def get_record(self, table, action=None, run_id=None):
        table = self.db[table]

        record = None

        if run_id:
            record = table.find_one({'_id': int(run_id)})
        if action:
            record = table.find_one({'action': action},
                                    sort=[('_id', DESCENDING)])
        else:
            record = table.find_one(sort=[('_id', DESCENDING)])

        if record:
            run_id = run_id if run_id else record['_id']
            return (record, run_id)
        return (None, 0)


    @usedb
    def get_records(self, table, count=10):
        table = self.db[table]

        if count == 'all':
            return table.find().sort(DESCENDING)
        return list(table.find(limit=count, sort=[('_id', DESCENDING)]))


    @usedb
    def get_tables(self):
        return self.db.list_collection_names()


    def remove_record(self, table, key, value):
        pass


    @usedb
    def search(self, table, key=None):
        table = self.db[table]

        if key:
            return table.find({key: {"$exists": True}})
        return table.find()


    def query(self, table, query):
        pass


    @usedb
    def purge(self, table):
        table = self.db[table]
        table.purge()
