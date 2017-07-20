#!/usr/bin/env python3
"""
Simple script that generates hosts files usable with dsh/pssh
for runnign administrative actions on a bunch of toollabs hosts
at the same time. Salt is just way too unreliable to be useful
for this purpose.

Hits the openstack-browser API and then classifies instances into different
groups based on their names. Update classifier here when things change, to
keep this useful.

You can execute commands via pssh like:

    pssh -t0 -p4 -h <hostgroup> '<command>'

This sets parallelism to 4, tweak as necessary.
"""
import json
from urllib.request import urlopen


# Maps prefixes to hostgroup names
classifier = {
    '': 'all'
    'bastion-': 'bastion',
    'checker-': 'checker',
    'cron-': 'cron',
    'docker-': 'docker',
    'elastic-': 'elastic',
    'exec-': 'exec-all',
    'flannel-': 'flannel',
    'k8s-': 'k8s',
    'mail': 'mail',
    'master': 'master',
    'proxy-': 'proxy',
    'redis-': 'redis',
    'services-': 'services',
    'static-': 'static',
    'webgrid-': 'webgrid-all',
    'webgrid-generic': 'webgrid-generic',
    'webgrid-lighttpd-': 'webgrid-lighttpd-all',
    'webgrid-lighttpd-14': 'webgrid-lighttpd-trusty',
    'worker-': 'worker',
}

OSB = 'https://tools.wmflabs.org/openstack-browser'

# Initialize hostgroups with empty list
hostgroups = {name: [] for name in classifier.values()}

api_url = '{}/api/dsh/project/tools'.format(OSB)
hosts = urlopen(api_url).read().decode('utf-8').split('\n')

for instance in hosts:
    for prefix in classifier:
        if instance.startswith('tools-{}'.format(prefix)):
            hostgroups[classifier[prefix]].append(instance)

for groupname, hosts in hostgroups.items():
    with open(groupname, 'w') as f:
        f.write("\n".join(hosts))
