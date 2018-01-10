#!/usr/bin/env python

import yaml
import json
import subprocess

# CentOS 6 EPEL provides an alternate Jinja2 package
try:
    from jinja2 import BaseLoader
    from jinja2 import Environment
except ImportError:
    import sys
    sys.path.insert(0, '/usr/lib/python2.6/site-packages/Jinja2-2.6-py2.6.egg')
    from jinja2 import BaseLoader
    from jinja2 import Environment


from linchpin.exceptions import LinchpinError
from linchpin.exceptions import ValidationError


def dict_representer(dumper, data):
    _mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
    return dumper.represent_mapping(_mapping_tag, data.iteritems())


def dict_constructor(loader, node):
    return dict(loader.construct_pairs(node))


class DataParser(object):


    def __init__(self):

        self._mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


    def process(self, file_w_path, data_w_path=None):
        """ Processes the PinFile and any data (if a template)
        using Jinja2. Returns json of PinFile, topology, layout,
        and hooks.

        :param file_w_path:
            Full path to the provided file to process

        :param targets:
            A tuple of targets to provision

        :param run_id:
            An optional run_id if the task is idempotent or a destroy action
        """

        with open(file_w_path, 'r') as stream:
            file_data = stream.read()

            pf_data = '{}'
            if data_w_path:
                pf_data = data_w_path
                try:
                    with open(data_w_path, 'r') as strm:
                        pf_data = strm.read()
                except Exception:
                    pass

            file_data = self.render(file_data, pf_data)
            return self.parse_json_yaml(file_data)

        return self.load_pinfile(file_w_path)


    def render(self, template, context):
        """
        Performs the rendering of template and context data using
        Jinja2.

        :param template:
            Full path to the Jinja2 template

        :param context:
            A dictionary of variables to be rendered againt the template
        """

        c = self.parse_json_yaml(context)
        t = Environment(loader=BaseLoader).from_string(template)
        return t.render(c)


    def parse_json_yaml(self, data):

        """ parses yaml file into json object """

        d = None

        # Setup support for ordered dicts so we do not lose ordering
        # when importing from YAML
        yaml.add_representer(dict, dict_representer)
        yaml.add_constructor(self._mapping_tag, dict_constructor)

        try:
            data = yaml.load(data)
        except Exception as e:
            raise LinchpinError('YAML parsing error: {}'.format(e))

        if isinstance(data, dict):
            return data

        return d


    def run_script(self, script):

        sp = None
        try:
            sp = subprocess.Popen(script,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        except OSError as e:
            raise ValidationError("problem running {0} ({1})".format(script, e))

        (stdout, stderr) = sp.communicate()

        if sp.returncode != 0:
            raise ValidationError("Script {0} had execution error"
                                  " ({1})".format(script, e))

        return stdout


    def load_pinfile(self, pinfile):
        # try to convert the data into json
        pf = None
        try:
            with open(pinfile, 'r') as stream:
                pf_data = stream.read()
                pf = self.parse_json_yaml(pf_data)
        except ValidationError as e:
            pass

        if not pf:
            # assume not json, so dynamic script
            # once executed, verify it is json
            try:
                pf = json.loads(self.run_script(pinfile))
            except Exception as e:
                raise LinchpinError(e)

        return pf

    def write_json(self, provision_data, pf_outfile):

        with open(pf_outfile, 'w') as outfile:
            json.dump(provision_data, outfile, indent=4)
