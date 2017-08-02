import os
import sys
import shutil
import configparser

from abc import ABCMeta, abstractmethod
from linchpin.exceptions import LinchpinError

class Fetch(object):
    __metaclass__ = ABCMeta

    def __init__(self, ctx, fetch_type, dest, root):
        self.ctx = ctx
        self.fetch_type = fetch_type
        self.root = root
        self.tempdirs = []
        self.dest = os.path.abspath(os.path.realpath(dest))
        
        self.config_path = os.path.abspath(os.path.join(os.path.expanduser('~'),
                        '.cache/linchpin/fetch.conf'))
        self.cfgs = self.read_cfg()

    @abstractmethod
    def fetch_files(self):
        pass

    def copy_files(self):
        if self.fetch_type == 'workspace':
            workspace_dirs = [
                    self.ctx.get_evar("topologies_folder"),
                    self.ctx.get_evar("layouts_folder"),
                    self.ctx.get_evar("resources_folder"),
                    self.ctx.get_evar("hooks_folder"),
                    ]
            for path in self.tempdirs:
                pinfile = os.path.join(path, self.ctx.get_cfg("init",
                    "pinfile"))
                if os.path.exists(pinfile):
                    shutil.copy2(pinfile, self.dest)
            for section in workspace_dirs:
                self.transfer_section(section)
        else:
            self.transfer_section(self.fetch_type)


    def transfer_section(self, section):

        dest_dir = os.path.join(self.dest, section)
        dir_exists = True
        if section not in os.listdir(self.dest):
            dir_exists = False
            os.mkdir(dest_dir)

        for path in self.tempdirs:
            src_dir = os.path.join(path, section)
            if not os.path.exists(src_dir):
                if not dir_exists:
                    shutil.rmtree(dest_dir)
                raise LinchpinError('The {0} directory does not exist in '
                        '{1}'.format(self.fetch_type, self.src))
            self.transfer_files(src_dir, dest_dir)

    def transfer_files(self, src, dest):
        for item in os.listdir(src):
            try:
                s = os.path.join(src, item)
                d = os.path.join(dest, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            except OSError as e:
                    if e.errno == 17:
                        self.ctx.log_state('The {0} directory already'
                                ' exists'.format(item))
    def read_cfg(self):
        config = configparser.ConfigParser(delimiters=('='))
        config.optionxform = str

        cfgs = {}
        if not os.path.exists(self.config_path):
            config['http'] = {}
            config['git'] = {}
            config['local'] = {}
            with open(self.config_path, 'w') as configfile:
                config.write(configfile)
            print "config created"
        else:
            config.read(self.config_path)

        for section in config.sections():
            cfgs[section] = {}
            if config.items(section) is None:
                continue
            for k, v in config.items(section):
                cfgs[section][k] = v
            
        
        print "config read"
        for section in config.sections():
            print "SECTION: " + section
            for item in config[section]:
                print 'key: {0}, value: {1}'.format(item,
                        config[section][item])
        return cfgs

    def write_cfg(self, section, key, value):
        config = configparser.ConfigParser(delimiters=('='))
        config.optionxform = str
        config.read(self.config_path)
        config[section][key] = value

        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
