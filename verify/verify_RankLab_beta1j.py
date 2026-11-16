#!/usr/bin/env python3
"""verify_RankLab_beta1j.py -- checks RankLab beta 1j (Round 16, 15 Nov 2026): Page's L and the runs test, their four
presets and two kinds of "Use my data", ten help pages, and a mended label of the Null page.  Runs from the repository
alone (Lessons Learned s14 rule 18): tools/, programs/ and verify/ by relative path, beta 1i from git (main at 4e8ff66).
Needs hp-prime-kit (HPKIT), SciPy, NumPy, statsmodels.  About six minutes.

  T1  verify/round16/make_ranklab_1j.py, run again from beta 1i, makes programs/RankLab_beta1j.txt byte for byte.
  A   the arithmetic, every routine called through the harness (rule 19) against references written here in exact
      fractions.  PAGE'S L: the counted one-block lists; L, its mean, its variance and both exact tails for tables
      without ties (also against SciPy's page_trend_test) and with ties (the conditional null, block by block, and by
      brute force over every configuration; the variance against the exact null's own); Hollander, Wolfe & Chicken's
      example with a tie; the largest table counted, for each k, against the numbers the header and the help print;
      the mean Spearman rs against SciPy.  THE RUNS TEST: the null for every n1, n2 up to 12 against the counting
      formula and against every arrangement written out; random sequences; 2,000 values; statsmodels' z; how a list
      of numbers becomes a sequence, and what is refused.
  P   the pages of the four presets, line for line against numbers computed here from the same data; the pictures
      (squares, run lengths, chart, the mean ranks in order), the null pages, taps and arrow keys.
  V   every way in and out: the two menu items, the presets, both kinds of your own data, every refusal with its
      sentence and nothing changed, Esc during a count, the Enter menus, the soft keys, the closing lines, Home's
      variables; the mended fault (beta 1i writes "infinite" for a U of 119,657).
  R   regression against beta 1i: the monkey, 40 seeds, on beta 1i and on beta 1j with its new entrances shut and beta
      1i's help text: the same verdict, boxes and closing line, every screen the same text for text but the opening page.
  H   the help: 10 pages; the old pages word for word where they were not meant to change; every line within 296
      pixels, 13 lines a page.
  G   static.     D   layout: text_overlap_v1 and label_fit_v1 over every beta 1j screen drawn above.

  --save   writes the ten help pages to verify/round16/help_RankLab_beta1j.txt
"""
import os, sys, io, re, json, math, random, signal, subprocess, tempfile, warnings, itertools, collections
from fractions import Fraction
from decimal import Decimal, ROUND_HALF_UP
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import label_fit_v1 as LF  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

BASE = '4e8ff66'
PROG = os.path.join('programs', 'RankLab_beta1j.txt')
tmp = tempfile.mkdtemp(prefix='rkv_')
OLD = os.path.join(tmp, 'RankLab_beta1i.txt')
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/RankLab_beta1i.txt'], check=True, capture_output=True).stdout)
SRC = io.open(PROG, encoding='utf-8').read()
OSRC = io.open(OLD, encoding='utf-8').read()
GW = json.load(open(os.path.join('verify', 'round11', 'glyph_widths_vc.json')))
FAIL, NPASS = [], [0]
MINUS, AL, H0, H1, LE, GE, TX, ARROW = chr(8722), chr(945), 'H' + chr(8320), 'H' + chr(8321), chr(8804), chr(8805), chr(215), chr(8594)
UD, LR = chr(8645), chr(8646)
K1, K2, K3, K4, K5, K6 = (26, 228), (80, 228), (133, 228), (186, 228), (240, 228), (293, 228)
OV.install()


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:900]) if (detail != '' and not ok) else ''), flush=True)
    if ok: NPASS[0] += 1
    else: FAIL.append(name)


def key(h, name):
    for k in h.globals_:
        if k.lower() == name.lower(): return k
    raise KeyError(name)


def G(h, name): return h.globals_[key(h, name)]
def setg(h, name, v): h.globals_[key(h, name)] = v
def px(s, font=1): return sum((GW.get(str(ord(ch))) or [8, 9, 10])[int(font) - 1] for ch in s)
def close(a, b, tol=1e-10): return abs(a - b) <= tol * max(1.0, abs(a), abs(b))
def rel(a, b): return abs(a - b) / max(abs(b), 1e-300)


def fx(v, d):
    """a number as the Prime writes it with d decimals: rounded half away from zero, the Prime's minus, commas"""
    q = Decimal(repr(float(v))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    if q == 0: q = abs(q)
    t = '{:,f}'.format(q)
    return t.replace('-', MINUS)


def sg(v, d):
    t = fx(v, d)
    return t if t.startswith(MINUS) else '+' + t


def num(v):
    """rk_Num: whole numbers without a point, others to 4 decimals at the most, trailing zeros dropped; with commas"""
    if float(v) == int(v): return '{:,d}'.format(int(v)).replace('-', MINUS)
    t = fx(v, 4)
    return t.rstrip('0').rstrip('.') if '.' in t else t


def pt(p): return 'p < 0.0001' if p < 0.0001 else 'p = ' + fx(p, 4)


def fresh(path=PROG, d=None):
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=d)
    h.execute('rk_Init()')
    return h


def run(script, path=PROG, d=None):
    h = Harness(path, idle_key=4, home_minus=True, cas='fail', app_data=d)
    h.press('Enter')                     # the welcome page takes the first key
    script(h)
    try: res = h.execute('RankLab()'); err = None
    except Exception as e: res, err = None, '%s: %s' % (type(e).__name__, str(e)[:200])
    return h, res, err


def views(h):
    """the pages the view showed (the screens with soft keys), each as its lines of text, in order, repeats dropped"""
    out = []
    for s in h.screens:
        if s.func == 'rk_View':
            L = [t.text for t in s.texts]
            if not out or out[-1][0] != L or out[-1][1] != s.menu: out.append((L, s.menu, s))
    return out


def boxes(h): return [' '.join(m.lines) for m in h.msgboxes]


# ---------------- the references: exact fractions, written here ----------------
def midranks(row): return [Fraction(v).limit_denominator(2) for v in stats.rankdata(row)]


ONE = {}
def block_dist(ranks):
    """the distribution of sum_j j x (rank in place j) over every order of this block's own (mid)ranks: {value: Fraction}"""
    kk = tuple(sorted(ranks))
    if kk not in ONE:
        k = len(ranks); c = collections.Counter()
        for p in itertools.permutations(ranks):
            c[sum((j + 1) * p[j] for j in range(k))] += 1
        tot = sum(c.values())
        ONE[kk] = {v: Fraction(n, tot) for v, n in c.items()}
    return ONE[kk]


def page_ref(table, exact=True):
    """rows = blocks, columns = treatments in the order.  L, its mean and its variance by the formulas, and (exact) the
    conditional null as a dict, from which the two tails (not for more than 9 treatments: 10! orders a block)."""
    b = len(table); k = len(table[0]); L = Fraction(0); var = Fraction(0); dist = {Fraction(0): Fraction(1)}; nt = 0; rs = []
    for row in table:
        r = midranks(row); Li = sum((j + 1) * r[j] for j in range(k)); L += Li
        T = sum(t ** 3 - t for t in collections.Counter(r).values()); nt += 1 if T else 0
        var += Fraction(k * (k + 1) * (k * (k * k - 1) - T), 144)
        if exact:
            bd = block_dist(r); nd = collections.defaultdict(Fraction)
            for v, p in dist.items():
                for w, q in bd.items(): nd[v + w] += p * q
            dist = nd
        if T < k ** 3 - k: rs.append(stats.spearmanr(row, list(range(1, k + 1)))[0])
    mean = Fraction(b * k * (k + 1) ** 2, 4)
    up = sum(p for v, p in dist.items() if v >= L) if exact else None; lo = sum(p for v, p in dist.items() if v <= L) if exact else None
    return dict(L=L, mean=mean, var=var, up=up, lo=lo, dist=dist if exact else None, nt=nt, rs=float(np.mean(rs)) if rs else None)


def page_brute(table):
    """every configuration written out: all (k!)^b orders of the blocks' own midranks"""
    k = len(table[0]); rk = [midranks(row) for row in table]
    L = sum(sum((j + 1) * r[j] for j in range(k)) for r in rk)
    per = [[sum((j + 1) * p[j] for j in range(k)) for p in itertools.permutations(r)] for r in rk]
    up = lo = tot = 0
    for combo in itertools.product(*per):
        s_ = sum(combo); tot += 1; up += s_ >= L; lo += s_ <= L
    return Fraction(up, tot), Fraction(lo, tot)


def runs_pmf(n1, n2):
    """P(runs = r) by the counting formula, in whole numbers"""
    n = n1 + n2; tot = math.comb(n, n1); pmf = {}
    for r in range(2, n + 1):
        if r % 2 == 0:
            kk = r // 2; c = 2 * math.comb(n1 - 1, kk - 1) * math.comb(n2 - 1, kk - 1)
        else:
            kk = (r - 1) // 2; c = math.comb(n1 - 1, kk) * math.comb(n2 - 1, kk - 1) + math.comb(n1 - 1, kk - 1) * math.comb(n2 - 1, kk)
        if c: pmf[r] = Fraction(c, tot)
    return pmf


def runs_brute(n1, n2):
    """every arrangement of n1 ones among n written out, its runs counted"""
    n = n1 + n2; c = collections.Counter()
    for pos in itertools.combinations(range(n), n1):
        seq = [0] * n
        for q in pos: seq[q] = 1
        c[1 + sum(1 for a, b in zip(seq, seq[1:]) if a != b)] += 1
    tot = sum(c.values())
    return {r: Fraction(v, tot) for r, v in c.items()}


def runs_ref(seq):
    """seq: 1 or 2 for each place"""
    n = len(seq); n1 = seq.count(1); n2 = n - n1
    r = 1 + sum(1 for a, b in zip(seq, seq[1:]) if a != b)
    mu = Fraction(2 * n1 * n2, n) + 1; var = Fraction(2 * n1 * n2 * (2 * n1 * n2 - n), n * n * (n - 1))
    pmf = runs_pmf(n1, n2)
    lo = sum(p for v, p in pmf.items() if v <= r); up = sum(p for v, p in pmf.items() if v >= r)
    lens = [(g, len(list(it))) for g, it in itertools.groupby(seq)]
    best = max(l for _, l in lens); st = 1; first = None
    for g, l in lens:
        if l == best and first is None: first = (g, st)
        st += l
    return dict(r=r, n1=n1, n2=n2, mu=mu, var=var, lo=lo, up=up, long=best, lk=first[0], ls=first[1], lens=lens)


def set_table(h, table):
    b = len(table); k = len(table[0])
    setg(h, 'rkFM', [float(v) for row in table for v in row]); setg(h, 'rkFB', float(b)); setg(h, 'rkFK', float(k)); setg(h, 'rkFNoP', 0.0)
    setg(h, 'rkFTn', ['T%d' % (j + 1) for j in range(k)]); setg(h, 'rkFBn', ['B%d' % (i + 1) for i in range(b)])


SHARED = []
def shared():
    """one harness for the arithmetic calls (building one takes 0.6 s; the routines called set everything they read)"""
    if not SHARED: SHARED.append(fresh())
    return SHARED[0]


def do_page(table, h=None):
    h = h or shared(); set_table(h, table)
    setg(h, 'rkTest', 7.0)
    ok = h.execute('rk_DoPage()')
    return h, ok


def do_runs(seq, h=None):
    h = h or shared()
    setg(h, 'rkUSq', [float(v) for v in seq]); setg(h, 'rkTest', 8.0)
    ok = h.execute('rk_DoRuns()')
    return h, ok


print('=== T. the build')
out = os.path.join(tmp, 'built')
subprocess.run([sys.executable, os.path.join(HERE, 'round16', 'make_ranklab_1j.py'), out], check=True, capture_output=True)
check('T1 the build makes programs/RankLab_beta1j.txt byte for byte',
      open(os.path.join(out, 'RankLab_beta1j.txt'), 'rb').read() == open(PROG, 'rb').read())

print('=== A. the arithmetic')
h = fresh()
ok = True; tot = []
for k in range(3, 10):
    got = [int(v) for v in h.execute('rk_LOne(%d)' % k)]
    bd = block_dist([Fraction(j) for j in range(1, k + 1)])
    lo_ = k * (k + 1) * (k + 2) // 6; hi_ = k * (k + 1) * (2 * k + 1) // 6
    want = [int(bd.get(Fraction(v), 0) * math.factorial(k)) for v in range(lo_, hi_ + 1)]
    ok = ok and got == want and sum(got) == math.factorial(k); tot.append(len(got))
check('A1 rk_LOne: the counted one-block lists for k = 3 to 9 (%s values) are every order of the ranks 1..k, counted again here; an empty list for k = 2 and k = 10'
      % ', '.join(str(v) for v in tot), ok and h.execute('rk_LOne(2)') == [] and h.execute('rk_LOne(10)') == [], tot)

