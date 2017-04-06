#!/usr/bin/python
# Copyright 2017 RedHat Inc. All Rights Reserved.
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>

DOCUMENTATION = '''
---
module: openshift
version_added: "2.4"
short_description: Manage OpenShift resources.
description:
    - This module can manage OpenShift resources on an existing cluster using
      the OpenShift server API. Users can specify in-line API data, or
      specify an existing OpenShift YAML file. Currently, this module,
        Only supports 'strategic merge' for update, http://goo.gl/fCPYxT
        SSL certs are not working, use 'validate_certs=off' to disable
options:
  api_endpoint:
    description:
      - The IPv4 API endpoint of the OpenShift cluster.
    required: true
    default: null
    aliases: ["endpoint"]
  inline_data:
    description:
      - The OpenShift YAML data to send to the API I(endpoint). This option is
        mutually exclusive with C('file_reference').
    required: true
    default: null
  file_reference:
    description:
      - Specify full path to a OpenShift YAML file to send to API I(endpoint).
        This option is mutually exclusive with C('inline_data').
    required: false
    default: null
  certificate_authority_data:
    description:
      - Certificate Authority data for OpenShift server. Should be in either
        standard PEM format or base64 encoded PEM data. Note that certificate
        verification is broken until ansible supports a version of
        'match_hostname' that can match the IP address against the CA data.
    required: false
    default: null
  state:
    description:
      - The desired action to take on the OpenShift data.
    required: true
    default: "present"
    choices: ["present", "absent", "update", "replace"]
  api_token:
    description:
      - The OpenShift token for use when authenticating against the API. This
        can be acquired with the OpenShift CLI client ("oc") after loggin in
        by executing the command "oc whoami --token"
    required: true
    aliases: ["token"]
  validate_certs:
    description:
      - Enable/disable certificate validation. Note that this is set to
        C(false) until Ansible can support IP address based certificate
        hostname matching (exists in >= python3.5.0).
    required: false
    default: false

author: "Greg Hellings @greg-hellings <greg.hellings@gmail.com>"
'''

EXAMPLES = '''
# Create a new namespace with in-line YAML.
- name: Create a openshift namespace
  openshift:
    api_endpoint: 123.45.67.89
    api_token: sometokenstringhere
    inline_data:
      kind: Namespace
      apiVersion: v1
      metadata:
        name: ansible-test
        labels:
          label_env: production
          label_ver: latest
        annotations:
          a1: value1
          a2: value2
    state: present

# Create a new namespace from a YAML file.
- name: Create a openshift namespace
  openshift:
    api_endpoint: 123.45.67.89
    api_token: sometokenstringhere
    file_reference: /path/to/create_namespace.yaml
    state: present
'''

RETURN = '''
# Example response from creating a OpenShift Namespace.
api_response:
    description: Raw response from OpenShift API, content varies with API.
    returned: success
    type: dictionary
    contains:
        apiVersion: "v1"
        kind: "Namespace"
        metadata:
            creationTimestamp: "2016-01-04T21:16:32Z"
            name: "test-namespace"
            resourceVersion: "509635"
            selfLink: "/api/v1/namespaces/test-namespace"
            uid: "6dbd394e-b328-11e5-9a02-42010af0013a"
        spec:
            finalizers:
                - openshift
        status:
            phase: "Active"
'''

import yaml
import base64

from copy import copy

############################################################################
############################################################################
# For API coverage, this Anislbe module provides capability to operate on
# all OpenShift objects that support a "create" call (except for 'Events').
# In order to obtain a valid list of OpenShift objects, the v1 spec file
# was referenced and the below python script was used to parse the JSON
# spec file, extract only the objects with a description starting with
# 'create a'. The script then iterates over all of these base objects
# to get the endpoint URL and was used to generate the KIND_URL map.
#
#import json
#from urllib2 import urlopen
#
#apis = {}
#cluster_apis = {}
#
#def load_api(api):
#    v1 = json.load(api)
#
#    for a in v1['apis']:
#        p = a['path']
#        for o in a['operations']:
#            if o["summary"].startswith("create a") and o["type"] != "v1.Event":
#                if "{namespace}" in p:
#                    apis[o["type"]] = p
#                else:
#                    cluster_apis[o["type"]] = p
#
#def print_kind_url_map():
#    results = ['"{0}": "{1}"'.format(a[3:].lower(), apis[a])
#               for a in apis.keys()]
#    cluster_results = ['"{0}": "{1}"'.format(a[3:].lower(), cluster_apis[a])
#                       for a in cluster_apis.keys()]
#    results.sort()
#    cluster_results.sort()
#    print "KIND_URL = {"
#    print ",\n".join(results)
#    print "}"
#    print "CLUSTER_URL = {"
#    print ",\n".join(cluster_results)
#    print "}"
#
#if __name__ == '__main__':
#    k = urlopen("https://raw.githubusercontent.com/openshift"
#               "/origin/master/api/swagger-spec/api-v1.json")
#    o = urlopen("https://raw.githubusercontent.com/openshift"
#               "/origin/master/api/swagger-spec/oapi-v1.json")
#    load_api(k)
#    load_api(o)
#    print_kind_url_map()
############################################################################
############################################################################

