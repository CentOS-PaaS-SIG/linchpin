LinchPin Unit Testing
---------------------

Setup and Teardown functions for each test function
- @with_setup() decorator

Running the Tests
++++++++++++++++++

To run all tests:

.. code:: bash
   pip install -e .[tests]
   python setup.py test

To run an individual test:

.. code:: bash
   nosetests -vv -s path/to/tests:ClassName.test_method

Class name and test_method are optional.  The following are all valid parameters:

.. code:: bash
   nosetests -vv -s linchpin/tests/cli
   nosetests -vv -s lincpin/tests/cli/test_context_pass.py
   nosetests -vv -s linchpin/tests/cli/test_contet_pass.py:test_context_create

Creating tests
++++++++++++++

Each file should have a test_{filename}_pass.py and test_{filename}_fail.py
associated with it.  Each function should be tested at least once in its
respective test file.

We use Pytest and Nose to run tests.  Nose provides us with powerful assertions
and, unlike unittest, does not require us to create classes for our tests.
Pytest is used as a werapper around the tests. Test are run through Pytest,
which allows Nose to be swapped out for another unit testing framework.

You can use the @with_setup() decorator to add setup and teardown functions to
each test
