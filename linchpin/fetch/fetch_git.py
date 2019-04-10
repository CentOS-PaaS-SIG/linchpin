import os
import subprocess
import tempfile

from .fetch import Fetch
from linchpin.exceptions import LinchpinError


class FetchGit(Fetch):

    def __init__(self, ctx, fetch_type, src, dest, cache_dir, root='',
                 root_ws='', ref=None):
        super(FetchGit, self).__init__(ctx, fetch_type, dest, root=root,
                                       root_ws=root_ws, ref=ref)
        self.src = src

        self.cache_dir = os.path.join(cache_dir, "git")
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)


    def fetch_files(self):
        # The key cannot contain ':' since linchpin does not support python 3.
        # Configparser uses ':' as a delimiter, which poses problem when using
        # urls in key during parsing. Delimiters can be specified when
        # initializing a configparser object in python 3 so this does not
        # become an issue.

        ref = 'None'
        if self.ref:
            ref = self.ref

        key = "{0}|{1}".format(self.src.replace(':', ''), ref)

        fetch_dir = self.cfgs["git"].get(key, None)
        self.td = self.call_clone(fetch_dir)

        self.td_w_root = '{0}/{1}'.format(self.td, self.root)

        if not fetch_dir:
            self.write_cfg("git", key, self.td)


    def call_clone(self, fetch_dir=None):

        ref = None
        src = self.src
        if self.ref:
            ref = self.ref
            src = '{0}@{1}'.format(self.src, ref)

        if fetch_dir and os.path.exists(fetch_dir):
            cmd = ['git', 'pull', '--quiet']
            retval = subprocess.call(cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     cwd=fetch_dir)
        else:
            if not fetch_dir:
                fetch_dir = tempfile.mkdtemp(prefix="git_", dir=self.cache_dir)

            cmd = ['git', 'clone', '--quiet', self.src]
            if ref:
                cmd.extend(['-b', ref])

            cmd.append(fetch_dir)

            retval = subprocess.call(cmd, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

        if retval != 0:
            raise LinchpinError("Unable to clone {0}".format(src))
        return fetch_dir
