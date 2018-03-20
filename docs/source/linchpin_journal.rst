.. _cli_journal:

linchpin journal
----------------

Upon completion of any provision (up) or teardown (destroy) task, there's a record that is created and stored in the :term:`RunDB`. The ``linchpin journal`` command displays data about these tasks.

.. code-block:: bash

    $ linchpin journal --help
    Usage: linchpin journal [OPTIONS] TARGETS

      Display information stored in Run Database

      view:       How the journal is displayed

                  'target': show results of transactions on listed targets
                  (or all if omitted)

                  'tx': show results of each transaction, with results
                  of associated targets used

      (Default: target)

      count:      Number of records to show per target

      targets:    Display data for the listed target(s). If omitted, the latest
      records for any/all targets in the RunDB will be displayed.

      fields:     Comma separated list of fields to show in the display.
      (Default: action, uhash, rc)

      (available fields are: uhash, rc, start, end, action)

    Options:
      --view VIEW          Type of view display (default: target)
      -c, --count COUNT    (up to) number of records to return (default: 3)
      -f, --fields FIELDS  List the fields to display
      -h, --help           Show this message and exit.

There are two specific ways to view the data using the journal, by 'target' and 'transactions (tx)'.

Target
======

.. include:: includes/journal_target.rst

Transactions
============

.. include:: includes/journal_tx.rst

