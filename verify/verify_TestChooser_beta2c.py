#!/usr/bin/env python3
"""verify_TestChooser_beta2c.py -- checks TestChooser beta 2c (31 Oct 2026): the two t-test pages point to TTestLab,
and four on-screen lines that beta 2b's symbol sweep missed (mu1 - mu2 twice, mu0, pi0) use the symbols.  Nothing
else changes, and this script checks that too, against beta 2b (verify_TestChooser_beta2a.py's 252 checks ran on
the logic, which beta 2b and 2c do not touch).

  1. the details pages of tests 1, 3, 21 and 22, as drawn: the new lines, at their places and colours;
  2. every details line of all 24 tests fits (at most 42 characters, x + 6.2 px a character <= 312);
  3. only tcDetail's strings and the header changed: the routines that differ, the code lines that differ;
     tcNotP (the hatching) is the same;
  4. no spelled-out mu1, mu2, mu0 or pi0 left on screen (the R call wilcox.test(x, mu) is kept);
     no glyph that beta 2b did not already show;
  5. TTestLab really does what the pages say (pooled and separate t; pairs in D1 and D2);
  6. layout: text_overlap_v1 over the 24 details pages, beta 2b and beta 2c: no new firm finding.

Needs ppl_run_v3e.py and text_overlap_v1.py (./tools, ../tools, this folder or $TC_TOOLS), hp-prime-kit ($HPKIT),
TestChooser_beta2b.txt and TestChooser_beta2c.txt, and TTestLab_beta1a.txt (this folder or ../programs).
Run:  python3 verify_TestChooser_beta2c.py     (exit code 0 = all passed)
"""
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/home/claude/kit/hp-prime-kit-HEAD')
_c = [c for c in (os.environ.get('TC_TOOLS', ''), os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'),
                  HERE, '/home/claude/pv25g/gate/tools') if c]
for cand in reversed(_c):
    if any(os.path.exists(os.path.join(cand, f)) for f in ('ppl_run_v3e.py', 'text_overlap_v1.py')):
        sys.path.insert(0, cand)
from ppl_run_v3e import Harness  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402


def find(name):
    for d in (HERE, os.path.join(HERE, '..', 'programs')):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    if name == 'TestChooser_beta2b.txt':
        # in the repository beta 2b has left programs/: take it from git history into a temporary folder
        import subprocess
        repo = os.path.abspath(os.path.join(HERE, '..'))
        rel = 'programs/TestChooser_beta2b.txt'
        last = subprocess.run(['git', '-C', repo, 'rev-list', '-n', '1', 'HEAD', '--', rel],
                              capture_output=True, text=True).stdout.strip()
        for rev in ([last + '^', last] if last else []) + ['HEAD']:
            src = subprocess.run(['git', '-C', repo, 'show', rev + ':' + rel], capture_output=True, text=True)
            if src.returncode == 0 and src.stdout:
                p = os.path.join(tempfile.mkdtemp(), name)
                open(p, 'w', encoding='utf-8').write(src.stdout)
                return p
    sys.exit('not found: ' + name)


NEW, OLD, TTL = find('TestChooser_beta2c.txt'), find('TestChooser_beta2b.txt'), find('TTestLab_beta1a.txt')
SN, SO = open(NEW, encoding='utf-8').read(), open(OLD, encoding='utf-8').read()
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:400]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


OV.install()


def details(path, i):
    h = Harness(path, strict=False, cas='fail', stall_limit=30000, idle_key=4)
    h.call('tcInit')
    h.reset_records()
    h.call('tcDetails', float(i), 1.0, 1.0)
    return h.pages[0]


Y = {1: 55, 2: 81, 3: 119, 4: 145, 5: 171}
WANT = {(1, 3): 'Fleet: TTestLab.  Inference: T-Test μ₁-μ₂.', (1, 4): 'Also T-Int: μ₁ - μ₂ for the difference.',
        (3, 3): 'Fleet: TTestLab, pairs in D1 and D2.', (3, 4): 'Or Inference > T-Test: 1 μ, diffs, μ₀ = 0.',
        (21, 1): 'One group\'s mean against a given μ₀.', (22, 1): 'One proportion vs π₀; counts vs expected.'}
got = {}
fits = []
for i in range(1, 25):
    pg = details(NEW, i)
    for t in pg.texts:
        if round(t.x) == 14:
            ok = len(t.text) <= 42 and t.x + 6.2 * len(t.text) <= 312
            if not ok:
                fits.append((i, t.text))
            for ln, y in Y.items():
                if round(t.y) == y:
                    got[(i, ln)] = (t.text, t.hex)
    details(OLD, i)                                     # beta 2b's pages, for the layout comparison
print('=== 1. the new lines, as drawn')
for k, v in WANT.items():
    g = got.get(k, (None, None))
    check('details page of test %d, line %d (y %d) reads %r' % (k[0], k[1], Y[k[1]], v), g[0] == v, g)
check('the "On the Prime" lines are blue and the "Afterwards" lines magenta, as before: %s, %s'
      % (got[(1, 3)][1], got[(1, 4)][1]), got[(1, 3)][1] == got[(5, 3)][1] and got[(1, 4)][1] == got[(5, 4)][1])
