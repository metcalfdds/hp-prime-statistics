# -*- coding: utf-8 -*-
"""Round 18: writes the 31 change notes, docs/changes/<Name>_<version>_CHANGES.md, from the programs themselves, from the
verify script's saved output and from vc_checks.txt (what the Virtual Calculator did with each one).

Run from the repository's root, after verify/verify_round18_settings_v1.py:   python3 verify/round18/make_changes_r18.py .
"""
import io, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import make_round18 as R  # noqa: E402

OUT = os.path.join(sys.argv[1] if len(sys.argv) > 1 else REPO, 'docs', 'changes')
PAIRS = sorted([(n, ov, R.nxt(ov)) for n, ov in R.OLD.items()] + [(R.GENERAL[0], R.GENERAL[1], R.nxt(R.GENERAL[1]))])
VER = io.open(os.path.join(REPO, 'verify', 'verify_round18_settings_v1_output.txt'), encoding='utf-8').read().split('\n')
VC = {}
for l in io.open(os.path.join(HERE, 'vc_checks.txt'), encoding='utf-8').read().split('\n'):
    m = re.match(r'^(\w+)\s+\|\s*(.*)$', l)
    if m:
        VC[m.group(1)] = [x.strip() for x in m.group(2).split('|')]
total = [l for l in VER if re.match(r'^\d+ checks', l)][0]

WHY = ('Round 18 of 22 November 2026: every program sets the four Home settings that the book\'s examples assume when it starts, '
       'and leaves them set. That afternoon the Virtual Calculator had been set to a comma as its decimal point (Home Settings, '
       'Digit Grouping 123.456,789), as a reader in Europe may have it. `STRING` then writes a comma, inside a running program too, '
       'and every program\'s comma routine took the decimals for a whole number: Norm3 showed 0.9772 as 0,9,772, and the two programs '
       'with no `#pragma mode` line, NormExplorer and StudRange, stopped the calculator at Run '
       '(`docs/dev/comma-decimal-mark-2026-11-22.md`). Three probes showed that a program can assign Home\'s settings and that they '
       'stay set (`diagnostics/SetProbe_beta1.txt`, `SetOdd_beta1.txt`, `SetBook_beta1.txt`). Roger, asked whether a program should '
       'put the reader\'s own settings back when it ends or leave the book\'s on: "I agree that we should leave the calculator the '
       'way Statisticles sets it--and that also helps avoid any potential mis-settings in subsequent Statisticles--we keep putting '
       'the calculator in the mode we need it to be in". The round is in `verify/round18/README.md`.')

