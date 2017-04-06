import os
import click
from linchpin.api import LinchpinAPI
from linchpin.api.invoke_playbooks import invoke_linchpin
from utils import parse_yaml


class LinchpinCli(LinchpinAPI):

    def __init__(self, context):
        LinchpinAPI.__init__(self, context)

    def test(self):
        print("test function inside linchpincli")
