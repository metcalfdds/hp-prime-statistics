# -*- coding: utf-8 -*-
"""verify_SampDist_v2.3b.py -- checks SampDist v2.3b (19 Oct 2026): S1 (critical-value mode clamps alpha at 1E-7,
not 1E-6, so the floor reads "< 0.000001") and S2 (sd_fix's right tail as the lower tail at 2mu - a), from the fleet
review of 19 Oct 2026 (findings_B).  Built from verify_SampDist_v2.3a.py: parts A-I run on v2.3b with only the file
names changed (absolute paths to /home/claude/work/out for the earlier versions and the harnesses, so the script runs
from any folder); part I's code diff (I5) stays v2.3a's change set (v2.3 -> v2.3a).  Part J is new: S1 and S2 before
and after, through the live graph and sd_fix, in doubles and under the review's twelve_digits(); the review's
check_SampDist.py on both versions (its bug demonstrations turned round); the routine diff v2.3a -> v2.3b; the
static rules; scientific fixed decimals.

    python3 verify_SampDist_v2.3b.py

(verify_SampDist_v2.3a.py's docstring follows.)

verify_SampDist_v2.3a.py -- checks SampDist v2.3a (17 Oct 2026, evening): no "=" before a relation (sd_Eq) and
the right tail as the lower tail NORMALD_CDF(mu, se, 2mu - a).  Parts A-H are verify_SampDist_v2.3.py, run on
v2.3a with only the file name changed (ppl_harness_v1; v2.2 still the comparison where they compare).  Part I is
new (harness v3e): the panel before and after for each tail; the exported EP_SD_P and sd_prob against SciPy; a
sweep of 108 panels identical to v2.3 once its "= <" and right-tail zeros are written the v2.3a way; sd_Eq; the
code-line diff; names; version strings; comments; no new scientific fixed decimals.

    python3 verify_SampDist_v2.3a.py

(verify_SampDist_v2.3.py's docstring follows.)

verify_SampDist_v2.3.py -- runs SampDist v2.3 (and v2.2 for comparison) in
hp-prime-kit's interpreter through ppl_harness_v1, with scripted menu answers,
form values, soft-key taps, drags and keys, and checks every number against
SciPy.  16 Oct 2026.

    python3 verify_SampDist_v2.3.py
"""
from __future__ import print_function
import sys, os, math, random, itertools
HERE = '/home/claude/work/out'          # v2.3b: the earlier versions and the harnesses, by absolute path
sys.path.insert(0, HERE)
from ppl_harness_v1 import Harness
from scipy.stats import norm

NEW = '/home/claude/work/fix19/SampDist_v2.3b.txt'
V23A = os.path.join(HERE, 'SampDist_v2.3a.txt')   # v2.3b
OLD = os.path.join(HERE, 'SampDist_v2.2.txt')
EP = ['EP_SD_SE', 'EP_SD_P', 'EP_SD_ZLO', 'EP_SD_ZHI', 'EP_SD_LO', 'EP_SD_HI']
fails = []
checks = [0]


def ok(cond, msg):
    checks[0] += 1
    if not cond:
        fails.append(msg)
        print('FAIL', msg)


def close(a, b, tol=1e-12):
    return abs(a - b) <= tol * max(1.0, abs(b))


def eps(h):
    return [h.g(k) for k in EP]


def soft(slot):                  # a tap in soft-key slot 1..6
    return ('tap', int((slot - 0.5) * 53.4), 230)


def sp_prob(mu, se, lo, hi, t):
    if t == 1: return norm.cdf(lo, mu, se)
    if t == 2: return 1 - norm.cdf(lo, mu, se)
    if t == 3: return norm.cdf(hi, mu, se) - norm.cdf(lo, mu, se)
    return norm.cdf(lo, mu, se) + 1 - norm.cdf(hi, mu, se)


# ---------------------------------------------------------------- A. numbers
print('A. Find probability / Find critical value: v2.3 against v2.2 and SciPy')
cases = [(0, 1, 30), (100, 15, 30), (100, 15, 1), (-12.5, 4.2, 7), (500, 100, 400)]
nA = 0
for mu, sg, n in cases:
    se = sg / math.sqrt(n)
    for t in (1, 2, 3, 4):
        a, b = mu - 1.3 * se, mu + 0.7 * se
        bounds = [a] if t <= 2 else [b, a]          # two-bound form typed reversed
        res = []
        for path in (OLD, NEW):
            h = Harness(path)
            h.run('SampDist()', events=[('key', 4)], chooses=[1, t, 0],
                  inputs=[[mu, sg, n], bounds])
            res.append(eps(h))
        lo, hi = (a, a) if t <= 2 else (a, b)
        ok(all(close(x, y) for x, y in zip(res[0], res[1])),
           'prob mu=%g sg=%g n=%g t=%d: v2.3 %r != v2.2 %r' % (mu, sg, n, t, res[1], res[0]))
        ok(close(res[1][1], sp_prob(mu, se, lo, hi, t), 1e-12),
           'prob vs scipy %r' % ((mu, sg, n, t),))
        nA += 1
    for t in (1, 2, 3):
        for alp in (0.05, 0.01, 0.2):
            res = []
            for path in (OLD, NEW):
                h = Harness(path)
                h.run('SampDist()', events=[('key', 4)], chooses=[2, t, 0],
                      inputs=[[mu, sg, n, alp]])
                res.append(eps(h))
            ok(all(close(x, y, 1e-12) for x, y in zip(res[0], res[1])),
               'crit mu=%g n=%g t=%d a=%g: %r vs %r' % (mu, n, t, alp, res[1], res[0]))
            if t == 1: lo = norm.ppf(alp, mu, se)
            if t == 2: lo = norm.ppf(1 - alp, mu, se)
            if t == 3: lo = norm.ppf(alp / 2, mu, se)
            ok(close(res[1][4], lo, 1e-12), 'crit lo vs scipy %r' % ((mu, n, t, alp),))
            nA += 1
print('   %d cases run through both files' % nA)

