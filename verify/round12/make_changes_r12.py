# -*- coding: utf-8 -*-
"""make_changes_r12.py -- docs/changes/<Name>_<version>_CHANGES.md for Round 12's twelve new versions, from the build's
own records (make_round12.EDITS), the two help dumps, the gate reports and the checks, all in this folder.  Run from
the repository's root:  python3 verify/round12/make_changes_r12.py ."""
import io, os, re, sys, json, difflib, importlib.util
REPO = os.path.abspath(sys.argv[1]); H = os.path.dirname(os.path.abspath(__file__)); os.chdir(REPO)
spec = importlib.util.spec_from_file_location('m12', os.path.join(H, 'make_round12.py')); m12 = importlib.util.module_from_spec(spec)
sys.argv = ['x', '/dev/null']; spec.loader.exec_module(m12)
HO = json.load(open(os.path.join(H, 'helppages_before_r12.json'), encoding='utf-8')); HN = json.load(open(os.path.join(H, 'helppages_r12.json'), encoding='utf-8'))
HC = json.load(open(os.path.join(H, 'helpcheck_r12.json'), encoding='utf-8'))
VC = {l.split()[0]: l for l in open(os.path.join(H, 'vc_checks.txt'), encoding='utf-8') if 'No errors' in l}
CK = open(os.path.join(H, 'checks_r12.txt'), encoding='utf-8').read()
MK = {}
for f in os.listdir(os.path.join(H, 'mk')):
    if f.endswith('.jsonl'):
        v = [json.loads(l)['verdict'] for l in open(os.path.join(H, 'mk', f))]
        MK[f[:-6]] = (sum(x == 'OK' for x in v), len(v))
UNRES = {
 'TTestLab': 'TTestLab is the version that follows the lecture, so its rounding notes and the pooled-or-separate note still '
             'begin "The lecture" (three places); TTestLabG has none.  The book uses both.',
 'AnovaLab': 'The menus, the Pairs page\'s method name and the message about Tukey still write "Scheffe" without the accent; '
             'only the help page\'s prose has it.',
 'DataLoad': 'Whether a backslash in a PPL string prints once or twice on the calculator is still untested; no help page '
             'needs one now.',
}
DEV = {
 'TTestLab': 'The menu reads "Choose the test (flowchart)" and fits its box; the flowchart\'s title reads "Which t-test?".',
 'AnovaLab': 'Help page 4/9: the é of Scheffé is drawn as an accented e.',
 'SampDist': 'Help pages 1/2 and 2/2: each label alone on its line in blue, its items indented in black; nothing reaches '
             'the footer.',
 'PowerViz': 'Help page 3/7: five lines under DRAG ON THE PLOT, and TAP THE READOUT below them.',
 'RankLab': 'Help pages 2/7 and 5/7: one key per line; every line inside the page. Load the jury preset, then Your data > Groups with only D1 filled: refused with its sentence, and a Mann-Whitney afterwards still offers the jury\'s three groups.',
 'BayesTree': 'Help page 2/5: the three sets of soft keys on three lines.',
 'EpiStats': 'Help pages 1/15 and 11/15.',
}


def routine_of(lines, i):
    for j in range(i, -1, -1):
        mm = re.match(r'^(?:EXPORT |LOCAL )?([A-Za-z_]\w*)\([^)]*\)\s*$', lines[j])
        if mm:
            return mm.group(1)
    return '(header)'


for name, (ov, nv, eds, note) in m12.EDITS.items():
    old = m12.old_text(name, ov).split('\n')
    new = io.open(os.path.join(REPO, 'programs', '%s_%s.txt' % (name, nv)), encoding='utf-8').read().split('\n')
    hunks, rout = [], {}
    for tag_, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag_ == 'equal':
            continue
        what = 'comment' if all(l.lstrip().startswith('//') for l in new[j1:j2]) and j2 > j1 else 'code'
        hunks.append('%s %s' % ('line %d' % (j1 + 1) if j2 - j1 <= 1 else 'lines %d-%d' % (j1 + 1, j2), '(%s)' % what))
        if what == 'code':
            r = routine_of(new, j1)
            rout[r] = rout.get(r, 0) + max(j2 - j1, i2 - i1)
    tv, to = m12.tag(nv), m12.tag(ov)
    o = ['# %s %s: changes (13 November 2026)' % (name, tv), '',
         'Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which '
         'prints every program\'s help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix '
         'the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change '
         'is an exact replacement in %s %s (a miss stops it), then the version (header, history note, version strings).'
         % (name, to), '', '## What changed', '', '1. ' + note, '',
         '2. **Nothing else changed**, apart from the header, the history note and the version strings.', '',
         'Lines of %s %s that differ from %s %s: %s. Routines whose code changed, with the number of lines: %s.'
         % (name, tv, name, to, '; '.join(hunks), ', '.join('%s %d' % kv for kv in rout.items())), '',
         '## The help, before and after', '',
         'As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the '
         'screens that changed.', '']
    for k, (a, b) in enumerate(zip(HO.get(name, []), HN.get(name, []))):
        a = a if isinstance(a, list) else [a]; b = b if isinstance(b, list) else [b]
        if a != b:
            o += ['### Screen %d, before (%s)' % (k + 1, to), '', '```text'] + a + ['```', '',
                  '### Screen %d, after (%s)' % (k + 1, tv), '', '```text'] + b + ['```', '']
    g = io.open(os.path.join(H, 'gates', '%s_%s.txt' % (name, nv)), encoding='utf-8').read()
    lint = re.search(r'lint_ppl \(v4\): \d+ checks, (\d+) problems', g)
    hc = HC.get(name)
    o += ['## Checks', '',
          '- `tools/ppl_gate_v1e.py` against %s %s: %s. lint_ppl %s problems, as in %s %s; fleet_names_v2 over the 31 newest '
          'files: no collisions.' % (name, to, 'PASS' if 'RESULT: PASS' in g else 'FAIL', lint.group(1) if lint else '?', name, to),
          '- `verify/round12/helpcheck_r12.json` (Round 11\'s `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): '
          + ('%d screens, %s.' % (hc['screens'], 'no reports' if not hc['problems'] else 'one known report: ' + '; '.join(hc['problems']))),
          '- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that '
          'changed, and they changed only as listed.']
    sm = re.search(r'^S %-10s .*$' % re.escape(name), CK, re.M)
    tt = re.search(r'^T %-10s .*$' % re.escape(name), CK, re.M)
    if sm: o.append('- The harness smoke test (main routine, idle key Esc): %s.' % sm.group(0)[13:].strip())
    if tt: o.append('- `tools/text_overlap_v1.py --walk`: %s.' % tt.group(0)[13:].strip())
    if name in MK:
        o.append('- The monkey (`tools/monkey_chunks_v1.py`, base 12, with `--lists`): %d of %d runs OK.' % MK[name])
    if name in VC:
        o.append('- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "%s".'
                 % 'No errors in the program')
    o += ['', '## On a G1 or a G2', '',
          'Not yet run on a G1 or a G2. To look at: ' + DEV.get(name, 'the help page that changed.'), '']
    if name in UNRES:
        o += ['## Unresolved', '', UNRES[name], '']
    io.open(os.path.join(REPO, 'docs', 'changes', '%s_%s_CHANGES.md' % (name, nv)), 'w', encoding='utf-8').write('\n'.join(o))
    print('%s_%s_CHANGES.md' % (name, nv), len('\n'.join(o).split()), 'words')
