#!/usr/bin/env python3
"""
Simple script that generates hosts files usable with dsh/pssh
for runnign administrative actions on all hosts in a particular
labs project. Salt is just way too unreliable to be useful
for this purpose.

Hits the openstack-browser API.

You can execute commands via pssh like:

    pssh -t0 -p4 -h <hostgroup> '<command>'

This sets parallelism to 4, tweak as necessary.
"""
import json
import sys
from urllib.request import urlopen

OSB = 'https://tools.wmflabs.org/openstack-browser'

project_spec = sys.argv[1]

if project_spec == 'all-instances':
    projects_url = '{}/api/projects.txt'.format(OSB)
    projects = urlopen(projects_url).read().decode('utf-8').split('\n')
else:
    projects = [project_spec]

instances = []
for project_name in projects:
    api_url = '{}/api/dsh/project/{}'.format(OSB, project_name)
    hosts = urlopen(api_url).read().decode('utf-8').split('\n')
    instances.extend(hosts)

with open(project_spec, 'w') as f:
    f.write("\n".join(instances))
