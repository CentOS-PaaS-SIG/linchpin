The following settings are in the ``[playbooks]`` section of the linchpin.conf.

.. note:: The entirety of this section is removed in version 1.5.0+.
   The redesign of the LinchPin API now calls individual playbooks based
   upon the :term:`resource_group_type` value.

up
~~

Removed in version 1.5.0

Name of the playbook associated with the 'up' (provision) action

.. code-block:: cfg

    up = site.yml

destroy
~~~~~~~

Removed in version 1.5.0

Name of the playbook associated with the 'destroy' (teardown) action

.. code-block:: cfg

    destroy = site.yml

down
~~~~

Removed in version 1.5.0

Name of the playbook associated with the 'down' (halt) action

.. note:: This action has not been implemented.

.. code-block:: cfg

    down = site.yml

schema_check
~~~~~~~~~~~~

Removed in version 1.5.0

Name of the playbook associated with the 'schema_check' action.

.. note:: This action was never implemented.

.. code-block:: cfg

    schema_check = schemacheck.yml

inv_gen
~~~~~~~

Removed in version 1.5.0

Name of the playbook associated with the 'inv_gen' action.

.. note:: This action was never implemented.

.. code-block:: cfg

    inv_gen = invgen.yml

test
~~~~

Removed in version 1.5.0

Name of the playbook associated with the 'test' action.

.. note:: This action was never implemented.

.. code-block:: cfg

    test = test.yml