# ---------------------------------------------------------------- B. soft keys
print('B. Soft keys n-, n+, nx4, Tail on the probability graph')
mu, sg, n, a = 100.0, 15.0, 30.0, 95.0
h = Harness(NEW)
seq = [soft(3), soft(2), soft(1), soft(1), soft(5), soft(5), soft(5), soft(5), ('key', 4)]
h.run('SampDist()', events=seq, chooses=[1, 1, 0], inputs=[[mu, sg, n], [a]])
# frame 0 = entry; then one frame per action
expect_n = [30, 120, 160, 100, 64, 64, 64, 64, 64]
expect_t = [1, 1, 1, 1, 1, 2, 3, 4, 1]
for i, f in enumerate(h.frames):
    hdr = [t['s'] for t in f['text'] if t['y'] == 4.0][0]
    ok(('n = %d' % expect_n[i]) in hdr, 'frame %d header %r' % (i, hdr))
    p1 = [t['s'] for t in f['text'] if t['y'] == 169.0][0]
    se = sg / math.sqrt(expect_n[i])
    t = expect_t[i]
    lo, hi = (a, a) if t <= 2 else ((95.0, 105.0))
    pv = sp_prob(mu, se, lo, hi, t)
    shown = p1.split('= ')[-1]
    want = ('%.6f' % pv) if pv >= 1e-6 else '< 0.000001'
    ok(shown == want, 'frame %d P shown %r want %r (n=%d t=%d)' % (i, shown, want, expect_n[i], t))
    ok(f['menu'] == [u'n−', 'n+', u'n×4', u'μ,σ', 'Tail', 'Menu'],
       'soft keys %r' % f['menu'])
ok(close(h.g('EP_SD_SE'), 15 / 8.0), 'EP_SD_SE after the run')

# the ladder at its ends, and nx4's cap
for n0, slot, n1 in [(1, 1, 1), (37, 2, 40), (37, 1, 30), (400, 2, 400), (1000, 1, 400),
                     (400, 3, 1600), (1600, 3, 1600), (3, 3, 12)]:
    h = Harness(NEW)
    h.run('SampDist()', events=[soft(slot), ('key', 4)], chooses=[1, 1, 0],
          inputs=[[0, 1, n0], [-0.1]])
    hdr = [t['s'] for t in h.frames[-1]['text'] if t['y'] == 4.0][0]
    ok(('n = %d' % n1) in hdr, 'ladder from %d slot %d: %r' % (n0, slot, hdr))
    note = [t['s'] for t in h.frames[-1]['text'] if t['y'] == 202.0][0]
    if n0 == n1:
        ok('drag or' not in note, 'a refused step should say why: %r' % note)
    ok(close(h.g('EP_SD_P'), norm.cdf(-0.1, 0, 1 / math.sqrt(n1)), 1e-12), 'P after ladder')

# ---------------------------------------------------------------- C. drag + keys
print('C. Live bound: drag, snap on lift, arrows, nearer-bound choice')
h = Harness(NEW)
# between 95 and 105, n = 30: window frozen at 100 +/- 16*2.7386 = 56.18 .. 143.82
seq = [('drag', [(220, 90), (230, 90), (236, 95)]), ('key', 7), ('key', 12), ('key', 8), ('key', 4)]
h.run('SampDist()', events=seq, chooses=[1, 3, 0], inputs=[[100, 15, 30], [95, 105]])
se = 15 / math.sqrt(30)
ww = max(4 * se, min(3.5 * 15, 16 * se))
xlo, xhi = 100 - ww, 100 + ww
x_at = lambda px: xlo + (px - 40) / 274.0 * (xhi - xlo)
stp = 0.5            # NiceNum(2.7386/4 = 0.68) = 0.5
hi_drag = x_at(236)
hi_snap = round(hi_drag / stp) * stp
ok(abs(x_at(220) - 105) < abs(x_at(220) - 95), 'press at 220 is nearer hi')
lines = [t['s'] for f in h.frames for t in f['text'] if t['y'] == 169.0]
ok(any(('%.3f' % hi_drag) in s for s in lines), 'drag frame shows hi = %.3f' % hi_drag)
# after the lift: hi snapped; Left moves hi (active) down one step; Down
# switches to lo; Right moves lo up one step
want_hi = hi_snap - stp
want_lo = 95 + stp
ok(close(h.g('EP_SD_HI'), want_hi, 1e-12) and close(h.g('EP_SD_LO'), want_lo, 1e-12),
   'bounds after drag/keys: lo %r hi %r want %r %r' % (h.g('EP_SD_LO'), h.g('EP_SD_HI'), want_lo, want_hi))
ok(close(h.g('EP_SD_P'), sp_prob(100, se, want_lo, want_hi, 3), 1e-12), 'P after drag/keys')

# crossing over: drag lo past hi -> they swap
h = Harness(NEW)
h.run('SampDist()', events=[('drag', [(150, 90), (300, 90)]), ('key', 4)], chooses=[1, 4, 0],
      inputs=[[100, 15, 30], [99, 101]])
ok(h.g('EP_SD_LO') <= h.g('EP_SD_HI'), 'lo <= hi after a crossing drag')
ok(close(h.g('EP_SD_P'), sp_prob(100, se, h.g('EP_SD_LO'), h.g('EP_SD_HI'), 4), 1e-12), 'outside P after crossing')

# ---------------------------------------------------------------- D. critical mode
print('D. Critical-value mode: a new n moves the critical values, alpha kept; drag changes alpha')
for t in (1, 2, 3):
    h = Harness(NEW)
    h.run('SampDist()', events=[soft(3), ('key', 4)], chooses=[2, t, 0], inputs=[[100, 15, 30, 0.05]])
    se4 = 15 / math.sqrt(120)
    want = {1: norm.ppf(0.05, 100, se4), 2: norm.ppf(0.95, 100, se4), 3: norm.ppf(0.025, 100, se4)}[t]
    ok(close(h.g('EP_SD_LO'), want, 1e-12), 'crit t=%d nx4 lo %r want %r' % (t, h.g('EP_SD_LO'), want))
    ok(close(h.g('EP_SD_P'), 0.95 if t == 3 else 0.05, 1e-12), 'crit t=%d P kept' % t)
# two-tailed drag: mirror about mu, alpha read back from the snapped bound
h = Harness(NEW)
h.run('SampDist()', events=[('drag', [(150, 90), (140, 90)]), ('key', 4)], chooses=[2, 3, 0],
      inputs=[[100, 15, 30, 0.05]])
lo, hi = h.g('EP_SD_LO'), h.g('EP_SD_HI')
ok(close(lo + hi, 200, 1e-12), 'two-tailed drag stays symmetric: %r %r' % (lo, hi))
ok(close(h.g('EP_SD_P'), 1 - 2 * norm.cdf(lo, 100, se), 1e-12), 'two-tailed alpha from bound')
ok(close(round(lo / 0.5) * 0.5, lo, 1e-12), 'snapped to 0.5: %r' % lo)
# then nx4 keeps the dragged alpha
alpha_d = 2 * norm.cdf(lo, 100, se)
h = Harness(NEW)
h.run('SampDist()', events=[('drag', [(150, 90), (140, 90)]), soft(3), ('key', 4)], chooses=[2, 3, 0],
      inputs=[[100, 15, 30, 0.05]])
