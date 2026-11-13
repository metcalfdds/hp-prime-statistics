#!/usr/bin/env python3
"""verify_round12_v1.py -- checks Round 12 (13 Nov 2026): help-page fixes found in the book's pre-submission read, in
twelve programs: AnovaLab beta 1g, BayesTree beta 8k, CICatcher beta 2j, DataLoad beta 1g, EpiStats v1.7l, FitCheck
beta 1g, PowerViz v2.5s, RankLab beta 1h, RiskLab beta 1g, SampDist v2.3k, StatDist v2.7m and TTestLab beta 1j.

Runs from the repository alone (Lessons Learned §14 rule 18): tools/, programs/ and verify/ by relative path, the old
versions from git (the commit before Round 12, make_round12.BASE).  Needs hp-prime-kit (HPKIT) for the harness.

  T1  verify/round12/make_round12.py, run again from the old versions, makes each new file byte for byte.
  T2  each new file differs from its old one only in (a) the lines of the build's own replacements, (b) comment lines
      (the header and the history note), and (c) lines whose only change is the version string, old to new.
  T3  the help pages, dumped again by the harness (verify/round11/helpdump_r11.py), are verify/round12/helppages_r12.json;
      and against the old versions' dump, the only screens that changed are the ones the replacements touch.
  T4  every help screen laid out at the glyph widths GlyphProbe_v1 measured (verify/round11/helpcheck_r11.py): no line
      past its width argument or the screen's edge and no two texts overlapping; StatDist's known report only (the
      harness cannot call st_ABHelp without its argument).
  T5  tools/ppl_gate_v1e.py on each new version against its old one: PASS (needs the kit as a zip beside tools/;
      skipped with a note when it is not there).
  X1  RankLab, the fault the monkey found: with the jury preset loaded (3 groups) and only D1 filled, Your data >
      Groups is refused; beta 1g then held 3 groups but 1 name, and Mann-Whitney stopped with "index 2 out of range
      in cgN"; beta 1h keeps the jury's 3 groups and names, and Mann-Whitney picks two of them.
"""
import os, sys, io, json, glob, shutil, subprocess, tempfile, difflib, importlib.util, re

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
R12 = os.path.join(HERE, 'round12'); R11 = os.path.join(HERE, 'round11')
os.chdir(REPO)
spec = importlib.util.spec_from_file_location('m12', os.path.join(R12, 'make_round12.py'))
m12 = importlib.util.module_from_spec(spec)
argv = sys.argv; sys.argv = ['x', os.devnull]; spec.loader.exec_module(m12); sys.argv = argv
res = []


def rec(tag, ok, msg):
    res.append(ok)
    print('%-4s %s  %s' % (tag, 'PASS' if ok else 'FAIL', msg), flush=True)


tmp = tempfile.mkdtemp(prefix='r12v_')
# T1
out = os.path.join(tmp, 'built'); os.makedirs(out)
subprocess.run([sys.executable, os.path.join(R12, 'make_round12.py'), out], check=True, capture_output=True)
for name, (ov, nv, eds, note) in m12.EDITS.items():
    f = '%s_%s.txt' % (name, nv)
    a = open(os.path.join(out, f), 'rb').read(); b = open(os.path.join('programs', f), 'rb').read()
    rec('T1', a == b, '%s: the build makes programs/%s byte for byte' % (name, f))
# T2
for name, (ov, nv, eds, note) in m12.EDITS.items():
    old = m12.old_text(name, ov).split('\n')
    new = io.open(os.path.join('programs', '%s_%s.txt' % (name, nv)), encoding='utf-8').read().split('\n')
    # a changed line is one of the build's own: it holds a piece (a line) of a replacement's old or new text
    pieces_old = [x.strip() for a, b in eds for x in a.split('\n') if x.strip()]
    pieces_new = [x.strip() for a, b in eds for x in b.split('\n') if x.strip()]
    bad = []
    for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if t == 'equal':
            continue
        for l in old[i1:i2]:
            if not (any(x in l for x in pieces_old) or l.lstrip().startswith('//') or m12.tag(ov) in l or ov in l):
                bad.append('- ' + l)
        for l in new[j1:j2]:
            if not (any(x in l for x in pieces_new) or l.lstrip().startswith('//') or m12.tag(nv) in l or nv in l):
                bad.append('+ ' + l)
    rec('T2', not bad, '%s: only the replacements, comments and version strings differ%s'
        % (name, '' if not bad else ': ' + ' | '.join(x[:70] for x in bad[:3])))
# T3, T4: the help tools of Round 11, laid out as they expect (cwd with tools/; ../helpdump_r11.py; ../tools11)
w = os.path.join(tmp, 'w'); os.makedirs(w)
shutil.copytree('tools', os.path.join(w, 'tools'))
for f in ('helpdump_r11.py', 'helpcheck_r11.py', 'glyph_widths_vc.json'):
    shutil.copy(os.path.join(R11, f), tmp)
