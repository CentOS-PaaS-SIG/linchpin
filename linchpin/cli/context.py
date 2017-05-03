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

from linchpin.api.context import LinchpinContext
from linchpin.api import LinchpinError
from linchpin.version import __version__


class LinchpinCliContext(LinchpinContext):
    """
    LPContext object, which will be used to manage the cli,
    and load the configuration file.
    """


    def __init__(self):
        """
        Initializes basic variables
        """

        LinchpinContext.__init__(self)


    def load_config(self, lpconfig=None):
        """
        Create self.cfgs from the linchpin configuration file.

        These are the only hardcoded values, which are used to find the config
        file. The search path, is a first found of the following:

        """

        self.cfgs = OrderedDict()

        lib_path = '{0}'.format(os.path.dirname(
            os.path.realpath(__file__))).rstrip('/')
        self.lib_path = os.path.abspath(os.path.join(lib_path, os.pardir))

        expanded_path = None
        config_found = False

        if lpconfig:
            CONFIG_PATH = [ lpconfig ]
        else:
            # simply modify this variable to adjust where linchpin.conf can be found
            CONFIG_PATH = [
                '{0}/linchpin.conf'.format(
                            os.path.realpath(os.path.expanduser(os.path.curdir))),
                '~/.linchpin.conf',
                '/etc/linchpin.conf',
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

        self.evars = self.cfgs.get('evars', None)


    def setup_logging(self):

        """
        Setup logging to a file, console, or both.  Modifying the linchpin.conf
        appropriately will provide functionality.

        """

        self.enable_logging = ast.literal_eval(self.cfgs['logger'].get('enable', 'True'))

        if self.enable_logging:

            # create logger
            self.logger = logging.getLogger('lp_logger')
            self.logger.setLevel(eval(self.cfgs['logger'].get('level',
                                                            'logging.DEBUG')))

            fh = logging.FileHandler(self.cfgs['logger'].get('file',
                                                            'linchpin.log'))
            fh.setLevel(eval(self.cfgs['logger'].get('level',
                                                    'logging.DEBUG')))
            formatter = logging.Formatter(
                            self.cfgs['logger'].get('format',
                            '%(levelname)s %(asctime)s %(message)s'))
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)


        self.console = logging.getLogger('lp_console')
        self.console.setLevel(eval(self.cfgs['console'].get('level',
                                                        'logging.INFO')))

        ch = logging.StreamHandler()
        ch.setLevel(eval(self.cfgs['console'].get('level',
                                                'logging.INFO')))
        formatter = logging.Formatter(
                        self.cfgs['console'].get('format', '%(message)s'))
        ch.setFormatter(formatter)
        self.console.addHandler(ch)


    def log(self, msg, **kwargs):
        """
        Logs a message to a logfile or the console

        :param msg: message to log

        :param lvl: keyword argument defining the log level

        :param msg_type: keyword argument giving more flexibility.
        Only `STATE` is currently implemented.
        """

        lvl = kwargs.get('level')
        msg_type = kwargs.get('msg_type')

        if lvl is None:
            lvl = logging.INFO

        if self.verbose and not msg_type:
            self.console.log(logging.INFO, msg)

        state_msg = msg
        if msg_type == 'STATE':
            state_msg = 'STATE - {0}'.format(msg)
            self.console.log(logging.INFO, msg)

        if self.enable_logging:
            self.logger.log(lvl, state_msg)


    def log_state(self, msg):
        """Logs a message to stdout."""

        self.log(msg, msg_type='STATE', level=logging.DEBUG)

    def log_info(self, msg):
        """Logs a message to """
        self.log(msg, level=logging.INFO)

    def log_debug(self, msg):
        """Logs a message to stderr."""
        self.log(msg, level=logging.DEBUG)

