#!/usr/bin/env python3
"""verify_CICatcher_beta2a.py -- checks for CICatcher beta 2a (HP Prime PPL), 17 Oct 2026: the CAS call
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

Run:  python3 verify_CICatcher_beta2a.py
"""
import math, os, re, sys, time, subprocess, tempfile
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.join(HERE, 'CICatcher_beta2a.txt')
V2 = os.path.join(HERE, 'CICatcher_beta2.txt')
sys.path.insert(0, '/home/claude/work/harness')
from ppl_run_v3b import Harness, ACCEPT, PPLError, prime_print   # noqa: E402
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
        check(bool(hp) and hp[0].find('exact ends: bisection on BINOMIAL_CDF (checked)') is not None,
              'help page 4 shown, with its engine line')
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
    s = open(os.path.join(HERE, 'verify_CICatcher.py'), encoding='utf-8').read()
    s = s.replace("os.path.join(HERE, 'CICatcher_beta1.txt')", repr(PROG))
    s = s.replace("    h.press('Enter', 'Enter', 'Enter', 'Enter', 'Enter')\n",
                  "    h.press('Enter', 'Enter', 'Enter', 'Enter', 'Enter', 'Enter')   # beta 2: six help pages\n")
    d = tempfile.mkdtemp()
    path = os.path.join(d, 'verify_CICatcher_on_beta2.py')
    open(path, 'w').write(s)
    t0 = time.time()
    r = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=HERE)
    oks = r.stdout.count('  ok    ')
    last = [ln for ln in r.stdout.split('\n') if ln.startswith(('PASS', 'FAIL'))]
    print('  ' + (last[-1] if last else r.stdout[-500:]))
    check(r.returncode == 0, 'beta 1\'s suite passes on beta 2: %d checks (one script change: six help pages)  [%.0f s]'
          % (oks, time.time() - t0))


# ============================================================================ G (2a)
def part_g():
    print('\n' + '=' * 78)
    print('G. 2a: beta 2 in harness v3b, and beta 2a against beta 2')
    print('=' * 78)
    h = session('giac', 0)
    g = h.globals_
    rows = [r for r in range(1, 51) if round(g['cqEst'][int((g['cqHead'] - r) % 50)] * 20) == 0]
    h2 = session('giac', rows[0], prog=V2)
    cf = [t.text for p in h2.pages for t in p.texts if t.text.startswith(('upper = ', 'lower = '))]
    check(any(t.startswith('upper = 1-(50/2000)^(1/20)') for t in cf) and any('non-literal' in w for w in h2.warnings),
          '2a: beta 2 in v3b shows its own CAS text, "upper = 1-(50/2000)^(1/20)", unreduced, as if the CAS '
          'had answered -- the emulator\'s finding')
    exec(G_CODE, globals())


G_CODE = "\n# ================================================================ G (round 2a)\nsay('\\nG. beta 2a: beta 2 in harness v3b, and beta 2a against beta 2')\nimport re as _re\n_b_old = open(V2, encoding='utf-8').read()\n_b_new = open(PROG, encoding='utf-8').read()\n\n\ndef _bodies(txt):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', txt)\n    c = _re.sub(r'//[^\\n]*', '', c)\n    out = {}\n    for m in _re.finditer(r'(?m)^(?:EXPORT\\s+|LOCAL\\s+)?([A-Za-z]\\w*)\\(([^()\\n]*)\\)\\s*\\nBEGIN\\n.*?^END;', c, _re.S):\n        out[m.group(1)] = _re.sub(r'[ \\t]+\\n', '\\n', m.group(0))\n    return out\n\n\n_B0, _B1 = _bodies(_b_old), _bodies(_b_new)\n_diff = sorted(n for n in set(_B0) | set(_B1) if _B0.get(n) != _B1.get(n))\ncheck(_diff == ['cqCas'], 'beta 2a: routines that differ from beta 2: %s (want cqCas)' % _diff)\n\n\ndef _outside(t, names):\n    c = _re.sub(r'(?s)#PYTHON.*?#END', '', _re.sub(r'//[^\\n]*', '', t))\n    if names:\n        c = _re.sub(r'(?ms)^(?:EXPORT\\s+|LOCAL\\s+)?(?:%s)\\([^\\n]*\\)\\s*\\nBEGIN\\n.*?^END;' % '|'.join(names), '', c)\n    return _re.sub(r'\\s+', ' ', c)\n\n\ncheck(_outside(_b_old, _diff) == _outside(_b_new, _diff), 'beta 2a: outside those routines only comments differ')\n_py0 = _re.findall(r'(?s)#PYTHON.*?#END', _b_old)\n_py1 = _re.findall(r'(?s)#PYTHON.*?#END', _b_new)\ncheck(_py0 == _py1, 'beta 2a: the #PYTHON blocks are unchanged')\nsay('  routines that differ from beta 2: %s; everything else differs only in comments' % ', '.join(_diff))\n"


def main():
    t0 = time.time()
    part_a(); part_b(); out = part_c(); part_d(out); part_e(); part_f(); part_g()
    print('\n' + '=' * 78)
    print('%s: %d checks, %d failures  [%.0f s]' % ('PASS' if not FAILS else 'FAIL', NCHK[0], len(FAILS), time.time() - t0))
    for f in FAILS:
        print('  -', f)
    return 1 if FAILS else 0


if __name__ == '__main__':
    sys.exit(main())
