# -*- coding: utf-8 -*-
"""probe_fm_families.py -- how long Giac takes for every CAS question StatDist's Formula page asks of a continuous family,
with parameters typed to two decimals (23 Nov 2026, round 19).

Round 18's monkey found the page waiting on E[X^2] for Student's t with df = 206.3 (verify/round18/probes/).  This asks
the same questions for every continuous family: E[X], E[X^2] and, for the Exponential, Weibull and Pareto, the CDF.  The
CAS text is the program's own (st_FmPars, st_FmDens, st_FmInt, st_FmAsm, read through the harness from the version named
on the command line); Giac 1.9.0 (icas) answers, with 60 s for each question, as the harness allows.  Two at a time.

Run from the repository's root:   python3 verify/round19/probe_fm_families.py programs/StatDist_v2.7o.txt
"""
import json, os, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'tools'); os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
from ppl_run_v3e import Harness  # noqa: E402

PROG = sys.argv[1] if len(sys.argv) > 1 else 'programs/StatDist_v2.7o.txt'
# id: (name, parameters with two decimals) -- shapes 2.37, scales 1.83, locations 0.37, dfs 17.83
FAM = {1: ('Normal', [0.37, 1.83, 0]), 2: ('Uniform', [0.37, 2.37, 0]), 3: ('Exponential', [1.83, 0, 0]),
       4: ('Weibull', [2.37, 1.83, 0]), 5: ('LogNormal', [0.37, 1.83, 0]), 6: ('Laplace', [0.37, 1.83, 0]),
       7: ('Student t', [17.83, 0, 0]), 8: ('chi-square', [17.83, 0, 0]), 9: ('Fisher F', [7.37, 17.83, 0]),
       10: ('Burr XII', [2.37, 3.37, 1.83]), 11: ('Gumbel', [0.37, 1.83, 0]), 12: ('Pareto', [1.83, 3.37, 0]),
       13: ('Rayleigh', [1.83, 0, 0]), 14: ('Logistic', [0.37, 1.83, 0]), 18: ('Triangular', [0.37, 1.83, 2.37]),
       19: ('Cauchy', [0.37, 1.83, 0]), 20: ('Frechet', [3.37, 1.83, 0.37]), 21: ('Gompertz', [0.37, 1.83, 0]),
       22: ('Maxwell-Boltzmann', [1.83, 0, 0]), 23: ('Erlang', [3, 1.83, 0]), 24: ('Gamma', [2.37, 1.83, 0]),
       25: ('Beta', [2.37, 3.37, 0])}


def texts(fid, par):
    h = Harness(PROG, idle_key=4, home_minus=True)
    h.globals_.update({'stId': fid, 'stPar': list(par)})
    fp = h.execute('st_FmPars()')
    h.globals_['stFmPT'] = fp
    fd = h.execute('st_FmDens(%d, stFmPT, "stqx")' % fid)
    h.globals_['prFD'] = fd
    sf = str(h.execute('st_FmAsm()')).strip('"')
    q = []
    for k in (1, 2):
        q.append(('E[X^%d]' % k, 'string(simplify(' + str(h.execute('st_FmInt(prFD, %d, "stqx")' % k)).strip('"') + ')' + sf + ')'))
    return q


def ask(job):
    fid, what, expr = job
    with tempfile.NamedTemporaryFile('w', suffix='.giac', delete=False) as f:
        f.write(expr + ';\n')
    t = time.time()
    try:
        out = subprocess.run(['icas', f.name], capture_output=True, timeout=60).stdout.decode()[-70:].strip().replace('\n', ' ')
    except subprocess.TimeoutExpired:
        out = 'NOT DONE IN 60 s'
    return fid, what, round(time.time() - t, 1), out


if __name__ == '__main__':
    jobs = []
    for fid, (name, par) in FAM.items():
        try:
            for what, e in texts(fid, par):
                jobs.append((fid, what, e))
        except Exception as ex:
            print('%2d %-18s the harness could not build the text: %s' % (fid, name, str(ex)[:80]), flush=True)
    with ThreadPoolExecutor(2) as ex:
        for fid, what, secs, out in ex.map(ask, jobs):
            print('%2d %-18s %-7s %6.1f s  %s' % (fid, FAM[fid][0], what, secs, out[-50:]), flush=True)