# A2: no ties
rng = random.Random(1611)
worst = dict(L=0, sd=0, z=0, up=0, lo=0, sp=0, eff=0); ncase = 0; nsp = 0; bad = []
for k, bs in ((3, (2, 3, 5, 12, 40, 77)), (4, (2, 7, 20, 33)), (5, (2, 6, 17)), (6, (2, 5, 10)), (7, (2, 6)), (8, (2, 4)), (9, (2, 3))):
    for b in bs:
        for rep_ in range(3 if b <= 12 else 1):
            table = [rng.sample(range(1, 1000), k) for _ in range(b)]
            if rep_ == 1: table = [sorted(r) if rng.random() < 0.7 else r for r in table]          # a rising trend
            if rep_ == 2: table = [sorted(r, reverse=True) if rng.random() < 0.7 else r for r in table]
            ref = page_ref(table); hh, okk = do_page(table); ncase += 1
            if okk != 1 or G(hh, 'rkEx') != 1: bad.append((k, b, okk, G(hh, 'rkEx'), G(hh, 'rkExWhy'))); continue
            worst['L'] = max(worst['L'], abs(G(hh, 'rkSt') - float(ref['L']))); worst['sd'] = max(worst['sd'], rel(G(hh, 'rkSd'), float(ref['var']) ** 0.5))
            worst['z'] = max(worst['z'], abs(G(hh, 'rkZ2') - (float(ref['L'] - ref['mean'])) / float(ref['var']) ** 0.5))
            worst['up'] = max(worst['up'], rel(G(hh, 'rkPeU'), float(ref['up']))); worst['lo'] = max(worst['lo'], rel(G(hh, 'rkPeL'), float(ref['lo'])))
            worst['eff'] = max(worst['eff'], abs(G(hh, 'rkEff') - ref['rs']))
            if abs(G(hh, 'rkMu') - float(ref['mean'])) > 1e-9 or abs(sum(G(hh, 'rkNull')) - 1) > 1e-10: bad.append((k, b, 'mean or total'))
            if b * k <= 60:
                sp = stats.page_trend_test(table, method='exact'); nsp += 1
                worst['sp'] = max(worst['sp'], rel(G(hh, 'rkPeU'), sp.pvalue), abs(G(hh, 'rkSt') - sp.statistic))
                spa = stats.page_trend_test(table, method='asymptotic')
                worst['sp'] = max(worst['sp'], rel(stats.norm.sf(G(hh, 'rkZ2')), spa.pvalue))
check('A2 Page\'s L without ties, %d tables (k 3 to 9, b 2 to 77; random, rising and falling): L, mean, SD, z and both exact tails against the fractions (largest relative error of a tail %.1e), the total probability 1; %d of them against SciPy\'s page_trend_test, exact and asymptotic (%.1e); the mean Spearman rs against SciPy\'s spearmanr, block by block (%.1e)'
      % (ncase, max(worst['up'], worst['lo']), nsp, worst['sp'], worst['eff']),
      not bad and ncase >= 40 and nsp >= 20 and worst['L'] < 1e-9 and worst['sd'] < 1e-12 and worst['z'] < 1e-9 and worst['up'] < 1e-10 and worst['lo'] < 1e-10 and worst['sp'] < 1e-9 and worst['eff'] < 1e-10, (bad[:3], worst))

# A3: ties
worst = dict(up=0, lo=0, var=0, sd=0, eff=0); ncase = 0; nexact = 0; nall = 0; bad = []; smaller = 0; nbr = 0; wbr = 0
for k, bs, top in ((3, (2, 3, 4, 8, 20, 40), 3), (4, (2, 3, 6, 12), 3), (5, (2, 4, 7), 4), (6, (2, 3), 4), (7, (2,), 5)):
    for b in bs:
        for rep_ in range(4):
            table = [[rng.randint(1, top) for _ in range(k)] for _ in range(b)]
            if rep_ == 3: table[0] = [5] * k                                                     # a block that ties everything
            if all(len(set(r)) == 1 for r in table): table[-1] = list(range(1, k + 1))
            ref = page_ref(table); hh, okk = do_page(table); ncase += 1
            if okk != 1: bad.append((k, b, 'refused')); continue
            mean_d = sum(v * p for v, p in ref['dist'].items()); var_d = sum((v - mean_d) ** 2 * p for v, p in ref['dist'].items())
            if mean_d != ref['mean']: bad.append((k, b, 'mean of the null'))
            worst['var'] = max(worst['var'], abs(float(var_d - ref['var'])))                      # the variance formula IS the exact null's variance
            worst['sd'] = max(worst['sd'], rel(G(hh, 'rkSd'), float(ref['var']) ** 0.5))
            untied = Fraction(b * k * k * (k + 1) * (k * k - 1), 144); smaller += 1 if ref['var'] < untied else 0
            if ref['rs'] is not None: worst['eff'] = max(worst['eff'], abs(G(hh, 'rkEff') - ref['rs']))
            if G(hh, 'rkLNt') != ref['nt']: bad.append((k, b, 'tied blocks'))
            nall += 1 if any(len(set(r)) == 1 for r in table) else 0
            if G(hh, 'rkEx') == 1:
                nexact += 1
                worst['up'] = max(worst['up'], rel(G(hh, 'rkPeU'), float(ref['up']))); worst['lo'] = max(worst['lo'], rel(G(hh, 'rkPeL'), float(ref['lo'])))
                if G(hh, 'rkNSt') != 0.5 or abs(sum(G(hh, 'rkNull')) - 1) > 1e-10: bad.append((k, b, 'scale or total'))
                if math.factorial(k) ** b <= 50000:
                    bu, bl = page_brute(table); nbr += 1
                    wbr = max(wbr, rel(G(hh, 'rkPeU'), float(bu)), rel(G(hh, 'rkPeL'), float(bl)))
check('A3 Page\'s L with ties, %d tables (k 3 to 7; %d with a block that ties everything): the variance formula is the exact conditional null\'s own variance (largest difference %.0e) and smaller than the untied one in every table; the exact tails of the %d tables counted, against the conditional null in fractions (%.1e) and, for %d of them, against every configuration written out (%.1e); the mean Spearman rs with ties (%.1e)'
      % (ncase, nall, worst['var'], nexact, max(worst['up'], worst['lo']), nbr, wbr, worst['eff']),
      not bad and ncase >= 60 and nexact >= 40 and nbr >= 15 and smaller == ncase and worst['var'] == 0 and worst['sd'] < 1e-12 and worst['up'] < 1e-10 and worst['lo'] < 1e-10 and wbr < 1e-10 and worst['eff'] < 1e-10, (bad[:3], worst, smaller, nexact, nbr))

# A4: the book's example with a tie (Hollander, Wolfe & Chicken, section 7.2, Comment 19), and the untied null of Comment 17
hw = [[2.4, 3.6, 2.4], [4.0, 5.9, 1.7]]
hh, okk = do_page(hw); ref = page_ref(hw); bu, bl = page_brute(hw)
g19 = (G(hh, 'rkSt'), G(hh, 'rkPeU'), G(hh, 'rkPeL'))
c17 = page_ref([[1, 2, 3], [1, 2, 3]])
h17, _ = do_page([[1, 2, 3], [1, 2, 3]])
g17 = (G(h17, 'rkSt'), G(h17, 'rkPeU'), G(h17, 'rkMu'), G(h17, 'rkSd'))
check('A4 Hollander, Wolfe & Chicken\'s example with a tie (k = 3, n = 2, rank vectors (1.5, 3, 1.5) and (2, 3, 1)): L = 23 as they find, and the exact conditional P(L >= 23) = %s = %.4f over the 36 configurations; their no-ties case k = 3, n = 2: L = 28 has probability 1/36, mean 24, variance 4'
      % (bu, float(bu)), okk == 1 and g19[0] == 23 and ref['up'] == bu and close(g19[1], float(bu), 1e-12) and close(g19[2], float(bl), 1e-12)
      and g17[0] == 28 and close(g17[1], 1 / 36, 1e-12) and g17[2] == 24 and close(g17[3], 2.0, 1e-12) and c17['var'] == 4, (g19, g17, float(bu)))

# A5: the largest table counted, for each k: the numbers the header prints, tried at that size and at one block more
def exact_at(k, b, tied=False):
    table = [rng.sample(range(1, 1000), k) for _ in range(b)]
    if tied: table[0][1] = table[0][0]
    hh_, okk_ = do_page(table)
    return okk_ == 1 and G(hh_, 'rkEx') == 1, G(hh_, 'rkExWhy')
m_hdr = re.search(r'no ties: up to ([\d, \n/]+?) blocks for k = 3, 4, \.\.\., 9 treatments', SRC)
hdr = [int(v) for v in re.findall(r'\d+', m_hdr.group(1))] if m_hdr else []
m_help = re.search(r'up to (\d+) blocks; 5: (\d+); 9: (\d+); fewer with ties', SRC)
LIMS = dict(zip(range(3, 10), hdr)); why = set(); at = {}; over = {}
for k in range(3, 10):
    at[k] = exact_at(k, LIMS[k])[0]; o_ = exact_at(k, LIMS[k] + 1); over[k] = o_[0]; why.add(o_[1])
LIMT = {3: 41, 4: 17, 5: 8, 6: 5, 7: 2}                 # with one block that has a tie: the build prints these
tied_ok = all(exact_at(k, b, True)[0] and not exact_at(k, b + 1, True)[0] for k, b in LIMT.items()) and not exact_at(8, 2, True)[0] and not exact_at(9, 2, True)[0]
hh10, ok10 = do_page([rng.sample(range(1, 1000), 10) for _ in range(2)])
check('A5 the largest table whose exact null is counted: without ties b = %s for k = 3..9, as the header says, counted at that size and not at one block more ("%s"); the help page gives the same for 3, 5 and 9 columns (%s, %s, %s); with a tie in one block b = %s for k = 3..7 and none at k = 8 or 9; k = 10 gets "%s"'
      % (', '.join(str(v) for v in hdr), '; '.join(sorted(why)), m_help.group(1), m_help.group(2), m_help.group(3), ', '.join(str(LIMT[k]) for k in sorted(LIMT)), G(hh10, 'rkExWhy')),
      hdr == [77, 33, 17, 10, 6, 4, 3] and all(at.values()) and not any(over.values()) and [int(m_help.group(i)) for i in (1, 2, 3)] == [LIMS[3], LIMS[5], LIMS[9]]
      and why == {'none for a table this large (normal)'} and tied_ok and ok10 == 1 and G(hh10, 'rkEx') == 0 and G(hh10, 'rkExWhy') == 'none for more than 9 treatments (normal)', (hdr, at, over, tied_ok))

# A6: the runs test's null
worst = 0; npair = 0; bad = []
for n1 in range(1, 13):
    for n2 in range(1, 13):
        if n1 + n2 < 3: continue
        hh = shared(); okk = hh.execute('rk_RuNull(%d,%d)' % (n1, n2)); pm = runs_pmf(n1, n2); npair += 1
        nl = G(hh, 'rkNull'); den = G(hh, 'rkNDen')
        if okk != 1 or G(hh, 'rkNLo') != 2 or G(hh, 'rkNSt') != 1 or len(nl) != (2 * min(n1, n2) + (1 if n1 != n2 else 0)) - 1: bad.append((n1, n2, 'shape')); continue
        for j, v in enumerate(nl):
            want = float(pm.get(j + 2, Fraction(0)))
            if want == 0:
                if v != 0: bad.append((n1, n2, j + 2))
            else: worst = max(worst, rel(v / den, want))
brute = 0
for n1, n2 in ((1, 2), (2, 2), (3, 3), (2, 5), (4, 6), (6, 6), (5, 7), (3, 9), (1, 8)):
    brute += 1
    if runs_brute(n1, n2) != runs_pmf(n1, n2): bad.append((n1, n2, 'the counting formula'))
check('A6 the runs test\'s exact null, rk_RuNull, for every n1 and n2 from 1 to 12 (%d pairs): each probability against the counting formula in whole numbers (largest relative error %.1e); the counting formula itself against every arrangement written out, %d pairs up to 12 values'
      % (npair, worst, brute), not bad and npair == 143 and worst < 1e-12, (bad[:3], worst))

# A7: sequences through rk_DoRuns
worst = dict(mu=0, sd=0, z=0, lo=0, up=0); ncase = 0; bad = []
for trial in range(120):
    n = rng.choice([3, 4, 5, 8, 13, 25, 40, 60, 150, 400]); p1 = rng.choice([0.1, 0.3, 0.5, 0.5, 0.7])
    seq = [1 if rng.random() < p1 else 2 for _ in range(n)]
    if trial % 7 == 0: seq = sorted(seq)                                   # two runs
    if trial % 11 == 0: seq = [1 + (i % 2) for i in range(n)]              # the most runs
    if len(set(seq)) < 2: seq[0] = 3 - seq[0]
    ref = runs_ref(seq); hh, okk = do_runs(seq); ncase += 1
    if okk != 1 or G(hh, 'rkSt') != ref['r'] or G(hh, 'rkUN1') != ref['n1'] or G(hh, 'rkUN2') != ref['n2'] or G(hh, 'rkEx') != 1: bad.append((trial, 'counts')); continue
    worst['mu'] = max(worst['mu'], rel(G(hh, 'rkMu'), float(ref['mu']))); worst['sd'] = max(worst['sd'], rel(G(hh, 'rkSd'), float(ref['var']) ** 0.5))
    worst['z'] = max(worst['z'], abs(G(hh, 'rkZ2') - float(ref['r'] - ref['mu']) / float(ref['var']) ** 0.5))
    worst['lo'] = max(worst['lo'], rel(G(hh, 'rkPeL'), float(ref['lo']))); worst['up'] = max(worst['up'], rel(G(hh, 'rkPeU'), float(ref['up'])))
    if (G(hh, 'rkULong'), G(hh, 'rkULk'), G(hh, 'rkULs')) != (ref['long'], ref['lk'], ref['ls']): bad.append((trial, 'longest run'))
    st = G(hh, 'rkUSt'); ru = G(hh, 'rkURun'); pos = 1
    for i_, (g_, l_) in enumerate(ref['lens']):
        if st[i_] != pos or any(ru[q] != i_ + 1 for q in range(pos - 1, pos - 1 + l_)): bad.append((trial, 'runs list')); break
        pos += l_
    if trial < 25 and [hh.execute('rk_RuEnd(%d)' % (i_ + 1)) for i_ in range(len(ref['lens']))] != list(itertools.accumulate(l_ for _, l_ in ref['lens'])): bad.append((trial, 'rk_RuEnd'))
    if G(hh, 'rkEff') != ref['r'] / float(ref['mu']) and rel(G(hh, 'rkEff'), ref['r'] / float(ref['mu'])) > 1e-12: bad.append((trial, 'ratio'))
