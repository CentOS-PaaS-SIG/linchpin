import os
import sys
import requests
from linchpin.api.repository_controls.repository_control import RepositoryControl

class GithubRepositoryControl(RepositoryControl):

#TODO: HANDLE ERROR CHECKING -- USE linchpin/linchpin/exception
# to create RepositoryControlError(LinchpinError)

    def __init__(self, fetch_type, url, local):
        #Need to parse this: https://github.com/agharibi/SampleLinchpinDirectory
        #API follows this standard: GET /repos/:owner/:repo/contents/:path

        self.local = local.rstrip('/')
        self.fetch_type = fetch_type
        self.fetch_types = {
        'workspace': '',
        'layout': 'layouts',
        'topology': 'topologies',
        'hooks': 'hooks',
        'credentials': 'credentials',
        'PinFile': 'PinFile',
        'resource': 'resources',
        'inventory': 'inventories'
        }

        base_url = "https://api.github.com/repos"
        username = repo = path = ""
        split_url = url.split('/')

        if len(split_url) < 3:
            print "invalid URL"
            sys.exit(1)

        if split_url[0] == 'https:':
            try:
                username = split_url[3]
                repo = split_url[4]
                if len(split_url) > 5:
                    path = '/'.join(split_url[5:])
            except IndexError:
                print "invalid URL"
                sys.exit(1)
        else:
            try:
                username = split_url[1]
                repo = split_url[2]
                if len(split_url) > 3:
                    path = '/'.join(split_url[3:])
            except IndexError:
                print "invalid URL"
                sys.exit(1)

        
        if path == "":
            self.url = '{0}/{1}/{2}/contents/{3}'.format(
                base_url, username, repo, self.fetch_types[fetch_type])
        else:
            path = path.rstrip('/')
            self.url = '{0}/{1}/{2}/contents/{3}/{4}'.format(
                base_url, username, repo, path, self.fetch_types[fetch_type])


            
    def list_files(self):
        fetch_type = self.fetch_type
        if fetch_type == 'workspace' or fetch_type == 'PinFile':
            print "Cannot list " + fetch_type
            sys.exit(1)
        r = requests.get(self.url)
        if r.status_code != 200:
            print "Request failed"
            sys.exit(1)

        print "Fetching {0} list".format(fetch_type)
        for item in r.json():
            print item["name"]


    def fetch_files(self):
        r = requests.get(self.url)
        if  self.fetch_type == 'PinFile':
            print "Dealing with this later"#TODO: DEAl with this
            sys.exit(1)
        if r.status_code != 200:
            print "Request failed"
            sys.exit(1)
        if self.fetch_type == "workspace":
            print "Fetching workspace..."
            for key in self.fetch_types:
                if not os.path.isdir('./{0}'.format(fetch_types[key]))
                    os.makedirs(self.fetch_types[key])
                self.fetch_section(r, key)
            print "done"
        else:
            self.fetch_section(r, self.fetch_type)

    def fetch_section(self, request, section):
        print 'Fetching {0}...'.format(section)
        section_path= '{0}/{1}'.format(self.local.rstrip('/'),self.fetch_types[section])

        if not os.path.isdir(self.local):
            print '{0} is an invalid filepath. Please specify a valid workspace.'.format(self.local)
            sys.exit(1)
        for item in request.json():
            if item["type"] == "file":
                fd = requests.get(item["download_url"],stream=True)
                with open('{0}/{1}'.format(section_path, item["name"]),'wb') as f:
                    for chunk in fd.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
        print "done!"