ok(close(h.g('EP_SD_LO'), norm.ppf(alpha_d / 2, 100, 15 / math.sqrt(120)), 1e-9),
   'nx4 after a drag keeps the dragged alpha')
# Tail cycles lower -> upper -> two-tailed -> lower with alpha kept
h = Harness(NEW)
h.run('SampDist()', events=[soft(5), soft(5), soft(5), ('key', 4)], chooses=[2, 1, 0],
      inputs=[[0, 1, 30, 0.1]])
ok(close(h.g('EP_SD_LO'), norm.ppf(0.1, 0, 1 / math.sqrt(30)), 1e-12), 'tail cycle back to lower')

# ---------------------------------------------------------------- E. mu,sigma and Enter menu
print('E. mu,sigma soft key and the Enter menu')
h = Harness(NEW)
h.run('SampDist()', events=[soft(4), ('key', 30), ('key', 4)], chooses=[1, 1, 3, 0],
      inputs=[[100, 15, 30], [95], [50, 10, 25], [48]])
ok(close(h.g('EP_SD_P'), 1 - norm.cdf(48, 50, 2.0), 1e-12), 'mu,sigma edit then Enter>Next tail: P(xbar > 48)')
h = Harness(NEW)
h.run('SampDist()', events=[soft(4), ('key', 4)], chooses=[1, 1, 0],
      inputs=[[100, 15, 30], [95], [100, -1, 30]])
ok(any(l[0] == 'MSGBOX' for l in h.log), 'invalid sigma refused')
ok(close(h.g('EP_SD_SE'), se, 1e-12), 'nothing changed after a refused edit')
h = Harness(NEW)
h.run('SampDist()', events=[soft(4), ('key', 4)], chooses=[2, 2, 0],
      inputs=[[100, 15, 30, 0.05], [100, 15, 30, 0.01]])
ok(close(h.g('EP_SD_LO'), norm.ppf(0.99, 100, se), 1e-12), 'crit edit of alpha')

# ---------------------------------------------------------------- F. compare view
print('F. Compare: animation, cursor readings, pick a curve, fill order')
h = Harness(NEW)
h.run('SampDist()', events=[('pause', 60), ('drag', [(200, 100)]), ('tap', 172, 42), ('key', 4)],
      chooses=[3, 0], inputs=[[100, 15, 10, 40, 160]])
anim = [f for f in h.frames if any('n growing' in t['s'] for t in f['text'])]
ok(len(anim) == 8, '8 animation frames: %d' % len(anim))
ses = [15 / math.sqrt(k) for k in (10, 40, 160)]
xlo, xhi = 100 - 4 * ses[0], 100 + 4 * ses[0]
cur = [f for f in h.frames if any(t['s'].startswith('P(') and t['y'] == 208.0 for t in f['text'])]
for f in cur:
    lab = [t for t in f['text'] if t['y'] == 208.0 and not t['s'].startswith('touch')]
    xs = float(lab[0]['s'].split('< ')[1].rstrip('):'))
    cx = [l for l in f['line'] if l[1] == l[3] and l[2] == 22.0 and l[4] == 172.0 and l[5] == 0][0][1]
    xv = xlo + (cx - 30) / 284.0 * (xhi - xlo)
    for k in range(3):
        ok(lab[k + 1]['s'] == '%.4f' % norm.cdf(xv, 100, ses[k]), 'cursor P n%d at %g' % (k, xv))
picked = [t['s'] for f in h.frames for t in f['text'] if t['s'].startswith('n = 160:')]
ok(len(picked) >= 1 and '1.1859' in picked[0], 'tap at the n = 160 peak picks it: %r' % picked)
# fill order: the light colours appear in the G2 compose widest first (red n=10, blue, green)
big = max(h.frames, key=lambda f: f['calls'])
fills = [l[5] for l in big['line'] if l[1] == l[3] and l[2] == 172.0 and l[5] in
         (0xFFEBEB, 0xEBF2FF, 0xE8F6EB)]
order = [c for c, _ in itertools.groupby(fills)]
ok(order[:3] == [0xFFEBEB, 0xEBF2FF, 0xE8F6EB], 'fills widest first: %r' % [hex(int(c)) for c in order[:3]])
# compare order reversed n = 160, 40, 10: widest is still drawn first
h = Harness(NEW)
h.run('SampDist()', events=[('key', 4), ('key', 4)], chooses=[3, 0], inputs=[[100, 15, 160, 40, 10]])
big = max(h.frames, key=lambda f: f['calls'])
fills = [l[5] for l in big['line'] if l[1] == l[3] and l[2] == 172.0 and l[5] in
         (0xFFEBEB, 0xEBF2FF, 0xE8F6EB)]
order = [c for c, _ in itertools.groupby(fills)]
ok(order[:3] == [0xE8F6EB, 0xEBF2FF, 0xFFEBEB], 'reversed entry: widest (n3 = 10, green fill) first: %r'
   % [hex(int(c)) for c in order[:3]])
title = [t['s'] for t in big['text'] if t['y'] == 4.0][0]
ok('σ = 15.00' in title, 'compare title sigma (v2.2 fix kept): %r' % title)

# ---------------------------------------------------------------- G. watch
print('G. Watch sample means: the 40 means, their mean and SD, the histogram')
for seed, n in ((7, 30), (11, 4), (3, 250)):
    h = Harness(NEW, seed=seed)
    h.run('SampDist()', events=[('pause', 100000), ('key', 30)], chooses=[4, 0], inputs=[[100, 15, n]])
    rng = random.Random(seed)

    def z():
        while True:
            v1 = 2 * rng.random() - 1
            v2 = 2 * rng.random() - 1
            s = v1 * v1 + v2 * v2
            if 0 < s < 1:
                return v1 * math.sqrt(-2 * math.log(s) / s)
    se = 15 / math.sqrt(n)
    ms = []
    for i in range(40):
        if n > 100:
            ms.append(100 + se * z())
        else:
            ms.append(sum(100 + 15 * z() for j in range(n)) / n)
    mbar = sum(ms) / 40
    sd = math.sqrt(sum((m - mbar) ** 2 for m in ms) / 39)
    last = h.frames[-1]
    s1 = [t['s'] for t in last['text'] if t['y'] == 169.0][0]
    s2 = [t['s'] for t in last['text'] if t['y'] == 180.0][0]
    ok(('%.3f' % mbar) in s1, 'watch n=%d mean %s vs %.3f' % (n, s1, mbar))
    ok(('%.3f' % sd) in s2 and ('%.4f' % se) in s2, 'watch n=%d SD %s vs %.3f' % (n, s2, sd))
    drops = [f for f in h.frames if any(t['s'].startswith('sample ') for t in f['text'])]
    ok(len(drops) == 6 * 5 + 34 * 2, 'drop frames %d' % len(drops))
    # histogram: bar heights are count/(40 se) on the curve's scale
    ymx = norm.pdf(100, 100, se) * 1.15
    bars = [r for r in last['rect'] if r[5] == 0xC800C8]
    tot = 0
    for r in bars:
        cnt_est = (150 - r[2]) / 130.0 * ymx * 40 * se
        tot += cnt_est
    ok(abs(tot - 40) < len(bars) * 1.0, 'histogram heights add to about 40 (%.1f from %d bars)' % (tot, len(bars)))
    if n > 100:
        ok(any('drawn from' in t['s'] for t in last['text']), 'n > 100 says the means were drawn directly')
