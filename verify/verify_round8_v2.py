#!/usr/bin/env python3
"""verify_round8_v2.py -- checks round 8 (4 Nov 2026, evening and night): the monkey test's 1,000 runs on the 16 programs
that had not had them, and the fixes.  Fourteen programs changed: AgreeLab beta 1e, AnovaLab beta 1c, BiNorm3D
beta 1d, BurrLab beta 1m, DNAMixLR beta 3h, DataLoad beta 1d, ErrorRate beta 1h, FitCheck beta 1c, RankLab beta 1d,
ResampLab beta 1e, SeizureLab beta 1d (renamed ExhibitLab beta 1d the same night), StudRange beta 15j, SurvLab beta 1d and TrendTest beta 3j (RiskLab and
TestChooser passed 1,000 of 1,000 unchanged).  Later the same night "t test" became "t-test" on every screen and in
every comment (Roger, 4 Nov 2026): in AnovaLab beta 1c, FitCheck beta 1c and StudRange beta 15j, which had not been
released, and in four new versions, PowerViz v2.5o, TTestLab beta 1f, TTestLabG beta 1d and TestChooser beta 2e.

For each, against the version before it (programs/, a _superseded folder or git history):
  T1  every INPUT form's fields are typed {name,[0]}, as many forms as the change note says;
  T2  with comments out and every {name,[0]} read as name, only the routines named below differ from the old version
      (the forms' routines are the same code but for the typing; a welcome page differs in its version string);
  T3  the header names the new version.
  (In T2 every "t test" of the old version is read as "t-test", and for ExhibitLab and DataLoad SeizureLab as
  ExhibitLab and SZ_ as EX_: the rename.)
  T4  for the four new versions, the whole file is the old one with every "t test" made "t-test", the header's
      version and a three-line change note, and nothing else: line by line.
Then the harness runs the extra fixes:
  X1  each list reader (AgreeLab, AnovaLab, RankLab, FitCheck) leaves out a list holding 1E300, with its sentence,
      and returns an ordinary list unchanged;
  X2  ResampLab's, BurrLab's and ExhibitLab's (SeizureLab's) own-data readers refuse 1E300 with the sentence;
  X3  AnovaLab's one-sigma test refuses sigma0 = 1E-300 (v1b divided by zero there) and takes sigma0 = 10;
  X4  DataLoad's SD: the old value for ordinary lists, and a finite SD for 1E300, -1E300, 5 (Python's own, scaled).
  X5  RankLab's one-sample m0 beyond 1E50 is refused with a sentence and 3 is taken (beta 1d's own monkey run, seed
      1000810, typed -1E300), and rk_Num keeps a scientific number's exponent (1E300 had read 1.0000E3); both fail on
      beta 1c.
The monkey test's 1,000 runs, before and after, are in verify/monkey_<Name>_<version>_output.txt.
Run from the repository:  python3 verify/verify_round8_v2.py"""
import os, re, sys, subprocess, tempfile, glob, math, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import comma_check_v1 as CC  # noqa: E402
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
from ppl_run_v3e import Harness  # noqa: E402
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:500]) if detail != '' and not ok else ''))
    (FAIL.append(name) if not ok else NPASS.__setitem__(0, NPASS[0] + 1))


def older(name):
    for p in [os.path.join(ROOT, 'programs', name)] + sorted(glob.glob(os.path.join(ROOT, '..', '_superseded_*', name)), reverse=True) \
            + sorted(glob.glob(os.path.join(ROOT, '_old*', name))):
        if os.path.exists(p):
            return p
    rel = 'programs/' + name
    try:
        c = subprocess.run(['git', '-C', ROOT, 'rev-list', '-n', '1', 'HEAD', '--', rel], capture_output=True, text=True).stdout.strip()
        for ref in ((c + ':' + rel, c + '^:' + rel) if c else ()):
            o = subprocess.run(['git', '-C', ROOT, 'show', ref], capture_output=True)
            if o.returncode == 0:
                p = os.path.join(tempfile.mkdtemp(), name)
                open(p, 'wb').write(o.stdout)
                return p
    except Exception:
        pass
    return None


