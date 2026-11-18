# FitCheck beta 1j: changes (17 November 2026)

Round 17 of 17 November 2026: the words on the screen. Roger, reading Draft 46 of the book that morning: "The p-value and t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". The book prints every program's help pages word for word, so the programs' own text had to follow; asked whether now or later, he answered "Now, as Round 17". A calculator's screen has no italics, so a program keeps the rest of each rule: a hyphen joins a statistic's letter to its noun (F-test, t-table, z-values), an expression like n - 1 stands in parentheses of its own (df = (n - 1)), and the p of p-value is a small letter. `tools/screen_text_v1.py` is the check: before the round it found 116 places in 16 programs (the quoted strings and the texts the generic walks drew; `verify/round17/screen_text_before.txt`), and now none. The build is `verify/round17/make_round17.py`: each change is an exact replacement inside a quoted string of FitCheck beta 1i (a replacement that is not found the number of times the build names stops it), then the version (header, history note, version strings).

## What changed

1. The degrees of freedom stand in parentheses wherever a page writes them out: "df = (k-1-m)" (the curve page, in both of its forms, the working lines of the test page, and help), "df = (k-2)", "df = (k-1)" and "df = (k-3)" (the working lines of the Poisson, binomial and normal fits, the two notes of a normal fit to bins, two data-source pages, and help).  They are written without spaces because most of these sentences flow from line to line, and the wrap breaks a line at a space: the old "df = k - 3" could end one line at "k -" and begin the next with "3."; "(k-3)" stays whole.  For the same reason the note on raw values in bins writes "chi-square(k-3) and chi-square(k-1)".  One help sentence was turned so that no parenthesis stands inside another: "BINOMIAL: p estimated, df = (k-2); typed, df = (k-1)."  No text is longer than it was, so no page gains a line.

| Line | Routine | It said | It says |
|---|---|---|---|
| 1267 | `fc_RawBins` | (k - 3) and  ... (k - 1) (Chernoff & Lehmann 1954); df = k - 3 is the usual textbook rule. | (k-3) and  ... (k-1) (Chernoff & Lehmann 1954); df = (k-3) is the usual textbook rule. |
| 1931 | `fc_DrawCurve` | df = k - 1 - m =  | df = (k-1-m) =  |
| 1990 | `fc_DrawCurve` | df = k - 1 - m =  | df = (k-1-m) =  |
| 2022 | `fc_TestLines` | df = k - 1 - m =  | df = (k-1-m) =  |
| 2079 | `fc_TestLines` |  K), so the E add up to N.  One parameter estimated: df = k - 2. |  K), so the E add up to N.  One parameter estimated: df = (k-2). |
| 2083 | `fc_TestLines` | : one parameter estimated, df = k - 2. | : one parameter estimated, df = (k-2). |
| 2085 | `fc_TestLines` |  was given, not estimated: df = k - 1. |  was given, not estimated: df = (k-1). |
| 2089 | `fc_TestLines` | .  Each cell's E = N (normal CDF at its upper edge - at its lower edge); the end cells are open.  Two parameters estimated: df = k - 3. | .  Each cell's E = N (normal CDF at its upper edge - at its lower edge); the end cells are open.  Two parameters estimated: df = (k-3). |
| 2851 | `fc_NorBins` |  bins); the cells are the bins, so the estimates and the cells match and df = k - 3. |  bins); the cells are the bins, so the estimates and the cells match and df = (k-3). |
| 3276 | `fc_PreCrim` |  fit on the bins (Bins key): the sparse tails are merged, df = k - 3. |  fit on the bins (Bins key): the sparse tails are merged, df = (k-3). |
| 3383 | `fc_PreBinIll` | p is estimated from the data, so df = k - 2. | p is estimated from the data, so df = (k-2). |
| 3639 | `fc_Help` | /E: big when the counts are far from E.  df = k - 1 - m, where m counts the parameters estimated from the same data (Poisson  | /E: big when the counts are far from E.  df = (k-1-m), where m counts the parameters estimated from the same data (Poisson  |
| 3649 | `fc_Help` |  is estimated as the mean count; the last cell is the tail (K or more), so the E add up to N; df = k - 2.  BINOMIAL: p estimated (df = k - 2) or typed (df = k - 1). |  is estimated as the mean count; the last cell is the tail (K or more), so the E add up to N; df = (k-2).  BINOMIAL: p estimated, df = (k-2); typed, df = (k-1). |
| 3653 | `fc_Help` |  on bins: df = k - 3.   |  on bins: df = (k-3).   |

2. **Nothing else changed.** With every quoted string taken out, the code of FitCheck beta 1i and of FitCheck beta 1j is the same line for line. The other differences are the header and its history note (lines 17-30), and the version the program shows (1 line of code).

## For the book

- The book prints the help pages word for word. 3 of the 12 help screens changed: "FitCheck help 2/12: Goodness of fit", "FitCheck help 4/12: Benford, Poisson, binomial", "FitCheck help 5/12: Normality". `helppages.json` takes them with the book's next draft.
- None of the book's screen captures of FitCheck shows a wording that changed: the figures of the sixteen programs were read for the changed lines, and the two that showed one (Figures 11.3 and 13.4) were taken again.

## Checks

- `verify/verify_round17_screen_text_v1.py` (160 checks, 0 failed, for the sixteen programs together; its output is beside it). For FitCheck: the build makes this file byte for byte; of its 3,029 lines of code 15 differ, each only inside quotation marks; with the round's replacements made in the old help pages, the two versions' 12 help screens read the same, and nothing on them is cut or overlaps at the glyph widths GlyphProbe_v1 measured on the Virtual Calculator; **every changed text was seen on a screen of the new version** ("(k-3) and χ²(k-1) (Chernoff" 2 times; "df = (k-1-m)" 160 times; "p estimated, df = (k-2); typed, df = (k-1)." 5 times; "df = (k-2)" 13 times; "df = (k-1)." 5 times; "df = (k-3)" 27 times); the tightest of them has 88 px to spare in its line; and over 30 seeds of the monkey the old and the new version show the same 900 screens and 243 boxes, menus and forms, text for text once the replacements are made (76 screens whose text flows were compared as running text) (runs that ended OK: 30).
- `tools/ppl_gate_v1e.py` against FitCheck beta 1i (`verify/round17/gates/FitCheck_beta1j.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 10 reports, as in FitCheck beta 1i; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round17/helpcheck_r17.json` (Round 11's `helpcheck_r11.py`): 12 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`, the new version beside the old (`verify/round17/overlap_FitCheck.txt`): the same report.
- The monkey's 1,000 runs were not made again: nothing the calculator runs differs but the words it shows, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 17 Nov 2026: Program Catalog > Edit > Check said "No errors in the program" (`verify/round17/vc_checks.txt`). The program was not run there in this round.

## On a G1 or a G2

Not yet run on a G1 or a G2. Only words on the screen changed, and the version the opening page shows; the program should behave exactly as beta 1i.
