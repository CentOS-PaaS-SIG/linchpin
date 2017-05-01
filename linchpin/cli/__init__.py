#!/usr/bin/env python

from linchpin.api import LinchpinAPI


class LinchpinCli(LinchpinAPI):

    def __init__(self, ctx):
        """
        Set some variables, pass to parent class
        """

        LinchpinAPI.__init__(self, ctx)



