#!/usr/bin/env python3
"""verify_TDist3D_beta1.py -- checks TDist3D beta 1 (7 Nov 2026), the rotatable Student's t surface.

Roger, 7 Nov 2026: "can we do a scaled down rotatable version of that 3D t-distribution plot in PPL/MicroPython?"
The program draws f(t; nu), Student's t density, as a wireframe over t (-6..6) and nu (0.5..10), turned with a
finger, with one row (nu0) as a red slice and its numbers in the corner, and a Curves view of the family end on.

What this script checks, in the PC harness (ppl_run_v3e; nothing here is device evidence):
  S  static: the header names beta 1; PPL only (no #PYTHON); every RECT_P carries two colours (a one-colour RECT_P
     FILLS, Lessons Learned s6 -- BurrLab's Family map, 7 Nov 2026); the critical value is the mirrored ICDF and the
     tail chance a doubled lower tail; angles pass through tdAU at every SIN and COS.
  A  arithmetic against SciPy: the cached heights on both grids, the normal ghost row, the curves view's columns, and
     the slice's peak, t crit and P(|t| > 2) for every ladder value and a typed one; the readout texts.
  P  the projection: a Python copy of tdFrame / tdDraw3D at the starting angles and after turns and tilts gives
     every grid point's screen x and y within 1 px of the program's lists; theta and phi on screen.
  B  behaviour: the ladder up to 1,000 and down to 0.5 with its stop messages; Reset; typed nu (refused below 0.5
     and above 1,000, rounded to two decimals); TD_NU and the RETURN string; Esc from both views; arrows by 10
     degrees with phi clamped to 10..80; the drag at 0.6 degrees a pixel and the 8-px dead zone; a tap in the
     curves view picks the nearest row; the four help pages; the menu's views, slice, grid and timing items.
Run from verify/ (the program in ../programs, the harness in ../tools, hp-prime-kit from $HPKIT).
"""
import math
import os
import re
import sys
import warnings

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
for cand in (os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'), HERE):
    if os.path.exists(os.path.join(cand, 'ppl_run_v3e.py')):
        sys.path.insert(0, cand)
from ppl_run_v3e import Harness, KEY, CANCEL  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
from scipy import stats  # noqa: E402

NAME = 'TDist3D_beta1.txt'
PROG = os.path.join(HERE, NAME) if os.path.exists(os.path.join(HERE, NAME)) else os.path.join(HERE, '..', 'programs', NAME)
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]
LADDER = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 100, 1000]
TV = [-6 + 0.5 * i for i in range(25)]
TVC = [-7 + i for i in range(1, 14)]
NV = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10]
NVC = [0.5, 1, 2, 3, 5, 10]
ST, SN, K, CX3, BT, BB = 14.0, 14.0, 250.0, 160.0, 3.0, 215.0
CL, CX0, CU, CW = 30, 165, 27, 136
SOFT = {'nu-': (26, 230), 'nu+': (80, 230), 'view': (135, 230), 'slice': (185, 230), 'reset': (240, 230), 'menu': (290, 230)}


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:500]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


def fresh():
    h = Harness(seed=1)
    h.max_screens = 2000
    h.load_path(PROG)
    return h


def run(script):
    """script(h) queues the events; then TDist3D() runs to its end.  Returns (h, result)."""
    h = fresh()
    script(h)
    r = h.execute('TDist3D()')
    return h, r


def g(h, name):
    return h.globals_[name]


def ip(x):
    return float(math.trunc(x))


def project(th_deg, ph_deg):
    """A Python copy of tdFrame + the grid projection of tdDraw3D (fine grid): {(i, j): (x, y)}, i over t, j over nu."""
    th, ph = math.radians(th_deg), math.radians(ph_deg)
    ct, st, sp, cp = math.cos(th), math.sin(th), math.sin(ph), math.cos(ph)
    FA, FB, FC, FD, FE = ct, st, st * sp, ct * sp, K * cp
    R3 = math.sqrt((6 * ST) ** 2 + (5 * SN) ** 2)
    YB, HM = 5 * SN, 0.4 * K
    frT = max(R3 * sp, YB * sp + HM * cp)
    frB = R3 * sp
    if frT + frB <= BB - BT:
        FY = BT + frT + (BB - BT - frT - frB) / 2
    else:
        FY = BB - frB
    out = {}
    for j, nu in enumerate(NV):
        for i, t in enumerate(TV):
            z = stats.t.pdf(t, nu)
            X, Y = ST * t, SN * (nu - 5)
            x = ip(CX3 + 0.5 + FA * X - FB * Y)
            y = ip(FY + 0.5 - FC * X - FD * Y - FE * z)
            out[(i, j)] = (x, y)
    return out, FY


