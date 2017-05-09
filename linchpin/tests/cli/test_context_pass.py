import os

from nose.tools import *

import logging
from unittest import TestCase

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser

from linchpin.cli.context import LinchpinCliContext
from linchpin.tests.mockdata.context import ContextData


def test_context_create():

    lpc = LinchpinCliContext()
    assert_equal(isinstance(lpc, LinchpinCliContext), True)


def setup_load_config():

    """
    Perform setup of ContextData() object, and run get_temp_filename()
    """

    global config_path
    global config_data

    cd = ContextData()
    cd.parse_config()
    config_path = cd.get_temp_filename()
    config_data = cd.config_data
    cd.write_config_file(config_path)


@with_setup(setup_load_config)
def test_load_config():

    lpc = LinchpinCliContext()
    lpc.load_config(lpconfig=config_path)

    assert_dict_equal.__self__.maxDiff = None
    assert_dict_equal(config_data, lpc.cfgs)


def setup_load_evars():

    """
    Perform setup of ContextData() object, and run get_temp_filename()
    """

    global cfg_path
    global evars_data

    cd = ContextData(parser=ConfigParser.RawConfigParser)
    cd.create_context_evars()
    cfg_path = cd.get_temp_filename()
    evars_data = cd.evars
    cd.write_config_file(cfg_path)


@with_setup(setup_load_evars)
def test_load_global_evars():

    lpc = LinchpinCliContext()
    lpc.load_config(cfg_path)
    lpc.load_global_evars()

    assert_dict_equal(evars_data, lpc.evars)


def setup_logging_setup():

    """
    Setup the logger configuration
    """

    global cfg_path
    global logfile

    cd = ContextData()
    cd.parse_config()
    cfg_path = cd.get_temp_filename()
    logfile = cd.logfile
    cd.write_config_file(cfg_path)


@with_setup(setup_logging_setup)
def test_logging_setup():


    lpc = LinchpinCliContext()
    lpc.load_config(cfg_path)
    lpc.setup_logging()

    assert os.path.isfile(logfile)


@with_setup(setup_logging_setup)
def test_log_msg():

    # This test assumes the default message format found around line 139
    # of linchpin/cli/context.py

    lvl=logging.DEBUG
    msg = 'Test Msg'
    regex = '^{0}.*{1}'.format(logging.getLevelName(lvl), msg)

    lpc = LinchpinCliContext()
    lpc.load_config(cfg_path)
    lpc.setup_logging()
    lpc.log(msg, level=lvl)

    with open(logfile) as f:
        line = f.readline()

    assert_regexp_matches(line, regex)

@with_setup(setup_logging_setup)
def test_log_state():

    lvl=logging.DEBUG
    msg = '{0}: State Msg'.format(logging.getLevelName(lvl))
    regex = '^{0}.*STATE - {1}'.format(logging.getLevelName(lvl), msg)

    lpc = LinchpinCliContext()
    lpc.load_config(cfg_path)
    lpc.setup_logging()
    lpc.log_state(msg)

    with open(logfile) as f:
        line = f.readline()

    assert_regexp_matches(line, regex)

@with_setup(setup_logging_setup)
def test_log_info():

    lvl=logging.INFO
    msg = 'Info Msg'
    regex = '^{0}.*{1}'.format(logging.getLevelName(lvl), msg)

    lpc = LinchpinCliContext()
    lpc.load_config(cfg_path)
    lpc.setup_logging()
    lpc.log_info(msg)

    with open(logfile) as f:
        line = f.readline()

    assert_regexp_matches(line, regex)

@with_setup(setup_logging_setup)
def test_log_debug():

    lvl=logging.DEBUG
    msg = 'Debug Msg'
    regex = '^{0}.*{1}'.format(logging.getLevelName(lvl), msg)

    lpc = LinchpinCliContext()
    lpc.load_config(cfg_path)
    lpc.setup_logging()
    lpc.log_debug(msg)


    with open(logfile) as f:
        line = f.readline()

    assert_regexp_matches(line, regex)


def main():

    tlc = TestLinchpinCliContext()
    tlc.setup_load_config()
    tlc.test_load_config()

if __name__ == '__main__':
    sys.exit(main())