# skip: a key during the drop finishes at once
h = Harness(NEW, seed=7)
h.run('SampDist()', events=[('pause', 30), ('key', 4), ('key', 4)], chooses=[4, 0], inputs=[[100, 15, 30]])
drops = [f for f in h.frames if any(t['s'].startswith('sample ') for t in f['text'])]
ok(len(drops) < 20, 'a key skips the drop (%d frames)' % len(drops))

# ---------------------------------------------------------------- H. pictures
print('H. Population ghost scale, window, label; help pages; widths; frame cost')
h = Harness(NEW)
h.run('SampDist()', events=[('key', 4)], chooses=[1, 1, 0], inputs=[[100, 15, 30], [95]])
f = h.frames[0]
grey = [l for l in f['line'] if l[5] == 0x969696]
blue = [l for l in f['line'] if l[5] == 0x003CC8]
top_grey = min(min(l[2], l[4]) for l in grey)
top_blue = min(min(l[2], l[4]) for l in blue)
ratio = (150 - top_grey) / float(150 - top_blue)
ok(abs(ratio - 1 / math.sqrt(30)) < 0.02, 'population peak / xbar peak = %.3f (1/sqrt(30) = %.3f)'
   % (ratio, 1 / math.sqrt(30)))
lab = [t for t in f['text'] if t['s'].startswith('population')]
ok(len(lab) == 1 and lab[0]['s'] == u'population (σ = 15)', 'label %r' % lab)
ok(any(t['s'] == '0.10' for t in f['text']) or any(t['s'] == '0.05' for t in f['text']),
   'y-axis density labels present')
# window frozen across n: the x tick labels do not change after nx4
h = Harness(NEW)
h.run('SampDist()', events=[soft(3), soft(3), ('key', 4)], chooses=[1, 1, 0], inputs=[[100, 15, 30], [95]])
ticks = [[t['s'] for t in fr['text'] if t['y'] == 154.0] for fr in h.frames]
ok(ticks[0] == ticks[1] == ticks[2], 'x window frozen across n x4: %r' % ticks)
# help: two pages, both held by a key or a tap
h = Harness(NEW)
h.run('SampDist()', events=[('key', 30), ('tap', 100, 100)], chooses=[5, 0])
ok(len(h.frames) == 2, 'help pages %d' % len(h.frames))
# widths: font-1 text without a width argument must end inside the screen
worst = 0
for path_events in [
        ([('key', 4)], [1, 3, 0], [[-12345.678, 12345.678, 100000], [-20000, 20000]]),
        ([('key', 4)], [2, 3, 0], [[100, 15, 30, 0.05]]),
        ([('pause', 60), ('drag', [(200, 100)]), ('key', 4)], [3, 0], [[100, 15, 10, 40, 160]]),
        ([('key', 30), ('key', 30)], [5, 0], [])]:
    h = Harness(NEW)
    h.run('SampDist()', events=path_events[0], chooses=path_events[1], inputs=path_events[2])
    for fr in h.frames:
        for t in fr['text']:
            if t['w'] is None and (t['font'] in (1.0, None)):
                end = t['x'] + 6.2 * len(t['s'])
                worst = max(worst, end)
                ok(end <= 320, 'text may run off: %r at x=%g (ends ~%d)' % (t['s'], t['x'], end))
print('   widest unclipped font-1 line ends near x = %d (6.2 px per character)' % worst)
# cost of one drag frame
h = Harness(NEW)
h.run('SampDist()', events=[('drag', [(150, 90), (160, 90), (170, 90), (180, 90)]), ('key', 4)],
      chooses=[1, 2, 0], inputs=[[100, 15, 30], [80]])
costs = [fr['calls'] for fr in h.frames]
print('   drawing calls per live frame (right tail, n = 30): %s' % costs)

# =========================================================================== I. v2.3a (harness v3e)
print('I. v2.3a: no "=" before a relation; the right tail as a lower tail (harness v3e)')
import re as _re
import difflib as _dl
from ppl_run_v3e import Harness as H3
V23 = os.path.join(HERE, 'SampDist_v2.3.txt')
I_RUNS = {NEW: [], V23: []}
XB = chr(57344)


def i_run(path, tail, lo, hi=None, mu=0.0, sg=1.0, nn=1):
    h = H3(path)
    h.answer({'mu': mu, 'sg': sg, 'nn': nn}); h.choose(tail)
    h.answer({'lo': lo} if hi is None else {'lo': lo, 'hi': hi}); h.press('Esc')
    h.call('sd_modeProb')
    I_RUNS[path].append(h)
    f = h.pages[-1]
    return [t.text for t in f.texts if t.text.startswith('P(') or t.text.startswith('z =')], h.globals_['EP_SD_P']


def i_sp(tail, lo, hi, mu, se):
    if tail == 1:
        return norm.cdf(lo, mu, se)
    if tail == 2:
        return norm.sf(lo, mu, se)
    if tail == 3:
        return norm.cdf(hi, mu, se) - norm.cdf(lo, mu, se)
    return norm.cdf(lo, mu, se) + norm.sf(hi, mu, se)


