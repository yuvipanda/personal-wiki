#!/usr/bin/python3
"""
Simple script that generates hosts files usable with dsh/pssh
for runnign administrative actions on a bunch of toollabs hosts
at the same time. Salt is just way too unreliable to be useful
for this purpose.

Hits the wikitech API and then classifies instances into different
groups based on their names. Update classifier here when things
change, to keep this useful.
"""
import json
from urllib.request import urlopen


# Maps prefixes to hostgroup names
classifier = {
    'webgrid-': 'webgrid-all',
    'webgrid-lighttpd-': 'webgrid-lighttpd-all',
    'webgrid-generic': 'webgrid-generic',
    'exec-': 'exec-all',
    'webproxy-': 'webproxy',
    'checker-': 'checker',
    'redis-': 'redis',
    'services-': 'services',
    'bastion-': 'bastion',
    'submit': 'submit',
    'master': 'master',
    'shadow': 'shadow',
    'mail': 'mail',
    'static-': 'static'
}

# Initialize hostgroups with empty list
hostgroups = {name: [] for name in classifier.values()}

api_url = 'https://wikitech.wikimedia.org/w/api.php' \
          '?action=query&list=novainstances&niregion=eqiad&format=json' \
          '&niproject=tools'

data = json.loads(urlopen(api_url).read().decode('utf-8'))

for instance in data['query']['novainstances']:
    name = instance['name']
    for prefix in classifier:
        if name.startswith('tools-' + prefix):
            hostgroups[classifier[prefix]].append(name + ".eqiad.wmflabs")

for groupname, hosts in hostgroups.items():
    with open(groupname, 'w') as f:
        f.write("\n".join(hosts))