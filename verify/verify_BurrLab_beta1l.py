#!/usr/bin/env python3
"""verify_BurrLab_beta1l.py -- checks BurrLab beta 1l (2 Nov 2026, night): a y axis you can see.
Roger, beta 1k on the Virtual Calculator: "IN Burr, Explore...is there a y-axis?  If so I can't see it--there is a
number in the upper left of the white area of the plot just under the orange ribbon, but I dont know what that's for".
beta 1k's y axis was the plot box's left edge in the grid's pale grey, with "0" and the axis's top value (written
above the box, no tick, no name) as its only numbers.  beta 1l's bu_YAxis draws a dark axis, two to four 1-2-5 ticks
with grid lines and numbers, "0", and the axis's name, on every plot page.
  G  static: only the plot routines, the x-axis label routines (bu_TickLbl, bu_XAxis) and the title page differ from
     beta 1k, and bu_LWd, bu_LogY and bu_YAxis are new;
     the numbers of bu_YAxis are never cut (TEXTOUT_P's width 36 against a 28 px limit), STRING(x, 2, d) only for
     d up to 12, and a fixed form that comes out scientific is never drawn.
  G7 every menu item at most 30 characters (Roger: "some of the menu items run out of the box").
  Y1 bu_YAxis alone, at 400 axis tops from 1E-12 to 1E14: every number it writes is its tick's value, level with
     its tick, at most 28 px wide, 2 px or more from the screen's edge and clear of the ticks, grouped with
     commas, never scientific; when plain numbers would not fit, the axis counts in units of a power of ten
     ("pdf (×0.0001)" over 2, 4, 6, 8: whole numbers, the unit in the name); none against the name; two to four
     ticks above 0.
  Y2 Explore at C and K in {0.2, 0.5, 1, 2, 5, 20, 50} and S in {0.01, 1, 10, 1000}: the pdf view shows "pdf"
     above the axis and its tick numbers, never beta 1k's lone top value or "pdf" at the foot; the CDF view has no
     numbers left of the axis; no text over another or cut (tools/text_overlap_v1, tools/label_fit_v1).
  Y3 the other pages on the three presets (Family, How rare is this?, Histogram linear and log, Q-Q, Survival,
     Hazard, The mean that never settles): each shows its axis's name and tick numbers, nothing over anything,
     nothing cut.
  Y4 x-axis labels: none touches the one before it (bu_XAxis on Family's narrow plot and the wide one, 300 ranges
     each; Explore's own row; Family at S = 1,000, where the Virtual Calculator showed "1,0002,0003,000").  And
     Explore's grey row at C = 0.2, K = 20, S = 0.01 keeps its SD whole (its note "(C <= 1)" makes room).
  Overlap rule: tools/text_overlap_v1 calls a finding firm "when it survives the narrower measured glyph widths
     too", but judges only right-edge straddles at those widths; a left-edge one is always firm.  Here a left-edge
     straddle is judged at the measured widths as well (tools/label_fit_v1.measure: 5.5 px a character in font 1,
     3 px a decimal point; Lessons Learned): the y numbers end 2 px short of their ticks at those widths, and the
     Virtual Calculator showed the gap (Explore, default and S = 1,000).
  R  the monkey, 30 seeds on both versions (tools/comma_check_v1.py): the same path, the same texts to the CAS,
     every big number grouped, no year grouped, no new overlap or cut number.
Run from verify/ as it is.  Beta 1k is verify/BurrLab_beta1k.txt: it was never committed (beta 1l replaced it
the same night), so git history does not hold it.
    python3 verify_BurrLab_beta1l.py [BurrLab_beta1k.txt]
"""
import glob
import math
import os
import random
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
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
prime_facts_v1.apply()
_ANALYSE = OV.analyse_screen


