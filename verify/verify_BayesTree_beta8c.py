#!/usr/bin/env python3
"""verify_BayesTree_beta8c.py -- checks BayesTree beta 8c (17 Oct 2026): the fixes from the second
emulator round (BRIEF_R2FIX_v1, section 4 "BayesTree", items 1-8).  Built from
verify_BayesTree_beta8b.py: every check is kept and now runs on beta 8c in harness v3d, which raises
"Invalid input" for INSTRING("", ...) and prints small fixed decimals in the Prime's scientific form
(h.sci_strings).  Changed or new checks are marked "8c"; the new ones are part R.

Part R (8c):
  R1 the stale-spot case, both ways: a real later tap at the spot of a MOUSE-read closing tap now
     counts (the emulator's "2x2 closed at the ROC key, then ROC once: nothing" -- beta 8b shows it,
     beta 8c opens ROC); a click injected as ALREADY QUEUED (harness mouse_tail=True, the clock not
     moved) is still skipped, and so it is when the student's own taps take time.
  R2 the PPV, ROC and Fagan views close on a footer tap that arrives ONLY as {3, x, y} (round 2),
     nothing else opens; beta 8b in the same model stays open; the type-0 "outside = back" still works.
  R3 the two-test breadcrumb from measured widths (a width model of 6.5 px per character at font 1,
     the brief's assumption; and a stress model with an 11-px arrow): no piece overlaps the one
     before, everything ends left of x 102; beta 8b's fixed layout overlaps.
  R4 the Exact page with two tests: the four counts on two lines, every line inside the screen,
     the page within its footer (the emulator's case: prior 0.041, 0.835 / 0.95 twice).
  R5 Diagnostics says "EpiStats 2x2", not ConTable2; R6 the soft key reads "Forens" (<= 6 chars).
  R7 INSTRING never sees "": bt_Rep on a pattern at the end, at the start, the whole string, an empty
     pattern and an empty text; bt_Strip(""); every CAS page end to end with cas='fail' (one test,
     two tests, forensic) gives the "decimal" badge and no error -- and beta 8b stops on the same run.
  R8 the scientific STRING results (h.sci_strings) of every harness run of beta 8c: none.
  G (8c) beta 8c against beta 8b: only the routines named in the CHANGES differ, bt_WaitAny is
     byte-identical, and the only new line outside them is the threshold btQueuedMs.

(The beta 8b description follows.)

Part S (8b): the soft keys fire on a type-3 strip tap, on every page; beta 8a under v3d does nothing
  (the emulator's FAIL); no tap runs twice (a type-0 press on the strip does nothing, a screen tap's
  click is ignored); a page closed by a tap on its footer leaves no stale click for the tree.
Part L (8b): every pair on the tree adds up -- root = D+ + D-, D+ = TP + FN, D- = FP + TN, in counts
  and in shares, and each branch pair to 1 -- for a grid of inputs and two tests; the emulator's case
  (sens 0.835: T+ 84, T- 16, not 17); node pages and the 2x2 view agree with the boxes.
Part C (8b): the first-level numbers sit clear of the branch lines; their tap boxes moved with them.
Part G (8b): beta 8b against beta 8a -- only the routines named in the CHANGES differ.

Part A (desktop Giac 1.9 against Python):
  every CAS template the program can build -- exact PPV, NPV, 1 - PPV, the break-even
  solve and the symbolic solve, for one and two tests -- is built EXACTLY as the program
  builds it (a Python replica of bt_Rat / bt_RT / bt_RC / bt_ExactUpd), run through icas,
  and compared with Python's fractions.Fraction (and SymPy for the symbolic solves).
  Also: bt_Rat recovers the student's ratios; no CAS text ever holds a decimal point.

Part B (the program itself, harness ppl_run_v3, cas='giac' and cas='fail'):
  the tree's exact panel and badge, the break-even mark and lines, the CAS asked only on
  events (never during a slider or branch drag; the break-even never on a prior change),
  the Exact page (natural frequencies, Bayes with the numbers, the solve), forensic and
  two-test modes, Enter counts, the PPV view's break-even mark, the decimal fallback with
  no error, the slow-CAS switch, stale-key mode, the layout, and a regression run of the
  beta 7 verification against beta 8.

Part G (8a): beta 8 in harness v3b (its bt_Cas returns its own text: no fraction anywhere), and
  beta 8a against beta 8 (only bt_Cas differs).

Run:  python3 verify_BayesTree_beta8b.py      (exit code 0 = all passed)
"""
import math
import os
import re
import subprocess
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3d import Harness, giac_eval, prime_eval   # noqa: E402
from ppl_run_v3d import CANCEL   # noqa: E402
import ppl_run_v3d   # noqa: E402

PROG = '/home/claude/work/out/BayesTree_beta8c.txt'
BETA8B = '/home/claude/work/out/BayesTree_beta8b.txt'
BETA8 = '/home/claude/work/out/BayesTree_beta8.txt'
BETA8A = '/home/claude/work/out/BayesTree_beta8a.txt'


# 8c: every harness made in this script is remembered, for part R8 (the scientific STRING results
# that harness v3d records in h.sci_strings)
ALL_H = []
_h_init = Harness.__init__


def _h_init_rec(self, *a, **k):
    _h_init(self, *a, **k)
    ALL_H.append(self)


Harness.__init__ = _h_init_rec


def cas_text(txt):
    """8a: what bt_Cas hands back on the calculator for this CAS text: string(...) of the answer
    in the Prime's printing, its quotes dropped (BRIEF_CAS_v2)."""
    a = prime_eval('string(' + txt + ')')
    return a[1:-1] if len(a) >= 2 and a[0] == a[-1] == '"' else a
SCR = '/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad'
FAIL = []
NPASS = [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + detail) if detail else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


def hround(x, d=0):
    m = 10 ** d
    return math.copysign(math.floor(abs(x) * m + 0.5), x) / m


# ------------------------------------------------------------ replicas of the program
def bt_rat(v):
    """bt_Rat: {num, den, kind}."""
    for d in range(7):
        s = v * 10 ** d
        if abs(s - hround(s)) < 1e-6:
            return [int(hround(s)), 10 ** d, 0]
    x, h, h1, k, k1, i, f = v, 1, 0, 0, 1, 0, 0
    while f == 0 and i < 20:
        i += 1
        a = math.floor(x)
        h, h1 = a * h + h1, h
        k, k1 = a * k + k1, k
        if k > 1000000:
            f = 2
        if f == 0 and abs(v - h / k) < 1e-10:
            f = 1
        if f == 0:
            if x - a < 1e-12:
                f = 2
            else:
                x = 1 / (x - a)
    if f == 1:
        return [h, k, 1]
    return [int(hround(v * 1e6)), 1000000, 2]


def rt(r):
    return '%d/%d' % (r[0], r[1])


def rc(r):
    return '%d/%d' % (r[1] - r[0], r[1])


def templates(p, se, spc, tests1=None, forensic=False):
    """The CAS texts bt_ExactUpd builds; tests1 = (se1, sp1) of test 1 when two tests."""
    D, H = rt(bt_rat(p)), rc(bt_rat(p))
    DB = HB = ''
    if tests1:
        DB = rt(bt_rat(tests1[0])) + '*'
        HB = rc(bt_rat(tests1[1])) + '*'
        D += '*' + rt(bt_rat(tests1[0]))
        H += '*' + rc(bt_rat(tests1[1]))
    TS, TC = bt_rat(se), bt_rat(spc)
    ppv = '(' + D + '*' + rt(TS) + ')/(' + D + '*' + rt(TS) + '+' + H + '*' + rc(TC) + ')'
    out = {'ppv': ppv}
    if forensic:
        out['comp'] = '1-' + ppv
    out['npv'] = '(' + H + '*' + rt(TC) + ')/(' + H + '*' + rt(TC) + '+' + D + '*' + rc(TS) + ')'
    out['be'] = ('solve((btq*' + DB + rt(TS) + ')/(btq*' + DB + rt(TS) + '+(1-btq)*' + HB + rc(TC)
                 + ')=1/2,btq)')
    return out


def exact(p, se, spc, tests1=None):
    """Python fractions: PPV, NPV, 1 - PPV, break-even, from the same ratios."""
    fr = lambda v: F(bt_rat(v)[0], bt_rat(v)[1])
    P, S, C = fr(p), fr(se), fr(spc)
    Dw, Hw = P, 1 - P
    lr = S / (1 - C)
    if tests1:
        s1, c1 = fr(tests1[0]), fr(tests1[1])
        Dw, Hw = Dw * s1, Hw * (1 - c1)
        lr *= s1 / (1 - c1)
    ppv = Dw * S / (Dw * S + Hw * (1 - C))
    npv = Hw * C / (Hw * C + Dw * (1 - S))
    return {'ppv': ppv, 'npv': npv, 'comp': 1 - ppv, 'be': 1 / (1 + lr)}


def strip(s):
    t = ''.join(c for c in s if c not in '[]{} ')
    return t[4:] if t.startswith('list') else t


def isfr(s):
    return len(s) > 0 and all(c in '0123456789/-' for c in s)


# ====================================================================== PART A
print('== A. every CAS template through desktop Giac 1.9, against Python fractions ==')
ver = subprocess.run(['giac', '--version'], capture_output=True, text=True).stdout.strip().split('\n')[0]
print('   (icas: %s)' % (ver or 'giac'))

# A1. bt_Rat recovers what the student entered
cases = [(0.95, (95, 100)), (0.014, (14, 1000)), (0.0001, (1, 10000)), (0.999, (999, 1000)),
         (45 / 50, (9, 10)), (920 / 950, (92, 95)), (7 / 9, (7, 9)), (2 / 3, (2, 3)), (30 / 950, (3, 95))]
bad = []
for v, want in cases:
    r = bt_rat(v)
    if F(r[0], r[1]) != F(*want):
        bad.append((v, r, want))
check('A1 bt_Rat: decimals as n/10^d, count ratios recovered exactly (92/95, 7/9, 2/3)', not bad, str(bad))
r = bt_rat(0.12345678)
check('A1 bt_Rat: a value with more than 6 decimals is rounded and flagged (kind 2)', r[2] == 2, str(r))

# A2. the grid of inputs (priors from the ladder / slider / typed; sens and spec from
# arrows, drags, typing and Enter counts)
priors = [0.0001, 0.001, 0.01, 0.014, 0.05, 0.1, 0.5, 0.9, 0.986, 0.999, 1 / 20]
tests = [(0.9, 0.95), (0.95, 0.95), (0.99, 0.999), (0.905, 0.951), (0.5, 0.5), (0.01, 0.999),
         (0.999, 0.01), (45 / 50, 920 / 950), (7 / 9, 0.8)]
n_t, bad, decimals, times = 0, [], [], []
for p in priors:
    for se, spc in tests:
        for t1 in (None, (0.9, 0.95)):
            for forensic in (False, True):
                tp = templates(p, se, spc, t1, forensic)
                ex = exact(p, se, spc, t1)
                for key, txt in tp.items():
                    if '.' in txt:
                        decimals.append(txt)
                    if key == 'be' and forensic:
                        continue            # the same template as without forensic
                    out = cas_text(txt)          # 8a: the Prime's printing
                    n_t += 1
                    got = strip(out)
                    if not isfr(got) or F(got) != ex[key]:
                        bad.append((p, se, spc, t1, key, txt, out, ex[key]))
