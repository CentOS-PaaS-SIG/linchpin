Template Data
=============

PinFiles in LinchPin can be templated.  Templates are parsed with Jinja2, so the syntax is exactly the same.

Templates in a PinFile
-----------------------

To get started, let's take a look at the PinFile below.

.. code::yaml
    aws-ec2-new:
      topology:
        topology_name: ec2-new
        resource_groups:
          - resource_group_name: "aws"
            resource_group_type: "aws"
            resource_definitions:
              - name: demo-day
                role: aws_ec2
                flavor: {{ flavor }}
                image: {{ image | default('ami-984189e2') }}
                count: 1
            {% if credentials is defined %}
            credentials:
              filename: {{ credentials.filename }}
              profile: {{ credentials.profile }}
            {% else %}
            credentials:
              filename: aws.key
              profile: default
            {% endif %}
```

Here we have a simple PinFile used to provision an AWS EC2 instance.  The :term:`flavor` field makes use of basic templating.  The double curly brackets tell the template parser that "flavor" is a variable which can be found in the template data.  We cover template data more in the next section.  The :term:`image` field expands upon this with a filter.  Filters modify variables and are separated from the variable by a pipe.  In this case, the fitter is the :code:`default()` filter, which provides a value for the field if the variable is not defined.

Finally, we can see templates used to fill in the :term:`credentials` section of the PinFile.  In this case, we have a conditional.  If the credentials are defined in template data, we can use those values to fill in the credentials.  Otherwise, we have default credentials we can use.  :code:`if` statements and :code:`for` loops are defined with a :code:`{% ... %}` syntax. Why can't the default filter be used in this example?  Why can't we simply use the line :code:`filename: {{ credentials.filename | default('aws.key') }}` and do the same for the profile?  In this version, the template parser will fall back to the default field if credentials.filename is not defined.  However, if the credentials section is not defined at all, an error will be thrown.  Because of this, we need to use an if statement here to correctly handle a case in which no credentials are defined in the template data.

This example only demonstrates the use of template data in a topology, but it can also be used in the :term:`layout` or :term:`cfgs` sections


Template Data
-------------

Where does the template data come from?  The template data can either be declared inline or defined in a file.  The data is supplied to linchpin with the :code:`--template-data` or :code:`-d` flags.  The template data can be formatted as JSON or as yaml.  Below is an example of a template file, called data.yml, that goes with the PinFile above

.. code::yaml

    flavor: m1.small
    credentials:
      filename: example.key
      profile: default


This file does not define an image, so LinchPin will fall back on the default.  However, the flavor and credentials fields will be pulled from the above file.  To run LinchPin with a file, run the command below:

.. code::bash

	$ linchpin -vv --template-data @data.yml up aws-ec2-new

Notice the :term:`@` prepended to the filename.  This is used so that the template engine knows that this is a filename and not raw data.  Our example topology requires the user to provide a flavor in template data but doesn't actually require anything else.  In a case as simple as this, we can provide the data inline.

.. code::bash

	$ linchpin -vv --template-data "{'flavor': 'm1.small'}" up aws-ec2-new

That should be enough to get started.  To read more about Jinja2 syntax, `go here`_

.. _go here: http://jinja.pocoo.org/docs/2.10/templates/