T = [  # new, old, forms, header, routines allowed to differ beyond the typing
    ('AgreeLab_beta1e', 'AgreeLab_beta1d', 2, '// AGREELAB - beta 1e', ['ag_Hello', 'ag_ReadD']),
    ('AnovaLab_beta1c', 'AnovaLab_beta1b', 5, '// ANOVALAB - beta 1c', ['av_Hello', 'av_ReadD', 'av_V1Ask', 'av_V2Ask']),
    ('BiNorm3D_beta1d', 'BiNorm3D_beta1c', 1, '// BINORM3D - beta 1d', []),
    ('BurrLab_beta1m', 'BurrLab_beta1l', 2, '// BurrLab - beta 1m', ['bu_LoadMine', 'bu_Opening']),
    ('DNAMixLR_beta3h', 'DNAMixLR_beta3g', 15, '// DNAMIXLR - beta 3h', []),
    ('DataLoad_beta1d', 'DataLoad_beta1c', 1, '// DATALOAD - beta 1d', ['dd_Stats']),
    ('ErrorRate_beta1h', 'ErrorRate_beta1g', 4, '// ERRORRATE LAB - beta 1h', []),
    ('FitCheck_beta1c', 'FitCheck_beta1b', 2, '// FITCHECK - beta 1c', ['fc_Opening', 'fc_ReadD1', 'fc_ReadD2']),
    ('RankLab_beta1d', 'RankLab_beta1c', 1, '// RANKLAB - beta 1d', ['rk_MyData', 'rk_Num', 'rk_ReadD', 'rk_Welcome']),
    ('ResampLab_beta1e', 'ResampLab_beta1d', 1, '// RESAMPLAB - beta 1e', ['rs_Mine', 'rs_Splash']),
    ('ExhibitLab_beta1d', 'SeizureLab_beta1c', 3, '// EXHIBITLAB - beta 1d', ['sz_WtLoad']),
    ('StudRange_beta15j', 'StudRange_beta15i', 13, '// STUDRANGE - beta 15j', None),
    ('SurvLab_beta1d', 'SurvLab_beta1c', 1, '// SURVLAB - beta 1d', []),
    ('TrendTest_beta3j', 'TrendTest_beta3i', 5, '// TRENDTEST - beta 3j', None),
    ('PowerViz_v2.5o', 'PowerViz_v2.5n', None, '// POWERVIZ - v2.5o', []),
    ('TTestLab_beta1f', 'TTestLab_beta1e', None, '// TTESTLAB - beta 1f', []),
    ('TTestLabG_beta1d', 'TTestLabG_beta1c', None, '// TTESTLABG - beta 1d', []),
    ('TestChooser_beta2e', 'TestChooser_beta2d', None, '// TESTCHOOSER - beta 2e', []),
]
TT = re.compile(r'\b([tT]) ([tT]ests?)\b')     # "t test" -> "t-test" (4 Nov 2026, night)
NEWV = {'PowerViz_v2.5o', 'TTestLab_beta1f', 'TTestLabG_beta1d', 'TestChooser_beta2e'}
EXTRA_ALLOWED = {}   # filled for StudRange and TrendTest by make_round8b's notes
TY = re.compile(r'\{([A-Za-z_]\w*),\[0\]\}')
for new, old, nf, hdr, allowed in T:
    pn = os.path.join(ROOT, 'programs', new + '.txt')
    if not os.path.exists(pn):
        print('=== %s: not in programs/, skipped' % new)
        continue
    po = older(old + '.txt')
    print('=== %s against %s' % (new, os.path.relpath(po, ROOT) if po else 'NOT FOUND'))
    if not po:
        check(new + ' older version found', False)
        continue
    sn, so = open(pn, encoding='utf-8').read(), TT.sub(r'\1-\2', open(po, encoding='utf-8').read())
    so = re.sub(r'\bSZ_', 'EX_', so.replace('SeizureLab', 'ExhibitLab')) if new.startswith(('ExhibitLab', 'DataLoad')) else so   # the rename
    code = CC.strip_comments(sn)
    forms = re.findall(r'INPUT\(\s*\{(.*?)\}\s*,', code, re.S)
    forms = re.findall(r'INPUT\(\s*(\{(?:\{[A-Za-z_]\w*,\[0\]\}(?:\s*,\s*)?)+\}|\{[^{}]*\})', code)
    untyped = [f for f in forms if not f.startswith('{{')]
    if nf is None:   # the four new versions: the same forms as before, already typed in an earlier round
        nf = len(re.findall(r'INPUT\(', CC.strip_comments(so)))
    check('T1 %s: %d forms, every field typed {name,[0]}' % (new, len(forms)), len(forms) == nf and not untyped, (len(forms), untyped[:2]))
    rn, ro = CC.routines(TY.sub(r'\1', code)), CC.routines(TY.sub(r'\1', CC.strip_comments(so)))   # typing read as the name in both
    diff = sorted(r for r in set(ro) | set(rn) if ro.get(r) != rn.get(r))
    allow = set(allowed if allowed is not None else EXTRA_ALLOWED.get(new, []))
    check('T2 %s: beyond the typing, only %s differ: %s' % (new, sorted(allow) or 'no routines', diff), set(diff) <= allow, diff)
    check('T3 %s: the header names the version' % new, hdr in sn[:2000], sn[:120])
    if new in NEWV:
        import difflib
        a, b = so.split('\n'), sn.split('\n')
        odd = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag == 'equal': continue
            old_l, new_l = a[i1:i2], b[j1:j2]
            if tag == 'replace' and len(old_l) == 1 and len(new_l) == 1 and old_l[0].startswith('// ') and hdr in new_l[0]:
                continue                                   # the header's version
            if tag == 'insert' and sorted(new_l) == sorted(['//'] + [l for l in new_l if l != '//'][:2]) and len(new_l) == 3 \
                    and sum('"t test" now reads "t-test"' in l for l in new_l) == 1 and sum(l.startswith('//   and in the comments (') for l in new_l) == 1:
                continue                                   # the change note
            odd.append((tag, old_l[:2], new_l[:2]))
        n_tt = len(TT.findall(open(po, encoding='utf-8').read()))
        check('T4 %s: the old file with its %d "t test" made "t-test", the header and the note; nothing else' % (new, n_tt),
              not odd and n_tt > 0 and '(%d places)' % n_tt in sn, odd[:3])

