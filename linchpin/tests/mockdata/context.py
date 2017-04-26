import os

import tempfile
import ConfigParser
from collections import OrderedDict

from linchpin.api import LinchpinError

"""
Provide valid context data to test against.

"""

class ContextData(object):

    def __init__(self, parser=ConfigParser.SafeConfigParser):

        """
        Create a dictionary to represent an ini-style configuration file

        """

        self.logfile = tempfile.mktemp(suffix='.log', prefix='linchpin', dir='/tmp')
        self.parser = parser()

        self.config_data = {
            'console': {
                'enable': 'True', # placeholder
            },
            'logger': {
                'enable': 'True',
                'file': self.logfile,
            },
            'playbooks': {
                'up': 'up.yml',
                'destroy': 'destroy.yml',
                'down': 'down.yml',
                'schema_check': 'schemacheck.yml',
                'inv_gen': 'invgen.yml',
                'test': 'test.yml'
            },
            'lp': {
                'module_folder': 'modules',
                'pf_excludes': 'upstream1,upstream2'
            },
        }

        self.evars = {
                'async': False,
                'async_timeout': '1000',
                'output': True,
                'check_mode': False
        }


    def get_temp_filename(self):

        return tempfile.NamedTemporaryFile(delete=False).name


    def write_config_file(self, path):

        try:
            with open(path, 'w+') as f:
                self.parser.write(f)
        except Exception as e:
            raise LinchpinError('Unable to write configuration file:'
                    ' {0}'.format(e))


    def parse_config(self, config_data=None):

        """
        Creates a config object using ConfigParser from the config_data object

        """

        if not config_data:
            config_data = self.config_data

        #we know that data is a dict, containing dicts
        for k, v in config_data.iteritems():
            self.parser.add_section(k)
            for kv, vv in v.iteritems():
                self.parser.set(k, kv, vv)


    def create_context_evars(self):

        """
        Adds extra_vars (evars) to a config object

        .. note:: To use thie function with boolean objects, RawConfigParser
                  is required

        """

        self.parser.add_section('evars')
        for k, v in self.evars.iteritems():
            self.parser.set('evars', k, v)


