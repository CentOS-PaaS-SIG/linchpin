import os
import subprocess
import tempfile
from fetch import Fetch

class FetchGit(Fetch):
    def __init__(self, ctx, fetch_type, src, dest, cache_dir, root):
        super(FetchGit, self).__init__(ctx, fetch_type, dest, root)
        self.src = src

        self.cache_dir = os.path.join(cache_dir, "git")
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

    def fetch_files(self):
        td = self.call_clone()
        if self.root is not None:
            for ext in self.root:
                self.tempdirs.append(os.path.join(td, ext.lstrip('/')))
        else:
            self.tempdirs.append(td)


    def call_clone(self):
        tempdir = tempfile.mkdtemp(prefix="git_", dir=self.cache_dir)
        subprocess.call(['git', 'clone', '--quiet', self.src, tempdir])
        return tempdir
