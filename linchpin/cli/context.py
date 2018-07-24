#!/usr/bin/env python

import os
import ast
import errno
import logging

from linchpin.context import LinchpinContext


class LinchpinCliContext(LinchpinContext):
    """
    Context object, which will be used to manage the cli,
    and load the configuration file
    """


    def __init__(self):
        """
        Initializes basic variables
        """

        # The following values are set in the parent class
        #
        # self.version = __version__
        # self.verbosity = 1
        #
        # self.lib_path = '{0}'.format(os.path.dirname(
        #                              os.path.realpath(__file__)))
        #
        # self.cfgs = {}
        # Load constants from linchpin.constants file.
        # self._load_constants()

        LinchpinContext.__init__(self)


    def load_config(self, lpconfig=None):
        """
        Update self.cfgs from the linchpin configuration file (linchpin.conf).

        The following paths are used to find the config file.
        The search path defaults to the first-found order::

          * /etc/linchpin.conf
          * /linchpin/library/path/linchpin.conf
          * <workspace>/linchpin.conf

        An alternate search_path can be passed.

        :param search_path: A list of paths to search a linchpin config
        (default: None)
        """

        if not self.workspace:
            self.workspace = os.path.realpath(os.path.curdir)

        expanded_path = None

        if lpconfig:
            CONFIG_PATH = [lpconfig]
        else:
            CONFIG_PATH = [
                '/etc/linchpin.conf',
                '~/.config/linchpin/linchpin.conf',
                '{0}/linchpin.conf'.format(self.workspace)
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

        for path in existing_paths:
            self._parse_config(path)


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
        self.set_evar('workspace', workspace)


    def setup_logging(self):

        """
        Setup logging to a file, console, or both. Modifying the `linchpin.conf`
        appropriately will provide functionality.

        """

        self.enable_logging = ast.literal_eval(
            self.cfgs['logger'].get('enable', 'True'))

        if self.enable_logging:

            # create logger
            self.logger = logging.getLogger('lp_logger')
            self.logger.setLevel(eval(self.cfgs['logger'].get('level',
                                                              'logging.DEBUG')))

            logfile = os.path.realpath(os.path.expanduser(
                self.cfgs['logger'].get('file', 'linchpin.log')))

            logdir = os.path.dirname(logfile)

            if not os.path.exists(logdir):
                try:
                    os.makedirs(logdir)
                except OSError as exc:
                    if (exc.errno == errno.EEXIST and
                            os.path.isdir(logdir)):
                        pass
                    else:
                        raise


            fh = logging.FileHandler(logfile)
            fh.setLevel(eval(self.cfgs['logger'].get('level',
                                                     'logging.DEBUG')))
            formatter = logging.Formatter(
                self.cfgs['logger'].get('format',
                                        '%(levelname)s'
                                        ' %(asctime)s %(message)s'))
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

        .. note:: Only msg_type `STATE` is currently implemented.
        """

        lvl = kwargs.get('level')
        msg_type = kwargs.get('msg_type')

        if lvl is None:
            lvl = logging.INFO

        if self.verbosity > 1 and not msg_type:
            self.console.log(logging.INFO, msg)

        state_msg = msg
        if msg_type == 'STATE':
            state_msg = 'STATE - {0}'.format(msg)
            self.console.log(logging.INFO, msg)

        if self.enable_logging:
            self.logger.log(lvl, state_msg)


    def log_state(self, msg):
        """Logs a message to stdout"""

        self.log(msg, msg_type='STATE', level=logging.DEBUG)

    def log_info(self, msg):
        """Logs an INFO message """
        self.log(msg, level=logging.INFO)

    def log_debug(self, msg):
        """Logs a DEBUG message"""
        self.log(msg, level=logging.DEBUG)
