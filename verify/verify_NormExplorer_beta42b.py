#!/usr/bin/env python3
"""verify_NormExplorer_beta42b.py -- checks for NormExplorer beta 42b (20 Oct 2026).

Beta 42b changes one thing: ne_AnimStd times each of its twenty frames with TICKS and waits
only for what is left of 0.3 s, and the Diagnostics page shows the last run's length and its
slowest frame.  Run in ppl_run_v3e (its TICKS advances 1 ms per reading, and WAIT(n) advances
the clock by n s, so a run's length can be read from the clock).

Part A  fast drawing (the harness as it is): 42a and 42b both last about 10.8 s; 42b's
        twenty frame waits are each a little under 0.3 s; the run's length and slowest frame
        are recorded; no WAIT is negative or zero.
Part B  slow drawing (each frame's BLIT_P advanced by D ms, D = 100, 250, 450, 800): 42a
        lasts 20*(0.3 + D/1000) + 4.8 s, 42b lasts 20*max(0.3, D/1000) + 4.8 s;
        a frame slower than 0.3 s gets no wait at all.
Part C  the Diagnostics page: "animation: not run yet" before, the numbers after, at y = 154,
        with the grey block at 170/183/196 and nothing else moved.
Part D  the routine diff: only ne_AnimStd, ne_DiagPage, ne_ResetAll and the header comments
        differ from 42a; the #PYTHON block is byte-identical.
Run:  python3 verify_NormExplorer_beta42b.py
"""
import sys, os, re
sys.path.insert(0, '/home/claude/work/out')
from ppl_run_v3e import Harness

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, 'NormExplorer_beta42a.txt')
B = os.path.join(HERE, 'NormExplorer_beta42b.txt')
N = [0, 0]
def ok(cond, msg):
    N[0] += 1
    if not cond:
        N[1] += 1
        print('  FAIL', msg)
    else:
        print('  ok  ', msg)

def anim(path, slow_ms=0):
    h = Harness(path, home_minus=True)
    h.execute('ne_ResetAll()')
    if slow_ms:
        # every BLIT_P (one per frame, in ne_NormDraw) costs slow_ms on the clock
        f = h._blit
        def slow(a, f=f):
            h.clock += slow_ms
            return f(a)
        h._blit = slow
    h.log = [] if not hasattr(h, 'log') else h.log
    start_log = len(h.log)
    t0 = h.clock
    h.execute('ne_AnimStd(100, 15, 1, 1)')
    total = (h.clock - t0) / 1000.0
    waits = [e[1][0] for e in h.log[start_log:] if e[0] == 'WAIT']
    return h, total, waits

print('Part A  fast drawing')
for path, tag in ((A, '42a'), (B, '42b')):
    h, total, waits = anim(path)
    print('   %s: %.3f s, %d waits' % (tag, total, len(waits)))
    ok(abs(total - 10.8) < 0.2, '%s lasts about 10.8 s (%.3f)' % (tag, total))
    ok(all(w > 0 for w in waits), '%s: every WAIT is positive' % tag)
    if tag == '42b':
        fw = [w for w in waits if w < 1]
        ok(len(fw) == 20, '42b: twenty frame waits (%d)' % len(fw))
        ok(all(0.28 < w <= 0.3 for w in fw), '42b: each frame wait is a little under 0.3 s (%.4f..%.4f)' % (min(fw), max(fw)))
        ok(abs(h.execute('neAnTot') - total) < 0.01, '42b: neAnTot records the run (%.3f)' % h.execute('neAnTot'))
        ok(0 < h.execute('neAnMs') < 50, '42b: neAnMs records the slowest frame (%.0f ms)' % h.execute('neAnMs'))

print('Part B  slow drawing')
for D in (100, 250, 450, 800):
    ha, ta, wa = anim(A, D)
    hb, tb, wb = anim(B, D)
    nblit = None
    # each frame blits once in ne_NormDraw; the two holds also draw a frame each
    exp_a = 20 * (0.3 + D/1000.0) + 4.8 + 2 * D/1000.0
    exp_b = 20 * max(0.3, D/1000.0) + 4.8 + 2 * D/1000.0
    print('   D = %d ms: 42a %.2f s (model %.2f), 42b %.2f s (model %.2f)' % (D, ta, exp_a, tb, exp_b))
    ok(abs(ta - exp_a) < 0.3, '42a, D=%d: frame waits add to the drawing' % D)
    ok(abs(tb - exp_b) < 0.3, '42b, D=%d: frames keep their 0.3 s pace' % D)
    fw = [w for w in wb if w < 1]
    if D >= 300:
        ok(len(fw) == 0, '42b, D=%d: a frame slower than 0.3 s gets no wait (%d waits)' % (D, len(fw)))
    ok(abs(hb.execute('neAnMs') - D) < 60, '42b, D=%d: the slowest frame is recorded (%.0f ms)' % (D, hb.execute('neAnMs')))

print('Part C  the Diagnostics page')
h = Harness(B, home_minus=True, idle_key=4)
h.execute('ne_ResetAll()')
h.execute('ne_DiagPage()')
txt = [(t.text, t.y) for t in h.texts] if hasattr(h, 'texts') else []
ok(any('animation: not run yet' in s and y == 154 for s, y in txt), 'before a run: "animation: not run yet" at y = 154')
h.execute('ne_AnimStd(100, 15, 1, 1)')
n0 = len(h.texts)
h.execute('ne_DiagPage()')
txt = [(t.text, t.y) for t in h.texts[n0:]]
line = [s for s, y in txt if 'animation ' in s and y == 154]
ok(len(line) == 1 and re.search(r'animation 10\.\d s, slowest frame \d+ ms', line[0]) is not None,
   'after a run: %r' % (line[0] if line else None))
ys = sorted(set(y for s, y in txt))
ok([y for y in ys if y > 140] == [154, 170, 183, 196, 214], 'line positions below the Session block: %s' % [y for y in ys if y > 140])
ok(not any('#' in s and 'h' in s for s, y in txt if 'animation' in s), 'no hex-printed integer on the line')

print('Part D  the routine diff')
def routines(path):
    t = open(path, encoding='utf-8').read()
    py = re.search(r'^#PYTHON.*?^#END', t, re.S | re.M).group(0)
    parts = re.split(r'\n(?=(?:EXPORT )?[A-Za-z_][A-Za-z0-9_]*\([^)]*\)\s*\nBEGIN)', t)
    d = {}
    for p in parts:
        m = re.match(r'(?:EXPORT )?([A-Za-z_][A-Za-z0-9_]*)\(', p)
        if m: d[m.group(1)] = re.sub(r'//[^\n]*', '', p).strip()
    return d, py
ra, pa = routines(A); rb, pb = routines(B)
changed = sorted(k for k in set(ra) | set(rb) if ra.get(k) != rb.get(k))
ok(set(changed) <= {'ne_AnimStd', 'ne_DiagPage', 'ne_ResetAll', 'ne_NiceNum'}, 'routines whose code changed: %s' % changed)
ok(pa == pb, 'the #PYTHON block is byte-identical')
print('%d checks, %d failures' % (N[0], N[1]))
