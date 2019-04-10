Some :doc:`providers` require authentication to acquire
:ref:`managing_resources`. LinchPin provides tools for these providers to
authenticate. The tools are called credentials.

Credentials
```````````

Credentials come in many forms. LinchPin wants to let the user control how the
credentials are formatted. In this way, LinchPin supports the standard
formatting and options for a provider. The only constraints that exist are how
to tell LinchPin which credentials to use, and where they credentials data
resides. In every case, LinchPin tries to use the data similarly to the way
the provider might.

.. include:: credentials/aws.rst




