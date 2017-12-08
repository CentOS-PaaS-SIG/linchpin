#!/usr/bin/env python

import sys
import yaml
import json
import yaml
import json
import subprocess

from linchpin.exceptions import ValidationError


def parse_json_yaml(f):

    """ parses yaml file into json object """

    d = None

    # Setup support for ordered dicts so we do not lose ordering
    # when importing from YAML
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
    yaml.add_representer(dict, dict_representer)
    yaml.add_constructor(_mapping_tag, dict_constructor)

    with open(f, 'r') as stream:
        data = stream.read()
        data = yaml.load(data)

        if isinstance(data, dict):
            return data

    return d


def run_script(script):

    try:
        sp = subprocess.Popen(script,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
    except OSError as e:
        raise ValidationError("problem running {0} ({1})".format(script, e))

    (stdout, stderr) = sp.communicate()

    if sp.returncode != 0:
        raise ValidationError("Script {0} had execution error ({1})".format(script, e))

    return stdout


def load_pinfile(pinfile):
    # try to convert the data into json
    pf = None
    try:
        pf = parse_json_yaml(pinfile)
    except ValidationError as e:
        pass

    if not pf:
        # assume not json, so dynamic script
        # once executed, verify it is json
        try:
            pf = json.loads(run_script(pinfile))
        except ValueError as e:
            raise LinchpinError(e)

    return pf


def dict_representer(dumper, data):
    return dumper.represent_mapping(_mapping_tag, data.iteritems())


def dict_constructor(loader, node):
    return dict(loader.construct_pairs(node))


def main():
    pass
#    data = yaml.load(open(sys.argv[1]))
#    print(type(data))
#    print json.dumps(data, indent=4)


if __name__ == '__main__':
    sys.exit(main())
