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
            for path in self.tempdirs:
                self.copy_dir(path, self.dest)
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
            self.copy_dir(src_dir, dest_dir)

    def copy_dir(self, src, dest):
        for root, dirs, files in os.walk(src):
            files = [f for f in files if not f[0] == '.']
            dirs[:] = [d for d in dirs if not d[0] == '.']
            if not os.path.isdir(root):
                os.makedirs(root)
            for file in files:
                rel_path = root.replace(src, '').lstrip(os.sep)
                dest_path = os.path.join(dest, rel_path)

                if not os.path.isdir(dest_path):
                    os.makedirs(dest_path)

                shutil.copyfile(os.path.join(root, file), os.path.join(dest_path, file))

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
        else:
            config.read(self.config_path)

        for section in config.sections():
            cfgs[section] = {}
            if config.items(section) is None:
                continue
            for k, v in config.items(section):
                cfgs[section][k] = v
        
        return cfgs

    def write_cfg(self, section, key, value):
        config = configparser.ConfigParser(delimiters=('='))
        config.optionxform = str
        config.read(self.config_path)
        config[section][key] = value

        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
