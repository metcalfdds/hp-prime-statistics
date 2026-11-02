#!/usr/bin/env python3
"""verify_BayesTree_beta8f.py -- checks BayesTree beta 8f (1 Nov 2026), the fixes for what the monkey test found in
beta 8e (400 random runs: 1 division by zero, 47 typed lists):
  - a node's page with two tests and a small N: test 1's positives can round to 0 people, N on the tree is then 0,
    and the page's "share of N" was 0/0 ("Error: X/0"); it now says "(N is 0 here)";
  - a prior, sens or spec below 0 or above 1 (a 7 meant as 70 %) is refused with a sentence on the Values and Second
    test forms; beta 8e moved it to 0.999 or 0.01 without a word.  From 0 to 1 the program's limits apply as before;
  - an N outside 10 to 1,000,000, a negative count, and four counts adding to more than 1,000,000 are refused with a
    sentence (beta 8e: N below 10 became 10, a negative count 0);
  - every form field takes a real number only ({name,[0]});
  - bt_fmtp's "pv != 0" is "pv <> 0": on the Prime "!=" is a factorial and a test (the Virtual Calculator, 1 Nov
    2026), so its "< 0.001" floor never ran there, and at prior, sens and spec 0.999 the program ended with "Error:
    Numerical overflow";
  - three layout faults found by the overlap check on this script's screens: the tree's odds line ("odds 999.000 ×
    LR+ = 998001.000"), the Diagnostics page's DOR line with its cap note, and a piece of the two-test breadcrumb
    left beside the slider's label.

This is a new script in the repository's present layout (the 19 October scripts read the author's folders). It runs
from verify/ as it is: the program from ../programs, beta 8e from ../programs or git history (Lessons Learned rule
18), the harness, the overlap recorder and the monkey test from ../tools, hp-prime-kit from $HPKIT.  Every run
here has tools/prime_facts_v1.py's device facts (STRING(x, 2, d) is "Invalid input" for d of 13 or more, which the
harness does not yet model; the Virtual Calculator, 1 Nov 2026).  The CAS calls
go to the desktop Giac (icas) in part B; elsewhere the harness makes them fail (cas='fail'), and the program shows its
decimal answers, the same in both versions.

R  beta 8f against beta 8e over 50 states (priors, sens and spec at their limits and inside them, N 10 to
   1,000,000, two tests, forensic labels, the leaves as probabilities): the tree, eight views and 13 node pages,
   screen for screen; every text identical but for the two lines that ran into their neighbours (the odds line, the
   DOR's cap note), which are checked by value.
B  the Exact page and the tree's exact panel with the desktop CAS, both versions: identical.
M  the monkey test's findings, one check each, each also run on beta 8e, where it fails: the typed fields; the
   node page at N = 0; the monkey's own run (seed 11000398) replayed; the proportions refused, and nothing changed;
   the ends 0 and 1 accepted as before; N; the counts; Cancel on each form; every new box within 4 lines at 32
   characters a line (the Virtual Calculator wrapped 112 characters into 4 lines, 1 Nov 2026).
G  static: only the header, BayesTree, bt_DiagView, bt_NodeInfo, bt_fmtp (one line: "!=" is "<>") and the new
   bt_PBad and bt_fmtO differ from beta 8e; no "!=" in the code; every routine tagged bt_; at most six names per LOCAL
   line; only beta 8e's glyphs in strings.  ("!=" cannot be tested in the harness, which reads it as "not equal";
   on the Prime it is a factorial and a test, and beta 8e ended with "Numerical overflow" at prior, sens and spec
   0.999.  The Virtual Calculator's runs are in the change note.)
D  layout: text_overlap_v1 over every beta 8f screen drawn: no firm overlap, straddle or overrun (beta 8e had three:
   the tree's odds line at a prior of 0.999 ran into the spec number, the Diagnostics page's DOR line with a capped
   sens or spec ran past the right edge, and the two-test breadcrumb's first try, painted over to x 103 only, left
   the end of its last number beside the slider's "prior 0.999").

Run:  python3 verify_BayesTree_beta8f.py [BayesTree_beta8f.txt]     (exit code 0 = all passed)
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import textwrap
import warnings

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
_cands = [c for c in (os.environ.get('TTL_TOOLS', ''), os.path.join(HERE, 'tools'), os.path.join(HERE, '..', 'tools'),
                      HERE) if c]
TOOLS = None
for cand in reversed(_cands):
    if any(os.path.exists(os.path.join(cand, f)) for f in ('ppl_run_v3e.py', 'text_overlap_v1.py')):
        sys.path.insert(0, cand)
        TOOLS = cand
for cand in _cands:
    if os.path.exists(os.path.join(cand, 'ppl_run_v3e.py')):
        TOOLS = cand
        break
from ppl_run_v3e import Harness, CANCEL  # noqa: E402
import text_overlap_v1 as OV  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()      # the device facts the harness does not model yet: STRING(x, 2, d) refuses d >= 13

PROG = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'BayesTree_beta8f.txt')
if not os.path.exists(PROG):
    PROG = os.path.join(HERE, '..', 'programs', 'BayesTree_beta8f.txt')
SRC = open(PROG, encoding='utf-8').read()
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:500]) if (detail != '' and not ok) else ''))
    if ok:
        NPASS[0] += 1
    else:
        FAIL.append(name)


OLD_FROM = ['']


def older(name):
    """the previous version: beside this script, in ../programs, in an _superseded_* folder beside it (the author's
    D:\\HP-Prime), or from git history (Lessons Learned rule 18)"""
    for pth in [os.path.join(HERE, name), os.path.join(HERE, '..', 'programs', name)] + \
            sorted(glob.glob(os.path.join(HERE, '_superseded_*', name)), reverse=True):
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
                OLD_FROM[0] = 'git history'
                return pth
    except Exception:
        pass
    return None


OLD = older('BayesTree_beta8e.txt')
OV.install()


def run(script, path=PROG, cas='fail'):
    """the whole program: it opens with its menu; script queues the answers and the keys; Esc (idle) closes a view
    or a page, and Esc on the tree ends the program"""
    h = Harness(path, idle_key=4, home_minus=True, cas=cas)
    script(h)
    try:
        res = h.execute('BayesTree()')
        err = None
    except Exception as e:
        res, err = None, '%s: %s' % (type(e).__name__, str(e)[:150])
    return h, res, err


def boxes(h):
    return [' '.join(m.lines) for m in h.msgboxes]


def texts(h):
    return [tuple(s.lines()) for s in h.screens]


# the tree's tap boxes (btHX1..btHY2), id 1 to 13: the root, D+, D-, the four leaves, the two first-level numbers,
# the four second-level numbers; a tap at each box's centre
NODES = [(43, 111), (130, 58), (130, 176), (262, 38), (262, 90), (262, 154), (262, 206), (116, 83), (116, 141),
         (180, 38), (180, 78), (180, 156), (180, 196)]
VIEWS = (3, 4, 5, 6, 7, 10, 11, 14)          # ROC, PPV, 2x2, Diagnostics, Fagan, Icons, three prevalences, Help


def setup(pr, se, spc, N, test2=None, forensic=False, probs=False):
    """the Values form, then (each from the menu, opened with Enter) a second test, forensic labels, leaves as
    probabilities"""
    def f(h):
        h.choose(1)
        h.answer({'pr2': pr, 'se2': se, 'sp2': spc, 'np2': N})
        if test2:
            h.press('Enter')
            h.choose(8)
            h.answer({'se2': test2[0], 'sp2': test2[1]})
        if forensic:
            h.press('Enter')
            h.choose(12)
        if probs:
            h.press('Enter')
            h.choose(13)
    return f


def s_view(st, v):
    def f(h):
        st(h)
        h.press('Enter')
        h.choose(v)
    return f


def s_nodes(st, nodes=NODES):
    def f(h):
        st(h)
        h.press('Enter')
        h.choose(16)                                     # Close: the tree
        for x, y in nodes:
            h.tap(x, y, lift=True)                       # the node's page
            h.press('Enter')                             # any key: back to the tree
    return f


# ===================================================================== R. beta 8f = beta 8e where nothing changed
print('=== R. beta 8f against beta 8e, screen for screen, where nothing was meant to change')
print('   beta 8e: %s' % ((OLD_FROM[0] or os.path.relpath(OLD, HERE)) if OLD else 'NOT FOUND'))
states = []
for pr in (0.0001, 0.01, 0.3, 0.999):
    for se in (0.01, 0.9, 0.999):
        for spc in (0.01, 0.95, 0.999):
            states.append(dict(pr=pr, se=se, spc=spc, N=1000.0))
for N in (10.0, 1000000.0):
    for pr, se, spc in ((0.0001, 0.9, 0.95), (0.3, 0.6, 0.7), (0.999, 0.999, 0.01)):
        states.append(dict(pr=pr, se=se, spc=spc, N=N))
for kw in (dict(test2=(0.8, 0.9)), dict(forensic=True), dict(probs=True)):
    for pr, se, spc in ((0.001, 0.95, 0.99), (0.2, 0.7, 0.8)):
        d = dict(pr=pr, se=se, spc=spc, N=1000.0)
        d.update(kw)
        states.append(d)
# two tests after a near-certain test 1: the odds line's longest case ("998001 × LR+ = 997002999")
for pr, se, spc in ((0.999, 0.999, 0.999), (0.5, 0.999, 0.999)):
    states.append(dict(pr=pr, se=se, spc=spc, N=1000.0, test2=(0.999, 0.999)))

ODDS = re.compile(r'^(odds )?(.+?) × LR\+( = | < | > )(.+)$')


def is_odds(ln):
    return ' × LR+' in ln and ODDS.match(ln) is not None


def odds_8f(ln):
    """beta 8e's odds line as beta 8f writes it, as a set: an odds of 100 or more as a whole number (bt_fmtO), and
    the word "odds" only while the rest is at most 21 characters.  beta 8e's 3 decimals hide which side of 100 a
    value such as 99.99999999999999 lies (prior 0.1, sens 0.9, spec 0.999: 0.111 x 900), so "100.000" may stay."""
    m = ODDS.match(ln)
    out = set()
    for edge in (False, True):
        def w(t):
            if re.fullmatch(r'[0-9.]+', t) and float(t) >= 100 and not (edge and float(t) < 100.0005):
                return '%d' % round(float(t))
            return t
        core = w(m.group(2)) + ' × LR+' + m.group(3) + w(m.group(4))
        out.add(('odds ' + core) if len(core) <= 21 else core)
    return out


CAP_OLD, CAP_NEW = '   (sens or spec at its 0.999 cap)', '   (at the 0.999 cap)'


def as_8f(scr):
    """a beta 8e screen's text with beta 8f's two layout changes applied: each line as the set of lines beta 8f may
    write there"""
    return tuple(odds_8f(ln) if is_odds(ln) else {ln.replace(CAP_OLD, CAP_NEW)} for ln in scr)


def same_8f(tn, to):
    """beta 8f's screens tn are beta 8e's to with the two layout changes"""
    return len(tn) == len(to) and all(len(a) == len(b) and all(x in y for x, y in zip(a, as_8f(b)))
                                      for a, b in zip(tn, to))


same, diff, errs, nscreens = 0, [], [], 0
n_odds, n_cap, long_odds, firm_8f = 0, 0, [], []
for st in states:
    sf = setup(st['pr'], st['se'], st['spc'], st['N'], st.get('test2'), st.get('forensic'), st.get('probs'))
    for nm, sc in [('view %d' % v, s_view(sf, v)) for v in VIEWS] + [('13 node pages', s_nodes(sf))]:
        hn, rn, en = run(sc)
        ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'no beta 8e')
        nscreens += len(hn.screens)
        if en or eo:
            errs.append((st, nm, en, eo))
            continue
        tn, to = texts(hn), texts(ho)
        n_odds += sum(1 for sc_ in tn for ln in sc_ if is_odds(ln) and ln not in [x for y in to for x in y])
        n_cap += sum(1 for sc_ in tn for ln in sc_ if CAP_NEW in ln)
        long_odds += [ln for sc_ in tn for ln in sc_ if is_odds(ln) and len(ln) > 26]
        if same_8f(tn, to) and rn == ro and boxes(hn) == boxes(ho):
            same += 1
        else:
            diff.append((st, nm, [(a_, b_) for x, y in zip(tn, to) for a_, b_ in zip(x, as_8f(y)) if a_ not in b_][:2]))
check('R1 %d states x (eight views and the 13 node pages) = %d runs, %d screens: beta 8f\'s text is beta 8e\'s on '
      'every screen, but for the two lines that ran into their neighbours, with the same summary, and no error in '
      'either' % (len(states), same + len(diff) + len(errs), nscreens),
      OLD is not None and not diff and not errs and same == len(states) * (len(VIEWS) + 1), (diff[:3], errs[:3]))
check('R2 the odds line: odds of 100 or more as whole numbers (%d lines differ from beta 8e\'s), every line at most 26 '
      'characters, so it ends before the spec number at x 168; "odds" left out only with two near-certain tests'
      % n_odds, n_odds > 0 and not long_odds, long_odds[:4])
check('R3 the Diagnostics page\'s DOR line reads "(at the 0.999 cap)" (%d screens), inside the screen (part D)'
      % n_cap, n_cap > 0, '')

# ===================================================================== B. the CAS
print('=== B. the exact answers with the desktop CAS (icas)')
bres = []
for st in (setup(0.1, 0.9, 0.95, 1000.0), setup(0.001, 0.95, 0.99, 1000.0, test2=(0.8, 0.9)),
           setup(0.02, 0.9, 0.95, 1000.0, forensic=True)):
    sc = s_view(st, 15)
    hn, rn, en = run(sc, cas='giac')
    ho, ro, eo = run(sc, OLD, cas='giac') if OLD else (None, None, 'no beta 8e')
    bres.append((en, eo, texts(hn) == texts(ho), len(hn.cas_calls)))
check('B1 the Exact page and the tree\'s exact panel, three cases (one test, two tests, forensic), with the desktop '
      'CAS: identical in both versions, no error (CAS calls %s)' % [b[3] for b in bres],
      all(b[0] is None and b[1] is None and b[2] and b[3] > 0 for b in bres), bres)

# ===================================================================== M. the monkey test's findings
print("=== M. the monkey test's findings (1 Nov 2026; each check fails on beta 8e)")


def split_top(t):
    out, d, cur = [], 0, ''
    for ch in t:
        if ch in '([{':
            d += 1
        elif ch in ')]}':
            d -= 1
        if ch == ',' and d == 0:
            out.append(cur.strip())
            cur = ''
        else:
            cur += ch
    out.append(cur.strip())
    return out


def input_fields(src):
    code_ = '\n'.join(ln.split('//')[0] for ln in src.split('\n'))
    out = []
    for m in re.finditer(r'\bINPUT\(', code_):
        i = j = m.end()
        d = 0
        while True:
            ch = code_[j]
            if ch in '([{':
                d += 1
            elif ch in ')]}':
                d -= 1
                if d < 0:
                    break
            elif ch == ',' and d == 0:
                break
            j += 1
        a = code_[i:j].strip()
        out.append(split_top(a[1:-1]) if a.startswith('{') else [a])
    return out


OSRC = open(OLD, encoding='utf-8').read() if OLD else ''
ff, ffo = input_fields(SRC), input_fields(OSRC)
typed = all(re.fullmatch(r'\{[A-Za-z]\w*,\[0\]\}', x) for f in ff for x in f)
typed_old = any(re.fullmatch(r'\{[A-Za-z]\w*,\[0\]\}', x) for f in ffo for x in f)
check('M1 all %d forms take real numbers only: every field is {name,[0]} (%d fields), so the form refuses a typed '
      'list; beta 8e\'s were bare names' % (len(ff), sum(len(f) for f in ff)),
      len(ff) == 3 and sum(len(f) for f in ff) == 10 and typed and OLD is not None and not typed_old, ff)

# M2: two tests, N = 10, prior 0.0001, sens 0.01, spec 0.999: test 1's positives are 10 x (0.0001 x 0.01 + 0.9999 x
# 0.001) = 0.01 people, and the tree's root (rounded) holds 0
zst = setup(0.0001, 0.01, 0.999, 10.0, test2=(0.9, 0.95))
hn, rn, en = run(s_nodes(zst))
ho, ro, eo = run(s_nodes(zst), OLD) if OLD else (None, None, 'no beta 8e')
pages = [ln for s in hn.screens for ln in s.lines() if ln.startswith('count =')]
check('M2 two tests at N = 10 (test 1\'s positives: 0.01 people, the root 0): all 13 node pages open, and the six count '
      'pages say "count = 0  (N is 0 here)"; beta 8e: %s' % (eo or 'no error'),
      en is None and pages.count('count = 0  (N is 0 here)') == 6 and OLD is not None and eo is not None
      and 'zero' in eo, (en, pages[:8], eo))


def monkey_replay(prog, seed=11000398):
    tool = os.path.join(TOOLS, 'monkey_v1b.py') if TOOLS else None
    if not tool or not os.path.exists(tool):
        return 'no monkey_v1b.py'
    out = subprocess.run([sys.executable, tool, prog, 'BayesTree()', '--lists', '--events', '150', '--replay',
                          str(seed)], capture_output=True, text=True, timeout=600).stdout
    m = re.search(r'"verdict":\s*"(\w+)"', out)
    return m.group(1) if m else out[-200:]


vn, vo = monkey_replay(PROG), (monkey_replay(OLD) if OLD else 'no beta 8e')
check('M3 the monkey\'s own run, seed 11000398 (sens 7 typed, then taps), replayed: beta 8f %s, beta 8e %s'
      % (vn, vo), vn == 'OK' and vo == 'CRASH', (vn, vo))

DEF = 'BayesTree: PPV = 0.667, NPV = 0.988 (prior 0.100, sens 0.900, spec 0.950)'


def s_vals(d):
    def f(h):
        h.choose(1)
        h.answer(d)
        h.press('Enter')
        h.choose(16)
    return f


def s_t2(d):
    def f(h):
        h.choose(8)
        h.answer(d)
        h.press('Enter')
        h.choose(16)
    return f


P = lambda nm, ex: '%s is a proportion from 0 to 1: type %s. Nothing changed.' % (nm, ex)  # noqa: E731
BIG = 'A number you typed has more than 50 digits: too large to work with. Nothing changed.'
NMSG = 'N is the number of people at the root of the tree: 10 to 1,000,000. Nothing changed.'
cases = (
    ('Values, prior 25', s_vals({'pr2': 25.0}), P('The prior', '0.02 for 2 %')),
    ('Values, prior -0.1', s_vals({'pr2': -0.1}), P('The prior', '0.02 for 2 %')),
    ('Values, sens 7', s_vals({'se2': 7.0}), P('sens', '0.7 for 70 %')),
    ('Values, sens 70', s_vals({'se2': 70.0}), P('sens', '0.7 for 70 %')),
    ('Values, spec 98.6', s_vals({'sp2': 98.6}), P('spec', '0.95 for 95 %')),
    ('Values, spec 1.0001', s_vals({'sp2': 1.0001}), P('spec', '0.95 for 95 %')),
    ('Values, sens 1E60', s_vals({'se2': 1E60}), BIG),
    ('Values, N 9.9', s_vals({'np2': 9.9}), NMSG),
    ('Values, N -5', s_vals({'np2': -5.0}), NMSG),
    ('Values, N 1000001', s_vals({'np2': 1000001.0}), NMSG),
    ('Values, N 1E60', s_vals({'np2': 1E60}), NMSG),
    ('Second test, sens 2 = 7', s_t2({'se2': 7.0}), P('sens 2', '0.7 for 70 %')),
    ('Second test, spec 2 = -0.5', s_t2({'sp2': -0.5}), P('spec 2', '0.95 for 95 %')),
)
res = []
DEF_N = texts(run(s_vals({}))[0])                        # the screens when nothing is changed (OK as shown)
DEF_O = texts(run(s_vals({}), OLD)[0]) if OLD else None
for name, sc, want in cases:
    hn, rn, en = run(sc)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'no beta 8e')
    # nothing changed: the summary and every screen as with OK on the untouched form; beta 8e changed something (the
    # summary, or for N, which the summary does not name, the tree)
    ok = en is None and boxes(hn) == [want] and rn == DEF and texts(hn) == DEF_N and OLD is not None and eo is None \
        and not boxes(ho) and (ro != DEF or texts(ho) != DEF_O)
    res.append((name, ok, boxes(hn), rn, ro))
    check('M4 %s: "%s", nothing changed; beta 8e: no box, and %s' % (
        name, want[:44] + '...', ((ro or '')[34:] if ro != DEF else 'a different tree')), ok, (en, boxes(hn), rn, eo))

# the ends: 0 and 1 are proportions; the program's limits apply as before, with no box, as in beta 8e
ends = []
for d in ({'pr2': 0.0}, {'pr2': 1.0}, {'se2': 0.0}, {'se2': 1.0}, {'sp2': 0.0}, {'sp2': 1.0}, {'np2': 10.0},
          {'np2': 1000000.0}, {'np2': 10.7}):
    hn, rn, en = run(s_vals(d))
    ho, ro, eo = run(s_vals(d), OLD) if OLD else (None, None, 'no beta 8e')
    ends.append((d, en is None and not boxes(hn) and rn == ro and same_8f(texts(hn), texts(ho))))
check('M5 the ends accepted as before, no box, every screen as in beta 8e (but for part R\'s odds line: a prior of 1 '
      'is 0.999, odds 999): prior, sens, spec 0 and 1; N 10, 1,000,000 and 10.7 (cut to 10): %s'
      % [e[1] for e in ends], all(e[1] for e in ends), ends)


def s_cnt(d):
    def f(h):
        h.choose(2)
        h.answer(d)
        h.press('Enter')
        h.choose(16)
    return f


CNEG = 'A count is a number of people: 0 or more. Nothing changed.'
CBIG = 'The four counts add to more than 1,000,000 people: too many for the tree. Nothing changed.'
for name, d, want in (('a count of -3', {'fn': -3.0}, CNEG),
                      ('counts 400,000 + 300,000 + 200,000 + 100,001', {'tp': 400000.0, 'fn': 300000.0,
                                                                         'btFP': 200000.0, 'tn': 100001.0}, CBIG),
                      ('a count of 1E60', {'tn': 1E60}, CBIG)):
    hn, rn, en = run(s_cnt(d))
    ho, ro, eo = run(s_cnt(d), OLD) if OLD else (None, None, 'no beta 8e')
    check('M6 Enter counts, %s: "%s", nothing changed; beta 8e: no box, %s' % (name, want[:40] + '...',
                                                                               eo or (ro or '')[34:]),
          en is None and boxes(hn) == [want] and rn == DEF and OLD is not None and not boxes(ho) and ro != DEF,
          (en, boxes(hn), rn, eo, ro))
d = {'tp': 400000.0, 'fn': 100000.0, 'btFP': 100000.0, 'tn': 400000.0}
hn, rn, en = run(s_cnt(d))
ho, ro, eo = run(s_cnt(d), OLD) if OLD else (None, None, 'no beta 8e')
check('M6 counts adding to exactly 1,000,000 accepted, every screen as in beta 8e (%s)' % (rn or '')[11:],
      en is None and not boxes(hn) and rn == ro and same_8f(texts(hn), texts(ho)), (en, boxes(hn), rn, ro))

canc = []
for nm, sc in (('Values', lambda h: (h.choose(1), h.answer(CANCEL), h.press('Enter'), h.choose(16))),
               ('Counts', lambda h: (h.choose(2), h.answer(CANCEL), h.press('Enter'), h.choose(16))),
               ('Second test', lambda h: (h.choose(8), h.answer(CANCEL), h.press('Enter'), h.choose(16)))):
    hn, rn, en = run(sc)
    ho, ro, eo = run(sc, OLD) if OLD else (None, None, 'no beta 8e')
    canc.append((nm, en is None and rn == DEF and not boxes(hn) and same_8f(texts(hn), texts(ho))))
check('M7 Cancel on each form changes nothing and shows no box, as in beta 8e: %s' % canc, all(c[1] for c in canc), canc)

msgs = sorted(set([c[2] for c in cases] + [CNEG, CBIG]))
lines = [len(textwrap.wrap(m, 32)) for m in msgs]
check('M8 every new box within 4 lines at 32 characters a line: %s' % lines, max(lines) <= 4, lines)

# ===================================================================== G. static
print('=== G. static checks')


def bodies(txt):
    """routine name -> its text, from its head line to the next head line (comments kept)"""
    lines_ = txt.split('\n')
    heads = [i for i, ln in enumerate(lines_) if re.match(r'^(EXPORT\s+)?[A-Za-z_]\w*\([^()]*\)\s*$', ln)]
    out = {}
    for k, i in enumerate(heads):
        nm = re.match(r'^(?:EXPORT\s+)?([A-Za-z_]\w*)', lines_[i]).group(1)
        out[nm] = '\n'.join(lines_[i:heads[k + 1] if k + 1 < len(heads) else len(lines_)])
    return out, '\n'.join(lines_[:heads[0]]) if heads else txt


bn, hdn = bodies(SRC)
bo, hdo = bodies(OSRC) if OLD else ({}, '')
changed = sorted(k for k in set(bn) | set(bo) if bn.get(k) != bo.get(k))
WANT = ['BayesTree', 'bt_BEp', 'bt_DiagView', 'bt_NodeInfo', 'bt_PBad', 'bt_fmtO', 'bt_fmtp']
check('G1 only BayesTree, bt_DiagView, bt_NodeInfo, bt_fmtp and the new bt_PBad and bt_fmtO differ from beta 8e (and '
      'bt_BEp\'s block, which the new routines follow): %s' % changed, changed == WANT, changed)
fp_n = [ln.strip() for ln in bn.get('bt_fmtp', '').split('\n') if ln.strip() and not ln.strip().startswith('//')]
fp_o = [ln.strip() for ln in bo.get('bt_fmtp', '').split('\n') if ln.strip() and not ln.strip().startswith('//')]
check('G1 bt_fmtp differs from beta 8e in one code line, "pv != 0" written "pv <> 0"',
      [a for a in fp_n if a not in fp_o] == ['IF pv <> 0 AND ABS(pv) < thr THEN']
      and [a for a in fp_o if a not in fp_n] == ['IF pv != 0 AND ABS(pv) < thr THEN'], (fp_n, fp_o))
upto_end = lambda t: t[:t.index('\nEND;') + 5] if '\nEND;' in t else t  # noqa: E731
check('G1 bt_BEp\'s code is beta 8e\'s, character for character (only the comment above bt_PBad follows it)',
      upto_end(bn.get('bt_BEp', '')) == upto_end(bo.get('bt_BEp', '-')), '')
code = [ln.split('//')[0] for ln in SRC.split('\n')]
routines = re.findall(r'^([A-Za-z_]\w*)\([^()]*\)\s*$', SRC, re.M)
check('G2 %d routines; every one but the EXPORT is tagged bt_' % len(routines),
      all(r.startswith('bt_') for r in routines) and re.search(r'^EXPORT BayesTree\(\)', SRC, re.M) is not None,
      [r for r in routines if not r.startswith('bt_')])
ne_n = [ln.strip() for ln in code if '!=' in ln]
ne_o = [ln.split('//')[0].strip() for ln in OSRC.split('\n') if '!=' in ln.split('//')[0]]
check('G4 no "!=" in the code (on the Prime it is a factorial and an "=": {3!=0, 0!=0} gave {0, 0} and 999!=0 '
      '"Numerical overflow", Virtual Calculator, 1 Nov 2026); beta 8e had %d' % len(ne_o), not ne_n and len(ne_o) == 1,
      ne_n)
wide = [ln.strip() for ln in code if re.match(r'\s*LOCAL\b', ln) and len(ln.split('LOCAL', 1)[1].split(',')) > 6]
check('G2 at most six names on every LOCAL line', not wide, wide)
VERIFIED = set('χ²√≥≤≠±×→∞αβμσφθρλ⇆⇅') | {chr(8320), chr(8321), chr(8322), chr(8323), chr(57344), chr(8722), '—', '…',
                                         '·', '←', '↑', '↓'}
glyphs = sorted(set(c for ln in code for c in ln if ord(c) > 126))
gl_old = sorted(set(c for ln in OSRC.split('\n') for c in ln.split('//')[0] if ord(c) > 126))
check('G3 the glyphs in the code\'s strings are beta 8e\'s own set: %s' % ''.join(glyphs), glyphs == gl_old,
      (glyphs, gl_old))

# ===================================================================== D. layout
print('=== D. layout (text_overlap_v1 over every screen above)')
rep = OV.report()
tag = [t for t in rep if t.startswith(os.path.splitext(os.path.basename(PROG))[0])]
f = rep[tag[0]] if tag else None
firm = []
if f:
    firm += [('overlap', c['a'], c['b']) for c in f['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm += [('straddle', x['text'], x['edge']) for x in f['straddles'] if x['firm']]
    firm += [('overrun', x['text'], x.get('right')) for x in f['overruns'] if x['firm']]
    print('   screens: %d distinct of %d' % (f['screens_distinct'], f['screens_total']))
tago = [t for t in rep if t.startswith('BayesTree_beta8e')]
fo = rep[tago[0]] if tago else None
firm_o = []
if fo:
    firm_o += [('overlap', c['a'], c['b']) for c in fo['collisions'] if c['severity'] == 'overlap' and c['firm']]
    firm_o += [('straddle', x['text'], x['edge']) for x in fo['straddles'] if x['firm']]
    firm_o += [('overrun', x['text'], x.get('right')) for x in fo['overruns'] if x['firm']]
check('D1 no firm overlap, frame straddle or overrun on any beta 8f screen drawn (beta 8e, on the same runs: %d: %s)'
      % (len(firm_o), sorted(set(str(x[1])[:40] for x in firm_o))[:3]), bool(tag) and not firm, firm[:8])

print()
print('%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for n_ in FAIL:
    print('  FAILED: ' + n_)
sys.exit(1 if FAIL else 0)
