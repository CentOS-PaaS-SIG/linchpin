#!/usr/bin/env python

import os
import sys
import click
import shutil
import logging
import ConfigParser

from distutils import dir_util
from jinja2 import Environment, PackageLoader

from linchpin.api import LinchpinError
from linchpin.cli import LinchpinCli
from linchpin.version import __version__

class LinchpinContext(object):
    """
    LPContext object, which will be used to manage the cli,
    and load the configuration file.
    """


    def __init__(self):
        """
        Initializes basic variables, loads the configuration, sets up logging.
        """

        self.version = __version__
        self.verbose = False

        # load all configurations
        self._load_config()

        # setup logging
        self._setup_logging(eval(self.cfgs['logger']['enable']))

        # create a LinchpinCLI object
        self.lpcli = LinchpinCli(self)


    def _load_config(self):
        """
        Create self.cfgs from the linchpin configuration file.

        These are the only hardcoded values, which are used to find the config
        file. The search path, is a first found of the following:

        """

        self.cfgs = {}
        self.lib_path = '{0}/'.format(os.path.dirname(
            os.path.realpath(__file__))).rstrip('/')

        expanded_path = None
        config_found = False


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
            if not self.cfgs.has_key(section):
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


    def _setup_logging(self, enable_logging=True):
        """
        Create a local log file to manage debugging and the like

        These are the only hardcoded values, which are used to find the config
        file. The search path, is a first found of the following:

        """
        self.enable_logging = enable_logging

        if self.enable_logging:

            # create logger
            self.logger = logging.getLogger('linchpin')
            self.logger.setLevel(eval(self.cfgs['logger']['loglevel']))

            fh = logging.FileHandler(self.cfgs['logger']['file'])
            fh.setLevel(eval(self.cfgs['logger']['loglevel']))

            formatter = logging.Formatter(self.cfgs['logger']['format'])
            fh.setFormatter(formatter)

            self.logger.addHandler(fh)


    def log(self, msg, **kwargs):
        """Logs a message to a logfile"""

        lvl = kwargs.get('level')

        if lvl is None:
            lvl = logging.INFO

        if self.verbose:
            click.echo(msg, file=sys.stderr)

        if not self.enable_logging:
            return

        self.logger.log(lvl, msg)

    def log_state(self, msg, lvl=logging.INFO):
        """Logs a message to stdout."""

        click.echo(msg)
        self.log('STATE - {0}'.format(msg), level=lvl)

    def log_info(self, msg):
        """Logs a message to """
        self.log(msg, level=logging.INFO)

    def log_debug(self, msg):
        """Logs a message to stderr."""
        self.log(msg, level=logging.DEBUG)


