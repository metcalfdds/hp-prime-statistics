#!/usr/bin/env python3
"""verify_round16_wording_v1.py -- checks the wording part of Round 16 (15 Nov 2026): what four programs say about the
programs they stand beside: StatDist v2.7n, AgreeLab beta 1h, RiskLab beta 1h and BurrLab beta 1r.  Only comments
changed, and the version each program shows, so the checks are of the text and of everything else staying put.
Made from verify_round15_wording_v1.py.

Runs from the repository alone (Lessons Learned s14 rule 18): tools/, programs/ and verify/ by relative path, the old
versions from git (the commit before Round 16, make_wording_r16.BASE).  Needs hp-prime-kit (HPKIT) for the harness.

  T1  verify/round16/make_wording_r16.py, run again from the old versions, makes each new file byte for byte.
  T2  each new file differs from its old one only in comment lines and in lines whose only change is the version string,
      old to new (with its date): no other line that is not a comment differs.
  T3  the help pages, dumped by the harness (verify/round11/helpdump_r11.py) from the old and the new version, are the
      same screen for screen once the version string is put back.
  T5  tools/ppl_gate_v1e.py on each new version against its old one: PASS (needs the kit; made from HPKIT when it is
      not there as a zip).
  T6  no line of any of the 31 programs begins "// Replaces / reworks", and "framework after" is in none of them; each
      of the four says what was done ("written new", "None of his code", "Takes the place of Burr3", "Follows no TI").
  T7  the monkey, 30 seeds on the old and the new version of each program: the same verdict, boxes and closing line, and
      every screen the same text for text, apart from the version string.
"""
import os, sys, io, json, glob, shutil, subprocess, tempfile, difflib, importlib.util, re, random, signal, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
R16 = os.path.join(HERE, 'round16'); R11 = os.path.join(HERE, 'round11')
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
spec = importlib.util.spec_from_file_location('m16', os.path.join(R16, 'make_wording_r16.py'))
m16 = importlib.util.module_from_spec(spec)
argv = sys.argv; sys.argv = ['x', os.devnull]; spec.loader.exec_module(m16); sys.argv = argv
res = []
CALL = {'AgreeLab': 'AgreeLab()', 'RiskLab': 'RiskLab()', 'BurrLab': 'BurrLab()', 'StatDist': 'StatDist()'}
OLDDATE = {'AgreeLab': '9 Nov 2026', 'RiskLab': '13 Nov 2026', 'BurrLab': '9 Nov 2026', 'StatDist': '13 Nov 2026'}
SAYS = {'AgreeLab': ['// Follows no TI-83/84 program:', 'AgreeLab was written new in PPL from the papers listed'],
        'RiskLab': ['// No Triola program does this.  The nearest TI-83/84 program, LOGIT', 'RiskLab was written new in PPL, and none of LOGIT\'s code'],
        'BurrLab': ['// Takes the place of Burr3 v2.4c, the fleet\'s own earlier program, and', 'It follows no TI program.'],
        'StatDist': ['// Does on the Prime, with menus and plots, what Salvo Micciche\'s', 'None of his code is in StatDist']}


def rec(tag, ok, msg):
    res.append(ok)
    print('%-4s %s  %s' % (tag, 'PASS' if ok else 'FAIL', msg), flush=True)


tmp = tempfile.mkdtemp(prefix='r16v_')
# T1
out = os.path.join(tmp, 'built'); os.makedirs(out)
subprocess.run([sys.executable, os.path.join(R16, 'make_wording_r16.py'), out], check=True, capture_output=True)
for name, (ov, nv, eds, note) in m16.EDITS.items():
    f = '%s_%s.txt' % (name, nv)
    a = open(os.path.join(out, f), 'rb').read(); b = open(os.path.join('programs', f), 'rb').read()
    rec('T1', a == b, '%s: the build makes programs/%s byte for byte' % (name, f))
# T2
for name, (ov, nv, eds, note) in m16.EDITS.items():
    old = m16.old_text(name, ov).split('\n')
    new = io.open(os.path.join('programs', '%s_%s.txt' % (name, nv)), encoding='utf-8').read().split('\n')
    code_old = [l for l in old if not l.lstrip().startswith('//')]; code_new = [l for l in new if not l.lstrip().startswith('//')]
    back = [l.replace(m16.tag(nv), m16.tag(ov)).replace(nv, ov).replace('15 Nov 2026', OLDDATE[name]) for l in code_new]
    differ = [(a, b) for a, b in zip(code_old, code_new) if a != b]
    rec('T2', len(code_old) == len(code_new) and back == code_old and all(m16.tag(nv) in b or nv in b for a, b in differ),
        '%s: %d lines that are not comments, the same in both versions but for %d with the version string%s'
        % (name, len(code_new), len(differ), (': ' + ' | '.join(b.strip()[:60] for a, b in differ)) if differ else ''))
# T3: the help pages
w = os.path.join(tmp, 'w'); os.makedirs(w)
shutil.copytree('tools', os.path.join(w, 'tools'))
for f in ('helpdump_r11.py', 'helpcheck_r11.py', 'glyph_widths_vc.json'):
    shutil.copy(os.path.join(R11, f), tmp)
