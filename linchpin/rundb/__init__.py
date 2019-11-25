from __future__ import absolute_import

from abc import ABCMeta, abstractmethod
import six


def usedb(func):
    def func_wrapper(*args, **kwargs):
        args[0]._opendb()
        x = func(*args, **kwargs)
        args[0]._closedb()
        return x
    return func_wrapper


class RunDB(six.with_metaclass(ABCMeta, object)):

    @abstractmethod
    def init_table(self, table):
        return self.driver.init_table(table)

    @abstractmethod
    def update_record(self, table, run_id, key, value):
        return self.driver.update_record(table, run_id, key, value)

    @abstractmethod
    def get_tx_record(self, table, tx_id):
        return self.driver.get_tx_record(table, tx_id)

    def get_tx_records(self, table, tx_ids):
        return self.driver.get_tx_records(table, tx_ids)

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