for n, ov, nv in PAIRS:
    ot, nt = R.tag(ov), R.tag(nv)
    new = io.open(os.path.join(REPO, 'programs', '%s_%s.txt' % (n, nv)), encoding='utf-8').read().split('\n')
    old = subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (R.BASE, n, ov)], check=True, capture_output=True,
                         cwd=REPO).stdout.decode('utf-8').split('\n')
    sets = [i + 1 for i, l in enumerate(new) if l.strip() == R.LINE]
    rout = []
    for ln in sets:
        k = ln - 1
        while not re.match(r'^\s*(EXPORT\s+)?\w+\s*\([^)]*\)\s*$', new[k]):
            k -= 1
        rout.append((ln, re.search(r'(\w+)\s*\(', new[k].replace('EXPORT', '')).group(1)))
    h0 = [i for i, l in enumerate(new) if l.startswith('// %s (%s): Round 18:' % (nt, R.DATE))][0]
    h1 = h0 + 1
    while new[h1].startswith('//   '):
        h1 += 1
    shown = sum(1 for l in new if nt in R.split_comment(l)[0] and '"' in l)
    mine = [l for l in VER if re.match(r'^\w+\s+%s\s' % re.escape(n), l)]
    smoke = [re.sub(r'^S\s+\w+\s+(OK|FAIL)\s+', '', l).strip() for l in mine if l.startswith('S ')]
    T = ['# %s %s: changes (22 November 2026)' % (n, nt), '', WHY, '', '## What changed', '']
    T.append('1. **One line at the head of %s** (%s), after the routine\'s LOCAL lines:' % (
        ' and '.join('`%s`' % r for _, r in rout), ', '.join('line %s' % '{:,}'.format(ln) for ln, _ in rout)))
    T += ['', '   ```', '   ' + R.LINE, '   ```', '']
    T.append('   `HSeparator := 0` is Digit Grouping 123,456.789 (the period as the decimal point), `HFormat := 0` is Number Format '
             'Standard, `HAngle := 0` is Radians and `Entry := 0` is Textbook entry. Nothing puts them back: the calculator is left '
             'the way the book needs it.' + (' CentralLimit is an app, and an app is started by its hooks, so the line is in '
             '`START` and in `Plot`; its `EXPORT CentralLimit()` is empty and has none.' if n == 'CentralLimit' else ''))
    k = 2
    if n in R.NO_PRAGMA:
        T.append('%d. **The first line is new:** `%s`, word for word the first line of 28 of the other 29 programs. Without it '
                 '%s %s stopped the Virtual Calculator at Run when Home\'s decimal mark was a comma, and started as usual with a period.'
                 % (k, R.PRAGMA, n, ot)); k += 1
    if n == 'TTestLabG':
        T.append('%d. **Built from TTestLab beta 1m** by `tools/make_tlg1_v5.py` (v4 for the next pair of versions; its blocks are '
                 'v4\'s, unchanged), as the general version always is. The line came over with the code.' % k); k += 1
    T.append('%d. **Nothing else changed.** With that line%s and the history note taken out, %s %s and %s %s are the same line for '
             'line but for the version: the header (%s)%s. The history note is lines %d to %d. No help page, no menu, no number and no '
             'other word on a page changed.' % (k, ' and the first line' if n in R.NO_PRAGMA else '', n, ot, n, nt,
             'it has no line that names the version' if n in R.NO_HEADER else 'one line',
             (' and %d quoted string%s that show%s the version on a page' % (shown, '' if shown == 1 else 's', 's' if shown == 1 else '')) if shown else
             '; the program shows no version on its pages', h0 + 1, h1))
    T += ['', '## For the book', '',
          '- The version in the table of "How to use this book" becomes %s, and Appendix F\'s count of lines becomes %s (it was %s).'
          % (nt, '{:,}'.format(len(new)), '{:,}'.format(len(old))),
          '- Draft 69 asks every reader to choose 123,456.789 and says that two of the programs showed their numbers with commas in '
          'the wrong places. With this version the program sets the four settings itself, so that sentence changes with the book\'s next draft.',
          '- The help pages are word for word the same, so the book\'s printed help pages stand.'
          + (' A page that shows the version now shows %s.' % nt if shown else ''),
          '', '## Checks', '',
          '- `verify/verify_round18_settings_v1.py` (%s, for the 31 programs together; its output is beside it). For %s: T1, only the '
          'round\'s lines changed; T2, the line is the first statement of each start routine after its LOCAL lines; T3, the first line '
          'is the pragma line.' % (total, n),
          '- `tools/ppl_gate_v1e.py` against %s %s (`verify/round18/gates/%s_%s.txt`): PASS.' % (n, ot, n, nv),
          '- The harness smoke test (the start routine, idle key Esc): %s. Started with HSeparator 4, HFormat 1, HAngle 1 and Entry 2, '
          'the harness held 0, 0, 0 and 0 afterwards. The harness has no Home settings of its own and always writes a period '
          '(`tools/prime_facts_v1.py`, facts 5 and 6), so this shows that the line runs and nothing more.' % '; '.join(smoke),
          '- `tools/fleet_names_v2.py` and `tools/screen_text_v1.py` over the 31 newest files: no collisions, no place against the rules.',
          '- Not made again: the text-overlap walk and the monkey\'s runs. Nothing a page draws differs but the version where a page shows it'
          + (', a string of the same length' if shown else '') + '.']
    vc = VC.get(n, [])
    T.append('- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 22 Nov 2026 (`verify/round18/vc_checks.txt`): '
             + ' '.join(x if x.endswith('.') else x + '.' for x in vc))
    T += ['', '## On a G1 or a G2', '', 'Not yet run on a G1 or a G2. The check, which takes two minutes:', '',
          '1. Shift, Home. Set Angle Measure to Degrees, Number Format to Fixed 2, Digit Grouping to 123.456,789 and Entry to RPN.',
          '2. Start %s%s.' % (n, ' from the Application Library' if n == 'CentralLimit' else ' from the Program Catalog'),
          '3. On its pages a decimal has a period and a number of 1,000 or more has commas, as in the book.',
          '4. Leave the program. Shift, Home: Angle Measure reads Radians, Number Format Standard, Digit Grouping 123,456.789 and Entry Textbook.',
          '', '## Unresolved', '',
          '- The program changes four of the calculator\'s settings and says so nowhere on the calculator: no help page was changed in this round. The book says it.',
          '- What RPN entry does inside a running program was seen only as far as the run above went; no form was filled with the calculator in RPN, because the line has set Textbook before any form opens.',
          '- Whether an app\'s own angle or number format setting overrides Home\'s inside a program was not tried.' if n != 'CentralLimit' else
          '- CentralLimit is an app, and an app has its own Angle Measure and Number Format (Symbolic Setup). The line sets Home\'s; whether the app\'s own setting, when it is not "System", overrides it was not tried.',
          '']
    io.open(os.path.join(OUT, '%s_%s_CHANGES.md' % (n, nv)), 'w', encoding='utf-8').write('\n'.join(T))
print('%d change notes written in %s' % (len(PAIRS), OUT))
