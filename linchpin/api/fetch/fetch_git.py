import os
import subprocess
import tempfile

from fetch import Fetch
from linchpin.exceptions import LinchpinError


class FetchGit(Fetch):
    def __init__(self, ctx, fetch_type, src, dest, cache_dir, root):
        super(FetchGit, self).__init__(ctx, fetch_type, dest, root)
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
        key = "{0}|{1}".format(self.dest.replace(':', ''),
                               self.src.replace(':', ''))

        fetch_dir = self.cfgs["git"].get(key, None)
        td = self.call_clone(fetch_dir)

        if fetch_dir is None:
            self.write_cfg("git", key, td)

        if self.root is not None:
            for ext in self.root:
                self.tempdirs.append(os.path.join(td, ext.lstrip('/')))
        else:
            self.tempdirs.append(td)


    def call_clone(self, fetch_dir=None):
        if fetch_dir:
            retval = subprocess.call(
                ['git', '-C', fetch_dir, 'pull', '--quiet'])
            tempdir = fetch_dir
        else:
            tempdir = tempfile.mkdtemp(prefix="git_", dir=self.cache_dir)
            retval = subprocess.call(
                ['git', 'clone', '--quiet', self.src, tempdir])

        if retval != 0:
            raise LinchpinError("Unable to clone {0}".format(self.src))
        return tempdir