KIND_URL = {
    "binding": "/api/v1/namespaces/{namespace}/bindings",
    "build": "/oapi/v1/namespaces/{namespace}/builds",
    "buildconfig": "/oapi/v1/namespaces/{namespace}/buildconfigs",
    "configmap": "/api/v1/namespaces/{namespace}/configmaps",
    "deploymentconfig": "/oapi/v1/namespaces/{namespace}/deploymentconfigs",
    "deploymentconfigrollback": "/oapi/v1/namespaces/{namespace}/deploymentconfigrollbacks",
    "egressnetworkpolicy": "/oapi/v1/namespaces/{namespace}/egressnetworkpolicies",
    "imagestream": "/oapi/v1/namespaces/{namespace}/imagestreams",
    "imagestreamimport": "/oapi/v1/namespaces/{namespace}/imagestreamimports",
    "imagestreammapping": "/oapi/v1/namespaces/{namespace}/imagestreammappings",
    "imagestreamtag": "/oapi/v1/namespaces/{namespace}/imagestreamtags",
    "limitrange": "/api/v1/namespaces/{namespace}/limitranges",
    "localresourceaccessreview": "/oapi/v1/namespaces/{namespace}/localresourceaccessreviews",
    "localsubjectaccessreview": "/oapi/v1/namespaces/{namespace}/localsubjectaccessreviews",
    "persistentvolumeclaim": "/api/v1/namespaces/{namespace}/persistentvolumeclaims",
    "pod": "/api/v1/namespaces/{namespace}/pods",
    "podsecuritypolicyreview": "/oapi/v1/namespaces/{namespace}/podsecuritypolicyreviews",
    "podsecuritypolicyselfsubjectreview": "/oapi/v1/namespaces/{namespace}/podsecuritypolicyselfsubjectreviews",
    "podsecuritypolicysubjectreview": "/oapi/v1/namespaces/{namespace}/podsecuritypolicysubjectreviews",
    "podtemplate": "/api/v1/namespaces/{namespace}/podtemplates",
    "policy": "/oapi/v1/namespaces/{namespace}/policies",
    "policybinding": "/oapi/v1/namespaces/{namespace}/policybindings",
    "replicationcontroller": "/api/v1/namespaces/{namespace}/replicationcontrollers",
    "resourceaccessreview": "/oapi/v1/namespaces/{namespace}/resourceaccessreviews",
    "resourcequota": "/api/v1/namespaces/{namespace}/resourcequotas",
    "role": "/oapi/v1/namespaces/{namespace}/roles",
    "rolebinding": "/oapi/v1/namespaces/{namespace}/rolebindings",
    "rolebindingrestriction": "/oapi/v1/namespaces/{namespace}/rolebindingrestrictions",
    "route": "/oapi/v1/namespaces/{namespace}/routes",
    "secret": "/api/v1/namespaces/{namespace}/secrets",
    "selfsubjectrulesreview": "/oapi/v1/namespaces/{namespace}/selfsubjectrulesreviews",
    "service": "/api/v1/namespaces/{namespace}/services",
    "serviceaccount": "/api/v1/namespaces/{namespace}/serviceaccounts",
    "subjectaccessreview": "/oapi/v1/namespaces/{namespace}/subjectaccessreviews",
    "subjectrulesreview": "/oapi/v1/namespaces/{namespace}/subjectrulesreviews",
    "template": "/oapi/v1/namespaces/{namespace}/templates"
}
CLUSTER_URL = {
    "binding": "/api/v1/bindings",
    "build": "/oapi/v1/builds",
    "buildconfig": "/oapi/v1/buildconfigs",
    "clusternetwork": "/oapi/v1/clusternetworks",
    "clusterpolicy": "/oapi/v1/clusterpolicies",
    "clusterpolicybinding": "/oapi/v1/clusterpolicybindings",
    "clusterresourcequota": "/oapi/v1/clusterresourcequotas",
    "clusterrole": "/oapi/v1/clusterroles",
    "clusterrolebinding": "/oapi/v1/clusterrolebindings",
    "configmap": "/api/v1/configmaps",
    "deploymentconfig": "/oapi/v1/deploymentconfigs",
    "deploymentconfigrollback": "/oapi/v1/deploymentconfigrollbacks",
    "egressnetworkpolicy": "/oapi/v1/egressnetworkpolicies",
    "group": "/oapi/v1/groups",
    "hostsubnet": "/oapi/v1/hostsubnets",
    "identity": "/oapi/v1/identities",
    "image": "/oapi/v1/images",
    "imagesignature": "/oapi/v1/imagesignatures",
    "imagestream": "/oapi/v1/imagestreams",
    "imagestreamimport": "/oapi/v1/imagestreamimports",
    "imagestreammapping": "/oapi/v1/imagestreammappings",
    "imagestreamtag": "/oapi/v1/imagestreamtags",
    "limitrange": "/api/v1/limitranges",
    "localresourceaccessreview": "/oapi/v1/localresourceaccessreviews",
    "localsubjectaccessreview": "/oapi/v1/localsubjectaccessreviews",
    "namespace": "/api/v1/namespaces",
    "netnamespace": "/oapi/v1/netnamespaces",
    "node": "/api/v1/nodes",
    "oauthaccesstoken": "/oapi/v1/oauthaccesstokens",
    "oauthauthorizetoken": "/oapi/v1/oauthauthorizetokens",
    "oauthclient": "/oapi/v1/oauthclients",
    "oauthclientauthorization": "/oapi/v1/oauthclientauthorizations",
    "persistentvolume": "/api/v1/persistentvolumes",
    "persistentvolumeclaim": "/api/v1/persistentvolumeclaims",
    "pod": "/api/v1/pods",
    "podsecuritypolicyreview": "/oapi/v1/podsecuritypolicyreviews",
    "podsecuritypolicyselfsubjectreview": "/oapi/v1/podsecuritypolicyselfsubjectreviews",
    "podsecuritypolicysubjectreview": "/oapi/v1/podsecuritypolicysubjectreviews",
    "podtemplate": "/api/v1/podtemplates",
    "policy": "/oapi/v1/policies",
    "policybinding": "/oapi/v1/policybindings",
    "project": "/oapi/v1/projects",
    "projectrequest": "/oapi/v1/projectrequests",
    "replicationcontroller": "/api/v1/replicationcontrollers",
    "resourceaccessreview": "/oapi/v1/resourceaccessreviews",
    "resourcequota": "/api/v1/resourcequotas",
    "role": "/oapi/v1/roles",
    "rolebinding": "/oapi/v1/rolebindings",
    "rolebindingrestriction": "/oapi/v1/rolebindingrestrictions",
    "route": "/oapi/v1/routes",
    "secret": "/api/v1/secrets",
    "selfsubjectrulesreview": "/oapi/v1/selfsubjectrulesreviews",
    "service": "/api/v1/services",
    "serviceaccount": "/api/v1/serviceaccounts",
    "subjectaccessreview": "/oapi/v1/subjectaccessreviews",
    "subjectrulesreview": "/oapi/v1/subjectrulesreviews",
    "template": "/oapi/v1/templates",
    "user": "/oapi/v1/users",
    "useridentitymapping": "/oapi/v1/useridentitymappings"
}
USER_AGENT = "ansible-openshift-module/0.0.1"


