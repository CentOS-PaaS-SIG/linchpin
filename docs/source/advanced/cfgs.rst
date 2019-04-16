PinFile Configs
===============

You can use the cfgs section of the PinFile to define variables for use in inventories.  These variables map to values in the json returned by the relevant provider, and are dot-separated.  For example, the variable __IP__ in the cfgs below would map to the address 55.234.16.11 in the following json:

.. code-block:: json

   {
      'addresses': [
         {
            'public_v4': '55.234.16.11'
         },
         {
            'public_v4': '219.16.122.93'
         }
      ]
   }

.. code-block:: yaml

   cfgs:
     aws:
       __IP__: addresses.0.public_v4

Information on the json returned by different providers can be found below:

.. toctree::
   :glob:

   ../outputs/*
