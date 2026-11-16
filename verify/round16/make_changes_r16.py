# -*- coding: utf-8 -*-
"""make_changes_r16.py -- docs/changes/<Name>_<version>_CHANGES.md for the four versions of Round 16 whose only change is
what their header says about the programs they stand beside (StatDist v2.7n, AgreeLab beta 1h, RiskLab beta 1h, BurrLab
beta 1r), from the build's own records (make_wording_r16.EDITS), the two help dumps, the gate reports and the checks, all
in this folder.  (The notes of BiNorm3D beta 1g, CICatcher beta 2l, FitCheck beta 1i, RankLab beta 1j and AnovaLab beta 1i
are written by hand: they have new arithmetic.)  Made from round15/make_changes_r15.py.  Run from the repository's root,
after records_r16.py:
    python3 verify/round16/make_changes_r16.py ."""
import io, os, re, sys, json, difflib, importlib.util
REPO = os.path.abspath(sys.argv[1]); H = os.path.dirname(os.path.abspath(__file__)); os.chdir(REPO)
spec = importlib.util.spec_from_file_location('m16', os.path.join(H, 'make_wording_r16.py')); m16 = importlib.util.module_from_spec(spec)
sys.argv = ['x', '/dev/null']; spec.loader.exec_module(m16)
HO = json.load(open(os.path.join(H, 'helppages_before_r16.json'), encoding='utf-8')); HN = json.load(open(os.path.join(H, 'helppages_r16.json'), encoding='utf-8'))
HC = json.load(open(os.path.join(H, 'helpcheck_r16.json'), encoding='utf-8'))
VC = {l.split()[0]: l for l in open(os.path.join(H, 'vc_checks.txt'), encoding='utf-8') if 'No errors' in l}
CK = open(os.path.join(H, 'checks_r16.txt'), encoding='utf-8').read()
WV = open(os.path.join(REPO, 'verify', 'verify_round16_wording_v1_output.txt'), encoding='utf-8').read()
# what the record says, beyond the one line the build keeps
MORE = {
 'StatDist': ('**The record** (15 November 2026; `statistic.zip` from hpcalc.org, in `D:\\HP-Prime`, set beside the StatDist '
              'files). Micciche\'s "Statistic Distributions" is 494 lines: 55 exported density and distribution '
              'functions, typed at Home, with no menus and no plots. Of its 134 distinct code lines not one is in '
              'StatDist v2.7m (5,091 lines), in v2.5 or in v2.2 (29 July 2026, the oldest copy kept); none of its '
              'function names or of its "Use: ..." messages is in them either. Eleven of the 13 families StatDist adds '
              'to the Prime\'s own are families his file has (not Burr XII, not the triangular). So the two programs '
              'do the same kind of thing for many of the same distributions, and share no code. "Framework after" '
              'said more than that.'),
 'BurrLab': ('**Why this one keeps the word "reuses".** Burr3 is the author\'s own earlier program, and parts of it were '
             'carried over: its header, its drag idiom and its log-domain pdf and CDF. The rule asks that a credit '
             'say which code was carried over where any was, and this one does.'),
 'RiskLab': ('**What LOGIT is.** A TI-83/84 program that fits a one-predictor logistic model to grouped counts by '
             'weighted least squares. Its decoded listing (`LOGIT__257.txt`, from `logit.zip`, in the author\'s working folder) was read to see what it '
             'computes. RiskLab fits one to four predictors by Newton–Raphson, gives standard errors, tests and odds '
             'ratios, and detects separation; none of that is in LOGIT, and none of LOGIT\'s code is in RiskLab.'),
 'AgreeLab': ('**What was looked for.** The decoded TI programs in the author\'s working folder (`ref/triola_ti_programs/`) hold no agreement program '
              '(a search for kappa finds only Bayesian posterior programs). AgreeLab was written from the papers its '
              'header lists.'),
}
# the two standing reports of the help layout check, as verify/round11/README.md explains them
KNOWN = {
 'StatDist': 'one known report, as in Rounds 11 and 12: the harness cannot call `st_ABHelp` without its argument (its pages are checked through the menu)',
 'AgreeLab': ('one known report, as in Round 11: the d̄ drawn on help page 7 (the check measures the bar\'s d as a plain '
              'letter beside the next text; the Virtual Calculator shows the line correctly)'),
}
SEEN = {
 'AgreeLab': 'its opening page ("AgreeLab - beta 1h") and its menu were seen, and it was left with "AgreeLab: no analysis run"',
 'RiskLab': 'its opening page ("beta 1h, 15 Nov 2026.  Help is in the menu.") and its menu were seen, and it was left with "RiskLab: COMPAS, AUC = 0.711, ≥ 5: sens 0.645, spec 0.670"',
 'BurrLab': 'its opening page ("BurrLab beta 1r: the long right tail") and its menu were seen, and it was left with "BurrLab: no fit; explorer at C = 2.00, K = 1.50, S = 10.00"',
 'StatDist': 'its menu and its four help pages were seen, and it was left with "StatDist: no plot drawn yet"',
}


def routine_of(lines, i):
    for j in range(i, -1, -1):
        mm = re.match(r'^(?:EXPORT |LOCAL )?([A-Za-z_]\w*)\([^)]*\)\s*$', lines[j])
        if mm:
            return mm.group(1)
    return '(header)'


