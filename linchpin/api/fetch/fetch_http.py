import os
import subprocess
import tempfile
import requests
from fetch import Fetch

class FetchHttp(Fetch):
    def __init__(self, ctx, fetch_type, src, dest, cache_dir, root):
        self.ctx = ctx
        self.fetch_type = fetch_type
        self.dest = dest
        self.root = root
        self.tempdirs = []

        self.cache_dir = os.path.join(cache_dir, "http")
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        if requests.get(src).status_code != 200:
            self.ctx.log_state("The entered url is invalid")
            sys.exit(1)
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
            self.ctx.log_state("An error occurred while fetching files")
            rmtree(tempdir)
            sys.exit(1)
        return tempdir
