The following settings are in the ``[init]`` section of the linchpin.conf.

These settings specifically pertain to :doc:`../linchpin_init`, which stores
templates in the source code to generate a simple example workspace.

source
~~~~~~

Location of templates stored in the source code. The structure is built to
resemble the directory structure explained in :doc:`../linchpin_init`.

.. code-block:: cfg

    source = templates/

pinfile
~~~~~~~

Formal name of the :term:`PinFile <pinfile>`. Can be changed as desired.

.. code-block:: cfg

    pinfile = PinFile

