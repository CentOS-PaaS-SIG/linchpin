import os
import sys
import subprocess
import requests
from linchpin.api.repository_controls.repository_control import RepositoryControl

class HttpRepositoryControl(RepositoryControl):
    def __init__(self, ctx, fetch_type, url, local):
        self.ctx = ctx
        self.fetch_type = fetch_type
        self.local = local

        request_workspace = requests.get(url)
        if request_workspace.status_code != 200:
            self.ctx.log_state("The entered url is invalid")
            sys.exit(1)
        self.url = url
        self.wget_args = ['wget', '-r','-np', '-q', '--reject', "index.html", self.url,
                '-P', self.local]


    def fetch_files(self):
        if self.fetch_type == "workspace":
            subprocess.call(self.wget_args)
        else:
            self.url = os.path.join(self.url, self.fetch_type)
            wget_args = ['wget', '-r', '-q', '--reject', "index.html",
                    self.url, '-P', self.local]
            subprocess.call(self.wget_args)