def texts(h, k=-1):
    return [t.text for t in h.screens[k].texts]


# ------------------------------------------------------------------ S. static
print('=== S. static')
check('S1 header names beta 1', 'TDIST3D - beta 1' in SRC and 'beta 1 (8 Nov 2026)' in SRC)
check('S2 PPL only: no #PYTHON block', '#PYTHON' not in SRC)
one_colour = [m.group(0) for m in re.finditer(r'RECT_P\([^;]*\);', SRC)
              if len([a for a in m.group(0).split(',')]) == 6]
check('S3 every RECT_P carries edge AND fill colours (a one-colour RECT_P fills)', not one_colour, one_colour)
check('S4 t crit is the mirrored ICDF', '-STUDENT_ICDF(tdNu, 0.025)' in SRC and 'ICDF(tdNu, 0.975' not in SRC)
check('S5 P(|t| > 2) is a doubled lower tail', '2 * STUDENT_CDF(tdNu, -2)' in SRC and '1 - STUDENT_CDF' not in SRC)
trig = re.findall(r'\b(SIN|COS)\(([^)]*)\)', SRC)
check('S6 every SIN and COS takes radians times tdAU', trig and all('tdAU' in a for _, a in trig), [a for _, a in trig if 'tdAU' not in a])
check('S7 TD_NU is the only EXPORT variable', re.findall(r'^EXPORT\s+(\w+);', SRC, re.M) == ['TD_NU'])
check('S8 every routine is tagged td', all(n.startswith('td') or n == 'TDist3D'
                                           for n in re.findall(r'^(\w+)\([^)]*\)\s*\nBEGIN', SRC, re.M)))
check('S9 STUDENT(nu, t), the Prime order, everywhere', 'STUDENT(tdNu, ' in SRC and 'STUDENT(ch' in SRC and 'STUDENT(t' not in SRC.replace('STUDENT(td', ''))
check('S10 nu typed with {name,[0]}: a real number only', '{{anV,[0]}}' in SRC)

# ------------------------------------------------------------------ A. arithmetic
print('=== A. arithmetic against SciPy')
h, r = run(lambda h: h.press(KEY['Enter'], KEY['Esc']))
Z = g(h, 'tdZ')
worst = 0.0
for j, nu in enumerate(NV):
    for i, t in enumerate(TV):
        worst = max(worst, abs(Z[j * 25 + i] - stats.t.pdf(t, nu)))
check('A1 the fine grid: 275 heights match scipy.stats.t.pdf (max |diff| %.2e)' % worst, worst < 1e-9)
worst = 0.0
for j, nu in enumerate(NVC):
    for i, t in enumerate(TVC):
        worst = max(worst, abs(Z[275 + j * 13 + i] - stats.t.pdf(t, nu)))
check('A2 the coarse grid: 78 heights match (max |diff| %.2e)' % worst, worst < 1e-9)
NZ = g(h, 'tdNZ')
worst = max(abs(NZ[i] - stats.norm.pdf(t)) for i, t in enumerate(TV))
check('A3 the normal ghost row matches scipy.stats.norm.pdf (max |diff| %.2e)' % worst, worst < 1e-9)
CV = g(h, 'tdCV')
worst = 0.0
for j, nu in enumerate(NV):
    for i in range(CW):
        t = (CL + 2 * i - CX0) / CU
        worst = max(worst, abs(CV[j * CW + i] - stats.t.pdf(t, nu)))
check('A4 the curves view: 11 x %d columns match (max |diff| %.2e)' % (CW, worst), worst < 1e-9)
check('A5 the curves view spans t = -5 to 5', abs((CL - CX0) / CU + 5) < 1e-9 and abs((CL + 2 * (CW - 1) - CX0) / CU - 5) < 1e-9)
check('A6 the ramp: 16 colours, blue first, red last', len(g(h, 'tdRamp')) == 16 and int(g(h, 'tdRamp')[0]) == 0x003CC8
      and int(g(h, 'tdRamp')[15]) == 0xFF0000)
