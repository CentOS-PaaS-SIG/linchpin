LinchPin Command Line Shell implementation
=========================================

The linchpin.shell module contains calls to implement the Command Line
Interface within linchpin. It uses the `Click <http://click.pocoo.org>`_
command line interface composer. All calls here interface with the
:doc:`libcli` API.

.. automodule:: linchpin.shell
    :members:
    :undoc-members:
    :exclude-members: main,help,_handle_results,runcli

.. autofunction:: init
.. autofunction:: up
.. autofunction:: destroy
.. autofunction:: fetch
.. autofunction:: journal

.. automodule:: linchpin.shell.default_group
    :members:

