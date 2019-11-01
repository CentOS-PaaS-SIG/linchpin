from __future__ import absolute_import

from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.operations import add
from tinydb.operations import set as tinySet
from tinydb.middlewares import CachingMiddleware
from six.moves import range

from . import usedb
from .basedb import BaseDB


class TinyRunDB(BaseDB):

    def __init__(self, conn_str):
        self.name = 'TinyRunDB'
        self.conn_str = conn_str
        self.default_table = 'linchpin'


    def _opendb(self):
        self.middleware = CachingMiddleware(JSONStorage)
        self.middleware.WRITE_CACHE_SIZE = 4096
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
        changed = t.update(add(key, value), doc_ids=[run_id])
        return changed


    @usedb
    def get_tx_record(self, table, tx_id):

        t = self.db.table(name=table)
        return t.get(doc_id=tx_id)


    @usedb
    def get_tx_records(self, table, tx_ids):

        txs = {}
        t = self.db.table(name=table)
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
    def get_record(self, table, action=None, run_id=None):

        t = self.db.table(name=table)
        if run_id:
            record = t.get(eid=int(run_id))
            if record:
                return(record, int(run_id))
        if action:
            run_id = self.get_run_id(table, action)
            if not run_id:
                return (None, 0)
            record = t.get(eid=int(run_id))
            if record and record['action'] == action:
                return (record, int(run_id))
        else:
            record = t.get(doc_id=len(t))
            run_id = record['run_id']

        if record:
            return (record, int(run_id))
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