check('A2 %d CAS texts (PPV, NPV, 1 - PPV, break-even; 1 and 2 tests): Giac = Python fractions'
      % n_t, not bad, str(bad[:2]))
check('A2 no CAS text holds a decimal point (BRIEF_CAS rule 1)', not decimals, str(decimals[:2]))

# A3. the worked examples, by name
for (p, se, spc, t1, key, want) in [
        (0.01, 0.95, 0.95, None, 'ppv', '19/118'), (0.01, 0.95, 0.95, None, 'npv', '1881/1882'),
        (0.01, 0.95, 0.95, None, 'be', '1/20'), (0.1, 0.9, 0.95, None, 'ppv', '2/3'),
        (0.1, 0.9, 0.95, (0.9, 0.95), 'ppv', '36/37'), (0.1, 0.9, 0.95, (0.9, 0.95), 'be', '1/325'),
        (0.05, 0.9, 920 / 950, None, 'ppv', '3/5'), (0.1, 0.9, 0.95, None, 'comp', '1/3')]:
    got = strip(cas_text(templates(p, se, spc, t1, key == 'comp')[key]))
    check('A3 %s(prior %g, %g / %g%s) = %s' % (key, p, se, spc, ', 2 tests' if t1 else '', want),
          got == want, got)
# the natural-frequency fraction of the task: 95/590 reduces to 19/118 (Python)
check('A3 natural frequencies at N = 10000: TP 95, FP 495, PPV 95/590 = 19/118 = 0.161',
      F(95, 590) == F(19, 118) and '%.3f' % (95 / 590) == '0.161')

# A4. the symbolic solves (page 2) against SymPy
q, s_, c_, l_, m_ = sp.symbols('btq bts btc btl btm', positive=True)
g1r = cas_text('solve(btq*bts/(btq*bts+(1-btq)*(1-btc))=1/2,btq)')
g2r = cas_text('solve(btq*btl*btm/(btq*btl*btm+1-btq)=1/2,btq)')
check('A4 8a: the solves arrive in the Prime\'s braces (%s, %s), which bt_Strip drops' % (g1r, g2r),
      g1r.startswith('{') and g1r.endswith('}') and g2r.startswith('{') and 'list' not in g1r + g2r)
g1, g2 = strip(g1r), strip(g2r)
loc = {'btq': q, 'bts': s_, 'btc': c_, 'btl': l_, 'btm': m_}
e1 = sp.sympify(g1, locals=loc)
e2 = sp.sympify(g2, locals=loc)
t1 = sp.solve(sp.Eq(q * s_ / (q * s_ + (1 - q) * (1 - c_)), sp.Rational(1, 2)), q)[0]
t2 = sp.solve(sp.Eq(q * l_ * m_ / (q * l_ * m_ + 1 - q), sp.Rational(1, 2)), q)[0]
check('A4 symbolic break-even, 1 test: Giac %s = SymPy %s' % (g1, t1), sp.simplify(e1 - t1) == 0)
check('A4 symbolic break-even, 2 tests: Giac %s = SymPy %s' % (g2, t2), sp.simplify(e2 - t2) == 0)
check('A4 the solve is linear in the prior: exactly one root, so the Strip step needs no choice',
      len(sp.solve(sp.Eq(q * s_ / (q * s_ + (1 - q) * (1 - c_)), sp.Rational(1, 2)), q)) == 1)

# A5. the break-even, PPL's number (it places the mark) = the CAS's fraction
worst = 0
for p in (0.1,):
    for se, spc in tests:
        for t1 in (None, (0.9, 0.95)):
            lr = se / (1 - spc) * ((t1[0] / (1 - t1[1])) if t1 else 1)
            pp = 1 / (1 + lr)
            worst = max(worst, abs(pp - float(exact(p, se, spc, t1)['be'])))
check('A5 bt_BEp (PPL, draws the mark) = the CAS break-even, every test and both chains',
      worst < 1e-12, 'max diff %.1e' % worst)

# ====================================================================== PART B
print('\n== B. the program in the harness (ppl_run_v3d), cas = giac and cas = fail ==')


def run(script, cas='giac', stale=False, prog=PROG):
    h = Harness(prog, strict=True, cas=cas, stale_keys=stale)
    script(h)
    h.call('BayesTree')
    return h


def trees(h):
    return [s for s in h.pages if s.func == 'BayesTree']


def panel(page):
    return [t.text for t in page.texts if t.x == 214]


def cas_names(h):
    # 8a: the CAS text now arrives as string(...)
    body = lambda t: t[7:] if t.startswith('string(') else t
    return [('solve' if body(c[0]).startswith('solve') else ('1-' if body(c[0]).startswith('1-') else 'frac'))
            for c in h.cas_calls]


# B1. defaults
h = run(lambda h: (h.choose('Close'), h.press('Esc')))
tr = trees(h)[-1]
check('B1 defaults: panel PPV = 2/3, NPV = 171/173, badge exact (CAS)',
      panel(tr)[:3] == ['PPV = 2/3', 'NPV = 171/173', 'exact (CAS), tap'], str(panel(tr)))
check('B1 defaults: break-even lines "Most T+ are false / if prior < 5.3 %" (1/19)',
      panel(tr)[3:] == ['Most T+ are false', 'if prior < 5.3 %'], str(panel(tr)[3:]))
check('B1 defaults: the CAS was asked 3 times for the first frame (PPV, NPV, break-even)',
      len(h.cas_calls) == 3, str([c[0] for c in h.cas_calls]))
check('B1 summary on exit carries the exact PPV', h.result.startswith('BayesTree: PPV = 0.667 = 2/3,'), h.result)
check('B1 8a: every CAS text asks for string(...), every answer arrives quoted; no CAS variable assigned, '
      'no CAS call of a variable',
      all(c[0].startswith('string(') and c[1].startswith('"') for c in h.cas_calls)
      and not h.cas_vars and not any('non-literal' in w for w in h.warnings), str(h.cas_calls[:1]))
# the slider mark: magenta at bt_SlX(1/19), the tint left of it
LGL = math.log(0.001 / 0.999)
slx = lambda pv: 174 + hround((math.log(pv / (1 - pv)) - LGL) / (-2 * LGL) * 136)
bx = slx(1 / 19)
mk = [sh for sh in tr.shapes if sh.cmd == 'LINE_P' and sh.args[0] == bx and sh.args[1] == 2 and sh.args[3] == 8]
tint = [sh for sh in tr.shapes if sh.cmd == 'RECT_P' and sh.args[0:4] == [175, 10, bx, 11]]
check('B1 break-even mark: magenta line above the track at x = %d (bt_SlX(1/19)), red tint left of it' % bx,
      len(mk) == 1 and len(tint) == 1, '%d mark, %d tint' % (len(mk), len(tint)))
low = [t for t in tr.texts if t.y >= 218 or t.x + t.est_width > 318]
check('B1 layout: no tree text reaches the soft keys (y >= 218) or x 318', not low, str([(t.text, t.x, t.y) for t in low]))

# B2. the task's example: Enter values 0.01 / 0.95 / 0.95
ex_script = lambda h: (h.choose('Enter values'), h.answer({'pr2': 0.01, 'se2': 0.95, 'sp2': 0.95, 'np2': 1000}),
                       h.press('Enter'), h.choose('Exact answers'), h.press('Enter'), h.press('Enter'),
                       h.press('Esc'))
h = run(ex_script)
pages = [s for s in h.pages if s.func == 'bt_PageL']
p1 = pages[0].lines() if pages else []
p2 = pages[1].lines() if len(pages) > 1 else []
check('B2 example tree panel: PPV = 19/118, NPV = 1881/1882', panel(trees(h)[-1])[:2] == ['PPV = 19/118', 'NPV = 1881/1882'],
      str(panel(trees(h)[-1])))
for want in ('Picture N = 10000 people (natural frequencies):', 'TP = 95, FP = 495, FN = 5, TN = 9405',
             'PPV = TP/(TP+FP) = 95/590', '    = 19/118 = 0.161', '    = 1881/1882 = 0.999',
             '    prior = 1/20 = 0.0500 = 5.0 %', 'Below a prior of 5.0 %, a positive result is more'):
    check('B2 Exact page 1 shows "%s"' % want.strip(), want in p1)
for want in ('PPV = TP/(TP+FP) = p×se / (p×se + (1−p)×(1−sp))', '    = 0.01×0.95 / (0.01×0.95 + 0.99×0.05)',
             '    p = (-sp+1)/(-sp+se+1)', '    your numbers: p = 1/20 = 0.0500'):
    check('B2 Exact page 2 shows "%s"' % want.strip(), want in p2)
check('B2 both pages carry the badge "exact (CAS)"', all(pg.has('exact (CAS)') for pg in pages[:2]))
over = [(t.text, round(t.x + t.est_width)) for pg in pages for t in pg.texts if t.x + t.est_width > 318]
check('B2 layout: no Exact-page line past x 318 (estimated widths)', not over, str(over))
check('B2 opening the page asked the CAS once more (the symbolic solve), the rest was cached',
      cas_names(h).count('solve') == 2 and len(h.cas_calls) == 4 + 0, str(cas_names(h)))

# B3. slider drag: no CAS call while the finger is down; PPV/NPV once on the lift; no solve
xs = [210, 200, 190, 180, 176]
h = run(lambda h: (h.choose('Close'), h.drag([(x, 10) for x in xs]), h.press('Esc')))
trs = trees(h)
drag_frames = trs[1:-1]
check('B3 slider drag: every drag frame says "exact: on lift" (no stale fraction shown)',
      drag_frames and all(panel(f)[0] == 'exact: on lift' for f in drag_frames),
      str([panel(f)[0] for f in drag_frames]))
check('B3 slider drag: CAS asked 3 times at the start and 2 times after the lift (PPV, NPV) -- no solve',
      cas_names(h) == ['frac', 'frac', 'solve', 'frac', 'frac'], str(cas_names(h)))
check('B3 slider drag: the break-even lines stay put through the drag (they do not depend on the prior)',
      all(panel(f)[-1] == 'if prior < 5.3 %' for f in trs), str({panel(f)[-1] for f in trs}))
def leaves(page):
    return [t.text for t in page.texts if t.x == 216 and t.font == 2]


def want_leaves(pv, se=0.9, spc=0.95, N=1000):
    # 8b: as bt_RCnt does it -- D+ and each T+ rounded, each complement its parent minus that
    # (8a rounded every box by itself: 5 - 4.5 = 0.5 rounded to 1, and the pair made 6)
    d = N * pv
    hh = N - d
    tp = d * se
    fp = hh * (1 - spc)
    rd = min(N, hround(d)); rh = N - rd
    rtp = min(rd, hround(tp)); rfp = min(rh, hround(fp))
    return ['T+ %d' % rtp, 'T− %d' % (rd - rtp), 'T+ %d' % rfp, 'T− %d' % (rh - rfp)]


def sig2(pv):
    qq = max(min(pv, 1 - pv), 0.001)
    dd = min(3, 1 - math.floor(math.log10(qq)))
    qq = hround(qq, dd)
    return 1 - qq if pv > 0.5 else qq


def slp(x):
    u = min(1, max(0, (x - 174) / 136))
    return sig2(1 / (1 + math.exp(-(LGL + u * (-2 * LGL)))))


# the priors the frames are for: the start, one per changed sample, the lift frame
want_p = [0.1]
for x in xs:
    if slp(x) != want_p[-1]:
        want_p.append(slp(x))
