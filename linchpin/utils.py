#!/usr/bin/env python

import yaml
import json

from linchpin.exceptions import ValidationError


def parse_json_yaml(f):

    """ parses yaml file into json object """

    d = None

    with open(f, 'r') as stream:
        data = stream.read()
        try:
            d = json.loads(data)
        except Exception:
            try:
                d = yaml.safe_load(data)
            except Exception as exc:
                raise ValidationError(exc)

    return d
