Some providers require additional dependencies installed on the system running linchpin. Use ``linchpin setup`` to setup the given provider(s) properly.

If a list of providers is ommitted, then it will install dependencies for all providers that need so.

In case you execute ``linchpin setup`` with a user not allowed to install packages, then pass the `--ask-sudo-pass` option to prompt for the sudo password.
