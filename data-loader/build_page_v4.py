#!/usr/bin/env python3
"""build_page_v4.py -- assembles DataLoader_v4.html from page_template_v4.html, dl_core_v2.js and the Rossi example.

v4 (17 Nov 2026, the review "they must be bullet proof and as simple as possible"): the template's v4 and the core's
v2.  The page opens with an empty box (v3 opened with the example in it, and a paste went into the middle of it);
step 2 lists everything the page did to the paste that the student did not ask for, and lets the student say whether
the first row is names and what separates the columns; a workbook opened as a file is refused with the way round it;
step 4 sends the student to the Prime Loader, which checks the file and puts DataLoad on the calculator.  The build
also writes index.html, which sends a browser on to the page, so the address .../data-loader/ stays the same.
v3 (31 Oct 2026, night): the template's v3 (the starter-pack note no longer names a pack version).
v2 (31 Oct 2026): the template's v2.  The example is read from examples/rossi.csv.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
PRIMELOADER_URL = 'https://metcalfdds.github.io/hp-prime-statistics/prime-loader/'   # its index.html sends the browser on
t = open(os.path.join(HERE, 'page_template_v4.html'), encoding='utf-8').read()
core = open(os.path.join(HERE, 'dl_core_v2.js'), encoding='utf-8').read()
ex = open(os.path.join(HERE, 'examples', 'rossi.csv'), encoding='utf-8').read()
assert t.count('/*CORE*/') == 1 and t.count('/*EXAMPLE*/') == 1 and t.count('__PRIMELOADER_URL__') == 2
t = t.replace('/*CORE*/', core).replace('/*EXAMPLE*/', json.dumps(ex)).replace('__PRIMELOADER_URL__', PRIMELOADER_URL)
open(os.path.join(HERE, 'DataLoader_v4.html'), 'w', encoding='utf-8').write(t)
print('DataLoader_v4.html', len(t), 'bytes')
# index.html beside the page sends a browser on to the current version, as prime-loader/index.html does, so the
# address .../data-loader/ never changes and the front page need not be edited when the version does.
SITE = 'https://metcalfdds.github.io/hp-prime-statistics/'
page = 'DataLoader_v4.html'
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<title>HP Prime Data Loader</title>\n'
    '<meta http-equiv="refresh" content="0; url=' + page + '">\n'
    '<link rel="canonical" href="' + SITE + 'data-loader/' + page + '">\n'
    '<style>body{font:16px/1.5 system-ui,sans-serif;margin:2rem;color:#172033;background:#f6f8fb}'
    '@media (prefers-color-scheme:dark){body{color:#e8edf6;background:#0f1420}a{color:#7d9cff}}</style>\n'
    '</head>\n<body>\n<!-- Written by build_page_v4.py: sends the browser on to the current Data Loader, so the '
    'address .../data-loader/ never changes. -->\n'
    '<p>Opening the HP Prime Data Loader&hellip; If nothing happens, <a href="' + page + '">click here</a>.</p>\n'
    '</body>\n</html>\n')
print('index.html -> ' + page)
