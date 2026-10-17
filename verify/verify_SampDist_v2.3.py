# -*- coding: utf-8 -*-
"""verify_SampDist_v2.3.py -- runs SampDist v2.3 (and v2.2 for comparison) in
hp-prime-kit's interpreter through ppl_harness_v1, with scripted menu answers,
form values, soft-key taps, drags and keys, and checks every number against
SciPy.  16 Oct 2026.

    python3 verify_SampDist_v2.3.py
"""
from __future__ import print_function
import sys, os, math, random, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ppl_harness_v1 import Harness
from scipy.stats import norm

NEW = os.path.join(HERE, 'SampDist_v2.3.txt')
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

print()
print('%d checks, %d failures' % (checks[0], len(fails)))
sys.exit(1 if fails else 0)