shutil.copytree(os.path.join(R11, 'tools11'), os.path.join(tmp, 'tools11'))
olddir = os.path.join(tmp, 'old'); os.makedirs(olddir)
for name, (ov, nv, eds, note) in m12.EDITS.items():
    io.open(os.path.join(olddir, '%s_%s.txt' % (name, ov)), 'w', encoding='utf-8', newline='').write(m12.old_text(name, ov))
newfiles = [os.path.join(REPO, 'programs', '%s_%s.txt' % (n, e[1])) for n, e in m12.EDITS.items()]
env = dict(os.environ)
subprocess.run([sys.executable, '../helpdump_r11.py', '../dump_new.json'] + newfiles, cwd=w, env=env, capture_output=True)
subprocess.run([sys.executable, '../helpdump_r11.py', '../dump_old.json'] + sorted(glob.glob(olddir + '/*.txt')), cwd=w, env=env,
               capture_output=True)
DN = json.load(open(os.path.join(tmp, 'dump_new.json'), encoding='utf-8'))
DO = json.load(open(os.path.join(tmp, 'dump_old.json'), encoding='utf-8'))
SAVED = json.load(open(os.path.join(R12, 'helppages_r12.json'), encoding='utf-8'))
for name, (ov, nv, eds, note) in m12.EDITS.items():
    rec('T3', DN.get(name) == SAVED.get(name), '%s: %d help screens, as helppages_r12.json holds them' % (name, len(DN.get(name, []))))
    words = set()
    CODE = {'TEXTOUT', 'CHAR', 'hBl', 'hBk', 'hMg', 'cblk', 'cnul', 'avBLUE', 'ttGRAY', 'ddBLK', 'Frame'}
    for a, b in eds:
        words |= set(re.findall(r'[A-Za-z]{4,}', b)) - CODE
    changed = [k for k, (x, y) in enumerate(zip(DO.get(name, []), DN.get(name, []))) if x != y]
    unexpected = [k + 1 for k in changed if not any(wd in ' '.join(DN[name][k] if isinstance(DN[name][k], list) else [DN[name][k]])
                                                  for wd in words)]
    rec('T3', len(DO.get(name, [])) == len(DN.get(name, [])) and not unexpected,
        '%s: screens changed against the old version: %s' % (name, ', '.join(str(k + 1) for k in changed) or 'none (not a help page)'))
subprocess.run([sys.executable, '../helpcheck_r11.py'] + newfiles, cwd=w, env=env, capture_output=True)
HC = json.load(open(os.path.join(tmp, 'helpcheck_r11.json'), encoding='utf-8'))
for name in m12.EDITS:
    pr = HC.get(name, {}).get('problems', ['not checked'])
    known = [p for p in pr if 'st_ABHelp' in p]
    rec('T4', len(pr) == len(known), '%s: %s screens laid out, %s' % (name, HC.get(name, {}).get('screens', '?'),
                                                                     'no reports' if not pr else '; '.join(pr)))
# T5
kit = [p for p in (os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit.zip'),) if os.path.exists(p)]
if not kit and os.environ.get('HPKIT'):
    os.makedirs(os.path.join(w, 'Community_Library', 'github'))
    base = os.path.dirname(os.environ['HPKIT'].rstrip('/'))
    shutil.make_archive(os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit'), 'zip', base,
                        os.path.basename(os.environ['HPKIT'].rstrip('/')))
    kit = [1]
if kit:
    for name, (ov, nv, eds, note) in m12.EDITS.items():
        r = subprocess.run([sys.executable, 'ppl_gate_v1e.py', os.path.join(REPO, 'programs', '%s_%s.txt' % (name, nv)),
                            os.path.join(olddir, '%s_%s.txt' % (name, ov))], cwd=os.path.join(w, 'tools'), capture_output=True,
                           text=True)
        rec('T5', 'RESULT: PASS' in r.stdout, '%s: the gate' % name)
else:
    print('T5   skipped: hp-prime-kit not found (set HPKIT)')
# X1
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness


def rk_case(path):
    h = Harness(path, idle_key=4, app_data={'D1': [3.0, 1.0, 4.0, 1.0, 5.0]})
    h.execute('rk_LdJury()')
    h.choose(1)
    r = h.execute('rk_MyData()')
    k, n = h.globals_['rkGK'], len(h.globals_['rkGNm'])
    try:
        h.choose(1); h.choose(2); h.execute('rk_PickTwo()'); err = ''
    except Exception as e:
        err = str(e)
    return r, k, n, err


r, k, n, err = rk_case(os.path.join(olddir, 'RankLab_beta1g.txt'))
rec('X1', r == 0 and k == 3 and n == 1 and 'out of range' in err, 'RankLab beta 1g: the refused read leaves 3 groups and 1 name; Mann-Whitney: ' + err[:60])
r, k, n, err = rk_case(os.path.join(REPO, 'programs', 'RankLab_beta1h.txt'))
rec('X1', r == 0 and k == 3 and n == 3 and not err, 'RankLab beta 1h: the refused read changes nothing (3 groups, 3 names); Mann-Whitney picks two')
shutil.rmtree(tmp, ignore_errors=True)
print('\n%d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