shutil.copytree(os.path.join(R11, 'tools11'), os.path.join(tmp, 'tools11'))
olddir = os.path.join(tmp, 'old'); os.makedirs(olddir)
for name, (ov, nv, eds, note) in m16.EDITS.items():
    io.open(os.path.join(olddir, '%s_%s.txt' % (name, ov)), 'w', encoding='utf-8', newline='').write(m16.old_text(name, ov))
newfiles = [os.path.join(REPO, 'programs', '%s_%s.txt' % (n, e[1])) for n, e in m16.EDITS.items()]
env = dict(os.environ)
subprocess.run([sys.executable, '../helpdump_r11.py', '../dump_new.json'] + newfiles, cwd=w, env=env, capture_output=True)
subprocess.run([sys.executable, '../helpdump_r11.py', '../dump_old.json'] + sorted(glob.glob(olddir + '/*.txt')), cwd=w, env=env,
               capture_output=True)
DN = json.load(open(os.path.join(tmp, 'dump_new.json'), encoding='utf-8'))
DO = json.load(open(os.path.join(tmp, 'dump_old.json'), encoding='utf-8'))
for name, (ov, nv, eds, note) in m16.EDITS.items():
    a = json.dumps(DO.get(name), ensure_ascii=False)
    b = json.dumps(DN.get(name), ensure_ascii=False).replace(m16.tag(nv), m16.tag(ov)).replace(nv, ov).replace('15 Nov 2026', OLDDATE[name])
    rec('T3', a == b and len(DN.get(name, [])) > 0, '%s: %d help screens, the same as the old version\'s' % (name, len(DN.get(name, []))))
# T5
kit = [p for p in (os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit.zip'),) if os.path.exists(p)]
if not kit and os.environ.get('HPKIT'):
    os.makedirs(os.path.join(w, 'Community_Library', 'github'))
    base = os.path.dirname(os.environ['HPKIT'].rstrip('/'))
    shutil.make_archive(os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit'), 'zip', base,
                        os.path.basename(os.environ['HPKIT'].rstrip('/')))
    kit = [1]
if kit:
    for name, (ov, nv, eds, note) in m16.EDITS.items():
        r = subprocess.run([sys.executable, 'ppl_gate_v1e.py', os.path.join(REPO, 'programs', '%s_%s.txt' % (name, nv)),
                            os.path.join(olddir, '%s_%s.txt' % (name, ov))], cwd=os.path.join(w, 'tools'), capture_output=True,
                           text=True)
        rec('T5', 'RESULT: PASS' in r.stdout, '%s: the gate' % name)
        if '--save' in sys.argv:
            os.makedirs(os.path.join(R16, 'gates'), exist_ok=True)
            io.open(os.path.join(R16, 'gates', '%s_%s.txt' % (name, nv)), 'w', encoding='utf-8').write(r.stdout)
else:
    print('T5   skipped: hp-prime-kit not found (set HPKIT)')
# T6
allp = sorted(glob.glob(os.path.join('programs', '*.txt')))
lab = [os.path.basename(p) for p in allp if any(re.match(r'^// Replaces / reworks', l) or re.search(r'2026 \(framework after', l)
                                                 for l in io.open(p, encoding='utf-8').read().split('\n'))]
rec('T6', len(allp) == 31 and not lab, 'no line of the %d programs begins "// Replaces / reworks" and no author line says "(framework after"%s' % (len(allp), '' if not lab else ': ' + ', '.join(lab)))
for name, (ov, nv, eds, note) in m16.EDITS.items():
    t = io.open(os.path.join('programs', '%s_%s.txt' % (name, nv)), encoding='utf-8').read()
    rec('T6', all(x in t for x in SAYS[name]), '%s: its header says "%s ..." and "... %s"' % (name, SAYS[name][0][3:], SAYS[name][1]))
# T7
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
import prime_facts_v1  # noqa: E402
prime_facts_v1.apply()
sys.argv = ['monkey_v1b.py']
import monkey_v1b as MK  # noqa: E402
sys.argv = argv


def one(path, call, seed, vmap):
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
    return verdict, scr, [nv(' '.join(m.lines)) for m in hh.msgboxes], nv(str(hh.result))


for name, (ov, nv_, eds, note) in m16.EDITS.items():
    oldp = os.path.join(olddir, '%s_%s.txt' % (name, ov)); newp = os.path.join(REPO, 'programs', '%s_%s.txt' % (name, nv_))
    vmap = [(m16.tag(nv_), m16.tag(ov)), (nv_, ov), ('15 Nov 2026', OLDDATE[name])]
    diffs = []; nscr = 0; verd = {}
    for sd in range(1600, 1630):
        a = one(oldp, CALL[name], sd, []); b = one(newp, CALL[name], sd, vmap)
        nscr += len(b[1]); verd[b[0]] = verd.get(b[0], 0) + 1
        if a != b:
            k = next((i for i, (x, y) in enumerate(zip(a[1], b[1])) if x != y), None)
            diffs.append((sd, a[0], b[0], a[2] == b[2], a[3] == b[3], len(a[1]), len(b[1]), k, (a[1][k][:2], b[1][k][:2]) if k is not None else None))
    rec('T7', not diffs and nscr > 100, '%s: 30 seeds, %d screens the same text for text (%s)%s'
        % (name, nscr, ', '.join('%s %d' % kv for kv in sorted(verd.items())), '' if not diffs else ': ' + str(diffs[:2])[:500]))
shutil.rmtree(tmp, ignore_errors=True)
print('\n%d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