want_p.append(want_p[-1])
bad = []
for f, pv_ in zip(trs, want_p):
    if sorted(leaves(f)) != sorted(want_leaves(pv_)):
        bad.append((pv_, leaves(f), want_leaves(pv_)))
check('B3 8b: slider drag: the four leaves re-count in every frame, the lift frame too, each pair adding up (%d frames)' % len(trs),
      not bad, str(bad[:2]))
check('B3 slider drag: exactly one extra frame after the lift (the CAS update), same prior as the last sample',
      len(trs) == 1 + len(set(xs)) + 1 and trs[-1].lines()[1] == trs[-2].lines()[1],
      '%d frames' % len(trs))
last = panel(trs[-1])
p_end = float(re.search(r'prior ([0-9.]+)', ' '.join(t.text for t in trs[-1].texts if t.y == 6)).group(1))
ex_end = exact(p_end, 0.9, 0.95)['ppv']
check('B3 after the lift the panel shows the exact PPV for the new prior (%g): %s' % (p_end, last[0]),
      last[0] in ('PPV = %s' % ex_end, 'PPV: %d digits' % sum(c.isdigit() for c in str(ex_end))), str(last))

# B4. a drag of the D+ pair (sens): the mark follows live (PPL), the CAS waits for the lift
h = run(lambda h: (h.choose('Close'), h.drag([(185, 60), (185, 66), (185, 70), (185, 90)]), h.press('Esc')))
trs = trees(h)
marks = []
for f in trs:
    m = [sh.args[0] for sh in f.shapes if sh.cmd == 'LINE_P' and sh.args[1] == 2 and sh.args[3] == 8
         and sh.args[0] == sh.args[2]]
    marks.append(m[0] if m else None)
check('B4 sens drag: the break-even mark moves in the drag frame, before the lift (PPL), %s' % marks,
      len(marks) >= 3 and marks[1] != marks[0] and panel(trs[1])[0] == 'exact: on lift')
check('B4 sens drag: CAS asked 3 times at the start, then 3 after the lift (PPV, NPV, solve)',
      cas_names(h) == ['frac', 'frac', 'solve', 'frac', 'frac', 'solve'], str(cas_names(h)))
sens_end = h.globals_.get('btSe')
# B5. a key is an event: Right (spec + 0.01) asks PPV, NPV and the break-even once
h = run(lambda h: (h.choose('Close'), h.press('Right'), h.press('Esc')))
check('B5 a key (Right, spec 0.96): one update of 3 CAS calls, then the panel is exact',
      len(h.cas_calls) == 6 and panel(trees(h)[-1])[0] == 'PPV = %s' % exact(0.1, 0.9, 0.96)['ppv'],
      '%d calls, %s' % (len(h.cas_calls), panel(trees(h)[-1])))
# same key twice in a row with no change (Left then Right back): cached values are reused
h = run(lambda h: (h.choose('Close'), h.press('Right'), h.press('Left'), h.press('Esc')))
check('B5 back to a value seen before still asks again (one cache, by design): 9 calls',
      len(h.cas_calls) == 9, str(len(h.cas_calls)))
# a tap on a box (no value change): no CAS call for the redraw
h = run(lambda h: (h.choose('Close'), h.tap(40, 110, lift=True), h.press('Enter'), h.press('Esc')))
check('B5 tapping a box and closing its page: no new CAS call (inputs unchanged)', len(h.cas_calls) == 3,
      str(len(h.cas_calls)))

# B6. forensic
h = run(lambda h: (h.choose('Forensic'), h.press('Esc')))
check('B6 forensic panel: PPV = 2/3, 1−PPV = 1/3, "Most matches false / below 1 in 19"',
      panel(trees(h)[-1]) == ['PPV = 2/3', '1−PPV = 1/3', 'exact (CAS), tap', 'Most matches false', 'below 1 in 19'],
      str(panel(trees(h)[-1])))

# B7. two tests
h = run(lambda h: (h.choose('Second test'), h.answer({'se2': 0.9, 'sp2': 0.95}), h.press('Enter'),
                   h.choose('Exact answers'), h.press('Enter'), h.press('Enter'), h.press('Esc')))
pg = [s for s in h.pages if s.func == 'bt_PageL']
check('B7 two tests panel: PPV = 36/37 (= 0.972973), NPV = 19/23, "Most T+T+ false / if prior < 0.31 %"',
      panel(trees(h)[-1]) == ['PPV = 36/37', 'NPV = 19/23', 'exact (CAS), tap', 'Most T+T+ false', 'if prior < 0.31 %'],
      str(panel(trees(h)[-1])))
check('B7 two tests Exact page: N = 100000, 13500 positive on test 1, prior = 1/325',
      pg[0].has('Picture N = 100000: 13500 test + on test 1,') and pg[0].has('    prior = 1/325 = 0.0031 = 0.31 %'))
check('B7 two tests page 2: the CAS solve in LR form, p = 1/(LR₁×LR₂+1)', pg[1].has('    p = 1/(LR₁×LR₂+1)'))
be2 = 1 / (1 + 18 * 18)
bx2 = slx(be2)
mk = [sh for sh in trees(h)[-1].shapes if sh.cmd == 'LINE_P' and sh.args[0] == bx2 and sh.args[1] == 2]
check('B7 two tests: the slider mark sits at the base prior 1/325 (x = %d)' % bx2, len(mk) == 1)

# B8. Enter counts: the student's ratios come back exactly
h = run(lambda h: (h.choose('Enter counts'), h.answer({'tp': 45, 'fn': 5, 'btFP': 30, 'tn': 920}),
                   h.press('Esc')))
check('B8 Enter counts 45/5/30/920: PPV = 3/5 (= 45/75), NPV = 184/185 (= 920/925)',
      panel(trees(h)[-1])[:2] == ['PPV = 3/5', 'NPV = 184/185'], str(panel(trees(h)[-1])))

# B9 / B10. the panel tap and the soft key open the Exact page
h = run(lambda h: (h.choose('Close'), h.tap(260, 115, lift=True), h.press('Esc'), h.press('Esc')))
check('B9 a tap on the exact panel opens the Exact page', any(s.func == 'bt_PageL' for s in h.pages))
h = run(lambda h: (h.choose('Close'), h.tap(300, 230, lift=True), h.tap(300, 230, lift=True),
                   h.tap(240, 230, lift=True), h.press('Esc'), h.press('Esc')))
check('B10 soft key page 3, slot 5 "Exact" opens the Exact page', any(s.func == 'bt_PageL' for s in h.pages))

# B11. the PPV view: the break-even point where the PPV curve crosses 1/2
h = run(lambda h: (h.choose('PPV vs prevalence'), h.press('Esc'), h.choose('Close'), h.press('Esc')))
pv = [s for s in h.pages if s.func == 'bt_PrevView'][0]
bxp, byp = 40 + int((1 / 19) * 250), 183 - int(0.5 * 153)
sq = [sh for sh in pv.shapes if sh.cmd == 'RECT_P' and sh.args[0:4] == [bxp - 2, byp - 2, bxp + 2, byp + 2]]
check('B11 PPV view: magenta square at the crossing (x %d, y %d)' % (bxp, byp), len(sq) == 1)
check('B11 PPV view: "Below 5.3 %, most positives are false (PPV < 1/2)."',
      pv.has('Below 5.3 %, most positives are false (PPV < 1/2).'))
txt = [t for t in pv.texts if t.y >= 186 and t.y < 210]
check('B11 PPV view layout: tick labels at y 189, the sentence at y 199, readout 212, footer 226',
      sorted({t.y for t in pv.texts if t.y > 183}) == [189.0, 199.0, 212.0, 226.0],
      str(sorted({t.y for t in pv.texts if t.y > 183})))

# B12. the fallback: every CAS call fails -> decimals, the badge, no error
h = run(ex_script, cas='fail')
pages = [s for s in h.pages if s.func == 'bt_PageL']
check('B12 cas=fail: no runtime error, the program ends normally', h.error is None and h.result.startswith('BayesTree:'),
      str(h.error))
check('B12 cas=fail: tree panel shows the decimals and "decimal, tap"',
      panel(trees(h)[-1])[:3] == ['PPV = 0.161', 'NPV = 0.999', 'decimal, tap'], str(panel(trees(h)[-1])))
check('B12 cas=fail: Exact pages say "decimal", keep the natural-frequency fraction 95/590 (PPL counts)',
      all(pg.has('decimal') for pg in pages) and pages[0].has('PPV = TP/(TP+FP) = 95/590')
      and pages[0].has('    = 0.161  (decimal)'))
check('B12 cas=fail: page 2 gives the break-even by hand and says no CAS answer',
      pages[1].has('    p = (1 − sp)/(se + 1 − sp)   (no CAS: by hand)')
      and pages[1].has("(No CAS answer: the decimals are the program's.)"))
check('B12 cas=fail: the summary has no fraction', ' = ' not in h.result.split(',')[0].replace('PPV = ', ''), h.result)
# 8c: beta 8b in harness v3d stops on this very run -- INSTRING("", ...) is "Invalid input" on the
# Prime (emulator, round 2); bt_Cas tested INSTRING(cR, "undef") on the "" of a failed call
try:
    h8b = run(ex_script, cas='fail', prog=BETA8B)
    err8b = h8b.error
except Exception as e:          # the harness raises the PPL error out of h.call
    err8b = e
check('B12 8c: beta 8b in harness v3d STOPS on the same cas=fail run (%s)' % str(err8b)[:80],
      err8b is not None and 'INSTRING' in str(err8b))

# B13. a slow CAS: the tree stops asking by itself (threshold patched to -1 in a copy)
src = open(PROG, encoding='utf-8').read()
slow = os.path.join(SCR, 'BayesTree_beta8c_slowcas.txt')
open(slow, 'w', encoding='utf-8').write(src.replace('IF btCasMs > 1500 THEN', 'IF btCasMs > -1 THEN'))
h = run(lambda h: (h.choose('Close'), h.press('Right'), h.tap(260, 115, lift=True), h.press('Esc'),
                   h.press('Esc')), prog=slow)
trs = trees(h)
check('B13 slow CAS: after the first update the tree says "tap for exact" and asks no more',
      panel(trs[1])[0] == 'tap for exact', str(panel(trs[1])))
pg = [s for s in h.pages if s.func == 'bt_PageL']
check('B13 slow CAS: a tap still opens the Exact page, which asks the CAS and says the tree waits for a tap',
      pg and pg[0].has('    = 2/3 = 0.667'.replace('2/3', str(exact(0.1, 0.9, 0.96)['ppv']))
                       .replace('0.667', '%.3f' % float(exact(0.1, 0.9, 0.96)['ppv'])))
      and any('the tree asks on a tap' in t.text for t in pg[0].texts))

# B14. stale-key mode: the menu's Enter left in the buffer does not skip an Exact page
h = run(ex_script, stale=True)
check('B14 stale-key mode: no page skipped on the way to and through the Exact pages',
      not h.stale_skips and len([s for s in h.pages if s.func == 'bt_PageL']) == 2, str(h.stale_skips))

# B15. help page 4
h = run(lambda h: (h.choose('Help'), h.press('Enter'), h.press('Enter'), h.press('Enter'), h.press('Enter'),
                   h.choose('Close'), h.press('Esc')))
