Common Workflows
================

.. __foreword:

Having a basic understanding of LinchPin is crucial to this section. Knowing
the basic :doc:`CLI <cli>` operations leads nicely into using LinchPin in powerful
ways.

.. toctree::
   :maxdepth: 1

.. contents:: Topics

.. _wf_fetch:

Using ``linchpin fetch``
------------------------

.. include:: includes/fetch.rst

Fetching a Remote Workspace
---------------------------

This document will cover how to use ``linchpin fetch`` to obtain a workspace
from both a git repository. An example for fetching an http workspace can be
found :doc:`here <fetch_http>`.

First, determine the destination. By default, the destination location
is the current working directory. In this guide, we'll use ``/tmp/workspaces``.

.. code-block:: bash

    $ mkdir /tmp/workspaces
    $ cd /tmp/workspaces

Using the simplest possible ``linchpin fetch`` command will fetch the
workspaces from `git://github.com/herlo/lp_test_workspace`.

.. code-block:: bash

    $ linchpin fetch git://github.com/herlo/lp_test_workspace
    destination workspace: /tmp/workspaces/

    $ pwd
    /tmp/workspaces
    $ ls -l
    total 4
    -rw-rw-r-- 1 herlo herlo 980 Sep  5 13:53 linchpin.log
    drwxrwxr-x 5 herlo herlo 140 Sep  5 13:54 multi-target
    drwxrwxr-x 2 herlo herlo  80 Sep  5 13:54 openstack
    drwxrwxr-x 3 herlo herlo 120 Sep  5 13:54 os-server-addl-vols

The directory structure of `<https://github.com/herlo/lp_test_workspace>`_
should match the local directory as shown above.

As can be easily seen, ``linchpin fetch`` performed a git clone. Then copied
all of the directories to the current directory. ``linchpin fetch`` assumes the
root of the repository is a workspace.

Additional Options
``````````````````

If pulling all workspaces was not the intended action, there are other useful
options. First, perform a little clean up.

.. code-block:: bash

    $ cd && rm -rf /tmp/workspaces  # remove the workspaces directory
    $ ls -l /tmp/workspaces
    ls: cannot access '/tmp/workspaces/': No such file or directory

.. note:: From here on in, this guide will use the LinchPin git repository.
          There are several :lp_dir:`workspaces <docs/source/examples/workspaces>`
          with useful use cases. Feel free to peruse them as desired. This guide
          will use these workspaces going forward.

To clone from a repository with multiple workspaces (eg. the linchpin
repository), a root must be specified. It is also recommended to use the
``--dest`` flag.

.. code-block:: bash

    $ linchpin fetch git://github.com/CentOS-PaaS-SIG/linchpin \
    > --root workspaces/simple --dest /tmp/workspaces
    Created destination workspace: /tmp/workspaces/simple

In this example, there are additional options. Let's cover them in
detail:

``--root ROOT``
    This is the root of the repository. Normally, the root of the repository
    is used. However, if the workspaces reside elsewhere (eg. workspaces),
    use this option.

``--dest DESTINATION``
    If the current working directory is not the desired location, use this
    option.

Performing a listing will show how these options affected the fetch.

.. code-block:: bash

    $ ls -R /tmp/workspaces/
    /tmp/workspaces/:
    simple

    /tmp/workspaces/simple:
    PinFile  README.rst

As expected, the ``simple`` root was pulled down, and placed inside the
``/tmp/workspaces`` directory on the local machine.

To have **all** workspaces copied into /tmp/workspaces, a change is needed.

.. code-block:: bash

    $ linchpin fetch git://github.com/CentOS-PaaS-SIG/linchpin \
    > --root workspaces --dest /tmp
    destination workspace: /tmp/workspaces

.. note:: An observant user will notice that the same destination was used.
          This is because ``linchpin fetch`` maps the ROOT to the destination
          automatically. This behavior can be adjusted by removing the --dest
          option and specifying --workspace instead.

Listing the files again reveals more workspaces.

.. code-block:: bash

    $ ls /tmp/workspaces/
    dummy-aws  dummy-two  os-server-addl-vols  random  simple

Take a moment and investigate each of these workspaces. 

Contents of a Workspace
-----------------------

Whether a workspace watch created, or pulled using ``linchpin fetch``, they
all have should some common components.

``README.rst``
    A short description of the purpose for (or use case) the workspace
``PinFile``
    A declarative file which indicates which resources should be provisioned,
    any inventory layout to be generated, hooks, and other configurations

.. note:: The ``PinFile`` can be in YAML, JSON format. It can also be a script
          that returns JSON to STDOUT

No other requirements are put on a workspace. However, there can be several
other files or directories. See :doc:`managing_resources` for more information.