print('=== X. the extra fixes, in the harness')


def H(name, d1=None, d2=None):
    app = {}
    if d1 is not None: app['D1'] = d1
    if d2 is not None: app['D2'] = d2
    return Harness(os.path.join(ROOT, 'programs', name + '.txt'), idle_key=4, app_data=app or None)


def boxes(h):
    return [m.text for m in h.msgboxes]


BIG = [1.0, 1E300, 2.0]
OKL = [3.0, 1.0, 4.0, 1.0, 5.0]
bad = []
for name, call in (('AgreeLab_beta1e', 'ag_ReadD(1)'), ('AnovaLab_beta1c', 'av_ReadD(1)'), ('RankLab_beta1d', 'rk_ReadD(1)'),
                   ('FitCheck_beta1c', 'fc_ReadD1()')):
    h = H(name, BIG, OKL)
    r = h.execute(call)
    if r != [] or not any('more than 50 digits' in t and 'D1' in t for t in boxes(h)):
        bad.append((name, 'big', r, boxes(h)[:1]))
    h = H(name, OKL, OKL)
    r = h.execute(call)
    if list(r) != OKL or boxes(h):
        bad.append((name, 'ordinary', r, boxes(h)[:1]))
h = H('FitCheck_beta1c', OKL, BIG)
if h.execute('fc_ReadD2()') != [] or not any('D2' in t for t in boxes(h)):
    bad.append(('FitCheck D2', boxes(h)[:1]))
check('X1 the list readers leave out a list holding 1E300, with its sentence, and return an ordinary list as it is', not bad, bad)
bad = []
for name, call, d1 in (('ResampLab_beta1e', 'rs_Mine()', BIG), ('BurrLab_beta1m', 'bu_LoadMine()', [1.0, 2.0, 3.0, 4.0, 1E300, 6.0]),
                       ('ExhibitLab_beta1d', 'sz_WtLoad(1)', [0.5, 1E300, 0.6])):
    h = H(name, d1, [])
    if name.startswith('Exhibit'):
        h.globals_['szN'] = 100.0
    try:
        r = h.execute(call)
    except Exception as e:
        bad.append((name, 'CRASH', str(e)[:80])); continue
    if r != 0 or not any('more than 50 digits' in t for t in boxes(h)):
        bad.append((name, r, boxes(h)[:2]))