hp = [s for s in h.pages if s.func == 'bt_HelpView']
check('B15 help: four pages, page 4 "exact answers (CAS)", all text above y 218 and inside x 318',
      len(hp) == 4 and hp[3].has('Help 4/4: exact answers (CAS)')
      and all(t.y < 218 or t.y == 226 for s in hp for t in s.texts)
      and all(t.x + t.est_width <= 318 for s in hp for t in s.texts))

# B17. 8a: canned answers as the calculator gives them: string(...) answers (PPL strings, so
# STRING() adds the quotes bt_Cas drops), the solve in braces (CASProbe beta 1b T18).
canned = {'string((1/10*9/10)/(1/10*9/10+9/10*5/100))': '"2/3"',
          'string((9/10*95/100)/(9/10*95/100+1/10*1/10))': '"171/173"',
          'string(solve((btq*9/10)/(btq*9/10+(1-btq)*5/100)=1/2,btq))': '"{1/19}"'}
h = run(lambda h: (h.choose('Close'), h.press('Esc')), cas=canned)
check('B17 answers wrapped in quotes: the kit strips them, the panel still shows PPV = 2/3, NPV = 171/173',
      panel(trees(h)[-1])[:3] == ['PPV = 2/3', 'NPV = 171/173', 'exact (CAS), tap'], str(panel(trees(h)[-1])))
# and an answer in decimals (a CAS left in approximate mode) is refused as "exact"
canned2 = dict(canned)
canned2['string((1/10*9/10)/(1/10*9/10+9/10*5/100))'] = '"0.666666666667"'
h = run(lambda h: (h.choose('Close'), h.press('Esc')), cas=canned2)
check('B17 a decimal answer (approximate mode) is not shown as exact: PPV = 0.667, badge decimal',
      panel(trees(h)[-1])[:3] == ['PPV = 0.667', 'NPV = 171/173', 'decimal, tap'], str(panel(trees(h)[-1])))

# ---- B16. the beta 7 verification, run against beta 8 (regression) ----
print('\n== B16. beta 7\'s verify_BayesTree.py run against beta 8c (harness v3d) ==')
old = open('/home/claude/work/out/verify_BayesTree.py', encoding='utf-8').read()
old = old.replace("PROG = '/home/claude/work/out/BayesTree_beta7.txt'", "PROG = '%s'" % PROG)
old = old.replace('from ppl_run_v1 import Harness', 'from ppl_run_v3d import Harness')
old = old.replace("sys.path.insert(0, '/home/claude/work/harness')", "sys.path.insert(0, '/home/claude/work/out')")
reg = os.path.join(SCR, 'verify_BayesTree_on_beta8c.py')
open(reg, 'w', encoding='utf-8').write(old)
res = subprocess.run([sys.executable, reg], capture_output=True, text=True)
fails = [ln for ln in res.stdout.split('\n') if ln.startswith('FAIL')]
npass = sum(1 for ln in res.stdout.split('\n') if ln.startswith('PASS'))
print('   %d PASS, %d FAIL' % (npass, len(fails)))
for ln in fails:
    print('   ' + ln)
# The beta 7 checks that beta 8 changes ON PURPOSE (each is re-checked above):
#   'A summary returned'      the summary now carries the exact PPV (" = 2/3")       -> B1
#   'B slider: one redraw...' one extra frame after the lift: the CAS update        -> B3
#   'B slider: all six...'    the same extra frame shifts beta 7's frame alignment;
#                             B3 re-counts every frame, the lift frame included     -> B3
#   'E More cycles...'        soft-key page 3 slot 5 is now "Exact" (was empty)     -> B10
#   'I breadcrumb ...'        8c: the two-test breadcrumb is laid out from MEASURED
#                             widths, not at x 2 / 38 / 74, so the next number cannot
#                             cover the arrow (round 2)                             -> R3
INTENDED = ('A summary returned', 'B slider: one redraw per changed drag sample',
            'B slider: all six boxes re-count at every sample', 'E More cycles three pages and back',
            'I breadcrumb 0.10 -> 0.67 -> 0.97')
unexpected = [f for f in fails if not any(f.startswith('FAIL ' + k) for k in INTENDED)]
check('B16 every other beta 7 check passes on beta 8c (%d pass; the %d intended changes listed above)'
      % (npass, len(fails) - len(unexpected)), not unexpected, str(unexpected))

# ---- G (8a). beta 8 in v3b: the emulator's finding; and 8a against 8 ----
print('\n== G. beta 8 in harness v3d (the CAS finding stays), and beta 8b against beta 8a ==')
h8 = run(lambda h: (h.choose('Close'), h.press('Esc')), prog=BETA8)
check('G beta 8 in v3d: its bt_Cas hands back its own text, so the panel shows decimals only (%s)'
      % panel(trees(h8)[-1])[:3], panel(trees(h8)[-1])[:3] == ['PPV = 0.667', 'NPV = 0.988', 'decimal, tap']
      and any('non-literal' in w for w in h8.warnings), str(panel(trees(h8)[-1])))
say = print
# 8c: the beta 8b-against-8a checks are kept as they were, on those two files
SRC = BETA8B
FAILS = FAIL


_saved_check = check


def _check2(cond, msg):
    _saved_check(msg, cond)


check = _check2

# ================================================================ G (8b)
say('\nG. beta 8b against beta 8a')
import re as _re
_b_old = open(BETA8A, encoding='utf-8').read()
_b_new = open(SRC, encoding='utf-8').read()


def _bodies(txt):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)
    c = _re.sub(r'//[^\n]*', '', c)
    out = {}
    for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
        out[m.group(1)] = _re.sub(r'[ \t]+\n', '\n', m.group(0))
    return out


_B0, _B1 = _bodies(_b_old), _bodies(_b_new)
_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))
_want = ['BayesTree', 'bt_FaganView', 'bt_PrevView', 'bt_RCnt', 'bt_RPrb', 'bt_RocView', 'bt_WaitAny', 'bt_fmtq']
check(_diff == _want, 'beta 8b: routines that differ from beta 8a: %s (want %s)' % (_diff, _want))
check(all(n not in _B0 for n in ('bt_RCnt', 'bt_RPrb', 'bt_fmtq')), 'beta 8b: bt_RCnt, bt_RPrb, bt_fmtq are new')


def _outside(t, names):
    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\n]*', '', t))
    if names:
        c = _re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
    return _re.sub(r'\s+', ' ', c)


_newline = 'LOCAL btTLX, btTLY, btTLi;'
check(_outside(_b_new, _diff).count(_newline) == 1, 'beta 8b: one new file-level LOCAL line, the stale-click list')
check(_outside(_b_old, _diff) == _outside(_b_new, _diff).replace(_newline + ' ', ''),
      'beta 8b: outside those routines and that line only comments differ')
_c0 = _re.sub(r'//[^\n]*', '', _B0['bt_Cas']); _c1 = _re.sub(r'//[^\n]*', '', _B1['bt_Cas'])
check(_c0 == _c1, 'beta 8b: bt_Cas (the CAS call form) is byte-identical to beta 8a')
say('  routines that differ from beta 8a: %s; everything else differs only in comments' % ', '.join(_diff))

check = _saved_check


# ====================================================================== PART S (8b)
print('\n== S. 8b: soft keys under WAIT(-1), as the emulator answers (harness v3d) ==')


def slot_x(k):
    """the middle of soft key k (1..6): slots are 53.4 px wide"""
    return int(53.4 * (k - 0.5))


def run_v(prog, script, cas='fail', **kw):
    h = Harness(prog, strict=True, cas=cas, **kw)
    script(h)
    h.call('BayesTree')
    return h


def funcs(h):
    return [s.func for s in h.pages]


def inputs(h):
    return [d.title for d in h.inputs]


# S1. page 1: every soft key runs its item from a type-3 click (the only event a strip tap sends)
page1 = [(1, 'input', 'Exact Values'), (2, 'input', 'Leaf Counts (2x2)'), (3, 'page', 'bt_RocView'),
         (4, 'page', 'bt_PrevView'), (5, 'page', 'bt_Tbl2View')]
for k, kind, what in page1:
    def sc(h, k=k, kind=kind):
        h.choose('Close')
        h.tap(slot_x(k), 230)
        if kind == 'input':
            h.answer(CANCEL)
        else:
            h.press('Esc')
        h.press('Esc')
    h = run_v(PROG, sc)
    got = (what in inputs(h)) if kind == 'input' else (what in funcs(h))
    clicks = [e for e in h.timeline if e[0] == 'event' and 'WAIT(-1)' in str(e[2])]
    check('S1 8b: soft key %d (%s) runs from the type-3 strip click alone' % (k, ['Values', 'Counts', 'ROC', 'PPV', '2×2'][k - 1]),
          got and h.error is None,
          '%s %s' % (inputs(h), sorted(set(funcs(h)))))
# S2. beta 8a under v3d: the same taps do nothing -- the emulator's finding
for k, kind, what in page1[:3]:
    def sc(h, k=k):
        h.choose('Close'); h.tap(slot_x(k), 230); h.press('Esc')
    # 8c: cas='giac' -- under harness v3d beta 8a stops on a failed CAS call (INSTRING("", ...))
    h = run_v(BETA8A, sc, cas='giac')
    got = (what in inputs(h)) if kind == 'input' else (what in funcs(h))
    check('S2 8b: beta 8a in v3d: soft key %d does nothing (the emulator: "tapping Values or ROC does '
          'nothing")' % k, not got and not h.inputs and h.error is None, str(sorted(set(funcs(h)))))
# S3. More steps the pages and wraps; page 2 Help and page 3 Leaves and Exact run
h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(6), 230), h.tap(slot_x(6), 230),
                             h.tap(slot_x(6), 230), h.press('Esc')))
menus = [tuple(s.menu) for s in h.pages if s.func == 'BayesTree' and s.menu] + \
        [tuple(s.menu) for s in h.screens if s.menu]
labels = [m[0] for m in [tuple(s.menu) for s in h.screens if s.menu]]
check('S3 8b: More (slot 6) steps page 1 -> 2 -> 3 -> 1 from type-3 clicks',
      ['Values', 'Diag', 'Test 2', 'Values'] == [l for i, l in enumerate(labels) if i == 0 or l != labels[i - 1]][:4],
      str(labels))
h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(6), 230), h.tap(slot_x(5), 230),
                             h.press('Esc'), h.press('Esc'), h.press('Esc'), h.press('Esc'), h.press('Esc')))
check('S3 8b: page 2 slot 5 (Help) opens the help pages', 'bt_HelpView' in funcs(h), str(sorted(set(funcs(h)))))
h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(6), 230), h.tap(slot_x(6), 230),
                             h.tap(slot_x(4), 230), h.press('Esc')))
tr = trees(h)[-1]
check('S3 8b: page 3 slot 4 (Leaves) turns the leaves into shares (T+ 0.090 ...)',
      any(t.text == 'T+ 0.090' for t in tr.texts), str([t.text for t in tr.texts if t.x == 216][:4]))
# S4. no tap runs twice
h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(2), 230, lift=True), h.press('Esc')),
          wait_model='v3b')
check('S4 8b: a type-0 PRESS on the strip (v3b model: {0, x, y}, {2}) does nothing -- neutralised',
      not h.inputs and h.error is None, str(inputs(h)))


def inject(evs):
    def sc(h):
        h.choose('Close')
        h._pending_wait = [list(map(float, e)) for e in evs]
        h.answer(CANCEL)
        h.press('Esc')
    return sc


