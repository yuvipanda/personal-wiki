#!/usr/bin/env python3
"""
Simple script that generates hosts files usable with dsh/pssh
for runnign administrative actions on all hosts in a particular
labs project. Salt is just way too unreliable to be useful
for this purpose.

Hits the wikitech API.

You can execute commands via pssh like:

    pssh -t0 -p4 -h <hostgroup> '<command>'

This sets parallelism to 4, tweak as necessary.
"""
import json
import sys
from urllib.request import urlopen


project_spec = sys.argv[1]

if project_spec == 'all-instances':
    projects_url = 'https://wikitech.wikimedia.org/w/api.php?action=query&list=novaprojects&format=json'
    projects = json.loads(urlopen(projects_url).read().decode('utf-8'))['query']['novaprojects']
else:
    projects = [project_spec]

instances = []
for project_name in projects:
    api_url = 'https://wikitech.wikimedia.org/w/api.php' \
              '?action=query&list=novainstances&niregion=eqiad&format=json' \
              '&niproject=%s' % project_name

    data = json.loads(urlopen(api_url).read().decode('utf-8'))
    for instance in data['query']['novainstances']:
        instances.append(instance['name'] + ".eqiad.wmflabs")

with open(project_spec, 'w') as f:
    f.write("\n".join(instances))
