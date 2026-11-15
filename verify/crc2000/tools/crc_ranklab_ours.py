# -*- coding: utf-8 -*-
"""crc_ranklab_ours.py -- RankLab beta 1i's own exact null distribution of the Mann-Whitney U (rk_MWNull, whole-number counts
in PPL) on every cell read from the U table of Zwillinger & Kokoska (2000), beside the printed value and beside the count
made in crc_check_v4.py.  Through the PC harness.
  HPKIT=... python3 tools/crc_ranklab_ours.py REPO work/part4.json"""
import sys, json, os
repo = sys.argv[1]; sys.path.insert(0, os.path.join(repo, 'tools'))
from ppl_run_v3e import Harness
g = json.load(open(sys.argv[2]))['grid']
h = Harness(os.path.join(repo, 'programs', 'RankLab_beta1i.txt'), idle_key=4, home_minus=True, cas='fail')
cache = {}; n_all = n_same = n_print = 0; worst = 0.0; bad = []
for n, m, u, printed, true in g:
    if (m, n) not in cache:
        h.execute('rk_MWNull(%d,%d)' % (m, n)); cache[(m, n)] = ([float(x) for x in h.globals_['rkNull']], float(h.globals_['rkNDen']))
    c, den = cache[(m, n)]
    if u >= len(c): continue
    ours = sum(c[:u + 1]) / den; n_all += 1; worst = max(worst, abs(ours - true))
    if abs(ours - true) < 1e-12: n_same += 1
    if abs(ours - float(printed)) <= 0.0005 + 1e-9: n_print += 1
    else: bad.append([n, m, u, printed, round(ours, 5)])
print('cells %d; RankLab equals the exact count in %d (largest difference %.1e); RankLab rounds to the printed value in %d' % (n_all, n_same, worst, n_print))
print('not the printed value:', bad[:14])
