#!/usr/bin/env python

import yaml

from linchpin.exceptions import LinchpinError


def yaml2json(pf):

    """ parses yaml file into json object """

    with open(pf, 'r') as stream:
        try:
            pf = yaml.load(stream)
            return pf
        except yaml.YAMLError as exc:
            raise LinchpinError(exc)
