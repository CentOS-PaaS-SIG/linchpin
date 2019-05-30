#!/bin/bash
set -x

for server in `openstack server list --name ci-lp-cp* -c ID --format value`; do
    start=$(openstack server show -c OS-SRV-USG:launched_at --format value $server)
    uptime=$(($(date +%s)-$(date --date "$start" +%s)))
    # delete instance if it is more than 6hrs old
    if [ $uptime -gt 21600 ]; then
        # openstack server delete $server
        openstack server delete $server
    fi
done