def _analyse_measured(d):
    """text_overlap_v1.analyse_screen, with a left-edge straddle judged at the measured widths as a right-edge one
    is (see the docstring's Overlap rule)."""
    coll, strad, over, ghosts = _ANALYSE(d)
    fonts = {(it['text'], it['x'], it['y']): it['font'] for it in d['items'] if 'text' in it}
    out = []
    for (txt, x, y, which, by, firm) in strad:
        if firm and which == 'left':
            firm = x + LF.measure(txt, fonts.get((txt, x, y), 1)) > x + by
        out.append((txt, x, y, which, by, firm))
    return coll, out, over, ghosts


OV.analyse_screen = _analyse_measured
NAME, OLDNAME = 'BurrLab_beta1l.txt', 'BurrLab_beta1k.txt'
PROG = os.path.join(HERE, NAME) if os.path.exists(os.path.join(HERE, NAME)) else os.path.join(HERE, '..', 'programs', NAME)
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]
PL, PR, PT, PB = 36, 304, 36, 153
SCI = 'ᴇ'


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:600]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


def older(name):
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


OLD = older(OLDNAME)
print('=== BurrLab beta 1l against beta 1k ({})'.format(os.path.relpath(OLD, HERE) if OLD else 'NOT FOUND'))
if not OLD:
    check('the older version found', False)
    sys.exit(1)
OSRC = open(OLD, encoding='utf-8').read()

# ------------------------------------------------------------------ G
print('=== G. static')
ro, rn = CC.routines(CC.strip_comments(OSRC)), CC.routines(CC.strip_comments(SRC))
diff = sorted(r for r in set(ro) | set(rn) if ro.get(r) != rn.get(r))
WANT = ['BurrLab', 'bu_DrawFam', 'bu_DrawRare', 'bu_ExBase', 'bu_ExFrame', 'bu_FitMenu', 'bu_HazPage', 'bu_Hist', 'bu_LWd',
        'bu_LogY',
        'bu_Opening', 'bu_QQ', 'bu_SimFrame', 'bu_Surv', 'bu_TickLbl', 'bu_XAxis', 'bu_YAxis']
check('G1 only the plot routines, bu_TickLbl, bu_XAxis, the two menus\' routines and the title page differ from '
      'beta 1k; bu_LWd, bu_LogY and '
      'bu_YAxis are new: %s' % diff, diff == WANT and not {'bu_YAxis', 'bu_LWd', 'bu_LogY'} & set(ro), diff)
check('G2 the header names beta 1l, the title page too', '// BurrLab - beta 1l' in SRC and
      '"BurrLab beta 1l: the long right tail"' in SRC and '"BurrLab beta 1k: the long right tail"' not in SRC)
check('G3 no new "!=" and nothing new for the CAS', SRC.count('!=') == OSRC.count('!=') and
      SRC.count('bu_Cas(') == OSRC.count('bu_Cas('))
ya = rn['bu_YAxis']
tx = re.findall(r'TEXTOUT_P\(yaS, G[14], yaX, yaY - 5, 1, buGRAY, (\d+)\)', ya)
check('G4 bu_YAxis: each number drawn only when at most 28 px wide, with width %s (never cut); fixed decimals '
      'only up to 12, and never one that comes out scientific' % tx, tx == ['36', '36'] and
      ya.count('IF yaW <= 28 AND yaY >= buPT + 4 THEN') == 2 and 'IF yaD > 12 THEN yaU := 1; END;' in ya and
      ya.count('bu_Fx(') == 2 and 'INSTRING(yaS, CHAR(7431)) > 0 THEN yaU := 1' in ya)
calls = [r for r in rn if r != 'bu_YAxis' and 'bu_YAxis(' in rn[r]]
first = {r: re.search(r'^' + r + r'\(', SRC, re.M).start() for r in calls + ['bu_YAxis', 'bu_Nice', 'bu_Fx',
                                                                            'bu_Cm', 'bu_LWd', 'bu_Pow10',
                                                                            'bu_IStr']}
