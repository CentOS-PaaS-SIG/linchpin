LinchPin Command-Line API
==========================

The linchpin.cli module provides an API for writing a command-line interface,
the :doc:`libshell` being the reference implementation.

.. automodule:: linchpin.cli

.. autoclass:: LinchpinCli

  .. automethod:: __init__
  .. automethod:: lp_up
  .. automethod:: lp_destroy
  .. automethod:: lp_down
  .. automethod:: run_playbook
  .. automethod:: find_topology
  .. automethod:: get_cfg
  .. automethod:: set_cfg
  .. automethod:: get_evar
  .. automethod:: set_evar
  .. automethod:: set_magic_var

  .. -- deprecated methods --

  .. automethod:: lp_rise
  .. automethod:: lp_drop

.. automodule:: linchpin.cli.context
    :members:
    :undoc-members:
    :inherited-members:
