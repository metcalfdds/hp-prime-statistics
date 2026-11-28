#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_TTestLabG_beta1k.py -- checks TTestLabG beta 1k (28 Nov 2026, round 21; made from verify_TTestLab_beta1n.py
by round21/make_verify_tlg_1k.py): every step that works the arithmetic out
checks on a calculator from the numbers it shows (the book's read-through of its Draft 127, item A10).

  A  static: the header names beta 1n and carries its history note; every routine of beta 1m is beta 1m's, word for
     word, but the ones the note names (Step2, Step4, Step4N, BookNote, Help) and the new ones (DcK, TrD, WkD, RdC, RdK,
     ExC, Txt, TyD, WV, Dev, WkAt, Work); no "!="; the code is ASCII.
  B  the monkey runs each seed on beta 1m and beta 1n (tools/comma_check_v1.runs): every run takes beta 1m's path (the
     same ending, number of screens, boxes and summary), and every screen whose texts differ is a step 2 or step 4 page;
     every number of 1,000 or more has its commas, no year has one; no new firm overlap and no new number cut short.
  C  the worked steps, read off the screen as a student reads them, for every example and for random cases of all six
     tests, typed and from raw scores: every relation written on steps 2 and 4 holds from the numbers shown, worked
     with a calculator's arithmetic and rounded half away from zero to the digits shown (a = s1^2/N1, the numerator and
     the denominator of df, df, the sum under the root, SE, the difference of the means, t or z, sp^2, the pooled root,
     the deviations and squares of the pairs, sD, p-hat, the pooled p and its complement); the last numbers (SE, df, t
     or z) are the exact ones (SciPy and Python's own arithmetic, not the program's) at the digits shown; step 2's a
     and b are step 4's; and k is the smallest for which the chain gives the exact answers (tt_WkAt at k - 1 does not).
  E  the book's two screens: TTestLab's age-at-arrest step 4 (Figure 11.4) and, through TTestLabG's script, the draft
     lottery's steps 2 and 4 (Figure 11.2), each line as it is to be printed.
  D  layout of steps 2 and 4 with the largest numbers the forms allow, typed and from raw scores: text_overlap_v1 (no
     firm overlap, nothing off the screen) and every text's right edge at the calculator's glyph widths.
Run from anywhere:   python3 verify/verify_TTestLabG_beta1k.py        (beta 1j comes from git)
"""
import os, sys, re, json, math, random, subprocess, tempfile, warnings, statistics as st
from decimal import Decimal, ROUND_HALF_UP, getcontext
warnings.filterwarnings('ignore')
getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
import comma_check_v1 as CC  # noqa: E402
from scipy import stats  # noqa: E402

# ---------------------------------------------------------------- what differs between the advanced and general versions
BASE = '44652dd'                                   # the commit that holds the version before
NAME, OLDNAME = 'TTestLabG_beta1k.txt', 'TTestLabG_beta1j.txt'
VER, OLDVER, PROGNAME, ENTRY, TAG = 'beta 1k', 'beta 1j', 'TTestLabG', 'TTESTLABG()', 'tz'
EXAMPLES = (1, 2, 3, 4, 5, 6, 7)                   # tz_Example's numbers
CHANGED = ('Step2', 'Step4', 'Step4N', 'Help')
MONKEY_RUNS = 300
HELP_NEW = ('Steps 2 and 4 work each number from those shown, so all check.',)
HELP_OLD = ('Step 4 keeps 4 significant digits at each step.',)
QUICK = os.environ.get('QUICK')                    # a quick look: few cases, few runs
# ----------------------------------------------------------------
T_ = TAG + '_'
NEW_R = ('DcK', 'TrD', 'WkD', 'RdC', 'RdK', 'ExC', 'Txt', 'TyD', 'WV', 'Dev', 'WkAt', 'Work')
PROG = os.path.join('programs', NAME)
tmp = tempfile.mkdtemp(prefix='tg1k_')
OLD = os.path.join(tmp, OLDNAME)
open(OLD, 'wb').write(subprocess.run(['git', 'show', BASE + ':programs/' + OLDNAME], check=True, capture_output=True).stdout)
SRC = open(PROG, encoding='utf-8').read(); OSRC = open(OLD, encoding='utf-8').read()
GW = {int(k): v for k, v in json.load(open(os.path.join(HERE, 'round11', 'glyph_widths_vc.json'))).items()}
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:900]) if (detail != '' and not ok) else ''), flush=True)
    if ok: NPASS[0] += 1
    else: FAIL.append(name)


def width(t, font=1):
    return sum(GW[ord(c)][font - 1] if ord(c) in GW else 8 for c in t)


def routines(t):
    """{name: text} of every routine, from its first line to the next routine's first line"""
    out, cur, buf = {}, None, []
    for ln in t.split('\n'):
        m = re.match(r'^(?:LOCAL |EXPORT )?(\w+)\([\w, ]*\)\s*$', ln)
        if m:
            if cur: out[cur] = '\n'.join(buf).rstrip()
            cur, buf = m.group(1), []
        buf.append(ln)
    if cur: out[cur] = '\n'.join(buf).rstrip()
    return out


def code(t):
    """a routine's text without its comments and the comment lines before the next routine"""
    ls = [ln for ln in t.split('\n') if not ln.strip().startswith('//')]
    ls = [ln.split('//')[0].rstrip() if ln.count('"') % 2 == 0 else ln for ln in ls]
    return '\n'.join(x for x in ls if x.strip())


# ================================================================ A. static
print('=== A. static')
check('A1 the header names %s and carries its history note' % VER,
      ('// %s - %s' % (PROGNAME.upper(), VER)) in SRC and ('// %s (28 Nov 2026): Round 21' % VER) in SRC and
      ('// %s (22 Nov 2026)' % OLDVER) in SRC)
rn, ro = routines(SRC), routines(OSRC)
chg = sorted(n for n in rn if n in ro and code(rn[n]) != code(ro[n]))
new = sorted(n for n in rn if n not in ro)
gone = sorted(n for n in ro if n not in rn)
check('A2 the routines that changed are the four the note names: %s' % ', '.join(chg),
      chg == sorted(T_ + x for x in CHANGED), chg)
check('A3 the new routines are the chain\'s twelve: %s' % ', '.join(new), new == sorted(T_ + x for x in NEW_R) and not gone, (new, gone))
body = '\n'.join(ln.split('//')[0] for ln in SRC.split('\n') if ln.count('"') % 2 == 0)
check('A4 no "!=" in the code, and the code (strings and comments aside) is ASCII',
      '!=' not in body and all(ord(c) < 128 for c in re.sub(r'"[^"\n]*"', '', body)))

# ================================================================ C. the worked steps, as a student reads them
print('=== C. every worked step checks from the numbers on the screen')
NUM = r'-?\d[\d,]*(?:\.\d+)?(?:ᴇ-?\d+)?'             # fixed, or the Prime's scientific form (1.142ᴇ-8)


def D(s): return Decimal(s.replace(',', '').replace('ᴇ', 'E'))


def dec(s):
    s = s.replace(',', '')
    return len(s.split('.')[1]) if '.' in s else 0


def rnd(x, d):
    """x rounded half away from zero to d decimals, as the calculator's ROUND and a student's pencil do"""
    q = Decimal(1).scaleb(-d)
    return Decimal(x).quantize(q, rounding=ROUND_HALF_UP)


def sq(x):
    return Decimal(x).sqrt()


def sigd(s):
    """the significant digits a text shows, its zeros at the end included"""
    t = s.replace(',', '').replace('-', '').replace('.', '').lstrip('0')
    return len(t)


def rsig(x, n):
    x = Decimal(x)
    if x == 0: return Decimal(0)
    e = x.adjusted()
    return rnd(x, n - 1 - e)


def same(shown, value):
    """the text shown equals value at the decimals the text shows (its significant digits, in the scientific form)"""
    if 'ᴇ' in shown: return rsig(value, sigd(shown.split('ᴇ')[0])) == D(shown)
    return rnd(value, dec(shown)) == D(shown)


hh = Harness(PROG, idle_key=4, home_minus=True)


def page(step):
    hh.execute(T_ + step + '()')
    # the minus sign as a hyphen; x-bar and p-hat (the Prime's own glyphs U+E000, U+E001) left out
    return [ln.replace(chr(0x2212), '-').replace(chr(0xE000), '').replace(chr(0xE001), '') for ln in hh.screens[-1].lines()]


def grab(lines, pat):
    for ln in lines:
        m = re.search(pat, ln)
        if m: return m.groups()
    return None


def g(n): return hh.globals_[TAG + n]


def finals(se_t, t_t, se, t, df_t=None, df=None):
    """the chain's last numbers against the exact ones"""
    bad = []
    if rsig(Decimal(repr(se)), sigd(se_t.split('ᴇ')[0])) != D(se_t): bad.append(('SE exact', se_t, se))
    if rnd(Decimal(repr(t)), 2) != D(t_t): bad.append(('t exact', t_t, t))
    if df_t is not None and rnd(Decimal(repr(df)), 2) != D(df_t): bad.append(('df exact', df_t, df))
    return bad


def welch_exact(m1, s1, n1, m2, s2, n2):
    a, b = s1 ** 2 / n1, s2 ** 2 / n2
    return (a + b) ** .5, (m1 - m2) / (a + b) ** .5, (a + b) ** 2 / (a ** 2 / (n1 - 1) + b ** 2 / (n2 - 1))


def pooled_exact(m1, s1, n1, m2, s2, n2):
    sp2 = ((n1 - 1) * s1 ** 2 + (n2 - 1) * s2 ** 2) / (n1 + n2 - 2)
    se = (sp2 * (n1 + n2) / (n1 * n2)) ** .5
    return se, (m1 - m2) / se


