#!/usr/bin/env python


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def combine_hosts_names(hosts, names):
    result = []
    min_hosts_names = min(len(hosts), len(names))
    for i in range(min_hosts_names):
        result.append(merge_two_dicts(hosts[i], names[i]))
    if len(hosts) > min_hosts_names:
        for i in range(min_hosts_names, len(hosts)):
            result.append(hosts[i])
    if len(names) > min_hosts_names:
        for i in range(min_hosts_names, len(names)):
            result.append(names[i])
    return result


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'combine_hosts_names': combine_hosts_names
        }
