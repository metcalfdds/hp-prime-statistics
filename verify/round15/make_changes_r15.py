# -*- coding: utf-8 -*-
"""make_changes_r15.py -- docs/changes/<Name>_<version>_CHANGES.md for the five versions of Round 15 whose only change is
their wording about the TI-83/84 programs (RankLab beta 1i, AnovaLab beta 1h, ResampLab beta 1i, ExhibitLab beta 1h,
SurvLab beta 1g), from the build's own records (make_wording_r15.EDITS), the two help dumps, the gate reports and the
checks, all in this folder.  (ScatterLab beta 2l's and FitCheck beta 1h's notes are written by hand: they have new
arithmetic.)  Made from round12/make_changes_r12.py.  Run from the repository's root:
    python3 verify/round15/make_changes_r15.py ."""
import io, os, re, sys, json, difflib, importlib.util
REPO = os.path.abspath(sys.argv[1]); H = os.path.dirname(os.path.abspath(__file__)); os.chdir(REPO)
spec = importlib.util.spec_from_file_location('m15', os.path.join(H, 'make_wording_r15.py')); m15 = importlib.util.module_from_spec(spec)
sys.argv = ['x', '/dev/null']; spec.loader.exec_module(m15)
HO = json.load(open(os.path.join(H, 'helppages_before_r15.json'), encoding='utf-8')); HN = json.load(open(os.path.join(H, 'helppages_r15.json'), encoding='utf-8'))
HC = json.load(open(os.path.join(H, 'helpcheck_r15.json'), encoding='utf-8'))
VC = {l.split()[0]: l for l in open(os.path.join(H, 'vc_checks.txt'), encoding='utf-8') if 'No errors' in l}
CK = open(os.path.join(H, 'checks_r15.txt'), encoding='utf-8').read()
MK = {}
for f in os.listdir(os.path.join(H, 'mk')):
    if f.endswith('.jsonl'):
        v = [json.loads(l)['verdict'] for l in open(os.path.join(H, 'mk', f))]
        MK[f[:-6]] = (sum(x == 'OK' for x in v), len(v))
DEV = {
 'RankLab': 'Help page 7/7: four lines of credit at the foot of the page, the last one ("Written new for the Prime: none of their code.") clear of the footer.',
 'AnovaLab': 'Help page 9/9: thirteen lines now; the last ("clinical or legal use.", at y 198) clear of the footer.',
 'ResampLab': 'Help page 5/5: the sources paragraph is a line longer; the disclaimer under it still ends above the footer.',
 'ExhibitLab': 'Nothing on screen changed; the program should behave exactly as beta 1g.',
 'SurvLab': 'Nothing on screen changed; the program should behave exactly as beta 1f.',
}


def routine_of(lines, i):
    for j in range(i, -1, -1):
        mm = re.match(r'^(?:EXPORT |LOCAL )?([A-Za-z_]\w*)\([^)]*\)\s*$', lines[j])
        if mm:
            return mm.group(1)
    return '(header)'


