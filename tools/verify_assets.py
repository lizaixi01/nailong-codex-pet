#!/usr/bin/env python3
"""Verify release hashes and PNG dimensions using only the Python standard library."""
from pathlib import Path
import hashlib
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
for item in manifest['files']:
    data = (ROOT / item['path']).read_bytes()
    if hashlib.sha256(data).hexdigest() != item['sha256']:
        raise SystemExit('Hash mismatch: ' + item['path'])
    if 'width' in item:
        if data[:8] != b'\x89PNG\r\n\x1a\n':
            raise SystemExit('Not a PNG: ' + item['path'])
        width, height = struct.unpack('>II', data[16:24])
        if (width, height) != (item['width'], item['height']):
            raise SystemExit('Wrong dimensions: ' + item['path'])
    print('OK ' + item['path'])
print('All release assets verified.')
