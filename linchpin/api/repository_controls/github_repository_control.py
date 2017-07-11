import os
import sys
import requests
from linchpin.api.repository_controls.repository_control import RepositoryControl

class GithubRepositoryControl(RepositoryControl):

#TODO: HANDLE ERROR CHECKING -- USE linchpin/linchpin/exception
# to create RepositoryControlError(LinchpinError)

    def __init__(self, ctx, fetch_type, url, local):
        #Need to parse this: https://github.com/agharibi/SampleLinchpinDirectory
        #API follows this standard: GET /repos/:owner/:repo/contents/:path

        self.ctx = ctx
        self.local = local.rstrip('/')
        self.fetch_type = fetch_type
        self.fetch_types = ctx.cfgs["fetch_types"]
        del self.fetch_types['pkg']
        #self.fetch_types = {
        #'layout': 'layouts',
        #'topology': 'topologies',
        #'hooks': 'hooks',
        #'credentials': 'credentials',
        #'PinFile': '',
        #'resources': 'resources',
        #'inventory': 'inventories'
        #}

        base_url = "https://api.github.com/repos"
        username = repo = path = ""
        split_url = url.split('/')

        if len(split_url) < 3:
            self.ctx.log_state("invalid URL")
            sys.exit(1)

        if split_url[0] == 'https:':
            try:
                username = split_url[3]
                repo = split_url[4]
                if len(split_url) > 5:
                    path = '/'.join(split_url[5:])
            except IndexError:
                self.ctx.log_state("invalid URL")
                sys.exit(1)
        else:
            try:
                username = split_url[1]
                repo = split_url[2]
                if len(split_url) > 3:
                    path = '/'.join(split_url[3:])
            except IndexError:
                self.ctx.log_state("invalid URL")
                sys.exit(1)

        
        if path == "":
            self.root_url = '{0}/{1}/{2}/contents'.format(
                base_url, username, repo)
        else:
            path = path.rstrip('/')
            self.root_url = '{0}/{1}/{2}/contents/{3}'.format(
                base_url, username, repo, path)


            
    def list_files(self):
        fetch_type = self.fetch_type
        if fetch_type == 'workspace' or fetch_type == 'PinFile':
            self.ctx.log_state("Cannot list " + fetch_type)
            sys.exit(1)
        r = requests.get(self.build_section_url(self.fetch_type))
        if r.status_code != 200:
            self.ctx.log_state("Request failed")
            sys.exit(1)

        self.ctx.log_state("Fetching {0} list".format(fetch_type))
        for item in r.json():
            self.ctx.log_state(item["name"])


    def fetch_files(self):
        if self.fetch_type == "workspace":
            self.fetch_workspace()
        else:
            self.fetch_section(self.fetch_type)


    def fetch_workspace(self):
        print("Fetching workspace...")

        for key in self.fetch_types:
            if key == "workspace":
                continue
            if not os.path.isdir('{0}/{1}'.format(self.local, self.fetch_types[key])):
                os.makedirs('{0}/{1}'.format(self.local, self.fetch_types[key]))
            self.fetch_section(key)

        print("Workspace successfully fetched!")
        

    def fetch_section(self, section):
        print('Fetching {0}...'.format(section))

        section_path = '{0}/{1}'.format(self.local.rstrip('/'),self.fetch_types[section])
        fetch_url = self.build_section_url(section)
        request = requests.get(fetch_url)

        if request.status_code != 200:
            self.ctx.log_state("Request failed")
            return
        if not os.path.isdir(self.local):
            self.ctx.log_state("{0} is an invalid filepath. Please specify a valid workspace."
                    .format(self.local))
            sys.exit(1)
        for item in request.json():
            if item["name"] == ".empty":
                self.ctx.log_state("This directory is empty. There is nothing to fetch.")
                break
            if item["type"] == "file":
                fd = requests.get(item["download_url"],stream=True)
                with open('{0}/{1}'.format(section_path, item["name"]),'wb') as f:
                    for chunk in fd.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
        print("done!")
    
    def build_section_url(self, section):
        return '{0}/{1}'.format(self.root_url, self.fetch_types[section])
