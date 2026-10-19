#!/usr/bin/env python3
"""verify_CICatcher_beta2c.py -- CICatcher beta 2c (19 Oct 2026): the fleet review's C-C1 and C-C2.
Built from verify_CICatcher_beta2b.py; every check is kept and now runs in harness v3e (out/ppl_run_v3e.py;
with home_minus off, as here, it prints exactly what v3d printed).  Changed (2c):
  - E's "help page 4 shown, with its engine line" now expects "exact ends: bisection on BINOMIAL_CDF,
    checked": the old expected text, "(checked)", 47 characters, WAS the C-C2 finding.
  - R3's "every CHOOSE line is 28 characters or fewer" no longer excepts the main menu's first line
    ("New setup: interval, population, n", 34): that exception WAS the C-C1 finding.
  - The section that compared beta 2b with beta 2a (G 2b) now compares those two files, as the record of
    2b; G 2c (new) compares beta 2c with beta 2b.
  - Predecessor files (beta 2b, 2a, 2, and beta 1's verify_CICatcher.py) are looked for beside this
    script, then in its _old and _superseded* folders, then in /home/claude/work/out; a check that needs
    one that is not found prints SKIP and is not counted (review item 22: the 2b script stopped with
    FileNotFoundError in a folder holding only the current versions).
New (2c), after S:
  X1 the review's regressions, inline: check_CICatcher.py's E2 (every CHOOSE item fits, <= 31) and a
     stricter E3 (every fixed help-page string <= 46, the header's own limit), on beta 2c and on 2b
     (2b fails both: 34 and 47 characters);
  X2 C-C1 in a run: the main menu shows "New: interval, population, n" and item 1 still opens the setup
     ("Which interval?"), and Cancel keeps the run; every CHOOSE line shown is 28 characters or fewer;
  X3 C-C2 as drawn: help page 4's last line is "exact ends: bisection on BINOMIAL_CDF, checked" (46), and
     every line of all six help pages, as drawn, is 46 characters or fewer, with the BINOMIAL check
     passing and failing; beta 2b drew one 47-character line;
  X4 the review's own check_CICatcher.py, run on beta 2c (every check passes) and on beta 2b (E2 fails,
     nothing else), when it is found;
  G2c beta 2c against beta 2b: only cqMenu and cqXEngS differ, each by exactly its one string.
(The beta 2b description follows; "v3d" there now means v3e.)

verify_CICatcher_beta2b.py -- CICatcher beta 2b (17 Oct 2026): the round-2 emulator fixes.
Built from verify_CICatcher_beta2a.py; every check is kept and now runs in harness v3d (out/ppl_run_v3d.py),
which raises "Invalid input" for INSTRING("", ...) and prints small fixed decimals the Prime's way
(h.sci_strings).  Beta 1's suite (F) runs in v3d too.  New (2b), after F:
  R1 cqCas with the CAS failing returns "" with no error (beta 2a stops on INSTRING("", "undef"));
     with Giac the closed form is kept and undef / infinity refused.
  R2 the E session with cas='fail' (Exact, +50, the 0-yes line, the level drag, Up, Help, Quit) runs to
     Quit with the "decimal" badge; beta 2a in v3d stops in the same session.
  R3 the setup menu's Exact line is "Proportion: Exact (C-P)" and every CHOOSE line fits (the main
     menu's 34-character first line, shown in full on the emulator, excepted); item 5 still sets Exact.
  R4 fixed decimals: five setups that reach tiny interval ends, estimates and typed parameters, with
     +50 twice, eight picked lines, a level drag and the keys, both CAS modes: no scientific STRING in
     beta 2b; beta 2a's are listed.  R5: cqF, cqNumS, cqPct on edge values.
  G  beta 2b against beta 2a: only cqCas, cqF, cqNumS, cqPct and cqSetup differ, each as listed.
  S  h.sci_strings over every beta 2b harness run in the script: none.
(The beta 2a description follows; "v3b" there now means v3d.)

verify_CICatcher_beta2a.py -- checks for CICatcher beta 2a (HP Prime PPL), 17 Oct 2026: the CAS call
form that CASProbe beta 1b found on the emulator.  Built from verify_CICatcher_beta2.py: every check
is kept and run in harness v3b, which models the calculator's CAS (CAS of a variable unevaluated,
the Prime's printing, a CAS string as a PPL string); E also reads every closed form in the Prime's
printing; G (new) runs beta 2 itself in v3b and compares beta 2a with beta 2.  New or changed
checks are marked "2a".

  A. The exact interval, computed by the program's own cqCPInt / cqCPB in the run harness
     (ppl_run_v3), against statsmodels proportion_confint(method='beta'): a grid of k, n
     and levels, and the drag path (each level from the last one's ends, 500 levels).
  B. The coverage bookkeeping: cqXBuild's catch level for every count against a direct
     "does statsmodels' interval contain p" at every level 500..999, for six (p, n);
     then 1,500 PPL samples per setting through cqAdd1: cqLimits vs statsmodels, colour
     from the catch level == the interval contains the truth, the long-run tally after
     cqSetLevel == a direct recount (as beta 1's section B2 does for the other four).
  C. Coverage by exact enumeration at the defaults (p = 0.10, n = 20) for Exact, Wilson and
     Wald at 80/90/95/99 %, the worst exact coverage over p (n = 20), the k = 0 end; every
     number help page 4 quotes, checked against the program text.
  D. The PPL's own sampler: 20,000 Exact intervals through cqAdd1 vs the exact coverage.
  E. Scripted sessions of CICatcher() with cas = 'giac' and cas = 'fail': Exact setup, +50,
     tap a line with 0 "yes" answers (the closed form and its badge), a slider drag with
     that line picked (no CAS call inside the drag), Up, Help (6 pages), Quit; the CAS
     templates through icas for every n and level the program can send; the frame budget
     and BINOMIAL calls per drag step.
  F. Beta 1's own suite (verify_CICatcher.py) run against beta 2, with its help-page count
     changed from five to six.

  G. 2a: beta 2 in harness v3b (its cqCas returns its own text: "1-(50/2000)^(1/20)", unreduced,
     with the badge), and beta 2a against beta 2 (only cqCas differs).

Run:  python3 verify_CICatcher_beta2c.py   (2c; the 2a run line was: python3 verify_CICatcher_beta2a.py)
"""
import math, os, re, sys, time, subprocess, tempfile
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('VERIFY_PRED_DIR', '/home/claude/work/out')   # 2c: where older versions are looked for last
PROG = os.path.join(HERE, 'CICatcher_beta2c.txt')


def find_pred(name):
    """2c: a predecessor file (an older version, or an older verify script).  Beside this script first,
    then in its _old folder and any _superseded* folder, then in /home/claude/work/out.  None if absent:
    the checks that need it print SKIP (review item 22)."""
    import glob as _glob
    places = [HERE, os.path.join(HERE, '_old')] + sorted(_glob.glob(os.path.join(HERE, '_superseded*'))) + [OUT]
    for d in places:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    return None


V2B = find_pred('CICatcher_beta2b.txt')
V2A = find_pred('CICatcher_beta2a.txt')
V2 = find_pred('CICatcher_beta2.txt')
V1SUITE = find_pred('verify_CICatcher.py')
SKIPS = []


def skip(what):
    SKIPS.append(what)
    print('  SKIP  ' + what)


# 2c: harness v3e (the brief's); it sits beside this script or in /home/claude/work/out
for _d in (HERE, OUT, '/home/claude/work/out'):
    if os.path.exists(os.path.join(_d, 'ppl_run_v3e.py')):
        sys.path.insert(0, _d)
        break
