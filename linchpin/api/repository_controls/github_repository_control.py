import os
import requests
from linchpin.api.repository_controls.repository_control import RepositoryControl

class GithubRepositoryControl(RepositoryControl):


    def __init__(self, url, item):
        self.url = url
        self.item = item
    
    def list_files(self):