def chk_two(ty, ex):
    """steps 2 and 4 of a two-sample test; ex = (m1, s1, n1, m2, s2, n2) exact; -> the relations that fail"""
    bad = []
    p4 = page('Step4')
    n1, n2 = int(ex[2]), int(ex[5])
    if ty == 2:
        p2 = page('Step2')
        a = grab(p2, r'^a = s₁²/N₁ = (%s)²/(%s) = (%s)$' % (NUM, NUM, NUM))
        b = grab(p2, r'^b = s₂²/N₂ = (%s)²/(%s) = (%s)$' % (NUM, NUM, NUM))
        f = grab(p2, r'^df = (%s) / (%s) = (%s)$' % (NUM, NUM, NUM))
        r1 = grab(p4, r'^   = √\((%s)²/(%s) \+ (%s)²/(%s)\)$' % (NUM, NUM, NUM, NUM))
        r2 = grab(p4, r'^   = √\((%s) \+ (%s)\) = √(%s)$' % (NUM, NUM, NUM))
        if None in (a, b, f, r1, r2): return [('a line is missing', p2, p4)]
        S1, A, S2, B, NU, DE, DF = a[0], a[2], b[0], b[2], f[0], f[1], f[2]
        if int(D(a[1])) != n1 or int(D(b[1])) != n2: bad.append(('N', a[1], b[1]))
        if not same(A, D(S1) ** 2 / n1): bad.append(('a = s1^2/N1', S1, A))
        if not same(B, D(S2) ** 2 / n2): bad.append(('b = s2^2/N2', S2, B))
        if not same(NU, (D(A) + D(B)) ** 2): bad.append(('(a + b)^2', A, B, NU))
        if not same(DE, D(A) ** 2 / (n1 - 1) + D(B) ** 2 / (n2 - 1)): bad.append(('the denominator', A, B, DE))
        if not same(DF, D(NU) / D(DE)): bad.append(('df = num/den', NU, DE, DF))
        if (r1[0], r1[2], r2[0], r2[1]) != (S1, S2, A, B): bad.append(('step 2 and step 4 differ', (S1, S2, A, B), r1, r2))
        if not same(r2[2], D(A) + D(B)): bad.append(('a + b', r2))
        SUM = r2[2]
    else:
        r1 = grab(p4, r'^   = √\[\((%s) × (%s)² \+ (%s) × (%s)²\)/(%s)\]$' % (NUM, NUM, NUM, NUM, NUM))
        r2 = grab(p4, r'^       × √\[(%s)/(%s)\]$' % (NUM, NUM))
        r3 = grab(p4, r'^   = √(%s) × √(%s)$' % (NUM, NUM)) + grab(p4, r'^   = (%s) × (%s)$' % (NUM, NUM)) \
            if grab(p4, r'^   = √(%s) × √(%s)$' % (NUM, NUM)) and grab(p4, r'^   = (%s) × (%s)$' % (NUM, NUM)) else None
        if None in (r1, r2, r3): return [('a line is missing', p4)]
        S1, S2 = r1[1], r1[3]
        if (int(D(r1[0])), int(D(r1[2])), int(D(r1[4])), int(D(r2[0])), int(D(r2[1]))) != (n1 - 1, n2 - 1, n1 + n2 - 2, n1 + n2, n1 * n2):
            bad.append(('the counts', r1, r2))
        if not same(r3[0], ((n1 - 1) * D(S1) ** 2 + (n2 - 1) * D(S2) ** 2) / (n1 + n2 - 2)): bad.append(('sp^2', r1, r3[0]))
        if not same(r3[1], Decimal(n1 + n2) / (n1 * n2)): bad.append(('(N1+N2)/(N1N2)', r3[1]))
        if not same(r3[2], sq(D(r3[0]))): bad.append(('sp = root of sp^2', r3[0], r3[2]))
        if not same(r3[3], sq(D(r3[1]))): bad.append(('the root of (N1+N2)/(N1N2)', r3[1], r3[3]))
    se = grab(p4, r'^   = (%s)$' % NUM)
    t0 = grab(p4, r'^(t obt = \(₁ - ₂\)/SE)$')
    t1 = grab(p4, r'^      = \((%s) - (%s)\)/(%s)$' % (NUM, NUM, NUM))
    t2 = grab(p4, r'^      = (%s)/(%s) = (%s)$' % (NUM, NUM, NUM))
    if None in (se, t0, t1, t2): return bad + [('a line is missing', p4)]
    SE = se[0]
    if ty == 2 and not same(SE, sq(D(SUM))): bad.append(('SE = root of a + b', SUM, SE))
    if ty == 1 and not same(SE, D(r3[2]) * D(r3[3])): bad.append(('SE = sp x root', r3[2], r3[3], SE))
    if (t1[2], t2[1]) != (SE, SE): bad.append(('SE differs', SE, t1, t2))
    if D(t2[0]) != D(t1[0]) - D(t1[1]): bad.append(('the difference of the means', t1, t2[0]))
    if not same(t2[2], D(t2[0]) / D(SE)): bad.append(('t = difference/SE', t2))
    # the means and SDs shown are the exact ones at their digits, so a student who has the data finds them too
    for shown, x in ((t1[0], ex[0]), (t1[1], ex[3]), (S1, ex[1]), (S2, ex[4])):
        if not same(shown, Decimal(repr(x))): bad.append(('a mean or SD is not the exact one at its digits', shown, x))
    if ty == 2:
        e = welch_exact(*ex)
        bad += finals(SE, t2[2], e[0], e[1], DF, e[2])
        s3 = '\n'.join(page('Step3'))
        if ('df = ' + DF) not in s3: bad.append(('step 3 shows another df', DF))
    else:
        e = pooled_exact(*ex)
        bad += finals(SE, t2[2], e[0], e[1])
    return bad


def chk_pairs(raw, xd=None, md=None, sd=None, n=None):
    bad = []
    p4 = page('Step4')
    if raw:
        n = len(xd)
        md = sum(Decimal(repr(x)) for x in xd) / n
        ssq = sum((Decimal(repr(x)) - md) ** 2 for x in xd)
        sd = (ssq / (n - 1)).sqrt()
        m = grab(p4, r'^D = (%s)$' % NUM)
        su = grab(p4, r'^sum = (%s)$' % NUM)
        s1 = grab(p4, r'^sD = √\(sum/\(N-1\)\) = √\((%s)/(%s)\) = (%s)$' % (NUM, NUM, NUM))
        if None in (m, su, s1): return [('a line is missing', p4)]
        MD, SU, SD = m[0], su[0], s1[2]
        if s1[0] != SU or int(D(s1[1])) != n - 1: bad.append(('sD line', s1))
        if not same(MD, md): bad.append(('the mean of the differences', MD, md))
        # the rows: the difference, its deviation from the mean shown, that squared
        nums = [ln for ln in p4 if re.fullmatch(NUM, ln)]
        rows = [nums[i:i + 3] for i in range(0, 3 * min(n, 5), 3)]
        sqs = []
        for i, r in enumerate(rows):
            if len(r) < 3: bad.append(('a row is short', r)); continue
            if D(r[0]) != rnd(Decimal(repr(xd[i])), dec(r[0])): bad.append(('xD', r[0], xd[i]))
            if not same(r[1], D(r[0]) - D(MD)): bad.append(('xD - mean', r))
            if not same(r[2], D(r[1]) ** 2): bad.append(('(xD - mean)^2', r))
            sqs.append(D(r[2]))
        if n <= 5:
            if not same(SU, sum(sqs)): bad.append(('the sum of the squares shown', SU, sum(sqs)))
        else:
            if not same(SU, sum((Decimal(repr(x)) - D(MD)) ** 2 for x in xd)): bad.append(('the sum, every row', SU))
        if not same(SD, sq(D(SU) / (n - 1))): bad.append(('sD = root of sum/(N-1)', SU, SD))
    else:
        md, sd = Decimal(repr(md)), Decimal(repr(sd))
        line = grab(p4, r'^D = (%s),  sD = (%s),  N pairs = (%s)$' % (NUM, NUM, NUM))
        if line is None: return [('a line is missing', p4)]
        MD, SD = line[0], line[1]
    se = grab(p4, r'^SE = sD/√N = (%s)/√(%s) = (%s)$' % (NUM, NUM, NUM))
    tt = grab(p4, r'^t obt = D/SE = (%s)/(%s) = (%s)$' % (NUM, NUM, NUM))
    if None in (se, tt): return bad + [('a line is missing', p4)]
    if se[0] != SD or int(D(se[1])) != n: bad.append(('SE line', se))
    if not same(se[2], D(SD) / sq(Decimal(n))): bad.append(('SE = sD/root N', se))
    if tt[0] != MD or tt[1] != se[2]: bad.append(('t line', tt))
    if not same(tt[2], D(MD) / D(se[2])): bad.append(('t = mean/SE', tt))
    sde = float(sd) / n ** .5
    bad += finals(se[2], tt[2], sde, float(md) / sde)
    return bad


def chk_one(raw, xs=None, m=None, s=None, n=None, mu=0):
    bad = []
    p4 = page('Step4N')
    if raw:
        n = len(xs); m = st.mean(xs); s = st.stdev(xs)
    h1 = grab(p4, r'^ = (%s),   s = (%s)$' % (NUM, NUM)); h2 = grab(p4, r'^N = (%s),   μ₀ = (%s)$' % (NUM, NUM))
    head = (h1 + h2) if h1 and h2 else None
    se = grab(p4, r'^SE = s/√N = (%s)/√(%s) = (%s)$' % (NUM, NUM, NUM))
    t0 = grab(p4, r'^(t obt = \( - μ₀\)/SE)$')
    t1 = grab(p4, r'^      = \((%s) - \(?(%s)\)?\)/(%s)$' % (NUM, NUM, NUM))
    t2 = grab(p4, r'^      = (%s)/(%s) = (%s)$' % (NUM, NUM, NUM))
    if None in (head, se, t0, t1, t2): return [('a line is missing', p4)]
    M, S = head[0], head[1]
    if not same(M, Decimal(repr(m))) or not same(S, Decimal(repr(s))): bad.append(('mean or SD not exact at its digits', M, S, m, s))
    if se[0] != S or int(D(se[1])) != n: bad.append(('SE line', se))
    if not same(se[2], D(S) / sq(Decimal(n))): bad.append(('SE = s/root N', se))
    if t1[0] != M or t1[2] != se[2] or t2[1] != se[2]: bad.append(('t lines', t1, t2))
    if D(t2[0]) != D(M) - D(t1[1]): bad.append(('mean - mu0', t1, t2))
    if not same(t2[2], D(t2[0]) / D(se[2])): bad.append(('t = difference/SE', t2))
    sde = s / n ** .5
    bad += finals(se[2], t2[2], sde, (m - mu) / sde)
    return bad


def chk_prop(ty, ka, na, kb=None, nb=None, p0=None):
    bad = []
    ka, na = int(ka), int(na)
    if ty == 6: kb, nb = int(kb), int(nb)
    p4 = page('Step4N')
    if ty == 5:
        p = grab(p4, r'^ = x/n = (%s)/(%s) = (%s)$' % (NUM, NUM, NUM))
        s1 = grab(p4, r'^   = √\((%s) × (%s)/(%s)\) = (%s)$' % (NUM, NUM, NUM, NUM))
        z0 = grab(p4, r'^(z obt = \( - p₀\)/SE)$')
        z1 = grab(p4, r'^      = \((%s) - (%s)\)/(%s)$' % (NUM, NUM, NUM))
        z2 = grab(p4, r'^      = (%s)/(%s) = (%s)$' % (NUM, NUM, NUM))
        if None in (p, s1, z0, z1, z2): return [('a line is missing', p4)]
        PA, SE = p[2], s1[3]
        if not same(PA, Decimal(ka) / Decimal(na)): bad.append(('p-hat = x/n', p))
        if D(s1[0]) + D(s1[1]) != 1: bad.append(('p0 and 1 - p0', s1))
        if not same(SE, sq(D(s1[0]) * D(s1[1]) / na)): bad.append(('SE', s1))
        if z1[0] != PA or z1[2] != SE or z2[1] != SE: bad.append(('z lines', z1, z2))
        if D(z2[0]) != D(PA) - D(z1[1]): bad.append(('p-hat - p0', z1, z2))
        if not same(z2[2], D(z2[0]) / D(SE)): bad.append(('z = difference/SE', z2))
        se = (p0 * (1 - p0) / na) ** .5
        bad += finals(SE, z2[2], se, (ka / na - p0) / se)
    else:
        p1 = grab(p4, r'^₁ = x₁/n₁ = (%s)/(%s) = (%s)$' % (NUM, NUM, NUM))
        p2 = grab(p4, r'^₂ = x₂/n₂ = (%s)/(%s) = (%s)$' % (NUM, NUM, NUM))
        pp = grab(p4, r'^   = (%s)/(%s) = (%s)$' % (NUM, NUM, NUM)) if grab(p4, r'^(p = \(x₁ \+ x₂\)/\(n₁ \+ n₂\))$') else None
        s1 = grab(p4, r'^   = √\((%s) × (%s)$' % (NUM, NUM))
        s1b = grab(p4, r'^       × \(1/(%s) \+ 1/(%s)\)\)$' % (NUM, NUM))
        s1 = (s1 + s1b) if s1 and s1b else None
        s2 = grab(p4, r'^   = (%s)$' % NUM)
        z0 = grab(p4, r'^(z obt = \(₁ - ₂\)/SE)$')
        z1 = grab(p4, r'^      = \((%s) - (%s)\)/(%s)$' % (NUM, NUM, NUM))
        z2 = grab(p4, r'^      = (%s)/(%s) = (%s)$' % (NUM, NUM, NUM))
        if None in (p1, p2, pp, s1, s2, z0, z1, z2): return [('a line is missing', p4)]
        PA, PB, PP, SE = p1[2], p2[2], pp[2], s2[0]
        if not same(PA, Decimal(ka) / Decimal(na)) or not same(PB, Decimal(kb) / Decimal(nb)): bad.append(('p-hats', p1, p2))
        if not same(PP, Decimal(ka + kb) / Decimal(na + nb)) or (int(D(pp[0])), int(D(pp[1]))) != (ka + kb, na + nb): bad.append(('pooled p', pp))
        if s1[0] != PP or not same(s1[1], 1 - D(PP)) or ('ᴇ' not in PP and D(PP) + D(s1[1]) != 1): bad.append(('p and 1 - p', s1))
        if (int(D(s1[2])), int(D(s1[3]))) != (na, nb): bad.append(('n1 and n2', s1))
        if not same(SE, sq(D(s1[0]) * D(s1[1]) * (Decimal(1) / na + Decimal(1) / nb))): bad.append(('SE', s1, SE))
        if (z1[0], z1[1], z1[2], z2[1]) != (PA, PB, SE, SE): bad.append(('z lines', z1, z2))
        if D(z2[0]) != D(PA) - D(PB): bad.append(('p-hat1 - p-hat2', z1, z2))
        if not same(z2[2], D(z2[0]) / D(SE)): bad.append(('z = difference/SE', z2))
        q = (ka + kb) / (na + nb); se = (q * (1 - q) * (1 / na + 1 / nb)) ** .5
        bad += finals(SE, z2[2], se, (ka / na - kb / nb) / se)
    return bad


def smallest():
    """k is the smallest whose chain gives the exact answers: the chain at k - 1 does not"""
    k = int(hh.execute(T_ + 'Work()')[1])
    return k, (k == 4 or hh.execute(T_ + 'WkAt(%d)' % (k - 1))[0] == 0)


def plist(xs):
    """a list as PPL text, exponents with a capital E"""
    return '{' + ','.join(repr(float(x)).upper() for x in xs) + '}'


def setv(**kv):
    """the program's variables, as the calculator holds them: reals (the harness's MAX takes no Python int)"""
    for k, v in kv.items():
        hh.globals_[TAG + k] = [float(x) for x in v] if isinstance(v, (list, tuple)) else float(v)


def calc():
    return hh.execute(T_ + 'Calc()') == 1 and g('OK') == 1


# the examples
exbad, ks = [], {}
for ex in EXAMPLES:
    hh.execute(T_ + 'Example(%d)' % ex)
    if not calc(): exbad.append((ex, 'Calc failed')); continue
    ty, src = int(g('TY')), int(g('SRC'))
    if ty <= 2:
        r = chk_two(ty, (g('M1'), g('S1'), g('N1'), g('M2'), g('S2'), g('N2')))
    elif ty == 3:
        r = chk_pairs(src == 2, xd=[a - b for a, b in zip(g('X1'), g('X2'))], md=g('MD'), sd=g('SDv'), n=g('NP'))
    elif ty == 4:
        r = chk_one(src == 2, xs=list(g('XO')), m=g('MO'), s=g('SO'), n=g('NO'), mu=g('MU'))
    else:
        r = chk_prop(ty, g('KA'), g('NA'), g('KB'), g('NB'), g('P0'))
    k, ok = smallest()
    ks[ex] = k
    if r or not ok: exbad.append((ex, r[:3], k, ok))
check('C1 every example: every worked step checks from the numbers shown, the last numbers are the exact ones, and k is the '
      'smallest that does it (k: %s)' % ', '.join('%d: %d' % kv for kv in sorted(ks.items())), not exbad, exbad)

rng = random.Random(21)


def rlist(n, loc, scale, dp):
    return [round(rng.gauss(loc, scale), dp) for _ in range(n)]


groups, LIMIT, FLAT = {}, [], [0]
EXACT = ('SE exact', 't exact', 'df exact')


def tally(name, r, k, ok):
    """one case: when even k = 8 cannot give the exact answers (a t or z of 100,000 or more needs more digits than
    that), the chain at 8 stands, every relation on the screen still holds, and its t or z may differ from the exact
    one by what an SE of 8 significant digits allows: 1E-7 of t, and the two roundings to 2 decimals"""
    e = groups.setdefault(name, [0, [], {}])
    e[0] += 1
    e[2][k] = e[2].get(k, 0) + 1
    if r and k == 8 and ok and all(x[0] in EXACT for x in r):
        far = [x for x in r if x[0] != 't exact' or abs(float(D(x[1])) - x[2]) > 1E-7 * abs(x[2]) + 0.01]
        if not far:
            LIMIT.append((name, abs(float(D([x for x in r if x[0] == 't exact'][0][1]))) if any(x[0] == 't exact' for x in r) else None, r))
            return
    if r or not ok: e[1].append((r[:2], k, ok))