h = run_v(PROG, inject([(0, slot_x(2), 230), (2,), (3, slot_x(2), 230)]))
check('S4 8b: a firmware that sent {0}, {2} AND {3} for a strip tap would still run the key ONCE',
      inputs(h) == ['Leaf Counts (2x2)'], str(inputs(h)))
h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(40, 110), h.press('Enter'), h.press('Esc')))
nodes = [s for s in h.pages if s.func == 'bt_NodeInfo']
check('S4 8b: a tap on the root box ({0}, {2}, {3}) opens its node page once, not twice',
      len(nodes) == 1 and nodes[0].has('N — the whole population'), '%d node pages' % len(nodes))
h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(180, 38), h.press('Enter'), h.press('Esc')))
nodes = [s for s in h.pages if s.func == 'bt_NodeInfo']
check('S4 8b: a tap on a branch number opens its page once, on the lift ({2}), not again on the click',
      len(nodes) == 1 and nodes[0].has('Branch: P(T+ | D+) = sens'), '%d node pages' % len(nodes))
# S5. a page closed by a tap on its footer leaves no stale click for the tree
for k, view, fx in ((4, 'bt_PrevView', 150), (3, 'bt_RocView', 100), (None, 'bt_FaganView', 230)):
    def sc(h, k=k, fx=fx):
        if k is None:
            h.choose('Fagan nomogram')
        else:
            h.choose('Close'); h.tap(slot_x(k), 230)
        h.tap(fx, 226)                       # the view's footer: back (no soft keys drawn there)
        h.press('Esc')
    h = run_v(PROG, sc)
    other = [f for f in funcs(h) if f not in ('BayesTree', view)]
    check('S5 8b: %s closed by a tap on its footer (x %d, y 226): its {2}, {3} reach the tree and run no '
          'soft key' % (view, fx), view in funcs(h) and not other and not h.inputs and h.error is None,
          '%s %s' % (sorted(set(funcs(h))), inputs(h)))
# ... and the guard is what does it: the same run with the guard switched off fires slot IP(x/53.4)+1
srcP = open(PROG, encoding='utf-8').read()
noguard = os.path.join(SCR, 'BayesTree_beta8c_noguard.txt')
open(noguard, 'w', encoding='utf-8').write(
    srcP.replace('IF ABS(btMX - btTLX(btTLi)) <= 2 AND ABS(btMY - btTLY(btTLi)) <= 2 THEN', 'IF 0 THEN'))
h = run_v(noguard, lambda h: (h.choose('Close'), h.tap(slot_x(4), 230), h.tap(150, 226), h.press('Esc'),
                                h.press('Esc')))
check('S5 8b: without the guard the PPV view\'s closing click WOULD run soft key 3 (ROC) on the tree',
      'bt_RocView' in funcs(h), str(sorted(set(funcs(h)))))
# a real soft-key tap at that same spot right after still works (the guard skips one click only)
h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(4), 230), h.tap(150, 226), h.tap(150, 226),
                             h.press('Esc'), h.press('Esc')))
check('S5 8b: the guard skips that one click only: a tap at the same spot afterwards runs ROC',
      'bt_RocView' in funcs(h), str(sorted(set(funcs(h)))))
# S6. the worst case for a page held by bt_WaitAny (MOUSE): its tap's click ALSO reaches WAIT(-1)
h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(40, 110), h.tap(150, 226), h.press('Esc')),
          mouse_tail=True)
other = [f for f in funcs(h) if f not in ('BayesTree', 'bt_NodeInfo')]
check('S6 8b: mouse_tail (not measured): a node page closed by a footer tap leaves its click, which the '
      'tree skips', not other and h.error is None and 'bt_NodeInfo' in funcs(h), str(sorted(set(funcs(h)))))
h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(6), 230), h.tap(slot_x(5), 230),
                             h.tap(150, 226), h.tap(150, 226), h.tap(150, 226), h.tap(150, 226),
                             h.press('Esc')), mouse_tail=True)
check('S6 8b: mouse_tail: four help pages closed by footer taps, back on the tree, no soft key fired',
      [f for f in funcs(h) if f not in ('BayesTree', 'bt_HelpView')] == [] and h.error is None,
      str(sorted(set(funcs(h)))))
check('S7 8b: the stale-click list is filled by the three WAIT(-1) views and bt_WaitAny, and reset by keys and presses',
      srcP.count('btTLX := CONCAT(btTLX') == 4 and srcP.count('btTLX := {}; btTLY := {}; btTLi := 1;') == 3)
check('S7 8b: no WAIT(-1) type-0 test at y >= 218 acts any more; the strip is read from type 3 only',
      'IF btEvT == 3 AND btMY >= 218 THEN' in srcP and 'btNode := 0;\n        ELSE\n          btNode := bt_Hit' in srcP)

# ====================================================================== PART L (8b)
print('\n== L. 8b: every pair on the tree adds up ==')


def tree_numbers(page):
    """the numbers in the tree's boxes and on its branches, by position (x, y of each TEXTOUT_P)"""
    t = {}
    for tx in page.texts:
        t[(tx.x, tx.y)] = tx.text
    return t


def num(sx):
    sx = sx.replace('N = ', '').replace('T+ ', '').replace('T− ', '').replace('D+ ', '').replace('D− ', '')
    sx = sx.replace('match ', '').replace('no ', '').strip()
    if sx.startswith('<'):
        return None
    return float(sx)


def pairs_ok(page, prob=False, tests=1):
    t = tree_numbers(page)
    if prob:
        D, H = num(t[(106, 54)]), num(t[(106, 172)])
        root = 1.0
    else:
        D, H = num(t[(106, 52)]), num(t[(106, 170)])
        root = num(t[(8, 104)])
    TP, FN, FP, TN = (num(t[(216, y)]) for y in (32, 84, 148, 200))
    b1, b2 = num(t[(98, 78)]), num(t[(98, 136)])
    s1, s2, c1, c2 = (num(t[(168, y)]) for y in (34, 74, 152, 192))
    vals = dict(root=root, D=D, H=H, TP=TP, FN=FN, FP=FP, TN=TN)
    z = lambda v: 0.0 if v is None else v
    eq = lambda a, b: abs(a - b) < 1e-9
    ok = (eq(z(D) + z(H), root) and eq(z(TP) + z(FN), z(D)) and eq(z(FP) + z(TN), z(H))
          and eq(z(b1) + z(b2), 1) and eq(z(s1) + z(s2), 1) and eq(z(c1) + z(c2), 1))
    return ok, vals


def exact_counts(p, se, spc, N, t1=None):
    pe, ne = p, N
    if t1:
        tt = pe * t1[0] + (1 - pe) * (1 - t1[1]); ne = ne * tt; pe = pe * t1[0] / tt
    d = ne * pe; hh = ne - d
    return dict(root=ne, D=d, H=hh, TP=d * se, FN=d - d * se, FP=hh * (1 - spc), TN=hh - hh * (1 - spc))


# L1. the emulator's case: D+ 100 at sens 0.835
for prog, label in ((PROG, 'beta 8c'), (BETA8A, 'beta 8a')):
    # 8c: beta 8a with cas='giac' (under harness v3d it stops on a failed CAS call)
    h = run_v(prog, lambda h: (h.choose('Enter values'), h.answer({'pr2': 0.1, 'se2': 0.835, 'sp2': 0.95, 'np2': 1000}),
                               h.press('Esc')), cas=('giac' if prog == BETA8A else 'fail'))
    lv = leaves(trees(h)[-1])
    if prog == PROG:
        check('L1 8b: sens 0.835, D+ 100: T+ 84, T− 16 (84 + 16 = 100); D− 900: T+ 45, T− 855', lv ==
              ['T+ 84', 'T− 16', 'T+ 45', 'T− 855'], str(lv))
    else:
        check('L1 8b: beta 8a shows the emulator\'s T+ 84, T− 17 (101) for the same tree', lv[:2] == ['T+ 84', 'T− 17'],
              str(lv))
# L2. a grid: one test and two, counts; every pair adds up and each box is within 1 of exact
grid = [(p, se, spc, N) for p in (0.1, 0.0125, 0.1235, 0.333, 0.5, 0.987, 0.0001, 0.05)
        for se, spc in ((0.835, 0.95), (0.9, 0.95), (0.8345, 0.9155), (0.999, 0.01), (0.5, 0.5), (0.95, 0.999))
        for N in (1000, 10, 37)]
bad, far, n = [], [], 0
for (p, se, spc, N) in grid:
    h = run_v(PROG, lambda h: (h.choose('Enter values'), h.answer({'pr2': p, 'se2': se, 'sp2': spc, 'np2': N}),
                               h.press('Esc')))
    ok, vals = pairs_ok(trees(h)[-1])
    n += 1
    if not ok:
        bad.append(((p, se, spc, N), vals))
    pp = min(0.999, max(0.0001, p)); ex = exact_counts(pp, se, spc, max(10, int(N)))
    if any(abs(vals[k] - ex[k]) >= 1 for k in vals if vals[k] is not None):
        far.append(((p, se, spc, N), vals, ex))
check('L2 8b: %d trees (priors, sens/spec pairs, N 10, 37, 1000): root = D+ + D−, D+ = TP + FN, D− = FP + TN, '
      'and every branch pair adds to 1' % n, not bad, str(bad[:2]))
check('L2 8b: every count is within one person of its exact value', not far, str(far[:1]))
# two tests (the root is test 1's positives, not a whole number)
bad, n = [], 0
for (p, se, spc) in ((0.1, 0.9, 0.95), (0.01, 0.95, 0.95), (0.1235, 0.835, 0.9155), (0.3, 0.6, 0.7)):
    for (s2, c2) in ((0.9, 0.95), (0.835, 0.95), (0.99, 0.5)):
        h = run_v(PROG, lambda h: (h.choose('Enter values'), h.answer({'pr2': p, 'se2': se, 'sp2': spc, 'np2': 1000}),
                                   h.press('Enter'), h.choose('Second test'), h.answer({'se2': s2, 'sp2': c2}),
                                   h.press('Esc')))
        ok, vals = pairs_ok(trees(h)[-1], tests=2)
        n += 1
        if not ok:
            bad.append(((p, se, spc, s2, c2), vals))
check('L2 8b: %d two-test trees (root = test 1\'s positives): every pair adds up' % n, not bad, str(bad[:2]))
# L3. shares (Leaves): D+ + D− = 1, TP + FN = D+, FP + TN = D−; the "< 0.001" floor is kept
bad, n, floor = [], 0, []
for (p, se, spc) in ((0.1, 0.835, 0.95), (0.1235, 0.8345, 0.9155), (0.0125, 0.9, 0.95), (0.0001, 0.95, 0.95),
                     (0.001, 0.999, 0.999), (0.5, 0.5, 0.5)):
    h = run_v(PROG, lambda h: (h.choose('Enter values'), h.answer({'pr2': p, 'se2': se, 'sp2': spc, 'np2': 1000}),
                               h.press('Enter'), h.choose('Leaves'), h.press('Esc')))
    tr = trees(h)[-1]
    ok, vals = pairs_ok(tr, prob=True)
    n += 1
    if not ok:
        bad.append(((p, se, spc), vals))
    floor += [t.text for t in tr.texts if '< 0.001' in t.text]
check('L3 8b: %d trees in shares: every pair adds up at three decimals' % n, not bad, str(bad[:2]))
check('L3 8b: a share that rounds to 0 still says "< 0.001", not "0.000" (prior 0.0001: TP, FN, D+, the prior branch)',
      len(floor) >= 3, str(floor[:6]))