check('A7 the runs test on %d random sequences of 3 to 400 values (sorted and alternating ones among them): the runs, the two counts, the longest run and where it is, the list of runs (where each starts and, by rk_RuEnd, ends), the mean, SD and z, and both exact tails against the fractions (largest relative error %.1e)'
      % (ncase, max(worst['lo'], worst['up'])), not bad and worst['mu'] < 1e-12 and worst['sd'] < 1e-12 and worst['z'] < 1e-9 and worst['lo'] < 1e-10 and worst['up'] < 1e-10, (bad[:3], worst))

# A8: 2,000 values, and one more
wl = 0; cases = []
for n1, n2 in ((1000, 1000), (300, 1700), (1, 1999), (999, 1001), (50, 1950)):
    hh = shared(); okk = hh.execute('rk_RuNull(%d,%d)' % (n1, n2)); pm = runs_pmf(n1, n2); nl = G(hh, 'rkNull'); den = G(hh, 'rkNDen')
    cum = 0.0; lo_ref = Fraction(0); k_ = 0
    for r in sorted(pm):
        lo_ref += pm[r]; cum += nl[r - 2] / den
        if float(lo_ref) > 1e-290 and float(lo_ref) < 0.9999: wl = max(wl, rel(cum, float(lo_ref))); k_ += 1
    cases.append((n1, n2, k_))
seq = [1] * 1000 + [2] * 1001; random.Random(5).shuffle(seq)
hh, okk = do_runs(seq)
g2001 = (okk, G(hh, 'rkEx'), G(hh, 'rkExWhy'), G(hh, 'rkPeL'))
import statsmodels.sandbox.stats.runs as SMR  # noqa: E402
wz = 0; nsm = 0
for trial in range(12):
    n = rng.choice([20, 45, 80]); x = [rng.randint(0, 1) for _ in range(n)]
    if len(set(x)) < 2: x[0] = 1 - x[0]
    zs, ps = SMR.runstest_1samp(x, cutoff=0.5, correction=False)
    h2, _ = do_runs([1 if v == 1 else 2 for v in x]); nsm += 1
    wz = max(wz, abs(G(h2, 'rkZ2') - zs), abs(2 * stats.norm.sf(abs(G(h2, 'rkZ2'))) - ps))
check('A8 the runs test at its limit: the lower tail at every number of runs for n1, n2 = %s (2,000 values each) against whole-number counts (largest relative error %.1e, tails down to 1E-290); a sequence of 2,001 values gets the normal p only ("%s"); z and its two-sided p against statsmodels\' runstest_1samp without its correction, %d sequences (%.1e)'
      % ('; '.join('%d, %d' % (a, b) for a, b, _ in cases), wl, g2001[2], nsm, wz),
      wl < 1e-9 and g2001 == (1, 0, 'none for n > 2,000 (normal)', -1) and wz < 1e-9 and all(c[2] > 0 for c in cases), (wl, wz, cases))

# A9: a list of numbers becomes a sequence (rk_RuFrom); what is refused, and that a refusal changes nothing
def ru_from(vals, hh=None):
    hh = hh or fresh()
    okk = hh.execute('rk_RuFrom({' + ','.join(repr(float(v)) for v in vals) + '}, "src", "lab")')
    return hh, okk
def state(hh): return tuple(repr(G(hh, n_)) for n_ in ('rkUSq', 'rkUVal', 'rkUCut', 'rkUDrop', 'rkUNmA', 'rkUNmB', 'rkUSrc', 'rkULab', 'rkUHas', 'rkUCh', 'rkUCl'))
bad = []
hh, okk = ru_from([1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0])
if not (okk == 1 and G(hh, 'rkUSq') == [1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2] and G(hh, 'rkUVal') == [] and G(hh, 'rkUNmA') == '1' and G(hh, 'rkUNmB') == '0' and G(hh, 'rkUCh') == 0): bad.append('two values')
vals = [5, 7, 7, 9, 3, 7, 8, 2, 6, 10, 1, 7, 4]
hh, okk = ru_from(vals); med = float(np.median(vals))
if not (okk == 1 and G(hh, 'rkUCut') == med == 7 and G(hh, 'rkUVal') == [v for v in vals if v != 7] and G(hh, 'rkUSq') == [1 if v > 7 else 2 for v in vals if v != 7]
        and G(hh, 'rkUDrop') == 4 and G(hh, 'rkUNmA') == 'above' and G(hh, 'rkUNmB') == 'below' and G(hh, 'rkUCh') == 1 and G(hh, 'rkUHas') == 1): bad.append('median cut')
vals = [rng.gauss(50, 10) for _ in range(402)]
hh, okk = ru_from(vals)
if not (okk == 1 and G(hh, 'rkUCh') == 0 and len(G(hh, 'rkUSq')) == 402 and G(hh, 'rkUDrop') == 0 and close(G(hh, 'rkUCut'), float(np.median(vals)), 1e-14)): bad.append('402 values')
hh, okk = ru_from(vals[:401])                              # an odd count: the median is one of the values and is dropped, 400 are left
if not (okk == 1 and G(hh, 'rkUCh') == 1 and len(G(hh, 'rkUSq')) == 400 and G(hh, 'rkUDrop') == 1 and G(hh, 'rkUCut') == float(np.median(vals[:401]))): bad.append('401 values')
ref_msgs = {}
for nm, vals in (('two values only', [1, 2]), ('every value the same', [4] * 6), ('one side of the median', [1, 1, 1, 1, 1, 2, 3]), ('two left after the drop', [1, 5, 5, 5, 9])):
    hh = fresh(); ru_from([3, 1, 2, 5, 4, 6], hh); before_ = state(hh)
    n0 = len(hh.msgboxes); okk = hh.execute('rk_RuFrom({' + ','.join(repr(float(v)) for v in vals) + '}, "new", "new")')
    ref_msgs[nm] = ' '.join(hh.msgboxes[-1].lines) if len(hh.msgboxes) > n0 else None
    if okk != 0 or state(hh) != before_ or ref_msgs[nm] is None: bad.append(nm)
check('A9 rk_RuFrom: two different values are the two kinds as they are (the larger is kind 1); more are cut at their median, a value equal to it dropped (NumPy\'s median); 400 kept numbers open on the chart, 402 on the squares; a list of two values, of one value repeated, with all the rest on one side of the median, or with two left after the drop is refused with a sentence and the loaded sequence stays as it was',
      not bad and ref_msgs['two values only'] == 'The runs test needs at least 3 values, in the order they happened.' and ref_msgs['every value the same'] == 'Every value is the same: there are no runs to count.'
      and ref_msgs['one side of the median'] == 'With the values equal to the median (1) dropped, too few are left on its two sides for a runs test.'
      and ref_msgs['two left after the drop'] == 'With the values equal to the median (5) dropped, too few are left on its two sides for a runs test.', (bad, ref_msgs))

print('=== P. the pages of the four presets')
OZONE = [[-.08, .01, .06], [.21, .17, .19], [.50, -.11, .34], [.14, .07, .14]]          # Hollander, Wolfe & Chicken (2014) Table 7.2
m = re.search(r'rk_DraftNo\(\)\nBEGIN\n  RETURN \{(.*?)\};', SRC, re.S)
DRAFT = [int(v) for v in re.findall(r'\d+', m.group(1))]
MDAYS = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]; MST = [sum(MDAYS[:i]) for i in range(12)]
MONTHS = [[DRAFT[MST[mm] + d] for mm in range(12)] for d in range(28)]
MNAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
ROUL = [1 if c == 'R' else 2 for c in 'RRRRBRRRBBBBBRRBBBRRBBRRR']                        # HP-65 Stat Pac 2 (1975), p. 86
check('P0 the data: the 366 draft numbers are beta 1i\'s, each of 1..366 once; the roulette sequence has 14 R, 11 B and 9 runs, as the HP-65 book says',
      sorted(DRAFT) == list(range(1, 367)) and m.group(1) == re.search(r'rk_DraftNo\(\)\nBEGIN\n  RETURN \{(.*?)\};', OSRC, re.S).group(1) and ROUL.count(1) == 14 and ROUL.count(2) == 11 and runs_ref(ROUL)['r'] == 9)


def wrap_means(means):
    lines = []; s_ = 'Mean ranks, in order: '
    for j, v in enumerate(means):
        t = fx(v, 1) + (', ' if j < len(means) - 1 else '')
        if len(s_) + len(t) > 46: lines.append(s_); s_ = '  '
        s_ += t
    lines.append(s_)
    return lines[:2]


def page_lines(table, names, lab, src, tail, exact_why=None):
    ref = page_ref(table, exact=exact_why is None); b = len(table); k = len(table[0])
    sd = float(ref['var']) ** 0.5; z = float(ref['L'] - ref['mean']) / sd
    pn = stats.norm.sf(z) if tail == 2 else stats.norm.cdf(z); pe = float(ref['up'] if tail == 2 else ref['lo']) if exact_why is None else None
    word = 'rising' if tail == 2 else 'falling'
    full = 'Order: ' + (' ' + ARROW + ' ').join(n_[:10] for n_ in names)
    order = full if len(full) <= 44 else 'Order: ' + (' ' + ARROW + ' ').join([names[0][:10], names[1][:10], '...', names[-1][:10]])
    means = [float(sum(midranks(row)[j] for row in table)) / b for j in range(k)]
    L = ['Page\'s L: results', src, lab, 'b = %d blocks, k = %d treatments in the order listed' % (b, k), order,
         'L = %s  (mean %s, SD %s%s)' % (num(ref['L']), num(ref['mean']), fx(sd, 2), ('; ties in %d block%s' % (ref['nt'], '' if ref['nt'] == 1 else 's')) if ref['nt'] else ''),
         ('Exact ' + pt(pe) + '  (' + word + ')') if exact_why is None else 'Exact p: ' + exact_why,
         'Normal: z = %s, %s (no cont. corr.)' % (sg(z, 3), pt(pn)), 'Mean Spearman rs with the order = ' + sg(ref['rs'], 3)]
    L += wrap_means(means)
    pm = pe if exact_why is None else pn
    L += [H0 + ': no trend.  ' + H1 + ': the ranks ' + ('rise' if tail == 2 else 'fall') + ' in that order.',
          ('p < 0.05: evidence against ' + H0 + ' (at ' + AL + ' = 0.05)') if pm < 0.05 else ('p ' + GE + ' 0.05: no evidence against ' + H0 + ' (not proof)'),
          'Choose the order and the direction before the', 'data are seen.  The blocks must be independent.', UD + ' = page, Ent = menu, 0 = help, Esc = back']
    return L, ref, dict(z=z, pn=pn, pe=pe, sd=sd, means=means)


