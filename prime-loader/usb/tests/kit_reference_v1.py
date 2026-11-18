#!/usr/bin/env python3
"""kit_reference_v1.py -- what hp-prime-kit's own code makes of every program in programs/, for test_usb_core_v1.js
to compare prime_usb_v1.js with, byte for byte.  Roger Metcalf & Claude, 17 Nov 2026.

    python3 kit_reference_v1.py OUTDIR [--kit PATH]

hp-prime-kit (MIT, JordiRigau/hp-prime-kit) is the one description of the cable that was measured from Windows on
firmware 2.4.15515, and its hpkit/usb.py is that description as code: program_message() builds the message that
installed a program on a G2, and to_reports() cuts it into reports.  For each program this writes the kit's message
(NAME.msg) and one line of reference.json: the name, the characters of its source, the uncompressed part's SHA-256
and length, the message's length, and the number and SHA-256 of the reports.  The kit's SELFTEST example goes in too:
its uncompressed part is the one a G2 itself sent (docs/topics/usb.md, usb.program-message).
"""
import glob, hashlib, io, json, os, re, sys, zlib

argv = sys.argv[1:]
KIT = os.environ.get('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
if '--kit' in argv:
    i = argv.index('--kit'); KIT = argv[i + 1]; del argv[i:i + 2]
OUT = argv[0]
sys.path.insert(0, KIT)
from hpkit import usb, program

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRAMS = os.path.join(HERE, '..', '..', '..', 'programs')
os.makedirs(OUT, exist_ok=True)
rows = []

def one(name, path):
    with io.open(path, encoding='utf-8') as f:
        source = program.normalize_source(f.read())
    msg = usb.program_message(name, source)
    inner = zlib.decompress(msg[10:])
    reports = usb.to_reports(msg)
    open(os.path.join(OUT, name + '.msg'), 'wb').write(msg)
    rows.append({'name': name, 'file': os.path.basename(path), 'chars': len(source),
                 'inner_len': len(inner), 'inner_sha': hashlib.sha256(inner).hexdigest(),
                 'inner_head': inner[:4].hex(), 'msg_len': len(msg), 'reports': len(reports),
                 'reports_sha': hashlib.sha256(b''.join(reports)).hexdigest()})

for p in sorted(glob.glob(os.path.join(PROGRAMS, '*.txt'))):
    m = re.match(r'^(.+?)_(beta|v)[^_]*\.txt$', os.path.basename(p))
    if not m:
        sys.exit('STOP: no name in ' + p)
    one(m.group(1), p)
one('SELFTEST', os.path.join(KIT, 'examples', 'selftest', 'SELFTEST.txt'))
json.dump(rows, open(os.path.join(OUT, 'reference.json'), 'w'), indent=1)
print('%d programs; reports %d to %d' % (len(rows) - 1, min(r['reports'] for r in rows[:-1]), max(r['reports'] for r in rows[:-1])))
