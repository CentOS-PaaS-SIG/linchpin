#!/usr/bin/env python
import os
import json
import yaml
import yamlordereddictloader
from camel import Camel

def to_ordered_dict(filepath):
    data = yaml.load(open(filepath), Loader=yamlordereddictloader.Loader)
    data = Camel().dump(data["inventory_layout"])
    return data

class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        return {
            'ordered_yaml': to_ordered_dict
        }