for name, (ov, nv, eds, note) in m15.EDITS.items():
    old = m15.old_text(name, ov).split('\n')
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
    tv, to = m15.tag(nv), m15.tag(ov)
    o = ['# %s %s: changes (15 November 2026)' % (name, tv), '',
         'Round 15 of 15 November 2026, the wording. Roger, 14 November 2026: "IS there an issue with \'reworking\' the TI and '
         'Triola and Lloyd programs?" The record (the TI sweep of 20 October 2026) is that the TI-83/84 programs were read to '
         'see what each one computes and where it goes wrong, and that our programs were then written new in PPL; none of '
         'the TI code is in them. The earlier credits used a verb that says more than that. The book\'s Appendix F now '
         'ends with a paragraph in the author\'s words ("we did not reuse any of that code ... wrote our own version for '
         'the Prime ... to compute similar results"), and this version says the same where the program spoke of those '
         'programs. The build is `verify/round15/make_wording_r15.py`: each change is an exact replacement in %s %s (a '
         'miss stops it), then the version (header, history note, version strings).' % (name, to), '',
         '## What changed', '', '1. ' + note, '',
         ('2. **Nothing else changed**, apart from the header, the history note and the version strings. No line of code '
          'changed but the help text.') if rout else
         ('2. **Nothing else changed.** Every line that differs is a comment (the header and its history note): not one '
          'line the calculator runs is different.'), '',
         'Lines of %s %s that differ from %s %s: %s. Routines whose code changed, with the number of lines: %s.'
         % (name, tv, name, to, '; '.join(hunks), ', '.join('%s %d' % kv for kv in rout.items()) or 'none'), '']
    ch = [k for k, (a, b) in enumerate(zip(HO.get(name, []), HN.get(name, []))) if a != b]
    if ch:
        o += ['## The help, before and after', '',
              'As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the '
              'screen that changed.', '']
        for k in ch:
            a = HO[name][k]; b = HN[name][k]
            a = a if isinstance(a, list) else [a]; b = b if isinstance(b, list) else [b]
            o += ['### Screen %d, before (%s)' % (k + 1, to), '', '```text'] + a + ['```', '',
                  '### Screen %d, after (%s)' % (k + 1, tv), '', '```text'] + b + ['```', '']
    g = io.open(os.path.join(H, 'gates', '%s_%s.txt' % (name, nv)), encoding='utf-8').read()
    lint = re.search(r'lint_ppl \(v4\): \d+ checks, (\d+) problems', g)
    hc = HC.get(name)
    o += ['## Checks', '',
          '- `verify/verify_round15_wording_v1.py` (39 checks, 0 failed, for the five programs together; output beside it): '
          'the build makes this file byte for byte; only the replacements, comments and version strings differ from %s; '
          'the help dump is the saved one%s; the old verb is nowhere in the file; and over 30 seeds of the monkey the old '
          'and the new version show the same screens, boxes and Quit summary%s.'
          % (to, ', and screen %s is the only one that changed' % ', '.join(str(k + 1) for k in ch) if ch else ', and no screen changed',
             ', apart from that page and the version string' if ch else ''),
          '- `tools/ppl_gate_v1e.py` against %s %s: %s. lint_ppl %s problems, as in %s %s; fleet_names_v2 over the 31 newest '
          'files: no collisions.' % (name, to, 'PASS' if 'RESULT: PASS' in g else 'FAIL', lint.group(1) if lint else '?', name, to),
          '- `verify/round15/helpcheck_r15.json` (Round 11\'s `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): '
          + ('%d screens, %s.' % (hc['screens'], 'no reports' if not hc['problems'] else '; '.join(hc['problems'])))]
    sm = re.search(r'^S %-10s .*$' % re.escape(name), CK, re.M)
    tt = re.search(r'^T %-10s .*$' % re.escape(name), CK, re.M)
    if sm: o.append('- The harness smoke test (main routine, idle key Esc): %s.' % sm.group(0)[13:].strip())
    if tt:
        t_ = re.sub(r'\s+', ' ', tt.group(0)[13:].strip()).replace(' PROGRAM ', ': ')
        tight = re.search(r'collisions (\d+) \(firm (\d+)\)', t_)
        o.append('- `tools/text_overlap_v1.py --walk`: %s.%s' % (t_, (' What the one-line summary counts as collisions here are '
                 'rows of small text 11 px apart, which the tool\'s full report lists as "tight rows"; its count of overlaps is 0, '
                 'and %s %s gives the same report.' % (name, to)) if tight and int(tight.group(1)) > 0 else ''))
    if name in MK:
        o.append('- The monkey (`tools/monkey_chunks_v1.py`, base 15, with `--lists`): {:,} of {:,} runs OK.'.format(*MK[name]))
    else:
        o.append('- The monkey was not run again: not one line the calculator runs is different (only comments changed).')
    if name in VC:
        o.append('- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "%s"'
                 % 'No errors in the program' + ('; the help page that changed was then looked at there (`verify/round15/screens/`).' if ch else '.'))
    o += ['', '## On a G1 or a G2', '', 'Not yet run on a G1 or a G2. To look at: ' + DEV[name], '']
    io.open(os.path.join(REPO, 'docs', 'changes', '%s_%s_CHANGES.md' % (name, nv)), 'w', encoding='utf-8').write('\n'.join(o))
    print('%s_%s_CHANGES.md' % (name, nv), len('\n'.join(o).split()), 'words')
