The ``linchpin fetch`` command provides a simple way to access a resource from
a remote location. One could simply perform a `git clone`, or use `wget` to
download a ``workspace``. However, ``linchpin fetch`` makes this process
simpler, and includes some tooling to make the workflow smooth.

.. code-block:: bash

    $ linchpin fetch --help
    Usage: linchpin fetch [OPTIONS] REMOTE

      Fetches a specified linchpin workspace or component from a remote location

    Options:
      -t, --type TYPE              Which component of a workspace to fetch.
                                   (Default: workspace)
      -r, --root ROOT              Use this to specify the location of the
                                   workspace within the root url. If root is not
                                   set, the root of the given remote will be used.
      --dest DEST                  Workspaces destination, the fetched workspace
                                   will be relative to this location. (Overrides
                                   -w/--workspace)
      --branch REF                 Specify the git branch. Used only with git
                                   protocol (eg. master).
      --git                        Remote is a Git repository (default)
      --web                        Remote is a web directory
      --nocache                    Do not check the cached time, just copy the
                                   data to the destination
      -h, --help                   Show this message and exit.