from ppl_run_v3e import Harness as _HarnessV3d, ACCEPT, PPLError, prime_print   # noqa: E402

ALL_H = []          # 2b: every harness made in this script, for the sci_strings audit (S)


class Harness(_HarnessV3d):
    def __init__(self, paths=None, *a, **k):
        _HarnessV3d.__init__(self, paths, *a, **k)
        self._src = paths
        ALL_H.append(self)
say = print

FAILS = []
NCHK = [0]


def check(ok, what):
    NCHK[0] += 1
    print(('  ok    ' if ok else '  FAIL  ') + what)
    if not ok:
        FAILS.append(what)


def beta(k, n, L):
    lo, hi = proportion_confint(k, n, alpha=1 - L, method='beta')
    return (0.0 if np.isnan(lo) else lo), (1.0 if np.isnan(hi) else hi)


def new_harness(seed=1, cas='giac'):
    h = Harness(PROG, seed=seed, cas=cas)
    h.call('cqInit')
    return h


def setup(h, kind, n, level, p=0.1, mu=100.0, sigma=15.0):
    g = h.globals_
    g['cqType'] = float(kind)
    g['cqMu'], g['cqSg'], g['cqP'] = mu, sigma, p
    g['cqN'], g['cqL'] = float(n), float(level)
    h.call('cqReset')


def nbin(h):
    return len([s for s in h.stat_calls if s[0].startswith('BINOMIAL')])


# ============================================================================ A
def part_a():
    print('=' * 78)
    print('A. The exact interval, by the program\'s own cqCPInt / cqCPB (harness)')
    print('=' * 78)
    h = new_harness()
    check(h.call('cqBinCheck') == 1, 'cqBinCheck passes with BINOMIAL_CDF(n, p, k)')
    w = 0; cnt = 0
    for L in (500, 800, 900, 950, 990, 999):
        a2 = (1000 - L) / 2000
        for n in list(range(5, 31)) + [50, 100]:
            for k in range(0, n + 1):
                lo, hi = h.call('cqCPInt', k, n, a2, 0)
                rl, rh = beta(k, n, L / 1000)
                w = max(w, abs(lo - rl), abs(hi - rh)); cnt += 1
    check(w < 1e-8, 'cqCPInt vs statsmodels beta: %d intervals (n 5-30, 50, 100; 50-99.9 %%), worst |diff| %.1e' % (cnt, w))
    # the drag path: every level from 500 to 999, each end started from the last level's
    w = 0; calls = []
    for k, n in ((0, 20), (1, 20), (2, 20), (5, 20), (19, 20), (20, 20), (38, 100), (3, 5)):
        lo, hi = h.call('cqCPInt', k, n, 0.25, 0)
        for L in range(501, 1000):
            a2 = (1000 - L) / 2000
            h.stat_calls[:] = []
            lo = h.call('cqCPB', k, n, a2, 1, 0, lo)
            hi = h.call('cqCPB', k, n, a2, 2, 0, hi)
            calls.append(nbin(h))
            rl, rh = beta(k, n, L / 1000)
            w = max(w, abs(lo - rl), abs(hi - rh))
    check(w < 1e-8, 'the drag path (each level started from the last one\'s ends, 8 counts x 499 levels): worst |diff| %.1e' % w)
    print('    BINOMIAL_CDF + BINOMIAL calls per count per level step: mean %.1f, max %d' % (np.mean(calls), max(calls)))
    h2 = new_harness()
    h2._table['BINOMIAL_CDF'] = lambda a, site: stats.binom.cdf(a[1], a[0], a[2]) if 0 <= a[2] <= 1 else 0.5
    check(h2.call('cqBinCheck') == 0, 'cqBinCheck fails when BINOMIAL_CDF reads (n, k, p); setup then refuses Exact')


# ============================================================================ B
def part_b():
    print('\n' + '=' * 78)
    print('B. The coverage bookkeeping for Exact')
    print('=' * 78)
    for p, n in ((0.1, 20), (0.5, 5), (0.38, 100), (0.01, 5), (0.99, 50), (0.25, 37)):
        h = new_harness()
        setup(h, 5, n, 950, p=p)
        cat = h.globals_['cqXCat']
        mism = 0
        for k in range(n + 1):
            for L in range(500, 1000):
                lo, hi = beta(k, n, L / 1000)
                if (lo <= p <= hi) != (cat[k] <= L):
                    mism += 1
        check(mism == 0, 'p %-4s n %-3d cqXBuild: catch level <= L  <=>  statsmodels\' interval contains p, '
              'every k and every level 500..999 (%d mismatches)' % (p, n, mism))
    levels = (500, 650, 800, 900, 950, 975, 990, 999)
    for n, p in ((20, 0.1), (5, 0.1), (100, 0.38)):
        h = new_harness(seed=n + 5)
        setup(h, 5, n, 950, p=p)
        g = h.globals_
        samples = []
        for _ in range(1500):
            h.call('cqAdd1')
            s = int(g['cqHead']) - 1
            samples.append((g['cqEst'][s], g['cqCat'][s]))
        mism = tally_bad = 0; worst = 0
        for L in levels:
            h.call('cqSetLevel', float(L))
            if int(g['cqHit']) != sum(1 for e, c in samples if c <= L):
                tally_bad += 1
            for e, c in samples:
                lo, hi = h.call('cqLimits', e, 0.0)
                if (lo <= p <= hi) != (c <= L):
                    mism += 1
                rl, rh = beta(round(e * n), n, L / 1000)
                worst = max(worst, abs(lo - rl), abs(hi - rh))
        nm = 'Exact n = %d, p = %s' % (n, p)
        check(worst < 1e-8, '%-22s cqLimits vs statsmodels beta: worst %.1e (1,500 PPL samples x 8 levels)' % (nm, worst))
        check(mism == 0, '%-22s colour from the catch level == interval contains the truth: %d mismatches' % (nm, mism))
        check(tally_bad == 0, '%-22s long-run tally after cqSetLevel == direct recount at all 8 levels' % nm)


# ============================================================================ C
def coverage(method, p, n, L):
    k = np.arange(n + 1); pk = stats.binom.pmf(k, n, p)
    if method == 'exact':
        lo, hi = proportion_confint(k, n, alpha=1 - L / 1000, method='beta')
        lo = np.nan_to_num(lo, nan=0.0); hi = np.nan_to_num(hi, nan=1.0)
    else:
        z = stats.norm.ppf(0.5 + L / 2000); ph = k / n
        if method == 'wald':
            lo = ph - z * np.sqrt(ph * (1 - ph) / n); hi = ph + z * np.sqrt(ph * (1 - ph) / n)
        else:
            den = 1 + z * z / n; cen = (ph + z * z / (2 * n)) / den
            hw = z * np.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
            lo, hi = cen - hw, cen + hw
    return pk[(lo <= p) & (p <= hi)].sum()