lcalls = [r for r in rn if r != 'bu_LogY' and 'bu_LogY(' in rn[r]]
tcalls = [r for r in rn if r != 'bu_TickLbl' and 'bu_TickLbl(' in rn[r]]
first.update({r: re.search(r'^' + r + r'\(', SRC, re.M).start() for r in lcalls + tcalls + ['bu_LogY', 'bu_TickLbl']})
check('G6 bu_LogY comes before its callers %s and after bu_LWd; every call of bu_TickLbl (%s) passes and keeps where '
      'the row\'s last label ends' % (lcalls, tcalls), sorted(lcalls) == ['bu_QQ', 'bu_Surv'] and
      all(first[r] > first['bu_LogY'] for r in lcalls) and first['bu_LogY'] > first['bu_LWd'] and
      sorted(tcalls) == ['bu_Hist', 'bu_QQ', 'bu_Surv', 'bu_XAxis'] and
      all(len(re.findall(r'(\w+) := bu_TickLbl\([^;]*, \1\);', rn[r])) == rn[r].count('bu_TickLbl(') for r in tcalls))
items = []
for m_ in re.finditer(r'CHOOSE\s*\(', CC.strip_comments(SRC)):
    t_ = CC.strip_comments(SRC)[m_.end() - 1:]
    d_, q_ = 0, False
    for j_, ch in enumerate(t_):
        if ch == '"':
            q_ = not q_
        elif not q_ and ch in '([{':
            d_ += 1
        elif not q_ and ch in ')]}':
            d_ -= 1
            if d_ == 0:
                break
    items += re.findall(r'"([^"]*)"', t_[:j_ + 1])[1:]
longest = max(items, key=len)
check('G7 every menu item at most 30 characters (Roger: "some of the menu items run out of the box"; the box shows '
      'about 30, round 2\'s rule): %d items, the longest %d ("%s")' % (len(items), len(longest), longest),
      len(longest) <= 30 and 'Family: Lomax, Fisk, Weibull' in items and 'Danish fire: 2,156 in bins' in items)
check('G5 bu_YAxis comes before its %d callers and after what it calls (BurrLab declares nothing ahead)'
      % len(calls), all(first[r] > first['bu_YAxis'] for r in calls) and
      all(first[r] < first['bu_YAxis'] for r in ('bu_Nice', 'bu_Fx', 'bu_Cm', 'bu_LWd', 'bu_Pow10', 'bu_IStr'))
      and len(calls) == 7)


# ------------------------------------------------------------------ Y1
def lwd(s):
    return 5.5 * (len(s) - 1) + 3 if '.' in s else 5.5 * len(s)


def val(s):
    s = s.replace(',', '').replace('−', '-')
    if SCI in s:
        m, e = s.split(SCI)
        return float(m) * 10 ** int(e)
    return float(s)


def nice(v):
    e = math.floor(math.log10(v))
    f = v / 10 ** e
    r = 10 if f > 5 else 5 if f > 2 else 2 if f > 1 else 1
    return r * 10 ** e


print('=== Y1. bu_YAxis alone, 400 axis tops')
h = Harness(PROG, idle_key=4)
h.execute('bu_Init()')
rng = random.Random(7)
tops = [10 ** rng.uniform(-12, 14) for _ in range(360)]
for e in range(-9, 13, 3):
    for m in (1, 2, 5):
        tops += [m * 10 ** e, m * 1.08 * 10 ** e]