for args, old, new in (
        ((1, -6), ['P(' + XB + ' < -6.000) = < 0.000001', 'z = -6.0000   = < 0.001%'],
         ['P(' + XB + ' < -6.000) < 0.000001', 'z = -6.0000   < 0.001%']),
        ((2, 6), ['P(' + XB + ' > 6.000) = < 0.000001', 'z = 6.0000   = < 0.001%'],
         ['P(' + XB + ' > 6.000) < 0.000001', 'z = 6.0000   < 0.001%']),
        ((2, 10), ['P(' + XB + ' > 10.000) = 0.000000', 'z = 10.0000   = 0.000%'],
         ['P(' + XB + ' > 10.000) < 0.000001', 'z = 10.0000   < 0.001%']),
        ((3, 5, 6), ['P(5.000 < ' + XB + ' < 6.000) = < 0.000001', 'z = 5.0000 to 6.0000   = < 0.001%'],
         ['P(5.000 < ' + XB + ' < 6.000) < 0.000001', 'z = 5.0000 to 6.0000   < 0.001%']),
        ((4, -10, 10), ['P(outside -10.000 .. 10.000) = < 0.000001', 'z = -10.0000 / 10.0000   = < 0.001%'],
         ['P(outside -10.000 .. 10.000) < 0.000001', 'z = -10.0000 / 10.0000   < 0.001%']),
        ((2, 1), ['P(' + XB + ' > 1.000) = 0.158655', 'z = 1.0000   = 15.866%'], None),
        ((4, -1, 1), ['P(outside -1.000 .. 1.000) = 0.317311', 'z = -1.0000 / 1.0000   = 31.731%'], None),
        ((2, 0.5, None, 0.0, 1.0, 30), ['P(' + XB + ' > 0.500) = 0.003085', 'z = 2.7386   = 0.308%'], None)):
    a, b = i_run(V23, *args), i_run(NEW, *args)
    if new is None:
        ok(a[0] == old and b[0] == old, 'I1 %r: an ordinary panel is the same in v2.3 and v2.3a: %r %r' % (args, a[0], b[0]))
    else:
        ok(a[0] == old and b[0] == new, 'I1 %r: v2.3 %r -> v2.3a %r' % (args, a[0], b[0]))
    print('   I1 %r: v2.3 %r  ->  v2.3a %r' % (args, a[0], b[0]))
# the exported value: the right tail kept
a, b = i_run(V23, 2, 10), i_run(NEW, 2, 10)
ok(a[1] == 0 and close(b[1], norm.sf(10), 1e-9), 'I2 EP_SD_P, P(x̄ > 10), μ 0, σx̄ 1: v2.3 %r -> v2.3a %r (SciPy %r)'
   % (a[1], b[1], norm.sf(10)))
a, b = i_run(V23, 4, -10, 10), i_run(NEW, 4, -10, 10)
ok(close(a[1], norm.cdf(-10), 1e-9) and close(b[1], 2 * norm.sf(10), 1e-9),
   'I2 EP_SD_P, outside -10..10: v2.3 held only the left half (%r), v2.3a both (%r; SciPy %r)' % (a[1], b[1], 2 * norm.sf(10)))
# sd_prob directly (the live graph): every tail against SciPy, and v2.3 where 1 - CDF still has its digits
hq = H3(NEW)
hq3 = H3(V23)
worst, same, n = 0.0, 0, 0
for mu_, se_ in ((0.0, 1.0), (100.0, 15.0 / 30 ** 0.5), (-2.5, 0.2)):
    for z1 in (-12, -6, -3, -1.5, 0, 0.7, 2, 4, 8, 12):
        for dz in (0.5, 2):
            lo_, hi_ = mu_ + z1 * se_, mu_ + (z1 + dz) * se_
            for tail in (1, 2, 3, 4):
                v = hq.call('sd_prob', mu_, se_, lo_, hi_, float(tail))
                s = i_sp(tail, lo_, hi_, mu_, se_)
                n += 1
                if s > 1e-300:
                    worst = max(worst, abs(v - s) / max(s, 1e-12) if s < 1e-12 else abs(v - s) / s)
                v3 = hq3.call('sd_prob', mu_, se_, lo_, hi_, float(tail))
                if abs(v3 - v) <= 1e-12 * max(1.0, abs(v)) or (tail in (2, 4) and s < 1e-8):
                    same += 1
ok(worst < 1e-9, 'I2 sd_prob, %d cases (3 normals, 4 tails, z -12 to 14): within %.1e of SciPy' % (n, worst))
ok(same == n, 'I2 sd_prob: equal to v2.3 in every case but a right tail too small for 1 - CDF (%d of %d)' % (same, n))


# I3. a sweep of panels: identical to v2.3 once its "= <" and its right-tail zeros are written the v2.3a way
def i_rw(t, s):
    t = _re.sub(r' = ([<>] )', r' \1', t)
    if s > 0:
        t = t.replace(') = 0.000000', ') < 0.000001').replace('   = 0.000%', '   < 0.001%')
    return t


diffs, nrw, n = [], 0, 0
for nn_ in (1, 30, 400):
    se_ = 1.0 / nn_ ** 0.5
    for tail in (1, 2, 3, 4):
        for z1 in (-9, -5, -3.2, -1, 0, 1.3, 2.6, 4.9, 9):
            lo_ = round(z1 * se_, 3)
            hi_ = None if tail <= 2 else round((z1 + 1.5) * se_, 3)
            a, b = i_run(V23, tail, lo_, hi_, 0.0, 1.0, nn_), i_run(NEW, tail, lo_, hi_, 0.0, 1.0, nn_)
            s = i_sp(tail, lo_, lo_ if hi_ is None else hi_, 0.0, se_)
            ra = [i_rw(x, s) for x in a[0]]
            n += 1
            nrw += ra != a[0]
            if ra != b[0]:
                diffs.append((tail, lo_, hi_, nn_, ra, b[0]))
ok(not diffs, 'I3 %d panels (4 tails, n 1 / 30 / 400, z -9 to 9): identical to v2.3 once its "= <" and right-tail '
   'zeros are written the v2.3a way (%d needed it): %r' % (n, nrw, diffs[:1]))
print('   I3 %d panels, %d of them rewritten from v2.3\'s text' % (n, nrw))
# I4. sd_Eq
e = [hq.call('sd_Eq', x) for x in ('< 0.000001', '> -0.000001', '0.158655', '')]
ok(e == [' < 0.000001', ' > -0.000001', ' = 0.158655', ' = '], 'I4 sd_Eq: %r' % e)


# I5. the diff v2.3 -> v2.3a
def i_code(txt):
    out = []
    for l in txt.split('\n'):
        o, ins = [], False
        for i, ch in enumerate(l):
            if ch == '"':
                ins = not ins
            if not ins and l[i:i + 2] == '//':
                break
            o.append(ch)
        s = ''.join(o).strip()
        if s:
            out.append(s)
    return out


# v2.3b: I5 is v2.3a's change set (v2.3 -> v2.3a), so it reads the v2.3a file; part J has v2.3b's
t0, t1 = open(V23, encoding='utf-8').read(), open(V23A, encoding='utf-8').read()
k0, k1 = i_code(t0), i_code(t1)
mi, pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, k0, k1, autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        mi += k0[i1:i2]
    if op in ('replace', 'insert'):
        pl += k1[j1:j2]
