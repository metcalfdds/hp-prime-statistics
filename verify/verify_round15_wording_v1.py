#!/usr/bin/env python3
"""verify_round15_wording_v1.py -- checks the wording part of Round 15 (15 Nov 2026): what five programs say about the
TI-83/84 programs they follow: RankLab beta 1i, AnovaLab beta 1h, ResampLab beta 1i, ExhibitLab beta 1h and SurvLab beta 1g.
(FitCheck beta 1h, the sixth, has its own script, verify_FitCheck_beta1h.py, because it also has new arithmetic.)
Only words changed, so the checks are of the text and of everything else staying put.  Made from verify_round12_v1.py.

Runs from the repository alone (Lessons Learned s14 rule 18): tools/, programs/ and verify/ by relative path, the old
versions from git (the commit before Round 15, make_wording_r15.BASE).  Needs hp-prime-kit (HPKIT) for the harness.

  T1  verify/round15/make_wording_r15.py, run again from the old versions, makes each new file byte for byte.
  T2  each new file differs from its old one only in (a) the lines of the build's own replacements, (b) comment lines
      (the header and the history note), and (c) lines whose only change is the version string, old to new.
  T3  the help pages, dumped again by the harness (verify/round11/helpdump_r11.py), are verify/round15/helppages_r15.json;
      against the old versions' dump, the only screen that changed is the credits page of RankLab, AnovaLab and
      ResampLab, and no screen of ExhibitLab or SurvLab changed.
  T4  every help screen laid out at the glyph widths GlyphProbe_v1 measured (verify/round11/helpcheck_r11.py): no line
      past its width argument or the screen's edge and no two texts overlapping.
  T5  tools/ppl_gate_v1e.py on each new version against its old one: PASS (needs the kit; made from HPKIT when it is
      not there as a zip).
  T6  the old verb is in none of the six programs (these five and FitCheck beta 1h), and each of the three help pages
      says "none of their code".
  T7  the monkey, 30 seeds on the old and the new version of each program: the same verdict, boxes and Quit summary, and
      every screen the same text for text, apart from the version string and the one credits page.
"""
import os, sys, io, json, glob, shutil, subprocess, tempfile, difflib, importlib.util, re, random, signal, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
R15 = os.path.join(HERE, 'round15'); R11 = os.path.join(HERE, 'round11')
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
spec = importlib.util.spec_from_file_location('m15', os.path.join(R15, 'make_wording_r15.py'))
m15 = importlib.util.module_from_spec(spec)
argv = sys.argv; sys.argv = ['x', os.devnull]; spec.loader.exec_module(m15); sys.argv = argv
res = []
CREDITS = {'RankLab': 'RankLab help 7/7', 'AnovaLab': 'AnovaLab help 9/9', 'ResampLab': 'ResampLab help 5/5'}
CALL = {'RankLab': 'RankLab()', 'AnovaLab': 'AnovaLab()', 'ResampLab': 'ResampLab()', 'ExhibitLab': 'ExhibitLab()', 'SurvLab': 'SurvLab()'}


def rec(tag, ok, msg):
    res.append(ok)
    print('%-4s %s  %s' % (tag, 'PASS' if ok else 'FAIL', msg), flush=True)


tmp = tempfile.mkdtemp(prefix='r15v_')
# T1
out = os.path.join(tmp, 'built'); os.makedirs(out)
subprocess.run([sys.executable, os.path.join(R15, 'make_wording_r15.py'), out], check=True, capture_output=True)
for name, (ov, nv, eds, note) in m15.EDITS.items():
    f = '%s_%s.txt' % (name, nv)
    a = open(os.path.join(out, f), 'rb').read(); b = open(os.path.join('programs', f), 'rb').read()
    rec('T1', a == b, '%s: the build makes programs/%s byte for byte' % (name, f))