for i in range(5 if QUICK else 150):                          # two samples, typed: the forms' ranges
    for ty in (1, 2):
        m1 = round(rng.uniform(-10000, 10000) * 10 ** rng.uniform(-4, 0), rng.randint(0, 5))
        m2 = round(m1 + rng.uniform(-3, 3) * 10 ** rng.uniform(-3, 2), rng.randint(0, 5))
        if abs(m2) > 10000: m2 = round(m1 / 2, 2)
        s1 = round(10 ** rng.uniform(-3, 3), rng.randint(0, 5)) or 1; s2 = round(10 ** rng.uniform(-3, 3), rng.randint(0, 5)) or 2
        s1, s2 = min(s1, 1000), min(s2, 1000)
        n1, n2 = int(10 ** rng.uniform(0.31, 4)), int(10 ** rng.uniform(0.31, 4))
        setv(TY=ty, SRC=1, TL=0, AL=0.05, M1=m1, S1=s1, N1=n1, M2=m2, S2=s2, N2=n2, EX=0)
        if not calc(): continue
        tally('typed, test %d' % ty, chk_two(ty, (m1, s1, n1, m2, s2, n2)), *smallest())
for i in range(5 if QUICK else 150):                          # two samples, from raw scores
    for ty in (1, 2):
        n1, n2 = rng.randint(2, 300), rng.randint(2, 300)
        sc = 10 ** rng.uniform(-2, 4); loc = rng.uniform(-50, 50) * sc * rng.choice((0.1, 1, 30)); dp = rng.randint(0, 3)
        x1, x2 = rlist(n1, loc, sc, dp), rlist(n2, loc + sc * rng.uniform(-1, 1), sc * rng.uniform(0.3, 3), dp)
        if st.stdev(x1) == 0 and st.stdev(x2) == 0: continue
        r = hh.execute(T_ + 'MSN(' + plist(x1) + ')'); r2 = hh.execute(T_ + 'MSN(' + plist(x2) + ')')
        for rr, xx in ((r, x1), (r2, x2)):
            if st.stdev(xx) == 0: rr[0], rr[1] = xx[0], 0.0; FLAT[0] += 1
        setv(TY=ty, SRC=2, TL=0, AL=0.05, M1=r[0], S1=r[1], N1=r[2], M2=r2[0], S2=r2[1], N2=r2[2], EX=0)
        if not calc(): continue
        tally('raw scores, test %d' % ty, chk_two(ty, (st.mean(x1), st.stdev(x1), n1, st.mean(x2), st.stdev(x2), n2)), *smallest())
for i in range(5 if QUICK else 200):                          # dependent samples
    n = rng.randint(2, 40); dp = rng.randint(0, 3); sc = 10 ** rng.uniform(-1, 3)
    x1 = rlist(n, rng.uniform(0, 100) * sc, sc, dp); x2 = [round(x - rng.gauss(sc * 0.3, sc * 0.5), dp) for x in x1]
    if len(set(round(a - b, 6) for a, b in zip(x1, x2))) < 2: continue
    setv(TY=3, SRC=2, TL=0, AL=0.05, X1=x1, X2=x2, EX=0)
    if not calc(): continue
    tally('raw pairs, test 3', chk_pairs(True, xd=[a - b for a, b in zip(x1, x2)]), *smallest())
    md = round(rng.uniform(-10000, 10000) * 10 ** rng.uniform(-4, 0), rng.randint(0, 5)); sd = min(1000, round(10 ** rng.uniform(-3, 3), rng.randint(0, 5)) or 1)
    nn = int(10 ** rng.uniform(0.31, 4))
    setv(TY=3, SRC=1, TL=0, AL=0.05, MD=md, SDv=sd, NP=nn, EX=0)
    if not calc(): continue
    tally('typed, test 3', chk_pairs(False, md=md, sd=sd, n=nn), *smallest())
for i in range(5 if QUICK else 200):                          # one sample
    n = rng.randint(2, 200); dp = rng.randint(0, 3); sc = 10 ** rng.uniform(-1, 3)
    xs = rlist(n, rng.uniform(-30, 30) * sc, sc, dp); mu = round(st.mean(xs) + rng.uniform(-3, 3) * sc / n ** .5, rng.randint(0, 4))
    if st.stdev(xs) == 0: continue
    setv(TY=4, SRC=2, TL=0, AL=0.05, XO=xs, MU=mu, EX=0)
    if not calc(): continue
    tally('raw scores, test 4', chk_one(True, xs=xs, mu=mu), *smallest())
    m = round(rng.uniform(-10000, 10000) * 10 ** rng.uniform(-4, 0), rng.randint(0, 5)); s = min(1000, round(10 ** rng.uniform(-3, 3), rng.randint(0, 5)) or 1)
    nn = int(10 ** rng.uniform(0.31, 4)); mu = round(m + rng.uniform(-3, 3) * s / nn ** .5, rng.randint(0, 5))
    if abs(mu) > 10000: mu = 0
    setv(TY=4, SRC=1, TL=0, AL=0.05, MO=m, SO=s, NO=nn, MU=mu, EX=0)
    if not calc(): continue
    tally('typed, test 4', chk_one(False, m=m, s=s, n=nn, mu=mu), *smallest())
for i in range(5 if QUICK else 200):                          # proportions
    na = int(10 ** rng.uniform(0, 6)); ka = rng.randint(0, na); p0 = round(rng.uniform(0.00001, 0.99999), rng.randint(1, 5))
    p0 = min(max(p0, 0.00001), 0.99999)
    setv(TY=5, SRC=1, TL=0, AL=0.05, KA=ka, NA=na, P0=p0, EX=0)
    if calc(): tally('test 5', chk_prop(5, ka, na, p0=p0), *smallest())
    na, nb = int(10 ** rng.uniform(0, 5)), int(10 ** rng.uniform(0, 5)); ka, kb = rng.randint(0, na), rng.randint(0, nb)
    setv(TY=6, SRC=1, TL=0, AL=0.05, KA=ka, NA=na, KB=kb, NB=nb, EX=0)
    if calc(): tally('test 6', chk_prop(6, ka, na, kb, nb), *smallest())
