#!/usr/bin/env python
# import linchpin.FilterUtils.FilterUtils as filter_utils


def write_to_file(data, path, filename):
    filename = filename.replace(' ', '_').lower()

    fd = open(path + filename + ".output", "w")
    fd.write(json.dumps(data))
    fd.close()
    return data


class FilterModule(object):
    ''' A filter to write variables to file '''
    def filters(self):
        return {
            'write_to_file': write_to_file
        }
