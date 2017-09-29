

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.operations import add, delete
from tinydb.middlewares import CachingMiddleware

from linchpin.rundb.basedb import BaseDB


class TinyRunDB(BaseDB):

    def __init__(self, conn_str):
        self.name = 'TinyRunDB'
        self.conn_str = conn_str
        self.db = TinyDB(conn_str,
                         storage=CachingMiddleware(JSONStorage),
                         default_table='linchpin')

    def __str__(self):
        if self.conn_str:
            return "{0} at {1}".format(self.name, self.conn_str)
        return "{0} at {1}".format(self.name, 'None')

    def init_table(self, table, record_data):
        t = self.db.table(name=table)
        return t.insert(record_data)

    def update_record(self, table, run_id, key, value):
        t = self.db.table(name=table)
        return t.update(add(key, [value]), eids=[run_id])

    def remove_record(self, table, key, value):
        pass

    def search(self, table, key):
        t = self.db.table(name=table)
        if record_data:
            return t.search(record_data)
        return t.all()

    def query(self, table, query):
        pass

    def purge(self, table=None):
        if table:
            return self.db.purge_table(table)
        return self.db.purge_tables()

    def close(self):
        return self.db.close()


