#!/usr/bin/env python3
"""monkey_labels_v1.py -- every program's labels under random use (2 Nov 2026; round 4 of the monkey work).

A generic walk or a verify script draws a program at sensible values, where labels are short.  Cut numbers and crowded
labels show at the odd values a careless student types, so this drives each current program in programs/ (the newest
letter of each name) with the monkey (monkey_v1b.py: random keys, taps, menu picks and typed values, 1E300 and 1E-300
among them) with text_overlap_v1's recorder on, and reports per program the firm overlaps / straddles / overruns and
the numbers label_fit_v1 finds cut short by a TEXTOUT_P width argument.  The findings of each program are written to
OUT/<Name>.json.  docs/dev/label-check-2026-11-02.md has the first run.

    python3 tools/monkey_labels_v1.py RUNS [NAME ...] [--out DIR]      (RUNS a program; GaltonBoard gets RUNS/4)

Seeds are 3000, 3001, ...: a finding's run is found again by rerunning those seeds one at a time with the recorder on.
Give the job a processor of its own: the monkey's time limit is wall-clock (Lessons Learned v7zj).
"""
import glob
import json
import os
import re
import sys
import warnings

warnings.filterwarnings('ignore')
TOOLS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
args = sys.argv[1:]
out_dir = 'monkey_labels_out'
if '--out' in args:
    i = args.index('--out')
    out_dir = args[i + 1]
    del args[i:i + 2]
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
os.chdir(TOOLS)
import text_overlap_v1 as OV  # noqa: E402
OV.install()
import label_fit_v1 as LF  # noqa: E402
sys.argv = ['monkey_v1b.py']
import monkey_v1b as M  # noqa: E402

CALL = {'Norm3': 'Norm3(0,1,1.96)', 'DataLoad': 'DATALOAD()', 'NormExplorer': 'NormExp()', 'PowerViz': 'POWERVIZ()',
        'TTestLab': 'TTESTLAB()', 'TTestLabG': 'TTESTLABG()'}
RUNS = int(args[0])
progs = {}
for p in sorted(glob.glob(os.path.join(ROOT, 'programs', '*.txt'))):
    progs[re.match(r'([A-Za-z0-9]+?)_', os.path.basename(p)).group(1)] = p      # sorted: the newest letter wins
for name in (args[1:] or sorted(progs)):
    p = progs[name]
    call = CALL.get(name, name + '()')
    OV.RECORDS.clear()
    runs = RUNS if name != 'GaltonBoard' else max(10, RUNS // 4)
    verdicts = {}
    for k in range(runs):
        try:
            r = M.one_run(p, call, 3000 + k, 150, 30, True)
            verdicts[r['verdict']] = verdicts.get(r['verdict'], 0) + 1
        except Exception:
            verdicts['ERR'] = verdicts.get('ERR', 0) + 1
    rep = OV.report()
    firm = []
    for t, f in rep.items():
        firm += [('overlap', c['a'][:24], c['b'][:24], c['func']) for c in f['collisions']
                 if c['severity'] == 'overlap' and c['firm']]
        firm += [('straddle', x['text'][:24], x.get('edge'), x.get('func')) for x in f['straddles'] if x['firm']]
        firm += [('overrun', x['text'][:24], x.get('right'), x.get('func')) for x in f['overruns'] if x['firm']]
    cut = LF.clipped(OV.RECORDS)
    nscr = sum(f['screens_distinct'] for f in rep.values())
    print('%-13s runs %4d %s  screens %5d  firm %3d  cut %3d' % (name, runs, dict(sorted(verdicts.items())), nscr,
                                                                 len(firm), sum(len(v) for v in cut.values())),
          flush=True)
    for x in firm[:8]:
        print('      %s %r %r in %s' % x, flush=True)
    for tag, lst in cut.items():
        for x in lst[:8]:
            print('      cut %r at (%g, %g) font %s width %g needs %g' % x, flush=True)
    json.dump({'firm': firm, 'cut': {k: [list(x) for x in v] for k, v in cut.items()}},
              open(os.path.join(out_dir, name + '.json'), 'w'))
    for f in glob.glob(os.path.join(TOOLS, 'session.tex')):
        os.remove(f)
