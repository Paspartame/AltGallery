#!/usr/bin/env python3
"""Validate and apply upstream Swipt rolling-build metadata before merge."""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
URL = 'https://github.com/swipt-automation/swipt/releases/download/nightly/altstore.json'
DOWNLOAD = 'https://github.com/swipt-automation/swipt/releases/download/nightly/Swipt.ipa'

def apply(source, official):
    matches = [a for a in official['apps'] if a.get('bundleIdentifier') == 'io.nekohasekai.swipt']
    if len(matches) != 1:
        raise ValueError('Unexpected official Swipt app identity')
    v = dict(matches[0]['versions'][0])
    if v.get('downloadURL') != DOWNLOAD or not str(v.get('buildVersion', '')).isdigit() or not v.get('version'):
        raise ValueError('Invalid official Swipt version')
    v['buildNumber'] = str(v['buildVersion'])
    app = source['apps'][0]
    if app['bundleIdentifier'] != 'io.nekohasekai.swipt':
        raise ValueError('Local Swipt identity mismatch')
    app['versions'] = [v]
    if 'appPermissions' in matches[0]:
        app['appPermissions'] = matches[0]['appPermissions']
    return source

if __name__ == '__main__':
    with urllib.request.urlopen(urllib.request.Request(URL, headers={'User-Agent':'XHN-IPA'}), timeout=30) as r:
        official = json.load(r)
    path = ROOT / 'apps/Swipt/apps.json'
    result = apply(json.loads(path.read_text()), official)
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('Swipt build:', result['apps'][0]['versions'][0]['buildVersion'])