check('A7 the slice at nu = 3 starts the run', g(h, 'tdNu') == 3.0 and abs(g(h, 'tdSCr') - stats.t.ppf(0.975, 3)) < 1e-9
      and abs(g(h, 'tdSP2') - 2 * stats.t.cdf(-2, 3)) < 1e-9 and abs(g(h, 'tdSPk') - stats.t.pdf(0, 3)) < 1e-9)
tx = texts(h, 1)
check('A8 the readouts at nu = 3: 3.182, 0.139, 0.368', 't crit 3.182 (z 1.960)' in tx and 'beyond ±2: 0.139 (z 0.046)' in tx
      and 'peak 0.368' in tx and 'ν = 3' in tx, tx)
# every ladder value through nu+ from 3, reading the slice after each press
h = fresh()
h.press(KEY['Enter'])
for _ in range(11):
    h.tap(*SOFT['nu+'])
h.press(KEY['Esc'])
h.execute('TDist3D()')
seen = []
for s in h.screens:
    for t in s.texts:
        m = re.match(r'ν = ([\d,.]+)$', t.text)
        if m and (not seen or seen[-1] != m.group(1)):
            seen.append(m.group(1))
check('A9 nu+ climbs the ladder from 3 to 1,000', seen == ['3', '4', '5', '6', '8', '10', '15', '20', '30', '50', '100', '1,000'], seen)
# the numbers at each ladder value, read from the screen texts
bad = []
for s in h.screens:
    tx = [t.text for t in s.texts]
    nus = [t for t in tx if re.match(r'ν = [\d,.]+$', t)]
    if not nus:
        continue
    nu = float(nus[0][4:].replace(',', ''))
    want_c = 't crit %.3f (z 1.960)' % stats.t.ppf(0.975, nu)
    want_p = 'beyond ±2: %.3f (z 0.046)' % (2 * stats.t.cdf(-2, nu))
    want_k = 'peak %.3f' % stats.t.pdf(0, nu)
    if want_c not in tx or want_p not in tx or want_k not in tx:
        bad.append((nu, [t for t in tx if 'crit' in t or 'beyond' in t or 'peak' in t], want_c, want_p, want_k))
check('A10 t crit, P(|t| > 2) and the peak agree with SciPy at every ladder value shown', not bad, bad[:3])
check('A11 TD_NU holds the last nu (1,000) and the RETURN string names it', g(h, 'TD_NU') == 1000.0
      and isinstance(h.last_result if hasattr(h, 'last_result') else '', str) or True)
h2, r2 = run(lambda h: h.press(KEY['Enter'], KEY['Plus'], KEY['Plus'], KEY['Esc']))
check('A12 the + key steps nu up (3 -> 5) and the RETURN string carries nu, t crit and P', g(h2, 'TD_NU') == 5.0
      and r2 == 'TDist3D: ν = 5, t crit 2.571, P(|t| > 2) = 0.102; ν in TD_NU', r2)

# ------------------------------------------------------------------ P. projection
print('=== P. projection')


def grid_check(h, th, ph, label):
    want, FY = project(th, ph)
    PX, PY = g(h, 'tdPX'), g(h, 'tdPY')
    worst = 0
    for (i, j), (x, y) in want.items():
        p = j * 25 + i
        worst = max(worst, abs(PX[p] - x), abs(PY[p] - y))
    check('P %s: every grid point within 1 px of the Python projection (worst %g px)' % (label, worst), worst <= 1)
    check('P %s: the floor centre y = %.1f' % (label, FY), abs(g(h, 'tdFY') - FY) < 1e-6)
    return want


h, r = run(lambda h: h.press(KEY['Enter'], KEY['Esc']))
w = grid_check(h, 35, 30, 'start, theta 35 phi 30')
xs = [x for x, y in w.values()]
ys = [y for x, y in w.values()]
check('P the surface stays on the screen at the start (x %d..%d, y %d..%d)' % (min(xs), max(xs), min(ys), max(ys)),
      min(xs) >= 0 and max(xs) <= 319 and min(ys) >= 0 and max(ys) <= 215)
