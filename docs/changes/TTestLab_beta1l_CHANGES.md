# TTestLab beta 1l: changes (17 November 2026)

Round 17 of 17 November 2026: the words on the screen. Roger, reading Draft 46 of the book that morning: "The p-value and t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". The book prints every program's help pages word for word, so the programs' own text had to follow; asked whether now or later, he answered "Now, as Round 17". A calculator's screen has no italics, so a program keeps the rest of each rule: a hyphen joins a statistic's letter to its noun (F-test, t-table, z-values), an expression like n - 1 stands in parentheses of its own (df = (n - 1)), and the p of p-value is a small letter. `tools/screen_text_v1.py` is the check: before the round it found 116 places in 16 programs (the quoted strings and the texts the generic walks drew; `verify/round17/screen_text_before.txt`), and now none. The build is `verify/round17/make_round17.py`: each change is an exact replacement inside a quoted string of TTestLab beta 1k (a replacement that is not found the number of times the build names stops it), then the version (header, history note, version strings).

## What changed

1. Step 2 writes "Pooled variances:  df = (N1 + N2 - 2)" and "One sample:  df = (N - 1)"; step 3 says "t-table, row df = ..."; help 3 of 3 says "df = (N - 1)" (they said "df = N1 + N2 - 2", "df = N - 1", "t table").

| Line | Routine | It said | It says |
|---|---|---|---|
| 1060 | `tt_Step2` | Pooled variances:  df = N ...  - 2 | Pooled variances:  df = (N ...  - 2) |
| 1090 | `tt_Step3` | t table, row df =  | t-table, row df =  |
| 1356 | `tt_Step2N` | One sample:  df = N - 1 | One sample:  df = (N - 1) |
| 2069 | `tt_Help` |  - μ₀)/(s/√N), df = N - 1.  Type the mean, SD and N, |  - μ₀)/(s/√N), df = (N - 1).  Type the mean, SD and N, |

2. **Nothing else changed.** With every quoted string taken out, the code of TTestLab beta 1k and of TTestLab beta 1l is the same line for line. The other differences are the header and its history note (line 4; lines 21-27); the program shows no version on its pages.

## For the book

- The book prints the help pages word for word. One of the 3 help screens changed: "TTestLab help 3/3: One sample, proportions". `helppages.json` takes them with the book's next draft.
- The book's Figure 11.3, step 3 of the age-at-arrest example, showed "t table, row df = 60". It was taken again on the Virtual Calculator (`verify/round17/screens/TTestLab_crit.png`; the book prints it enlarged three times). No other capture of TTestLab in the book shows a changed wording.

## Checks

- `verify/verify_round17_screen_text_v1.py` (160 checks, 0 failed, for the sixteen programs together; its output is beside it). For TTestLab: the build makes this file byte for byte; of its 1,640 lines of code 4 differ, each only inside quotation marks; with the round's replacements made in the old help pages, the two versions' 3 help screens read the same, and nothing on them is cut or overlaps at the glyph widths GlyphProbe_v1 measured on the Virtual Calculator; **every changed text was seen on a screen of the new version** ("df = (N₁ + N₂ - 2)" 2 times; "t-table, row df" 100 times; "df = (N - 1)" 9 times); the tightest of them has 24 px to spare in its line; and over 30 seeds of the monkey the old and the new version show the same 805 screens and 117 boxes, menus and forms, text for text once the replacements are made (runs that ended OK: 30).
- `tools/ppl_gate_v1e.py` against TTestLab beta 1k (`verify/round17/gates/TTestLab_beta1l.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 4 reports, as in TTestLab beta 1k; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round17/helpcheck_r17.json` (Round 11's `helpcheck_r11.py`): 3 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`, the new version beside the old (`verify/round17/overlap_TTestLab.txt`): the same report.
- The monkey's 1,000 runs were not made again: nothing the calculator runs differs but the words it shows, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 17 Nov 2026: Program Catalog > Edit > Check said "No errors in the program" (`verify/round17/vc_checks.txt`). After the checked file had been collected the program was run there, for the book's Figure 11.3: the age-at-arrest example, step 2 ("Pooled variances:  df = (N₁ + N₂ - 2)", then "= 44 + 31 - 2 = 73") and step 3 ("t-table, row df = 60:  t crit = ±2.000"; exact, df = 73: ±1.993), the numbers of the capture before (`verify/round17/screens/TTestLab_df.png`, `TTestLab_crit.png`). Each line ends 1 to 2 px short of where the glyph widths put it.

## On a G1 or a G2

Not yet run on a G1 or a G2. Only words on the screen changed; the program should behave exactly as beta 1k.