print('=== 2. every details line fits')
check('all 24 details pages: every line at most 42 characters and inside x 312', not fits, fits)
print('=== 3. nothing else changed')


def routines(src):
    out, name, buf = {}, None, []
    for ln in src.split('\n'):
        code = ln.split('//')[0].rstrip() if not ln.strip().startswith('//') else ''
        m = re.match(r'^(?:EXPORT\s+)?(\w+)\s*\(', code)
        if m and not code.endswith(';'):
            if name:
                out[name] = '\n'.join(buf)
            name, buf = m.group(1), []
        if name and code:
            buf.append(code)
    if name:
        out[name] = '\n'.join(buf)
    return out


rn, ro = routines(SN), routines(SO)
diff_r = sorted(k for k in set(rn) | set(ro) if rn.get(k) != ro.get(k))
check('the routines that differ from beta 2b: %s (want tcDetail only); %d routines' % (diff_r, len(rn)),
      diff_r == ['tcDetail'] and set(rn) == set(ro))
cn = [ln.split('//')[0] for ln in SN.split('\n') if not ln.strip().startswith('//')]
co = [ln.split('//')[0] for ln in SO.split('\n') if not ln.strip().startswith('//')]
import difflib  # noqa: E402
ch = [d for d in difflib.unified_diff(co, cn, lineterm='', n=0) if d[:1] in '+-' and d[:3] not in ('+++', '---')]
check('code lines changed: %d removed, %d added, all of them detail strings'
      % (len([d for d in ch if d[0] == '-']), len([d for d in ch if d[0] == '+'])),
      len(ch) == 12 and all(re.fullmatch(r'[+-]\s+".*",?', d) for d in ch), ch)
hn = Harness(NEW, strict=False, cas='fail')
hn.call('tcInit')
ho = Harness(OLD, strict=False, cas='fail')
ho.call('tcInit')
check('tcNotP (the hatched cells) is the same as beta 2b\'s', hn.globals_['tcNotP'] == ho.globals_['tcNotP'])
rule = [1 if any(x.startswith('Not on the Prime') for x in hn.call('tcDetail', float(i))) else 0 for i in range(1, 25)]
check('tcNotP still equals the tests whose details say "Not on the Prime"', rule == [int(v) for v in hn.globals_['tcNotP']])
check('the banner reads "beta 2c" and the header has the beta 2c paragraph and status line',
      '// TESTCHOOSER - beta 2c\n' in SN and '// beta 2c (31 Oct 2026)' in SN and '(ppl_run_v3e, 31 Oct 2026)' in SN)
print('=== 4. symbols')


def screen_strings(src):
    out = []
    for ln in src.split('\n'):
        if ln.strip().startswith('//'):
            continue
        out += re.findall(r'"([^"]*)"', ln.split('//')[0])
    return out


spelled = [s for s in screen_strings(SN) if re.search(r'\b(mu1|mu2|mu0|pi0)\b', s)]
check('no spelled-out mu1, mu2, mu0 or pi0 on screen (%s); the R call wilcox.test(x, mu) is kept' % spelled,
      not spelled and any('wilcox.test(x, mu)' in s for s in screen_strings(SN)))
gn = set(c for s in screen_strings(SN) for c in s if ord(c) > 126)
go = set(c for s in screen_strings(SO) for c in s if ord(c) > 126)
VERIFIED = set('χ²√≥≤≠±×→∞αβμσφθρλ') | {chr(8320), chr(8321), chr(8322)}    # Lessons Learned s5
check('no glyph that is neither on beta 2b\'s screens nor on the verified list (new to TestChooser: %s, both '
      'device-verified subscripts)' % ''.join(sorted(gn - go)), gn <= go | VERIFIED, sorted(gn - go - VERIFIED))
print('=== 5. TTestLab does what the pages say')
st = open(TTL, encoding='utf-8').read()
check('TTestLab beta 1a has the pooled and separate t, and reads pairs from D1 and D2',
      'Pooled-variances t test' in st and 'Separate-variances t test' in st and
      '"Pairs in D1 (x₁) and D2 (x₂)"' in st and 'EXPORT TTESTLAB()' in st)
print('=== 6. layout')
rep = OV.report()


def firm(f):
    s = set()
    for c in f['collisions']:
        if c['severity'] == 'overlap' and c['firm']:
            s.add(('overlap', c['a'], c['b']))
    for x in f['straddles']:
        if x['firm']:
            s.add(('straddle', x['text'], x['edge']))
    for x in f['overruns']:
        if x['firm']:
            s.add(('overrun', x['text']))
    return s


tn = [t for t in rep if 'beta2c' in t]
to = [t for t in rep if 'beta2b' in t]
fn = firm(rep[tn[0]]) if tn else None
fo = firm(rep[to[0]]) if to else None
check('text_overlap_v1 over the 24 details pages: beta 2c adds no firm overlap, straddle or overrun (beta 2b %s, '
      'beta 2c %s)' % (len(fo) if fo is not None else '?', len(fn) if fn is not None else '?'),
      fn is not None and fo is not None and not (fn - fo), sorted(fn - fo) if fn is not None else '')
print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for x in FAIL:
    print('  FAILED: ' + x)
sys.exit(1 if FAIL else 0)