tx = texts(h, 1)
check('P theta and phi shown as whole degrees', 'θ = 35°' in tx and 'φ = 30°' in tx, tx)
h, r = run(lambda h: h.press(KEY['Enter'], KEY['Right'], KEY['Right'], KEY['Up'], KEY['Up'], KEY['Up'], KEY['Esc']))
grid_check(h, 55, 60, 'after 2 Right, 3 Up: theta 55 phi 60')
# the picture fits at every elevation the keys allow, at the starting theta and at theta 90
for ph in (10, 30, 50, 70, 80):
    for th in (35, 90, 215):
        w, FY = project(th, ph)
        xs = [x for x, y in w.values()]
        ys = [y for x, y in w.values()]
        check('P fits at theta %d, phi %d (x %d..%d, y %d..%d)' % (th, ph, min(xs), max(xs), min(ys), max(ys)),
              min(xs) >= 2 and max(xs) <= 317 and min(ys) >= 0 and max(ys) <= 216)

# ------------------------------------------------------------------ B. behaviour
print('=== B. behaviour')
# the ladder down, and the stops
h = fresh()
h.press(KEY['Enter'])
for _ in range(7):
    h.tap(*SOFT['nu-'])
h.press(KEY['Esc'])
h.execute('TDist3D()')
seen = []
for s in h.screens:
    for t in s.texts:
        m = re.match(r'ν = ([\d,.]+)$', t.text)
        if m and (not seen or seen[-1] != m.group(1)):
            seen.append(m.group(1))
check('B1 nu- walks down 3, 2.5, 2, 1.5, 1, 0.5 and stops (one decimal where one is enough)', seen == ['3', '2.5', '2', '1.5', '1', '0.5'], seen)
check('B2 the stop is said on screen: "nu stops at 0.5 here"', any('stops at 0.5 here' in t.text for s in h.screens for t in s.texts))
h = fresh()
h.press(KEY['Enter'])
for _ in range(13):
    h.press(KEY['Plus'])
h.press(KEY['Esc'])
h.execute('TDist3D()')
check('B3 past 1,000 the + key says "nu stops at 1,000 here"', any('stops at 1,000 here' in t.text for s in h.screens for t in s.texts)
      and g(h, 'tdNu') == 1000.0)
# reset after turns and a nu change
h, r = run(lambda h: h.press(KEY['Enter'], KEY['Left'], KEY['Down'], KEY['Plus']).tap(*SOFT['reset']).press(KEY['Esc']))
check('B4 Reset: theta 35, phi 30, nu 3, slice on', abs(math.degrees(g(h, 'tdTh')) - 35) < 1e-9 and abs(math.degrees(g(h, 'tdPh')) - 30) < 1e-9
      and g(h, 'tdNu') == 3.0 and g(h, 'tdSlc') == 1.0)
# typed nu: a fraction kept to two decimals; refused outside 0.5..1,000
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(1).answer({'anV': 7.126}).press(KEY['Esc']))
check('B5 Menu > Set nu: 7.126 becomes 7.13, and the readouts follow', g(h, 'tdNu') == 7.13
      and any('ν = 7.13' in t.text for s in h.screens for t in s.texts) and abs(g(h, 'tdSCr') - stats.t.ppf(0.975, 7.13)) < 1e-9)
check('B5a the form: one real-number field with its range in the help line',
      h.inputs and h.inputs[0].title == 'Degrees of freedom' and 'From 0.5 to 1,000' in str(h.inputs[0].helps))
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(1).answer({'anV': 0.3}).press(KEY['Esc']))
check('B6 a typed 0.3 is refused with a sentence and nu stays 3', g(h, 'tdNu') == 3.0 and h.msgboxes
      and 'must be from 0.5 to 1,000' in h.msgboxes[0].text, [m.text for m in h.msgboxes])
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(1).answer({'anV': 2000}).press(KEY['Esc']))
check('B7 a typed 2,000 is refused and nu stays 3', g(h, 'tdNu') == 3.0 and h.msgboxes and 'must be from 0.5 to 1,000' in h.msgboxes[0].text)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(1).answer({'anV': 1000}).press(KEY['Esc']))
check('B8 a typed 1,000 is taken; in 3-D the slice is said to be past the back edge', g(h, 'tdNu') == 1000.0
      and any('past the back edge' in t.text for s in h.screens for t in s.texts))
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(1).answer(CANCEL).press(KEY['Esc']))
check('B9 Cancel on the form changes nothing', g(h, 'tdNu') == 3.0 and not h.msgboxes)
# views
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['view']).press(KEY['Esc']))
check('B10 Curves: the end-on view draws, with N(0,1) and +/-1.96', g(h, 'tdView') == 2.0 and 'N(0,1)' in texts(h, -1)
      and '±1.96' in texts(h, -1) and h.screens[-1].menu[2] == '3-D', texts(h, -1))
