#!/usr/bin/env python

from linchpin.api import LinchpinAPI


class LinchpinCli(LinchpinAPI):

    def __init__(self, ctx):
        LinchpinAPI.__init__(self, ctx)