for name, (n, bad, kk) in sorted(groups.items()):
    nl = sum(1 for x in LIMIT if x[0] == name)
    check('C2 %s: %d cases, every worked step checks and the answers are exact (k: %s)%s' %
          (name, n, ', '.join('%d: %d' % kv for kv in sorted(kk.items())), ' but in the %d at the limit of k = 8 (C3)' % nl if nl else ''),
          (QUICK or n >= 50) and not bad, bad[:3])
ncases = sum(v[0] for v in groups.values())
lt = [x[1] for x in LIMIT]
check('C3 where even k = 8 does not give the exact t or z (%d of %d cases: %s), every step still checks, and the t or z '
      'shown is within 1E-7 of it and the roundings; each is a t or z of 100,000 or more (from %s to %s)'
      % (len(LIMIT), ncases, ', '.join(sorted(set(x[0] for x in LIMIT))) or 'none', '{:,.0f}'.format(min(lt)) if lt else '-',
         '{:,.0f}'.format(max(lt)) if lt else '-'),
      all(x is not None and x >= 100000 for x in lt), [x for x in LIMIT if x[1] is None or x[1] < 100000][:3])
print('     (%d samples with no spread, from raw scores, were given the mean and the SD of 0 that the calculator works out;'
      ' the harness\'s binary arithmetic gives an SD of about 1E-16)' % FLAT[0])

# ================================================================ E. the book's screens
print('=== E. the book\'s screens')
if TAG == 'tz':
    hh.execute(T_ + 'Example(2)'); calc()
    want2 = ['a = s₁²/N₁ = 106.1437²/182 = 61.9038', 'b = s₂²/N₂ = 100.7567²/184 = 55.1734', 'df = 13,707 / 37.806 = 362.56',
             'A fraction is fine: SPSS and R print this df.', 'By hand: df = the smaller of (N₁-1), (N₂-1) = 181,',
             't crit = ±1.973: larger, so a safer test.']
    want4 = ['   = √(106.1437²/182 + 100.7567²/184)', '   = √(61.9038 + 55.1734) = √117.0772', '   = 10.820', 't obt = (₁ - ₂)/SE',
             '      = (206.3242 - 160.9239)/10.820', '      = 45.4003/10.820 = 4.20']
    p2, p4 = page('Step2'), page('Step4')
    check('E2 the draft lottery\'s steps 2 and 4 (the book\'s Figure 11.2), line by line', all(w in p2 for w in want2) and
          all(w in p4 for w in want4), [w for w in want2 if w not in p2] + [w for w in want4 if w not in p4])
if TAG == 'tt':
    hh.execute(T_ + 'Example(1)'); calc()
    want = ['   = √[(43 × 1.45² + 30 × 1.11²)/73]', '       × √[75/1,364]', '   = √1.74480 × √0.0549853', '   = 1.3209 × 0.23449',
            '   = 0.3097', 't obt = (₁ - ₂)/SE', '      = (15.89 - 16.57)/0.3097', '      = -0.68/0.3097 = -2.20',
            'The lecture rounds √0.0549853 to √.05, SE to .29,']
    p4 = page('Step4')
    check('E1 the age-at-arrest example\'s step 4 (the book\'s Figure 11.4), line by line', all(w in p4 for w in want),
          [w for w in want if w not in p4])

# ================================================================ H. help page 2
print('=== H. help')
n0 = len(hh.screens)
hh.execute(T_ + 'Help()')
hp = [sc for sc in hh.screens[n0:] if sc.lines() and ' help ' in sc.lines()[0]]
p2 = [sc for sc in hp if '2/' in sc.lines()[0]]
txt2 = '\n'.join(p2[-1].lines()) if p2 else ''
check('H1 help page 2 says what steps 2 and 4 do now: %s' % ' / '.join(HELP_NEW), p2 and all(x in txt2 for x in HELP_NEW) and
      'keeps 4 significant digits' not in txt2, txt2)
over = sorted(set((t.x + width(t.text, int(t.font or 1)), t.text) for sc in hp for t in sc.texts if t.x + width(t.text, int(t.font or 1)) > 318))
check('H2 every line of the help pages ends inside the screen at the calculator\'s glyph widths (%d pages)' % len(hp), hp and not over, over[:3])

# ================================================================ D. layout
print('=== D. layout of steps 2 and 4 with the largest numbers the forms allow')
OV.install()
BIG = [dict(TY=t, SRC=1, M1=-9999.99999, S1=999.99999, N1=9999, M2=9999.99999, S2=0.00001, N2=10000) for t in (1, 2)]
BIG += [dict(TY=t, SRC=1, M1=1234.56789, S1=0.12345, N1=2, M2=1234.5678, S2=987.65432, N2=3) for t in (1, 2)]
BIG += [dict(TY=3, SRC=1, MD=-9999.99999, SDv=999.99999, NP=10000), dict(TY=4, SRC=1, MO=-9999.99999, SO=999.99999, NO=10000, MU=9999.99999)]
BIG += [dict(TY=5, SRC=1, KA=123457, NA=999999, P0=0.98765), dict(TY=6, SRC=1, KA=12345, NA=99999, KB=99998, NB=99999)]
# the proportions at the ends of their forms: n of 1,000,000, p0 of 5 decimals, a pooled p of 10 decimals or below 1E-6
BIG += [dict(TY=5, SRC=1, KA=1, NA=1000000, P0=0.12345), dict(TY=5, SRC=1, KA=999999, NA=1000000, P0=0.00001),
        dict(TY=5, SRC=1, KA=0, NA=999999, P0=0.99999)]
