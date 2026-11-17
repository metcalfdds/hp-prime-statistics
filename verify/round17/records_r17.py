# -*- coding: utf-8 -*-
"""records_r17.py -- Round 17's records beyond the verify script, for all sixteen new versions (the screen text in the
book's house form: AgreeLab beta 1i, AnovaLab beta 1j, CICatcher beta 2m, EpiStats v1.7m, ExhibitLab beta 1i, FitCheck
beta 1j, PowerViz v2.5t, RankLab beta 1k, ResampLab beta 1j, ScatterLab beta 2m, StudRange beta 15n, TDist3D beta 1b,
TTestLab beta 1l, TTestLabG beta 1i, TestChooser beta 2h, TrendTest beta 3n).  Round 16's script with this round's
versions, the walks two at a time, and one more record (W).  Run from the repository's root; needs hp-prime-kit
(HPKIT).  It writes, in verify/round17/:
  gates/<Name>_<version>.txt   tools/ppl_gate_v1e.py on each new version against its old one (git, BASE), with the fleet's
                               names counted over all of programs/;
  helppages_before_r17.json, helppages_r17.json   every help screen of the old and the new versions, as the harness draws
                               them (verify/round11/helpdump_r11.py);
  helpcheck_r17.json           every new help screen laid out at the glyph widths GlyphProbe_v1 measured
                               (verify/round11/helpcheck_r11.py): what is cut or overlaps, if anything;
  checks_r17.txt               S, the harness smoke test (the main routine with idle key Esc: no error, and no more
                               warnings than the old version); T, tools/text_overlap_v1.py --walk on the new and the old
                               version (the two summaries; where a text changed, the two reports name different texts);
                               W, tools/screen_text_v1.py over all of programs/ with the texts the walks of all 31
                               programs drew (every one is read, beside every quoted string); F, tools/fleet_names_v2.py
                               over programs/;
  overlap_<Name>.txt           the two walks' reports;
  drawn/<file stem>.texts.json the distinct texts that the walk of each of the 31 programs now in programs/ drew
                               (drawn_texts_r17.py).  The walks themselves, as text_overlap_v1 --json writes them, come
                               to 381 MB and are not kept: they are written to the folder named by R17_WALKS, or to
                               a temporary one.
"""
import os, sys, io, re, glob, json, shutil, signal, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); R11 = os.path.join(os.path.dirname(HERE), 'round11')
os.chdir(REPO); os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
BASE = '39bb935'
PAIRS = [('AgreeLab', 'beta1h', 'beta1i'), ('AnovaLab', 'beta1i', 'beta1j'), ('CICatcher', 'beta2l', 'beta2m'), ('EpiStats', 'v1.7l', 'v1.7m'),
         ('ExhibitLab', 'beta1h', 'beta1i'), ('FitCheck', 'beta1i', 'beta1j'), ('PowerViz', 'v2.5s', 'v2.5t'), ('RankLab', 'beta1j', 'beta1k'),
         ('ResampLab', 'beta1i', 'beta1j'), ('ScatterLab', 'beta2l', 'beta2m'), ('StudRange', 'beta15m', 'beta15n'), ('TDist3D', 'beta1a', 'beta1b'),
         ('TTestLab', 'beta1k', 'beta1l'), ('TTestLabG', 'beta1h', 'beta1i'), ('TestChooser', 'beta2g', 'beta2h'), ('TrendTest', 'beta3m', 'beta3n')]
