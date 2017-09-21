LinchPin Contributions Welcome
-------------------------------

Thank you for desiring to provide contributions to the LinchPin project.
This handy guide should provide simple guidelines for getting started,
submitting a patch, etc.

Any questions regarding this guide, or in general? Please feel free to
`file an issue <https://github.com/CentOS-PaaS-SIG/linchpin/issues>`_.


Cloning the Repository
++++++++++++++++++++++

To start contributing to the LinchPin project, please fork the repository.
Documentation for forking can be found `here
<https://help.github.com/articles/fork-a-repo/>`_.

This should generate a forked repository with a format similar to
``https://github.com/<github-username>/linchpin``.

Once the fork has been created, clone the repository onto a development machine.

.. code-block:: bash

    $ cd ~/sandbox

    $ git clone git@github.com:<github-username>/linchpin.git
    or
    $ git clone https://github.com/<github-username>/linchpin

    $ cd linchpin
    $ git branch
    * develop

It should be immediately apparent that code is in the developer mode. This is
indicative of the ``develop`` branch. Once cloned, an additional remote will
need to be added.

.. code-block:: bash

    $ pwd
    ~/sandbox/linchpin
    $ git remote add upstream git://github.com/CentOS-PaaS-SIG/linchpin.git
    $ git remote -v
    origin  git@github.com:<github-username>/linchpin.git (fetch)
    origin  git@github.com:<github-username>/linchpin.git (push)
    upstream    git://github.com/CentOS-PaaS-SIG/linchpin.git (fetch)
    upstream    git://github.com/CentOS-PaaS-SIG/linchpin.git (push)

Having two remotes makes rebasing upstream changes much easier. How to pull in
changes from upstream will be covered later in this document. Additionally,
the upstream repository is a read-only repository (indicated by git://).


Make a Change
+++++++++++++

To make a change to linchpin, it is recommended to create a feature branch.
In this way, each feature can track its changes and not conflict with others.

.. code-block:: bash

    $ git checkout -b contributing_docs
    Switched to a new branch 'contributing_docs'
    $ git push -u origin contributing_docs
    Total 0 (delta 0), reused 0 (delta 0)
    To github.com:<github-user>/linchpin.git
     * [new branch]      contributing_docs -> contributing_docs
    Branch contributing_docs set up to track remote branch contributing_docs from origin.

.. note:: the ``-u`` option. This is a nicety of git, allowing future pushes
    to assume the remote ``origin`` and the branch ``contributing_docs``.

.. code-block:: bash

    $ git add CONTRIBUTING.rst
    $ git commit

On the ensuing editor screen, be clear and concise about what was committed.

Follow the guidance in the article by Chris Beams
`How to Write a Git Commit Message <https://chris.beams.io/posts/git-commit/>`_.

.. important:: It is recommended to avoid using the ``-m`` switch.

.. note:: It is considered useful to commit often. Usually small bits of work
    are easier to revert than large swaths of code across multiple files.

Once the feature branch is created, development work continues as normal.
After some code has been created, edited, or removed, please commit this work.


Testing
+++++++

Please test all commits before pushing.

1. make sure you have all the extras_require packages installed, as listed in `setup.py <https://github.com/CentOS-PaaS-SIG/linchpin/blob/develop/setup.py>`_

   * Specifically, one could perform ``pip install linchpin[tests]`` to install the requirements

2. From the repository-root, follow the ``install`` and ``script`` sections of `.travis.yaml <https://github.com/CentOS-PaaS-SIG/linchpin/blob/develop/.travis.yml>`_
3. The tests will have passed if all script commands exit with code 0


Submit a Pull Request
+++++++++++++++++++++

Once a set of commits for the feature have been completed and tested. It is time to
submit a Pull Request. Please follow the github article, `Creating a pull request
<https://help.github.com/articles/creating-a-pull-request/>`_.

Submit the Pull Request (PR) against the ``develop`` branch.

.. note:: The LinchPin project works from the ``develop`` branch. As features
    are completed toward the next release (currently `1.1.0,
    <https://github.com/CentOS-PaaS-SIG/linchpin/milestone/3>`_).

Once the PR is created, it will need to be reviewed, and CI automation testing
must be executed. It is possible that additional commits will be needed to
pass the tests, address issues in the PR, etc.

Once the PR is approved, it can be merged.

.. important:: Merging is the responsibility of the submitter. Please do this
    in a timely manner.


Rebase from Upstream
++++++++++++++++++++

After the PR is merged into the ``develop`` branch on github, it will be good
to rebase into the local ``develop`` branch on the developer's machine.

.. code-block:: bash

    $ git checkout develop
    $ git pull --rebase upstream develop
    From github.com:CentOS-PaaS-SIG/linchpin
     * branch            develop    -> FETCH_HEAD
    First, rewinding head to replay your work on top of it...
    Fast-forwarded develop to f7cd72f04ff9f03538c54c4f46e90344393613f0.

In some cases, there may be issues with rebasing. Usually because there is
an uncommitted, but changed file. Stash the changes, and rerun the pull.

.. code-block:: bash

    $ git stash
    Saved working directory and index state WIP on develop: b932757
    fixup contributing link to point to develop
    HEAD is now at b932757 fixup contributing link to point to develop

    $ git pull --rebase upstream develop
    From github.com:CentOS-PaaS-SIG/linchpin
     * branch            develop    -> FETCH_HEAD
    First, rewinding head to replay your work on top of it...
    Fast-forwarded develop to f7cd72f04ff9f03538c54c4f46e90344393613f0.

    $ git stash pop
    On branch develop
    Your branch up-to-date with 'origin/develop'.
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   AFILE.txt

    no changes added to commit (use "git add" and/or "git commit -a")
    Dropped refs/stash@{0} (6593564022ce350be91e44d71af2a16c0825524c)


Release Process
+++++++++++++++

To better familiarize contributors with the development model used by LinchPin,
the develop branch is used for both releases (using tags) and for forward looking
development.

A tag in the develop branch tracks what is currently in production and stable
(eg v1.0.1). The HEAD (or tip) of the develop branch tracks current and future
features. In the state as of 13 June 2017, the latest release tagged is v1.0.1.
The HEAD of develop is just beyond this tag, but is focused on releasing a
new 1.1.0 release.

As a release approaches, there will be three basic stages in develop.

#. New feature development, unstable development
#. Alpha versions, indicated by updating version.py (eg. 1.1.0a3). These updates are not ready for production, but are approaching stable. Generally this implies feature completeness, but not fully vetted, tested, etc.
#. Beta versions, indicated by updating version.py (eg. 1.1.0b2). These updates are very close to production. Once the release is stable, the beta (b2) will be removed from the version and a release will be created and announced.

Once a release tag is pushed to develop, it will be released to pypi,
followed (hopefully) with an RPM release.


Remove Feature Branch
+++++++++++++++++++++

If desired, one could remove the feature branch at this point. This can be
done because the code should be in the both the local and upstream
``develop`` branches.

.. code-block:: bash

    $ git branch
      contributing_docs
    * develop
    $ git branch -d contributing_docs
    Deleted branch contributing_docs (was e320607).
    $ git branch
    * develop

.. note:: Do not be in the branch when attempting the delete.

The above helps prune branches from the local git checkout. But it might also
be advantageous to remove the branches from the remote.

.. code-block:: bash

    $ git push origin :contributing_docs
    To github.com:<github-user>/linchpin.git
     - [deleted]         contributing_docs


