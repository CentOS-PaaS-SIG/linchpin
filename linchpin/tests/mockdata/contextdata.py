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


        self.lib_path = '{0}'.format(os.path.dirname(
            os.path.realpath(__file__))).rstrip('/')

        self.logfile = tempfile.mktemp(suffix='.log', prefix='linchpin')
        self.parser = parser()


    def load_config_data(self, provider='dummy'):
        """
        Load a test-based linchpin.conf into both a configs and evars
        dictionary to represent a configuration file

        """

        self.cfg_data = {}

        expanded_path = None
        config_found = False

        # simply modify this variable to adjust where linchpin.conf can be found
        CONFIG_PATH = [
            '{0}/{1}/conf/linchpin.conf'.format(self.lib_path, provider)
        ]

        for path in CONFIG_PATH:
            expanded_path = (
                "{0}".format(os.path.realpath(os.path.expanduser(path))))

            # implement first found
            if os.path.exists(expanded_path):
                config_found = True
                break

        if not config_found:
            raise LinchpinError('Configuration file not found in'
                                ' path: {0}'.format(CONFIG_PATH))

        config = ConfigParser.SafeConfigParser()
        try:
            f = open(path)
            config.readfp(f)
            f.close()
        except ConfigParser.InterpolationSyntaxError as e:
            raise LinchpinError('Unable to parse configuration file properly:'
                    ' {0}'.format(e))

        for section in config.sections():
            if section not in self.cfg_data:
                self.cfg_data[section] = {}

            # add evars to the ansible extra_vars when running a playbook.
            for k, v in config.items(section):
                if section != 'evars':
                    self.cfg_data[section][k] = v
                else:
                    try:
                        self.cfg_data[section][k] = config.getboolean(section, k)
                    except ValueError as e:
                        self.cfg_data[section][k] = v

        # override logger file
        self.cfg_data['logger']['file'] = self.logfile

        self.evars = self.cfg_data.get('evars', {})


    def get_temp_filename(self):

        tmpfile = tempfile.NamedTemporaryFile(delete=False).name
        return tmpfile


    def write_config_file(self, path):

        try:
            with open(path, 'a+') as f:
                self.parser.write(f)
        except Exception as e:
            raise LinchpinError('Unable to write configuration file:'
                    ' {0}'.format(e))


    def parse_config(self, config_data=None):

        """
        Creates a config object using ConfigParser from the config_data object

        """

        if not config_data:
            config_data = self.cfg_data

        #we know that data is a dict, containing dicts
        for k, v in config_data.iteritems():
            self.parser.add_section(k)
            for kv, vv in v.iteritems():
                if type(vv) is not str:
                    vv = str(vv)
                self.parser.set(k, kv, vv)

