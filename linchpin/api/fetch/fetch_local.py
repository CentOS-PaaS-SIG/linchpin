import os
import sys
import shutil
import urlparse
from fetch import Fetch


class FetchLocal(Fetch):

    def __init__(self, ctx, fetch_type, src, dest):
        self.ctx = ctx
        self.fetch_type = fetch_type

        src_parse = urlparse.urlparse(src)
        self.src = os.path.abspath(os.path.join(src_parse.netloc, src_parse.path))
        self.dest = os.path.abspath(os.path.realpath(dest))

    
        if not os.path.exists(self.src):
            ctx.log_state('{0} is not a valid path'.format(src))
            sys.exit(1)
        if not os.path.exists(self.dest):
            ctx.log_state('{0} is not a valid path'.format(self.dest))
            sys.exit(1)
        if os.path.samefile(self.src, self.dest):
            ctx.log_state("Provide two different locations")
            sys.exit(1)


    def fetch_files(self):
        for item in os.listdir(self.src):
            try:
                s = os.path.join(self.src, item)
                d = os.path.join(self.dest, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else shutil.copy2(s, d)
            except OSEerror as e:
                if e.errno == 17:
                    self.ctx.log_state('The {0} directory already'
                    'exists'.format(item))
