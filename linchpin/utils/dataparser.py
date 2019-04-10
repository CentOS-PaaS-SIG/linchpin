#!/usr/bin/env python

import yaml
import json
import subprocess
import yamlordereddictloader

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


class DataParser(object):


    def __init__(self):

        self._mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


    def process(self, file_w_path, data=None):
        """ Processes the PinFile and any data (if a template)
        using Jinja2. Returns json of PinFile, topology, layout,
        and hooks.

        :param file_w_path:
            Full path to the provided file to process

        :param data:
            A JSON representation of data mapped to a Jinja2 template in
            file_w_path

        """
        if not data:
            data = '{}'

        with open(file_w_path, 'r') as stream:
            file_data = stream.read()

            if data.startswith('@'):
                with open(data[1:], 'r') as strm:
                    data = strm.read()

            try:
                file_data = self.render(file_data, data)
                return self.parse_json_yaml(file_data)
            except TypeError:
                error_txt = "Error attempting to parse PinFile data file."
                error_txt += "\nTemplate-data files require a prepended '@'"
                error_txt += " (eg. '@/path/to/template-data.yml')"
                error_txt += "\nPerhaps the path to the PinFile or"
                error_txt += " template-data is missing or the incorrect path?."
                raise ValidationError(error_txt)

        return self.load_pinfile(file_w_path)


    def render(self, template, context, ordered=True):
        """
        Performs the rendering of template and context data using
        Jinja2.

        :param template:
            Full path to the Jinja2 template

        :param context:
            A dictionary of variables to be rendered againt the template
        """

        # setting ordered=False may be problematic, but it is required until
        # ansible supports OrderedDict in templates, which can't happen until
        # it stops supporting python 2.6
        c = self.parse_json_yaml(context, ordered=False)
        t = Environment(loader=BaseLoader).from_string(str(template))
        return t.render(c)


    def parse_json_yaml(self, data, ordered=True):

        """ parses yaml file into json object """

        d = None

        try:
            if ordered:
                data = yaml.load(data, Loader=yamlordereddictloader.Loader)
            else:
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
            raise ValidationError("Script {0}"
                                  " had execution error".format(script))

        return stdout


    def load_pinfile(self, pinfile):
        # try to convert the data into json
        pf = None
        try:
            with open(pinfile, 'r') as stream:
                pf_data = stream.read()
                pf = self.parse_json_yaml(pf_data)
                # ordered hooks gives parsing errors
                # since hooks are already in lists we need not maintain order
                pf['hooks'] = self.parse_json_yaml(pf_data,
                                                   ordered=False).get('hooks',
                                                                      {})
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