tops = tops[:400]
bad, forms, left_out, nt = [], {'plain': 0, 'units': 0}, 0, set()
for top in tops:
    h.grobs['G1'].items = []
    h.execute('bu_YAxis(1, %r, "pdf", buBLUE)' % top)
    items = h.grobs['G1'].items
    T = [t for t in items if t.__class__.__name__ == 'Text']
    ticks = sorted(s.args[1] for s in items if s.__class__.__name__ == 'Shape' and s.cmd == 'LINE_P'
                   and s.args[0] == PL - 3 and s.args[2] == PL)
    nums = [t for t in T if float(t.x) < PL and float(t.y) != PT - 14]
    name = [t for t in T if t.text.startswith('pdf') and float(t.x) == 1 and float(t.y) == PT - 14]
    stp = nice(top / 5)
    k = int(top / stp - 1e-9) if abs(top / stp - round(top / stp)) < 1e-9 else int(top / stp)
    want_ticks = sorted(PB - int(i * stp / top * (PB - PT) + 0.5) for i in range(0, k + 1) if i * stp < top)
    nt.add(len(want_ticks) - 1)
    if not name or ticks != want_ticks:
        bad.append((top, 'ticks', ticks, want_ticks))
        continue
    ttl = name[0].text
    unit = 1.0
    if ttl != 'pdf':                                      # units: "pdf (×0.0001)", "pdf (×1,000)", "pdf (×1ᴇ−15)"
        m_ = re.fullmatch(r'pdf \(\u00d7(.+)\)', ttl)
        unit = val(m_.group(1)) if m_ else None
        e_ = math.floor(math.log10(stp) + 1e-6)
        if unit is None or abs(unit / 10 ** e_ - 1) > 1e-9:
            bad.append((top, 'unit', ttl, e_))
            continue
    forms['units' if ttl != 'pdf' else 'plain'] += 1
    for t in nums:
        if t.text == '0':
            if float(t.y) != PB - 5:
                bad.append((top, 'zero', t.y))
            continue
        v = val(t.text) * unit
        i = round(v / stp)
        y = PB - int(i * stp / top * (PB - PT) + 0.5)
        w = lwd(t.text)
        grouped = all(len(r) <= 3 for r in re.findall(r'\d+', t.text.split('.')[0].replace(',', ' ')))
        if (abs(v - i * stp) > 1e-9 * max(stp, v) or float(t.y) != y - 5 or w > 28 or float(t.x) < 2 or
                float(t.x) + w > PL - 5 or float(t.y) < PT - 1 or SCI in t.text or not grouped or
                (unit != 1.0 and not re.fullmatch(r'\d+', t.text))):
            bad.append((top, ttl, t.text, t.x, t.y, w))
    left_out += (len(want_ticks) - 1) - sum(1 for t in nums if t.text != '0')
check('Y1 400 tops: every number (times its unit) its tick\'s value, level with it, <= 28 px, 2 px or more from '
      'the edge, grouped, never scientific; in units, whole numbers and the unit in the name; ticks above 0: %s; '
      'axes in plain numbers %d, in units %d; numbers left out (at the top): %d'
      % (sorted(nt), forms['plain'], forms['units'], left_out), not bad and nt <= {1, 2, 3, 4}, bad[:4])
h.grobs['G1'].items = []
h.execute('bu_YAxis(1, 0.093, "pdf", buBLUE)')
ex = sorted((float(t.y), t.text) for t in h.grobs['G1'].items if t.__class__.__name__ == 'Text')
print('   e.g. top 0.093 (Explore\'s default):', [s for _, s in ex])
h.grobs['G1'].items = []
h.execute('bu_YAxis(1, 0.00004, "pdf", buBLUE)')
ex = sorted((float(t.y), t.text) for t in h.grobs['G1'].items if t.__class__.__name__ == 'Text')
print('   e.g. top 0.00004:', [s for _, s in ex])
h.grobs['G1'].items = []
h.execute('bu_YAxis(1, 0.00093, "pdf", buBLUE)')
ex = sorted((float(t.y), t.text) for t in h.grobs['G1'].items if t.__class__.__name__ == 'Text')
print('   e.g. top 0.00093 (Explore at S = 1,000):', [s for _, s in ex])
h.grobs['G1'].items = []
h.execute('bu_YAxis(1, 2.4E13, "running mean", buGRAY)')
ex = sorted((float(t.y), t.text) for t in h.grobs['G1'].items if t.__class__.__name__ == 'Text')
print('   e.g. top 2.4E13:', [s for _, s in ex])


