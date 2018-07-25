Linchpin Container
==================

This document covers how to build and use the LinchPin container.

The LinchPin Container is built using the latest Fedora image (curently fedora:28).

Building the LinchPin Container image
-------------------------------------

Building the container with Docker requires the Docker daemon to be running. From within the linchpin directory:

.. code-block:: bash

    $ docker build -t linchpin .

Alternatively, install `buildah <https://github.com/projectatomic/buildah/blob/master/install.md>`_.

.. code-block:: bash

    $ sudo buildah bud -t linchpin .


Running the LinchPin Container image
------------------------------------

Docker can run the container

.. code-block:: bash

    $ docker pull contrainfra/linchpin
    .. snip ..
    $ docker run -v /path/to/workspace:/workdir -v /sys/fs/cgroup:/sys/fs/cgroup:ro --name linchpin contrainfra/linchpin -- linchpin -w /workdir up
    .. snip ..

Buildah can also run the container

.. code-block:: bash

    $ sudo buildah from contrainfra/linchpin
    linchpin-working-container
    $ sudo buildah run linchpin-working-container -v /path/to/workspace:/workdir -- linchpin -w /workdir up
    .. snip ..


Tips and Tricks
===============

* Setting the `CREDS_PATH` environment variable pointing the /workdir is recommended.
* AWS credentials could be passed as environment variables when the container is run, named `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID`.
* Beaker uses `kinit`, which is installed in the container but must be run within the container after it starts.
* The default /etc/krb5.conf for kerberos requires privilege escalation. This Dockerfile replaces it with a version that is modified in two ways:
  * `default_ccache_name` is commented out; this eliminates the need for privilege escalation and simply creates a cache in /tmp.
  * `default_realm` is defined; this is needed for some keytab types.