tmp = tempfile.mkdtemp(prefix='r17rec_'); w = os.path.join(tmp, 'w'); os.makedirs(w); olddir = os.path.join(tmp, 'old'); os.makedirs(olddir)
shutil.copytree('tools', os.path.join(w, 'tools'))
for f in ('helpdump_r11.py', 'helpcheck_r11.py', 'glyph_widths_vc.json'): shutil.copy(os.path.join(R11, f), tmp)
shutil.copytree(os.path.join(R11, 'tools11'), os.path.join(tmp, 'tools11'))
os.makedirs(os.path.join(w, 'Community_Library', 'github'))
base = os.path.dirname(os.environ['HPKIT'].rstrip('/'))
shutil.make_archive(os.path.join(w, 'Community_Library', 'github', 'JordiRigau__hp-prime-kit'), 'zip', base, os.path.basename(os.environ['HPKIT'].rstrip('/')))
new, old = {}, {}
for n, ov, nv in PAIRS:
    new[n] = os.path.join(REPO, 'programs', '%s_%s.txt' % (n, nv)); old[n] = os.path.join(olddir, '%s_%s.txt' % (n, ov))
    open(old[n], 'wb').write(subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (BASE, n, ov)], check=True, capture_output=True).stdout)
# gates
os.makedirs(os.path.join(HERE, 'gates'), exist_ok=True)
for n, ov, nv in PAIRS:
    r = subprocess.run([sys.executable, 'ppl_gate_v1e.py', new[n], old[n]], cwd=os.path.join(w, 'tools'), capture_output=True, text=True)
    io.open(os.path.join(HERE, 'gates', '%s_%s.txt' % (n, nv)), 'w', encoding='utf-8').write(r.stdout.replace(tmp, '.'))
    print('gate %-10s %s' % (n, 'PASS' if 'RESULT: PASS' in r.stdout else 'FAIL'), flush=True)
