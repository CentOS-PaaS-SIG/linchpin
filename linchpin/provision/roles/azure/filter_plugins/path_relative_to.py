#!/usr/bin/env python

import os


def path_relative_to(path, base_path):
    """
    If `path` is not an OS filesystem absolute or relative path then assume
    it is relative to `base_path`.
    """
    if path.startswith(('/', './', '../', '~/')):
        return path
    return os.path.join(base_path, path)


class FilterModule(object):
    def filters(self):
        return {'path_relative_to': path_relative_to}
