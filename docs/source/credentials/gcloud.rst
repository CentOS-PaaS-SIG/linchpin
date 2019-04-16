Google Cloud Key File
```````````````````````````
GCloud allows for the creation of keyfiles for authentication.  A keyfile will look something like this:

.. code-block:: json

    {
      "type": "service_account",
      "project_id": "[PROJECT-ID]",
      "private_key_id": "[KEY-ID]",
      "private_key": "-----BEGIN PRIVATE KEY-----\n[PRIVATE-KEY]\n-----END PRIVATE KEY-----\n",
      "client_email": "[SERVICE-ACCOUNT-EMAIL]",
      "client_id": "[CLIENT-ID]",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://accounts.google.com/o/oauth2/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/[SERVICE-ACCOUNT-EMAIL]"
    }

To learn how to generate key files, `see the google cloud documentation <https://cloud.google.com/iam/docs/creating-managing-service-account-keys>`.

This mechanism requires that credentials data be passed into LinchPin.  A GCloud topology can have a ``credentials`` section for each :term:`resource_group`, which requires the filename and the profile name.  By default, LinchPin searches for the filename in {{ workspace }}/credentials but can be made to search other places by setting the :code:`evars.default_credentials_path` variable in your linchpin.conf.  The credentials path can also be overridden by using the :code:`--creds-path` flag.

.. code-block:: json

    ---
    topology_name: mytopo
    resource_groups:
      - resource_group_name: gce
      - resource_group_type: gcloud
        resource_definitions:

          .. snip ..

        credentials:
          filename: gcloud.key
