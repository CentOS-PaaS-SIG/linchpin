#!/usr/bin/env python


def get_pod_status(pod_list, res_def_out):
    # this filter runs only when the kind is "Pod"
    pod_status = pod_list.get("resources", [])
    container_names = [x["name"]
                       for x in res_def_out["result"]["spec"]["containers"]]
    pod_stats = {}
    # filters out all the pods data w.r.to containers
    # provisioned in pods
    for x in pod_status:
        if x["metadata"]["name"] in container_names:
            pod_data = x
            pod_data["status"] = x["status"]["phase"]
            pod_stats[x["metadata"]["name"]] = pod_data
    # checks for the status of the container and returns Failure value
    # when any container is not in Running state
    for name in container_names:
        if pod_stats[name]["status"] != "Running":
            return "Failure"
    return pod_stats


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'get_pod_status': get_pod_status
        }