def part_c():
    print('\n' + '=' * 78)
    print('C. Coverage by exact enumeration, and the numbers help page 4 quotes')
    print('=' * 78)
    print('    p = 0.10, n = 20      80 %      90 %      95 %      99 %')
    out = {}
    for m in ('exact', 'wilson', 'wald'):
        row = [coverage(m, 0.1, 20, L) for L in (800, 900, 950, 990)]
        out[m] = row
        print('    %-12s       ' % m + '  '.join('%.4f  ' % v for v in row))
    ps = np.linspace(0.0005, 0.9995, 19991)
    cs = np.array([coverage('exact', q, 20, 950) for q in ps])
    worst, where = cs.min(), ps[cs.argmin()]
    print('    worst exact coverage over p (n = 20, 95 %%): %.4f at p = %.4f; mean %.4f' % (worst, where, cs.mean()))
    up0 = 1 - 0.025 ** (1 / 20)
    print('    the k = 0 upper end at n = 20, 95 %%: 1 - 0.025^(1/20) = %.6f (statsmodels %.6f)' % (up0, beta(0, 20, .95)[1]))
    widths = {}
    for m in ('exact', 'wilson'):
        k = np.arange(21); pk = stats.binom.pmf(k, 20, 0.1)
        if m == 'exact':
            lo, hi = proportion_confint(k, 20, 0.05, 'beta')
        else:
            lo, hi = proportion_confint(k, 20, 0.05, 'wilson')
        widths[m] = (pk * (np.nan_to_num(hi, nan=1) - np.nan_to_num(lo, nan=0))).sum()
    print('    mean width at p = 0.10, n = 20, 95 %%: exact %.3f, Wilson %.3f' % (widths['exact'], widths['wilson']))
    src = open(PROG, encoding='utf-8').read()
    m = re.search(r'hpK := cqPage\("Exact intervals: never below", \{(.*?)\},\n', src, re.S)
    page = m.group(1) if m else ''
    for txt, val in (('95.8 %', worst), ('98.9 %', out['exact'][2]), ('95.7 %, Wald', out['wilson'][2]),
                     ('Wald 87.6 %', out['wald'][2]), ('catches 95.7 %', out['exact'][1]), ('0.168', up0)):
        num = float(re.findall(r'\d+\.\d+', txt)[0])
        shown = round(100 * val, 1) if '%' in txt else round(val, 3)
        check(txt in page and abs(num - shown) < 1e-9, 'help page 4 quotes %r (computed %.4f)' % (txt, val))
    check(abs(out['exact'][0] - out['exact'][1]) < 1e-12, 'exact at 80 %% and 90 %% both %.4f (the page says 95.7 %% for both)'
          % out['exact'][0])
    check(min(out['exact']) >= 0.95 and worst >= 0.95, 'exact coverage is at or above 95 % at every level shown, and over all p')
    h = new_harness()
    h.press('Enter', 'Enter', 'Enter', 'Esc')
    h.call('cqHelp')
    hp = [p for p in h.pages if p.find('Exact intervals: never below')][0]
    body = [t_.text for t_ in hp.texts if t_.y >= 28 and t_.y < 215]
    check(len(body) == 14 and max(len(s) for s in body) <= 48,
          'help page 4 as drawn: %d lines, the longest %d characters (ChiTable\'s 48 fit)' % (len(body), max(len(s) for s in body)))
    for s in body:
        print('      | ' + s)
    return out


# ============================================================================ D
def part_d(out):
    print('\n' + '=' * 78)
    print('D. The PPL sampler: 20,000 Exact intervals through cqAdd1')
    print('=' * 78)
    t0 = time.time()
    h = new_harness(seed=99)
    setup(h, 5, 20, 950)
    for _ in range(20000):
        h.call('cqAdd1')
    g = h.globals_
    cov = g['cqHit'] / g['cqTot']
    se = math.sqrt(out['exact'][2] * (1 - out['exact'][2]) / 20000)
    check(abs(cov - out['exact'][2]) < 4 * se, 'PPL coverage %.4f vs exact %.4f (4 SE = %.4f)  [%.0f s]'
          % (cov, out['exact'][2], 4 * se, time.time() - t0))


# ============================================================================ E
def giac_many(exprs):
    with tempfile.NamedTemporaryFile('w', suffix='.giac', delete=False) as f:
        f.write(''.join(e + ';\n' for e in exprs)); name = f.name
    o = subprocess.run(['icas', name], capture_output=True, text=True, errors='replace', timeout=600).stdout
    os.unlink(name)
    return [ln.strip().rstrip(',') for ln in o.split('\n') if ln.strip() and not ln.strip().startswith('//')
            and 'synonyms' not in ln]


def session(cas, row, extra_after_tap=True, prog=None):
    h = Harness(prog or PROG, seed=5, cas=cas)
    h.press('Enter')                 # welcome
    h.choose(5)                      # Exact
    h.answer(ACCEPT)                 # p 0.10, n 20, level 0.95
    h.tap(130, 230)                  # +50
    if row:
        h.tap(150, 29 + 3 * (row - 1))                      # the line with 0 yeses
        if extra_after_tap:
            h.drag([(310, 104), (310, 90), (310, 70)])      # the level slider, the line still picked
            h.press('Up')                                   # one more level by key
    h.tap(300, 230); h.choose(3)                            # Menu > Help
    h.press('Enter', 'Enter', 'Enter', 'Enter', 'Enter', 'Enter')
    h.tap(300, 230); h.choose(4)                            # Menu > Quit
    h.execute('CICatcher()')
    return h