def runs_lines(seq, lab, src, tail, vals=None, cut=None, drop=0, names=('R', 'B'), exact=True):
    ref = runs_ref(seq); n = len(seq); mu = float(ref['mu']); sd = float(ref['var']) ** 0.5; z = (ref['r'] - mu) / sd
    lo, up = float(ref['lo']), float(ref['up'])
    pe = min(1, 2 * min(lo, up)) if tail == 0 else (lo if tail == 1 else up)
    pn = min(1, 2 * stats.norm.sf(abs(z))) if tail == 0 else (stats.norm.cdf(z) if tail == 1 else stats.norm.sf(z))
    word = {0: 'two-sided', 1: 'lower tail', 2: 'upper tail'}[tail]
    L = ['Runs test: results', src, lab]
    if vals is not None:
        L += ['Median %s: above or below (equal: dropped)' % num(cut), 'n = %s: %s above, %s below%s' % (num(n), num(ref['n1']), num(ref['n2']), (' (dropped: %s)' % num(drop)) if drop else '')]
    else:
        L += ['Two kinds of values, in the order they came', 'n = %s: %s of %s, %s of %s' % (num(n), num(ref['n1']), names[0], num(ref['n2']), names[1])]
    L += ['runs = %s  (mean %s, SD %s under %s)' % (num(ref['r']), fx(mu, 2), fx(sd, 2), H0), ('Exact ' + pt(pe) + '  (' + word + ')') if exact else 'Exact p: none for n > 2,000 (normal)',
          'Normal: z = %s, %s (no cont. corr.)' % (sg(z, 3), pt(pn))]
    ratio = Decimal(repr(ref['r'] / mu)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    L += ['Runs / mean = %s (%s)' % (fx(ref['r'] / mu, 2), 'below 1: like values cluster' if ratio < 1 else ('above 1: the kinds alternate' if ratio > 1 else 'as many runs as chance gives'))]
    nm = names[0] if ref['lk'] == 1 else names[1]
    L += ['Longest run: 1 (no two neighbors are the same kind)' if ref['long'] == 1 else 'Longest run: %s of %s, places %s to %s' % (num(ref['long']), nm, num(ref['ls']), num(ref['ls'] + ref['long'] - 1))]
    pm = pe if exact else pn
    L += [H0 + ': the order is random  (' + word + ')',
          ('p < 0.05: evidence against ' + H0 + ' (at ' + AL + ' = 0.05)') if pm < 0.05 else ('p ' + GE + ' 0.05: no evidence against ' + H0 + ' (not proof)'),
          'Lower tail = too few runs (clusters, a drift);', 'upper tail = too many (the kinds alternate).', 'Exact p: every order of the two kinds (n ' + LE + ' 2,000).',
          UD + ' = page, Ent = menu, 0 = help, Esc = back']
    return L, ref, dict(z=z, pn=pn, pe=pe, mu=mu, sd=sd, lo=lo, up=up)


# P1: ozone
hz, rz, ez = run(lambda h: (h.choose(7), h.choose(8), h.press('Down'), h.press('Right'), h.press('Right'), h.press('Right'), h.press('Left'), h.press('Down'), h.press('Minus'), h.press('Plus'), h.press('Up'), h.press('Up'), h.press('Esc'), h.choose(12)))
vz = views(hz)
want, refz, xz = page_lines(OZONE, ['0.1 ppm', '0.6 ppm', '1.0 ppm'], 'change in airway resistance after ozone', 'Goldsmith & Nadel 1969 (Hollander et al. 2014)', 2)
check('P1 ozone, the Result page, line for line against the reference: %s' % ' | '.join(want[5:9]), ez is None and vz[0][0] == want and vz[0][1] == ['Result', 'Plot', 'Null', 'Exact', 'Rising', 'More'], (ez, [(a, b) for a, b in zip(vz[0][0], want) if a != b][:3]))
check('P2 ozone, the numbers: L = 48 and its mean 48; variance 15/2 with the tie (8 without); exact P(L >= 48) = 14/27 with the tie kept, where the untied null gives 83/144 (what R\'s PageTest and SciPy print: %.4f)'
      % stats.page_trend_test(OZONE, method='exact').pvalue,
      refz['L'] == 48 and refz['mean'] == 48 and refz['var'] == Fraction(15, 2) and refz['up'] == Fraction(14, 27) and refz['lo'] == Fraction(14, 27)
      and close(stats.page_trend_test(OZONE, method='exact').pvalue, 83 / 144, 1e-12) and G(hz, 'rkFM') == [v for row in OZONE for v in row])
pic = vz[1][0]
rs_ = [float(sum(midranks(row)[j] for row in OZONE)) for j in range(3)]
want_pic = ['Page\'s L: mean ranks in the order listed', 'dot = mean rank;  ' + TX + '1, ' + TX + '2 ... = weight in L;  dotted: ' + H0]
check('P3 ozone, the picture: the three treatments left to right with their weights ' + TX + '1, ' + TX + '2, ' + TX + '3; the panel reads the picked one (rank sums %s; Right moves from the first to the third and stops there, Left comes back to the second)' % ', '.join(num(v) for v in rs_),
      pic[:2] == want_pic and [t for t in pic if t in ('0.1 ppm', '0.6 ppm', '1.0 ppm', TX + '1', TX + '2', TX + '3')] == ['0.1 ppm', TX + '1', '0.6 ppm', TX + '2', '1.0 ppm', TX + '3']
      and '0.1 ppm: rank sum 9.5, mean rank 2.38 (' + H0 + ' 2)' in pic and 'place 1 in the order: adds 1 ' + TX + ' 9.5 = 9.5 to L' in pic and 'L = 48 (mean 48): exact p = 0.5185, rising' in pic
      and '0.6 ppm: rank sum 5, mean rank 1.25 (' + H0 + ' 2)' in vz[2][0] and 'place 2 in the order: adds 2 ' + TX + ' 5 = 10 to L' in vz[2][0]
      and '1.0 ppm: rank sum 9.5, mean rank 2.38 (' + H0 + ' 2)' in vz[3][0] and 'place 3 in the order: adds 3 ' + TX + ' 9.5 = 28.5 to L' in vz[3][0]
      and vz[4][0] == vz[2][0] and len(vz) >= 9, pic)
nul = vz[5][0]
check('P4 ozone, the Null page: the bars of the exact null (step 0.5 with the tie), then - turns the direction (Falling, the same p by symmetry) and + the normal curve: "%s" / "%s" / "%s"' % (nul[1], vz[6][0][-4], vz[7][0][1]),
      nul[0] == 'Page\'s L: null distribution' and nul[1] == 'Exact null of L: every order in each of the 4 blocks' and 'L = 48 (red): exact p = 0.5185, rising' in nul and G(hz, 'rkNSt') == 0.5
      and vz[6][1][4] == 'Falling' and 'L = 48 (red): exact p = 0.5185, falling' in vz[6][0] and vz[7][1][3] == 'Normal' and vz[7][0][1] == 'Normal approx. of L: mean 48, SD 2.74'
      and 'L = 48: normal p = 0.5000, falling' in vz[7][0] and 'shaded = p; the curve is the approximate null' in vz[7][0]
      and rz == 'RankLab: Page\'s L, b = 4, k = 3, L = 48, normal p = 0.5000 (falling)', (nul, vz[6][0], vz[7][0], rz))

# P5: the draft lottery's months
hm, rm, em = run(lambda h: (h.choose(7), h.choose(9), h.press('Down'), h.tap(215, 80), h.press('Down'), h.press('Right'), h.press('Plus'), h.press('Minus'), h.press('Up'), h.press('Up'), h.press('Esc'), h.choose(12)))
vm = views(hm)
want, refm, xm = page_lines(MONTHS, MNAMES, 'draft number: days 1-28 (blocks), 12 months', 'Fienberg 1971 Science 171:255; Starr 1997 JSE', 1, exact_why='none for more than 9 treatments (normal)')
check('P5 the 1970 draft lottery, months in order (days 1-28 as blocks), the Result page line for line: %s | %s | %s' % (want[5], want[7], want[8]),
      em is None and vm[0][0] == want and vm[0][1] == ['Result', 'Plot', 'Null', 'Normal', 'Falling', 'More'] and refm['L'] == 13440 and refm['mean'] == 14196
      and G(hm, 'rkFM') == [float(v) for row in MONTHS for v in row] and G(hm, 'rkFBn')[0] == 'day 1' and G(hm, 'rkFBn')[27] == 'day 28',
      (em, [(a, b) for a, b in zip(vm[0][0], want) if a != b][:3]))
j8 = 8; s8 = float(sum(midranks(row)[j8 - 1] for row in MONTHS))
check('P6 the months, the picture and the Null page: a tap on August\'s column picks it ("%s"); the normal curve with its mean and SD, the read-out starts at L; + has no exact null to switch to and says so; - turns to Rising, where p = %s'
      % ('Aug: rank sum %s, mean rank %s (%s 6.5)' % (num(s8), fx(s8 / 28, 2), H0), pt(stats.norm.sf(xm['z']))),
      'Aug: rank sum %s, mean rank %s (%s 6.5)' % (num(s8), fx(s8 / 28, 2), H0) in vm[2][0] and 'place 8 in the order: adds 8 %s %s = %s to L' % (TX, num(s8), num(8 * s8)) in vm[2][0]
      and vm[3][0][1] == 'Normal approx. of L: mean 14,196, SD %s' % fx(xm['sd'], 2) and 'L = 13,440: normal %s, falling' % pt(xm['pn']) in vm[3][0]
      and any(t.startswith('at 13,440: P(L ' + GE + ' 13,440) = ') for t in vm[4][0])
      and boxes(hm) == ['No exact null here: none for more than 9 treatments (normal).'] and 'L = 13,440: normal %s, rising' % pt(stats.norm.sf(xm['z'])) in vm[5][0]
      and rm == 'RankLab: Page\'s L, b = 28, k = 12, L = 13,440, normal %s (rising)' % pt(stats.norm.sf(xm['z'])), (vm[2][0][-4:], vm[3][0][:2], vm[4][0][-3:], boxes(hm), rm))

# P7: roulette
hr, rr, er = run(lambda h: (h.choose(7), h.choose(10), h.press('Down'), h.press('Right'), h.press('Right'), h.press('Right'), h.press('Right'), h.tap(10 + 12 * 12 + 5, 99), h.press('Down'), h.press('Minus'), h.press('Minus'), h.press('Plus'), h.press('Up'), h.press('Up'), h.press('Esc'), h.choose(12)))
vr = views(hr)
want, refr, xr = runs_lines(ROUL, 'roulette: red (R) or black (B), 25 spins', 'HP-65 Stat Pac 2 (1975), the run test\'s example', 0)
check('P7 the roulette example of the HP-65 Stat Pac 2, the Result page line for line: %s | %s | %s (the HP-65 book: mean 13.32, SD 2.41, z = -1.79)' % (want[5], want[6], want[7]),
      er is None and vr[0][0] == want and vr[0][1] == ['Result', 'Plot', 'Null', 'Exact', '2-side', 'More'] and fx(xr['mu'], 2) == '13.32' and fx(xr['sd'], 2) == '2.41' and fx(xr['z'], 2) == MINUS + '1.79'
      and refr['lo'] == Fraction(409, 7429) and G(hr, 'rkUSq') == ROUL, (er, [(a, b) for a, b in zip(vr[0][0], want) if a != b][:3]))
cells = vr[1]
sq = [sh for sh in cells[2].shapes if sh.cmd == 'RECT_P' and len(sh.args) >= 6 and sh.args[2] - sh.args[0] == 10 and sh.args[3] - sh.args[1] == 10]
RED, BLK = 0xFF0000, 0
lens = [l for _, l in refr['lens']]
check('P8 roulette, the squares: 25 of them in one row, 12 pixels apart, red and black in the sequence\'s order; under each run its length (%s); the panel follows the picked place through Right (run 1, then the lone B as run 2) and a tap on the 13th square ("%s")'
      % (' '.join(str(v) for v in lens), vr[6][0][-4]),
      len(sq) == 25 and [sh.args[0] for sh in sq] == [10 + 12 * i for i in range(25)] and len(set(sh.args[1] for sh in sq)) == 1
      and [sh.args[4] for sh in sq] == [RED if v == 1 else BLK for v in ROUL] and [sh.args[5] for sh in sq] == [RED if v == 1 else BLK for v in ROUL]
      and [t for t in cells[0] if re.fullmatch(r'\d', t)] == [str(v) for v in lens] and cells[0][:5] == ['Runs test: the sequence, in order', 'R (14)', 'B (11)', '9 runs', 'one square a value; under each run, its length']
      and cells[0][-4:] == ['Place 1 of 25: R', 'run 1 of 9: places 1 to 4, 4 long', 'runs = 9, mean 13.32: exact p = 0.1101, two-sided', 'tap a square, ' + LR + ' = pick, ' + UD + ' = page, Esc = back']
      and vr[5][0][-4:-2] == ['Place 5 of 25: B', 'run 2 of 9: this place alone'] and vr[6][0][-4:-2] == ['Place 13 of 25: B', 'run 4 of 9: places 9 to 13, 5 long'], (len(sq), cells[0], vr[5][0][-4:], vr[6][0][-4:]))
hin = fresh(); setg(hin, 'rkUSq', [float(v) for v in ROUL]); setg(hin, 'rkTest', 8.0); hin.execute('rk_DoRuns()')
tails = {}
for tl in (0, 1, 2):
    setg(hin, 'rkTail', float(tl)); tails[tl] = [r_ for r_ in range(2, 24) if hin.execute('rk_InTail(%d)' % r_) == 1]
check('P9 roulette, the Null page: the exact bars; two-sided marks the smaller tail only (runs <= 9: p = 2 x %.4f = %.4f) and says so, lower marks runs <= 9, upper runs >= 9; the normal curve of the second -: "%s"'
      % (xr['lo'], 2 * xr['lo'], vr[10][0][-4] if len(vr) > 10 else ''),
      vr[7][0][1] == 'Exact null of the runs: all C(25, 11) orders' and 'runs = 9 (red): exact p = 0.1101, two-sided' in vr[7][0] and 'magenta = the smaller tail; two-sided p = twice it' in vr[7][0]
      and tails[0] == list(range(2, 10)) and tails[1] == list(range(2, 10)) and tails[2] == list(range(9, 24))
      and 'runs = 9 (red): exact p = 0.0551, lower tail' in vr[8][0] and 'magenta = the p tail(s), marked under the axis' in vr[8][0] and 'runs = 9 (red): exact %s, upper tail' % pt(xr['up']) in vr[9][0]
      and vr[10][1][3] == 'Normal' and vr[10][0][1] == 'Normal approx. of runs: mean 13.32, SD 2.41' and 'runs = 9: normal %s, upper tail' % pt(stats.norm.sf(xr['z'])) in vr[10][0]
      and rr == 'RankLab: Runs test, n = 25, runs = 9, normal %s (upper tail)' % pt(stats.norm.sf(xr['z'])), ([v[0][1:3] for v in vr[7:11]], tails, rr))

# P10: the draft lottery's runs by day
med = float(np.median(DRAFT)); DSEQ = [1 if v > med else 2 for v in DRAFT]
hd, rd, ed = run(lambda h: (h.choose(7), h.choose(11), h.press('Down'), h.tap(150, 90), h.tap(*K6), h.tap(*K2), h.tap(10 + 8 * 20 + 3, 71 + 10 * 3 + 3), h.tap(*K2), h.press('Down'), h.press('Plus'), h.press('Up'), h.press('Up'), h.press('Esc'), h.choose(12)))
vd = views(hd)
want, refd, xd = runs_lines(DSEQ, 'draft number by birth date, Jan 1 to Dec 31', 'Fienberg 1971 Science 171:255; Starr 1997 JSE', 0, vals=DRAFT, cut=med, drop=0, names=('above', 'below'))
check('P10 the 1970 draft lottery, runs by day, the Result page line for line: %s | %s | %s | %s' % (want[4], want[5], want[6], want[9]),
      ed is None and vd[0][0] == want and med == 183.5 and G(hd, 'rkUVal') == [float(v) for v in DRAFT] and G(hd, 'rkUSq') == DSEQ, (ed, [(a, b) for a, b in zip(vd[0][0], want) if a != b][:3]))
chart = vd[1]
dots = [sh for sh in chart[2].shapes if sh.cmd == 'RECT_P' and sh.args[2] - sh.args[0] == 1 and sh.args[3] - sh.args[1] == 1]
segs = [sh for sh in chart[2].shapes if sh.cmd == 'LINE_P' and sh.args[4] == 0xB4B4B4]
place = round((150 - 46) / 260 * 365) + 1
rgeo = fresh(); setg(rgeo, 'rkUSq', [float(v) for v in DSEQ]); rgeo.execute('rk_RuGeo()')
y0 = G(rgeo, 'rkUY0'); cplace = int((71 + 33 - y0) // 10) * 37 + 20 + 1
run_of = lambda p_: next((i + 1, s_, s_ + l_ - 1) for i, (s_, l_) in enumerate(zip(itertools.accumulate([1] + [l for _, l in refd['lens']][:-1]), [l for _, l in refd['lens']])) if s_ <= p_ <= s_ + l_ - 1)
r1 = run_of(place); r2 = run_of(cplace)
def run_line(r_): return 'run %s of 172: places %s to %s, %s long' % (num(r_[0]), num(r_[1]), num(r_[2]), num(r_[2] - r_[1] + 1)) if r_[2] > r_[1] else 'run %s of 172: this place alone' % num(r_[0])
cellv = next(v for v in vd if v[1] == ['Help', 'Cells', '', '', 'Menu', 'More'])
sq = [sh for sh in cellv[2].shapes if sh.cmd == 'RECT_P' and len(sh.args) >= 6 and sh.args[2] - sh.args[0] == 6 and sh.args[3] - sh.args[1] == 6 and sh.args[1] >= 40]
BLUE, ORNG = 0x003CC8, 0xE07800
check('P11 the draft lottery, the pictures: the run chart first (366 dots in their sides\' colors, 365 line pieces, y against the value); a tap at x = 150 picks place %d ("%s"); More then the second key turns to the squares (366 of them, 37 a row), where a tap picks place %d; the key names the picture that is on (Chart, Cells)'
      % (place, 'Place %d of 366: %s, %s' % (place, num(DRAFT[place - 1]), 'above' if DSEQ[place - 1] == 1 else 'below'), cplace),
      chart[0][:5] == ['Runs test: the sequence, in order', 'above (183)', 'below (183)', '172 runs', 'the values in order; dotted = their median'] and len(dots) == 366 and len(segs) == 365
      and [sh.args[4] for sh in dots] == [BLUE if v == 1 else ORNG for v in DSEQ]
      and all((dots[i].args[1] < dots[j].args[1]) == (DRAFT[i] > DRAFT[j]) or abs(DRAFT[i] - DRAFT[j]) < 8 for i, j in [(rng.randrange(366), rng.randrange(366)) for _ in range(400)])
      and vd[2][0][-4:-2] == ['Place %d of 366: %s, %s' % (place, num(DRAFT[place - 1]), 'above' if DSEQ[place - 1] == 1 else 'below'), run_line(r1)]
      and vd[3][1] == ['Help', 'Chart', '', '', 'Menu', 'More'] and len(sq) == 366 and [sh.args[4] for sh in sq] == [BLUE if v == 1 else ORNG for v in DSEQ]
      and [sh.args[0] for sh in sq[:38]] == [10 + 8 * i for i in range(37)] + [10]
      and any(v[0][-4:-2] == ['Place %d of 366: %s, %s' % (cplace, num(DRAFT[cplace - 1]), 'above' if DSEQ[cplace - 1] == 1 else 'below'), run_line(r2)] for v in vd)
      and cellv[0][4] == 'one square a value, in order; a run = one color' and cellv[0][-1] == 'tap a square, ' + LR + ' = pick, ' + UD + ' = page, Esc = back' and chart[0][-1] == 'tap the chart, ' + LR + ' = pick, ' + UD + ' = page, Esc = back',
      (len(dots), len(segs), len(sq), vd[2][0][-4:], [v[1] for v in vd], place, cplace, r1, r2))
nd = next(v for v in vd if v[0][0] == 'Runs test: null distribution')
check('P12 the draft lottery, the Null page and the closing line: "%s"; the runs test by day sees nothing (two-sided p = %.4f) where Page\'s L by month does (p = %.5f)' % (nd[0][1], xd['pe'], xm['pn']),
      nd[0][1] == 'Exact null of the runs: all C(366, 183) orders' and 'runs = 172 (red): exact %s, two-sided' % pt(xd['pe']) in nd[0]
      and rd == 'RankLab: Runs test, n = 366, runs = 172, normal %s (two-sided)' % pt(xd['pn']) and xd['pe'] > 0.2 and xm['pn'] < 0.001, (nd[0][:3], rd))

print('=== V. every way in and out')
# V1: the two tests from the main menu with nothing loaded: each loads its example and says so
h1, r1_, e1 = run(lambda h: (h.choose(9), h.press('Esc'), h.choose(10), h.press('Esc'), h.choose(12)))
v1 = views(h1)
check('V1 main menu items 9 (Page\'s L) and 10 (the runs test) with nothing loaded: each loads its example with a sentence and opens on its Result page; Quit is item 12; the closing line is the last test\'s',
      e1 is None and boxes(h1) == ['No blocks yet: the ozone data loaded. (Load a preset or Use my data to change it.)', 'No sequence yet: the roulette example loaded. (Load a preset or Use my data to change it.)']
      and [v[0][0] for v in v1] == ['Page\'s L: results', 'Runs test: results'] and v1[0][1][4] == 'Rising' and v1[1][1][4] == '2-side'
      and r1_ == 'RankLab: Runs test, n = 25, runs = 9, exact p = 0.1101 (two-sided)' and [len(c.items) for c in h1.chooses] == [12, 12, 12]
      and h1.chooses[0].items[6:] == ['Load a preset', 'Use my data (D1..D9)', 'Page\'s L (ordered trend)', 'Runs test (randomness)', 'Help', 'Quit']
      and h1.chooses[0].items[:8] == re.findall(r'"([^"]*)"', re.search(r'CHOOSE\(mnI, "RankLab: rank-based tests", \{(.*?)\}\);', OSRC, re.S).group(1))[:8], (e1, boxes(h1), r1_))
# V2: Help is item 11; Esc at the main menu leaves; Esc at the presets and at Your data comes back to the menu
h2, r2_, e2 = run(lambda h: (h.choose(11), h.press('Esc'), h.choose(7), h.choose(0), h.choose(8), h.choose(0), h.choose(0)))
check('V2 Help is item 11 of the main menu; Esc at the preset menu (11 items, the old seven where they were) and at Your data (7 items, the old five where they were) comes back to the main menu; Esc there leaves with "RankLab: no test run"',
      e2 is None and r2_ == 'RankLab: no test run' and [c.title for c in h2.chooses] == ['RankLab: rank-based tests', 'RankLab: rank-based tests', 'Load a preset', 'RankLab: rank-based tests', 'Your data (Statistics 1Var)', 'RankLab: rank-based tests']
      and any(s.lines() and s.lines()[0].startswith('RankLab help 1/10') for s in h2.screens)
      and h2.chooses[2].items == re.findall(r'"([^"]*)"', re.search(r'CHOOSE\(prI, "Load a preset", \{(.*?)\}\);', OSRC, re.S).group(1)) + ['Ozone: airway resistance', 'Draft 1970: months in order', 'Roulette: red and black', 'Draft 1970: runs by day']
      and h2.chooses[4].items == re.findall(r'"([^"]*)"', re.search(r'CHOOSE\(myI, "Your data \(Statistics 1Var\)", \{(.*?)\}\);', OSRC, re.S).group(1)) + ['Page\'s L: rows = blocks', 'Runs: D1 in order'], (e2, r2_, [c.title for c in h2.chooses]))
# V3: your own data under Page's L
D3 = {'D1': [1.0, 2, 3, 4, 5], 'D2': [2.0, 3, 1, 5, 6], 'D3': [3.0, 4, 5, 6, 4]}
tab3 = [[D3['D1'][i], D3['D2'][i], D3['D3'][i]] for i in range(5)]
h3, r3_, e3 = run(lambda h: (h.choose(8), h.choose(6), h.press('Esc'), h.choose(5), h.press('Esc'), h.choose(12)), d=D3)
ref3 = page_ref(tab3); v3 = views(h3)
check('V3 Use my data > Page\'s L: rows = blocks, D1..D3 with 5 rows: L = %s, exact p = %.4f (rising), as the reference; the same table then opens under Friedman (item 5) without a new load; closing line "%s"' % (num(ref3['L']), float(ref3['up']), r3_),
      e3 is None and v3[0][0][0] == 'Page\'s L: results' and v3[0][0][2] == 'blocks = rows, treatments = D1..D3' and v3[0][0][4] == 'Order: D1 ' + ARROW + ' D2 ' + ARROW + ' D3'
      and v3[0][0][5].startswith('L = %s  (mean %s, SD %s' % (num(ref3['L']), num(ref3['mean']), fx(float(ref3['var']) ** 0.5, 2))) and v3[0][0][6] == 'Exact ' + pt(float(ref3['up'])) + '  (rising)'
      and v3[1][0][0] == 'Friedman and Kendall\'s W: results' and not boxes(h3) and r3_.startswith('RankLab: Friedman and Kendall\'s W, n = 5'), (e3, v3[0][0][:7], r3_))
# V4: refusals of Page's L
h4a, r4a, e4a = run(lambda h: (h.choose(8), h.choose(6), h.choose(12)), d={'D1': [1.0, 2, 3], 'D2': [2.0, 1, 3]})
h4b, r4b, e4b = run(lambda h: (h.choose(8), h.choose(6), h.choose(12)), d={'D1': [1.0, 2, 3]})
h4c, r4c, e4c = run(lambda h: (h.choose(7), h.choose(7), h.press('Esc'), h.choose(9), h.choose(12)))
h4d, r4d, e4d = run(lambda h: (h.choose(8), h.choose(6), h.choose(12)), d={'D1': [2.0, 5, 7], 'D2': [2.0, 5, 7], 'D3': [2.0, 5, 7]})
h4e, r4e, e4e = run(lambda h: (h.choose(7), h.choose(10), h.press('Esc'), h.choose(8), h.choose(6), h.choose(12)), d={'D1': [1.0, 2, 3], 'D2': [2.0, 1, 3]})
check('V4 Page\'s L refused, each with its sentence: two columns ("%s"); one column (the loader\'s own sentence); the halo preset ("%s", and the closing line stays the halo\'s W); every block all tied ("%s"); after a refusal the closing line is still the last test that ran ("%s")'
      % (boxes(h4a)[0], boxes(h4c)[0][:60] + '...', boxes(h4d)[0], r4e),
      e4a is None and boxes(h4a) == ['Page\'s L needs at least 3 treatments (columns, in the order expected) and 2 blocks (rows).'] and r4a == 'RankLab: no test run' and not views(h4a)
      and e4b is None and boxes(h4b) == ['Treatments in D1, D2, ... (side by side, no gap), one row per block, every column the same length.'] and r4b == 'RankLab: no test run'
      and e4c is None and boxes(h4c) == ['The halo preset is a description only (its criteria are not independent raters), so it gets no test.  Load another data set for Page\'s L.']
      and r4c.startswith('RankLab: Kendall\'s W = ') and len(views(h4c)) == 1
      and e4d is None and boxes(h4d) == ['Every block ties all its treatments: there is no ranking to test.'] and r4d == 'RankLab: no test run'
      and e4e is None and r4e == 'RankLab: Runs test, n = 25, runs = 9, exact p = 0.1101 (two-sided)', (boxes(h4a), boxes(h4b), boxes(h4c), boxes(h4d), r4e))
# V5: your own data under the runs test
B12 = [1.0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0]
h5, r5_, e5 = run(lambda h: (h.choose(8), h.choose(7), h.press('Down'), h.tap(*K6), h.tap(*K2), h.press('Esc'), h.choose(12)), d={'D1': B12})
ref5 = runs_ref([1 if v == 1 else 2 for v in B12]); v5 = views(h5)
want5, _, x5 = runs_lines([1 if v == 1 else 2 for v in B12], 'D1 in order', 'your data: D1, in its order', 0, names=('1', '0'))
N13 = [5.0, 7, 7, 9, 3, 7, 8, 2, 6, 10, 1, 7, 4]
h5n, r5n, e5n = run(lambda h: (h.choose(8), h.choose(7), h.press('Down'), h.tap(*K6), h.tap(*K2), h.tap(*K2), h.press('Esc'), h.choose(12)), d={'D1': N13})
seq13 = [1 if v > 7 else 2 for v in N13 if v != 7]; want5n, _, x5n = runs_lines(seq13, 'D1 in order', 'your data: D1, in its order', 0, vals=[v for v in N13 if v != 7], cut=7, drop=4, names=('above', 'below'))
v5n = views(h5n)
check('V5 Use my data > Runs: D1 in order.  Twelve 0s and 1s: the Result page line for line (%s); the second key of More is blank and does nothing (two kinds have no chart).  Thirteen numbers with four at the median: "%s", the chart first, More\'s second key to the squares and back'
      % (want5[4], want5n[4]),
      e5 is None and v5[0][0] == want5 and v5[1][0][0] == 'Runs test: the sequence, in order' and [v[1] for v in v5[1:]] == [['Result', 'Plot', 'Null', 'Exact', '2-side', 'More'], ['Help', '', '', '', 'Menu', 'More']]
      and r5_ == 'RankLab: Runs test, n = 12, runs = %d, exact %s (two-sided)' % (ref5['r'], pt(x5['pe']))
      and e5n is None and v5n[0][0] == want5n and 'the values in order; dotted = their median' in v5n[1][0]
      and [v[1][1] for v in v5n[2:]] == ['Chart', 'Cells', 'Chart'] and 'one square a value; under each run, its length' in v5n[3][0] and 'the values in order; dotted = their median' in v5n[4][0],
      (e5, [(a, b) for a, b in zip(v5[0][0], want5) if a != b][:2], [v[1] for v in v5], e5n, [(a, b) for a, b in zip(v5n[0][0], want5n) if a != b][:2], [v[1] for v in v5n]))
# V6: refusals of the runs test's loader through the menu
outs = []
for dd in ({}, {'D1': [1.0, 2.0]}, {'D1': [4.0] * 6}, {'D1': [1.0, 1, 1, 1, 1, 2, 3]}):
    hx, rx, ex = run(lambda h: (h.choose(8), h.choose(7), h.choose(12)), d=dd); outs.append((ex, boxes(hx), rx, len(views(hx))))
hx, rx, ex = run(lambda h: (h.choose(7), h.choose(10), h.press('Esc'), h.choose(8), h.choose(7), h.choose(10), h.press('Esc'), h.choose(12)), d={'D1': [4.0] * 6})
check('V6 the runs test refused through the menu, each with its sentence and no page opened: D1 empty ("%s"), two values, every value the same, the rest on one side of the median; and after a refusal the roulette sequence loaded before is still there (item 10 opens it again)' % outs[0][1][0],
      [o[1] for o in outs] == [['Put the sequence in D1 of the Statistics 1Var app first, in the order it happened.'], ['The runs test needs at least 3 values, in the order they happened.'],
                               ['Every value is the same: there are no runs to count.'], ['With the values equal to the median (1) dropped, too few are left on its two sides for a runs test.']]
      and all(o[0] is None and o[2] == 'RankLab: no test run' and o[3] == 0 for o in outs)
      and ex is None and sum(1 for s_ in hx.screens if s_.func == 'rk_View') == 2 and views(hx)[0][0][2] == 'roulette: red (R) or black (B), 25 spins' and rx == 'RankLab: Runs test, n = 25, runs = 9, exact p = 0.1101 (two-sided)', (outs, ex, rx))
# V7: the Enter menus
h7, r7_, e7 = run(lambda h: (h.choose(9), h.press('Enter'), h.choose(5), h.press('Enter'), h.choose(4), h.press('Enter'), h.choose(2), h.press('Enter'), h.choose(3), h.press('Enter'), h.choose(1), h.press('Enter'), h.choose(0), h.press('Enter'), h.choose(6), h.press('Esc'), h.press('Enter'), h.choose(7), h.choose(12)))
m7 = [c for c in h7.chooses if c.title == 'Page\'s L']
h7r, r7r, e7r = run(lambda h: (h.choose(7), h.choose(11), h.press('Enter'), h.choose(6), h.press('Enter'), h.choose(5), h.press('Enter'), h.choose(4), h.press('Enter'), h.choose(8), h.choose(12)))
m7r = [c for c in h7r.chooses if c.title == 'Runs test']
h7s, r7s, e7s = run(lambda h: (h.choose(10), h.press('Enter'), h.choose(7), h.choose(12)))
m7s = [c for c in h7s.chooses if c.title == 'Runs test']
check('V7 Enter\'s menu.  Page\'s L: %s; Direction turns Rising to Falling, Exact / normal to normal, each page by its item, Esc changes nothing, Help opens the help, the last item goes back.  The runs test of numbers has an eighth item, "%s"; of two kinds, seven'
      % (m7[0].items, m7r[0].items[5]),
      e7 is None and m7[0].items == ['Result page', 'Picture page', 'Null distribution', 'Exact / normal (now exact)', 'Direction (now rising)', 'Help', 'Back to the main menu']
      and m7[1].items[4] == 'Direction (now falling)' and m7[2].items[3] == 'Exact / normal (now normal)'
      and [v[0][0] for v in views(h7)] == ['Page\'s L: results', 'Page\'s L: results', 'Page\'s L: results', 'Page\'s L: mean ranks in the order listed', 'Page\'s L: null distribution', 'Page\'s L: results']
      and any(s.lines() and s.lines()[0].startswith('RankLab help 1/10') for s in h7.screens) and r7_ == 'RankLab: Page\'s L, b = 4, k = 3, L = 48, normal p = 0.5000 (falling)'
      and e7r is None and m7r[0].items == ['Result page', 'Picture page', 'Null distribution', 'Exact / normal (now exact)', 'Tails (now two-sided)', 'Picture: squares or chart', 'Help', 'Back to the main menu']
      and m7r[2].items[4] == 'Tails (now lower tail)' and m7r[3].items[3] == 'Exact / normal (now normal)' and r7r == 'RankLab: Runs test, n = 366, runs = 172, normal %s (lower tail)' % pt(stats.norm.cdf(xd['z']))
      and e7s is None and len(m7s[0].items) == 7 and m7s[0].items[5:] == ['Help', 'Back to the main menu'], (e7, [c.items for c in m7][:1], [v[0][0] for v in views(h7)], r7_, e7r, r7r, e7s))
# V8: the soft keys by taps, and the keys + - 0
h8, r8_, e8 = run(lambda h: (h.choose(10), h.tap(*K2), h.tap(*K3), h.tap(*K4), h.tap(*K5), h.tap(*K5), h.tap(*K5), h.tap(*K1), h.tap(*K6), h.tap(*K1), h.press('Esc'), h.tap(*K5), h.choose(10), h.press('Zero'), h.press('Esc'), h.tap(*K6), h.tap(*K6), h.tap(*K6), h.tap(*K5), h.choose(12)))
v8 = views(h8)
check('V8 the soft keys by taps on the runs test: Plot, Null, the 4th key (Exact to Normal), Tails three times (lower, upper, two-sided again), Result; More, then Help (the help opens), Menu (back to the main menu); 0 opens the help too; More twice comes back to the first row',
      e8 is None and [v[0][0] for v in v8[:4]] == ['Runs test: results', 'Runs test: the sequence, in order', 'Runs test: null distribution', 'Runs test: null distribution']
      and [v[1][3] for v in v8[:4]] == ['Exact', 'Exact', 'Exact', 'Normal'] and [v[1][4] for v in v8[4:8]] == ['Lower', 'Upper', '2-side', '2-side'] and v8[7][0][0] == 'Runs test: results'
      and v8[8][1] == ['Help', '', '', '', 'Menu', 'More'] and sum(1 for s in h8.screens if s.lines() and s.lines()[0].startswith('RankLab help 1/10')) == 2
      and v8[-1][1] == ['Help', '', '', '', 'Menu', 'More'] and r8_ == 'RankLab: Runs test, n = 25, runs = 9, exact p = 0.1101 (two-sided)', (e8, [(v[0][0], v[1]) for v in v8], r8_))
# V9: Esc during a count
big = [float(v) for v in ([1, 0] * 500 + [1, 1, 0, 0] * 250)]
h9, r9_, e9 = run(lambda h: (h.choose(8), h.choose(7), h.press('Esc', anytime=True), h.press('Esc'), h.choose(12)), d={'D1': big})
h9p, r9p, e9p = run(lambda h: (h.choose(7), h.choose(9), h.press('Esc', anytime=True), h.choose(12)))
t16 = {'D%d' % (j + 1): [float(v) for v in col] for j, col in enumerate(zip(*[random.Random(77 + i).sample(range(1, 100), 5) for i in range(16)]))}
h9q, r9q, e9q = run(lambda h: (h.choose(8), h.choose(6), h.press('Esc', anytime=True), h.press('Esc'), h.choose(12)), d=t16)
busy = [t.text for t in h9.texts if 'Exact null of the runs' in t.text or 'Esc = stop' in t.text]
check('V9 Esc during a count.  The runs\' exact null of 2,000 values: the bar ("%s"), Esc stops it, the page opens on the normal p and says "Exact p: stopped by Esc (normal used)".  Page\'s exact null of 16 blocks x 5: the same.  The ranking of the lottery\'s 28 blocks: "Stopped by Esc: nothing was computed." and no page'
      % busy[0],
      e9 is None and busy[:2] == ['Exact null of the runs ...', 'Esc = stop (the normal approximation stays)'] and views(h9)[0][0][6] == 'Exact p: stopped by Esc (normal used)' and views(h9)[0][1][3] == 'Normal'
      and r9_.startswith('RankLab: Runs test, n = 2,000, runs = 1,500, normal p')
      and e9q is None and views(h9q)[0][0][6] == 'Exact p: stopped by Esc (normal used)' and any(t.text.startswith('Exact null of L: block ') for t in h9q.texts) and ', normal p' in r9q
      and e9p is None and boxes(h9p) == ['Stopped by Esc: nothing was computed.'] and not views(h9p) and r9p == 'RankLab: no test run', (e9, busy[:2], views(h9)[0][0][6] if views(h9) else None, r9_, e9q, r9q, boxes(h9p), r9p))
# V10: sequences too long for the exact p and for the chart
long_ = [float(rng.randint(0, 1)) for _ in range(2500)]
h10, r10, e10 = run(lambda h: (h.choose(8), h.choose(7), h.press('Plus'), h.press('Down'), h.press('Down'), h.press('Esc'), h.choose(12)), d={'D1': long_})
num9 = [rng.gauss(50, 10) for _ in range(900)]
h10n, r10n, e10n = run(lambda h: (h.choose(8), h.choose(7), h.press('Down'), h.tap(*K6), h.tap(*K2), h.press('Esc'), h.choose(12)), d={'D1': num9})
v10 = views(h10); v10n = views(h10n)
bars = [sh for sh in v10[1][2].shapes if sh.cmd == 'RECT_P' and len(sh.args) >= 6 and sh.args[3] - sh.args[1] == 1 and sh.args[1] >= 48]
ref10 = runs_ref([1 if v == 1 else 2 for v in long_[:2000]])
cells_cov = sum((sh.args[2] - sh.args[0] + 2) // 3 for sh in bars)
check('V10 2,500 values: "Exact p: none for n > 2,000 (normal)", + says "%s", the squares show the first 2,000 ("%s"; %s bars, one for each piece of a run on a row, covering 2,000 squares), the Null page is the normal curve.  900 numbers: the squares first, and the chart is refused with "%s"'
      % (boxes(h10)[0], v10[1][0][4], format(len(bars), ','), boxes(h10n)[0]),
      e10 is None and v10[0][0][6] == 'Exact p: none for n > 2,000 (normal)' and boxes(h10) == ['No exact null here: none for n > 2,000 (normal).'] and v10[1][0][4] == 'the first 2,000 of 2,500 values, in order'
      and cells_cov == 2000 and len(bars) >= ref10['r'] and v10[2][0][1].startswith('Normal approx. of runs: mean ') and r10.startswith('RankLab: Runs test, n = 2,500, runs = ') and ', normal p' in r10
      and e10n is None and boxes(h10n) == ['The chart is drawn for up to 400 values (here n = 900): the squares show every one.'] and [v[1][1] for v in v10n[2:]] == ['Cells'] and sum(1 for s_ in h10n.screens if s_.func == 'rk_View') == 4
      and 'one square a value, in order; a run = one color' in v10n[1][0], (e10, v10[0][0][6], boxes(h10), v10[1][0][4], cells_cov, len(bars), ref10['r'], e10n, boxes(h10n)))
# V11: Home's variables
h11, r11, e11 = run(lambda h: (h.choose(7), h.choose(8), h.press('Esc'), h.choose(12)))
h11r, r11r, e11r = run(lambda h: (h.choose(7), h.choose(10), h.press('Minus'), h.press('Esc'), h.choose(12)))
rkz = [float(v) for row in OZONE for v in midranks(row)]
check('V11 Home after Page\'s L on the ozone data: RK_STAT = 48, RK_P = the exact p %.6f, RK_PN = 0.5, RK_EFF = the mean Spearman rs (0), RK_HL = 0, RK_RANKS = the midranks within the blocks.  After the runs test read in the lower tail: RK_STAT = 9, RK_P = %.6f, RK_PN = %.6f, RK_EFF = runs / mean = %.4f, RK_RANKS = {0}'
      % (float(refz['up']), xr['lo'], stats.norm.cdf(xr['z']), 9 / xr['mu']),
      G(h11, 'RK_STAT') == 48 and close(G(h11, 'RK_P'), 14 / 27, 1e-12) and close(G(h11, 'RK_PN'), 0.5, 1e-12) and abs(G(h11, 'RK_EFF')) < 1e-12 and G(h11, 'RK_HL') == 0 and G(h11, 'RK_RANKS') == rkz
      and G(h11r, 'RK_STAT') == 9 and close(G(h11r, 'RK_P'), xr['lo'], 1e-12) and close(G(h11r, 'RK_PN'), stats.norm.cdf(xr['z']), 1e-12) and close(G(h11r, 'RK_EFF'), 9 / xr['mu'], 1e-12) and G(h11r, 'RK_RANKS') == [0],
      (G(h11, 'RK_P'), G(h11, 'RK_RANKS'), G(h11r, 'RK_P'), G(h11r, 'RK_EFF')))
# V12: the mended fault: "infinite" for a statistic of 100,000 or more
r12 = random.Random(3); g1 = [r12.gauss(10, 3) for _ in range(500)]; g2 = [r12.gauss(10.1, 3) for _ in range(500)]
sc12 = lambda h: (h.choose(8), h.choose(1), h.press('Down'), h.press('Down'), h.press('Right'), h.press('Esc'), h.choose(10 if h is ho12 else 12))
ho12 = Harness(OLD, idle_key=4, home_minus=True, cas='fail', app_data={'D1': g1, 'D2': g2}); ho12.press('Enter'); sc12(ho12); ro12 = ho12.execute('RankLab()')
hn12 = Harness(PROG, idle_key=4, home_minus=True, cas='fail', app_data={'D1': g1, 'D2': g2}); hn12.press('Enter'); sc12(hn12); rn12 = hn12.execute('RankLab()')
u12 = stats.mannwhitneyu(g1, g2).statistic
old_n = [v for v in views(ho12) if v[0][0] == 'Mann-Whitney: null distribution']; new_n = [v for v in views(hn12) if v[0][0] == 'Mann-Whitney: null distribution']
check('V12 the mended fault.  Mann-Whitney on two groups of 500 (U%s = %s by SciPy): beta 1i\'s Null page labels the red line "%s" and Right starts the read-out at the window\'s edge ("%s"); beta 1j writes "%s" and starts at the statistic ("%s"); every other line of the two pages is the same, and so is the closing line'
      % (chr(8321), num(u12), [t for t in old_n[0][0] if 'infinite' in t][0], old_n[1][0][-2], [t for t in new_n[0][0] if t.startswith('U' + chr(8321) + ' = ') and 'normal' not in t][0], new_n[1][0][-2]),
      u12 >= 100000 and 'U' + chr(8321) + ' = infinite' in old_n[0][0] and 'U' + chr(8321) + ' = ' + num(u12) in new_n[0][0] and not any('infinite' in t for v in views(hn12) for t in v[0])
      and new_n[1][0][-2].startswith('at %s: P(U%s %s %s) = ' % (num(u12), chr(8321), GE, num(u12))) and not old_n[1][0][-2].startswith('at %s:' % num(u12))
      and [t for t in old_n[0][0] if 'infinite' not in t] == [t for t in new_n[0][0] if t != 'U' + chr(8321) + ' = ' + num(u12)] and ro12 == rn12, (old_n[0][0], new_n[0][0], old_n[1][0][-2], new_n[1][0][-2]))
# V13: the last number of the Null page's axis (two groups of 500 that do not overlap at all: U = 250,000, the axis ends on it)
a1 = [float(v) for v in range(1001, 1501)]; a2 = [float(v) for v in range(1, 501)]
sc13 = lambda h, q: (h.choose(8), h.choose(1), h.press('Up'), h.press('Esc'), h.choose(q))
ho13 = Harness(OLD, idle_key=4, home_minus=True, cas='fail', app_data={'D1': a1, 'D2': a2}); ho13.press('Enter'); sc13(ho13, 10); ro13 = ho13.execute('RankLab()')
hn13 = Harness(PROG, idle_key=4, home_minus=True, cas='fail', app_data={'D1': a1, 'D2': a2}); hn13.press('Enter'); sc13(hn13, 12); rn13 = hn13.execute('RankLab()')
ax = lambda h: [(t.text, t.x, px(t.text)) for s_ in h.screens if s_.func == 'rk_View' and s_.lines()[0] == 'Mann-Whitney: null distribution' for t in s_.texts if t.y == 150]
check('V13 the Null page\'s axis for U = 250,000: beta 1i writes its last number, "250,000", from x = %d, so it runs %d pixels off the screen; beta 1j would move it left onto "200,000" and leaves it out instead (the tick stays): %s; the numbers before it are where they were'
      % (ax(ho13)[-1][1], ax(ho13)[-1][1] + ax(ho13)[-1][2] - 320, ', '.join(t for t, x, w in ax(hn13))),
      ax(ho13)[-1][0] == '250,000' and ax(ho13)[-1][1] + ax(ho13)[-1][2] > 320 and ax(hn13) == ax(ho13)[:-1] and all(x + w <= 320 for t, x, w in ax(hn13)) and ro13 == rn13, (ax(ho13), ax(hn13)))
# V14: a table of more than 10,000 values
c34 = {'D%d' % (j + 1): [float(rng.randint(1, 9999)) for _ in range(3400)] for j in range(3)}
hc5, rc5, ec5 = run(lambda h: (h.choose(8), h.choose(5), h.choose(12)), d=c34)
hc6, rc6, ec6 = run(lambda h: (h.choose(8), h.choose(6), h.choose(12)), d=c34)
c33 = {k_: v[:3333] for k_, v in c34.items()}; t33 = [[c33['D1'][i], c33['D2'][i], c33['D3'][i]] for i in range(3333)]
hc7, rc7, ec7 = run(lambda h: (h.choose(8), h.choose(6), h.press('Esc'), h.choose(12)), d=c33)
ref33 = page_ref(t33, exact=False); z33 = float(ref33['L'] - ref33['mean']) / float(ref33['var']) ** 0.5
check('V14 Your data with 3 columns of 3,400 rows (10,200 values): Friedman and Page\'s L are refused with "%s" and nothing opens; 3 columns of 3,333 rows (9,999 values) open under Page\'s L: L = %s as the reference, the normal p only ("%s")'
      % (boxes(hc5)[0], num(ref33['L']), views(hc7)[0][0][6]),
      ec5 is None and ec6 is None and boxes(hc5) == boxes(hc6) == ['Friedman and Page\'s L take a table of 10,000 values at the most (rows ' + TX + ' columns); this one has 10,200.'] and rc5 == rc6 == 'RankLab: no test run'
      and not views(hc5) and not views(hc6) and ec7 is None and views(hc7)[0][0][5].startswith('L = %s  (mean %s, SD %s' % (num(ref33['L']), num(ref33['mean']), fx(float(ref33['var']) ** 0.5, 2)))
      and views(hc7)[0][0][6] == 'Exact p: none for a table this large (normal)' and rc7 == 'RankLab: Page\'s L, b = 3,333, k = 3, L = %s, normal %s (rising)' % (num(ref33['L']), pt(stats.norm.sf(z33))),
      (boxes(hc5), rc5, ec7, rc7))

print('=== R. regression against beta 1i')
# beta 1j with its new entrances shut: the main routine, the preset menu, Your data and the help are beta 1i's
def routine(src, head):
    a = src.index('\n' + head) + 1
    return src[a:src.index('\nEND;\n', a) + 6]
SHUT = SRC
for head in ('rk_Preset()\nBEGIN', 'rk_MyData()\nBEGIN', 'rk_HPage(hpT, hpL, hpN)\nBEGIN', 'rk_Help()\nBEGIN', 'EXPORT RankLab()\nBEGIN'):
    assert SHUT.count(routine(SRC, head)) == 1
    SHUT = SHUT.replace(routine(SRC, head), routine(OSRC, head))
SHUTP = os.path.join(tmp, 'RankLab_beta1j_shut.txt'); io.open(SHUTP, 'w', encoding='utf-8', newline='').write(SHUT)
argv = sys.argv; sys.argv = ['monkey_v1b.py']
import monkey_v1b as MK  # noqa: E402
sys.argv = argv
def skip(lines): return bool(lines) and lines[0][0].startswith('RankLab - rank tests, beta')
def one(path, seed):
    rng_ = random.Random(seed)
    app, kind_ = MK.random_lists(rng_)
    hh_ = MK.Monkey(path, rng_, app, 150)
    for q in range(10): hh_.globals_.setdefault('M%d' % q, MK.R.interp.Matrix([[0.0]]))
    m1_, mk = MK.random_matrix(seed)
    if m1_ is not None: hh_.globals_['M1'] = m1_
    verdict = 'OK'
    signal.signal(signal.SIGALRM, MK._alarm); signal.alarm(90)
    try: hh_.execute('RankLab()')
    except MK.TimeUp: verdict = 'FREEZE'
    except Exception as e: verdict = 'END ' + type(e).__name__
    finally: signal.alarm(0)
    scr = [tuple((t.text, t.x, t.y) for t in s.texts) for s in hh_.screens]
    return verdict, [('<skipped>',) if skip(list(s)) else s for s in scr], [' '.join(m_.lines) for m_ in hh_.msgboxes], str(hh_.result), sum(1 for s in scr if skip(list(s)))
diffs = []; nscr = 0; nskip = 0; verd = {}; nhelp = 0; kinds = collections.Counter()
for sd in range(1700, 1740):
    a = one(OLD, sd); b = one(SHUTP, sd)
    nscr += len(b[1]); nskip += b[4]; verd[b[0]] = verd.get(b[0], 0) + 1; nhelp += sum(1 for x in b[1] if x and x[0] != '<skipped>' and x[0][0].startswith('RankLab help'))
    for x in b[1]:
        if x and x[0] != '<skipped>': kinds[x[0][0].split(':')[0]] += 1
    if a[0] != b[0] or a[2] != b[2] or a[3] != b[3] or a[1] != b[1]:
        k_ = next((i for i, (x, y) in enumerate(zip(a[1], b[1])) if x != y), None)
        diffs.append((sd, a[0], b[0], a[3] == b[3], len(a[1]), len(b[1]), k_, ([t for t in a[1][k_] if t not in b[1][k_]][:3], [t for t in b[1][k_] if t not in a[1][k_]][:3]) if k_ is not None else None))
check('R1 the monkey, 40 seeds, on beta 1i and on beta 1j with its new entrances shut (beta 1i\'s main menu, preset menu, Your data and help): the same verdict, boxes and closing line, and all %s screens the same, every text at its place, but the %d opening pages (%s; %d help pages among them; tests seen: %s)'
      % (format(nscr, ','), nskip, verd, nhelp, ', '.join('%s %d' % kv for kv in kinds.most_common(8))), not diffs and nscr > 400, diffs[:2])
# R2: every old way in, through beta 1j's real menus, against beta 1i
def texts(h): return [(tuple((t.text, t.x, t.y) for t in s.texts), tuple(s.menu or ())) for s in h.screens if s.func == 'rk_View']
DD = {'D1': [3.1, 4.7, 5.2, 5.9, 6.3, 7.7, 8.1, 9.6, 12.4], 'D2': [2.9, 5.1, 4.4, 6.6, 6.0, 7.1, 9.3, 9.9, 11.0], 'D3': [3.5, 4.0, 5.9, 5.5, 7.0, 6.9, 8.8, 10.4, 12.0]}
walk = lambda h: (h.press('Down'), h.press('Right'), h.press('Down'), h.press('Right'), h.press('Plus'), h.press('Minus'), h.press('Down'), h.press('Esc'))
pairs = []
for nm, pick in [('test %d with nothing loaded' % i, [i]) for i in range(1, 7)] + [('preset %d' % i, [7, i]) for i in range(1, 8)] + [('your data %d' % i, [8, i]) for i in (1, 2, 4, 5)]:
    def sc(h, q):
        for p_ in pick: h.choose(p_)
        if pick[0] == 3 or pick == [7, 1]: pass
        walk(h); h.choose(q)
    ho_ = Harness(OLD, idle_key=4, home_minus=True, cas='fail', app_data=DD); ho_.press('Enter'); sc(ho_, 10); ro_ = ho_.execute('RankLab()')
    hn_ = Harness(PROG, idle_key=4, home_minus=True, cas='fail', app_data=DD); hn_.press('Enter'); sc(hn_, 12); rn_ = hn_.execute('RankLab()')
    pairs.append((nm, ro_ == rn_ and texts(ho_) == texts(hn_) and boxes(ho_) == boxes(hn_) and len(texts(hn_)) >= 3, len(texts(hn_)), ro_, rn_))
check('R2 every old way in, through beta 1j\'s own menus against beta 1i\'s: the six tests with nothing loaded, the seven old presets at their numbers and four kinds of Your data, each walked through its pages, a pick, + and -: the same pages, every text at its place, the same boxes and closing line (%d ways, %d pages)'
      % (len(pairs), sum(p_[2] for p_ in pairs)), all(p_[1] for p_ in pairs) and len(pairs) == 17, [p_ for p_ in pairs if not p_[1]][:2])

print('=== H. the help')
def help_pages(path, item, quit_, keys=10):
    hh_ = Harness(path, idle_key=4, home_minus=True, cas='fail'); hh_.press('Enter'); hh_.choose(item)
    for _ in range(keys): hh_.press('Enter')
    hh_.choose(quit_); hh_.execute('RankLab()')
    out_ = []
    for s in hh_.screens:
        L = s.lines()
        if L and L[0].startswith('RankLab help') and (not out_ or out_[-1][0] != [t.text for t in s.texts]): out_.append(([t.text for t in s.texts], s))
    return out_, hh_
HN, hhn = help_pages(PROG, 11, 12); HO, hho = help_pages(OLD, 9, 10, keys=7)
TOPICS = ['What it does', 'Keys and touch', 'Sign test, signed-rank', 'Mann-Whitney, Kruskal-Wallis', 'Friedman, W, correlation', 'Page\'s L, an ordered trend', 'The runs test',
          'Exact or normal; the p-value', 'Data and Home', 'Credits']
check('H1 the help has 10 pages (beta 1i: %d), each headed "RankLab help n/10: <Topic>" and footed "Page n/10: key = next, %s = back, Esc = leave"; a key on page 10 leaves' % (len(HO), chr(8592)),
      len(HN) == 10 and len(HO) == 7 and [p[0][0] for p in HN] == ['RankLab help %d/10: %s' % (i + 1, t) for i, t in enumerate(TOPICS)]
      and [p[0][-1] for p in HN] == ['Page %d/10: key = next, %s = back, Esc = leave' % (i + 1, chr(8592)) for i in range(10)], [p[0][0] for p in HN])
body = lambda p: p[0][1:-1]
p2o = body(HO[1]); p2n = body(HN[1])
check('H2 pages 1, 3, 4 and 5 are beta 1i\'s word for word; page 2 is too but for the Tails line, which now ends "(Page\'s L: rising, falling)"',
      all(body(HN[i]) == body(HO[i]) for i in (0, 2, 3, 4)) and len(p2o) == len(p2n) and [(a, b) for a, b in zip(p2o, p2n) if a != b] == [('- = Tails: two-sided, lower, upper', '- = Tails: two-sided, lower, upper (Page\'s L: rising, falling)')],
      [(a, b) for a, b in zip(p2o, p2n) if a != b])
p6o = body(HO[5]); p8n = body(HN[7]); p7o = body(HO[6]); p9n = body(HN[8]); p10n = body(HN[9])
check('H3 page 8 is beta 1i\'s page 6 with one line more ("%s") and a longer last line ("%s"); pages 9 and 10 are its page 7 in two, the presets and Your data lines naming the new data and tests, the four credit lines word for word and the HP-65 credit under them'
      % (p8n[3], p8n[-1]),
      p8n[:3] == p6o[:3] and p8n[3] == '(Page\'s L and the runs test: z without that correction.)' and p8n[4:-1] == p6o[3:-1] and p6o[-1] == 'Friedman: upper only.' and p8n[-1] == 'Friedman: upper only.  Page\'s L: rising or falling.'
      and p9n[:3] == p7o[:3] and p7o[3] == 'uses attractiveness only; Crime is ignored).' and p9n[3] == 'uses attractiveness only; Crime is ignored),' and p9n[4] == 'ozone and airway resistance, a roulette wheel.'
      and p9n[5:7] == p7o[4:6] and p7o[6] == 'correlation D1, D2; Friedman: rows = blocks.' and p9n[7:9] == ['correlation D1, D2; Friedman and Page\'s L:', 'rows = blocks; runs: D1 in the order it happened.']
      and p9n[9:] == p7o[7:9] and p10n[:4] == p7o[9:] and len(p7o) == 13 and len(p10n) == 12 and p10n[4].startswith('The runs test does what Hewlett-Packard\'s Run Test') and p10n[-1] == 'Page\'s L is written from its formulas (Page 1963).',
      (p8n, p9n, p10n))
oldl = set(t for p in HO for t in body(p))
wide = [(i + 1, px(t), t) for i, p in enumerate(HN) for t in body(p) if px(t) > (300 if t in oldl else 296)] + [(i + 1, px(p[0][0], 2), p[0][0]) for i, p in enumerate(HN) if px(p[0][0], 2) > 296]
check('H4 every help line is within the 300 pixels the page gives it at the measured glyph widths (the widest, a line of beta 1i, is %d; the widest new or changed line is %d, within 296) and every header too; no page has more than 13 lines; no backslash anywhere'
      % (max(px(t) for p in HN for t in body(p)), max(px(t) for p in HN for t in body(p) if t not in oldl)), not wide and max(len(body(p)) for p in HN) <= 13 and not any('\\' in t for p in HN for t in p[0]), wide[:3])
m6 = re.search(r'up to (\d+) blocks; 5: (\d+); 9: (\d+); fewer with ties', ' '.join(body(HN[5])))
check('H5 the two new pages say what the program does: page 6 gives Page\'s L, its formula line, Rising and Falling on the 5th soft key, the exact count\'s limits (%s) and the normal z without a continuity correction; page 7 the runs test, its median rule, both tails in words, n %s 2,000 and the mean 2 n%s n%s/n + 1'
      % (m6.group(0) if m6 else None, LE, chr(8321), chr(8322)),
      m6 is not None and [int(m6.group(i)) for i in (1, 2, 3)] == [77, 17, 3] and 'L = 1 %s R%s + 2 %s R%s + ... + k %s Rk     (R = a column\'s rank sum)' % (TX, chr(8321), TX, chr(8322), TX) in body(HN[5])
      and 'NORMAL: z = (L - mean)/SD, with no continuity correction.' in body(HN[5]) and any('Rising and Falling' in t for t in body(HN[5]))
      and 'equal to the median is dropped.' in body(HN[6]) and 'NORMAL: z = (runs - mean)/SD, mean = 2 n%s n%s/n + 1.' % (chr(8321), chr(8322)) in body(HN[6])
      and H0 + '; RankLab counts the orders (n ' + LE + ' 2,000).' in body(HN[6]) and 'Tails: lower = too few, upper = too many, two-sided = either.' in body(HN[6]), (body(HN[5]), body(HN[6])))
hk = Harness(PROG, idle_key=4, home_minus=True, cas='fail'); hk.press('Enter'); hk.choose(11); hk.press('Enter'); hk.press('Enter'); hk.press('Left'); hk.press('Left'); hk.press('Left'); hk.press('Enter'); hk.press('Esc'); hk.choose(12); hk.execute('RankLab()')
seq_ = []
for s in hk.screens:
    L = s.lines()
    if L and L[0].startswith('RankLab help') and (not seq_ or seq_[-1] != L[0][13:15]): seq_.append(L[0][13:15])
check('H6 in the help, Left goes back a page (and stays on page 1), any other key goes on, Esc leaves: pages %s' % ' '.join(seq_), seq_ == ['1/', '2/', '3/', '2/', '1/', '2/'], seq_)
if '--save' in sys.argv:
    with io.open(os.path.join(HERE, 'round16', 'help_RankLab_beta1j.txt'), 'w', encoding='utf-8') as f:
        for p in HN: f.write('\n'.join(p[0]) + '\n\n')

print('=== G. static')
code = '\n'.join(re.sub(r'"[^"\n]*"', '""', l.split('//')[0]) for l in SRC.split('\n'))
check('G1 no "!=" in the code, and the code outside strings and comments is ASCII', '!=' not in code and all(ord(c) < 128 for c in code))
loc = [l for l in SRC.split('\n') if re.match(r'\s*LOCAL\s', l)]
check('G2 every LOCAL line names at most 6 variables (%d lines)' % len(loc), all(len(l.split('//')[0].replace('LOCAL', '').split(',')) <= 6 for l in loc))
check('G3 the header names beta 1j and its date, the note of beta 1j is there, and the welcome page shows the version',
      '// RANKLAB - beta 1j  (15 Nov 2026)' in SRC and '// beta 1j (15 Nov 2026): Round 16' in SRC and 'TEXTOUT_P("RankLab - rank tests, beta 1j"' in SRC and SRC.count('beta 1i"') == 0)
ALLH = [hz, hm, hr, hd, h1, h2, h3, h4a, h4c, h5, h5n, h7, h7r, h7s, h8, h9, h10, h10n, hn12, hn13, hc7, hhn, hk]
items = sorted(set(i for hh_ in ALLH for c in hh_.chooses for i in c.items)); lit = re.findall(r'"([^"\n]*)"', '\n'.join(m_.group(0) for m_ in re.finditer(r'CHOOSE\(.*?\}\);', SRC, re.S)))
check('G4 every item of every menu is at most 30 characters: the %d different items the runs above were shown (the longest is %r, %d) and the %d quoted pieces of the menus in the source'
      % (len(items), max(items, key=len), max(len(i) for i in items), len(lit)), len(items) >= 40 and max(len(i) for i in items) <= 30 and max(len(i) for i in lit) <= 30, sorted(items, key=len)[-3:])
L_ = SRC.split('\n'); a_ = next(i for i, l in enumerate(L_) if l.startswith('// FILE MAP')); mp = []
for l in L_[a_:a_ + 60]:
    m_ = re.match(r'//\s+(\d+)-(\d+)\s+(\S.*)$', l)
    if m_: mp.append((int(m_.group(1)), int(m_.group(2)), m_.group(3)))
first_ok = all(L_[a - 1].startswith('// ====') or L_[a - 1].startswith('// ---- Home exports') for a, b, t in mp)
ends_ok = all(b == len(L_) - 1 or L_[b].strip() == '' for a, b, t in mp) and mp[-1][1] == len(L_) - 1
check('G5 the file map in the header is true: each of its %d sections begins where the map says (a bar of = signs, or the Home exports) and ends on the line before a blank one, the last on the file\'s last line (%d)' % (len(mp), mp[-1][1]),
      len(mp) == 15 and first_ok and ends_ok and [a for a, b, t in mp] == sorted(a for a, b, t in mp), mp[:20])
rn_old = set(re.findall(r'(?m)^(?:EXPORT )?(rk_\w+|RankLab)\(', OSRC)); rn_new = set(re.findall(r'(?m)^(?:EXPORT )?(rk_\w+|RankLab)\(', SRC))
NEWR = {'rk_LOne', 'rk_LBlock', 'rk_LNull', 'rk_DoPage', 'rk_RuNull', 'rk_RuEnd', 'rk_DoRuns', 'rk_RuFrom', 'rk_LdOzone', 'rk_LdDraftM', 'rk_LdRoul', 'rk_LdDraftR', 'rk_LOrd', 'rk_PgTrend', 'rk_RuGeo', 'rk_AxS', 'rk_AxW', 'rk_RuCells', 'rk_RuChart', 'rk_PgRuns'}
unch = [n_ for n_ in sorted(rn_old) if n_ != 'RankLab' and OSRC.count('\n' + n_ + '(') == 1 and routine(OSRC, n_ + '(') == routine(SRC, n_ + '(')]
check('G6 the %d new routines carry the program\'s tag, and beta 1i\'s %d routines are all still there; %d of them are untouched, character for character (the arithmetic of the six old tests among them: rk_DoSign, rk_SRNull, rk_DoSR, rk_MWNull, rk_DoMW, rk_DoKW, rk_DoFr, rk_Kendall, rk_SpPerm, rk_KdNull, rk_DoCorr, rk_Midrank, rk_NSum)'
      % (len(NEWR), len(rn_old), len(unch)), rn_old <= rn_new and rn_new - rn_old == NEWR
      and {'rk_DoSign', 'rk_SRNull', 'rk_DoSR', 'rk_MWNull', 'rk_DoMW', 'rk_DoKW', 'rk_DoFr', 'rk_FrRbar', 'rk_Kendall', 'rk_SpPerm', 'rk_KdNull', 'rk_DoCorr', 'rk_CorrP', 'rk_Midrank', 'rk_Order', 'rk_NSum', 'rk_NullWin', 'rk_ChiUp', 'rk_CCZ', 'rk_PZ', 'rk_PgStrip', 'rk_PgBox', 'rk_PgDunn', 'rk_PgGrid', 'rk_PgScat', 'rk_View'} <= set(unch),
      (sorted(rn_new - rn_old - NEWR), sorted(NEWR - rn_new), len(unch)))
big_un = sorted(set((m_.group(0), it['text'][:40]) for rec in OV.RECORDS.values() for e in rec['screens'].values() for it in e[2]['items'] if 'text' in it
                    for m_ in re.finditer(r'(?<![\d.,])\d{4,}(?![\d,])', it['text']) if not re.fullmatch(r'(18|19|20)\d\d', m_.group(0))))
check('G7 commas: no number of four or more digits is drawn without them on any screen above (years in citations and in "Draft 1970" aside)', not big_un, big_un[:8])
verbs = lambda t: re.findall(r'\b(reworks?|reworked|ports?|ported|replaces)\b', t)
check('G8 the credits say what was done: no "reworks" or "replaces" in the file, and "ported" only where beta 1i has it (of the TI-82 versions\' intent); the header says what was read for the two new tests and that none of that code is in the program',
      verbs(SRC) == verbs(OSRC) == ['ported'] and 'Their pages were read to see what the' in SRC and SRC.count('none of their code is in it') == OSRC.count('none of their code is in it') + 1 and 'no other program was read for it' in SRC)

print('=== D. layout over every beta 1j screen above')
def pxw(t): return sum((GW.get(str(ord(ch))) or [6, 7, 8])[0] for ch in t)       # font 1; a glyph not in the table counts as a digit
NEWTAGS = [t for t in OV.RECORDS if t.startswith('RankLab_beta1j')]; OLDTAGS = [t for t in OV.RECORDS if t.startswith('RankLab_beta1i')]
firm = []; firm_old = []
for t, f in OV.report().items():
    dst = firm if t in NEWTAGS else firm_old
    dst += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    dst += [(x['text'][:30], 'off the screen') for x in f['overruns'] if x['firm']]
recs_new = dict((t, OV.RECORDS[t]) for t in NEWTAGS)
rep_ = sorted(set((x[0], x[3], x[4]) for v in LF.clipped(recs_new).values() for x in v))
cut = [(t, pxw(t) if int(f) == 1 else px(t, int(f)), w) for t, f, w in rep_ if (pxw(t) if int(f) == 1 else px(t, int(f))) > w]
nsc = sum(len(OV.RECORDS[t]['screens']) for t in NEWTAGS)
check('D1 no firm overlap and no text off the screen on any beta 1j screen above (text_overlap_v1 over %s different screens; on beta 1i\'s screens of the same runs it finds %s)'
      % (format(nsc, ','), ', '.join('"%s" %s' % x for x in sorted(set(firm_old))[:6]) or 'nothing'), not firm and len(NEWTAGS) == 2 and nsc > 250, sorted(set(firm))[:6])
check('D2 no number cut short by its width argument (label_fit_v1 reports %d texts at its estimate; none is wider than its width argument at the measured glyph widths)' % len(rep_), not cut, cut[:4])

print('\n%d checks, %d failed' % (NPASS[0] + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
