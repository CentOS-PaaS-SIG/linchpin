from abc import ABCMeta, abstractmethod

# this needs an key/value for 'action' (up/destroy added at runtime)
DB_SCHEMA = {'inputs': [], 'outputs': []}

class RunDB(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def init_table(self, table, record_data):
        return self.driver.init_table(table, record_data)

    @abstractmethod
    def update_record(self, table, run_id, key, value):
        return self.driver.update_record(table, run_id, key, value)

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

    @abstractmethod
    def close(self):
        return self.driver.close()