def part_e():
    print('\n' + '=' * 78)
    print('E. Scripted sessions, cas = giac and cas = fail; the CAS templates')
    print('=' * 78)
    # find a line with 0 yeses after +50 (the same seed gives the same samples)
    h = session('giac', 0)
    g = h.globals_
    rows = [r for r in range(1, 51) if round(g['cqEst'][int((g['cqHead'] - r) % 50)] * 20) == 0]
    check(h.error is None and bool(rows), 'a first run finds the rows with 0 yeses: %s' % rows[:8])
    row = rows[0]
    for cas in ('giac', 'fail'):
        t0 = time.time()
        h = session(cas, row)
        print('\n  --- cas = %s: %r  [%.1f s, %d frames]' % (cas, h.result, time.time() - t0, len(h.pages)))
        check(h.error is None and h.result.startswith('CICatcher: ') and 'Exact, p = 0.10, n = 20' in h.result,
              'the session runs to Quit: %r' % h.result)
        check(not any(h.leftover()), 'every scripted event was used')
        cf = [(i, t.text) for i, p in enumerate(h.pages) for t in p.texts if t.text.startswith(('upper = ', 'lower = '))]
        badges = [(i, t.text) for i, p in enumerate(h.pages) for t in p.texts if t.text in ('exact (CAS)', 'decimal')]
        print('    closed-form lines seen:', sorted(set(x[1] for x in cf)))
        print('    badges, frame by frame:', ''.join('C' if b == 'exact (CAS)' else 'd' for _, b in badges))
        calls = [x[0] for x in h.cas_calls]
        print('    CAS calls:', calls)
        if cas == 'giac':
            check(any(t == 'upper = 1-(1/40)^(1/20) = 0.1684' for _, t in cf),
                  'the picked line (0 of 20): "upper = 1-(1/40)^(1/20) = 0.1684" with "exact (CAS)"')
            check(len(calls) == len(set(calls)) and len(calls) <= 4,
                  'the CAS is asked once per (end, n, level) after an event, never twice: %d calls' % len(calls))
            check(calls[0] == 'string(1-(50/2000)^(1/20))',
                  'the template: alpha/2 as (1000 - L)/2000 in whole numbers (2a: asked as string(...))')
            check(all(c[1].startswith('"') for c in h.cas_calls) and not h.cas_vars
                  and not any('non-literal' in w for w in h.warnings),
                  '2a: every answer arrives quoted, no CAS variable assigned, no CAS call of a variable')
            # inside the drag the badge must be "decimal" (no CAS in a drag loop): the
            # levels the CAS was asked about are read back from its templates; every frame
            # at any OTHER level (the drag's intermediate levels) must show the decimal form
            asked = {1000 - int(re.search(r'\((\d+)/2000\)', c).group(1)) for c in calls}
            def lev(p):
                t_ = p.find('target ')
                return int(round(10 * float(t_.text.split()[1]))) if t_ else None
            mid = [(i, b) for i, b in badges if lev(h.pages[i]) not in asked]
            check(bool(mid) and all(b == 'decimal' for _, b in mid),
                  'the CAS was asked only at levels %s; the %d frames drawn at other levels (inside the drag) all show '
                  'the decimal form' % (sorted(asked), len(mid)))
        else:
            check(all(b == 'decimal' for _, b in badges) and any('(%s/2)^(1/n) = ' % chr(945) in t for _, t in cf),
                  'cas = fail: "upper = 1 - (alpha/2)^(1/n) = 0.1684" and the badge "decimal" throughout, no error')
        hp = [p for p in h.pages if p.find('Exact intervals: never below')]
        # 2c: the expected line was "... BINOMIAL_CDF (checked)" (47 characters): that WAS C-C2
        check(bool(hp) and hp[0].find('exact ends: bisection on BINOMIAL_CDF, checked') is not None,
              'help page 4 shown, with its engine line (2c: "exact ends: bisection on BINOMIAL_CDF, checked")')
        heads = [p for p in h.pages if p.find('Exact, p = 0.10, n = 20')]
        check(len(heads) > 5, 'the header names the method: "Exact, p = 0.10, n = 20" (%d frames)' % len(heads))
    # the templates the program can send: k = 0 and k = n, every n 5..100 and a spread of levels
    ex = []; want = []
    for n in range(5, 101):
        for L in (500, 503, 800, 900, 950, 953, 990, 995, 999):
            base = '(%d/2000)^(1/%d)' % (1000 - L, n)
            ex += ['1-' + base, base]
            want += [1 - ((1000 - L) / 2000) ** (1 / n), ((1000 - L) / 2000) ** (1 / n)]
    r = giac_many(ex)
    ev = giac_many(['evalf(%s,20)' % x for x in r])
    bad = [x for x, e, w in zip(r, ev, want) if 'Root' in x or 'rror' in x or abs(float(e) - w) > 1e-12]
    longest = max(len(x) for x in r)
    check(not bad and len(r) == len(ex), '%d CAS templates (n 5-100, 9 levels, both ends) evaluate to the closed form; '
          'longest answer %d characters (the panel shows up to 20 with the decimal, 28 without)' % (len(ex), longest))
    print('    e.g. %s -> %s; %s -> %s' % (ex[0], r[0], ex[9], r[9]))
    # 2a: the same answers as the calculator prints them
    pr = [prime_print(x) for x in r]
    check(not any('sqrt' in x for x in pr) and max(len(x) for x in pr) <= longest,
          '2a: in the Prime\'s printing no answer has "sqrt" and none is longer than desktop Giac\'s (longest %d)'
          % max(len(x) for x in pr))
    # frame budget with Exact: one main frame, and BINOMIAL calls per drag step
    h = Harness(PROG, seed=6)
    h.press('Enter'); h.choose(5); h.answer(ACCEPT)
    h.tap(130, 230); h.drag([(310, 104), (310, 96), (310, 88), (310, 80)]); h.press('Esc')
    h.execute('CICatcher()')
    full = [p for p in h.pages if p.find('of 50 (')]
    p = full[-1]
    print('    one frame with 50 Exact intervals: %d shapes, %d texts' % (len(p.shapes), len(p.texts)))
    check(len(p.shapes) < 200 and len(p.texts) < 25, 'per-frame drawing calls within the beta 1 budget')
    nb = len([s for s in h.stat_calls if s[0].startswith('BINOMIAL')])
    print('    BINOMIAL calls in the whole session (cqBinCheck, cqXBuild, 50 samples, 4 drag steps): %d' % nb)
    # keyboard-only and small-n sessions with Exact
    for n in (5, 100):
        h = Harness(PROG, seed=13 + n)
        h.press('Enter'); h.choose(5); h.answer({'suNn': n})
        h.tap(130, 230); h.tap(150, 29); h.tap(150, 29 + 3 * 20)
        h.drag([(310, 120), (310, 31), (310, 176)])
        h.press('Up', 'Up', 'Down', 'Left', 'Right')
        h.tap(20, 230); h.press('Esc')
        h.execute('CICatcher()')
        check(h.error is None and not any(h.leftover()), 'Exact n = %d session with drags and keys: %r' % (n, h.result))
    # Exact refused when the BINOMIAL check failed
    h = Harness(PROG, seed=2)
    h._table['BINOMIAL_CDF'] = lambda a, site: stats.binom.cdf(a[1], a[0], a[2]) if 0 <= a[2] <= 1 else 0.5
    h.press('Enter'); h.choose(5)
    h.execute('CICatcher()')
    check(h.error is None and h.msgboxes and 'Exact is off' in ' '.join(h.msgboxes[0].lines),
          'with BINOMIAL_CDF failing its check, Exact is refused with a message: %r' % (h.result,))


# ============================================================================ F
def part_f():
    print('\n' + '=' * 78)
    print('F. Beta 1\'s suite (verify_CICatcher.py) against beta 2')
    print('=' * 78)
    if V1SUITE is None:
        skip('F: beta 1\'s verify_CICatcher.py not found beside this script, in _old / _superseded*, or in %s' % OUT)
        return
    s = open(V1SUITE, encoding='utf-8').read()
    s = s.replace("os.path.join(HERE, 'CICatcher_beta1.txt')", repr(PROG))
    # 2b: beta 1's suite runs in harness v3d too; 2c: in v3e, from the folder this script found it in
    assert s.count("sys.path.insert(0, '/home/claude/work/harness')\nfrom ppl_run_v1 import Harness, KEY, ACCEPT, PPLError") == 1
    s = s.replace("sys.path.insert(0, '/home/claude/work/harness')\nfrom ppl_run_v1 import Harness, KEY, ACCEPT, PPLError",
                  "sys.path.insert(0, %r)\nfrom ppl_run_v3e import Harness, KEY, ACCEPT, PPLError"
                  % os.path.dirname(sys.modules[_HarnessV3d.__module__].__file__))
    s = s.replace("    h.press('Enter', 'Enter', 'Enter', 'Enter', 'Enter')\n",
                  "    h.press('Enter', 'Enter', 'Enter', 'Enter', 'Enter', 'Enter')   # beta 2: six help pages\n")
    d = tempfile.mkdtemp()
    path = os.path.join(d, 'verify_CICatcher_on_beta2.py')
    open(path, 'w').write(s)
    t0 = time.time()
    r = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=HERE,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    oks = r.stdout.count('  ok    ')
    last = [ln for ln in r.stdout.split('\n') if ln.startswith(('PASS', 'FAIL'))]
    print('  ' + (last[-1] if last else r.stdout[-500:]))
    check(r.returncode == 0, 'beta 1\'s suite passes on beta 2: %d checks (one script change: six help pages)  [%.0f s]'
          % (oks, time.time() - t0))


# ============================================================================ G (2a)
def part_g():
    print('\n' + '=' * 78)
    print('G. 2a: beta 2 in harness v3d, and beta 2a against beta 2 (kept from the 2a script)')
    print('=' * 78)
    if V2 is None or V2A is None:
        skip('G (2a): CICatcher_beta2.txt or CICatcher_beta2a.txt not found')
        return
    h = session('giac', 0)
    g = h.globals_
    rows = [r for r in range(1, 51) if round(g['cqEst'][int((g['cqHead'] - r) % 50)] * 20) == 0]
    h2 = session('giac', rows[0], prog=V2)
    cf = [t.text for p in h2.pages for t in p.texts if t.text.startswith(('upper = ', 'lower = '))]
    check(any(t.startswith('upper = 1-(50/2000)^(1/20)') for t in cf) and any('non-literal' in w for w in h2.warnings),
          '2a: beta 2 in v3b shows its own CAS text, "upper = 1-(50/2000)^(1/20)", unreduced, as if the CAS '
          'had answered -- the emulator\'s finding')
    exec(G_CODE, globals())


