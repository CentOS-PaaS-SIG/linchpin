from . import RunDB


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

    def get_record(self, table, action='up', run_id=None):
        return self.driver.get_record(table, run_id=run_id)

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