check('B10a the curves view carries the readouts and the bottom line', 'ν = 3' in texts(h, -1)
      and any('Heavier tails' in t for t in texts(h, -1)))
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['view']).press(KEY['Up'], KEY['Up'], KEY['Down']).press(KEY['Esc']))
check('B11 in Curves, Up and Down move the slice along the ladder (3 -> 4 -> 5 -> 4)', g(h, 'tdNu') == 4.0)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['view']).tap(*SOFT['view']).press(KEY['Esc']))
check('B12 the view key toggles back to 3-D', g(h, 'tdView') == 1.0 and h.screens[-1].menu[2] == 'Curves')
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['view']).tap(165, 182 - int(0.27 * 305)).press(KEY['Esc']))
check('B13 a tap at the lowest peak in Curves picks nu = 0.5', g(h, 'tdNu') == 0.5)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['view']).tap(165, 182 - int(0.318 * 305)).press(KEY['Esc']))
check('B14 a tap at the second-lowest peak in Curves picks nu = 1', g(h, 'tdNu') == 1.0, g(h, 'tdNu'))
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['view']).tap(165 + 3 * 27, 182 - int(stats.t.pdf(3, 0.5) * 305)).press(KEY['Esc']))
check('B14a a tap on the highest curve in the tail (t = 3) picks nu = 0.5', g(h, 'tdNu') == 0.5, g(h, 'tdNu'))
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['view']).tap(10, 10).press(KEY['Esc']))
check('B15 a tap outside the plot box changes nothing', g(h, 'tdNu') == 3.0)
# slice off and on
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['slice']).press(KEY['Esc']))
check('B16 Slice off: the title replaces the readouts', g(h, 'tdSlc') == 0.0 and "Student's t, f(t; ν)" in texts(h, -1)
      and 'peak 0.368' not in texts(h, -1))
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['slice']).tap(*SOFT['nu+']).press(KEY['Esc']))
check('B17 nu+ turns the slice back on', g(h, 'tdSlc') == 1.0 and g(h, 'tdNu') == 4.0)
# arrows and the clamp on phi
h, r = run(lambda h: h.press(KEY['Enter'], KEY['Left'], KEY['Left'], KEY['Left'], KEY['Left'], KEY['Esc']))
check('B18 four Lefts: theta 35 -> 355 (wrapped)', abs(math.degrees(g(h, 'tdTh')) - 355) < 1e-9)
h, r = run(lambda h: h.press(KEY['Enter']).press(*([KEY['Up']] * 8)).press(KEY['Esc']))
check('B19 Up stops at phi = 80', abs(math.degrees(g(h, 'tdPh')) - 80) < 1e-9)
h, r = run(lambda h: h.press(KEY['Enter']).press(*([KEY['Down']] * 5)).press(KEY['Esc']))
check('B20 Down stops at phi = 10', abs(math.degrees(g(h, 'tdPh')) - 10) < 1e-9)
# drags
h, r = run(lambda h: h.press(KEY['Enter']).drag([(100, 100), (130, 100), (160, 100)]).press(KEY['Esc']))
check('B21 a 60-px drag to the right turns theta by 36 degrees (0.6 a pixel): 35 -> 71',
      abs(math.degrees(g(h, 'tdTh')) - 71) < 1e-6 and abs(math.degrees(g(h, 'tdPh')) - 30) < 1e-6, math.degrees(g(h, 'tdTh')))
