The following settings are in the ``[logger]`` section of the linchpin.conf.

.. note:: These settings are ONLY used for the Command Line Interface. The API
   configures a console output only logger and expects the functionality to be
   overwritten in subclasses.

enable
~~~~~~

Whether logging to a file is enabled

.. code-block:: cfg

    enable = True

file
~~~~

Name of the file to write the log. A relative or full path is acceptable.

.. code-block:: cfg

    file = linchpin.log

format
~~~~~~

The format in which logs are written.
See `https://docs.python.org/2/library/logging.html#logrecord-attributes`
for more detail and available options.

.. code-block:: cfg

    format = %%(levelname)s %%(asctime)s %%(message)s


dateformat
~~~~~~~~~~

How to display the date in logs.
See `https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior`
for more detail and available options.

.. note:: This action was never implemented.

.. code-block:: cfg

    dateformat = %%m/%%d/%%Y %%I:%%M:%%S %%p

level
~~~~~

Default logging level

.. code-block:: cfg

    level = logging.DEBUG

The following settings are in the ``[console]`` section of the linchpin.conf.

Each of these settings is for logging output to the console, except for Ansible
output.

format
~~~~~~

The format in which console output is written.
See `https://docs.python.org/2/library/logging.html#logrecord-attributes`
for more detail and available options.

.. code-block:: cfg

    format = %%(message)s


level
~~~~~

Default logging level

.. code-block:: cfg

    level = logging.INFO

