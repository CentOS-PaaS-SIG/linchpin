import os
import subprocess
import tempfile
import requests

from fetch import Fetch
from linchpin.exceptions import LinchpinError

class FetchHttp(Fetch):
    def __init__(self, ctx, fetch_type, src, dest, cache_dir, root):
        super(FetchHttp, self).__init__(ctx, fetch_type, dest, root)

        self.cache_dir = os.path.join(cache_dir, "http")
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        if requests.get(src).status_code != 200:
            raise LinchpinError("The entered url is invalid")
        self.src = src.rstrip('/')

    def fetch_files(self):
        if self.root is not None:
            for ext in self.root:
                src = os.path.join(self.src, ext.lstrip('/'))
                self.tempdirs.append(self.call_wget(src))
        else:
            self.tempdirs.append(self.call_wget(self.src))

    def call_wget(self, src):
        list_args = src.split('/')
        list_args = list_args[3:]
        tempdir = tempfile.mkdtemp(prefix="http_", dir=self.cache_dir)

        wget_args = ['wget', '-r', '-np', '-nH', '-q', '--reject', '*.html',
                '--cut-dirs={0}'.format(len(list_args)), src, '-P', tempdir]
        retval = subprocess.call(wget_args)

        if retval == 1:
            from shutil import rmtree
            raise LinchpinError('Unable to fetch files with the following'
                    ' command {0}'.format(wget_args.join(' ')))
            rmtree(tempdir)
        return tempdir
