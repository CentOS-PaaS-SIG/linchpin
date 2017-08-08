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
        if self.root is not None:
            for ext in self.root:
                src = os.path.join(self.src, ext.lstrip('/'))
                key = "{0}|{1}".format(self.dest.replace(':', ''),
                                       src.replace(':', ''))
                fetch_dir = self.cfgs["http"].get(key, None)

                td = self.call_wget(src, fetch_dir)
                self.tempdirs.append(td)

                if not fetch_dir:
                    self.write_cfg("http", key, td)
        else:
            key = "{0}|{1}".format(self.dest.replace(':', ''),
                                   self.src.replace(':', ''))
            fetch_dir = self.cfgs["http"].get(key, None)

            td = self.call_wget(self.src, fetch_dir)
            self.tempdirs.append(td)

            if not fetch_dir:
                self.write_cfg("http", key, td)

    def call_wget(self, src, fetch_dir=None):
        list_args = src.split('/')
        list_args = list_args[3:]
        tempdir = None

        if fetch_dir is None:
            tempdir = tempfile.mkdtemp(prefix="http_", dir=self.cache_dir)
            wget_args = ['wget', '-r', '-np', '-nH', '-q', '--reject', 'html',
                         '--cut-dirs={0}'.format(len(list_args)),
                         src, '-P', tempdir]
        else:
            tempdir = fetch_dir
            wget_args = ['wget', '-r', '-np', '-N', '-nH', '-q', '--reject',
                         'html', '--cut-dirs={0}'.format(len(list_args)), src,
                         '-P', tempdir]

        retval = subprocess.call(wget_args)

        if retval != 0:
            try:
                os.rmdir(tempdir)
            except OSError:
                pass
            raise LinchpinError('Unable to fetch files with the following'
                                ' command:\n{0}'.format(" ".join(wget_args)))
        return tempdir
