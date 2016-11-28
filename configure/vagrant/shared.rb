$ip = 2

def vm(config, name, base_box="centos/7")
    config.vm.define name do |nodeconfig|
        nodeconfig.vm.box = base_box
        nodeconfig.vm.hostname = name + ".box"
        nodeconfig.vm.network "private_network", ip: "192.168.8.#{$ip}", netmask: "255.255.255.0"
        $ip += 1
    end
end
