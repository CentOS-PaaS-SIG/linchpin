YAML
````
These PinFiles represent many combinations of complexity and providers.
All are written using JSON format.


    :docs1.5:`workspace/PinFile.dummy.yml`
    :docs1.5:`workspace/PinFile.openstack.yml`
    :docs1.5:`workspace/PinFile.complex.yml`

The combined format is only available in v1.5.0+

    :docs1.5:`workspace/PinFile.combined.yml`

JSON
````

New in version 1.5.0

These PinFiles represent many combinations of complexity and providers.
All are written using JSON format.

    :docs1.5:`workspace/PinFile.dummy.json`
    :docs1.5:`workspace/PinFile.aws.json`
    :docs1.5:`workspace/PinFile.duffy.json`
    :docs1.5:`workspace/PinFile.combined.json`
    :docs1.5:`workspace/PinFile.complex.json`

Jinja2
``````

New in version 1.5.0

These PinFiles are examples of what can be done with templating using Jinja2.

Beaker Template
~~~~~~~~~~~~~~~

This template would be processed with a dictionary containing a key named `arches`.

    :docs1.5:`workspace/PinFile.beaker.template`

.. code-block:: bash

    linchpin -p PinFile.beaker.template \
        --template-data '{ "arches": [ "x86_64", "ppc64le", "s390x" ]}' up

The 
.. 

Libvirt Template and Data
~~~~~~~~~~~~~~~~~~~~~~~~~

    :docs1.5:`workspace/PinFile.libvirt-mi.template`
    :docs1.5:`workspace/Data.libvirt-mi.yml`


Scripts
```````

New in version 1.5.0
