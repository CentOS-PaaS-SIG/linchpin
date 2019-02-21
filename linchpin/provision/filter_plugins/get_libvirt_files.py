#!/usr/bin/env python
from xml.etree.ElementTree import fromstring


def get_libvirt_files(output):
    files = []
    results = output['results']
    for result in results:
        if len(result['stdout']) > 0:
            stdout = result['stdout']
            myxml = fromstring(stdout)
            devices = myxml.findall('devices')
            for device in devices:
                disks = device.findall('disk')
                for disk in disks:
                    if disk.attrib["type"] == 'file':
                        if len(disk.findall('source')) > 0:
                            source = disk.findall('source')[0]
                            files.append(source.attrib['file'])
    return files


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'get_libvirt_files': get_libvirt_files
        }
