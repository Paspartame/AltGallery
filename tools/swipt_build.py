#!/usr/bin/env python3
"""Supplement AltGen's IPA-derived version with CFBundleVersion for rolling builds."""
import io
import json
import plistlib
import urllib.request
import zipfile
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'apps/Swipt/apps.json'
source = json.loads(path.read_text())
version = source['apps'][0]['versions'][0]
url = version['downloadURL']
if url != 'https://github.com/swipt-automation/swipt/releases/download/nightly/Swipt.ipa':
    raise ValueError('Unexpected Swipt download URL')
with urllib.request.urlopen(url, timeout=90) as response:
    data = response.read(150 * 1024 * 1024 + 1)
if len(data) > 150 * 1024 * 1024:
    raise ValueError('IPA exceeds size limit')
with zipfile.ZipFile(io.BytesIO(data)) as archive:
    names = [n for n in archive.namelist() if n.startswith('Payload/') and n.count('/') == 2 and n.endswith('/Info.plist')]
    if len(names) != 1:
        raise ValueError('Ambiguous app bundle')
    info = plistlib.loads(archive.read(names[0]))
if info['CFBundleIdentifier'] != source['apps'][0]['bundleIdentifier']:
    raise ValueError('IPA identity mismatch')
version['version'] = str(info['CFBundleShortVersionString'])
version['buildVersion'] = version['buildNumber'] = str(info['CFBundleVersion'])
version['size'] = len(data)
path.write_text(json.dumps(source, ensure_ascii=False, indent=2) + '\n')
print('Swipt IPA version/build:', version['version'], version['buildVersion'])
