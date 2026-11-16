# -*- coding: utf-8 -*-
"""directed_r16.py -- Round 16's directed monkey runs: each session starts ON one of the round's new pages, then takes
the monkey's random keys, taps, drags, menu picks and typed values (tools/monkey_directed_v1.py).

Why: tools/monkey_reach_v1.py counted how often the plain monkey test's sessions found the new pages by themselves.  Of
the first 300 sessions of each program (mk/reach_r16.txt): Dunnett's table in 3 and its plot in none (AnovaLab); the
tolerance interval in none (CICatcher); the Outlier page in 19 (FitCheck); the pictures of Page's L and of the runs test
in 61 and 56 (RankLab); the target view in 69 (BiNorm3D).  So the plain test says little about Dunnett's two pages and
nothing about the tolerance interval.

Run from the repository's root (needs hp-prime-kit at HPKIT); RUNS sessions a set, written as they end, so a stopped job
resumes.  It writes mk/directed/<set>.jsonl and mk/directed_r16.txt (one line a set).

    python3 verify/round16/directed_r16.py [RUNS=200]
"""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
os.chdir(REPO)
os.environ.setdefault('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 200
K5 = (240, 228)
K3 = (133, 228)
E = ('key', 'Enter')


def c(n):
    return ('choose', n)


# (set, program, call, base, lead, the text that shows the page, extra options)
SETS = [
    # AnovaLab: the opening page, Load a preset, the preset, Enter = the menu, Dunnett, the control, "Compute it now"
    ('AnovaLab_dunnett_insects_table', 'AnovaLab_beta1i', 'AnovaLab()', 1611, [E, c(5), c(4), E, c(6), c(1), c(1)],
     'Dunnett: each group vs a control', []),
    ('AnovaLab_dunnett_draft_plot', 'AnovaLab_beta1i', 'AnovaLab()', 1612,
     [E, c(5), c(3), E, c(6), c(12), c(1), ('key', 'Right')], 'Dunnett plot: group minus control', []),
    ('AnovaLab_dunnett_jury_table', 'AnovaLab_beta1i', 'AnovaLab()', 1613, [E, c(5), c(1), E, c(6), c(2), c(1)],
     'Dunnett: each group vs a control', []),
    # ... Use my data > One-way: D1-D9 = groups, with the monkey's lists in D1 and D2 (two groups, one comparison)
    ('AnovaLab_dunnett_mydata', 'AnovaLab_beta1i', 'AnovaLab()', 1614, [E, c(6), c(1), E, c(6), c(1), c(1)],
     'Dunnett: each group vs a control', ['--missed-ok']),
    # FitCheck: Normality, Darwin's differences (or My values in D1), the Outlier key
    ('FitCheck_outlier_darwin', 'FitCheck_beta1i', 'FitCheck()', 1621, [E, c(5), c(3), E, ('tap',) + K5],
     r'Outlier\? ', ['--writes', 'D']),
    ('FitCheck_outlier_mydata', 'FitCheck_beta1i', 'FitCheck()', 1622, [E, c(5), c(4), ('tap',) + K5],
     r'Outlier\? ', ['--writes', 'D', '--missed-ok']),
    # CICatcher: Which interval? > Tolerance, hold 95 % (or 99 %), the form as it stands (or as the monkey fills it)
    ('CICatcher_tolerance_95', 'CICatcher_beta2l', 'CICatcher()', 1631, [E, c(6), c(2), ('input', 'ACCEPT')],
     r'tol\. [0-9]', []),
    ('CICatcher_tolerance_99_form', 'CICatcher_beta2l', 'CICatcher()', 1632, [E, c(6), c(3)],
     r'tol\. [0-9]', ['--missed-ok']),
    # RankLab: main menu 9 and 10 (each loads its example), the two lottery presets, and Runs: D1 in order
    ('RankLab_page_ozone', 'RankLab_beta1j', 'RankLab()', 1641, [E, c(9)], r'(^|\| )L = [0-9]', []),
    ('RankLab_page_months', 'RankLab_beta1j', 'RankLab()', 1642, [E, c(7), c(9)], r'(^|\| )L = [0-9]', []),
    ('RankLab_runs_roulette', 'RankLab_beta1j', 'RankLab()', 1643, [E, c(10)], r'runs = [0-9]', []),
    ('RankLab_runs_days', 'RankLab_beta1j', 'RankLab()', 1644, [E, c(7), c(11)], r'runs = [0-9]', []),
    ('RankLab_runs_mydata', 'RankLab_beta1j', 'RankLab()', 1645, [E, c(8), c(7)], r'runs = [0-9]', ['--missed-ok']),
    # BiNorm3D: soft key 3 twice = the target view
    ('BiNorm3D_target', 'BiNorm3D_beta1g', 'BiNorm3D()', 1651, [E, ('tap',) + K3, ('tap',) + K3], 'Target: CEP, ', []),
]

os.makedirs(os.path.join(HERE, 'mk', 'directed'), exist_ok=True)
lines = []
for name, prog, call, base, lead, reach, extra in SETS:
    out = os.path.join('verify', 'round16', 'mk', 'directed', name + '.jsonl')
    r = subprocess.run([sys.executable, 'tools/monkey_directed_v1.py', 'programs/%s.txt' % prog, call, str(base), '0',
                        str(RUNS), out, '--lists', '--lead', repr(lead), '--reach', reach] + extra,
                       capture_output=True, text=True)
    tail = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    # the tally over the whole file (a resumed job prints only the runs it added)
    import collections
    import json
    v = collections.Counter()
    on = 0
    n = 0
    for ln in open(out):
        d = json.loads(ln)
        n += 1
        v[d['verdict']] += 1
        on += 1 if d['reached'] else 0
    line = '%-32s %d runs: %s; on the page in %d%s' % (name, n, dict(v), on,
                                                    '  (--missed-ok)' if '--missed-ok' in extra else '')
    lines.append(line)
    print(line, flush=True)
    for l in tail[:-1][:20]:
        lines.append('    ' + l[:300])
        print('    ' + l[:300], flush=True)
io.open(os.path.join(HERE, 'mk', 'directed_r16.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
