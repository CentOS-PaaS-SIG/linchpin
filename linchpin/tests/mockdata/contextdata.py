import os

import tempfile
from six.moves import configparser as ConfigParser
from six import iteritems

from linchpin.exceptions import LinchpinError

"""
Provide valid context data to test against.

"""


class ContextData(object):

    def __init__(self, parser=ConfigParser.ConfigParser):


        self.lib_path = '{0}'.format(os.path.dirname(
            os.path.realpath(__file__))).rstrip('/')

        current_path = os.path.dirname(os.path.realpath(__file__))
        constants_path = '{0}/../../'.format(current_path)

        self.constants_path = '{0}'.format(os.path.dirname(
            constants_path)).rstrip('/')

        self.logfile = tempfile.mktemp(suffix='.log', prefix='linchpin')
        self.parser = parser()

        self.cfg_data = {}
        self._load_constants()


    def _load_constants(self):
        """
        Create self.cfgs with defaults from the linchpin constants file.
        """

        constants_file = '{0}/linchpin.constants'.format(self.constants_path)
        constants_file = os.path.realpath(os.path.expanduser(constants_file))
        self._parse_config(constants_file)


    def load_config_data(self, provider='dummy'):
        """
        Load a test-based linchpin.conf into both a configs and evars
        dictionary to represent a configuration file

        """


        expanded_path = None
        config_found = False

        # simply modify this variable to adjust where linchpin.conf can be found
        CONFIG_PATH = [
            '{0}/{1}/conf/linchpin.conf'.format(self.lib_path, provider)
        ]

        for path in CONFIG_PATH:
            expanded_path = (
                "{0}".format(os.path.realpath(os.path.expanduser(path))))

            if os.path.exists(expanded_path):
                self._parse_config(expanded_path)


        # override logger file
        self.cfg_data['logger'] = dict()
        self.cfg_data['logger']['file'] = self.logfile

        self.evars = self.cfg_data.get('evars', {})


    def _parse_config(self, path):
        """
        Parse configs into the self.cfg_data dict from provided path.

        :param path: A path to a config to parse
        """

        try:
            config = ConfigParser.ConfigParser()
            f = open(path)
            config.readfp(f)
            f.close()

            for section in config.sections():
                if not self.cfg_data.get(section):
                    self.cfg_data[section] = {}

                for k in config.options(section):
                    if section == 'evars':
                        try:
                            self.cfg_data[section][k] = (
                                config.getboolean(section, k)
                            )
                        except ValueError:
                            self.cfg_data[section][k] = config.get(section, k)
                    else:
                        try:
                            self.cfg_data[section][k] = config.get(section, k)
                        except ConfigParser.InterpolationMissingOptionError:
                            value = config.get(section, k, raw=True)
                            self.cfg_data[section][k] = value.replace('%%', '%')

        except ConfigParser.InterpolationSyntaxError as e:
            raise LinchpinError('Unable to parse configuration file properly:'
                                ' {0}'.format(e))


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


    def create_config(self, config_data=None):

        """
        Creates a config object using ConfigParser from the config_data object

        """

        if not config_data:
            config_data = self.cfg_data

        # we know that data is a dict, containing dicts
        try:
            for k, v in iteritems(config_data):
                self.parser.add_section(k)
                for kv, vv in iteritems(v):
                    if type(vv) is not str:
                        vv = str(vv)
                    self.parser.set(k, kv, vv)
        except ValueError:
            pass