# L4. node pages and the 2x2 view agree with the boxes
h = run_v(PROG, lambda h: (h.choose('Enter values'), h.answer({'pr2': 0.1, 'se2': 0.835, 'sp2': 0.95, 'np2': 1000}),
                           h.tap(250, 88), h.press('Enter'), h.press('Esc')))
nd = [s for s in h.pages if s.func == 'bt_NodeInfo']
check('L4 8b: the FN box\'s page says "count = 16  (0.016 of N)", as the box', nd and nd[0].has('count = 16  (0.016 of N)'),
      str(nd[0].lines()[:2] if nd else None))
h = run_v(PROG, lambda h: (h.choose('Enter values'), h.answer({'pr2': 0.1, 'se2': 0.835, 'sp2': 0.95, 'np2': 1000}),
                           h.press('Enter'), h.choose('2×2 table view'), h.press('Esc'), h.press('Esc')))
tb = [s for s in h.pages if s.func == 'bt_Tbl2View'][0]
cell = lambda x, y: float([t.text for t in tb.texts if t.x == x and t.y == y][0])
rows = [(cell(78, 60), cell(160, 60), cell(242, 60)), (cell(78, 92), cell(160, 92), cell(242, 92)),
        (cell(78, 124), cell(160, 124), cell(242, 124))]
check('L4 8b: the 2×2 view: 84 + 16 = 100, 45 + 855 = 900, columns 129 + 871 = 1000 (8a: 84 + 17 ≠ 100)',
      rows == [(84, 16, 100), (45, 855, 900), (129, 871, 1000)], str(rows))

# ====================================================================== PART C (8b)
print('\n== C. 8b: the first-level numbers off the branch lines ==')
h = run_v(PROG, lambda h: (h.choose('Close'), h.press('Esc')))
tr = trees(h)[-1]
segs = [sh.args for sh in tr.shapes if sh.cmd == 'LINE_P' and sh.args[0:2] == [84.0, 112.0]]


def hits(seg, box):
    """does segment (x1,y1,x2,y2) pass through box (bx1,by1,bx2,by2)? (sampled every 0.25 px)"""
    x1, y1, x2, y2 = seg[:4]
    for i in range(0, 401):
        u = i / 400.0
        x, y = x1 + u * (x2 - x1), y1 + u * (y2 - y1)
        if box[0] <= x <= box[2] and box[1] <= y <= box[3]:
            return True
    return False


for lbl, y in (('prior', 78), ('1 - prior', 136)):
    t = [tx for tx in tr.texts if tx.x == 98 and tx.y == y]
    box = (t[0].x - 1, t[0].y, t[0].x + t[0].est_width + 1, t[0].y + 10) if t else None
    check('C1 8b: the %s number (%s at x 98, y %d) does not touch either branch line' % (lbl, t[0].text if t else '?', y),
          t and len(segs) == 2 and not any(hits(sg, box) for sg in segs), str(box))
old = [tx for tx in tr.texts if tx.x == 84 and tx.y in (70, 142)]
check('C1 8b: nothing is drawn at the old spots (x 84, y 70 / 142)', not old)
# the old spots were ON the lines (the emulator's "sit on top of the branch lines")
check('C1 8b: (for the record) the old spot x 84, y 70 lay on the upper branch line',
      hits(segs[0] if segs[0][3] < 112 else segs[1], (83, 70, 84 + 28, 80)))
# the tap boxes moved with the numbers: a tap there opens the branch page
for (x, y, want) in ((110, 82, 'Branch: P(D+) = prior'), (110, 140, 'Branch: P(D−) = 1 − prior')):
    h = run_v(PROG, lambda h: (h.choose('Close'), h.tap(x, y), h.press('Enter'), h.press('Esc')))
    nd = [s for s in h.pages if s.func == 'bt_NodeInfo']
    check('C2 8b: a tap on the moved number (%d, %d) opens "%s"' % (x, y, want), nd and nd[0].has(want),
          str(nd[0].lines()[:1] if nd else None))
for t in tr.texts:
    pass
over = [(t.text, t.x, t.y) for t in tr.texts if t.y < 218 and t.y >= 0 and t.x + t.est_width > 318]
check('C3 8b: no tree text runs past x 318', not over, str(over))

# ====================================================================== PART G (8c)
print('\n== G (8c). beta 8c against beta 8b ==')
_c_old = open(BETA8B, encoding='utf-8').read()
_c_new = open(PROG, encoding='utf-8').read()
_C0, _C1 = _bodies(_c_old), _bodies(_c_new)
_cdiff = sorted(n for n in set(_C0) | set(_C1) if _C0.get(n) != _C1.get(n))
_cwant = ['BayesTree', 'bt_Cas', 'bt_Crumb', 'bt_DiagView', 'bt_ExactView', 'bt_FaganView', 'bt_HelpView',
          'bt_NumS', 'bt_Pct', 'bt_PrevView', 'bt_Rep', 'bt_RocView', 'bt_Strip', 'bt_fmtq']
check('G 8c: routines that differ from beta 8b: %s' % _cdiff, _cdiff == _cwant, 'want %s' % _cwant)
check('G 8c: bt_Crumb is the one new routine; bt_WaitAny (it still appends its tap) is byte-identical',
      'bt_Crumb' not in _C0 and _C0['bt_WaitAny'] == _C1['bt_WaitAny'])
_cline = 'LOCAL btQueuedMs := 100;'
check('G 8c: outside those routines the one new line is the threshold, "%s"; everything else is comments'
      % _cline, _outside(_c_new, _cdiff).count(_cline) == 1
      and _outside(_c_old, _cdiff) == _outside(_c_new, _cdiff).replace(_cline + ' ', ''))
_k0 = _re.sub(r'//[^\n]*', '', _C0['bt_Cas']); _k1 = _re.sub(r'//[^\n]*', '', _C1['bt_Cas'])
check('G 8c: bt_Cas keeps its IFERR call line and its quote strip byte-identical (only the INSTRING guard is new)',
      'cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + bt_S + ")" + CHAR(34) + ")"));' in _k1
      and 'IF LEFT(cR, 1) == CHAR(34) AND MID(cR, DIM(cR), 1) == CHAR(34) THEN' in _k1
      and _k0.replace('  IF INSTRING', '    IF INSTRING') != _k0)
_code = _re.sub(r'"[^"\n]*"', '""', _re.sub(r'//[^\n]*', '', _c_new))
check('G 8c: the stale test reads the threshold by name, and the threshold is set in ONE place',
      _code.count('btQueuedMs') == 2 and 'IF btEvT == 3 AND btWT <= btQueuedMs THEN' in _c_new
      and _c_new.count('btWT := TICKS;') == 1 and _c_new.count('btWT := TICKS - btWT;') == 1)
check('G 8c: the type-3 soft-key logic the emulator confirmed is unchanged (slot MIN(6, IP(x/53.4)+1) on a '
      'non-stale type 3 at y >= 218)',
      'IF btEvT == 3 AND btMY >= 218 THEN' in _c_new and 'btNode := MIN(6, IP(btMX/53.4) + 1);' in _c_new
      and _c_new.count('IF btStale == 0 THEN') == 1)

# ====================================================================== PART R (8c)
print('\n== R. 8c: the second emulator round ==')


class Timed(Harness):
    """Harness v3d plus what it does not model, for part R (17 Oct 2026, round 2):
      gap_ms  a fresh event the student makes (WAIT(-1) takes it from the script's queue) comes
              gap_ms after WAIT(-1) was called -- a person, not the queue.  What is ALREADY QUEUED
              (_pending_wait: a lift, a click, mouse_tail's tail) comes back at once, the clock not
              moved.  gap_ms = 0 is plain v3d, whose clock moves only 1 ms per TICKS reading.
      strip3  a tap at y >= 218 reaches WAIT(-1) ONLY as {3, x, y} on every screen, soft keys drawn
              or not (round 2: the PPV, ROC and Fagan footers).
      char_w  TEXTOUT_P at font 1 returns x + the width of its text in this model (a function of one
              character); v3d's own estimate is 5.5 px per character."""

    def __init__(self, *a, **k):
        self.gap_ms = k.pop('gap_ms', 0)
        self.strip3 = k.pop('strip3', False)
        self.char_w = k.pop('char_w', None)
        Harness.__init__(self, *a, **k)

    def _wait(self, a):
        n = a[0] if a else None
        if n is not None and n < 0 and self._stale is None and not self._pending_wait and self._queue:
            self.clock += self.gap_ms
        return Harness._wait(self, a)

    def _menu_shown(self):
        return True if self.strip3 else Harness._menu_shown(self)

    def _textout(self, a, cmd):
        r = Harness._textout(self, a, cmd)
        t = self.texts[-1]
        if self.char_w is not None and int(t.font or 0) == 1:
            return float(t.x or 0) + sum(self.char_w(c) for c in t.text)
        return r


def run_t(prog, script, cas='fail', **kw):
    h = Timed(prog, strict=True, cas=cas, **kw)
    script(h)
    h.call('BayesTree')
    return h


def opens(h, f):
    """how many times view f was opened (its first frame after some other screen)"""
    n, prev = 0, None
    for s in h.pages:
        if s.func == f and prev != f:
            n += 1
        prev = s.func
    return n


GAP = 400        # ms between the student's taps (a quick but human pace); anything over 100 works
ROCX = slot_x(3)


def two_by_two_then_roc(roc_taps):
    def sc(h):
        h.choose('Close')
        h.tap(slot_x(5), 230)        # soft key 2x2 (a click): the 2x2 view, held by bt_WaitAny (MOUSE)
        h.tap(ROCX, 226)             # close it on its footer, at the ROC key's spot (read by MOUSE)
        for _ in range(roc_taps):
            h.tap(ROCX, 226)         # then the ROC key at that same spot
        h.press('Esc'); h.press('Esc')
    return sc


# R1. the stale spot, both ways
h = run_t(BETA8B, two_by_two_then_roc(1), gap_ms=GAP, cas='giac')
check('R1 8c: beta 8b, the emulator\'s case: 2x2 closed on its footer at the ROC key, then ROC once -> '
      'NOTHING (the tap is eaten by the stale list)', 'bt_Tbl2View' in funcs(h) and opens(h, 'bt_RocView') == 0
      and h.error is None, str(sorted(set(funcs(h)))))
h = run_t(BETA8B, two_by_two_then_roc(2), gap_ms=GAP, cas='giac')
check('R1 8c: beta 8b: ... a second ROC tap works (the emulator: "the first tap is ignored, the second works")',
      opens(h, 'bt_RocView') == 1, str(sorted(set(funcs(h)))))
h = run_t(PROG, two_by_two_then_roc(1), gap_ms=GAP)
check('R1 8c: beta 8c: the same taps -- ROC opens on the FIRST tap (a real, later tap at the spot counts)',
      opens(h, 'bt_RocView') == 1 and h.error is None and not h.inputs, str(sorted(set(funcs(h)))))
