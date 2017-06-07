#!/usr/bin/env python

import os
import sys
import ast
import shutil
import logging

from distutils import dir_util
from collections import OrderedDict
from jinja2 import Environment, PackageLoader

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser

from linchpin.api import LinchpinError
from linchpin.version import __version__


class LinchpinContext(object):

    """
    LinchpinContext object, which will be used to manage the cli,
    and load the configuration file.
    """


    def __init__(self):
        """
        Initializes basic variables
        """

        self.version = __version__
        self.verbose = False

        lib_path = '{0}'.format(os.path.dirname(
            os.path.realpath(__file__))).rstrip('/')
        self.lib_path = os.path.realpath(os.path.join(lib_path, os.pardir))

        self.workspace = os.path.realpath(os.path.curdir)


    def load_config(self, lpconfig=None):
        """
        Create self.cfgs from the linchpin configuration file.

        These are the only hardcoded values, which are used to find
        the config file. The linchpin.conf file is found
        at `/linchpin/library/path/linchpin.conf`.

        Alternatively, a full path to the linchpin configuration file
        can be passed.

        :param lpconfig: absolute path to a linchpin config (default: None)

        """

        self.cfgs = {}

        expanded_path = None
        config_found = False

        if lpconfig:
            CONFIG_PATH = [ lpconfig ]
        else:
            # simply modify this variable to adjust where linchpin.conf can be found
            CONFIG_PATH = [
                '{0}/linchpin.conf'.format(self.lib_path)
            ]

        for path in CONFIG_PATH:
            expanded_path = (
                "{0}".format(os.path.realpath(os.path.expanduser(path))))

            # implement first found
            if os.path.exists(expanded_path):
                # logging before the config file is setup doesn't work
                # if messages are needed before this, use print.
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
            if section not in self.cfgs:
                self.cfgs[section] = {}

            # add evars to the ansible extra_vars when running a playbook.
            for k, v in config.items(section):
                if section != 'evars':
                    self.cfgs[section][k] = v
                else:
                    try:
                        self.cfgs[section][k] = config.getboolean(section, k)
                    except ValueError as e:
                        self.cfgs[section][k] = v


    def load_global_evars(self):

        """
        Instantiate the evars variable, then load the variables from the
        'evars' section in linchpin.conf. This will then be passed to
        invoke_linchpin, which passes them to the Ansible playbook as needed.

        """

        self.evars = self.cfgs.get('evars', {})


    def get_cfg(self, section=None, key=None, default=None):
        """
        Get cfgs value(s) by section and/or key, or the whole cfgs object

        :param section: section from ini-style config file

        :param key: key to get from config file, within section

        :param default: default value to return if nothing is found.
        Does not apply if section is not provided.
        """

        if section:
            s = self.cfgs.get(section, default)
            if key and s:
                return self.cfgs[section].get(key, default)
            return s
        return self.cfgs


    def set_cfg(self, section, key, value):
        """
        Set a value in cfgs. Does not persist into a file,
        only during the current execution.

        :param section: section within ini-style config file
        :param key: key to use
        :param value: value to set into section within config file
        """

        if not self.cfgs.get(section):
            self.cfgs.update({section: {}})

        self.cfgs[section][key] = value


    def get_evar(self, key=None, default=None):
        """
        Get the current evars (extra_vars)

        :param key: key to use

        :param default: default value to return if nothing is found (default: None)
        """

        if key:
            return self.evars.get(key, default)

        return self.evars


    def set_evar(self, key, value):
        """
        Set a value into evars (extra_vars). Does not persist into a file,
        only during the current execution.

        :param key: key to use

        :param value: value to set into evars
        """

        self.set_cfg('evars', key, value)


    def setup_logging(self):

        """
        .. attention:: Please implement this function in a subclass

        Setup logging to the console only

        """

        self.console = logging.getLogger('lp_console')
        self.console.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
        ch.setFormatter(formatter)

        self.console.addHandler(ch)


    def log(self, msg, **kwargs):
        """
        Logs a message to a logfile

        :param msg: message to output to log

        :param level: keyword argument defining the log level

        """

        lvl = kwargs.get('level')

        if lvl is None:
            lvl = logging.INFO

        self.console.log(logging.INFO, msg)


    def log_info(self, msg):
        """Logs a message"""

        self.log(msg, level=logging.INFO)


    def log_debug(self, msg):
        """Logs a message"""

        self.log(msg, level=logging.DEBUG)


    def log_state(self, msg):
        """Logs a debug message"""

        self.log_debug(msg)
