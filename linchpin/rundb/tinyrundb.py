from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.operations import add
from tinydb.middlewares import CachingMiddleware

from .basedb import BaseDB


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
        return t.update(add(key, value), eids=[run_id])


    @usedb
    def get_tx_record(self, tx_id):

        t = self.db.table(name='linchpin')
        return t.get(eid=tx_id)


    @usedb
    def get_tx_records(self, tx_ids):

        txs = {}
        t = self.db.table(name='linchpin')
        for tx_id in tx_ids:
            txs[tx_id] = t.get(eid=tx_id)

        return txs


    @usedb
    def get_record(self, table, action='up', run_id=None):

        t = self.db.table(name=table)
        if not run_id:
            run_id = len(t.all())
            if not run_id:
                return (None, 0)

            for rid in range(int(run_id), 0, -1):
                record = t.get(eid=int(rid))
                if record and record['action'] == action:
                    return (record, int(rid))
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
                end = start - count

                for i in xrange(start, end, -1):
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