check('X2 ResampLab, BurrLab and ExhibitLab refuse own data holding 1E300, with the sentence', not bad, bad)
bad = []
for s0, want in ((1E-300, True), (10.0, False)):
    h = H('AnovaLab_beta1c')
    h.choose(1)
    h.answer({'vaS': 12.0, 'vaN': 20.0})
    h.answer({'vaS0': s0, 'vaC': 0.95})
    try:
        h.execute('av_V1Ask()')
    except Exception as e:
        bad.append((s0, 'CRASH', str(e)[:80])); continue
    got = any('from 1E-50 to 1E50' in t for t in boxes(h))
    if got != want:
        bad.append((s0, boxes(h)[:2]))
check('X3 AnovaLab\'s one-sigma test refuses sigma0 = 1E-300 with a sentence and takes 10', not bad, bad)
bad = []
for L in ([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0], [1.5, 2.5], [10.0] * 5, [3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0]):
    hn, ho = H('DataLoad_beta1d'), Harness(older('DataLoad_beta1c.txt'), idle_key=4)
    sn_, so_ = hn.execute('dd_Stats(%s)' % ('{' + ','.join(repr(x) for x in L) + '}')), ho.execute('dd_Stats(%s)' % ('{' + ','.join(repr(x) for x in L) + '}'))
    want = statistics.stdev(L)
    if abs(sn_[2] - want) > 1E-9 * max(1, want) or abs(so_[2] - sn_[2]) > 1E-9 * max(1, want):
        bad.append((L, sn_[2], so_[2], want))
L = [1E300, -1E300, 5.0]
try:
    sd = H('DataLoad_beta1d').execute('dd_Stats({1E300,-1E300,5})')[2]
    m = sum(L) / 3; sc = max(abs(x - m) for x in L); want = sc * math.sqrt(sum(((x - m) / sc) ** 2 for x in L) / 2)
    if not (math.isfinite(sd) and abs(sd - want) <= 1E-9 * want):
        bad.append(('1E300', sd, want))
except Exception as e:
    bad.append(('1E300', 'CRASH', str(e)[:80]))
check('X4 DataLoad\'s SD: the old value for ordinary lists (statistics.stdev), and a finite SD for 1E300, -1E300, 5', not bad, bad)
bad = []
for prog in ('RankLab_beta1d', 'RankLab_beta1c'):
    path = os.path.join(ROOT, 'programs', prog + '.txt') if prog.endswith('1d') else older(prog + '.txt')
    res = []
    for m0, want_refused in ((-1E300, True), (3.0, False)):
        h = Harness(path, idle_key=4, app_data={'D1': [1.0, 4.0, 2.0, 8.0, 5.0, 7.0]})
        h.choose(3)
        h.answer({'myM': m0})
        try:
            r = h.execute('rk_MyData()')
        except Exception as e:
            res.append((m0, 'CRASH', str(e)[:60])); continue
        refused = r == 0 and any('more than 50 digits' in t for t in boxes(h))
        res.append((m0, refused == want_refused))
    h = Harness(path, idle_key=4)
    nums = [h.execute('rk_Num(%s)' % v) for v in ('1E300', '-1.5E20', '2.25', '12345.678')]
    ok = all(x[1] is True for x in res) and nums == ['1\u1d07300', '-1.5\u1d0720', '2.25', '12345.678']
    if (prog.endswith('1d') and not ok) or (prog.endswith('1c') and ok):
        bad.append((prog, res, nums))
check('X5 RankLab: m0 beyond 1E50 refused with a sentence, 3 taken, and 1E300 shown as 1\u1d07300; beta 1c fails it', not bad, bad)
print('\n%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for f in FAIL:
    print('  FAILED: ' + f)
sys.exit(1 if FAIL else 0)
