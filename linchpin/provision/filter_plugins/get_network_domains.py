#!/usr/bin/env python

from __future__ import absolute_import
import libvirt
from xml.dom import minidom
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'get_network_domains': filter_utils.get_network_domains
        }
