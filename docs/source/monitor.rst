Monitor and Progress Bar
===========================

Linchpin execution of Ansible is mostly a black box, where Ansible receives
input from Linchpin and returns expected output. The output is received in
a form of files and database changes. However, in version 1.9.1 there was
another channel of communication was created, a message bus. Before version
1.9.1, Linchpin was calling Ansible in a synchronize mode, that is once Ansible
was called, Linchpin was waiting for it to finish the execution. To support
progress bar, ZMQ message bus and multiprocessing was added. From version
1.9.1, Linchpin by default runs Ansible in multiprocess with a "monitoring"
process. The ZMQ message bus was added to Ansible using plugins, and to the
monitoring process. That means that Ansible, on different events or steps will
able to communicate with Linchpin. For progress bar it meant that Ansible could
update Linchpin with its progress in details, which allows better user
experience and understanding of deployment or tear down progress. The new
functionality is limited to provisioning process ('up' and 'destroy') and can
be disabled or limited with options --no-monitor or --no-progress:

--no-monitor will disable multiprocessing entirely and thus also disables the
progress bar.

--no-progress will cancel the progress bar which could be helpful in shell
scripts or in CI, but the monitoring/multiprocessing remains.

Examples:

::

   # Linchpin runs with multiprocessing and progress bar enabled
   linchpin up

   # Linchpin runs in verbose mode, progress bar disabled
   linchpin -vvvv up

   # Linchpin runs with disabled multiprocessing and without progress bar
   linchpin --no-monitor up

   # Linchpin runs without progress bar but with multiprocessing
   linchpin up --no-progress

The progress bar and multiprocessing can be disabled via linchpin.conf
settings file:

::

   [progress_bar]
   no_progress = True

   [monitor]
   no_monitor = True