wm = ['IF tailK == 2 THEN pv := 1 - NORMALD_CDF(mu, se, lo); END;'] * 2 + \
     ['pv := NORMALD_CDF(mu, se, lo) + (1 - NORMALD_CDF(mu, se, hi));'] * 2 + \
     ['s1 := "P(" + CHAR(57344) + " < " + STRING(lo,2,3) + ") = " + sd_fmtp(pv,6);',
      's1 := "P(" + CHAR(57344) + " > " + STRING(lo,2,3) + ") = " + sd_fmtp(pv,6);',
      'STRING(hi,2,3) + ") = " + sd_fmtp(pv,6);', '") = " + sd_fmtp(pv,6);',
      's2 := s2 + "   = " + sd_fmtp(pv*100,3) + "%";']
wp = ['sd_Eq(eqS)', 'BEGIN', 'IF DIM(eqS) > 0 THEN', 'IF LEFT(eqS, 1) == "<" OR LEFT(eqS, 1) == ">" THEN RETURN " " + eqS; END;',
      'END;', 'RETURN " = " + eqS;', 'END;'] + \
     ['IF tailK == 2 THEN pv := NORMALD_CDF(mu, se, 2*mu - lo); END;'] * 2 + \
     ['pv := NORMALD_CDF(mu, se, lo) + NORMALD_CDF(mu, se, 2*mu - hi);'] * 2 + \
     ['s1 := "P(" + CHAR(57344) + " < " + STRING(lo,2,3) + ")" + sd_Eq(sd_fmtp(pv,6));',
      's1 := "P(" + CHAR(57344) + " > " + STRING(lo,2,3) + ")" + sd_Eq(sd_fmtp(pv,6));',
      'STRING(hi,2,3) + ")" + sd_Eq(sd_fmtp(pv,6));', '")" + sd_Eq(sd_fmtp(pv,6));',
      's2 := s2 + "  " + sd_Eq(sd_fmtp(pv*100,3)) + "%";']
ok(sorted(mi) == sorted(wm) and sorted(pl) == sorted(wp), 'I5 the code lines that changed are exactly the 9 listed '
   '(and sd_Eq\'s 7): -%r +%r' % ([x for x in mi if x not in wm], [x for x in pl if x not in wp]))
BI = set(l.strip().lower() for l in open('/home/claude/work/gate_r2/HP_Prime_Builtin_Names.txt', encoding='utf-8')
         if l.strip() and not l.startswith('#'))
ok(not any(x.lower() in BI for x in ('sd_Eq', 'eqS')), 'I5 sd_Eq and eqS are not built-ins (case ignored)')
ok('(HP Prime G2 and G1).  v2.3a has' in t1 and 'SampDist_v2.3a_CHANGES.md' in t1 and '// v2.3a (17 Oct 2026, evening)' in t1
   and 'verify_SampDist_v2.3a.py' in t1, 'I5 version strings: the tested-on lines, the CHANGES and verify names, the '
   'v2.3a paragraph')
depth, bad = 0, []
for n_, l in enumerate(t1.split('\n'), 1):
    ins, start = False, depth
    for i, ch in enumerate(l):
        if ch == '"':
            ins = not ins
        elif not ins:
            if l[i:i + 2] == '//':
                if start > 0:
                    bad.append(n_)
                break
            if ch in '({[':
                depth += 1
            elif ch in ')}]':
                depth -= 1
ok(not bad, 'I5 no // comment inside an open bracket: %r' % bad[:5])
ok(not any('INSTRING(' in l for l in k1), 'I5 no INSTRING in v2.3a\'s code; sd_Eq reads LEFT(eqS, 1) only inside IF DIM(eqS) > 0')
sci = sorted(set((round(v, 12), d, r) for h in I_RUNS[NEW] for v, d, r in h.sci_strings))
sco = sorted(set((round(v, 12), d, r) for h in I_RUNS[V23] for v, d, r in h.sci_strings))
print('   I6 scientific fixed decimals: v2.3a %r, v2.3 %r' % (sci[:3], sco[:3]))
ok(not sci or sci == sco, 'I6 no new scientific fixed decimal in the %d v2.3a runs of part I' % len(I_RUNS[NEW]))


# =========================================================================== J. v2.3b (harness v3e)
print('J. v2.3b: S1 (the alpha floor 1E-7) and S2 (sd_fix\'s right tail as a lower tail)')
sys.path.insert(0, '/home/claude/work/review')
import io as _io
import contextlib as _cl
import check_SampDist as CSD      # the review's own checks (19 Oct 2026); it imports ppl_run_v3e
J_RUNS = {NEW: [], V23A: []}


def j_drag_edge(path, tail_label, digits):
    """the review's S1 reproduction: Find critical value, mu 100, sigma 15, n 30, alpha 0.05, the tail, then the red
    line dragged to the right edge of the plot; the last panel's P line and z line, and EP_SD_P"""
    h = H3(path, strict=False, cas='fail', stall_limit=30000)
    h.choose('Find critical value'); h.answer({'mu': 100, 'sg': 15, 'nn': 30, 'alp': 0.05})
    h.choose(tail_label)
    h.drag([(200, 80), (250, 80), (300, 80), (314, 80)])
    h.press('Esc'); h.choose(0)
    CSD.twelve_digits(digits)
    try:
        h.call('SampDist')
    finally:
        CSD.twelve_digits(False)
    J_RUNS[path].append(h)
    last = [pg for pg in h.pages if pg.has('P(' + XB)]
    line = [t.text for t in last[-1].texts if t.text.startswith('P(')] if last else ['?']
    zline = [t.text for t in last[-1].texts if t.text.startswith('z =')] if last else ['?']
    return line[0], zline[0], h.globals_['EP_SD_P']


for digits in (False, True):
    a = j_drag_edge(V23A, 'Upper tail', digits)
    b = j_drag_edge(NEW, 'Upper tail', digits)
    print('   J1 %s: v2.3a %r %r EP_SD_P %r' % ('12 digits' if digits else 'doubles', a[0], a[1], a[2]))
    print('   J1 %s: v2.3b %r %r EP_SD_P %r' % ('12 digits' if digits else 'doubles', b[0], b[1], b[2]))
    ok(a[0].endswith(') = 0.000001') and b[0].endswith(') < 0.000001') and b[1].endswith('< 0.001%')
       and a[0].split(')')[0] == b[0].split(')')[0] and close(b[2], 1e-7, 1e-12),
       'J1 S1 (%s): upper tail, line dragged to the right edge: v2.3a %r, v2.3b %r (EP_SD_P = 1E-7, the floor)'
       % ('12 digits' if digits else 'doubles', a[0], b[0]))
