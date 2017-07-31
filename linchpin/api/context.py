#!/usr/bin/env python

import os
import logging

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser

from linchpin.exceptions import LinchpinError
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

        self.cfgs = {}


    def load_config(self, lpconfig=None):
        """
        Create self.cfgs from the linchpin configuration file.

        .. note:: Overrides load_config in linchpin.api.LinchpinContext

        These are the only hardcoded values, which are used to find the config
        file. The search path consists of the following::

          * /linchpin/library/path/linchpin.conf
          * /etc/linchpin.conf
          * ~/.config/linchpin/linchpin.conf
          * path/to/workspace/linchpin.conf

        Linchpin will continuously override and extend the configuration as
        newer configurations are added and modified. Alternatively, a full path
        to the linchpin configuration file can be passed.

        :param lpconfig: absolute path to a linchpin config (default: None)

        """

        expanded_path = None

        if lpconfig:
            CONFIG_PATH = [lpconfig]
        else:
            # simply modify this variable to adjust where
            # linchpin.conf can be found
            CONFIG_PATH = [
                '{0}/linchpin.conf'.format(self.lib_path),
                '/etc/linchpin.conf',
                '~/.config/linchpin/linchpin.conf',
                '{0}/linchpin.conf'.format(self.workspace)
                # self.workspace is set in runcli beforehand, will never be None
            ]
        existing_paths = []
        for path in CONFIG_PATH:
            expanded_path = (
                "{0}".format(os.path.realpath(os.path.expanduser(path))))

            # implement first found
            if os.path.exists(expanded_path):
                # logging before the config file is setup doesn't work
                # if messages are needed before this, use print.
                existing_paths.append(expanded_path)
        if len(existing_paths) == 0:
            raise LinchpinError('Configuration file not found in'
                                ' path: {0}'.format(CONFIG_PATH))
        try:
            for path in existing_paths:
                config = ConfigParser.SafeConfigParser()
                f = open(path)
                config.readfp(f)
                f.close()

                for section in config.sections():
                    self.cfgs[section] = {}
                    for k, v in config.items(section):
                        if section != 'evars':
                            self.cfgs[section][k] = v
                        else:
                            try:
                                self.cfgs[section][k] = (
                                    config.getboolean(section, k)
                                )
                            except ValueError as e:
                                self.cfgs[section][k] = v
        except ConfigParser.InterpolationSyntaxError as e:
            raise LinchpinError('Unable to parse configuration file properly:'
                                ' {0}'.format(e))

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

        :param default: default value to return if nothing is found
        (default: None)
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


    @property
    def pinfile(self):

        """
        getter function for pinfile name
        """

        return self.get_cfg('init', 'pinfile')


    @pinfile.setter
    def pinfile(self, pinfile):

        """
        setter for workspace
        """

        self.set_cfg('init', 'pinfile', pinfile)


    @property
    def workspace(self):

        """
        getter function for workspace
        """

        return self.get_cfg('lp', 'workspace')


    @workspace.setter
    def workspace(self, workspace):

        """
        setter for workspace
        """

        self.set_cfg('lp', 'workspace', workspace)


    def setup_logging(self):

        """
        Setup logging to the console only

        .. attention:: Please implement this function in a subclass

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
        """Logs an INFO message"""

        self.log(msg, level=logging.INFO)


    def log_debug(self, msg):
        """Logs a DEBUG message"""

        self.log(msg, level=logging.DEBUG)


    def log_state(self, msg):
        """
        Logs nothing, just calls pass

        .. attention:: state messages need to be implemented in a subclass
        """

        pass