# help dumps and the help layout check
env = dict(os.environ)
subprocess.run([sys.executable, '../helpdump_r11.py', '../dump_new.json'] + [new[n] for n, _, _ in PAIRS], cwd=w, env=env, capture_output=True)
subprocess.run([sys.executable, '../helpdump_r11.py', '../dump_old.json'] + [old[n] for n, _, _ in PAIRS], cwd=w, env=env, capture_output=True)
DN = json.load(open(os.path.join(tmp, 'dump_new.json'), encoding='utf-8')); DO = json.load(open(os.path.join(tmp, 'dump_old.json'), encoding='utf-8'))
json.dump(DN, open(os.path.join(HERE, 'helppages_r17.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(DO, open(os.path.join(HERE, 'helppages_before_r17.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
subprocess.run([sys.executable, '../helpcheck_r11.py'] + [new[n] for n, _, _ in PAIRS], cwd=w, env=env, capture_output=True)
HC = json.load(open(os.path.join(tmp, 'helpcheck_r11.json'), encoding='utf-8'))
json.dump(HC, open(os.path.join(HERE, 'helpcheck_r17.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for n, _, _ in PAIRS:
    ch = [k + 1 for k, (a, b) in enumerate(zip(DO.get(n, []), DN.get(n, []))) if a != b]
    print('help %-10s %d screens (old %d); changed: %s; layout: %s' % (n, len(DN.get(n, [])), len(DO.get(n, [])), ch or 'none', HC.get(n, {}).get('problems') or 'no reports'), flush=True)
# S, T, F
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness  # noqa: E402
out = []
MAIN = {'PowerViz': 'POWERVIZ()', 'TTestLab': 'TTESTLAB()', 'TTestLabG': 'TTESTLABG()'}


class TO(Exception):
    pass


def alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, alarm)


def smoke(f, n):
    try:
        signal.alarm(120)
        h = Harness(f, idle_key=4, on_unverified='warn')
        try: h.execute(MAIN.get(n, n + '()')); err = ''
        except TO: err = 'timeout'
        except Exception as e: err = type(e).__name__ + ': ' + str(e)[:80]
        signal.alarm(0)
        return len(h.warnings), err
    except Exception as e:
        signal.alarm(0)
        return -1, 'load: ' + str(e)[:80]


for n, ov, nv in PAIRS:
    wn, en = smoke(new[n], n); wo, eo = smoke(old[n], n)
    ok = (en == eo == '' or en == eo) and wn <= wo
    out.append('S %-10s %s  warnings %d (old %d)%s' % (n, 'OK  ' if ok else 'FAIL', wn, wo, ('  ' + en) if en else '')); print(out[-1], flush=True)
WALKS = os.environ.get('R17_WALKS') or os.path.join(tmp, 'walks'); os.makedirs(WALKS, exist_ok=True); oldwalks = os.path.join(tmp, 'oldwalks'); os.makedirs(oldwalks)
from concurrent.futures import ThreadPoolExecutor  # noqa: E402


def walk1(job):
    g, jdir = job
    stem = os.path.basename(g)[:-4]
    r = subprocess.run([sys.executable, 'tools/text_overlap_v1.py', '--walk', g, '--json', os.path.join(jdir, stem + '.json')],
                       capture_output=True, text=True, timeout=3000, cwd=REPO)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    # the walk's own line ends with the seconds it took, which differ from run to run and say nothing about the program
    return g, [re.sub(r", 'seconds': [0-9.]+", '', l.replace(os.path.basename(g), 'PROGRAM')) for l in lines if not l.startswith(('screens', 'walked'))]


jobs = [(g, WALKS) for g in sorted(glob.glob('programs/*.txt'))] + [(old[n], oldwalks) for n, _, _ in PAIRS]
with ThreadPoolExecutor(2) as ex:
    REP = dict(ex.map(walk1, jobs))
for n, ov, nv in PAIRS:
    rep = [REP[os.path.join('programs', '%s_%s.txt' % (n, nv))], REP[old[n]]]
    same = rep[0] == rep[1]
    summ = [l for l in rep[0] if 'overlap' in l.lower() or 'straddl' in l.lower() or 'overrun' in l.lower() or 'firm' in l.lower()][-1:]
    summo = [l for l in rep[1] if 'overlap' in l.lower() or 'straddl' in l.lower() or 'overrun' in l.lower() or 'firm' in l.lower()][-1:]
    out.append('T %-10s %s  %s%s' % (n, 'same report as the old version' if same else 'not the old version\'s report (see overlap_%s.txt)' % n,
                                     re.sub(r'\s+', ' ', summ[0][:160]) if summ else '',
                                     '' if same else '   OLD: ' + (re.sub(r'\s+', ' ', summo[0][:160]) if summo else ''))); print(out[-1], flush=True)
    io.open(os.path.join(HERE, 'overlap_%s.txt' % n), 'w', encoding='utf-8').write('NEW\n' + '\n'.join(rep[0]) + '\n\nOLD\n' + '\n'.join(rep[1]) + '\n')
r = subprocess.run([sys.executable, os.path.join(HERE, 'drawn_texts_r17.py'), WALKS], capture_output=True, text=True, cwd=REPO)
assert r.returncode == 0, r.stderr[-400:]
r = subprocess.run([sys.executable, 'tools/screen_text_v1.py', '--walk', os.path.join(HERE, 'drawn')] + sorted(glob.glob('programs/*.txt')), capture_output=True, text=True, cwd=REPO)
st = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
out.append('W screen_text_v1 with the walks: exit %d; %s' % (r.returncode, st[-1] if st else '')); print(out[-1], flush=True)
out.extend('  ' + l for l in st[:-1])
r = subprocess.run([sys.executable, 'tools/fleet_names_v2.py'] + sorted(glob.glob('programs/*.txt')), capture_output=True, text=True, cwd=REPO)
fl = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
bad = [l for l in fl if any(k in l for k in ('COLLISION', 'UNTAGGED', 'MIXEDTAG', 'BUILTIN'))]
out.append('F fleet_names_v2 over %d programs: %s' % (len(glob.glob('programs/*.txt')), 'clean' if not bad else '%d findings' % len(bad)))
out.append('  ' + (fl[-1] if fl else '')); print('\n'.join(out[-2:]))
io.open(os.path.join(HERE, 'checks_r17.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n\n--- fleet_names_v2 output\n' + '\n'.join(fl) + '\n')
shutil.rmtree(tmp, ignore_errors=True)