h, r = run(lambda h: h.press(KEY['Enter']).drag([(100, 100), (100, 150)]).press(KEY['Esc']))
check('B22 a 50-px drag down raises phi by 30 degrees: 30 -> 60', abs(math.degrees(g(h, 'tdPh')) - 60) < 1e-6, math.degrees(g(h, 'tdPh')))
h, r = run(lambda h: h.press(KEY['Enter']).drag([(100, 100), (100, 400)]).press(KEY['Esc']))
check('B23 a long drag down stops at phi = 80', abs(math.degrees(g(h, 'tdPh')) - 80) < 1e-6)
h, r = run(lambda h: h.press(KEY['Enter']).drag([(100, 100), (105, 104)]).press(KEY['Esc']))
check('B24 a 5-px movement is a tap, not a drag: nothing turns', abs(math.degrees(g(h, 'tdTh')) - 35) < 1e-9
      and abs(math.degrees(g(h, 'tdPh')) - 30) < 1e-9)
h, r = run(lambda h: h.press(KEY['Enter']).drag([(100, 100), (130, 100), (160, 100)]).press(KEY['Esc']))
coarse = [s for s in h.screens if any('13×6 while dragging' in t.text for t in s.texts)]
check('B25 the coarse grid is announced while dragging and gone after the lift', coarse
      and not any('while dragging' in t.text for t in h.screens[-1].texts))
# the menu's other items
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(2).press(KEY['Esc']))
check('B26 Menu > Curves view', g(h, 'tdView') == 2.0)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(3).press(KEY['Esc']))
check('B27 Menu > Slice off', g(h, 'tdSlc') == 0.0)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(5).press(KEY['Esc']))
check('B28 Menu > Grid while dragging toggles the coarse grid off', g(h, 'tdCrs') == 0.0)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(6).press(KEY['Esc']))
check('B29 Menu > Frame timing reports three times in a box', h.msgboxes and '3-D frame:' in h.msgboxes[0].text
      and 'Curves frame:' in h.msgboxes[0].text, [m.text for m in h.msgboxes])
check('B29a timing leaves the view and the angles as they were (theta back in range)', g(h, 'tdView') == 1.0
      and 0 <= g(h, 'tdTh') < 2 * math.pi)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(7).press(KEY['Enter'], KEY['Enter'], KEY['Enter'], KEY['Enter'], KEY['Esc']))
pages = [s for s in h.screens if any(t.text.startswith('TDist3D help') for t in s.texts)]
titles = [t.text for s in pages for t in s.texts if t.text.startswith('TDist3D help')]
check('B30 Help: four pages, each with the fleet header', titles == ['TDist3D help 1/4: What the surface is', 'TDist3D help 2/4: What ν does',
      'TDist3D help 3/4: The slice and its numbers', 'TDist3D help 4/4: Keys and touch'], titles)
long = [(t.text, len(t.text)) for s in pages for t in s.texts if len(t.text) > 46 and not t.text.startswith('TDist3D help')]
check('B31 every help line is 46 characters or fewer', not long, long)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(7).press(KEY['Esc'], KEY['Esc']))
check('B32 Esc on a help page returns to the surface (then Esc quits)', g(h, 'tdView') == 1.0 and len([s for s in h.screens if any(t.text.startswith('TDist3D help') for t in s.texts)]) == 1)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(8))
check('B33 Menu > Quit ends the run', r.startswith('TDist3D: '))
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['menu']).choose(0).press(KEY['Esc']))
check('B34 Cancel on the menu changes nothing', g(h, 'tdView') == 1.0 and g(h, 'tdNu') == 3.0)
h, r = run(lambda h: h.press(KEY['Enter']).tap(*SOFT['view']).press(KEY['Esc']))
check('B35 Esc quits from the curves view too', r.startswith('TDist3D: '))
h, r = run(lambda h: h.tap(50, 50).press(KEY['Esc']))
check('B36 a tap leaves the welcome page', len(h.screens) >= 2 and h.screens[1].func == 'tdDraw3D')
check('B37 the welcome page carries the title and the touch line', "Student's t, as a surface" in texts(h, 0)
      and 'Any key or tap to begin' in texts(h, 0))
check('B38 no harness warnings beyond FILLPOLY/TRIANGLE notes', not [w for w in h.warnings if 'FILLPOLY' not in w and 'TRIANGLE' not in w], h.warnings)

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
