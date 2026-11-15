#!/usr/bin/env python3
"""verify_CICatcher_beta2k.py -- checks CICatcher beta 2k (Round 14, 14 Nov 2026): help pages 2 and 6 say "the share
caught" and "the 'all' rate" where beta 2j said "the catch rate" and "the 'all' catch rate".  Runs from the repository
alone (beta 2j from git, the commit before Round 14).  Needs hp-prime-kit (HPKIT) for the harness.

  T1  verify/round14/make_round14.py, run again from beta 2j, makes programs/CICatcher_beta2k.txt byte for byte.
  T2  the new file differs from the old one only in the three replaced literals and in comment lines (the header and
      the history note).
  T3  the six help pages, dumped by the harness from both versions, differ in exactly those three lines.
  T4  no help page of beta 2k says "catch rate".
  T5  every help line of beta 2k fits its width at the calculator's glyph widths (verify/round11/glyph_widths_vc.json).
  S1  the harness smoke test: CICatcher() with Esc as the idle key ends with no error.
"""
import os, sys, io, json, difflib, subprocess, tempfile, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
BASE = '26912a9'; NEW = os.path.join('programs', 'CICatcher_beta2k.txt')
tmp = tempfile.mkdtemp(prefix='cqv_'); OLD = os.path.join(tmp, 'CICatcher_beta2j.txt')
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/CICatcher_beta2j.txt'], check=True, capture_output=True).stdout)
GW = {int(k): v for k, v in json.load(open(os.path.join(HERE, 'round11', 'glyph_widths_vc.json'))).items()}
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:500]) if (detail != '' and not ok) else ''), flush=True)
    if ok: NPASS[0] += 1
    else: FAIL.append(name)


out = os.path.join(tmp, 'built')
subprocess.run([sys.executable, os.path.join(HERE, 'round14', 'make_round14.py'), out], check=True, capture_output=True)
check('T1 the build makes programs/CICatcher_beta2k.txt byte for byte', open(os.path.join(out, 'CICatcher_beta2k.txt'), 'rb').read() == open(NEW, 'rb').read())
a = io.open(OLD, encoding='utf-8').read().split('\n'); b = io.open(NEW, encoding='utf-8').read().split('\n')
changed = [l[2:] for l in difflib.ndiff(a, b) if l[:2] in ('- ', '+ ')]
code = [l for l in changed if not l.lstrip().startswith('//')]
want = ['    "value, so EVERY line grows, red lines turn blue and the catch rate",', '    "rises. 99 % catches more, but its longer lines give a less",',
        '    "CQ_COVER (the \'all\' catch rate)."},', '    "value, so EVERY line grows, red lines turn blue and the share",',
        '    "caught rises. 99 % catches more, but its longer lines give a less",', '    "CQ_COVER (the \'all\' rate)."},']
check('T2 only the three replaced literals and comment lines differ from beta 2j (%d comment lines)' % (len(changed) - len(code)), sorted(code) == sorted(want), code)


def pages(path):
    h = Harness(path, idle_key=4, on_unverified='warn')
    try: h.execute('CICatcher()')
    except Exception: pass
    h.screens[:] = []
    for i in range(60): h.press(30)
    h.call('cqHelp')
    seen, out = set(), []
    for s in h.screens:
        k = '\n'.join(s.lines())
        if s.lines() and k not in seen: seen.add(k); out.append(s)
    return out


po, pn = pages(OLD), pages(NEW)
diff = [(i + 1, x, y) for i, (p, q) in enumerate(zip(po, pn)) for x, y in zip(p.lines(), q.lines()) if x != y]
check('T3 six help pages in both; they differ in three lines, on pages 2 and 6', len(po) == 6 and len(pn) == 6 and len(diff) == 3 and sorted(set(d[0] for d in diff)) == [2, 6], diff)
check('T4 no help page of beta 2k says "catch rate"', not any('catch rate' in l for p in pn for l in p.lines()))
over = []
for p in pn:
    for t in [it for it in p.items if hasattr(it, 'text') and it.text.strip()]:
        w = sum(GW[ord(c)][int(t.font or 1) - 1] if ord(c) in GW else 8 for c in t.text)
        if w > min(318 - t.x, t.width or 999): over.append((w, t.text))
check('T5 every help line within its width at the glyph widths', not over, over)
h = Harness(NEW, idle_key=4, on_unverified='warn')
try: r = h.execute('CICatcher()'); err = None
except Exception as e: r, err = None, '%s: %s' % (type(e).__name__, str(e)[:200])
check('S1 CICatcher() with Esc as the idle key ends with no error', err is None, err)
print('\n%d checks, %d failed' % (NPASS[0] + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
