# -*- coding: utf-8 -*-
"""records_r16.py -- Round 16's records beyond the verify scripts, for all nine new versions (BiNorm3D beta 1g, CICatcher
beta 2l, FitCheck beta 1i, RankLab beta 1j, AnovaLab beta 1i, StatDist v2.7n, AgreeLab beta 1h, RiskLab beta 1h, BurrLab
beta 1r).  Round 15's script with this round's versions.  Run from the repository's root; needs hp-prime-kit (HPKIT).  It
writes, in verify/round16/:
  gates/<Name>_<version>.txt   tools/ppl_gate_v1e.py on each new version against its old one (git, BASE), with the fleet's
                               names counted over all of programs/;
  helppages_before_r16.json, helppages_r16.json   every help screen of the old and the new versions, as the harness draws
                               them (verify/round11/helpdump_r11.py);
  helpcheck_r16.json           every new help screen laid out at the glyph widths GlyphProbe_v1 measured
                               (verify/round11/helpcheck_r11.py): what is cut or overlaps, if anything;
  checks_r16.txt               S, the harness smoke test (the main routine with idle key Esc: no error, and no more
                               warnings than the old version); T, tools/text_overlap_v1.py --walk on the new and the old
                               version (the two summaries; a program with new pages walks more screens than its old
                               version, so its report is not expected to be the same); F, tools/fleet_names_v2.py over
                               programs/;
  overlap_<Name>.txt           the two walks' reports.
"""
import os, sys, io, re, glob, json, shutil, signal, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); R11 = os.path.join(os.path.dirname(HERE), 'round11')
os.chdir(REPO); os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
BASE = '4e8ff66'
PAIRS = [('BiNorm3D', 'beta1f', 'beta1g'), ('CICatcher', 'beta2k', 'beta2l'), ('FitCheck', 'beta1h', 'beta1i'), ('RankLab', 'beta1i', 'beta1j'),
         ('AnovaLab', 'beta1h', 'beta1i'), ('StatDist', 'v2.7m', 'v2.7n'), ('AgreeLab', 'beta1g', 'beta1h'), ('RiskLab', 'beta1g', 'beta1h'),
         ('BurrLab', 'beta1q', 'beta1r')]
tmp = tempfile.mkdtemp(prefix='r16rec_'); w = os.path.join(tmp, 'w'); os.makedirs(w); olddir = os.path.join(tmp, 'old'); os.makedirs(olddir)
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
json.dump(DN, open(os.path.join(HERE, 'helppages_r16.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(DO, open(os.path.join(HERE, 'helppages_before_r16.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
subprocess.run([sys.executable, '../helpcheck_r11.py'] + [new[n] for n, _, _ in PAIRS], cwd=w, env=env, capture_output=True)
HC = json.load(open(os.path.join(tmp, 'helpcheck_r11.json'), encoding='utf-8'))
json.dump(HC, open(os.path.join(HERE, 'helpcheck_r16.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for n, _, _ in PAIRS:
    ch = [k + 1 for k, (a, b) in enumerate(zip(DO.get(n, []), DN.get(n, []))) if a != b]
    print('help %-10s %d screens (old %d); changed: %s; layout: %s' % (n, len(DN.get(n, [])), len(DO.get(n, [])), ch or 'none', HC.get(n, {}).get('problems') or 'no reports'), flush=True)
# S, T, F
sys.path.insert(0, os.path.join(REPO, 'tools')); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness  # noqa: E402
out = []


class TO(Exception):
    pass


def alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, alarm)


def smoke(f, n):
    try:
        signal.alarm(120)
        h = Harness(f, idle_key=4, on_unverified='warn')
        try: h.execute(n + '()'); err = ''
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
for n, ov, nv in PAIRS:
    rep = []
    for g in (new[n], old[n]):
        r = subprocess.run([sys.executable, 'tools/text_overlap_v1.py', '--walk', g], capture_output=True, text=True, timeout=3000, cwd=REPO)
        lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
        # the walk's own line ends with the seconds it took, which differ from run to run and say nothing about the
        # program: they are taken out before the two reports are compared (the first run of this script did not, and
        # called six identical reports different)
        rep.append([re.sub(r", 'seconds': [0-9.]+", '', l.replace(os.path.basename(g), 'PROGRAM')) for l in lines if not l.startswith(('screens', 'walked'))])
    same = rep[0] == rep[1]
    summ = [l for l in rep[0] if 'overlap' in l.lower() or 'straddl' in l.lower() or 'overrun' in l.lower() or 'firm' in l.lower()][-1:]
    summo = [l for l in rep[1] if 'overlap' in l.lower() or 'straddl' in l.lower() or 'overrun' in l.lower() or 'firm' in l.lower()][-1:]
    out.append('T %-10s %s  %s%s' % (n, 'same report as the old version' if same else 'not the old version\'s report (see overlap_%s.txt)' % n,
                                     re.sub(r'\s+', ' ', summ[0][:160]) if summ else '',
                                     '' if same else '   OLD: ' + (re.sub(r'\s+', ' ', summo[0][:160]) if summo else ''))); print(out[-1], flush=True)
    io.open(os.path.join(HERE, 'overlap_%s.txt' % n), 'w', encoding='utf-8').write('NEW\n' + '\n'.join(rep[0]) + '\n\nOLD\n' + '\n'.join(rep[1]) + '\n')
r = subprocess.run([sys.executable, 'tools/fleet_names_v2.py'] + sorted(glob.glob('programs/*.txt')), capture_output=True, text=True, cwd=REPO)
fl = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
bad = [l for l in fl if any(k in l for k in ('COLLISION', 'UNTAGGED', 'MIXEDTAG', 'BUILTIN'))]
out.append('F fleet_names_v2 over %d programs: %s' % (len(glob.glob('programs/*.txt')), 'clean' if not bad else '%d findings' % len(bad)))
out.append('  ' + (fl[-1] if fl else '')); print('\n'.join(out[-2:]))
io.open(os.path.join(HERE, 'checks_r16.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n\n--- fleet_names_v2 output\n' + '\n'.join(fl) + '\n')
shutil.rmtree(tmp, ignore_errors=True)
