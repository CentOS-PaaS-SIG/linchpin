import abc

from . import RunDB

class BaseDB(RunDB):

    def __init__(self, driver, conn_str=None):

        self.name = 'BaseDB'
        self.conn_str = conn_str
        self.driver = driver(conn_str)

    def __str__(self):
        return self.driver.__str__()

    def add_record(self, table, record_data):
        return self.driver.add_record(table, record_data)

    def update_record(self, table, run_id, key, value):
        print('update_record: {}'.format(run_id))
        return self.driver.update_record(table, run_id, key, value)

    def remove_record(self, table, key, value):
        return self.driver.remove_record(table, key, value)

    def search(self, table, key):
        return self.driver.search(table, key)

    def query(self, table, query_info):
        return self.driver.query(table, query_info)

    def purge(self, table=None):
        return self.driver.purge(table)

    def close(self):
        return self.driver.close()