# ------------------------------------------------------------------ Y2
def screen_findings(scr):
    d = OV.digest_screen(scr)
    coll, strad, over, ghosts = OV.analyse_screen(d)
    cut = [t.text for t in scr.texts if LF.hidden_tail(t.text, OV._font(t.font), t.width)]
    return [c for c in coll if c[-1]], [s for s in strad if s[-1]], [o for o in over if o[-1]], cut


print('=== Y2. Explore over C, K and S')
vals = (0.2, 0.5, 1, 2, 5, 20, 50)
bad2, nonum, n2, ov2 = [], [], 0, []
for S in (0.01, 1, 10, 1000):
    for C in vals:
        for K in vals:
            for view in (0, 1):
                h = Harness(PROG, idle_key=4)
                h.execute('bu_Init()')
                g = h.globals_
                g['buC'], g['buK'], g['buS'], g['buView'] = float(C), float(K), float(S), float(view)
                g['buX0'] = float(S)
                h.execute('bu_Explore()')                # draws once, then Esc ends it
                scr = [s_ for s_ in h.screens if s_.reason == 'blit'][0]
                left = [t for t in scr.texts if float(t.x) < PL and PT - 2 <= float(t.y) <= PB]
                top = [t for t in scr.texts if float(t.y) == PT - 14]
                foot = [t for t in scr.texts if t.text == 'pdf' and float(t.y) == PB - 13]
                n2 += 1
                if view == 0:
                    if len(top) != 1 or not top[0].text.startswith('pdf') or foot or not any(t.text == '0' for t in left):
                        bad2.append((C, K, S, 'pdf view', [t.text for t in top], len(foot)))
                    if not [t for t in left if t.text != '0']:
                        nonum.append((C, K, S))
                elif left or top:
                    bad2.append((C, K, S, 'CDF view', [t.text for t in left + top]))
                f = screen_findings(scr)
                if any(f):
                    ov2.append((C, K, S, view, f))
check('Y2 %d Explore screens: the pdf view names its axis "pdf" above it and writes its ticks, no lone top value, '
      'no "pdf" at the foot; the CDF view writes nothing left of the axis' % n2, not bad2, bad2[:4])
check('Y2 every pdf view writes at least one tick number above 0 (%d without)' % len(nonum), not nonum, nonum[:6])
check('Y2 no text over another, over the frame or past the screen, and nothing cut', not ov2, ov2[:3])

# ------------------------------------------------------------------ Y3
print('=== Y3. the other pages on the three presets')
PAGES = [('bu_Family()', 'pdf', 'bu_DrawFam'), ('bu_Rare()', 'pdf', 'bu_DrawRare'),
         ('bu_HistPage()', 'density', 'bu_Hist'), ('bu_QQ()', 'data quantile', 'bu_QQ'),
         ('bu_Surv()', 'survival P(X > x) (log)', 'bu_Surv'), ('bu_HazPage()', 'hazard h(x)', 'bu_HazPage'),
         ('bu_Sim()', 'running mean', 'bu_SimFrame')]
seen, bad3, ov3 = {}, [], []
for loader in ('bu_LoadBJS()', 'bu_LoadRossi()', 'bu_LoadDan300()'):
    for call, nm, fn in PAGES:
        for _ in (0,):
            h = Harness(PROG, idle_key=4, cas='fail')
            h.execute('bu_Init()')
            h.execute(loader)
            h.execute('bu_Fit()')
            if call == 'bu_HistPage()':
                h.press(50)                      # + on the Histogram page: the other scale, then Esc
            try:
                h.execute(call)
            except Exception as e:
                bad3.append((loader, call, 'error', str(e)[:120]))
                continue
            scrs = [s for s in h.screens if any(float(t.y) == PT - 14 and t.text.startswith(nm) for t in s.texts)]
            if not scrs:
                bad3.append((loader, call, 'no screen with the name', nm))
                continue
            for scr in scrs:
                ttl = [t.text for t in scr.texts if float(t.y) == PT - 14]
                nums = [t.text for t in scr.texts if float(t.x) < PL and PT - 2 <= float(t.y) <= PB]
                seen.setdefault((call, ttl[0]), 0)
                seen[(call, ttl[0])] += 1
                if (('(log)' in ttl[0] and not nums) or
                        ('(log)' not in ttl[0] and ('0' not in nums or len(nums) < 2))):
                    bad3.append((loader, call, ttl, nums))
                f = screen_findings(scr)
                if any(f):
                    ov3.append((loader, call, f))
