Inventory Layouts (or just :term:`layout`) describe what an Ansible
inventory might look like after provisioning. A layout is needed
because information about the resources provisioned are unknown in advance.

Layouts, like topologies and PinFiles are processed top to bottom according
to the file.

YAML
````
Layouts written using YAML format:

  * :docs1.5:`aws-ec2.yml <workspace/layouts/aws-ec2.yml>`
  * :docs1.5:`dummy-new.yml <workspace/layouts/dummy-new.yml>`

JSON
````

New in version 1.5.0

Layouts can be written using JSON format.

  * :docs1.5:`gcloud.json <workspace/layouts/gcloud.json>`

Jinja2
``````

New in version 1.5.0

Topologies can be processed as templates using Jinja2.

Dummy Template
~~~~~~~~~~~~~~

This layout template would be processed with a dictionary containing one
key named `node_count`.

  * :docs1.5:`dummy.json <workspace/layouts/dummy.json>`

The PinFile.dummy.json contains the reference to the `dummy.json` layout.

.. code-block:: yaml

    {
        "dummy": {
            "topology": "dummy.json",
            "layout": "dummy.json"
        }
    }

.. seealso:: :docs1.5:`PinFile.dummy.json <workspace/PinFile.dummy.json>`

.. code-block:: bash

    $ linchpin -p PinFile.dummy.json --template-data '{ "node_count": 2 }' up

Advanced layout examples can be found by reading :ref:`ra_inventory_layouts`.