G_CODE = "\n# ================================================================ G (round 2a)\nsay('\\nG. beta 2a: beta 2 in harness v3b, and beta 2a against beta 2')\nimport re as _re\n_b_old = open(V2, encoding='utf-8').read()\n_b_new = open(V2A, encoding='utf-8').read()\n\n\ndef _bodies(txt):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)\n    c = _re.sub(r'//[^\\n]*', '', c)\n    out = {}\n    for m in _re.finditer(r'(?m)^(?:EXPORT\\s+|LOCAL\\s+)?([A-Za-z]\\w*)\\(([^()\\n]*)\\)\\s*\\nBEGIN\\n.*?^END;', c, _re.S):\n        out[m.group(1)] = _re.sub(r'[ \\t]+\\n', '\\n', m.group(0))\n    return out\n\n\n_B0, _B1 = _bodies(_b_old), _bodies(_b_new)\n_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))\ncheck(_diff == ['cqCas'], 'beta 2a: routines that differ from beta 2: %s (want cqCas)' % _diff)\n\n\ndef _outside(t, names):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\\n]*', '', t))\n    if names:\n        c = _re.sub(r'(?ms)^(?:EXPORT\\s+|LOCAL\\s+)?(?:%s)\\([^\\n]*\\)\\s*\\nBEGIN\\n.*?^END;' % '|'.join(names), '', c)\n    return _re.sub(r'\\s+', ' ', c)\n\n\ncheck(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'beta 2a: outside those routines only comments differ')\n_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)\n_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)\ncheck(_py0 == _py1, 'beta 2a: the #PYTHON blocks are unchanged')\nsay('  routines that differ from beta 2: %s; everything else differs only in comments' % ', '.join(_diff))\n"


# ============================================================================ R (2b)
def _norm(t):
    t = re.sub(r'//[^\n]*', '', t)
    return '\n'.join(l.rstrip() for l in t.split('\n') if l.strip())


def _choose_items(path):
    s = re.sub(r'//[^\n]*', '', open(path, encoding='utf-8').read())
    out = []
    for m in re.finditer(r'\bCHOOSE\(', s):
        i = m.end(); depth = 1; ins = False
        while depth:
            c = s[i]
            if c == '"':
                ins = not ins
            elif not ins and c in '({[':
                depth += 1
            elif not ins and c in ')}]':
                depth -= 1
            i += 1
        body = s[m.end():i - 1]
        lst = body[body.index('{') + 1:body.rindex('}')]
        parts, depth, ins, cur = [], 0, False, ''
        for c in lst:
            if c == '"':
                ins = not ins
            elif not ins and c in '({[':
                depth += 1
            elif not ins and c in ')}]':
                depth -= 1
            if c == ',' and depth == 0 and not ins:
                parts.append(cur); cur = ''
                continue
            cur += c
        parts.append(cur)
        for p_ in parts:
            # a glyph variable (cqSgS = sigma) counts as one character
            out.append(''.join(q[1:-1] if q.startswith('"') else '*' for q in [x.strip() for x in p_.split('+')]))
    return out