BIG += [dict(TY=6, SRC=1, KA=1, NA=999999, KB=151, NB=1000000), dict(TY=6, SRC=1, KA=76, NA=999983, KB=0, NB=1),
        dict(TY=6, SRC=1, KA=1, NA=1000000, KB=0, NB=1000000), dict(TY=6, SRC=1, KA=999999, NA=1000000, KB=1, NB=999999)]
RAW = [(1, [1234567.891 + i * 0.001 for i in range(200)], [1234567.89 + (i % 7) * 0.013 for i in range(150)]),
       (2, [98765.4321 * (1 + 0.37 * math.sin(i)) for i in range(300)], [0.0012 * i for i in range(300)])]
lay = []
for kv in BIG:
    setv(TL=0, AL=0.05, EX=0, **kv)
    if not calc(): lay.append(('refused', kv)); continue
    for stp in (('Step2', 'Step4') if kv['TY'] <= 3 else ('Step4N',)):
        hh.execute(T_ + stp + '()')
for ty, x1, x2 in RAW:
    r = hh.execute(T_ + 'MSN(' + plist(x1) + ')'); r2 = hh.execute(T_ + 'MSN(' + plist(x2) + ')')
    setv(TY=ty, SRC=2, TL=0, AL=0.05, M1=r[0], S1=r[1], N1=r[2], M2=r2[0], S2=r2[1], N2=r2[2], EX=0)
    if calc():
        for stp in ('Step2', 'Step4'): hh.execute(T_ + stp + '()')
pairs = ([1.23456 + 1000 * i for i in range(5)], [0.00001 * i for i in range(5)])
setv(TY=3, SRC=2, TL=0, AL=0.05, X1=pairs[0], X2=pairs[1], EX=0)
if calc(): hh.execute(T_ + 'Step4()')
firm, wide = [], []
for tag, f in OV.report().items():
    firm += [(c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm += [('overrun', x['text']) for x in f.get('overruns', []) if x['firm']]
for s in hh.screens:
    if not s.lines() or not s.lines()[0].startswith(('Step 2.', 'Step 4.')): continue
    for t in s.texts:
        wide.append((t.x + width(t.text, int(t.font or 1)), t.text.replace('−', '-')))
check('D1 %d sessions with the largest numbers the forms allow ran (nothing refused)' % (len(BIG) + len(RAW) + 1), not lay, lay)
check('D2 no firm overlap of two texts, and none off the screen (text_overlap_v1)', not firm, firm[:4])
edge = max(wide)
check('D3 every text of steps 2 and 4 ends inside the screen at the calculator\'s glyph widths (the widest ends at x = %d)' % edge[0],
      edge[0] <= 319, sorted(set(wide))[-4:])

# ================================================================ B. the monkey: the same path as the version before
print('=== B. the monkey on %s and %s, seed by seed (%d runs)' % (OLDVER, VER, MONKEY_RUNS))
res = CC.runs(OLD, PROG, ENTRY, 3 if QUICK else MONKEY_RUNS, 60, OLDVER + '|' + VER)
check('B1 every run takes %s\'s path: the same ending, number of screens, boxes and summary (%s)' % (OLDVER, res['verdicts']),
      not res['r_bad'] and set(res['verdicts']) <= {'OK'}, res['r_bad'][:3])
heads = sorted(set(d[2][0][:40] if d[2] else '' for d in res['r_txt']) | set(d[3][0][:40] if d[3] else '' for d in res['r_txt']))
other = [d for d in res['r_txt'] if not (set(d[2]) <= set(HELP_OLD) and set(d[3]) <= set(HELP_NEW)) and not any(x.startswith(('Step 2.', 'Step 4.', '   = ', '      = ', 'a = ', 'b = ', 'df = ', 't obt = ', 'z obt = ',
                                                         'SE = ', 'sD = ', 'sum = ', '', '', 'D = '))
                                            or re.fullmatch(NUM.replace('-', '[-−]'), x) for x in (d[2] + d[3]))]
check('B2 every screen whose texts differ (%d) differs on step 2 or step 4, or is help page 2 (%d)' %
      (len(res['r_txt']), sum(1 for d in res['r_txt'] if set(d[2]) <= set(HELP_OLD) and set(d[3]) <= set(HELP_NEW))), not other, other[:3])
check('B3 every number of 1,000 or more has its commas, and no year has one', not res['m_bad'] and not res['y_bad'],
      (list(res['m_bad'].items())[:3], list(res['y_bad'].items())[:3]))
# the new help lines are past the screen's edge by text_overlap_v1's average widths, and inside it by the calculator's
# own glyph widths (H2), the measure the help pages are held to
hl = [d for d in res['d_new'] if d[0] == 'overrun' and any(h.replace(',', '').startswith(d[1]) for h in HELP_NEW)]
dn = [d for d in res['d_new'] if d not in hl]
check('B4 no new firm overlap and no new number cut short (%s had %d and %d, %s has %d and %d, of which %d are help page 2\'s '
      'new lines, inside the screen by the calculator\'s glyph widths: H2)' %
      (OLDVER, res['firm_old'], res['cut_old'], VER, res['firm_new'], res['cut_new'], len(hl)), not dn and not res['c_new'], (dn[:3], res['c_new'][:3]))

print('\n%d checks, %d failed  (C: %d random cases besides the %d examples)' % (NPASS[0] + len(FAIL), len(FAIL), ncases, len(EXAMPLES)))
sys.exit(1 if FAIL else 0)