# T2
for name, (ov, nv, eds, note) in m15.EDITS.items():
    old = m15.old_text(name, ov).split('\n')
    new = io.open(os.path.join('programs', '%s_%s.txt' % (name, nv)), encoding='utf-8').read().split('\n')
    pieces_old = [x.strip() for a, b in eds for x in a.split('\n') if x.strip()]
    pieces_new = [x.strip() for a, b in eds for x in b.split('\n') if x.strip()]
    bad = []
    for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if t == 'equal':
            continue
        for l in old[i1:i2]:
            if not (any(x in l for x in pieces_old) or l.lstrip().startswith('//') or m15.tag(ov) in l or ov in l):
                bad.append('- ' + l)
        for l in new[j1:j2]:
            if not (any(x in l for x in pieces_new) or l.lstrip().startswith('//') or m15.tag(nv) in l or nv in l):
                bad.append('+ ' + l)
    code_old = [l for l in old if not l.lstrip().startswith('//')]; code_new = [l for l in new if not l.lstrip().startswith('//')]
    ncode = sum(1 for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, code_old, code_new, autojunk=False).get_opcodes() if t != 'equal' for _ in range(max(i2 - i1, j2 - j1)))
    rec('T2', not bad, '%s: only the replacements, comments and version strings differ (%d lines that are not comments)%s'
        % (name, ncode, '' if not bad else ': ' + ' | '.join(x[:70] for x in bad[:3])))
# T3, T4: the help tools of Round 11, laid out as they expect (cwd with tools/; ../helpdump_r11.py; ../tools11)
w = os.path.join(tmp, 'w'); os.makedirs(w)
shutil.copytree('tools', os.path.join(w, 'tools'))
for f in ('helpdump_r11.py', 'helpcheck_r11.py', 'glyph_widths_vc.json'):
    shutil.copy(os.path.join(R11, f), tmp)
shutil.copytree(os.path.join(R11, 'tools11'), os.path.join(tmp, 'tools11'))
olddir = os.path.join(tmp, 'old'); os.makedirs(olddir)
for name, (ov, nv, eds, note) in m15.EDITS.items():
    io.open(os.path.join(olddir, '%s_%s.txt' % (name, ov)), 'w', encoding='utf-8', newline='').write(m15.old_text(name, ov))
newfiles = [os.path.join(REPO, 'programs', '%s_%s.txt' % (n, e[1])) for n, e in m15.EDITS.items()]
env = dict(os.environ)
subprocess.run([sys.executable, '../helpdump_r11.py', '../dump_new.json'] + newfiles, cwd=w, env=env, capture_output=True)
subprocess.run([sys.executable, '../helpdump_r11.py', '../dump_old.json'] + sorted(glob.glob(olddir + '/*.txt')), cwd=w, env=env,
               capture_output=True)
