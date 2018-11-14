import os
import ast
import shutil

try:
    import configparser
except ImportError:
        import ConfigParser as configparser


from abc import ABCMeta, abstractmethod
from linchpin.exceptions import LinchpinError


class Fetch(object):
    __metaclass__ = ABCMeta

    def __init__(self, ctx, fetch_type, dest, root='', root_ws='', ref=None):
        """
        """

        self.ctx = ctx
        self.fetch_type = fetch_type
        self.root = root
        self.root_ws = root_ws
        self.ref = ref
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
            src_dir = '{0}/{1}'.format(self.td, self.root)
            self.copy_dir(src_dir, self.dest)
        else:
            self.transfer_section(self.fetch_type)


    def transfer_section(self, section):
        dest_dir = os.path.join(self.dest, section)
        dir_exists = True
        if section not in os.listdir(self.dest):
            dir_exists = False
            os.makedirs(dest_dir)

        src_dir = os.path.join('{0}/{1}'.format(self.td, self.root), section)
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
            for f in files:
                rel_path = root.replace(src, '').lstrip(os.sep)
                dest_path = os.path.join(dest, rel_path)

                if not os.path.isdir(dest_path):
                    try:
                        os.makedirs(dest_path)
                    except OSError as e:
                        if e.errno == 17:
                            raise LinchpinError('File {0} already exists'
                                                ' in destination directory'
                                                .format(e.filename))

                s_file = os.path.join(root, f)
                d_file = os.path.join(dest_path, f)

                # fetch.always_update_workspace flag determines whether or
                # not to update. can be overwritten on the cli with --nocache.
                cache_ws = (ast.literal_eval(
                            self.ctx.get_cfg('fetch', 'cache_ws',
                                             default='True')))

                cp_files = False
                if not cache_ws:
                    cp_files = True
                else:
                    if not os.path.exists(d_file):
                        cp_files = True
                    else:
                        cache_days = int(self.ctx.get_cfg('fetch',
                                                          'cache_days',
                                                          default=1))
                        s_file_mtime = int(os.stat(s_file).st_mtime)
                        d_file_mtime = int(os.stat(d_file).st_mtime)

                        if (s_file_mtime - d_file_mtime) >= cache_days:
                            cp_files = True

                if cp_files:

                    try:
                        if (os.path.islink(s_file) and
                                os.path.exists(os.readlink(s_file))):
                            s_file = os.readlink(s_file)

                        shutil.copy2(s_file, d_file)
                    except (IOError, OSError) as e:
                        self.ctx.log_state(e)


    def read_cfg(self):
        config = configparser.SafeConfigParser()
        config.optionxform = str

        cfgs = {}
        if not os.path.exists(self.config_path):
            config.add_section('http')
            config.add_section('git')
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
        config = configparser.SafeConfigParser()
        config.optionxform = str
        config.read(self.config_path)
        config.set(section, key, value)

        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
