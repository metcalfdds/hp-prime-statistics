# AnovaLab beta 1j: changes (17 November 2026)

Round 17 of 17 November 2026: the words on the screen. Roger, reading Draft 46 of the book that morning: "The p-value and t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". The book prints every program's help pages word for word, so the programs' own text had to follow; asked whether now or later, he answered "Now, as Round 17". A calculator's screen has no italics, so a program keeps the rest of each rule: a hyphen joins a statistic's letter to its noun (F-test, t-table, z-values), an expression like n - 1 stands in parentheses of its own (df = (n - 1)), and the p of p-value is a small letter. `tools/screen_text_v1.py` is the check: before the round it found 116 places in 16 programs (the quoted strings and the texts the generic walks drew; `verify/round17/screen_text_before.txt`), and now none. The build is `verify/round17/make_round17.py`: each change is an exact replacement inside a quoted string of AnovaLab beta 1i (a replacement that is not found the number of times the build names stops it), then the version (header, history note, version strings).

## What changed

1. Help 1 of 10: "follows the F-curve with (k - 1) and (N - k) df" (it said "follows the F(k - 1, N - k) curve").  Help 5: "(k - 1) comparisons".  Help 8: "df = (n - 1)" and "df = (n1 - 1) and (n2 - 1)" (they said "df n - 1", "df n1 - 1 and n2 - 1").  "F-test", "F-curve" and "q-distribution" with a hyphen: help 2 of 10, the waiting page of Tukey's studentized range, the band of the two-variance result, and one item in each of the three page menus ("F-curve and p", "F-curve of an effect", "F-curve (treatments)"); the items keep their numbers.

| Line | Routine | It said | It says |
|---|---|---|---|
| 1128 | `av_PrgPage` | The q distribution is an integral, done here | The q-distribution is an integral, done here |
| 3269 | `av_HelpPage` |  is true, F is near 1 and follows the |  is true, F is near 1 and follows the F-curve |
| 3270 | `av_HelpPage` | F(k - 1, N - k) curve; p = P(F this big \|  | with (k - 1) and (N - k) df; p = P(F this big \|  |
| 3279 | `av_HelpPage` | The F test assumes equal spreads (and roughly normal groups). | The F-test assumes equal spreads (and roughly normal groups). |
| 3318 | `av_HelpPage` | group (a placebo, the usual method): k - 1 comparisons, | group (a placebo, the usual method): (k - 1) comparisons, |
| 3363 | `av_HelpPage` | , df n - 1. | , df = (n - 1). |
| 3365 | `av_HelpPage` | , df n ...  - 1 and n ...  - 1. | , df = (n ...  - 1) and (n ...  - 1). |
| 3555 | `av_OMenu` | F curve and p | F-curve and p |
| 3967 | `av_TMenu` | F curve of an effect | F-curve of an effect |
| 4155 | `av_BMenu` | F curve (treatments) | F-curve (treatments) |
| 4242 | `av_VDrawRes` | : the F test and interval | : the F-test and interval |

2. **Nothing else changed.** With every quoted string taken out, the code of AnovaLab beta 1i and of AnovaLab beta 1j is the same line for line. The other differences are the header and its history note (line 17; lines 54-63), and the version the program shows (1 line of code).

## For the book

- The book prints the help pages word for word. 4 of the 10 help screens changed: "AnovaLab help 1/10: What one-way ANOVA asks", "AnovaLab help 2/10: Welch and the checks", "AnovaLab help 5/10: Dunnett's test", "AnovaLab help 8/10: One and two variances". `helppages.json` takes them with the book's next draft.
- Three menu items have a hyphen now and keep their numbers: "F-curve and p" (One-way ANOVA, item 3), "F-curve of an effect" (Two-way ANOVA, item 3) and "F-curve (treatments)" (Randomized blocks, item 3).
- None of the book's screen captures of AnovaLab shows a wording that changed: the figures of the sixteen programs were read for the changed lines, and the two that showed one (Figures 11.3 and 13.4) were taken again.

## Checks

- `verify/verify_round17_screen_text_v1.py` (160 checks, 0 failed, for the sixteen programs together; its output is beside it). For AnovaLab: the build makes this file byte for byte; of its 3,845 lines of code 12 differ, each only inside quotation marks; with the round's replacements made in the old help pages, the two versions' 10 help screens read the same, and nothing on them is cut or overlaps at the glyph widths GlyphProbe_v1 measured on the Virtual Calculator; **every changed text was seen on a screen of the new version** ("The q-distribution is" 2 times; " is true, F is near 1 and follows the F-curv" 15 times; "with (k - 1) and (N - k) df; p = P(F this bi" 15 times; "The F-test assumes" 15 times; "usual method): (k - 1) comparisons" 12 times; ", df = (n - 1)." 29 times; ", df = (n₁ - 1) and (n₂ - 1)." 29 times; "F-curve and p" 11 times; "F-curve of an effect" 10 times; "F-curve (treatments)" 8 times; ": the F-test and interval" 1 times); the tightest of them has 12 px to spare in its line; and over 30 seeds of the monkey the old and the new version show the same 1,296 screens and 216 boxes, menus and forms, text for text once the replacements are made (runs that ended OK: 30).
- `tools/ppl_gate_v1e.py` against AnovaLab beta 1i (`verify/round17/gates/AnovaLab_beta1j.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 5 reports, as in AnovaLab beta 1i; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round17/helpcheck_r17.json` (Round 11's `helpcheck_r11.py`): 10 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`, the new version beside the old (`verify/round17/overlap_AnovaLab.txt`): the same report.
- The monkey's 1,000 runs were not made again: nothing the calculator runs differs but the words it shows, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 17 Nov 2026: Program Catalog > Edit > Check said "No errors in the program" (`verify/round17/vc_checks.txt`). The program was not run there in this round.

## On a G1 or a G2

Not yet run on a G1 or a G2. Only words on the screen changed, and the version the opening page shows; the program should behave exactly as beta 1i.