# TODO(erjohnso): SSL Certificate validation is currently unsupported.
# It can be made to work when the following are true:
# - Ansible consistently uses a "match_hostname" that supports IP Address
#   matching. This is now true in >= python3.5.0. Currently, this feature
#   is not yet available in backports.ssl_match_hostname (still 3.4).
# - Ansible allows passing in the self-signed CA cert that is created with
#   a kubernetes master. The lib/ansible/module_utils/urls.py method,
#   SSLValidationHandler.get_ca_certs() needs a way for the OpenShift
#   CA cert to be passed in and included in the generated bundle file.
# When this is fixed, the following changes can be made to this module,
# - Remove the 'return' statement in line 254 below
# - Set 'required=true' for certificate_authority_data and ensure that
#   ansible's SSLValidationHandler.get_ca_certs() can pick up this CA cert
# - Set 'required=true' for the validate_certs param.

def decode_cert_data(module):
    return
    d = module.params.get("certificate_authority_data")
    if d and not d.startswith("-----BEGIN"):
        module.params["certificate_authority_data"] = base64.b64decode(d)


def api_request(module, url, method="GET", headers={}, data=None):
    body = None
    headers.update(base_headers)
    if data:
        data = json.dumps(data)
    response, info = fetch_url(module, url, method=method, headers=headers, data=data)
    if int(info['status']) == -1:
        module.fail_json(msg="Failed to execute the API request: %s" % info['msg'], url=url, method=method, headers=headers)
    if response is not None:
        body = json.loads(response.read())
    return info, body


def openshift_create_resource(module, url, data):
    info, body = api_request(module, url, method="POST", data=data, headers={"Content-Type": "application/json"})
    if info['status'] == 409:
        name = data["metadata"].get("name", None)
        info, body = api_request(module, url + "/" + name)
        return False, body
    elif info['status'] >= 400:
        module.fail_json(msg="failed to create the resource: %s" % info['msg'], url=url)
    return True, body