# the lower tail dragged to the left edge, and the two-tailed region: the floor reads the same way
for tail_label, drag, want_end in (('Lower tail', [(200, 80), (150, 80), (90, 80), (41, 80)], ') < 0.000001'),):
    h = H3(NEW, strict=False, cas='fail', stall_limit=30000)
    h.choose('Find critical value'); h.answer({'mu': 100, 'sg': 15, 'nn': 30, 'alp': 0.05})
    h.choose(tail_label); h.drag(drag); h.press('Esc'); h.choose(0)
    h.call('SampDist')
    J_RUNS[NEW].append(h)
    last = [pg for pg in h.pages if pg.has('P(' + XB)]
    line = [t.text for t in last[-1].texts if t.text.startswith('P(')] if last else ['?']
    ok(line[0].endswith(want_end) and close(h.globals_['EP_SD_P'], 1e-7, 1e-12),
       'J1 S1: lower tail, line dragged to the left edge: %r, EP_SD_P %r' % (line[0], h.globals_['EP_SD_P']))
# sd_fix directly: the clamp at both ends, and every tail
hj = H3(NEW)
hj3 = H3(V23A)
mu_, se_ = 100.0, 15 / 30 ** 0.5
r_hi = hj.call('sd_fix', mu_, se_, mu_ + 16 * se_, mu_ + 16 * se_, 2.0, 1.0, 1.0, 0.05)
r_lo = hj.call('sd_fix', mu_, se_, mu_ - 16 * se_, mu_ - 16 * se_, 2.0, 1.0, 1.0, 0.05)
r_lt = hj.call('sd_fix', mu_, se_, mu_ + 16 * se_, mu_ + 16 * se_, 1.0, 1.0, 1.0, 0.05)
o_hi = hj3.call('sd_fix', mu_, se_, mu_ + 16 * se_, mu_ + 16 * se_, 2.0, 1.0, 1.0, 0.05)
ok(r_hi[3] == 1e-7 and r_lo[3] == 0.9999999 and r_lt[3] == 0.9999999 and o_hi[3] == 1e-6,
   'J2 S1: sd_fix clamps alpha to [1E-7, 1 - 1E-7] (v2.3a [1E-6, 1 - 1E-6]): upper tail at z = 16 -> %r (v2.3a %r), '
   'at z = -16 -> %r; lower tail at z = 16 -> %r' % (r_hi[3], o_hi[3], r_lo[3], r_lt[3]))
crit = [hj.call('sd_crit', mu_, se_, a_, float(t_)) for a_ in (1e-7, 0.9999999) for t_ in (1, 2, 3)]
want = [norm.ppf(1e-7, mu_, se_), norm.ppf(1 - 1e-7, mu_, se_), norm.ppf(0.5e-7, mu_, se_),
        norm.ppf(0.9999999, mu_, se_), norm.ppf(1e-7, mu_, se_), norm.ppf(0.49999995, mu_, se_)]
ok(all(close(c[0], w, 1e-9) for c, w in zip(crit, want)),
   'J2 S1: sd_crit at the new floor and ceiling (NORMALD_ICDF at 1E-7, 5E-8, 1 - 1E-7): every tail = SciPy ppf')
# S2: alpha from a bound in the upper tail, z = 0.5 .. 5.3, against SciPy, doubles and 12 digits
for digits in (False, True):
    CSD.twelve_digits(digits)
    try:
        w_new = w_old = 0
        # z up to 5.1, where the tail (1.7E-7) is still above the new floor; v2.3a's own floor (1E-6) is reached
        # at z = 4.75, so it is measured up to 4.5
        for z in (0.5, 1, 1.645, 2.5, 3.2, 4, 4.5, 5, 5.1):
            b_ = mu_ + z * se_
            vn = hj.call('sd_fix', mu_, se_, b_, b_, 2.0, 1.0, 1.0, 0.05)[3]
            vo = hj3.call('sd_fix', mu_, se_, b_, b_, 2.0, 1.0, 1.0, 0.05)[3]
            s_ = norm.sf(z)
            w_new = max(w_new, abs(vn - s_) / s_)
            if z <= 4.5:
                w_old = max(w_old, abs(vo - s_) / s_)
    finally:
        CSD.twelve_digits(False)
    print('   J3 S2 (%s): alpha from the bound, z 0.5 .. 5.1: v2.3b worst relative error %.1e, v2.3a (z to 4.5) %.1e'
          % ('12 digits' if digits else 'doubles', w_new, w_old))
    ok(w_new < 1e-10, 'J3 S2 (%s): sd_fix\'s upper-tail alpha = SciPy sf within %.1e relative (v2.3a: %.1e)'
       % ('12 digits' if digits else 'doubles', w_new, w_old))
# the same α on the panel as before wherever v2.3a showed a digit: a sweep of dragged positions, both versions
same, n_ = 0, 0
for z in (-3, -1, 0, 0.8, 1.645, 2.33, 3.1, 4.2):
    for t_ in (1.0, 2.0, 3.0):
        if z == 0 and t_ == 3.0:
            continue          # alpha = 2 Phi(0) = 1: the ceiling itself (1 - 1E-6 then, 1 - 1E-7 now; J2)
        b_ = mu_ + z * se_
        vn = hj.call('sd_fix', mu_, se_, b_, b_ if t_ < 3 else 2 * mu_ - b_, t_, 1.0, 1.0, 0.05)
        vo = hj3.call('sd_fix', mu_, se_, b_, b_ if t_ < 3 else 2 * mu_ - b_, t_, 1.0, 1.0, 0.05)
        n_ += 1
        same += abs(vn[3] - vo[3]) <= 1e-12 and vn[:3] == vo[:3]
ok(same == n_, 'J3 sd_fix gives v2.3a\'s bounds and alpha (to 1E-12) for %d dragged positions inside the old clamp'
   % n_)

# J4. the review's check_SampDist.py: its parts on v2.3b; part C's two demonstrations of S1/S2 turned round
def j_cs(path, letters):
    CSD.PROG = path
    CSD.FAILS[:] = []
    CSD.NCHK[0] = 0
    buf = _io.StringIO()
    with _cl.redirect_stdout(buf):
        for L in letters:
            getattr(CSD, 'part' + L)()
    CSD.twelve_digits(False)
    return CSD.NCHK[0], list(CSD.FAILS), buf.getvalue()


