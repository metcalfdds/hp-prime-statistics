# -*- coding: utf-8 -*-
"""checks_r12.py -- Round 12's checks beyond the gate, the help dumps and the help layout check (run from r12/w):
  S  the harness smoke test: each new version loaded with idle_key=4 and its main routine called; no PPLError, and
     no more warnings than the version before;
  T  tools/text_overlap_v1.py --walk on the new and the old version: the same report;
  F  tools/fleet_names_v2.py over the fleet with the twelve new versions in place of the old ones.
Writes ../checks_r12.txt and prints one line per check."""
import os, sys, glob, subprocess, shutil, signal
sys.path.insert(0, 'tools'); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness

MAIN = {'PowerViz': 'POWERVIZ()', 'TTestLab': 'TTESTLAB()', 'DataLoad': 'DATALOAD()'}
NEW = sorted(glob.glob('../programs/*.txt'))
out = []


class TO(Exception):
    pass


def alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, alarm)


def smoke(f):
    name = os.path.basename(f).split('_')[0]
    try:
        signal.alarm(120)
        h = Harness(f, idle_key=4, on_unverified='warn')
        try:
            h.execute(MAIN.get(name, name + '()'))
            err = ''
        except TO:
            err = 'timeout'
        except Exception as e:
            err = type(e).__name__ + ': ' + str(e)[:80]
        signal.alarm(0)
        return len(h.warnings), err
    except Exception as e:
        signal.alarm(0)
        return -1, 'load: ' + str(e)[:80]


for f in NEW:
    name = os.path.basename(f).split('_')[0]
    old = glob.glob('../old/%s_*.txt' % name)[0]
    wn, en = smoke(f)
    wo, eo = smoke(old)
    ok = (en == eo == '' or en == eo) and wn <= wo
    out.append('S %-10s %s  warnings %d (old %d)%s' % (name, 'OK  ' if ok else 'FAIL', wn, wo, ('  ' + en) if en else ''))
    print(out[-1], flush=True)

for f in NEW:
    name = os.path.basename(f).split('_')[0]
    old = glob.glob('../old/%s_*.txt' % name)[0]
    rep = []
    for g in (f, old):
        r = subprocess.run([sys.executable, 'tools/text_overlap_v1.py', '--walk', g], capture_output=True, text=True, timeout=1500)
        lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
        rep.append([l.replace(os.path.basename(g), 'PROGRAM') for l in lines if not l.startswith(('screens', 'walked'))])
    same = rep[0] == rep[1]
    summ = [l for l in rep[0] if 'overlap' in l.lower() or 'straddl' in l.lower() or 'overrun' in l.lower() or 'firm' in l.lower()][-1:]
    out.append('T %-10s %s  %s' % (name, 'same as the old version' if same else 'DIFFERS', summ[0][:120] if summ else ''))
    print(out[-1], flush=True)
    if not same:
        open('../overlap_%s.txt' % name, 'w').write('NEW\n' + '\n'.join(rep[0]) + '\n\nOLD\n' + '\n'.join(rep[1]))

fleet = '../fleet'
shutil.rmtree(fleet, ignore_errors=True); os.makedirs(fleet)
newnames = {os.path.basename(f).split('_')[0] for f in NEW}
for g in glob.glob('/home/claude/hp-prime-statistics/programs/*.txt'):
    if os.path.basename(g).split('_')[0] not in newnames:
        shutil.copy(g, fleet)
for f in NEW:
    shutil.copy(f, fleet)
r = subprocess.run([sys.executable, 'tools/fleet_names_v2.py'] + sorted(glob.glob(fleet + '/*.txt')), capture_output=True, text=True)
fl = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
bad = [l for l in fl if any(k in l for k in ('COLLISION', 'UNTAGGED', 'MIXEDTAG', 'BUILTIN'))]
out.append('F fleet_names_v2 over %d programs: %s' % (len(glob.glob(fleet + '/*.txt')), 'clean' if not bad else '%d findings' % len(bad)))
out.append('  ' + (fl[-1] if fl else ''))
print('\n'.join(out[-2:]))
open('../checks_r12.txt', 'w').write('\n'.join(out) + '\n\n--- fleet_names_v2 output\n' + '\n'.join(fl) + '\n')
