# This directory contains all of the unit tests for linchpin.  The file
# tree within here is idential to that of the linchpin package.  Each
# file has a corresponding test_<filename>_pass and test_<filename>_fail
# file.  So linchpin/cli/__init__.py is tested via tests/cli/test_init_pass.py
# and tests/cli/test_init_fail.py.  As the name implies, *_fail.py tests all
# cases that should fail.  This includes cases in which the function returns
# a return code that is greater than 0 or throws an error.  *_pass.py should
# include all other test cases.
#
# Within each file, any given function should have one or more test functions
# beginning with test_<function_name>.  So the _write_to_inventory() function
# may have a test named test_write_to_inventory().  The do_action() function may
# have a test case named test_do_action_up() and another named
# test_do_action_destroy().
#
# When writing tests, aim for 100% coverage, but also make sure that the tests
# are thorough.  If you run a function and don't check that it returns the
# value you expect, that code isn't being properly tested regardless of
# coverage