print('   screens with each axis name:', sorted((k[1], v) for k, v in seen.items()))
check('Y3 each page names its axis and writes "0" and tick numbers (on log scales: its powers of ten): '
      '%d names' % len({k[1] for k in seen}), not bad3 and len({k[1] for k in seen}) >= 8, bad3[:4])
check('Y3 no text over another, over the frame or past the screen, and nothing cut', not ov3, ov3[:3])

# ------------------------------------------------------------------ Y4
print('=== Y4. x-axis labels')
bad4, n4 = [], 0
rng = random.Random(11)
for pr in (200, 304):
    h = Harness(PROG, idle_key=4)
    h.execute('bu_Init()')
    h.globals_['buPR'] = float(pr)
    for _ in range(300):
        xm = 10 ** rng.uniform(-6, 6)
        h.grobs['G1'].items = []
        h.execute('bu_XAxis(%r, buPB, 0)' % xm)
        row = sorted((float(t.x), t.text) for t in h.grobs['G1'].items if t.__class__.__name__ == 'Text')
        n4 += 1
        if not row or val(row[0][1]) != 0:
            bad4.append((pr, xm, 'no 0', row[:2]))
        for (x1, t1), (x2, t2) in zip(row, row[1:]):
            if x2 < x1 + int(6.5 * len(t1)) + 3:
                bad4.append((pr, xm, t1, t2))
check('Y4 bu_XAxis, %d ranges on the narrow (Family) and the wide plot: the 0 label always, and no label within 3 px of the '
      'one before it' % n4, not bad4, bad4[:4])
h = Harness(PROG, idle_key=4)
h.execute('bu_Init()')
h.globals_['buS'] = 1000.0
h.execute('bu_Family()')
scr = [s_ for s_ in h.screens if s_.reason == 'blit'][0]
row = sorted((float(t.x), t.text) for t in scr.texts if float(t.y) == PB + 3)
f = screen_findings(scr)
check('Y4 Family at S = 1,000: the x labels %s, none over another, nothing over anything' % [t for _, t in row],
      len(row) >= 3 and not any(f), f)
h = Harness(PROG, idle_key=4)
h.execute('bu_Init()')
g = h.globals_
g['buC'], g['buK'], g['buS'] = 0.2, 20.0, 0.01
h.execute('bu_Explore()')
scr = [s_ for s_ in h.screens if s_.reason == 'blit'][0]
row = sorted((float(t.x), t.text) for t in scr.texts if float(t.y) == PB + 3)
f = screen_findings(scr)
rowb = [t.text for t in scr.texts if float(t.y) == 180]
check('Y4 Explore at C = 0.2, K = 20, S = 0.01 (beta 1k drew "0.000020" over "0.000025" and cut "SD < 0.0001" off its '
      'grey row): %s; the row now %s; nothing over anything, nothing cut' % ([t for _, t in row], rowb),
      len(row) >= 3 and not any(f) and rowb and rowb[0].endswith('SD < 0.0001') and '(C' not in rowb[0], f)

# ------------------------------------------------------------------ R
print('=== R. the monkey, 30 seeds on both versions')
RES = CC.runs(OLD, PROG, 'BurrLab()', 30, 30, 'beta 1k|beta 1l', None)
for nm, ok, det in CC.report(RES, {}, (), {}):
    if ok is None:
        print('INFO ' + nm)
    else:
        check(nm, ok, det)
print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
