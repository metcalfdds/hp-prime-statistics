# -*- coding: utf-8 -*-
"""make_changes_r17.py -- docs/changes/<Name>_<version>_CHANGES.md for the sixteen versions of Round 17 (the words on the
screen in the book's house form for a statistic's letter), from the round's own records: the build
(make_round17.EDITS), the old and the new program (what each changed line said and says), the two help dumps, the gate
reports, the checks, the verify script's output and the Virtual Calculator's Check log, all in this folder or beside
it.  Made from round16/make_changes_r16.py.  Run from the repository's root, after records_r17.py and the verify
script:
    python3 verify/round17/make_changes_r17.py ."""
import io, os, re, sys, json, difflib, subprocess, importlib.util
REPO = os.path.abspath(sys.argv[1]); H = os.path.dirname(os.path.abspath(__file__)); os.chdir(REPO)
spec = importlib.util.spec_from_file_location('m17', os.path.join(H, 'make_round17.py')); m17 = importlib.util.module_from_spec(spec)
sys.argv = ['x', '/dev/null']; spec.loader.exec_module(m17)
HO = json.load(open(os.path.join(H, 'helppages_before_r17.json'), encoding='utf-8')); HN = json.load(open(os.path.join(H, 'helppages_r17.json'), encoding='utf-8'))
HC = json.load(open(os.path.join(H, 'helpcheck_r17.json'), encoding='utf-8'))
VC = {l.split()[0]: l for l in open(os.path.join(H, 'vc_checks.txt'), encoding='utf-8') if 'No errors in the program' in l and '|' in l}
CK = open(os.path.join(H, 'checks_r17.txt'), encoding='utf-8').read()
WV = open(os.path.join(REPO, 'verify', 'verify_round17_screen_text_v1_output.txt'), encoding='utf-8').read()
NCHECK = re.search(r'(\d+) of (\d+) checks PASS', WV); assert NCHECK and NCHECK.group(1) == NCHECK.group(2), NCHECK
BEFORE = open(os.path.join(H, 'screen_text_before.txt'), encoding='utf-8').read().strip().split('\n')[-1]
NBEFORE = re.search(r'places against the rules: (\d+) in (\d+) programs', BEFORE).groups(); assert NBEFORE == ('116', '16'), NBEFORE
PROGS = dict((n, (e[0], e[1], e[3])) for n, e in m17.EDITS.items())
PROGS['TTestLabG'] = ('beta1h', 'beta1i',
                      'Step 2 writes "Pooled variances:  df = (N1 + N2 - 2)", "One sample:  df = (N - 1)" and, for separate variances, '
                      '"By hand: df = the smaller of (N1-1), (N2-1) = ..."; help 3 of 3 says "df = (N - 1)" (they said "df = N1 + N2 - 2", '
                      '"df = N - 1", "the smaller of N1-1, N2-1").')
# the standing report of the help layout check, as verify/round11/README.md explains it
KNOWN = {'AgreeLab': ('one known report, as in Rounds 11 and 16: the d̄ drawn on help page 7 (the check measures the bar\'s d as a '
                      'plain letter beside the next text; the Virtual Calculator shows the line correctly)')}
