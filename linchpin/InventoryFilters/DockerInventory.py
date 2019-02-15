try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from .InventoryFilter import InventoryFilter


class DockerInventory(InventoryFilter):
    DEFAULT_HOSTNAMES = ['Config.Hostname']

    def get_host_data(self, res, config):
        host_data = {}
        if res['resource_type'] != 'docker_container_res':
            return host_data
        var_data = config.get('docker', {})
        if var_data is None:
            var_data = {}
        host = self.get_hostname(res, var_data,
                                 self.DEFAULT_HOSTNAMES)
        hostname_var = host[0]
        hostname = host[1]
        host_data[hostname] = {}
        if '__IP__' not in var_data.keys():
            var_data['__IP__'] = hostname_var
        self.set_config_values(host_data[hostname], res, var_data)
        return host_data

    def get_inventory(self, res, layout, config):
        output = StringIO()
        self.config.write(output)

        return output.getvalue()
