#!/usr/bin/env python


def render_os_server_insts(res_def, os_resource_name):

    output = []
    if "count" in res_def:
        server_names = [os_resource_name + str(i)
                        for i in range(1, res_def["count"] + 1)]
        for sname in server_names:
            server_dict = {}
            server_dict['name'] = sname
            if 'additional_volumes' in res_def:
                server_dict['volumes'] = []
                for vol in res_def.get("additional_volumes", []):
                    a_vol = {}
                    a_vol.update(vol)
                    a_vol["name"] = vol["name"] + "-" + server_dict["name"]
                    a_vol["server_name"] = server_dict["name"]
                    server_dict["volumes"].append(a_vol)
            output.append(server_dict)
    else:
        return res_def
    return output


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'render_os_server_insts': render_os_server_insts
        }