# what the book prints by name
BOOK = {
 'AnovaLab': 'Three menu items have a hyphen now and keep their numbers: "F-curve and p" (One-way ANOVA, item 3), "F-curve of an effect" (Two-way ANOVA, item 3) and "F-curve (treatments)" (Randomized blocks, item 3).',
 'StudRange': 'The main menu\'s first item reads "p-value from q" and keeps its number.',
 'TestChooser': 'Test 9 is named "Cochran\'s Q-test" wherever the program names it: the flowchart, the table, the details page, the quiz and the line the program returns.',
}
# the book's captures that showed a changed wording (verify/round17/README.md, "For the book")
CAPTURE = {
 'TTestLab': 'The book\'s Figure 11.3, step 3 of the age-at-arrest example, showed "t table, row df = 60". It was taken again on the Virtual Calculator '
             '(`verify/round17/screens/TTestLab_crit.png`; the book prints it enlarged three times). No other capture of TTestLab in the book shows a changed wording.',
 'ScatterLab': 'The book\'s Figure 13.4, the Inference page of the synthetic example, showed "df = n-2 = 14". It was taken again on the Virtual Calculator '
               '(`verify/round17/screens/ScatterLab_inference.png`; the book prints it enlarged three times). No other capture of ScatterLab in the book shows a changed wording.',
 'TTestLabG': 'The book\'s one capture of TTestLabG, its flowchart (Figure 11.5), shows no wording that changed.',
}
STRING = re.compile(r'"((?:[^"\\]|\\.)*)"')
# what was seen on the Virtual Calculator beyond the Check (verify/round17/vc_checks.txt, section 2)
SEEN = {
 'TTestLab': 'After the checked file had been collected the program was run there, for the book\'s Figure 11.3: the age-at-arrest example, step 2 '
             '("Pooled variances:  df = (N₁ + N₂ - 2)", then "= 44 + 31 - 2 = 73") and step 3 ("t-table, row df = 60:  t crit = ±2.000"; exact, df = 73: ±1.993), '
             'the numbers of the capture before (`verify/round17/screens/TTestLab_df.png`, `TTestLab_crit.png`). Each line ends 1 to 2 px short of where the glyph widths put it.',
 'ScatterLab': 'After the checked file had been collected the program was run there, for the book\'s Figure 13.4: the Inference page of the synthetic example reads '
               '"ŷ = 16.64 + 1.020 x,  n = 16,  df = (n - 2) = 14", and every number is the one in the capture of beta 2l (`verify/round17/screens/ScatterLab_inference.png`).',
 'PowerViz': 'After the checked file had been collected the program was run there for the round\'s tightest changed line: on help 5 of 7, "... the program puts in the '
             'z-values (PPL), giving" stands whole, its last dark pixel at x = 312 of 320, where the glyph widths put its end at 313 (`verify/round17/screens/PowerViz_help5.png`).',
 'TDist3D': 'After the checked file had been collected the program was run there: the opening page shows "Every t-curve at once: t runs across, the degrees", and help 1 of 4 '
            'shows "Student\'s t has one parameter: degrees of freedom, ν = (n − 1)." whole in its box, ending at x = 295 of 308 (`verify/round17/screens/TDist3D_welcome.png`, '
            '`TDist3D_help1.png`).',
}


def walk_parts(t):
    """(distinct screens, screens in all, collisions, firm ones, straddles, overruns, ghosts) of one walk's line"""
    m = re.search(r'screens\s+(\d+)/(\d+)\s+collisions\s+(\d+) \(firm\s+(\d+)\)\s+straddles\s+(\d+)\s+overruns\s+(\d+)\s+ghosts\s+(\d+)', t)
    return tuple(int(x) for x in m.groups())


def walk_says(name):
    """what the two walks of a program say of each other, in one clause; stops at a difference nobody has looked at"""
    t = re.sub(r'\s+', ' ', re.search(r'^T %-10s (.*)$' % re.escape(name), CK, re.M).group(1))
    if t.startswith('same report as the old version'):
        return 'the same report'
    new, old = t.split(' OLD: ')
    a, b = walk_parts(new), walk_parts(old)
    counts = 'collisions %d (firm %d), straddles %d, overruns %d, ghosts %d' % a[2:]
    if a == b:
        return 'the two reports count the same screens and the same findings (%s), and name different texts where the words changed' % counts
    if a[0] == b[0] and a[2:] == b[2:]:
        # the walk stops at its time budget, so the number of screens it gets through depends on the load of the machine
        return ('the two walks found the same %d distinct screens and the same findings (%s); a walk stops at its time budget, and the new '
                'version\'s got through %d screens where the old one\'s got through %d, while two other jobs had the processors' % (a[0], counts, a[1], b[1]))
    if name == 'TTestLabG' and a[:5] == b[:5] and a[6] == b[6] and a[5] == b[5] + 1:
        d = io.open(os.path.join(REPO, 'verify', 'round17', 'overlap_TTestLabG_detail.txt'), encoding='utf-8').read()
        assert 'only in the new version\'s walk: 1' in d and 'only in the old version\'s walk: 0' in d and 'marginal' in d and '225 px wide and ends at x = 233' in d
        return ('the same %d distinct screens, and one more overrun by the walk\'s own estimate (%d where the old version has %d, and the other %d are the old version\'s): '
                '"By hand: df = the smaller of (N₁-1), (N₂-1) = 181," has 50 characters where it had 46, and at the walk\'s 6.5 px a character its right edge is put at 333. '
                'The finding is marginal (not there at 5.5 px a character), and at the calculator\'s glyph widths the line is 225 px wide and ends at x = 233 of 320 '
                '(`verify/round17/overlap_TTestLabG_detail.txt`, written by `walk_detail_r17.py`)' % (a[0], a[5], b[5], b[5]))
    raise AssertionError((name, t))


