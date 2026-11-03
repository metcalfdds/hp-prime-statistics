#!/usr/bin/env python3
"""verify_RankLab_beta1c.py -- checks RankLab beta 1c (2 Nov 2026, night): commas in big numbers (round 5).

Roger, 2 Nov 2026: "always put comma delimiters in big numbers".  RankLab beta 1c was made from beta 1b by
tools/commas_v1.py with tools/commas_config_r5.py: a routine of its own, rk_Cm, puts a comma every three digits
into each run of four or more digits it draws ("12,345.678"); decimals, exponents, the program's own wording (a year in
a citation) and anything the CAS reads are left alone.  This script runs tools/comma_check_v1.py:
  G  static: rk_Cm is the fleet's routine word for word; with every call of it taken out, the code is beta 1b's
     routine for routine, except rk_Welcome; nothing the CAS or EXPR reads goes through it; no "!="; ASCII as before;
     the header names beta 1c.
  R  30 seeds of the monkey on both versions: every screen, box and summary the same once the commas are out.
  C  every text handed to the CAS or EXPR is the old version's, call for call (the commas are for the screen only).
  M  every number of four or more digits drawn is grouped.   Y  no year (or other number the program writes as text)
     is given a comma.   D  no new firm overlap, straddle, overrun or cut number.
Run from verify/ as it is (the older version from ../programs, an _superseded_* folder or git history; the harness and
the checks from ../tools; hp-prime-kit from $HPKIT).   python3 verify_RankLab_beta1c.py [RankLab_beta1b.txt]
"""
import glob
import os
import re
import subprocess
import sys
import tempfile
import warnings

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
for cand in reversed([c for c in (os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'), HERE) if c]):
    if os.path.exists(os.path.join(cand, 'comma_check_v1.py')):
        sys.path.insert(0, cand)
import comma_check_v1 as CC  # noqa: E402
from ppl_run_v3e import Harness  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()

NAME, OLDNAME = 'RankLab_beta1c.txt', 'RankLab_beta1b.txt'
PROG = os.path.join(HERE, NAME) if os.path.exists(os.path.join(HERE, NAME)) else os.path.join(HERE, '..', 'programs', NAME)
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:600]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


def older(name):
    """the previous version: given, beside this script, in ../programs, in an _superseded_* folder, or from git"""
    if len(sys.argv) > 1:
        return sys.argv[1]
    for pth in [os.path.join(HERE, name), os.path.join(HERE, '..', 'programs', name)] + \
            sorted(glob.glob(os.path.join(HERE, '..', '_superseded_*', name)), reverse=True):
        if os.path.exists(pth):
            return pth
    root, rel_ = os.path.join(HERE, '..'), 'programs/' + name
    try:
        c = subprocess.run(['git', '-C', root, 'rev-list', '-n', '1', 'HEAD', '--', rel_],
                           capture_output=True, text=True, timeout=60).stdout.strip()
        for ref in ((c + ':' + rel_, c + '^:' + rel_) if c else ()):
            out = subprocess.run(['git', '-C', root, 'show', ref], capture_output=True, timeout=60)
            if out.returncode == 0:
                pth = os.path.join(tempfile.mkdtemp(), name)
                open(pth, 'wb').write(out.stdout)
                return pth
    except Exception:
        pass
    return None

NORM = None


OLD = older(OLDNAME)
print('=== RankLab beta 1c against beta 1b ({})'.format(os.path.relpath(OLD, HERE) if OLD else 'NOT FOUND'))
if not OLD:
    check('the older version found', False)
    sys.exit(1)
OSRC = open(OLD, encoding='utf-8').read()
WANT = ['rk_Welcome']          # routines that differ beyond the wrapping (the configuration's edits, the version's text)
ADDED = ['rk_Cm']
CASN = []
print('=== G. static')
for nm, ok, det in CC.static(OSRC, SRC, 'rk_Cm', WANT, ADDED, 'beta 1c', CASN):
    check(nm, ok, det)
print('=== R, M, Y, D. the monkey, 30 seeds on both versions')
RES = CC.runs(OLD, PROG, 'RankLab()', 30, 30, 'beta 1b|beta 1c', NORM)
EXEMPT_M = {}
EXEMPT_R = {}     # seeds whose path differs, each with its reason
EXEMPT_Y = {}     # numbers from 1,500 to 2,099 that are quantities, not years, each with its reason
for nm, ok, det in CC.report(RES, EXEMPT_M, EXEMPT_Y, EXEMPT_R):
    if ok is None:
        print('INFO ' + nm)
    else:
        check(nm, ok, det)

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
