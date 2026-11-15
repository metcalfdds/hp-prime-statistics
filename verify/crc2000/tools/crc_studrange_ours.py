# -*- coding: utf-8 -*-
"""crc_studrange_ours.py -- StudRange beta 15m's own arithmetic (sr_SRCrit, the PPL routine after Dunlap, Powell and Konnerth,
64 nodes, as the program calls it) on every cell of the three studentized-range tables of Zwillinger & Kokoska (2000), beside
SciPy and beside the printed value.  Run through the PC harness, which counts in 16 digits where the Prime keeps 12.
  HPKIT=... python3 tools/crc_studrange_ours.py REPO work/part3.json work/part3_ours.json"""
import sys, json, os
repo = sys.argv[1]; sys.path.insert(0, os.path.join(repo, 'tools'))
from ppl_run_v3e import Harness
g = json.load(open(sys.argv[2]))['grid']
h = Harness(os.path.join(repo, 'programs', 'StudRange_beta15m.txt'), idle_key=4, home_minus=True, cas='fail')
out = json.load(open(sys.argv[3])) if os.path.exists(sys.argv[3]) else []; zcur = 0      # resumes where it stopped
for i, (a, k, lab, printed, sp) in enumerate(g):
    if i < len(out): continue
    df = 100000 if lab in ('∞',) else int(lab)
    nz = 48 if k > 5 else 32          # as the program does before each critical value (its lines 1630 and 1697)
    try:
        if nz != zcur: h.execute('sr_BuildZ(%d)' % nz); zcur = nz
        ours = float(h.execute('sr_SRCrit(%r,%d,%d,64)' % (a, k, df)))
    except Exception as e: ours = None
    out.append([a, k, lab, printed, sp, ours])
    if i % 40 == 0: json.dump(out, open(sys.argv[3], 'w'))
json.dump(out, open(sys.argv[3], 'w'))
ok = [o for o in out if o[5] is not None]
import collections
print('cells', len(out), 'computed', len(ok))
for a in (0.01, 0.05, 0.1):
    c = [o for o in ok if o[0] == a]
    d = sorted(abs(o[5] - o[4]) for o in c); r = sorted(abs(o[5] - o[4]) / o[4] for o in c)
    agree_book = sum(1 for o in c if abs(o[5] - float(o[3])) <= 0.005 + 1e-9)
    agree_sp = sum(1 for o in c if round(o[5], 2) == round(o[4], 2) or abs(o[5] - o[4]) < 0.005)
    worst = max(c, key=lambda o: abs(o[5] - o[4]) / o[4])
    print('alpha %g: %d cells; ours against SciPy: largest difference %.4f, largest relative %.5f (k=%d df=%s: ours %.4f SciPy %.4f); ours rounds to the printed value in %d cells' % (a, len(c), d[-1], r[-1], worst[1], worst[2], worst[5], worst[4], agree_book))
