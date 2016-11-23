#!/usr/bin/env python
from ansible import errors


def compare_host_counts(topo, inv):
    t_host_count = 0
    i_host_count = 0

    for k, v in inv['hosts'].iteritems():
        i_host_count += v.get('count', 1)

    t_host_count = len(topo['hosts'])

    return t_host_count >= i_host_count


def make_host_vars(host, host_vars):
    hv = {}

    rep = {"__IP__": host}

    for k, v in host_vars.iteritems():
        for i, j in rep.iteritems():
            v = v.replace(i, j)
        hv.update({k: v})

    return hv


def get_groups(topo, inv):
    # get the number left of hosts from the outputs
    t_count = len(topo['hosts'])
    t_prev_count = t_count
    inv_groups = {}
    hv = inv.get('vars')

    for k, v in inv['hosts'].iteritems():
        num_needed = v.get('count', 1)
        if t_count > 0:
            t_count -= num_needed

            for c in range(t_count, t_prev_count):

                for hg in v.get('host_groups'):
                    host = topo['hosts'][c]
                    host_vars = make_host_vars(host, hv)
                    if hg in inv_groups.keys():
                        inv_groups[hg][host] = host_vars
                    else:
                        inv_groups[hg] = {host: host_vars}
            t_prev_count = t_count

    return inv_groups


def get_group_children(inv):

    hg = inv.get('host_groups')
    inventory = ''

    for k, v in hg.iteritems():
        g_kids = v.get('children')
        if g_kids is not None:
            inventory += '[{}:children]\n'.format(k)
            for i in g_kids:
                inventory += '{}\n'.format(i)

    return inventory


def get_group_vars(inv):

    hg = inv.get('host_groups')
    inventory = ''

    for k, v in hg.iteritems():
        g_vars = v.get('vars')
        if g_vars is not None:
            inventory += '[{}:vars]\n'.format(k)
            for i, j in g_vars.iteritems():
                inventory += '{}={}'.format(i, j)
                if not isinstance(j, basestring) or not j.endswith('\n'):
                    inventory += '\n'
    return inventory


def duffy_inventory(topo, inv):

    print(topo['duffy_res'])
    if len(topo['duffy_res']):
        d_topo = topo['duffy_res'][0]
    else:
        return ''
    inventory = ''
    # verify counts. If there aren't enough nodes allocated, abort!
    if compare_host_counts(d_topo, inv):
        groups = get_groups(d_topo, inv)
        g_vars = get_group_vars(inv)
        g_kids = get_group_children(inv)
    for k, v in groups.iteritems():
        inventory += '[{}]\n'.format(k)
        for i, j in v.iteritems():
            hv = ''
            for k, l in j.iteritems():
                hv += ' {}={}'.format(k, l)

            inventory += '{}{}\n'.format(i, hv)
        inventory += '\n'
    if g_vars is not None:
        inventory += '{}\n'.format(g_vars)
    if g_kids is not None:
        inventory += '{}\n'.format(g_kids)
    inventory += '\n'
    return inventory


class FilterModule(object):
    ''' A filter to fix interface's name format '''
    def filters(self):
        return {
            'duffy_inventory': duffy_inventory
        }
