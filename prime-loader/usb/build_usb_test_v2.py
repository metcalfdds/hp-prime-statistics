#!/usr/bin/env python3
"""build_usb_test_v2.py -- assembles PrimeUSBTest_v2.html: the page template, prime_usb_v2.js (what travels on the
cable) and usb_ladder_v2.js (the test), in one file that opens from a folder or from the web.

    python3 build_usb_test_v2.py [OUT.html]

v2 (17 Nov 2026, night).  The first page ran on the author's G2 and G1 that evening (logs/) and stood still at its last
step.  This one has an end to every wait, asks what the first run left open (where the old framing stops; whether a
compressed program is kept once the calculator is told the page speaks version 03; whether the newer framing carries
a long program), and writes down every report the calculator sends.  README.md in this folder says what is known and
from whom.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = 'v2'
BUILT = '17 November 2026'
SITE = 'https://metcalfdds.github.io/hp-prime-statistics/'
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'PrimeUSBTest_' + VERSION + '.html')

t = open(os.path.join(HERE, 'usb_test_template_v2.html'), encoding='utf-8').read()
parts = {
    '/*PRIMEUSB*/': open(os.path.join(HERE, 'prime_usb_v2.js'), encoding='utf-8').read(),
    '/*LADDER*/': open(os.path.join(HERE, 'usb_ladder_v2.js'), encoding='utf-8').read(),
    '__VERSION__': VERSION,
    '__BUILT__': BUILT,
    '__LOADER_URL__': SITE + 'prime-loader/',
}
for k, v in parts.items():
    assert t.count(k) == 1, (k, t.count(k))
    assert '</script' not in v.lower(), k
    t = t.replace(k, v)
open(OUT, 'w', encoding='utf-8').write(t)
print('%s: %s bytes' % (os.path.basename(OUT), format(len(t.encode('utf-8')), ',')))