def routine_of(lines, i):
    for j in range(i, -1, -1):
        mm = re.match(r'^(?:EXPORT |LOCAL )?([A-Za-z_]\w*)\([^)]*\)\s*$', lines[j])
        if mm:
            return mm.group(1)
    return '(header)'


def old_text(name, ov):
    return subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (m17.BASE, name, ov)], check=True, capture_output=True).stdout.decode('utf-8')


def cell(t):
    return t.replace('|', '\\|').replace('`', "'")


for name, (ov, nv, note) in PROGS.items():
    old = old_text(name, ov).split('\n')
    new = io.open(os.path.join(REPO, 'programs', '%s_%s.txt' % (name, nv)), encoding='utf-8').read().split('\n')
    tv, to = m17.tag(nv), m17.tag(ov)
    # the lines of code that differ, old beside new (the new file has more comment lines at its top: pair by code)
    co = [(i, l) for i, l in enumerate(old) if not l.lstrip().startswith('//')]
    cn = [(i, l) for i, l in enumerate(new) if not l.lstrip().startswith('//')]
    assert len(co) == len(cn), name
    rows, vers = [], 0
    for (i, a), (j, b) in zip(co, cn):
        if a == b:
            continue
        sa, sb = STRING.findall(m17.split_comment(a)[0]), STRING.findall(m17.split_comment(b)[0])
        assert STRING.sub('""', m17.split_comment(a)[0]) == STRING.sub('""', m17.split_comment(b)[0]), (name, j + 1)
        ch = [(x, y) for x, y in zip(sa, sb) if x != y]
        if all(x.replace(to, tv).replace(ov, nv) == re.sub(r'\b\d{1,2} Nov 2026', 'DATE', y).replace('DATE', re.search(r'\b\d{1,2} Nov 2026', x).group(0) if re.search(r'\b\d{1,2} Nov 2026', x) else 'DATE')
               or x.replace(to, tv).replace(ov, nv) == y for x, y in ch):
            vers += 1
            continue
        rows.append((j + 1, routine_of(new, j), ' ... '.join(x for x, y in ch), ' ... '.join(y for x, y in ch)))
    comment_hunks = []
    for tag_, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag_ != 'equal' and j2 > j1 and all(l.lstrip().startswith('//') for l in new[j1:j2]):
            comment_hunks.append('line %d' % (j1 + 1) if j2 - j1 <= 1 else 'lines %d-%d' % (j1 + 1, j2))
    built = ('The build is `verify/round17/make_round17.py`: each change is an exact replacement inside a quoted string of %s %s '
             '(a replacement that is not found the number of times the build names stops it), then the version (header, history '
             'note, version strings).' % (name, to)) if name != 'TTestLabG' else (
             'TTestLabG is the general version of TTestLab and is always built from it: `tools/make_tlg1_v4.py` made this file '
             'from TTestLab beta 1l (v3\'s blocks, two lines of which carry this round\'s words: `tools/tlg1_v4_blocks.txt`).')
    o = ['# %s %s: changes (17 November 2026)' % (name, tv), '',
         'Round 17 of 17 November 2026: the words on the screen. Roger, reading Draft 46 of the book that morning: "The p-value and '
         't-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". '
         'The book prints every program\'s help pages word for word, so the programs\' own text had to follow; asked whether now or '
         'later, he answered "Now, as Round 17". A calculator\'s screen has no italics, so a program keeps the rest of each rule: '
         'a hyphen joins a statistic\'s letter to its noun (F-test, t-table, z-values), an expression like n - 1 stands in '
         'parentheses of its own (df = (n - 1)), and the p of p-value is a small letter. `tools/screen_text_v1.py` is the check: '
         'before the round it found %s places in %s programs (the quoted strings and the texts the generic walks drew; '
         '`verify/round17/screen_text_before.txt`), and now none. %s' % (NBEFORE[0], NBEFORE[1], built), '',
         '## What changed', '', '1. ' + note, '',
         '| Line | Routine | It said | It says |', '|---|---|---|---|']
    o += ['| %d | `%s` | %s | %s |' % (ln, r, cell(a), cell(b)) for ln, r, a, b in rows]
    o += ['',
          '2. **Nothing else changed.** With every quoted string taken out, the code of %s %s and of %s %s is the same line for line. '
          'The other differences are the header and its history note (%s)%s.'
          % (name, to, name, tv, '; '.join(comment_hunks) or 'none',
             (', and the version the program shows (%d line%s of code)' % (vers, '' if vers == 1 else 's')) if vers else '; the program shows no version on its pages'), '']
    ch = [k + 1 for k, (a, b) in enumerate(zip(HO.get(name, []), HN.get(name, []))) if a != b]
    assert len(HO.get(name, [])) == len(HN.get(name, [])) > 0, name
    titles = []
    for k in ch:
        t = next((l for l in HN[name][k - 1] if ' help' in l), HN[name][k - 1][0])
        if not any(a != b for a, b in zip(HO[name][k - 1], HN[name][k - 1]) if tv not in b) and len(HO[name][k - 1]) == len(HN[name][k - 1]):
            continue                                                    # only the version line differs
        titles.append('"%s"' % t.strip())
    o += ['## For the book', '',
          ('- The book prints the help pages word for word. %s of the %d help screens changed: %s. `helppages.json` takes them with the '
           'book\'s next draft.' % (('One' if len(titles) == 1 else str(len(titles))), len(HN[name]), ', '.join(titles))) if titles else
          '- No help screen changed, so the pages the book prints stay as they are.']
    if name in BOOK:
        o.append('- ' + BOOK[name])
    o += ['- ' + CAPTURE.get(name, 'None of the book\'s screen captures of %s shows a wording that changed: the figures of the sixteen programs were read '
                                 'for the changed lines, and the two that showed one (Figures 11.3 and 13.4) were taken again.' % name), '']
    g = io.open(os.path.join(H, 'gates', '%s_%s.txt' % (name, nv)), encoding='utf-8').read()
    lint = re.search(r'lint_ppl \(v4\): \d+ checks, (\d+) problems', g)
    hc = HC.get(name)
    t2 = re.search(r'^T2\s+PASS\s+%s: ([\d,]+) lines of code; (\d+) differ' % re.escape(name), WV, re.M)
    t4 = re.search(r'^T4\s+PASS\s+%s: (\d+) help screens' % re.escape(name), WV, re.M)
    t6 = re.findall(r'^T6\s+PASS\s+%s: "(.*?)" shown (\d+) times \((.*?)\)(?:; the tightest: (\d+) px of (\d+), (\d+) to spare)?' % re.escape(name), WV, re.M)
    t6f = re.findall(r'^T6\s+FAIL\s+%s:' % re.escape(name), WV, re.M)
    t7 = re.search(r'^T7\s+PASS\s+%s: (\d+) seeds, (\d+) screens and (\d+) boxes, menus and forms the same text for text( \((\d+) of the screens as running text[^)]*\))? \((.*?)\)' % re.escape(name), WV, re.M)
    assert t2 and t4 and t6 and t7 and not t6f, (name, bool(t2), bool(t4), len(t6), bool(t7), t6f)
    spare = [int(x[5]) for x in t6 if x[5]]
    o += ['## Checks', '',
          '- `verify/verify_round17_screen_text_v1.py` (%s checks, 0 failed, for the sixteen programs together; its output is beside '
          'it). For %s: the build makes this file byte for byte; of its %s lines of code %s differ, each only inside quotation marks; '
          'with the round\'s replacements made in the old help pages, the two versions\' %s help screens read the same, and nothing on '
          'them is cut or overlaps at the glyph widths GlyphProbe_v1 measured on the Virtual Calculator; **every changed text was seen '
          'on a screen of the new version** (%s)%s; and over %s seeds of the monkey the old and the new version show the same %s '
          'screens and %s boxes, menus and forms, text for text once the replacements are made%s (%s).'
          % (NCHECK.group(2), name, '{:,}'.format(int(t2.group(1).replace(',', ''))), t2.group(2), t4.group(1),
             '; '.join('"%s" %s times' % (a, n) for a, n, k, w, l, s in t6),
             ('; the tightest of them has %d px to spare in its line' % min(spare)) if spare else '',
             t7.group(1), '{:,}'.format(int(t7.group(2))), '{:,}'.format(int(t7.group(3))),
             (' (%s screens whose text flows were compared as running text)' % t7.group(5)) if t7.group(5) else '',
             t7.group(6).replace('OK', 'runs that ended OK:')),
          '- `tools/ppl_gate_v1e.py` against %s %s (`verify/round17/gates/%s_%s.txt`): %s. hp-prime-kit lint 0 errors; `lint_ppl` %s '
          'reports, as in %s %s; `fleet_names_v2` over the 31 newest files: no collisions.'
          % (name, to, name, nv, 'PASS' if 'RESULT: PASS' in g else 'FAIL', lint.group(1) if lint else '?', name, to),
          '- `verify/round17/helpcheck_r17.json` (Round 11\'s `helpcheck_r11.py`): %d screens, %s.'
          % (hc['screens'], 'no reports' if not hc['problems'] else KNOWN[name])]
    assert 'RESULT: PASS' in g and (not hc['problems'] or name in KNOWN), name
    sm = re.search(r'^S %-10s .*$' % re.escape(name), CK, re.M)
    tt = re.search(r'^T %-10s .*$' % re.escape(name), CK, re.M)
    assert sm and ' OK ' in sm.group(0) and tt, name
    o.append('- The harness smoke test (main routine, idle key Esc): %s.' % re.sub(r'\s+', ' ', sm.group(0)[13:].strip()))
    o.append('- `tools/text_overlap_v1.py --walk`, the new version beside the old (`verify/round17/overlap_%s.txt`): %s.'
             % (name, walk_says(name)))
    o.append('- The monkey\'s 1,000 runs were not made again: nothing the calculator runs differs but the words it shows, and %s '
             'seeds show the same screens in both versions.' % t7.group(1))
    assert name in VC, name
    o.append('- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 17 Nov 2026: Program Catalog > Edit > Check '
             'said "No errors in the program" (`verify/round17/vc_checks.txt`). %s' % SEEN.get(name, 'The program was not run there in this round.'))
    o += ['', '## On a G1 or a G2', '',
          'Not yet run on a G1 or a G2. Only words on the screen changed%s; the program should behave exactly as %s.'
          % (', and the version the opening page shows' if vers else '', to), '']
    io.open(os.path.join(REPO, 'docs', 'changes', '%s_%s_CHANGES.md' % (name, nv)), 'w', encoding='utf-8').write('\n'.join(o))
    print('%s_%s_CHANGES.md' % (name, nv), len('\n'.join(o).split()), 'words;', len(rows), 'rows;', len(titles), 'help screens')
