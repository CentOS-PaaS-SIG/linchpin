from linchpin.api.repository_controls.repository_control import RepositoryControl
import shutil
import os
import urlparse
import sys
        
class LocalRepositoryControl(RepositoryControl):
    
    def __init__(self, ctx, fetch_type, src, dest):
        self.ctx = ctx
        self.fetch_type = fetch_type
        src_parse = urlparse.urlparse(src)
        self.src = os.path.abspath(os.path.join(src_parse.netloc, src_parse.path))
        self.dest = dest.rstrip('/')

        if not os.path.exists(self.src):
            ctx.log_state('{0} is not a valid path'.format(src))
            sys.exit(1)
        if not os.path.exists(self.dest):
            ctx.log_state('{0} is not a valid path'.format(dest))
            sys.exit(1)
            

    def list_files(self):
        pass

    def fetch_files(self):
        if self.fetch_type == "workspace":
            for item in os.listdir(self.src):
                s = os.path.join(self.src, item)
                d = os.path.join(self.dest, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
