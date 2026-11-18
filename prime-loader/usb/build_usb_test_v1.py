#!/usr/bin/env python3
"""build_usb_test_v1.py -- assembles PrimeUSBTest_v1.html: the page template, prime_usb_v1.js (what travels on the
cable) and usb_ladder_v1.js (the test), in one file that opens from a folder or from the web.

    python3 build_usb_test_v1.py [OUT.html]

v1 (17 Nov 2026).  Roger: "we do need to make some sort of very simple loader ... to get the programs on a physical
calcuator", and "do we need the Kit?"  The page is the first run of the cable code on a real HP Prime: it sends test
programs four ways at five sizes, reads each back, and writes a log.  Nothing in it has run on a calculator; README.md
in this folder says what is known and from whom.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
VERSION = 'v1'
BUILT = '17 November 2026'
SITE = 'https://metcalfdds.github.io/hp-prime-statistics/'
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'PrimeUSBTest_' + VERSION + '.html')

t = open(os.path.join(HERE, 'usb_test_template_v1.html'), encoding='utf-8').read()
parts = {
    '/*PRIMEUSB*/': open(os.path.join(HERE, 'prime_usb_v1.js'), encoding='utf-8').read(),
    '/*LADDER*/': open(os.path.join(HERE, 'usb_ladder_v1.js'), encoding='utf-8').read(),
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
