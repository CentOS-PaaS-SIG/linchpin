#!/usr/bin/env python

import ast
import logging

from linchpin.api.context import LinchpinContext


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
        # self.verbose = False
        #
        # lib_path = '{0}'.format(os.path.dirname(
        #                       os.path.realpath(__file__))).rstrip('/')
        # self.lib_path = os.path.realpath(os.path.join(lib_path, os.pardir))
        #
        # self.cfgs = {}

        LinchpinContext.__init__(self)


    def load_config(self, lpconfig=None):
        return super(LinchpinCliContext, self).load_config(lpconfig)

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

            fh = logging.FileHandler(self.cfgs['logger'].get('file',
                                                             'linchpin.log'))
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

        if self.verbose and not msg_type:
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
