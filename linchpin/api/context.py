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


    def load_config(self, lpconfig=None):
        """
        Create self.cfgs and self.evars with hardcoded values

        These are the only hardcoded values, which are used to find the config
        file. The search path, is a first found of the following:

        """

        self.cfgs = OrderedDict()

        self.cfgs['lp'] = { 'pkg': 'linchpin' }
        self.cfgs['ansible'] = { 'console', 'False' }
        self.cfgs['evars'] = {
            'resources_folder': 'resources',
            'inventories_folder': 'inventories',
        }

        self.evars = self.cfgs.get('evars')


    def setup_logging(self):

        """
        .. attention:: Abstract method must be implemented in a subclass

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
