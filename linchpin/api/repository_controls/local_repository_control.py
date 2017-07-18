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

        if not os.path.exists(dest):
            ctx.log_state(dest + " does not exist.")
            sys.exit(1)
        self.dest = dest

        if os.path.samefile(self.src, self.dest):
            ctx.log_state("Provide two different locations")
            sys.exit(1)
            
        if not os.path.exists(self.src):
            ctx.log_state('{0} is not a valid path'.format(src))
            sys.exit(1)
        if not os.path.exists(self.dest):
            ctx.log_state('{0} is not a valid path'.format(dest))
            sys.exit(1)
            

    def fetch_files(self):
        if self.fetch_type == "workspace":
            for item in os.listdir(self.src):
                if self.ctx.cfgs['fetch_types'].get(item.lower(),
                        None) != 'True':
                    continue
                try:
                    s = os.path.join(self.src, item)
                    d = os.path.join(self.dest, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)
                except OSError as e:
                    if e.errno == 17:
                        self.ctx.log_state('The {0} directory already exists'
                                            .format(item))
        else:
            if self.ctx.cfgs['fetch_types'].get(self.fetch_type, None) != 'True':
                ctx.log_state(self.fetch_type + " not defined")
            self.fetch_section(self.fetch_type)
            

    def fetch_section(self, section):
        section_src = os.path.join(self.src, section)
        section_dest = os.path.join(self.dest, section)
        
        if not os.path.exists(section_dest):
            os.makedirs(section_dest)
            
        try:
            for item in os.listdir(section_src):
                s = os.path.join(section_src, item)
                d = os.path.join(section_dest, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
        except OSError as e:
            self.ctx.log_state(e)
            sys.exit(1)