def openshift_delete_resource(module, url, data):
    name = data.get('metadata', {}).get('name')
    if name is None:
        module.fail_json(msg="Missing a named resource in object metadata when trying to remove a resource")

    url = url + '/' + name
    info, body = api_request(module, url, method="DELETE")
    if info['status'] == 404:
        return False, "Resource name '%s' already absent" % name
    elif info['status'] >= 400:
        module.fail_json(msg="failed to delete the resource '%s': %s" % (name, info['msg']), url=url)
    return True, "Successfully deleted resource name '%s'" % name


def openshift_replace_resource(module, url, data):
    name = data.get('metadata', {}).get('name')
    if name is None:
        module.fail_json(msg="Missing a named resource in object metadata when trying to replace a resource")

    headers = {"Content-Type": "application/json"}
    url = url + '/' + name
    info, body = api_request(module, url, method="PUT", data=data, headers=headers)
    if info['status'] == 409:
        name = data["metadata"].get("name", None)
        info, body = api_request(module, url + "/" + name)
        return False, body
    elif info['status'] >= 400:
        module.fail_json(msg="failed to replace the resource '%s': %s" % (name, info['msg']), url=url)
    return True, body


def openshift_update_resource(module, url, data):
    name = data.get('metadata', {}).get('name')
    if name is None:
        module.fail_json(msg="Missing a named resource in object metadata when trying to update a resource")

    headers = {"Content-Type": "application/strategic-merge-patch+json"}
    url = url + '/' + name
    info, body = api_request(module, url, method="PATCH", data=data, headers=headers)
    if info['status'] == 409:
        name = data["metadata"].get("name", None)
        info, body = api_request(module, url + "/" + name)
        return False, body
    elif info['status'] >= 400:
        module.fail_json(msg="failed to update the resource '%s': %s" % (name, info['msg']), url=url)
    return True, body


base_headers = {}

def main():
    module = AnsibleModule(
        argument_spec=dict(
            http_agent=dict(default=USER_AGENT),

            api_token=dict(aliases=["token"]),
            force_basic_auth=dict(default="yes"),
            validate_certs=dict(default=False, type='bool'),
            certificate_authority_data=dict(required=False),
            api_endpoint=dict(required=True),
            file_reference=dict(required=False),
            inline_data=dict(required=False),
            state=dict(default="present", choices=["present", "absent", "update", "replace"])
        ),
        mutually_exclusive = (('file_reference', 'inline_data')),
        required_one_of = (('file_reference', 'inline_data'),),
    )

    decode_cert_data(module)

    api_endpoint = module.params.get('api_endpoint')
    state = module.params.get('state')
    inline_data = module.params.get('inline_data')
    file_reference = module.params.get('file_reference')
    base_headers['Authorization'] = 'Bearer {0}'.format(module.params.get('api_token'))

    if inline_data:
        if not isinstance(inline_data, dict) and not isinstance(inline_data, list):
            data = yaml.load(inline_data)
        else:
            data = inline_data
    else:
        try:
            f = open(file_reference, "r")
            data = [x for x in yaml.load_all(f)]
            f.close()
            if not data:
                module.fail_json(msg="No valid data could be found.")
        except:
            module.fail_json(msg="The file '%s' was not found or contained invalid YAML/JSON data" % file_reference)

    # set the transport type and build the target endpoint url
    transport = 'https'

    target_endpoint = "%s://%s" % (transport, api_endpoint)

    body = []
    changed = False

    # make sure the data is a list
    if not isinstance(data, list):
        data = [ data ]

    for item in data:
        namespace = None
        if item and 'metadata' in item:
            namespace = item.get('metadata', {}).get('namespace', None)
            kind = item.get('kind', '').lower()
            try:
                if namespace is None:
                    url = target_endpoint + CLUSTER_URL[kind]
                else:
                    url = target_endpoint + KIND_URL[kind]
            except KeyError:
                module.fail_json(msg="invalid resource kind specified in the data: '%s'" % kind)
            url = url.replace("{namespace}", namespace)
        else:
            url = target_endpoint

        if state == 'present':
            item_changed, item_body = openshift_create_resource(module, url, item)
        elif state == 'absent':
            item_changed, item_body = openshift_delete_resource(module, url, item)
        elif state == 'replace':
            item_changed, item_body = openshift_replace_resource(module, url, item)
        elif state == 'update':
            item_changed, item_body = openshift_update_resource(module, url, item)

        changed |= item_changed
        body.append(item_body)

    module.exit_json(changed=changed, api_response=body)


# import module snippets
from ansible.module_utils.basic import *    # NOQA
from ansible.module_utils.urls import *     # NOQA


if __name__ == '__main__':
    main()
