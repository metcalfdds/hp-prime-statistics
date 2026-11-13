# -*- coding: utf-8 -*-
"""Round 12 (13 Nov 2026): help-page fixes found in the book's pre-submission read.

The book *Statisticles* prints every program's help pages exactly as the programs show them.  Reading Draft 27 line by
line for submission found wording faults in twelve programs' help pages, and places where Round 11's re-wrap had run a
list's items together (a label and its first item on one line, two keys in one sentence with nothing between them, a
hyphenated name split by a space).  Roger, 13 Nov 2026: "Go ahead and fix the help files as we need to do that in any
case".

Every change is an exact replacement in the version before (read from git, BASE below); a replacement that does not
match exactly once stops the build.  Each program then gets its next version: the header line, a history note, and
every version string in a literal (as Round 11's bump did).  Run from the repository's root:
    python3 verify/round12/make_round12.py OUTDIR
"""
import io, os, re, subprocess, sys, textwrap

BASE = '2f7bc7c'                     # main before Round 12
DATE = '13 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r12_programs'

EDITS = {
 'TTestLab': ('beta1i', 'beta1j', [
   (' tt_Frame("Which t-test?  (Figure 11.2)");', ' tt_Frame("Which t-test?");'),
   ('{"Choose the test (Figure 11.2)",', '{"Choose the test (flowchart)",'),
   (' TEXTOUT_P("are equal, separate if not (Figure 11.2).  Many",G1,8,173,1,ttGRAY);',
    ' TEXTOUT_P("are equal, separate if not.  Many",G1,8,173,1,ttGRAY);')],
   'The figure number of the lecture note (Figure 11.2) is gone from the menu item (now "Choose the test (flowchart)", '
   'as in TTestLabG), the flowchart\'s title and the pooled-or-separate note: in the book, Figure 11.2 is a different '
   'picture.'),
 'DataLoad': ('beta1f', 'beta1g', [
   ('TEXTOUT_P("copy the file into Documents\\\\HP Prime\\\\", G1, 8, 82, 1, ddBLK);',
    'TEXTOUT_P("copy the file into Documents > HP Prime >", G1, 8, 82, 1, ddBLK);'),
   ('TEXTOUT_P("Calculators\\\\Prime, start it, run DataLoad.", G1, 8, 95, 1, ddBLK);',
    'TEXTOUT_P("Calculators > Prime, start it, run DataLoad.", G1, 8, 95, 1, ddBLK);')],
   'Help page 2/3 writes the Virtual Calculator\'s folder as Documents > HP Prime > Calculators > Prime.  The doubled '
   'backslashes of beta 1f may or may not print as one on the calculator (a backslash in a string is untested, Lessons '
   'Learned v7zq); the book printed them doubled.'),
 'StatDist': ('v2.7l', 'v2.7m', [
   ('"Gallery: tap a family (or arrows), Then two menus:",', '"Gallery: tap a family (or arrows), then two menus:",')],
   'Help page 1/4: "then", not "Then", after a comma.'),
 'SampDist': ('v2.3j', 'v2.3k', [
   ('  TEXTOUT_P("Watch sample means 40 simulated means fall onto the axis, then", G1, 6, 149, 1, hBl);\n'
    '  TEXTOUT_P("   become a histogram under the curve.", G1, 6, 160, 1, hBl);',
    '  TEXTOUT_P("Watch sample means", G1, 6, 149, 1, hBl);\n'
    '  TEXTOUT_P("   40 simulated means fall onto the axis, then become a", G1, 6, 160, 1, hBk);\n'
    '  TEXTOUT_P("   histogram under the curve.", G1, 6, 171, 1, hBk);'),
   ('  TEXTOUT_P("Soft keys n− n+  step n through 1, 2, 4 ... 400 n×4  quadruples n:", G1, 6, 69, 1, hBl);\n'
    '  TEXTOUT_P("   σ" + CHAR(57344) + " halves μ,σ  edit;  Tail  the next kind of region (left, right,", G1, 6, 80, 1, hBl);\n'
    '  TEXTOUT_P("   between, outside);  Menu", G1, 6, 91, 1, hBl);\n'
    '  TEXTOUT_P("Touch drag in the plot: the nearer bound moves ⇆ nudge it, ⇅", G1, 6, 105, 1, hBl);\n'
    '  TEXTOUT_P("   the other bound, +/- = n, Ent = more, Esc = menu", G1, 6, 116, 1, hBl);\n'
    '  TEXTOUT_P("Compare sample sizes drag = a cursor with P(" + CHAR(57344) + " < x) for each n;", G1, 6, 130, 1, hBl);\n'
    '  TEXTOUT_P("   tap a curve to pick it.", G1, 6, 141, 1, hBk);\n'
    '  TEXTOUT_P("Critical values: changing n moves them; α stays the same.", G1, 6, 155, 1, hMg);',
    '  TEXTOUT_P("Soft keys", G1, 6, 69, 1, hBl);\n'
    '  TEXTOUT_P("   n− n+  step n through 1, 2, 4 ... 400", G1, 6, 80, 1, hBk);\n'
    '  TEXTOUT_P("   n×4  quadruples n: σ" + CHAR(57344) + " halves", G1, 6, 91, 1, hBk);\n'
    '  TEXTOUT_P("   μ,σ  edit;  Tail  the next kind of region (left, right,", G1, 6, 102, 1, hBk);\n'
    '  TEXTOUT_P("   between, outside);  Menu  back to the menu", G1, 6, 113, 1, hBk);\n'
    '  TEXTOUT_P("Touch", G1, 6, 127, 1, hBl);\n'
    '  TEXTOUT_P("   drag in the plot: the nearer bound moves", G1, 6, 138, 1, hBk);\n'
    '  TEXTOUT_P("   ⇆ nudge it, ⇅ the other bound, +/- = n, Ent = more, Esc = menu", G1, 6, 149, 1, hBk);\n'
    '  TEXTOUT_P("Compare sample sizes", G1, 6, 163, 1, hBl);\n'
    '  TEXTOUT_P("   drag = a cursor with P(" + CHAR(57344) + " < x) for each n; tap a curve to pick it.", G1, 6, 174, 1, hBk);\n'
    '  TEXTOUT_P("Critical values: changing n moves them; α stays the same.", G1, 6, 188, 1, hMg);')],
   'Help pages 1/2 and 2/2 are lists again: Round 11\'s re-wrap had put "Watch sample means", "Soft keys", "Touch" and '
   '"Compare sample sizes" on one line with their first item, and run the soft keys together.  Each label is on a line of '
   'its own, in blue, with its items indented below it in black, as page 1\'s other three items are; Menu says what it '
   'does.'),
 'CICatcher': ('beta2i', 'beta2j', [
   ('"s changes from sample to sample, so t lines differ in length, so",',
    '"s changes from sample to sample, so t lines differ in length.",')],
   'Help page 2/6: two sentences where one had "so ... so".'),
 'PowerViz': ('v2.5r', 'v2.5s', [
   (' TEXTOUT_P("sideways near H₁ = move the alternative the dashed red line = set",G1,12,43,1,cblk);\n'
    ' TEXTOUT_P("α by hand; when you lift your finger, α jumps to the nearest of",G1,12,56,1,cblk);\n'
    ' TEXTOUT_P("those values if it is within 15 % of it up or down = change n (one",G1,12,69,1,cblk);\n'
    ' TEXTOUT_P("step for every 12 pixels)",G1,12,82,1,cblk);\n'
    ' TEXTOUT_P("TAP THE READOUT:",G1,12,98,1,cnul);\n'
    ' TEXTOUT_P("n = type n;  μ, p, d or h = type the effect",G1,12,111,1,cblk);',
    ' TEXTOUT_P("sideways near H₁ = move the alternative",G1,12,43,1,cblk);\n'
    ' TEXTOUT_P("the dashed red line = set α by hand; when you lift your",G1,12,56,1,cblk);\n'
    ' TEXTOUT_P("  finger, α jumps to the nearest of the seven α values",G1,12,69,1,cblk);\n'
    ' TEXTOUT_P("  (0.001 to 0.2) if it is within 15 % of it",G1,12,82,1,cblk);\n'
    ' TEXTOUT_P("up or down = change n (one step for every 12 pixels)",G1,12,95,1,cblk);\n'
    ' TEXTOUT_P("TAP THE READOUT:",G1,12,111,1,cnul);\n'
    ' TEXTOUT_P("n = type n;  μ, p, d or h = type the effect",G1,12,124,1,cblk);')],
   'Help page 3/7: the three drags are three lines again (Round 11\'s re-wrap had run them into one sentence), and "the '
   'nearest of those values", which had nothing before it to point to, is "the nearest of the seven α values (0.001 '
   'to 0.2)", the values page 4 steps through.'),
 'FitCheck': ('beta1f', 'beta1g', [
   ('In the two-digit test numbers below 10 are left out', 'In the two-digit test, numbers below 10 are left out')],
   'Help page 4/8: a comma after "In the two-digit test".'),
 'RankLab': ('beta1g', 'beta1h', [
   ('      hlL := {"Up / Down = the previous / next page Left / Right = pick the next",\n'
    '        "dot, group, cell, point or pair (on the Null page: move the",\n'
    '        "read-out line); on Result: turn pages + = the 4th soft key",\n'
    '        "(Exact/Normal, ranks/values, rs/tau-b);  - = Tails: two-sided,",\n'
    '        "lower, upper 0 = this help;  Enter = a menu of every action",',
    '      hlL := {"Up / Down = the previous / next page",\n'
    '        "Left / Right = pick the next dot, group, cell, point or pair",\n'
    '        "  (on the Null page: the read-out line; on Result: turn pages)",\n'
    '        "+ = the 4th soft key (Exact/Normal, ranks/values, rs/tau-b)",\n'
    '        "- = Tails: two-sided, lower, upper",\n'
    '        "0 = this help;  Enter = a menu of every action",'),
   ('"Judges: 43 judges (blocks) x 3 criteria. Halo preset: the same 8",\n'
    '        "judges ranked on 11 criteria; W only, no p (the same lawyers",',
    '"Judges: 43 judges (blocks) x 3 criteria. Halo preset: the first 8",\n'
    '        "of those judges on 11 criteria; W only, no p (the same lawyers",'),
   ('    // every non-empty column is a group\n'
    '    rkGV := {}; rkGG := {}; rkGNm := {}; myK := 0;\n'
    '    FOR myC FROM 1 TO 9 DO\n'
    '      myL := rk_ReadD(myC);\n'
    '      IF SIZE(myL) > 0 THEN\n'
    '        myK := myK + 1;\n'
    '        rkGV := CONCAT(rkGV, myL);\n'
    '        rkGG := CONCAT(rkGG, rk_Fill(myK, SIZE(myL)));\n'
    '        rkGNm := CONCAT(rkGNm, {"D" + rk_Cm(STRING(myC, 2, 0))});\n'
    '      END;\n'
    '    END;\n'
    '    IF myK < 2 THEN\n'
    '      MSGBOX("Put each group in its own column, D1, D2, ... of the Statistics 1Var app (at least two columns).");\n'
    '      RETURN 0;\n'
    '    END;\n'
    '    rkGK := myK;',
    '    // every non-empty column is a group.  Round 12 (the monkey, base 12): the columns are read into myA, myB\n'
    '    // and myM first, and the groups change only when there are two or more, so a refused read changes\n'
    '    // nothing (beta 1g emptied the groups but kept rkGK, and Mann-Whitney then indexed a missing name).\n'
    '    myA := {}; myB := {}; myM := {}; myK := 0;\n'
    '    FOR myC FROM 1 TO 9 DO\n'
    '      myL := rk_ReadD(myC);\n'
    '      IF SIZE(myL) > 0 THEN\n'
    '        myK := myK + 1;\n'
    '        myA := CONCAT(myA, myL);\n'
    '        myB := CONCAT(myB, rk_Fill(myK, SIZE(myL)));\n'
    '        myM := CONCAT(myM, {"D" + rk_Cm(STRING(myC, 2, 0))});\n'
    '      END;\n'
    '    END;\n'
    '    IF myK < 2 THEN\n'
    '      MSGBOX("Put each group in its own column, D1, D2, ... of the Statistics 1Var app (at least two columns).");\n'
    '      RETURN 0;\n'
    '    END;\n'
    '    rkGV := myA; rkGG := myB; rkGNm := myM;\n'
    '    rkGK := myK;')],
   'Help page 2/7: one key per line again (Round 11\'s re-wrap had run "Up / Down" into "Left / Right", "turn pages" '
   'into "+", and "upper" into "0").  Help page 5/7: the halo preset is "the first 8 of those judges", the 43 judges '
   'of the line before, which "the same 8 judges" did not say.  And a fix the monkey found (base 12, 3 of 1,000 runs): '
   'Your data > Groups with fewer than two columns filled emptied the groups but kept the old group count, so a '
   'Mann-Whitney after it asked for a group name that was not there ("index out of range" in rk_ChooseG).  The columns '
   'are now read into locals, and the groups change only when there are two or more.'),
 'AnovaLab': ('beta1f', 'beta1g', [
   ('av_Tx("Scheffe: covers every contrast, widest CIs.", 10, 30, avBLUE);',
    'av_Tx("Scheff" + CHAR(233) + ": covers every contrast, widest CIs.", 10, 30, avBLUE);')],
   'Help page 4/9: Scheffé with its accent (CHAR(233); GlyphProbe_v1 measured it, Round 11).  The menus keep '
   '"Scheffe".'),
 'EpiStats': ('v1.7k', 'v1.7l', [
   ('"rates, stratified (Mantel- Haenszel) analysis, and sample size.",',
    '"rates, stratified (Mantel-Haenszel) analysis, and sample size.",'),
   ('"NPV = spec(1-p) / (spec(1-p) + (1-sens)p) A rare disease makes",\n'
    '         "most positives false.",',
    '"NPV = spec(1-p) / (spec(1-p) + (1-sens)p)",\n'
    '         "A rare disease makes most positives false.",')],
   'Help page 1/15: "Mantel-Haenszel" in one piece (Round 11\'s re-wrap had left a space after the hyphen).  Help page '
   '11/15: the NPV formula ends its line, and "A rare disease makes most positives false." starts the next.'),
 'RiskLab': ('beta1f', 'beta1g', [
   ('or a penalised",', 'or a penalized",')],
   'Help page 2/8: "penalized", in American spelling.'),
 'BayesTree': ('beta8j', 'beta8k', [
   ('               "Soft keys: More (the 6th key) shows the next set of keys: Values",\n'
    '               "  Counts ROC PPV 2×2 | Diag Fagan Icons 3 prev Help | Test2",\n'
    '               "  Reset Forens Leaves Exact.",\n'
    '               "⇆ = spec, ⇅ = sens, +/- = prior, Ent = menu, Esc quits",\n'
    '               "BayesTree."};',
    '               "Soft keys: More (the 6th key) shows the next set of keys:",\n'
    '               "  Values, Counts, ROC, PPV, 2×2",\n'
    '               "  Diag, Fagan, Icons, 3 prev, Help",\n'
    '               "  Test 2, Reset, Forens, Leaves, Exact",\n'
    '               "⇆ = spec, ⇅ = sens, +/- = prior, Ent = menu,",\n'
    '               "Esc quits BayesTree."};')],
   'Help page 2/5: the three sets of soft keys on lines of their own, each key named as its label reads ("Test 2", not '
   '"Test2"), and "Esc quits BayesTree." in one piece.'),
}


