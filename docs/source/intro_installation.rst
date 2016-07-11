Installation
============

.. contents:: Topics

.. _getting_ansible:

Getting Ansible
```````````````

As linchpin is a collection of playbooks, Ansible should be installed on the machine before we start using linchpin . 
You may try the following link for installing Ansible.
| `Ansible Installation <http://docs.ansible.com/ansible/intro_installation.html>`_

.. note::

    Ansible version installed should be >= 2.1.0

.. _control_machine_requirements:

Minimum Requirements
````````````````````

Currently Linchpin can be run from any machine with Python 2.6 or 2.7, and Ansible 2.1.0  installed ( Windows isn't supported ).

This includes Red Hat, Debian, CentOS, OS X, any of the BSDs, and so on.


.. _getting_linchpin:

Getting Linchpin
````````````````

Linch pin is available as a public GitHub repository. Thus linchpin can be directly clone and used. 

.. _from_source:

Install from source.

.. code-block:: bash

    $ git clone https://github.com/CentOS-PaaS-SIG/linch-pin.git --recursive
    $ cd ./linch-pin
    $ sudo pip install -r requirements.txt # installs the dependencies required for linch-pin
