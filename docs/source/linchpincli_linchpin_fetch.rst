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

+--------------------------------------------------+--------------------------------------------------------------------------+
| Usage                                            | Action                                                                   |
+==================================================+==========================================================================+
| linchpin fetch <url>| Fetches workspace and puts into current working workspace|
+--------------------------------------------------+--------------------------------------------------------------------------+
| linchpin fetch topology <url>  | Fetches topology from the url and puts it into the current workspace |
+--------------------------------------------------+--------------------------------------------------------------------------+
| linchpin fetch <url> -r ws1,ws2                  | Fetches workspace from the specified url and goes to the subdirectories 'ws1' and 'ws2' and copies them into the workspace|
+--------------------------------------------------+--------------------------------------------------------------------------+
