import os
import urlparse
import tempfile

from fetch import Fetch
from linchpin.exceptions import LinchpinError


class FetchLocal(Fetch):

    def __init__(self, ctx, fetch_type, src, dest, cache_dir, root):
        super(FetchLocal, self).__init__(ctx, fetch_type, dest, root)

        self.cache_dir = os.path.join(cache_dir, "local")
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

        src_parse = urlparse.urlparse(src)
        self.src = os.path.abspath(os.path.join(
            src_parse.netloc, src_parse.path))

        if not os.path.exists(self.src):
            raise LinchpinError('{0} is not a valid path'.format(src))
        if os.path.samefile(self.src, self.dest):
            raise LinchpinError("Provide two different locations")


    def fetch_files(self):
        paths = []
        if self.root is not None:
            for ext in self.root:
                paths.append(os.path.join(self.src, ext.lstrip('/')))
        else:
            paths.append(self.src)

        for path in paths:
            key = "{0}|{1}".format(self.dest.replace(':', ''),
                                   path.replace(':', ''))
            fetch_dir = self.cfgs["local"].get(key, None)
            if not fetch_dir:
                td = tempfile.mkdtemp(prefix="local_", dir=self.cache_dir)
                self.write_cfg("local", key, td)
            else:
                td = fetch_dir

            self.copy_dir(path, td)
            self.tempdirs.append(td)