for k, nm in ((1, 'Values'), (4, 'PPV'), (6, 'More')):
    def sc(h, k=k):
        h.choose('Close'); h.tap(slot_x(5), 230); h.tap(slot_x(k), 226); h.tap(slot_x(k), 226)
        h.answer(CANCEL); h.press('Esc'); h.press('Esc'); h.press('Esc')
    h = run_t(PROG, sc, gap_ms=GAP)
    got = {1: 'Exact Values' in inputs(h), 4: opens(h, 'bt_PrevView') == 1,
           6: any(s.menu and s.menu[0] == 'Diag' for s in h.screens)}[k]
    check('R1 8c: the same at the %s key\'s spot: the 2x2 view closes there, the next tap there runs %s' % (nm, nm),
          got and h.error is None, '%s %s' % (sorted(set(funcs(h))), inputs(h)))
# the click that really IS queued: harness mouse_tail=True leaves the MOUSE-read tap's {2}, {3, x, y} for
# the next WAIT(-1) -- with the clock NOT moved (plain v3d), and with the student's own taps taking time
for gap, lbl in ((0, 'a clock that has not moved (plain v3d)'), (GAP, 'the student\'s taps %d ms apart' % GAP)):
    h = run_t(PROG, two_by_two_then_roc(0), gap_ms=gap, mouse_tail=True)
    other = [f for f in funcs(h) if f not in ('BayesTree', 'bt_Tbl2View')]
    check('R1 8c: a click ALREADY QUEUED at the ROC spot (mouse_tail, %s) is still skipped: no ROC' % lbl,
          not other and h.error is None and 'bt_Tbl2View' in funcs(h), str(sorted(set(funcs(h)))))
h = run_t(PROG, two_by_two_then_roc(1), gap_ms=GAP, mouse_tail=True)
check('R1 8c: ... and the real ROC tap after that queued click still counts: ROC opens once',
      opens(h, 'bt_RocView') == 1 and h.error is None, str(sorted(set(funcs(h)))))
noq = os.path.join(SCR, 'BayesTree_beta8c_noqueue.txt')
open(noq, 'w', encoding='utf-8').write(srcP.replace('IF btEvT == 3 AND btWT <= btQueuedMs THEN', 'IF 0 THEN'))
h = run_t(noq, two_by_two_then_roc(0), gap_ms=0, mouse_tail=True)
check('R1 8c: (with the stale test patched out, that queued click WOULD run ROC -- so the skip is real)',
      opens(h, 'bt_RocView') == 1, str(sorted(set(funcs(h)))))
# the same skip at its other sources, with time passing: a view closed by a type-0 tap outside its plot
# (its {2}, {3} reach the tree), the tree's own press, a node page in the worst case
h = run_t(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(4), 230), h.tap(150, 205), h.press('Esc'), h.press('Esc')),
          gap_ms=GAP)
check('R1 8c: PPV closed by a tap outside its plot (150, 205): its queued {2}, {3} run nothing on the tree',
      [f for f in funcs(h) if f not in ('BayesTree', 'bt_PrevView')] == [] and len(h.leftover()[0]) == 1,
      str(sorted(set(funcs(h)))))
h = run_t(PROG, lambda h: (h.choose('Close'), h.tap(40, 110), h.press('Enter'), h.press('Esc')), gap_ms=GAP)
nodes = [s for s in h.pages if s.func == 'bt_NodeInfo']
check('R1 8c: with time passing, a tap on the root box still opens its page once', len(nodes) == 1, '%d' % len(nodes))
h = run_t(PROG, lambda h: (h.choose('Close'), h.tap(40, 110), h.tap(150, 226), h.press('Esc')), gap_ms=GAP,
          mouse_tail=True)
check('R1 8c: mouse_tail with time passing: a node page closed on its footer leaves its click, which is skipped',
      [f for f in funcs(h) if f not in ('BayesTree', 'bt_NodeInfo')] == [] and h.error is None,
      str(sorted(set(funcs(h)))))

# R2. the views close on a footer tap that is ONLY {3, x, y}
for k, view, fx in ((4, 'bt_PrevView', 150), (3, 'bt_RocView', 100), (None, 'bt_FaganView', 230)):
    def sc(h, k=k, fx=fx):
        if k is None:
            h.choose('Fagan nomogram')
        else:
            h.choose('Close'); h.tap(slot_x(k), 230)
        h.tap(fx, 226)               # the view's footer: on the emulator ONLY {3, fx, 226}
        h.press('Esc'); h.press('Esc')
    h = run_t(PROG, sc, gap_ms=GAP, strip3=True)
    other = [f for f in funcs(h) if f not in ('BayesTree', view)]
    check('R2 8c: %s closes on a footer tap that arrives only as {3, %d, 226}; back on the tree, nothing else '
          'opens' % (view, fx), view in funcs(h) and not other and not h.inputs and h.error is None
          and len(h.leftover()[0]) == 1, '%s left over %d' % (sorted(set(funcs(h))), len(h.leftover()[0])))
    h = run_t(BETA8B, sc, gap_ms=GAP, strip3=True, cas='giac')
    check('R2 8c: (beta 8b in the same model: the footer tap does nothing, Esc has to close %s -- round 2\'s '
          'finding)' % view, len(h.leftover()[0]) == 0 and h.error is None, 'left over %d' % len(h.leftover()[0]))
h = run_t(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(3), 230), h.tap(slot_x(4), 226), h.tap(slot_x(4), 230),
                           h.press('Esc'), h.press('Esc')), gap_ms=GAP, strip3=True)
check('R2 8c: ROC closed by a footer tap at the PPV key\'s spot, then PPV tapped: PPV opens (no stale entry)',
      opens(h, 'bt_RocView') == 1 and opens(h, 'bt_PrevView') == 1, str(funcs(h)))
for view, script in (('bt_PrevView', lambda h: (h.choose('Close'), h.tap(slot_x(4), 230), h.tap(300, 205))),
                     ('bt_RocView', lambda h: (h.choose('Close'), h.tap(slot_x(3), 230), h.tap(300, 205))),
                     ('bt_FaganView', lambda h: (h.choose('Fagan nomogram'), h.tap(200, 100)))):
    h = run_t(PROG, lambda h, s=script: (s(h), h.press('Esc'), h.press('Esc')), gap_ms=GAP, strip3=True)
    check('R2 8c: %s: a type-0 tap outside the plot still means back (kept as it was)' % view,
          len(h.leftover()[0]) == 1 and [f for f in funcs(h) if f not in ('BayesTree', view)] == [],
          str(sorted(set(funcs(h)))))
h = run_t(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(4), 230), h.drag([(100, 100), (150, 100), (200, 100)]),
                           h.press('Esc'), h.press('Esc')), gap_ms=GAP, strip3=True)
pvf = [s for s in h.pages if s.func == 'bt_PrevView']
check('R2 8c: a drag inside the PPV plot still moves the prior (several frames) and does not close the view',
      len(pvf) >= 3 and len(h.leftover()[0]) == 0, '%d frames' % len(pvf))


# R3. the two-test breadcrumb from measured widths
def w65(c):
    return 6.5                                  # the brief's model: ~6.5 px per character at font 1


def w65arrow11(c):
    return 11.0 if c == chr(8594) else 6.5      # a stress model: a wide arrow glyph


def crumb(page):
    """the breadcrumb's pieces as drawn last (after the last paint-over), as (text, x)"""
    items = page.items
    cut = 0
    for i, it in enumerate(items):
        if getattr(it, 'cmd', None) == 'RECT_P' and list(it.args[:4]) == [0.0, 0.0, 103.0, 22.0]:
            cut = i + 1
    return [(it.text, it.x) for it in items[cut:] if hasattr(it, 'text') and it.y == 6 and it.x < 104]


def crumb_ok(pcs, cw):
    """five pieces, number / arrow / number / arrow / number, each starting at least 2 px after the
    one before ends (in the width model cw), the last one ending at x <= 102"""
    if len(pcs) != 5 or pcs[1][0] != chr(8594) or pcs[3][0] != chr(8594):
        return False, 0
    end = None
    for t, x in pcs:
        if end is not None and x < end + 2 - 1e-9:
            return False, end
        end = x + sum(cw(c) for c in t)
    return end <= 102 + 1e-9, end


def two_test(p, s1, c1, s2, c2):
    return lambda h: (h.choose('Enter values'), h.answer({'pr2': p, 'se2': s1, 'sp2': c1, 'np2': 1000}),
                      h.press('Enter'), h.choose('Second test'), h.answer({'se2': s2, 'sp2': c2}), h.press('Esc'))


EMU = (0.041, 0.835, 0.95, 0.835, 0.95)          # round 2's tree: "0.04 -0.42 -0.92"
h = run_t(PROG, two_test(*EMU), char_w=w65)
pcs = crumb(trees(h)[-1])
ok, end = crumb_ok(pcs, w65)
check('R3 8c: the emulator\'s tree (prior 0.041, 0.835 / 0.95 twice), 6.5 px per character: %s, no overlap, '
      'ends at x %.1f <= 102' % (' '.join(t for t, x in pcs), end), ok, str(pcs))
h = run_t(PROG, two_test(*EMU))
pcs5 = crumb(trees(h)[-1])
ok5, end5 = crumb_ok(pcs5, lambda c: 5.5)
check('R3 8c: the same tree in v3d\'s own 5.5 px model keeps the leading zeros: %s (ends at x %.1f)'
      % (' '.join(t for t, x in pcs5), end5), ok5 and pcs5[0][0] == '0.04', str(pcs5))
h = run_t(PROG, two_test(*EMU), char_w=w65arrow11)
pcsA = crumb(trees(h)[-1])
okA, endA = crumb_ok(pcsA, w65arrow11)
check('R3 8c: the same tree with an 11-px arrow (stress): %s, no overlap, ends at x %.1f'
      % (' '.join(t for t, x in pcsA), endA), okA, str(pcsA))
# beta 8b's fixed layout in the stress model: the arrow at +29 runs into the number at +36
h = run_t(BETA8B, two_test(*EMU), cas='giac')
p8b = [(t.text, t.x) for t in trees(h)[-1].texts if t.y == 6 and t.x < 104]
ov = [(p8b[i][0], p8b[i + 1][0]) for i in range(len(p8b) - 1)
      if p8b[i][1] + sum(w65arrow11(c) for c in p8b[i][0]) > p8b[i + 1][1]]
check('R3 8c: (beta 8b, fixed at x 2 / 31 / 38 / 67 / 74: with an 11-px arrow each arrow runs into the next number, '
      'the emulator\'s "0.04 -0.42 -0.92")', len(ov) >= 2, str(ov))
grid = [(p, a, b) for p in (0.0001, 0.001, 0.005, 0.02, 0.041, 0.1, 0.3, 0.5, 0.8, 0.95, 0.99, 0.999)
        for a, b in (((0.835, 0.95), (0.835, 0.95)), ((0.9, 0.95), (0.9, 0.95)), ((0.999, 0.999), (0.999, 0.999)),
                     ((0.5, 0.5), (0.6, 0.7)), ((0.99, 0.6), (0.95, 0.999)), ((0.3, 0.9), (0.999, 0.01)))]
bad, tiers, over11 = [], {}, []
for p, a, b in grid:
    h = run_t(PROG, two_test(p, a[0], a[1], b[0], b[1]), char_w=w65)
    pcs = crumb(trees(h)[-1])
    ok, end = crumb_ok(pcs, w65)
    if not ok or h.error is not None:
        bad.append(((p, a, b), pcs, end))
    # the form used = how many times the first try was painted over (0, 1 or 2)
    tier = sum(1 for it in trees(h)[-1].items
               if getattr(it, 'cmd', None) == 'RECT_P' and list(it.args[:4]) == [0.0, 0.0, 103.0, 22.0])
    tiers[tier] = tiers.get(tier, 0) + 1
    h = run_t(PROG, two_test(p, a[0], a[1], b[0], b[1]), char_w=w65arrow11)
    pcs = crumb(trees(h)[-1])
    ok, end = crumb_ok(pcs, w65arrow11)
    if not ok:
        over11.append(((p, a, b), ' '.join(t for t, x in pcs), round(end, 1)))
