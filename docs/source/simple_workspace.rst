Workspaces
==========

What is generated is commonly referred to as the :term:`workspace`. The workspace can live anywhere on the filesystem. The default is the current directory. The workspace can also be passed into the ``linchpin`` command line with the ``--workspace (--w)`` option, or it can be set with the ``$WORKSPACE`` environmental variable.

In our `simple` example, the workspaces is `/tmp/simple`.

A workspace requires only one file, the `PinFile`. This file is the cornerstone to LinchPin provisioning. It's a YAML file, written with declarative syntax. This means the `PinFile` is written to explain how things should be provisioned *after* running `linchpin up`.

Looking at the simple workspace, you'll see that it has a few other items.

.. code-block:: bash

    $ pwd
    /tmp/simple
    $ ls
    inventories  PinFile  PinFile.json  README.rst  resources

Ignoring everything but the `PinFile` for now, it's clear that other files and directories will exist in a workspace. Let's have a closer look at the components of a :doc:`simple_pinfile`.
