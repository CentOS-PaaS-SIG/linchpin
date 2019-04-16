Developing LinchPin
===================

.. _gs_foreword:

This guide will walk you through the basics of contributing to LinchPin.

.. toctree::
   :maxdepth: 1

.. contents:: Topics

.. _gs_developing:

Checking out the linchpin code
------------------------------

You can check out the linchpin code by cloning the git repository from github.  

.. code-block:: bash

   $ git clone https://github.com/CentOS-PaaS-SIG/linchpin.git

But to submit pull requests (PR's) you will need to fork the project on github webui first.
Then you can add a remote for that fork.  This is where you will push your changes.

.. code-block:: bash

   $ git remote add myfork git@github.com:<YOUR_GITHUB_USERNAME>/linchpin.git

Remember to replace <YOUR_GITHUB_USERNAME> with your actual github login.

Working on a feature or bug
---------------------------

All new work happens off the develop branch.  It is good practice to make sure you have
the latest version before starting work on your changes.

.. code-block:: bash

   $ git checkout develop
   $ git pull

Now that you are in the develop branch and have the latest version you can create a new
branch to use for your changes.

.. code-block:: bash

   $ git checkout -b <DESCRIPTIVE_BRANCH_NAME>

Replace <DESCRIPTIVE_BRANCH_NAME> with a branch name that makes sense.  This name will show up
in your github fork branches.

Creating a Pull Request
-----------------------

After you have committed your changes and tested them locally you can push them to your github fork repo.

.. code-block:: bash

   $ git pull --rebase origin develop
   $ git push myfork <DESCRIPTIVE_BRANCH_NAME>:<DESCRIPTIVE_BRANCH_NAME>
   Enumerating objects: 1014, done.
   Counting objects: 100% (768/768), done.
   Delta compression using up to 8 threads
   Compressing objects: 100% (290/290), done.
   Writing objects: 100% (634/634), 83.86 KiB | 6.99 MiB/s, done.
   Total 634 (delta 462), reused 436 (delta 324)
   remote: Resolving deltas: 100% (462/462), completed with 84 local objects.
   remote:
   remote: Create a pull request for 'devel_docs' on GitHub by visiting:
   remote:      https://github.com/<YOUR_GITHUB_USERNAME>/linchpin/pull/new/devel_docs
   remote:
   To github.com:<YOUR_GITHUB_USERNAME>/linchpin.git
    * [new branch]        devel_docs -> devel_docs

The remote output explains how you can create a pull request by following the url referenced.  Again,
<YOUR_GITHUB_USERNAME> will match your github username.

Once a pull request has been created the automated testing will kick off automatically.  There is
upstream testing which is run on publicly accessable servers and there is downstream testing which
is run inside Red Hat.  We try to do most testing upstream since this in an open source project,
but some of the providers are only available inside Red Hat.

The upstream testing is referenced from the All checks section.  Downstream testing is recorded
as a comment.

If for some reason you need to kick off the testing again you can add a comment with the keyword
[test] in it.  It has to be inside the square brackets in order to trigger.

Depending on your contribution status your PR may not kick off automated testing and will require
someone from the project to initiate the testing.

You can request reviewers at this point and depending on the files that have been changed github
may suggest some reviewers based on who last changed that code.

Updating a Pull Request
-----------------------

If changes are required for your PR then please amend to your commit and force push.
If other commits have been merged into develop since you started your PR you may need
to rebase your PR on the latest code.  One reason for this is if changes to the automated
testing infrastructure have been made.

.. code-block:: bash

   $ git add -u
   $ git commit --amend
   $ git pull --rebase origin develop
   $ git push myfork --force <DESCRIPTIVE_BRANCH_NAME>:<DESCRIPTIVE_BRANCH_NAME>

Merging a Pull Request
----------------------

When all the tests are passing and the code has been approved by the reviewers you can merge the PR.
Don't use the merge button on github.  There is a workflow that does the merge which is triggered by
the comment [merge] in it.  Again, it has to be inside the square brackets in order to trigger.

The reason for this is we have containers used in the testing process which may need to be updated
depending on the code that is changed.  Our workflow will promote those containers and do the merge
on github.

Depending on your contribution status you may not have permission to do a merge.  In that case you
can leave a comment saying the PR is ready for merging.
