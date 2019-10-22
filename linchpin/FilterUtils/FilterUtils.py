from __future__ import absolute_import
from __future__ import print_function
import json
from six.moves import range


def add_res_data(hosts, res_grp, role):
    new_hosts = []
    for host in hosts:
        host['resource_group'] = res_grp
        host['role'] = role
        new_hosts.append(host)
    return new_hosts


def ip_filter(forward_mode):
    if forward_mode == 'nat':
        return 'private'
    if forward_mode == 'bridge':
        return 'public'


def fetch_attr(output_dict, attr, default):
    return output_dict.get(attr, default)


def get_pod_status(pod_list, res_def_out):
    # this filter runs only when the kind is "Pod"
    pod_status = pod_list.get("resources", [])
    pod_stats = {}
    # filters out all the pods data w.r.to containers
    # provisioned in pods
    for x in pod_status:
        if x["metadata"]["name"] == res_def_out["result"]["metadata"]["name"]:
            pod_data = x
            pod_data["status"] = x["status"]["phase"]
            pod_stats[x["metadata"]["name"]] = pod_data
    # checks for the status of the pod and returns Failure value
    # when any pod is not in Running state
    for name in pod_stats.keys():
        if pod_stats[name]["status"] != "Running":
            return "Failure"
    return pod_stats


def omit_filter(output, omit):
    if output == "":
        return omit
    return output


def provide_default(fetched, default):
    if fetched == "":
        return default
    else:
        return fetched


def unicode_filter(output):
    output = json.dumps(output)
    return output


def format_rules(rules, rule_type):
    rules_output = []
    for rule in rules:
        if rule["rule_type"] == rule_type:
            rule_output = {}
            rule_output['from_port'] = rule['from_port']
            rule_output['to_port'] = rule['to_port']
            rule_output['cidr_ip'] = rule['cidr_ip']
            rule_output['proto'] = rule['proto']
            rules_output.append(rule_output)
    return rules_output


def fetch_list_by_attr(output, attr):
    new_output = []
    for ele in output:
        if attr in ele:
            new_output.append(ele[attr])
    return new_output


def get_host_from_uri(uri):
    """
    examples: qemu+ssh://root@hail.cloud.example.com/system
              test:///default
              qemu+ssh://192.168.122.6/system
    """
    uri = uri.split("//")[-1].split("/")[0].split("@")[-1]
    if uri == '':
        return 'localhost'
    return uri


def get_provider_resources(topo_output, res_type):
    provider_resources = []
    for host in topo_output:
        if host['resource_group'] == res_type:
            provider_resources.append(host)
    return provider_resources


def format_networks(networks):
    # "net-name=atomic-e2e-jenkins-test,net-name=atomic-e2e-jenkins-test2"
    nics = []
    if networks is not None and isinstance(networks, list):
        nics = ["net-name={0}".format(net) for net in networks]
        nics = ",".join(nics)

    return nics


def render_os_server_insts(res_def, res_def_names):

    output = []
    for sname in res_def_names:
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
    return output


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


def filter_list_by_attr(output, attr):
    new_output = []
    for ele in output:
        if attr in ele:
            new_output.append(ele)
    return new_output


def get_libvirt_files(output):
    from xml.etree.ElementTree import fromstring
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


def translate_ruletype(ruletype):
    if ruletype == "inbound":
        return "ingress"
    if ruletype == "outbound":
        return "egress"
    else:
        return "invalid ruletype "


def filter_list_by_attr_val(output, attr, val):
    new_output = []
    for ele in output:
        if attr in ele:
            if ele[attr] == val:
                new_output.append(ele)
    return new_output


def get_network_domains(network, uri):
    import libvirt
    from xml.dom import minidom
    network_hosts = []
    conn = libvirt.open(uri)
    if conn is None:
        return network_hosts

    hosts = conn.listDomainsID()

    for host in hosts:
        dom = conn.lookupByID(host)
        raw_xml = dom.XMLDesc(0)
        xml = minidom.parseString(raw_xml)
        interfaces = xml.getElementsByTagName('interface')
        usesNetwork = False
        for interface in interfaces:
            usesNetwork = usesNetwork or iterate_interfaces(interface, network)
        if usesNetwork:
            network_hosts.append(dom.name())

    return network_hosts


def iterate_interfaces(interface, network):
    """
    Returns true if the interface uses the given network
    Otherwise returns false
    """
    if interface.getAttribute('type') != 'network':
        return False
    interfaceNodes = interface.childNodes
    for node in interfaceNodes:
        if node.nodeName != 'source':
            continue
        if 'network' not in list(node.attributes.keys()):
            return False
        if node.attributes['network'].nodeValue == network:
            return True
        return False


def map_results(results, attr, subattr):
    output = []
    for task_result in results:
        output.append(task_result[attr][subattr])
    return output


def prepare_ssh_args(ssh_args, users, sshkey):
    # "{{ ssh_args }} --ssh-inject \
    # {{ item.0}}:string:'{{ pubkey_local.stdout }}'"
    for user in users:
        ssh_args += "--ssh-inject " + user + ":string:'" + sshkey + "' "
    return ssh_args


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


def fetch_beaker_job_ids(topo_out):
    output = []
    for entry in topo_out:
        entry_dict = {}
        entry_dict["ids"] = []
        if "id" in list(entry):
            entry_dict["ids"].append("J:" + entry["id"])
            output.append(entry_dict)
    return output


def get_os_server_names(topo_output):
    names = []
    for item in topo_output:
        if item["role"] == "os_server":
            openstack_res = item.get("openstack", [])
            for os_item in openstack_res:
                names.append(os_item["name"])
    return names


def write_to_file(data, path, filename):
    filename = filename.replace(' ', '_').lower()

    fd = open(path + filename + ".output", "w")
    fd.write(json.dumps(data))
    fd.close()
    return data
