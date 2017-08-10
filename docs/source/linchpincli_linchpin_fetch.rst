linchpin fetch
==============

Usage: ``linchpin fetch [OPTIONS] [FETCH_TYPE] REMOTE``

Fetches a specified linchpin workspace or component from a remote location

**Arguments**

``FETCH_TYPE...``
    Specifies which component of a workspace the user wants to fetch. This can
    include `topology`, `layout`, `resources` and `hooks`. The user can also specify
    `workspace` or leave the field blank to fetch the entire workspace.

``REMOTE``
    This is the url or uri of the remote directory. The user should specify the
    root of the workspace that they are referring to. If the user cannot
    specify the root of the workspace, especially when referring to a git
    repository, the user should provide the cloning url to the git repository
    and use the --root option to specify where in the git repository the root
    of the workspace is.


**Options**

``-r, --root``
    If the url does not point to the root of the workspace, use this option to
    specify the root. If the user wants to fetch from multiple workspace, root
    may be used to specify multiple workspaces. See examples below.
``-h, --help``
    Print the help text for this command.

Examples
--------
+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Usage                                                 | Action                                                                                                                                                                                                                                                                         |
+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``linchpin fetch <url>``                              | Fetches the entire workspace directory and puts into the current local workspace.                                                                                                                                                                                              |
+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``linchpin fetch topology <url>``                     | Fetches the topologies directory from the url and puts it into the current workspace.                                                                                                                                                                                          |
+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``linchpin fetch layout <url> --root /workspace1``    | Fetches the layouts directory from the subdirectory 'workspace1' from the url provided                                                                                                                                                                                         |
|                                                       | *note: This is typically used if you cannot specify the root of the workspace by using the URL. It may be particularly helpful when using git repositories.                                                                                                                    |
+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``linchpin fetch <url> --root workspace1,workspace2`` | Fetches the entire workspace from the subdirectories workspace1 and workspace2 and puts into the current working directory. This may be useful if one directory contains multiple workspaces and the user would like to fetch all contents and put into one workspace locally. |
+-------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