DN = json.load(open(os.path.join(tmp, 'dump_new.json'), encoding='utf-8'))
DO = json.load(open(os.path.join(tmp, 'dump_old.json'), encoding='utf-8'))
SAVEDP = os.path.join(R15, 'helppages_r15.json')
if '--save' in sys.argv:
    full = json.load(open(SAVEDP, encoding='utf-8')) if os.path.exists(SAVEDP) else {}
    full.update({k: DN[k] for k in m15.EDITS})
    json.dump(full, open(SAVEDP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
SAVED = json.load(open(SAVEDP, encoding='utf-8'))
def flat(pg): return ' '.join(pg if isinstance(pg, list) else [pg])
for name, (ov, nv, eds, note) in m15.EDITS.items():
    rec('T3', DN.get(name) == SAVED.get(name), '%s: %d help screens, as helppages_r15.json holds them' % (name, len(DN.get(name, []))))
    changed = [k for k, (x, y) in enumerate(zip(DO.get(name, []), DN.get(name, []))) if x != y]
    want = [k for k, pg in enumerate(DN.get(name, [])) if name in CREDITS and CREDITS[name] in flat(pg)]
    rec('T3', len(DO.get(name, [])) == len(DN.get(name, [])) and changed == want and (name not in CREDITS or len(want) == 1),
        '%s: screens changed against the old version: %s' % (name, ', '.join(str(k + 1) for k in changed) or 'none'))
subprocess.run([sys.executable, '../helpcheck_r11.py'] + newfiles, cwd=w, env=env, capture_output=True)
HC = json.load(open(os.path.join(tmp, 'helpcheck_r11.json'), encoding='utf-8'))
for name in m15.EDITS:
    pr = HC.get(name, {}).get('problems', ['not checked'])
    rec('T4', not pr, '%s: %s screens laid out, %s' % (name, HC.get(name, {}).get('screens', '?'), 'no reports' if not pr else '; '.join(pr)))
# T5
kit = [p for p in (os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit.zip'),) if os.path.exists(p)]
if not kit and os.environ.get('HPKIT'):
    os.makedirs(os.path.join(w, 'Community_Library', 'github'))
    base = os.path.dirname(os.environ['HPKIT'].rstrip('/'))
    shutil.make_archive(os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit'), 'zip', base,
                        os.path.basename(os.environ['HPKIT'].rstrip('/')))
    kit = [1]
if kit:
    for name, (ov, nv, eds, note) in m15.EDITS.items():
        r = subprocess.run([sys.executable, 'ppl_gate_v1e.py', os.path.join(REPO, 'programs', '%s_%s.txt' % (name, nv)),
                            os.path.join(olddir, '%s_%s.txt' % (name, ov))], cwd=os.path.join(w, 'tools'), capture_output=True,
                           text=True)
        rec('T5', 'RESULT: PASS' in r.stdout, '%s: the gate' % name)
else:
    print('T5   skipped: hp-prime-kit not found (set HPKIT)')
# T6
six = [os.path.join('programs', '%s_%s.txt' % (n, e[1])) for n, e in m15.EDITS.items()] + glob.glob(os.path.join('programs', 'FitCheck_beta1h.txt'))
hits = [(os.path.basename(p), len(re.findall('(?i)rework', io.open(p, encoding='utf-8').read()))) for p in six]
rec('T6', len(six) == 6 and all(n == 0 for _, n in hits), 'the old verb is in none of the six programs: %s' % ', '.join('%s %d' % h for h in hits))
for name in CREDITS:
    pg = next(flat(pg) for pg in DN[name] if CREDITS[name] in flat(pg))
    rec('T6', 'none of their code' in re.sub(r'\s+', ' ', pg), '%s: its credits page says "none of their code"' % name)
# T7
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
sys.argv = ['monkey_v1b.py']
import monkey_v1b as MK  # noqa: E402
sys.argv = argv


def one(path, call, seed, vmap, skipt):
    rng = random.Random(seed)
    app, kind = MK.random_lists(rng)
    hh = MK.Monkey(path, rng, app, 150)
    for q in range(10): hh.globals_.setdefault('M%d' % q, MK.R.interp.Matrix([[0.0]]))
    m1, mk = MK.random_matrix(seed)
    if m1 is not None: hh.globals_['M1'] = m1
    verdict = 'OK'
    signal.signal(signal.SIGALRM, MK._alarm); signal.alarm(60)
    try: hh.execute(call)
    except MK.TimeUp: verdict = 'FREEZE'
    except Exception as e: verdict = 'END ' + type(e).__name__
    finally: signal.alarm(0)
    def nv(t):
        for a, b in vmap: t = t.replace(a, b)
        return t
    scr = [tuple(nv(t.text) for t in s.texts) for s in hh.screens]
    sk = [bool(skipt) and any(skipt in t for t in s) for s in scr]
    return verdict, [('<credits page>',) if k else s for s, k in zip(scr, sk)], [nv(' '.join(m.lines)) for m in hh.msgboxes], nv(str(hh.result)), sum(sk)


for name, (ov, nv_, eds, note) in m15.EDITS.items():
    oldp = os.path.join(olddir, '%s_%s.txt' % (name, ov)); newp = os.path.join(REPO, 'programs', '%s_%s.txt' % (name, nv_))
    vmap = [(m15.tag(nv_), m15.tag(ov)), (nv_, ov), ('15 Nov 2026', '9 Nov 2026')]
    diffs = []; nscr = 0; nsk = 0; verd = {}
    for sd in range(1500, 1530):
        a = one(oldp, CALL[name], sd, [('15 Nov 2026', '9 Nov 2026')], CREDITS.get(name)); b = one(newp, CALL[name], sd, vmap, CREDITS.get(name))
        nscr += len(b[1]); nsk += b[4]; verd[b[0]] = verd.get(b[0], 0) + 1
        if a[:4] != b[:4]:
            k = next((i for i, (x, y) in enumerate(zip(a[1], b[1])) if x != y), None)
            diffs.append((sd, a[0], b[0], a[2] == b[2], a[3] == b[3], len(a[1]), len(b[1]), k, (a[1][k][:2], b[1][k][:2]) if k is not None else None))
    rec('T7', not diffs and nscr > 100, '%s: 30 seeds, %d screens the same text for text%s (%s)%s'
        % (name, nscr, (' but the %d showings of the credits page' % nsk) if name in CREDITS else '', ', '.join('%s %d' % kv for kv in sorted(verd.items())), '' if not diffs else ': ' + str(diffs[:2])[:500]))
shutil.rmtree(tmp, ignore_errors=True)
print('\n%d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
