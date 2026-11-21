#!/usr/bin/env python3
"""build_page_v6.py -- assembles DataLoader_v6.html from page_template_v6.html, dl_core_v2.js and the Rossi example.

v6 (21 Nov 2026): the template's v6, after the accessibility check of the two loader pages (tools/pages_a11y_v1.js;
docs/dev/pages-accessibility-2026-11-21.md).  Three things under WCAG 2.1 AA: the orange and the green used for text
are a shade deeper (contrast 5.5 to 1; they were 4.3 and 4.4), the page no longer scrolls sideways in a window 320 px
wide, and the list of warnings is announced as a live region without a role that a list may not carry.  Nothing the
page computes or writes has changed: the core is still v2.
v5 (17 Nov 2026, night): the template's v5, for the Prime Loader's v2a, whose layout is new (which calculator, which
programs, one button).  Step 4's link now ends ?data=1, which opens the Loader ready for a data file with no program
chosen, and its second line names the Loader's step 2, where the button now is.  The same two lines change in the
note that goes into the zip.  Nothing the page computes or writes has changed: the core is still v2.
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
t = open(os.path.join(HERE, 'page_template_v6.html'), encoding='utf-8').read()
core = open(os.path.join(HERE, 'dl_core_v2.js'), encoding='utf-8').read()
ex = open(os.path.join(HERE, 'examples', 'rossi.csv'), encoding='utf-8').read()
assert t.count('/*CORE*/') == 1 and t.count('/*EXAMPLE*/') == 1 and t.count('__PRIMELOADER_URL__') == 2
t = t.replace('/*CORE*/', core).replace('/*EXAMPLE*/', json.dumps(ex)).replace('__PRIMELOADER_URL__', PRIMELOADER_URL)
open(os.path.join(HERE, 'DataLoader_v6.html'), 'w', encoding='utf-8').write(t)
print('DataLoader_v6.html', len(t), 'bytes')
# index.html beside the page sends a browser on to the current version, as prime-loader/index.html does, so the
# address .../data-loader/ never changes and the front page need not be edited when the version does.
SITE = 'https://metcalfdds.github.io/hp-prime-statistics/'
page = 'DataLoader_v6.html'
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(
    '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    '<title>HP Prime Data Loader</title>\n'
    '<meta http-equiv="refresh" content="0; url=' + page + '">\n'
    '<link rel="canonical" href="' + SITE + 'data-loader/' + page + '">\n'
    '<style>body{font:16px/1.5 system-ui,sans-serif;margin:2rem;color:#172033;background:#f6f8fb}'
    '@media (prefers-color-scheme:dark){body{color:#e8edf6;background:#0f1420}a{color:#7d9cff}}</style>\n'
    '</head>\n<body>\n<!-- Written by build_page_v6.py: sends the browser on to the current Data Loader, so the '
    'address .../data-loader/ never changes. -->\n'
    '<p>Opening the HP Prime Data Loader&hellip; If nothing happens, <a href="' + page + '">click here</a>.</p>\n'
    '</body>\n</html>\n')
print('index.html -> ' + page)