check('R3 8c: %d two-test trees (12 priors x 6 test pairs, the extremes included), 6.5 px per character: every '
      'crumb is 5 pieces, none overlaps the one before, all end left of x 102' % len(grid), not bad, str(bad[:2]))
print('     forms used (6.5 px model; 0 = bt_fmtB as is, 1 = no leading zero, 2 = two decimals): %s' % tiers)
print('     with an 11-px arrow (stress): %d of %d still fit; those that do not: %s'
      % (len(grid) - len(over11), len(grid), over11[:4]))
check('R3 8c: with an 11-px arrow nothing ever overlaps either (the layout follows the measured widths)',
      all(isinstance(o[2], float) for o in over11))
# should TEXTOUT_P ever hand back no position past its start (its return value is cited from the corpus,
# not seen on our calculators), bt_Crumb assumes 7 px a character and 10 px for the arrow
h = run_t(PROG, two_test(*EMU), char_w=lambda c: 0.0)
pcsZ = crumb(trees(h)[-1])
okZ, endZ = crumb_ok(pcsZ, lambda c: 10.0 if c == chr(8594) else 7.0)
check('R3 8c: if TEXTOUT_P handed back no position past its start, the crumb is laid out at 7 px a character '
      '(10 for the arrow): %s, ends at x %.1f' % (' '.join(t for t, x in pcsZ), endZ), okZ and h.error is None,
      str(pcsZ))

# R4. the Exact page with two tests
for forensic in (False, True):
    def sc(h, forensic=forensic):
        h.choose('Enter values'); h.answer({'pr2': EMU[0], 'se2': EMU[1], 'sp2': EMU[2], 'np2': 1000})
        h.press('Enter'); h.choose('Second test'); h.answer({'se2': EMU[3], 'sp2': EMU[4]})
        if forensic:
            h.press('Enter'); h.choose('Forensic')
        h.press('Enter'); h.choose('Exact answers'); h.press('Enter'); h.press('Enter'); h.press('Esc')
    h = run_t(PROG, sc, cas='giac')
    pg = [s for s in h.pages if s.func == 'bt_PageL']
    p1 = pg[0] if pg else None
    lines = [t for t in p1.texts if 24 <= t.y <= 216] if p1 else []
    wide = [(t.text, round(t.x + t.est_width)) for s in pg for t in s.texts if t.x + t.est_width > 318]
    if not forensic:
        check('R4 8c: two tests, Exact page 1: "then test 2: TP = 28586225, FP = 2397500," and '
              '"  FN = 5648775, TN = 45552500" on two lines', p1 is not None
              and p1.has('then test 2: TP = 28586225, FP = 2397500,') and p1.has('  FN = 5648775, TN = 45552500'),
              str(p1.lines()[:4] if p1 else None))
    check('R4 8c: two tests%s: every Exact-page line inside x 318, at most 15 lines, the last at y <= 206 (above the '
          'footer at 226)' % (', forensic' if forensic else ''),
          p1 is not None and not wide and len(lines) <= 15 and max(t.y for t in lines) <= 206,
          '%d lines, last y %s, wide %s' % (len(lines), max(t.y for t in lines) if lines else None, wide))
h = run_t(BETA8B, lambda h: (h.choose('Enter values'), h.answer({'pr2': EMU[0], 'se2': EMU[1], 'sp2': EMU[2], 'np2': 1000}),
                             h.press('Enter'), h.choose('Second test'), h.answer({'se2': EMU[3], 'sp2': EMU[4]}),
                             h.press('Enter'), h.choose('Exact answers'), h.press('Esc'), h.press('Esc')), cas='giac')
pg = [s for s in h.pages if s.func == 'bt_PageL']
lng = [t for t in pg[0].texts if t.text.startswith('then test 2')] if pg else []
check('R4 8c: (beta 8b: that line was %d characters, to x %d -- off the 320-px screen)'
      % (len(lng[0].text) if lng else 0, round(lng[0].x + lng[0].est_width) if lng else 0),
      lng and lng[0].x + lng[0].est_width > 320)

# R5. Diagnostics wording; R6. the soft-key label
h = run_t(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(6), 230), h.tap(slot_x(1), 230), h.press('Enter'),
                           h.press('Esc')))
dg = [s for s in h.pages if s.func == 'bt_DiagView']
want = 'For p-values / CIs on real data: EpiStats 2×2.'
tx = [t for t in dg[0].texts if t.text == want] if dg else []
check('R5 8c: Diagnostics says "%s" (inside x 318), and ConTable2 is named nowhere in the program\'s text' % want,
      tx and tx[0].x + tx[0].est_width <= 318 and 'ConTable2' not in _re.sub(r'//[^\n]*', '', srcP),
      str([t.text for t in dg[0].texts][-4:] if dg else None))
h = run_t(PROG, lambda h: (h.choose('Close'), h.tap(slot_x(6), 230), h.tap(slot_x(6), 230), h.press('Esc')))
labels = [list(s.menu) for s in h.screens if s.menu]
p3 = [m for m in labels if m[0] == 'Test 2']
check('R6 8c: soft-key page 3 reads %s; every label of the three pages has at most 6 characters'
      % (p3[0] if p3 else None), p3 and p3[0][2] == 'Forens'
      and all(len(x) <= 6 for m in labels for x in m), str(sorted({x for m in labels for x in m}, key=len)[-3:]))

# R7. INSTRING never sees ""
hh = Harness(PROG, cas='fail')
cases = [('abcbtq', 'btq', 'p', 'abcp'), ('btqabc', 'btq', 'p', 'pabc'), ('btq', 'btq', 'p', 'p'),
         ('abc', '', 'p', 'abc'), ('', 'btq', 'p', ''), ('btq*btq', 'btq', 'p', 'p*p'), ('a*b*', '*', '×', 'a×b×'),
         ('(-btc+1)/(-btc+bts+1)', 'btc', 'sp', '(-sp+1)/(-sp+bts+1)'), ('xyz', 'btq', 'p', 'xyz')]
got = [(s_, a_, hh.call('bt_Rep', s_, a_, b_), w_) for s_, a_, b_, w_ in cases]
check('R7 8c: bt_Rep: a pattern at the end, at the start, the whole text, an empty pattern, an empty text, '
      'twice, none -- all right, no error', all(g == w for s_, a_, g, w in got), str([g for g in got if g[2] != g[3]]))
old = Harness(BETA8B, cas='fail')
errs = []
for s_ in ('abcbtq', ''):
    try:
        old.call('bt_Rep', s_, 'btq', 'p')
        errs.append(None)
    except Exception as e:
        errs.append(str(e)[:40])
check('R7 8c: (beta 8b\'s bt_Rep STOPS on a pattern at the end and on an empty text: %s)' % errs,
      all(e and 'INSTRING' in e for e in errs))
st = [hh.call('bt_Strip', x) for x in ('', '{1/20}', 'list[1/20]', '[ ]')]
check('R7 8c: bt_Strip("") = "", "{1/20}" -> 1/20, "list[1/20]" -> 1/20, "[ ]" -> "" (no error)',
      st == ['', '1/20', '1/20', ''], str(st))
check('R7 8c: bt_Cas with the CAS failing returns "" without an error', hh.call('bt_Cas', '1/3') == '')
hg = Harness(PROG, cas='giac')
check('R7 8c: bt_Cas still answers (1/3 -> "1/3") and refuses an infinity (1/0 -> "")',
      hg.call('bt_Cas', '1/3') == '1/3' and hg.call('bt_Cas', '1/0') == '', str(hg.cas_calls[-2:]))
scripts = {
    'one test': ex_script,
    'two tests': lambda h: (h.choose('Second test'), h.answer({'se2': 0.9, 'sp2': 0.95}), h.press('Enter'),
                            h.choose('Exact answers'), h.press('Enter'), h.press('Enter'), h.press('Esc')),
    'forensic': lambda h: (h.choose('Forensic'), h.press('Enter'), h.choose('Exact answers'), h.press('Enter'),
                           h.press('Enter'), h.press('Esc')),
    'forensic, two tests, soft key Exact': lambda h: (h.choose('Forensic'), h.press('Enter'), h.choose('Second test'),
                                                      h.answer({'se2': 0.835, 'sp2': 0.95}), h.press('Enter'),
                                                      h.choose('Close'), h.tap(slot_x(6), 230), h.tap(slot_x(6), 230),
                                                      h.tap(slot_x(5), 230), h.press('Enter'), h.press('Esc'),
                                                      h.press('Esc'))}
for nm, sc in scripts.items():
    h = run(sc, cas='fail')
    pg = [s for s in h.pages if s.func == 'bt_PageL']
    tr = trees(h)[-1]
    check('R7 8c: cas=fail end to end (%s): the tree badge "decimal, tap", both Exact pages "decimal", no error'
          % nm, h.error is None and h.result.startswith('BayesTree:') and 'decimal, tap' in panel(tr)
          and len(pg) == 2 and all(p.has('decimal') for p in pg), '%s %s' % (panel(tr)[:3], len(pg)))
    try:
        ho = run(sc, cas='fail', prog=BETA8B)
        eo = ho.error
    except Exception as e:
        eo = e
    check('R7 8c: (beta 8b on the same run STOPS: %s)' % str(eo)[:60], eo is not None and 'INSTRING' in str(eo))

# R8 (and the sweep). small numbers through STRING(x, 2, d)
for fn, args, want in (('bt_NumS', (1 - 0.9,), '0.1'), ('bt_NumS', (1 - 0.99,), '0.01'),
                       ('bt_Pct', (1 / (1 + 999 * 999),), '0.000 %'), ('bt_Pct', (0.00308,), '0.31 %'),
                       ('bt_fmtq', (0.005 - 0.004, 0.001), '0.001'), ('bt_fmtq', (0.1 - 0.099, 0.001), '0.001'),
                       ('bt_fmtq', (0.0, 0.0002), '< 0.001')):
    hh = Harness(PROG, cas='fail')
    g = hh.call(fn, *args)
    hold = Harness(BETA8B, cas='fail')
    go = hold.call(fn, *args)
    check('R8 8c: %s%s = "%s" (beta 8b: "%s")' % (fn, tuple(round(a, 12) for a in args), g, go),
          g == want and not hh.sci_strings, str(hh.sci_strings))
mine = [h for h in ALL_H if any(os.path.abspath(f) == PROG for f in h.files)]
sci = sorted({(round(v, 12), d, r) for h in mine for (v, d, r) in h.sci_strings})
print('     harness runs of beta 8c in this script: %d; scientific STRING results: %s' % (len(mine), sci or 'none'))
check('R8 8c: no STRING(x, 2, d) of beta 8c printed in scientific form in any of the %d runs' % len(mine), not sci,
      str(sci[:6]))
olds = sorted({(round(v, 12), d, r) for h in ALL_H if any(os.path.abspath(f) == BETA8B for f in h.files)
               for (v, d, r) in h.sci_strings})
print('     (beta 8b in the same script: %s)' % (olds or 'none'))

print('\n%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
sys.exit(1 if FAIL else 0)
