RunDB Drivers
================

Custom database drivers can be added to LinchPin.  LinchPin requires that these drivers contain certain functions in order to interface with the existing LinchPin code.


Existing Drivers
`````````````````

Currently, LinchPin supports two drivers.

TinyDB
------
This is the default database driver for LinchPin.  It has no exernal dependencies but cannot support reading and writing from multiple linchpin processes at the same time.  If you need this functionality, you should use another driver.


MongoDB
-------
This driver has the advantage of concurrency, but also requires a daemon in order to run.

Adding Custom Drivers
`````````````````````
All database drivers for LinchPin must extend the `linchpin.rundb.BaseDB` class and contain the following functions:

.. code:: python

    @schema.setter
    def schema(self, schema)

Sets the `schema` property for the class.  If your database requires a schema (such as MySQL), this is where you should set it.
 
.. code:: python

    def init_table(self, table)

Sets up the table for the current run of LinchPin.  Returns a run_id for the next run.  `run_id` is a variable used to identify a document in the RunDB.  It begins at 1 and increments from there.

.. code:: python

    def update_record(self, table, run_id, key, value)

updates a single record in the database.  Note that the "outputs" record is a list containing two items: a dict in the format of `{ "resources": [] }` and another one in the format of `{ "inventory_path": [] }`.  If a resources dict is passed to `update_record()`, the array needs to be appended to the existing resources array.  If the driver supports concurrent transactions, care must be taken to avoid race conditions.

.. code:: python

    def get_tx_record(self, tx_id)

Retrieves a single transaction record for the rundb. A transaction record contains a list of the targets provisioned, their uhashes and their return codes.  It does not contain the topology, layouts, or outputs from the cloud.  

.. code:: python

    def get_tx_records(self, tx_ids)

Gets multiple records corresponding with a list of transaction ids.

.. code:: python

    def get_run_id(self, table, action='up')

Returns the id corresponding with the most recent instance of the given action.

.. code:: python

    def get_record(self, table, action=None, run_id=None)

Returns a single record.  If a run_id is supplied, the record corresponding with the given run_id will be returned.  Else if an action is supplied, the most recent record corresponding with that action is supplied.

.. code:: python

    def get_records(self, table, count=10)

Returns the `count` most recent records.

.. code:: python

    def get_tables(self)

Returns a list of tables.

.. code:: python

    def remove_record(self, table, key)

Removes a record from the rundb

.. code:: python

    def purge(self, table)

Deletes a single database

In addition, the functions that use the database use the @usedb decorator, which opens the database, performs the operation, and closes it again

.. code:: python

    def usedb(func):
        def func_wrapper(*args, **kwargs):
            args[0]._opendb()
            x = func(*args, **kwargs)
            args[0]._closedb()
            return x
        return func_wrapper

