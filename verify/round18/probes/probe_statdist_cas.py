# -*- coding: utf-8 -*-
"""probe_statdist_cas.py -- how long Giac takes for StatDist's Formula page (CAS) of Student's t, by df (23 Nov 2026).

The monkey (round 18, seed 18000984) chose t with df = 206.3 and the Formula page, and the harness stopped the CAS call
for E[X^2] at its limit of 60 s.  This asks Giac (icas, Giac 1.9.0 here) the same integral, written as StatDist v2.7o
writes it (st_RTxt(st_Rat(df)), read from the program through the harness), for seven df, two at a time, with 600 s each.
It says nothing about the calculator's own CAS, which has not been tried.  About twenty minutes.

Run from the repository's root:   python3 verify/round18/probes/probe_statdist_cas.py
"""
import sys, os, time, subprocess, tempfile, json
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'tools'); os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
from ppl_run_v3e import Harness
h = Harness('programs/StatDist_v2.7o.txt', idle_key=4, home_minus=True)
T = 'string(simplify(int(stqx^K*(Gamma((D+1)/2)/(sqrt(D*pi)*Gamma(D/2))*(1+stqx^2/D)^(-(D+1)/2)),stqx,-inf,inf)))'
DFS = [5, 24, 206, 2.5, 9.5, 17.83, 206.3]
jobs = []
for v in DFS:
    d = str(h.execute('st_RTxt(st_Rat(%r))' % v)).strip('"')
    jobs.append((v, 2, T.replace('K', '2').replace('D', d)))
jobs.append((206.3, 1, T.replace('K', '1').replace('D', str(h.execute('st_RTxt(st_Rat(206.3))')).strip('"'))))
def run(j):
    v, k, e = j
    with tempfile.NamedTemporaryFile('w', suffix='.giac', delete=False) as f:
        f.write(e + ';\n')
    t = time.time()
    try:
        out = subprocess.run(['icas', f.name], capture_output=True, timeout=600).stdout.decode()[-80:].strip().replace('\n', ' ')
    except subprocess.TimeoutExpired:
        out = 'NOT DONE in 600 s'
    return dict(df=v, k=k, secs=round(time.time() - t, 1), out=out, expr=e[:160])
with ThreadPoolExecutor(2) as ex:
    for r in ex.map(run, jobs):
        print(json.dumps(r), flush=True)
