#!/usr/bin/env python3
"""summarize_probe_v1.py PROBE_DIR [OUT.tsv] -- caps_probe_v1's per-program results (PROBE_DIR/<Name>.json) as one
table, and the fields worth a look:
  BIG    a value of 1,000,000 or more accepted
  BREAK  a crash or a freeze right after a typed value
  HELP   the field's help line states a range, and a value outside it was accepted
Writes OUT.tsv (default PROBE_DIR/probe_summary.tsv) and prints the flagged fields."""
import glob
import json
import os
import re
import sys

D = os.path.join(sys.argv[1], '')
OUT = sys.argv[2] if len(sys.argv) > 2 else D + 'probe_summary.tsv'
rows, flag = [], []


def help_range(h):
    h = h.replace(',', '')
    m = re.search(r'(-?\d+(?:\.\d+)?)\s*(?:to|-|–)\s*(-?\d+(?:\.\d+)?)', h)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r'(?:at most|up to|no more than|<=|≤)\s*(\d+(?:\.\d+)?)', h)
    if m:
        return None, float(m.group(1))
    return None


for p in sorted(glob.glob(D + '*.json')):
    prog = os.path.basename(p)[:-5]
    for r in json.load(open(p)):
        tries = {float(v): c for v, c in r['tries'].items()}
        acc = sorted(v for v, c in tries.items() if (c.get('A') or c.get('M')) and not c.get('R'))
        brk = sorted(v for v, c in tries.items() if c.get('C') or c.get('F'))
        hr = help_range(r['help'] or '')
        out = []
        if hr:
            lo, hi = hr
            out = [v for v in acc if (hi is not None and v > hi) or (lo is not None and v < lo)]
        line = '\t'.join([prog, r['title'], r['name'], r['label'], r['help'],
                          ' '.join('%g:%s' % (v, ''.join(sorted(c))) for v, c in sorted(tries.items())),
                          '%g' % max(acc) if acc else '-'])
        rows.append(line)
        tags = []
        if any(v >= 1e6 for v in acc):
            tags.append('BIG')
        if brk:
            tags.append('BREAK at %s' % ','.join('%g' % v for v in brk))
        if out:
            tags.append('HELP says %s but took %s' % (hr, ','.join('%g' % v for v in out)))
        if tags:
            flag.append('%-12s %-28s %-8s %-30s | %s | %s' % (prog, r['title'][:28], r['name'], (r['help'] or '')[:30],
                                                            '; '.join(tags), ' '.join('%g:%s' % (v, ''.join(sorted(c)))
                                                                                      for v, c in sorted(tries.items()))))
open(OUT, 'w').write(
    'program\tform\tfield\tlabel\thelp\ttried\tmax accepted\n' + '\n'.join(rows) + '\n')
print('%d fields in %d programs; %d flagged' % (len(rows), len(glob.glob(D + '*.json')), len(flag)))
for f in flag:
    print(f)
