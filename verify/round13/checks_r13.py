# -*- coding: utf-8 -*-
"""checks_r13.py -- Round 13's checks beyond the gate, the verify script and the help layout check (run from r13/w,
with a copy of tools/ beside it, ChiTable beta 3m in ../programs and beta 3l in ../old):
  S  the harness smoke test: the new version loaded with idle_key=4 and ChiTable() called; no PPLError, and no more
     warnings than the version before;
  T  tools/text_overlap_v1.py --walk on the new and the old version: the same report;
  L  tools/label_fit_v1.py on the JSON of both walks (no new finding) and of the verify script's own run;
  F  tools/fleet_names_v2.py over the fleet with beta 3m in place of beta 3l.
Writes ../checks_r13.txt and prints one line per check.  Round 12's checks_r12.py, cut to one program."""
import os, re, sys, glob, subprocess, shutil, signal
sys.path.insert(0, 'tools'); sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness

NEW = '../programs/ChiTable_beta3m.txt'
OLD = '../old/ChiTable_beta3l.txt'
out = []


class TO(Exception):
    pass


def alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, alarm)


def smoke(f):
    try:
        signal.alarm(120)
        h = Harness(f, idle_key=4, on_unverified='warn')
        try:
            h.execute('ChiTable()')
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


wn, en = smoke(NEW)
wo, eo = smoke(OLD)
ok = (en == eo == '' or en == eo) and wn <= wo
out.append('S ChiTable %s  warnings %d (old %d)%s' % ('OK  ' if ok else 'FAIL', wn, wo, ('  ' + en) if en else ''))
print(out[-1], flush=True)

rep = []
for g, j in ((NEW, '../walk_new.json'), (OLD, '../walk_old.json')):
    r = subprocess.run([sys.executable, 'tools/text_overlap_v1.py', '--walk', g, '--json', j], capture_output=True, text=True,
                       timeout=1500)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    # the walk's own line carries its timing ('seconds': 10.2), which differs from run to run: leave it out
    rep.append([re.sub(r", 'seconds': [0-9.]+", '', l.replace(os.path.basename(g), 'PROGRAM'))
                for l in lines if not l.startswith(('screens', 'walked'))])
same = rep[0] == rep[1]
summ = [l for l in rep[0] if 'overlap' in l.lower() or 'straddl' in l.lower() or 'overrun' in l.lower() or 'firm' in l.lower()][-1:]
out.append('T ChiTable %s  %s' % ('same as the old version' if same else 'DIFFERS', summ[0][:120] if summ else ''))
print(out[-1], flush=True)
if not same:
    open('../overlap_ChiTable.txt', 'w').write('NEW\n' + '\n'.join(rep[0]) + '\n\nOLD\n' + '\n'.join(rep[1]))

lab = []
# label_fit_v1 reads the JSON the walks wrote, and the JSON of the verify script's own run (written beside them
# from the repository: python3 tools/text_overlap_v1.py --run verify/verify_ChiTable_beta3m.py --json r13/run_new.json)
for j in ('../walk_new.json', '../walk_old.json', '../run_new.json'):
    r = subprocess.run([sys.executable, 'tools/label_fit_v1.py', j], capture_output=True, text=True, timeout=600)
    lines = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    lab.append([l.replace(os.path.basename(g), 'PROGRAM') for l in lines])
newf = [l for l in lab[0] if l not in lab[1]]
out.append('L ChiTable walk: %s  %s' % ('no new finding' if not newf else '%d new lines' % len(newf), (lab[0][-1][:120] if lab[0] else '')))
out.append('L ChiTable verify run: %s' % (lab[2][-1][:140] if lab[2] else ''))
print(out[-1], flush=True)
if newf:
    open('../labelfit_ChiTable.txt', 'w').write('\n'.join(newf))

fleet = '../fleet'
shutil.rmtree(fleet, ignore_errors=True); os.makedirs(fleet)
for g in glob.glob('/home/claude/hp-prime-statistics/programs/*.txt'):
    if not os.path.basename(g).startswith('ChiTable_'):
        shutil.copy(g, fleet)
shutil.copy(NEW, fleet)
r = subprocess.run([sys.executable, 'tools/fleet_names_v2.py'] + sorted(glob.glob(fleet + '/*.txt')), capture_output=True, text=True)
fl = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
bad = [l for l in fl if any(k in l for k in ('COLLISION', 'UNTAGGED', 'MIXEDTAG', 'BUILTIN'))]
out.append('F fleet_names_v2 over %d programs: %s' % (len(glob.glob(fleet + '/*.txt')), 'clean' if not bad else '%d findings' % len(bad)))
out.append('  ' + (fl[-1] if fl else ''))
print('\n'.join(out[-2:]))
open('../checks_r13.txt', 'w').write('\n'.join(out) + '\n\n--- label_fit_v1, the walk of the new version\n' + '\n'.join(lab[0])
                                     + '\n\n--- label_fit_v1, the verify script\'s run\n' + '\n'.join(lab[2])
                                     + '\n\n--- fleet_names_v2 output\n' + '\n'.join(fl) + '\n')
