# -*- coding: utf-8 -*-
"""probe_fm_params.py -- for the three families whose Formula page waited in probe_fm_families.py (Student's t, Fisher F,
Burr XII), which parameters keep the CAS quick: whole, half and two-decimal values side by side (23 Nov 2026, round 19).
Giac 1.9.0 (icas), 60 s a question, two at a time; the CAS text is the program's own, as in probe_fm_families.py.

Run from the repository's root:   python3 verify/round19/probe_fm_params.py programs/StatDist_v2.7o.txt
"""
import os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe_fm_families as P  # noqa: E402

SETS = [(7, [17, 0, 0]), (7, [17.5, 0, 0]), (7, [2.37, 0, 0]), (7, [30.1, 0, 0]),
        (9, [7, 18, 0]), (9, [7.5, 17.5, 0]), (9, [7, 17.83, 0]), (9, [7.37, 18, 0]), (9, [3, 12, 0]),
        (10, [2, 3, 1, ]), (10, [2, 3, 1.83]), (10, [2.5, 3.5, 1]), (10, [2.5, 3.5, 1.5]), (10, [2.37, 3, 1]),
        (10, [2, 3.37, 1]), (10, [3, 2, 1])]

if __name__ == '__main__':
    P.PROG = sys.argv[1] if len(sys.argv) > 1 else P.PROG
    jobs, lab = [], {}
    for fid, par in SETS:
        for what, e in P.texts(fid, par):
            jobs.append((len(jobs), what, e)); lab[len(jobs) - 1] = (fid, par)
    with ThreadPoolExecutor(2) as ex:
        for j, what, secs, out in ex.map(P.ask, jobs):
            fid, par = lab[j]
            print('%-10s %-18s %-7s %6.1f s  %s' % (P.FAM[fid][0], par, what, secs, out[-45:]), flush=True)