def part_r():
    print('\n' + '=' * 78)
    print('R. 2b: the round-2 emulator findings (harness v3d)')
    print('=' * 78)
    # R1. cqCas with the CAS failing; beta 2a stops
    h = new_harness(cas='fail')
    r = h.call('cqCas', '1-(50/2000)^(1/20)')
    check(r == '' and h.error is None and h.globals_['cqCasOK'] == 0,
          'R1: cqCas with the CAS failing returns "" (%r), no error, cqCasOK = 0' % r)
    hg = new_harness(cas='giac')
    for q, want in (('1-(50/2000)^(1/20)', '1-(1/40)^(1/20)'), ('1/0', ''), ('0/0', ''), ('limit(1/cqq,cqq,0,1)', '')):
        got = hg.call('cqCas', q)
        check(got == want, 'R1: cqCas(%r) with Giac = %r (want %r)' % (q, got, want))
    if V2A is None:
        skip('R1-R4: the comparisons with beta 2a (CICatcher_beta2a.txt not found)')
    else:
        h0 = Harness(V2A, seed=1, cas='fail'); h0.call('cqInit')
        try:
            h0.call('cqCas', '1-(50/2000)^(1/20)')
            check(False, 'R1: beta 2a cqCas did not stop on a failed call in v3d')
        except PPLError as ex:
            check('INSTRING' in str(ex), 'R1: beta 2a cqCas, the same failed call in v3d, stops: %s' % str(ex)[:60])
    # R2. cas='fail' end to end: the E session (Exact, +50, the 0-yes line, the slider drag, Up, Help, Quit)
    hs = session('giac', 0)
    g = hs.globals_
    rows = [r_ for r_ in range(1, 51) if round(g['cqEst'][int((g['cqHead'] - r_) % 50)] * 20) == 0]
    hn = session('fail', rows[0])
    badges = [t.text for p in hn.pages for t in p.texts if t.text in ('exact (CAS)', 'decimal')]
    check(hn.error is None and hn.result.startswith('CICatcher: ') and badges and all(b == 'decimal' for b in badges),
          'R2: beta 2c, cas=fail session to Quit: %d closed-form frames, all "decimal", no error' % len(badges))
    ho = None
    if V2A is not None:
        try:
            session('fail', rows[0], prog=V2A)
        except PPLError:
            pass
        ho = [h_ for h_ in ALL_H if h_._src == V2A][-1]            # the harness that session made
        check(isinstance(ho.error, PPLError) and 'INSTRING' in str(ho.error),
              'R2: beta 2a, the same session in v3d, stops on INSTRING (%s)' % str(ho.error)[:50])
    # R3. the setup menu fits its box
    new_it = _choose_items(PROG)
    old_it = _choose_items(V2A) if V2A is not None else None
    check('Proportion: Exact (C-P)' in new_it and (old_it is None or ('Proportion: Exact (Clopper-Pearson)' in old_it
          and len(new_it) == len(old_it))), 'R3: the Exact item is "Proportion: Exact (C-P)" (%d characters)' % len('Proportion: Exact (C-P)'))
    over = [t for t in new_it if len(t) > 28]
    # 2c: beta 2b excepted the main menu's first line here ("New setup: interval, population, n", 34);
    # that exception WAS the C-C1 finding, so there is none now
    check(over == [],
          'R3 (2c): every CHOOSE line is 28 characters or fewer, the main menu\'s first included: %s' % over)
    if old_it is not None:
        old_over = sorted(t for t in old_it if len(t) > 30)
        check(old_over == ['New setup: interval, population, n', 'Proportion: Exact (Clopper-Pearson)'],
              'R3: beta 2a: %s' % old_over)
    print('    CHOOSE lines: %d, the longest %d ("%s"); the Exact item %r' % (
        len(new_it), max(len(t) for t in new_it), max(new_it, key=len), 'Proportion: Exact (C-P)'))
    hm = Harness(PROG, seed=5, cas='fail')
    hm.press('Enter'); hm.choose(5); hm.answer(ACCEPT); hm.tap(130, 230); hm.tap(300, 230); hm.choose(4)
    hm.execute('CICatcher()')
    shown = [it for c in hm.chooses for it in c.items]
    check(hm.error is None and 'Proportion: Exact (C-P)' in shown and int(hm.globals_['cqType']) == 5
          and 'Exact, p = 0.10, n = 20' in hm.result,
          'R3: in a run the new line is shown and item 5 still sets Exact: %r' % hm.result)
    # R4. fixed decimals: runs that reach small interval ends, shares and parameters
    CASES = [
        ('Exact, p = 0.01, n = 100 (lower end 0.00025 for one yes)', 5, {'suTr': 0.01, 'suNn': 100}),
        ('Wald, p = 0.05, n = 20, the level dragged (an end crosses 0)', 3, {'suTr': 0.05, 'suNn': 20}),
        ('Wilson, p = 0.01, n = 5', 4, {'suTr': 0.01, 'suNn': 5}),
        ('z, mu = 0.00003, sigma = 0.00001 (typed)', 1, {'suTr': 0.00003, 'suSD': 0.00001, 'suNn': 10}),
        ('t, mu = 0.0004, sigma = 0.0002, n = 2', 2, {'suTr': 0.0004, 'suSD': 0.0002, 'suNn': 2}),
    ]
    old_sci = {}
    for tag, typ, ans in CASES:
        for cas in ('giac', 'fail'):
            res = {V2A: None}
            for prog in ((PROG, V2A) if V2A is not None else (PROG,)):
                h = Harness(prog, seed=21, cas=cas)
                h.press('Enter'); h.choose(typ); h.answer(ans)
                h.tap(130, 230); h.tap(130, 230)                     # +50 twice
                for row in (1, 4, 9, 17, 26, 33, 41, 50):              # pick lines: the panel
                    h.tap(150, 29 + 3 * (row - 1))
                h.drag([(310, 104), (310, 140), (310, 176), (310, 120), (310, 60), (310, 31)])
                h.press('Up', 'Down', 'Left', 'Right')
                h.tap(300, 230); h.choose(4)
                try:
                    h.execute('CICatcher()')
                except Exception:
                    pass
                res[prog] = h
            hn, ho = res[PROG], res[V2A]
            check(hn.error is None and hn.result and hn.result.startswith('CICatcher: '),
                  'R4 %s [%s]: beta 2c runs to Quit (%s)' % (tag, cas, hn.error))
            check(hn.sci_strings == [], 'R4 %s [%s]: beta 2c printed scientific: %s' % (tag, cas, hn.sci_strings[:5]))
            shown = [t.text for p in hn.pages for t in p.texts] + [hn.result or '']
            check(not any(u'ᴇ' in s for s in shown), 'R4 %s [%s]: a small-capital E on screen' % (tag, cas))
            for v, d, t in (ho.sci_strings if ho is not None else []):
                old_sci.setdefault(t, (v, d))
            if cas == 'giac':
                print('    %-62s beta 2c: 0 scientific, %d frames; beta 2a: %s%s' % (
                    tag, len(hn.pages), len(ho.sci_strings) if ho is not None else 'not run',
                    ' (stopped)' if ho is not None and ho.error else ''))
                if typ == 4:
                    w0 = sorted({t.text for p in hn.pages for t in p.texts if t.text.startswith(chr(57345) + ' = 0/5 = 0.00: ')})
                    w0o = sorted({t.text for p in ho.pages for t in p.texts if t.text.startswith(chr(57345) + ' = 0/5 = 0.00: ')}) if ho is not None else []
                    print('        a 0-yes Wilson line: beta 2c %s; beta 2a %s' % (w0, w0o))
                    check(w0 and all(s.startswith(chr(57345) + ' = 0/5 = 0.00: 0.00 to ') for s in w0),
                          'R4: the Wilson 0-yes lower end reads 0.00 (not -0.00): %s' % w0)
                if typ == 4 or typ == 1:
                    heads = sorted({t.text for p in hn.pages for t in p.texts if t.text.startswith(('Wilson,', 'z,'))})
                    print('        header: %s' % heads[:1])
                    if typ == 1:
                        check(any(u'= 0.000030' in s and '= 0.000010' in s for s in heads),
                              'R4: the typed mu and sigma read 0.000030 and 0.000010: %s' % heads[:1])
                if typ == 5:
                    ends = sorted({t.text for p in hn.pages for t in p.texts if ' = 1/100 = ' in t.text})
                    print('        a one-yes panel: %s' % (ends[:1] or ['(none picked)']))
    if V2A is not None:
        print('    beta 2a printed, in these runs:')
        for t, (v, d) in sorted(old_sci.items(), key=lambda kv: (kv[1][1], abs(kv[1][0])))[:14]:
            print('      STRING(%.6g, 2, %d) -> %s' % (v, d, t))
        check(len(old_sci) >= 3, 'R4: beta 2a printed scientific strings in these runs (%d)' % len(old_sci))
    # R5. the helpers on edge values
    hu = new_harness(cas='fail')
    for v, d, want in ((0.000253, 3, '0.000'), (0.00052, 3, '0.001'), (-0.0002, 3, '0.000'), (0.1684, 4, '0.1684'),
                       (0.0000004, 6, '0.000000'), (100.0, 1, '100.0'), (-5.551115123125783e-17, 2, '0.00'),
                       (-0.0312, 4, '-0.0312')):
        got = hu.call('cqF', float(v), float(d))
        check(got == want, 'R5: cqF(%r, %d) = %r (want %r)' % (v, d, got, want))
    for v, want in ((100.0, '100'), (0.1, '0.10'), (0.12345, '0.1235'), (0.00001, '0.000010'), (0.00003, '0.000030'),
                    (0.000015, '0.000015'), (-0.00002, '-0.000020'), (15.0, '15'), (0.0005, '0.0005')):
        got = hu.call('cqNumS', float(v))
        check(got == want, 'R5: cqNumS(%r) = %r (want %r)' % (v, got, want))
    for a, b, want in ((1, 2000, '0.1'), (1, 3000, '0.0'), (47, 50, '94.0'), (0, 7, '0.0'), (3, 0, '--')):
        got = hu.call('cqPct', float(a), float(b))
        check(got == want, 'R5: cqPct(%d, %d) = %r (want %r)' % (a, b, got, want))
    check(hu.sci_strings == [], 'R5: the helpers printed scientific: %s' % hu.sci_strings)
    print('    cqF(0.000253, 3) = "0.000", cqNumS(0.00001) = "0.000010", cqPct(1, 3000) = "0.0"')


def part_g2b():
    print('\n' + '=' * 78)
    print('G. 2b: beta 2b against beta 2a (the record of 2b; 2c compares those two files, not itself)')
    print('=' * 78)
    if V2A is None or V2B is None:
        skip('G (2b): CICatcher_beta2a.txt or CICatcher_beta2b.txt not found')
        return
    t0, t1 = open(V2A, encoding='utf-8').read(), open(V2B, encoding='utf-8').read()
    def bodies(txt):
        c = re.sub(r'//[^\n]*', '', txt)
        return {m.group(1): _norm(m.group(0)) for m in re.finditer(
            r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S)}
    N0, N1 = bodies(t0), bodies(t1)
    d = sorted(n for n in set(N0) | set(N1) if N0.get(n) != N1.get(n))
    check(d == ['cqCas', 'cqF', 'cqNumS', 'cqPct', 'cqSetup'], 'G: routines that differ from beta 2a: %s' % d)
    gl = '  IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;'
    check(N1['cqCas'] == N0['cqCas'].replace(gl, '  IF DIM(cR) > 0 THEN\n  ' + gl + '\n  END;'), 'G: cqCas is the DIM guard only')
    check(N1['cqF'] == N0['cqF'].replace('STRING(fmV, 2, fmD)', 'STRING(ROUND(fmV, fmD) + 0, 2, fmD)'), 'G: cqF rounds (+ 0), nothing else')
    check(N1['cqPct'] == N0['cqPct'].replace('STRING(100 * pcA / pcB, 2, 1)', 'STRING(ROUND(100 * pcA / pcB, 1), 2, 1)'),
          'G: cqPct rounds, nothing else')
    check(N1['cqNumS'] == N0['cqNumS'].replace('  RETURN STRING(nsV, 2, nsD);',
          '  IF nsD == 4 AND ABS(nsV) < 0.0001 THEN nsD := MIN(11, 1 - FLOOR(LOG(ABS(nsV)))); END;\n'
          '  RETURN STRING(ROUND(nsV, nsD), 2, nsD);'), 'G: cqNumS: the small-value line and the ROUND')
    check(N1['cqSetup'] == N0['cqSetup'].replace('"Proportion: Exact (Clopper-Pearson)"', '"Proportion: Exact (C-P)"'),
          'G: cqSetup: the one menu line')
    def outside(t, names):
        c = re.sub(r'//[^\n]*', '', t)
        c = re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
        return re.sub(r'\s+', ' ', c)
    check(outside(t0, d) == outside(t1, d), 'G: outside those routines only comments differ')
    print('  differ from beta 2a: %s, each exactly as listed; everything else differs only in comments' % ', '.join(d))


