Linchpin Hooks CLI (Options)
============================

By default, hooks run as a part of the provisioning process.
Hooks are executed in the following order:
1. preup
2. postup
3. predestroy
4. postdestroy

Since each state can have multiple hooks defined hooks linchpin provisioning process can be affected by success and failure of hook.
By default, whenever there is any failure in execution of hook the provisioning process aborts. However, this behaviour can be defined changed by two command line options --ignore-failed-hooks and --no-hooks

--ignore-failed-hooks on enabling this option the failure of hooks does not affect the provisioning process. If provisioning is successful linchpin exits with 0

--no-hooks Allows user to skip the execution of hooks

Usage:

::

  linchpin -vvvv --creds-path ./credentials/ up --no-hooks

  linchpin -vvvv --creds-path ./credentials/ destroy --no-hooks

  linchpin -vvvv --creds-path ./credentials/ up --ignore-failed-hooks

  linchpin -vvvv --creds-path ./credentials/ destroy --ignore-failed-hooks

Further, the above mentioned options can be configured permanently in hookflags section of linchpin.conf

::

  [hookflags]
  no_hooks = False
  ignore_failed_hooks = False

