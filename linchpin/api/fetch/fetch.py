import os
import sys
import shutil
from abc import ABCMeta, abstractmethod

class Fetch(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

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
        if section not in os.listdir(self.dest):
            os.mkdir(dest_dir)

        for path in self.tempdirs:
            src_dir = os.path.join(path, section)
            if not os.path.exists(src_dir):
                self.ctx.log_state('The {0} directory does not exist in '
                        '{1}'.format(self.fetch_type, self.src))
                sys.exit(1)
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
                                'exists'.format(item))