def part_s():
    print('\n' + '=' * 78)
    print('S. h.sci_strings over every beta 2c harness run of this script (parts A-R)')
    print('=' * 78)
    mine = [h for h in ALL_H if h._src == PROG]
    sci = [(v, d, t) for h in mine for v, d, t in h.sci_strings]
    check(sci == [], 'S: %d beta 2c harness runs, %d scientific STRING results (%d runs of older versions not counted)'
          % (len(mine), len(sci), len(ALL_H) - len(mine)))
    if sci:
        print('   ', sci[:10])


# ============================================================================ X (2c)
OLD_MENU = 'New setup: interval, population, n'
NEW_MENU = 'New: interval, population, n'
OLD_ENG = 'exact ends: bisection on BINOMIAL_CDF (checked)'
NEW_ENG = 'exact ends: bisection on BINOMIAL_CDF, checked'


def review_e2_e3(path):
    """check_CICatcher.py's E2 and E3 scans, copied: the CHOOSE items longer than 27 characters, and the
    fixed strings on code lines (MSGBOX and suMsg lines left out) longer than 46 (E3 itself allowed 47;
    46 is the header's own limit for a help page, which C-C2 enforces)."""
    src = open(path, encoding='utf-8').read()
    long_menu = []
    for m in re.finditer(r'CHOOSE\(([^;]*?)\);', src, re.S):
        for s in re.findall(r'"([^"]*)"', m.group(1))[1:]:
            if len(s) > 27:
                long_menu.append((len(s), s))

    def code_only(l):
        out, ins = [], False
        for i, ch in enumerate(l):
            if ch == '"':
                ins = not ins
            if not ins and l[i:i + 2] == '//':
                break
            out.append(ch)
        return ''.join(out)
    code_lines = [code_only(l) for l in src.split('\n') if not l.strip().startswith('//')]
    strings = [t for l in code_lines if 'MSGBOX' not in l and 'suMsg :=' not in l for t in re.findall(r'"([^"]*)"', l)]
    long_help = [(len(t), t) for t in strings if len(t) > 46]
    return long_menu, long_help


def menu_run(prog):
    """Exact setup at the start, +50, Menu > New setup > Cancel (the run is kept), Menu > Quit."""
    h = Harness(prog, seed=5, cas='fail')
    h.press('Enter'); h.choose(5); h.answer(ACCEPT); h.tap(130, 230)
    h.tap(300, 230); h.choose(1); h.choose(0)
    h.tap(300, 230); h.choose(4)
    h.execute('CICatcher()')
    return h


def help_lines(prog, typ, binfail=False):
    """Every help page as drawn (setup typ at the start, then Menu > Help, six pages): the body lines and the
    footer, as (page title, text)."""
    h = Harness(prog, seed=7, cas='fail')
    if binfail:
        h._table['BINOMIAL_CDF'] = lambda a, site: stats.binom.cdf(a[1], a[0], a[2]) if 0 <= a[2] <= 1 else 0.5
    h.press('Enter'); h.choose(typ); h.answer(ACCEPT)
    h.tap(130, 230)
    h.tap(300, 230); h.choose(3)
    h.press('Enter', 'Enter', 'Enter', 'Enter', 'Enter', 'Enter')
    h.tap(300, 230); h.choose(4)
    h.execute('CICatcher()')
    out = []
    for p in h.pages:
        # a help page: cqPage draws its title at y 8 in font 2, its lines at x 12 from y 28, its footer at y 220
        if not any(t.text.startswith('any key or tap') and t.y == 220 for t in p.texts):
            continue
        tt = [t.text for t in p.texts if t.y == 8 and t.font == 2]
        title = tt[0] if tt else '?'
        out += [(title, t.text) for t in p.texts if 28 <= t.y <= 220 and t.x == 12]
    return h, out


