#!/usr/bin/env python

from __future__ import absolute_import
import linchpin.FilterUtils.FilterUtils as filter_utils
from xml.etree.ElementTree import fromstring


class FilterModule(object):
    ''' A filter to get libvirt files from xml '''
    def filters(self):
        return {
            'get_libvirt_files': filter_utils.get_libvirt_files
        }
