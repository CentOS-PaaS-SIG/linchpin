Getting Started
===============

.. contents:: Topics

.. _foreword:

Foreword
````````

Once linch-pin is installed, according to the directions in :doc:`intro_installation`, it is time to become familiar with how it is used.


.. _understanding_terminology:

Terminology
```````````

Linchpin makes use of a number of broad concepts it hopes are familiar enough to unify thinking and rationale surrounding collections of
systems in a variety of cloud, self-hosted, and local environments. Some of the more important terms are explained below

Topology
--------

A topology is the term given, in linchpin, to a file that specifies the set of resources that ought to be provisioned in each of the various
environments. A topology file is a YAML-formatted file (which means it can also be in JSON format, as JSON is a strict subset of YAML) which
includes the definitions of all the resources to provision.

Credentials
-----------

Many of the environments where systems can be hosted require some form of authentication. This could be a username and password, an SSH key,
an existing Kerberos certificate, or some other system. Each environment will have its own method for configuring and passing in these
credentials. Look into each particular environment's specific documentation for a discussion on configuring any needed credentials prior to
provisioning resources from it.

Layout
------

A layout is a set of optinos which maps the generated hosts in an environment to output variables and inventory groups when generating out
the resulting inventory hosts.