def part_x():
    print('\n' + '=' * 78)
    print('X. 2c: the fleet review\'s C-C1 and C-C2, and its regressions')
    print('=' * 78)
    # X1. check_CICatcher.py's E2 and a stricter E3, on beta 2c and beta 2b
    lm, lh = review_e2_e3(PROG)
    print('    beta 2c: CHOOSE items over 27: %s; fixed strings over 46: %s' % (lm, lh))
    check(all(n <= 31 for n, _ in lm), 'X1 review E2 on beta 2c: every CHOOSE item fits the box (<= 31): %s' % lm)
    check(not lh, 'X1 review E3 (at 46, the header\'s limit) on beta 2c: no fixed help string over 46: %s' % lh)
    if V2B is None:
        skip('X1: beta 2b not found; its failures are not shown')
    else:
        lm0, lh0 = review_e2_e3(V2B)
        check([s for n, s in lm0 if n > 31] == [OLD_MENU],
              'X1 beta 2b fails the same E2: %s' % [(n, s) for n, s in lm0 if n > 31])
        check(lh0 == [(47, OLD_ENG)], 'X1 beta 2b fails the same E3 at 46: %s' % lh0)
    # X2. C-C1 in a run
    h = menu_run(PROG)
    menus = [c for c in h.chooses if c.title == 'CICatcher']
    shown = [it for c in h.chooses for it in c.items]
    titles = [c.title for c in h.chooses]
    check(h.error is None and len(menus) == 2 and menus[0].items[0] == NEW_MENU and len(NEW_MENU) == 28,
          'X2 C-C1: the main menu\'s first line is %r (%d characters)' % (menus[0].items[0] if menus else None, len(NEW_MENU)))
    check(titles == ['Which interval?', 'CICatcher', 'Which interval?', 'CICatcher'],
          'X2 C-C1: item 1 still opens the setup ("Which interval?"): %s' % titles)
    check((h.result or '').startswith('CICatcher: ') and 'Exact, p = 0.10, n = 20' in h.result and not any(h.leftover()),
          'X2 C-C1: Cancel in the new setup keeps the run, and Quit returns it: %r' % h.result)
    check(max(len(t) for t in shown) <= 28, 'X2 every CHOOSE line shown in the run is 28 characters or fewer (longest %d: %r)'
          % (max(len(t) for t in shown), max(shown, key=len)))
    if V2B is not None:
        h0 = menu_run(V2B)
        m0 = [c for c in h0.chooses if c.title == 'CICatcher']
        check(m0 and m0[0].items[0] == OLD_MENU, 'X2 beta 2b, the same run: the first line is %r (%d characters)'
              % (m0[0].items[0] if m0 else None, len(OLD_MENU)))
    # X3. C-C2 as drawn: every help line, with the BINOMIAL check passing (Exact, then t) and failing
    worst = []
    for typ, binfail, what in ((5, False, 'Exact, BINOMIAL check passing'), (2, False, 't (the engine line)'),
                               (4, True, 'Wilson, BINOMIAL check failing')):
        hh, lines = help_lines(PROG, typ, binfail)
        last = [b for _t, b in lines if b.startswith(('exact ends:', 'exact: OFF'))]
        mx = max(len(b) for _t, b in lines)
        worst.append(mx)
        check(hh.error is None and len(lines) >= 6 * 10 and mx <= 46,
              'X3 C-C2 [%s]: %d help lines drawn, the longest %d characters (<= 46)' % (what, len(lines), mx))
        if binfail:
            check(last == ['exact: OFF (BINOMIAL_CDF failed its check)'], 'X3 the engine line when the check fails: %s' % last)
        else:
            check(last == [NEW_ENG], 'X3 C-C2: help page 4\'s last line is %r (%d characters)' % (last[:1], len(NEW_ENG)))
    if V2B is not None:
        hh, lines = help_lines(V2B, 5)
        over = sorted({b for _t, b in lines if len(b) > 46})
        check(over == [OLD_ENG], 'X3 beta 2b, the same pages: lines over 46: %s' % [(len(b), b) for b in over])
    # X4. the review's own check_CICatcher.py, on beta 2c and on beta 2b
    rv = None
    for d in (HERE, '/home/claude/work/review'):
        if os.path.exists(os.path.join(d, 'check_CICatcher.py')):
            rv = os.path.join(d, 'check_CICatcher.py')
            break
    if rv is None:
        skip('X4: the review\'s check_CICatcher.py not found')
        return
    src0 = open(rv, encoding='utf-8').read()
    m = re.search(r"^SRC = '([^']*)'$", src0, re.M)
    if not m:
        skip('X4: check_CICatcher.py has no SRC line to point at a file')
        return
    res = {}
    for nm, path in (('2c', PROG), ('2b', V2B)):
        if path is None:
            continue
        s2 = src0.replace(m.group(0), 'SRC = %r' % path)
        d = tempfile.mkdtemp()
        p2 = os.path.join(d, 'check_CICatcher_on_%s.py' % nm)
        open(p2, 'w', encoding='utf-8').write(s2)
        r = subprocess.run([sys.executable, p2], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
        fails = [ln[5:].strip() for ln in r.stdout.split('\n') if ln.startswith('FAIL ')]
        summ = [ln for ln in r.stdout.split('\n') if 'checks passed' in ln]
        res[nm] = (r.returncode, fails, summ[-1] if summ else r.stdout[-300:] + r.stderr[-300:])
        print('    check_CICatcher.py on beta %s: %s' % (nm, res[nm][2]))
    check(res['2c'][0] == 0 and not res['2c'][1], 'X4 the review\'s check_CICatcher.py on beta 2c: every check passes (%s)'
          % res['2c'][2])
    if '2b' in res:
        check(res['2b'][0] == 1 and len(res['2b'][1]) == 1 and res['2b'][1][0].startswith('E2 every CHOOSE item fits'),
              'X4 on beta 2b: only E2 fails, as the review left it: %s' % res['2b'][1])


# ============================================================================ G (2c)
def part_g2c():
    print('\n' + '=' * 78)
    print('G. 2c: beta 2c against beta 2b')
    print('=' * 78)
    if V2B is None:
        skip('G (2c): CICatcher_beta2b.txt not found')
        return
    t0, t1 = open(V2B, encoding='utf-8').read(), open(PROG, encoding='utf-8').read()

    def bodies(txt, keep_comments=False):
        c = txt if keep_comments else re.sub(r'//[^\n]*', '', txt)
        return {m.group(1): (m.group(0) if keep_comments else _norm(m.group(0))) for m in re.finditer(
            r'(?m)^(?:EXPORT\s+|LOCAL\s+)?([A-Za-z]\w*)\(([^()\n]*)\)\s*\nBEGIN\n.*?^END;', c, re.S)}
    N0, N1 = bodies(t0), bodies(t1)
    d = sorted(n for n in set(N0) | set(N1) if N0.get(n) != N1.get(n))
    check(d == ['cqMenu', 'cqXEngS'], 'G2c: routines that differ from beta 2b: %s (want cqMenu, cqXEngS)' % d)
    check(N1['cqMenu'] == N0['cqMenu'].replace('"%s"' % OLD_MENU, '"%s"' % NEW_MENU), 'G2c: cqMenu: the one menu line (C-C1)')
    check(N1['cqXEngS'] == N0['cqXEngS'].replace('"%s"' % OLD_ENG, '"%s"' % NEW_ENG), 'G2c: cqXEngS: the one line (C-C2)')
    R0, R1 = bodies(t0, True), bodies(t1, True)
    same = sorted(n for n in R0 if n not in d)
    check(set(R0) == set(R1) and all(R0[n] == R1[n] for n in same),
          'G2c: the other %d routines are byte-identical, comments included' % len(same))

    def outside(t, names):
        c = re.sub(r'//[^\n]*', '', t)
        c = re.sub(r'(?ms)^(?:EXPORT\s+|LOCAL\s+)?(?:%s)\([^\n]*\)\s*\nBEGIN\n.*?^END;' % '|'.join(names), '', c)
        return re.sub(r'\s+', ' ', c)
    check(outside(t0, d) == outside(t1, d), 'G2c: outside those two routines only comments differ (the header, two notes)')
    check(re.findall(r'(?s)#PYTHON.*?#END', t0) == re.findall(r'(?s)#PYTHON.*?#END', t1), 'G2c: no #PYTHON block, as before')
    check('// CICATCHER - beta 2c' in t1 and 'beta 2b\n' not in t1.split('// Author')[0],
          'G2c: the banner says beta 2c')
    # Roger, 19 Oct 2026: the disclaimer line beside the distribution terms (a comment; no page states the terms)
    check(t1.split('// Firmware:')[0].endswith('//   warranty: check any result you intend to rely on.\n' + '// DISCLAIMER: a teaching and demonstration aid. Not validated for\n//   forensic, clinical or legal use; do not rely on its results for\n//   legal purposes.\n' + '//\n')
          and not re.search(r'(?i)educational|personal use|warranty', ' '.join(re.findall(r'"([^"]*)"', re.sub(r'//[^\n]*', '', t1)))),
          'G2c: the header carries Roger\'s DISCLAIMER line under the terms; no on-screen string states the terms, so no '
          'page needs "Teaching aid; not for legal use."')
    print('  differ from beta 2b: %s; %d routines byte-identical' % (', '.join(d), len(same)))


def main():
    t0 = time.time()
    part_a(); part_b(); out = part_c(); part_d(out); part_e(); part_f(); part_g(); part_r(); part_g2b(); part_s()
    part_x(); part_g2c()
    # 2c: S again over every run, the X runs included
    mine = [h for h in ALL_H if h._src == PROG]
    sci = [(v, d, t) for h in mine for v, d, t in h.sci_strings]
    check(sci == [], 'S (2c, all parts): %d beta 2c harness runs, %d scientific STRING results' % (len(mine), len(sci)))
    print('\n' + '=' * 78)
    print('%s: %d checks, %d failures, %d skipped  [%.0f s]' % ('PASS' if not FAILS else 'FAIL', NCHK[0], len(FAILS),
                                                              len(SKIPS), time.time() - t0))
    for f in FAILS:
        print('  -', f)
    for s_ in SKIPS:
        print('  SKIP', s_)
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
