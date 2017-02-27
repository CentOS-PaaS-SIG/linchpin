Linch-Pin Contributions Welcome
-------------------------------

Thank you for desiring to provide contributions to the Linch-Pin project.
This handy guide should provide simple guidelines for getting started,
submitting a patch, etc.

Any questions regarding this guide, or in general? Please feel free to
`file an issue <https://github.com/CentOS-PaaS-SIG/linch-pin/issues>`_.

Cloning the Repository
++++++++++++++++++++++

To start contributing to the Linch-Pin project, please fork the repository.
Documentation for forking can be found `here
<https://help.github.com/articles/fork-a-repo/>`_.

This should generate a forked repository with a format similar to
``https://github.com/<github-username>/linch-pin``.

Once the fork has been created, clone the repository onto a development machine.

.. code-block:: bash

    $ cd ~/sandbox

    $ git clone git@github.com:<github-username>/linch-pin.git
    or
    $ git clone https://github.com/<github-username>/linch-pin

    $ cd linch-pin
    $ git branch
    * develop

It should be immediately apparent that code is in the developer mode. This is
indicative of the ``develop`` branch. Once cloned, an additional remote will
need to be added.

.. code-block:: bash

    $ pwd
    ~/sandbox/linchpin
    $ git remote add upstream git://github.com/CentOS-PaaS-SIG/linch-pin.git
    $ git remote -v
    origin  git@github.com:herlo/linch-pin.git (fetch)
    origin  git@github.com:herlo/linch-pin.git (push)
    upstream    git://github.com/CentOS-PaaS-SIG/linch-pin.git (fetch)
    upstream    git://github.com/CentOS-PaaS-SIG/linch-pin.git (push)

Having two remotes makes rebasing upstream changes much easier. How to pull in
changes from upstream will be covered later in this document. Additionally,
the upstream repository is a read-only repository (indicated by git://).

Make a Change
+++++++++++++

To make a change to linch-pin, it is recommended to create a feature branch.
In this way, each feature can track its changes and not conflict with others.

.. code-block:: bash

    $ git checkout -b contributing_docs
    Switched to a new branch 'contributing_docs'
    $ git push -u origin contributing_docs
    Total 0 (delta 0), reused 0 (delta 0)
    To github.com:herlo/linch-pin.git
     * [new branch]      contributing_docs -> contributing_docs
    Branch contributing_docs set up to track remote branch contributing_docs from origin.

.. note:: the ``-u`` option. This is a nicety of git, allowing future pushes
    to assume the remote ``origin`` and the branch ``contributing_docs``.

Once the feature branch is created, development work continues as normal.
After some code has been created, edited, or removed, please commit this work.

.. code-block:: bash

    $ 

It is considered useful to commit often. Usually small bits of work are easier to
revert than large swaths of code across multiple files.


Submit a Pull Request
+++++++++++++++++++++


Rebase from Upstream
++++++++++++++++++++


