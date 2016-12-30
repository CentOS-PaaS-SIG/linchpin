import yaml
import json
import jsonschema
from jsonschema import validate


def get_cred_schema(cred_type):
    aws_cred_schema = {
        "type": "object",
        "properties": {
           "aws_access_key_id": {"type": "string"},
           "aws_secret_access_key": {"type": "string"},
        },
        "required": ["aws_access_key_id", "aws_secret_access_key"]
    }
    os_cred_schema = {
        "type": "object",
        "properties": {
           "endpoint": {"type": "string"},
           "project": {"type": "string"},
           "username": {"type": "string"},
           "password": {"type": "string"},
        },
        "required": ["endpoint", "project", "username", "password"]
    }
    gcloud_cred_schema = {
        "type": "object",
        "properties": {
           "service_account_email": {"type": "string"},
           "project_id": {"type": "string"},
           "credentials_file": {"type": "string"},
        },
        "required": ["service_account_email", "project_id", "credentials_file"]
    }
    duffy_cred_schema = {
        "type": "object",
        "properties": {
           "key_path": {"type": "string"},
           "url_base": {"type": "string"},
        },
    }
    rx_cred_schema = {
        "type": "object",
        "properties": {
           "username": {"type": "string"},
           "api_key": {"type": "string"},
        },
    }
    cred_schemas = {
       "aws": aws_cred_schema,
       "os": os_cred_schema,
       "gcloud": gcloud_cred_schema,
       "duffy": duffy_cred_schema,
       "rax": rx_cred_schema
    }
    return cred_schemas[cred_type]


def validate_creds(cred_path, cred_type):
    schema = get_cred_schema(cred_type)
    cred_str = open(cred_path).read()
    cred_json = yaml.load(cred_str)
    try:
        validate(cred_json, schema)
        return True
    except:
        return False