n_o, f_o, log_o = j_cs(V23A, 'ABCDEFGHI')
n_n, f_n, log_n = j_cs(NEW, 'ABCDEFGHI')
print('   J4 the review\'s check_SampDist on v2.3a: %d checks, failed %s' % (n_o, f_o))
print('   J4 the review\'s check_SampDist on v2.3b: %d checks, failed %s' % (n_n, f_n))
s1 = [f for f in f_n if 'still computes alpha' in f]
s2 = [f for f in f_n if 'clamp itself shows' in f]
# part C's comparison of the two forms after a clamp to [1e-6, 0.999999] is written for v2.3a's clamp: at z = 7.5
# v2.3b's alpha is the new floor 1E-7, not 1E-6, so the comparison now differs by 9E-7 (S1 itself)
s2 += [f for f in f_n if f.startswith('C after the clamp to [1e-6, 0.999999]')]
s3 = [f for f in f_n if f.startswith('H sigma = 0.000045')]
other = [f for f in f_n if f not in s1 + s2 + s3]
ok(not other and s1 and s2 and s3 and [f for f in f_o if f.startswith('H sigma')] == s3,
   'J4 check_SampDist on v2.3b: everything passes except (a) part C\'s three demonstrations of S2 and S1 (the 1 - CDF '
   'slip, the "= 0.000001", and a comparison written for the old 1E-6 clamp), which held on v2.3a and now fail because '
   'those are gone, and (b) the H check of S3 (sigma 0.000045 prints '
   'the Prime\'s scientific form), which is not in this pass and fails on both versions alike: other failures %r' % other)
pl = [l for l in log_n.split('\n') if 'after a drag to the right edge' in l]
print('   J4 the review\'s own reproduction on v2.3b:%s' % (pl[0] if pl else ' ?'))
ok(bool(pl) and ') < 0.000001' in pl[0], 'J4 the review\'s reproduction of S1 (part C, 12 digits) reads "< 0.000001" on v2.3b')


# J5. the routine diff v2.3a -> v2.3b
def j_bodies(txt):
    c = _re.sub(r'//[^\n]*', '', txt)
    out = {}
    for m in _re.finditer(r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, _re.S):
        out[m.group(1)] = _re.sub(r'\n\s*\n', '\n', _re.sub(r'[ \t]+\n', '\n', m.group(0)))
    return out


ta, tb = open(V23A, encoding='utf-8').read(), open(NEW, encoding='utf-8').read()
Ba, Bb = j_bodies(ta), j_bodies(tb)
dif = sorted(n for n in set(Ba) | set(Bb) if Ba.get(n) != Bb.get(n))
ok(dif == ['sd_fix'], 'J5 the routines that differ from v2.3a: %r (want sd_fix only; %d routines)' % (dif, len(Bb)))
ka, kb = i_code(ta), i_code(tb)
mi, pl = [], []
for op, i1, i2, j1, j2 in _dl.SequenceMatcher(None, ka, kb, autojunk=False).get_opcodes():
    if op in ('replace', 'delete'):
        mi += ka[i1:i2]
    if op in ('replace', 'insert'):
        pl += kb[j1:j2]
ok(mi == ['IF tailK == 2 THEN fxP := 1 - NORMALD_CDF(mu, se, fxL); END;', 'fxP := MAX(0.000001, MIN(0.999999, fxP));']
   and pl == ['IF tailK == 2 THEN fxP := NORMALD_CDF(mu, se, 2*mu - fxL); END;', 'fxP := MAX(0.0000001, MIN(0.9999999, fxP));'],
   'J5 the code lines that changed are exactly the two of S1 and S2: -%r +%r' % (mi, pl))
# J6. the static rules
vb = tb.split('\n')
depth, badb = 0, []
for n_, l in enumerate(vb, 1):
    ins, start = False, depth
    for i, ch in enumerate(l):
        if ch == '"':
            ins = not ins
        elif not ins:
            if l[i:i + 2] == '//':
                if start > 0:
                    badb.append(n_)
                break
            if ch in '({[':
                depth += 1
            elif ch in ')}]':
                depth -= 1
ok(not badb, 'J6 no // comment inside an open bracket: %r' % badb[:5])
ok('(HP Prime G2 and G1).  v2.3b has' in tb and 'SampDist_v2.3b_CHANGES.md' in tb and '// v2.3b (19 Oct 2026)' in tb
   and 'verify_SampDist_v2.3b.py' in tb and 'only in the PC\n//   harness (ppl_run_v3e, 19 Oct 2026)' in tb,
   'J6 version strings: the tested-on lines (PC harness only), the CHANGES and verify names, the v2.3b paragraph')
ok('// DISCLAIMER: a teaching and demonstration aid. Not validated for' in tb and 'legal purposes.' in tb,
   'J6 the disclaimer line beside the distribution terms (Roger, 19 Oct 2026, 12:48)')
locs = _re.findall(r'^\s*LOCAL ([^;(]*);', '\n'.join(i_code(tb)), _re.M)
ok(max(len(m.split(',')) for m in locs) <= 6 and not any('INSTRING(' in l for l in i_code(tb)),
   'J6 every LOCAL line holds at most 6 names; no INSTRING')
# J7. scientific fixed decimals in the part-J runs
scj = sorted(set((round(v, 12), d, r) for h in J_RUNS[NEW] for v, d, r in h.sci_strings))
sco = sorted(set((round(v, 12), d, r) for h in J_RUNS[V23A] for v, d, r in h.sci_strings))
sci_i = sorted(set((round(v, 12), d, r) for h in I_RUNS[NEW] for v, d, r in h.sci_strings))
sci_i3 = sorted(set((round(v, 12), d, r) for h in I_RUNS[V23] for v, d, r in h.sci_strings))
print('   J7 scientific fixed decimals: v2.3b part J %r, part I %r; v2.3a part J %r; v2.3 part I %r'
      % (scj[:3], sci_i[:3], sco[:3], sci_i3[:3]))
# the one entry, a tick label -5.6E-17 from xv := xv + stp summed in doubles, is the harness's: on the Prime a sum of
# 1-2-5 steps is exact BCD (findings_B, SampDist); v2.3 and v2.3a log the same one
ok(not scj and sci_i == sci_i3 and all(abs(v) < 1e-15 and d == 1 for v, d, r in sci_i),
   'J7 no scientific fixed decimal in any v2.3b run of parts I and J (%d runs) but the harness\'s own tick-label '
   'artefact %r, which v2.3 logs too' % (len(J_RUNS[NEW]) + len(I_RUNS[NEW]), [r for v, d, r in sci_i]))

print()
print('%d checks, %d failures' % (checks[0], len(fails)))
sys.exit(1 if fails else 0)
