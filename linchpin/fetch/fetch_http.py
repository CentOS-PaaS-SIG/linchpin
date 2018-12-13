import os
import subprocess
import tempfile
import requests

from .fetch import Fetch
from linchpin.exceptions import LinchpinError


class FetchHttp(Fetch):

    def __init__(self, ctx, fetch_type, src, dest, cache_dir, root='',
                 root_ws='', ref=None):
        super(FetchHttp, self).__init__(ctx, fetch_type, dest, root=root,
                                        root_ws=root_ws, ref=ref)

        self.cache_dir = os.path.join(cache_dir, "http")
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        try:
            r = requests.get(src)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            raise LinchpinError("An HTTP error occurred")
        except requests.exceptions.RequestException:
            raise LinchpinError("Could not connect to given URL")

        if r.status_code != 200:
            raise LinchpinError("The entered url is invalid")

        self.src = src.rstrip('/')


    def fetch_files(self):

        key = "{0}|{1}".format(self.dest.replace(':', ''),
                               self.src.replace(':', ''))

        fetch_dir = self.cfgs["http"].get(key, None)
        self.td = self.call_wget(fetch_dir)

        self.td_w_root = '{0}/{1}/'.format(self.td, self.root)

        if not fetch_dir:
            self.write_cfg("http", key, self.td)


    def call_wget(self, fetch_dir=None):

        src_w_root = '{0}/{1}'.format(self.src, self.root)
        tempdir = None

        # globs to reject
        rej = '*html*'


        if not fetch_dir:
            fetch_dir = tempfile.mkdtemp(prefix="http_", dir=self.cache_dir)

        wget_args = ['wget', '-r', '-np', '-nH', '-q', '--reject',
                     rej, src_w_root, '-P', fetch_dir]

        retval = subprocess.call(wget_args)



        if retval != 0:
            try:
                os.rmdir(tempdir)
            except OSError:
                pass
            raise LinchpinError('Unable to fetch files with the following'
                                ' command:\n{0}'.format(" ".join(wget_args)))
        return fetch_dir
