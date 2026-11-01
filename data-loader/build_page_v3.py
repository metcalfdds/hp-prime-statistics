#!/usr/bin/env python3
"""build_page_v3.py -- assembles DataLoader_v3.html from page_template_v3.html, dl_core_v1.js and the Rossi example.

v3 (31 Oct 2026, night): the template's v3 (the starter-pack note no longer names a pack version).
v2 (31 Oct 2026): the template's v2 (step 4 says to clear lists left from an earlier load; the Virtual Calculator
result; American spelling). The example is read from examples/rossi.csv (the repository's layout), or ../rossi.csv.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, 'page_template_v3.html'), encoding='utf-8').read()
core = open(os.path.join(HERE, 'dl_core_v1.js'), encoding='utf-8').read()
for c in (os.path.join(HERE, 'examples', 'rossi.csv'), os.path.join(HERE, '..', 'rossi.csv')):
    if os.path.exists(c):
        ex = open(c, encoding='utf-8').read()
        break
assert t.count('/*CORE*/') == 1 and t.count('/*EXAMPLE*/') == 1
t = t.replace('/*CORE*/', core).replace('/*EXAMPLE*/', json.dumps(ex))
open(os.path.join(HERE, 'DataLoader_v3.html'), 'w', encoding='utf-8').write(t)
print('DataLoader_v3.html', len(t), 'bytes')