def tag(v):
    return v.replace('beta', 'beta ')


def die(msg):
    sys.exit('BUILD STOPPED: ' + msg)


def bump(name, s, ov, nv, note):
    """Round 11's bump: the header line, a history note before the old version's, and every version string in a literal."""
    ot, nt = tag(ov), tag(nv)
    L = s.split('\n')
    hv = None
    for i, l in enumerate(L[:40]):
        if re.match(r'^//\s*[A-Za-z0-9 ]+ - ' + re.escape(ot) + r'\b', l):
            hv = i
            break
    if hv is not None:
        L[hv] = L[hv].replace(ot, nt)
        L[hv] = re.sub(r'\((\d+ Nov 2026[^)]*)\)', '(%s)' % DATE, L[hv], count=1)
    hist = [i for i, l in enumerate(L) if re.match(r'^//\s*' + re.escape(ot) + r'\s*\(', l)]
    if not hist:
        die(name + ': no history line for ' + ot)
    body = ('Round 12: help-page fixes from the book\'s pre-submission read (Roger, 13 Nov 2026: "Go ahead and fix the '
            'help files").  ' + note + '  No other line changed.')
    L.insert(hist[0], '// %s (%s): ' % (nt, DATE) + '\n//   '.join(textwrap.wrap(body, 100)))
    s = '\n'.join(L)
    s = re.sub(r'"[^"\n]*"', lambda m: m.group(0).replace(ot, nt).replace(ov, nv), s)
    # a version on screen with its date: the new date (Round 11's bump did the same)
    s = re.sub(r'"[^"\n]*%s[^"\n]*"' % re.escape(nt), lambda m: re.sub(r'\b\d{1,2} Nov 2026', DATE, m.group(0)), s)
    return s


def old_text(name, ov):
    return subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (BASE, name, ov)], check=True,
                          capture_output=True).stdout.decode('utf-8')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, (ov, nv, eds, note) in EDITS.items():
        s = old_text(name, ov)
        for a, b in eds:
            n = s.count(a)
            if n != 1:
                die('%s: %d matches for %r' % (name, n, a[:80]))
            s = s.replace(a, b)
        s = bump(name, s, ov, nv, note)
        io.open(os.path.join(OUT, '%s_%s.txt' % (name, nv)), 'w', encoding='utf-8', newline='').write(s)
        print('%-10s %s -> %s  (%d changes)' % (name, ov, nv, len(eds)))
