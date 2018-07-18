#!/usr/bin/env python


def transform_os_server_output(res_def_out):
    res_def_out = res_def_out.get("results", [])
    res_def = {}
    res_def["ids"] = []
    res_def["openstack"] = []
    res_def["servers"] = []
    for ele in res_def_out:
        res_def["ids"].append(ele.get("id"))
        res_def["openstack"].append(ele.get("openstack", {}))
        res_def["servers"].append(ele.get("server", {}))
    return res_def


class FilterModule(object):
    ''' A filter fix distiller '''
    def filters(self):
        return {
            'transform_os_server_output': transform_os_server_output
        }
