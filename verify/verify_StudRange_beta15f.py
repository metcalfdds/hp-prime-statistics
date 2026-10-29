#!/usr/bin/env python3
"""verify_StudRange_beta15e.py -- the PPL engine's plot cache, beta 15d against beta 15e.

Independent review, 22 October 2026.  Two sections:
  A. sr_SRCDF with the outer grid at 32 and at 64 nodes, at the true 95th percentile of
     SciPy's studentized_range, k = 3 and 6, df 8 to 101: where 32 nodes lose the density of s.
  B. sr_Cache itself on the PPL path (the harness blanks #PYTHON, so the fallback builds the
     cache, as on a calculator whose MicroPython did not answer): beta 15d and beta 15e, each
     65-point CDF cache against SciPy on the cache's own q grid, with the harness time.
Needs: tools/ppl_run_v3e.py beside programs/ (run from the repository's verify/ folder or set
the paths below), hp-prime-kit (HPKIT or the Community_Library zip), SciPy.  Beta 15d is not
in programs/ any more; it is read from git (commit 98b8e39) when the OLD path is missing.
"""
import os, sys, io, contextlib, time, subprocess, tempfile
HERE = '/home/claude/metcalfdds/hp-prime-statistics/verify'
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'tools'))
NEW = '/home/claude/new6/StudRange_beta15f.txt'
OLD = os.path.join(ROOT, 'programs', 'StudRange_beta15d.txt')
if not os.path.exists(OLD):
    OLD = os.path.join(tempfile.gettempdir(), 'StudRange_beta15d_from_git.txt')
    if not os.path.exists(OLD):
        src = subprocess.check_output(['git', '-C', ROOT, 'show', '98b8e39:programs/StudRange_beta15d.txt'])
        open(OLD, 'wb').write(src)
from ppl_run_v3e import Harness
from scipy import stats
import numpy as np

def load(f):
    with contextlib.redirect_stdout(io.StringIO()):
        return Harness(f, strict=False, on_unverified='warn')

def ev(h, e):
    h.reset_records()
    with contextlib.redirect_stdout(io.StringIO()):
        return h.execute(e)

fails = 0
print('A. sr_SRCDF at SciPy\'s q(0.95; k, df), outer grid 32 vs 64 nodes (beta 15e source; the')
print('   routine is unchanged, only sr_Cache\'s choice of grid changed)')
h = load(NEW)
for k, nz in [(3, 24), (6, 48)]:
    ev(h, 'sr_BuildZ(%d)' % nz)
    for v in [8, 12, 20, 30, 40, 50, 60, 70, 80, 90, 100, 101]:
        q = stats.studentized_range.ppf(0.95, k, v)
        g32 = ev(h, 'sr_SRCDF(%.6f,%d,%d,32)' % (q, k, v))
        g64 = ev(h, 'sr_SRCDF(%.6f,%d,%d,64)' % (q, k, v))
        flag = ''
        if abs(g64 - 0.95) > 5e-5:
            flag = '  <-- 64 nodes off'; fails += 1
        print('   k=%d df=%3d  ns=32: %.5f   ns=64: %.5f   (true 0.95000)%s' % (k, v, g32, g64, flag))

print('B. sr_Cache on the PPL path: the 65-point CDF cache against SciPy on its own q grid')
print('   %-3s %-5s %-4s %-9s %-8s %-6s' % ('k', 'df', 'ver', 'max err', 'at q', 'sec'))
hs = {'15d': load(OLD), '15e': load(NEW)}
for k, df in [(6, 20), (6, 50), (6, 70), (6, 90), (6, 100), (6, 240), (3, 60), (10, 80), (4, 5)]:
    for ver in ('15d', '15e'):
        hh = hs[ver]; hh.reset_records(); t0 = time.time()
        with contextlib.redirect_stdout(io.StringIO()):
            hh.call('sr_Cache', float(k), float(df), 3.0)
        dt = time.time() - t0
        cdf = np.array(hh.globals_['EP_SRCDF'], dtype=float)
        qmax = float(hh.globals_['srQmax']); q = np.arange(65) * qmax / 64
        want = stats.studentized_range.cdf(q, k, df)
        err = np.abs(cdf - want); i = int(err.argmax())
        flag = ''
        if ver == '15e' and err[i] > 2e-4:
            flag = '  <-- beta 15e off'; fails += 1
        print('   %-3d %-5d %-4s %.5f   q=%.3f  %5.1f%s' % (k, df, ver, err[i], q[i], dt, flag))
print('failures: %d' % fails)