for name, (ov, nv, eds, note) in m16.EDITS.items():
    old = m16.old_text(name, ov).split('\n')
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
    tv, to = m16.tag(nv), m16.tag(ov)
    o = ['# %s %s: changes (15 November 2026)' % (name, tv), '',
         'Round 16 of 15 November 2026, the wording. Round 15 reworded the credits of the six programs that follow '
         'TI-83/84 programs, so that each says what was done in plain verbs. Four more programs spoke of other programs in '
         'words that said more, or less, than the record: StatDist\'s "framework after S. Micciche", and the label '
         '"Replaces / reworks:" in BurrLab, RiskLab and AgreeLab. Asked whether these should be reworded too, Roger, '
         '15 November 2026: "reword as the others---look, be consistent throughout the book". The build is '
         '`verify/round16/make_wording_r16.py`: each change is an exact replacement in %s %s (a miss stops it), then the '
         'version (header, history note, version strings).' % (name, to), '',
         '## What changed', '', '1. ' + note, '',
         ('2. **Nothing else changed**, apart from the header, the history note and the version the program shows (one '
          'line of code, in `%s`). The help is the same, screen for screen.' % ', '.join(rout)) if rout else
         ('2. **Nothing else changed.** Every line that differs is a comment (the header and its history note): not one '
          'line the calculator runs is different, and the program shows no version on its pages.'), '',
         MORE[name], '',
         'Lines of %s %s that differ from %s %s: %s.' % (name, tv, name, to, '; '.join(hunks)), '']
    ch = [k for k, (a, b) in enumerate(zip(HO.get(name, []), HN.get(name, []))) if a != b]
    assert not ch, (name, ch)                 # no help screen changed in this round's four
    g = io.open(os.path.join(H, 'gates', '%s_%s.txt' % (name, nv)), encoding='utf-8').read()
    lint = re.search(r'lint_ppl \(v4\): \d+ checks, (\d+) problems', g)
    hc = HC.get(name)
    t7 = re.search(r'^T7\s+PASS\s+%s: (.*)$' % re.escape(name), WV, re.M)
    t2 = re.search(r'^T2\s+PASS\s+%s: (\d+) lines that are not comments' % re.escape(name), WV, re.M)
    o += ['## Checks', '',
          '- `verify/verify_round16_wording_v1.py` (25 checks, 0 failed, for the four programs together; output beside it): '
          'the build makes this file byte for byte; its %s lines that are not comments are %s %s\'s%s; the help dump is '
          'the old version\'s, screen for screen; no line of any of the 31 programs begins "// Replaces / reworks", and '
          'no author line says "(framework after"; the header says the new words; and over 30 seeds of the monkey the '
          'old and the new version show the same screens text for text (%s).'
          % ('{:,}'.format(int(t2.group(1))) if t2 else '?', name, to, ', but for the one with the version' if rout else '',
             re.sub(r'(\d+) screens', lambda m: '{:,} screens,'.format(int(m.group(1))),
                    t7.group(1).replace(' the same text for text', '').replace('(OK 30)', 'all 30 runs OK')).replace('30 seeds, ', '').strip() if t7 else '?'),
          '- `tools/ppl_gate_v1e.py` against %s %s (`verify/round16/gates/%s_%s.txt`): %s. hp-prime-kit lint 0 errors; '
          '`lint_ppl` %s reports, as in %s %s; `fleet_names_v2` over the 31 newest files: no collisions.'
          % (name, to, name, nv, 'PASS' if 'RESULT: PASS' in g else 'FAIL', lint.group(1) if lint else '?', name, to),
          '- `verify/round16/helpcheck_r16.json` (Round 11\'s `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): '
          + ('%d screens, %s.' % (hc['screens'], 'no reports' if not hc['problems'] else KNOWN[name]))]
    sm = re.search(r'^S %-10s .*$' % re.escape(name), CK, re.M)
    tt = re.search(r'^T %-10s .*$' % re.escape(name), CK, re.M)
    if sm: o.append('- The harness smoke test (main routine, idle key Esc): %s.' % re.sub(r'\s+', ' ', sm.group(0)[13:].strip()))
    if tt:
        t_ = re.sub(r'\s+', ' ', tt.group(0)[13:].strip())
        assert t_.startswith('same report as the old version'), t_
        o.append('- `tools/text_overlap_v1.py --walk`: the same report as %s %s\'s, as it must be with the same screens (%s).'
                 % (name, to, t_.split('PROGRAM ')[1].strip()))
    o.append('- The monkey\'s 1,000 runs were not made again: %s, and 30 seeds show the same screens in both versions.'
             % ('only the version string differs among the lines the calculator runs' if rout else
                'not one line the calculator runs is different'))
    if name in VC:
        o.append('- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "No errors '
                 'in the program"; the program was then started from the Program Catalog, %s (`verify/round16/vc_checks.txt`, '
                 '`verify/round16/screens/%s_*.png`).' % (SEEN[name], name))
    o += ['', '## On a G1 or a G2', '',
          'Not yet run on a G1 or a G2. Nothing on the screen changed%s; the program should behave exactly as %s.'
          % (' but the version the opening page shows' if rout else '', to), '']
    io.open(os.path.join(REPO, 'docs', 'changes', '%s_%s_CHANGES.md' % (name, nv)), 'w', encoding='utf-8').write('\n'.join(o))
    print('%s_%s_CHANGES.md' % (name, nv), len('\n'.join(o).split()), 'words')
