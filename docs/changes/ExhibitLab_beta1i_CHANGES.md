# ExhibitLab beta 1i: changes (17 November 2026)

Round 17 of 17 November 2026: the words on the screen. Roger, reading Draft 46 of the book that morning: "The p-value and t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". The book prints every program's help pages word for word, so the programs' own text had to follow; asked whether now or later, he answered "Now, as Round 17". A calculator's screen has no italics, so a program keeps the rest of each rule: a hyphen joins a statistic's letter to its noun (F-test, t-table, z-values), an expression like n - 1 stands in parentheses of its own (df = (n - 1)), and the p of p-value is a small letter. `tools/screen_text_v1.py` is the check: before the round it found 116 places in 16 programs (the quoted strings and the texts the generic walks drew; `verify/round17/screen_text_before.txt`), and now none. The build is `verify/round17/make_round17.py`: each change is an exact replacement inside a quoted string of ExhibitLab beta 1h (a replacement that is not found the number of times the build names stops it), then the version (header, history note, version strings).

## What changed

1. Help 4 of 8: "t on (n - 1) df" (it said "t on n - 1 df"); the help line of the SD field of the weights form: "SD, divisor (n - 1), grams, 0 to 1,000" (it said "SD (divisor n - 1), ...").

| Line | Routine | It said | It says |
|---|---|---|---|
| 2292 | `sz_WtLoad` | SD (divisor n - 1), grams, 0 to 1,000 | SD, divisor (n - 1), grams, 0 to 1,000 |
| 2810 | `sz_Help` |  t SE, t on n - 1 |  t SE, t on (n - 1) |

2. **Nothing else changed.** With every quoted string taken out, the code of ExhibitLab beta 1h and of ExhibitLab beta 1i is the same line for line. The other differences are the header and its history note (line 17; lines 50-55); the program shows no version on its pages.

## For the book

- The book prints the help pages word for word. One of the 8 help screens changed: "ExhibitLab help 5/8: The total weight". `helppages.json` takes them with the book's next draft.
- None of the book's screen captures of ExhibitLab shows a wording that changed: the figures of the sixteen programs were read for the changed lines, and the two that showed one (Figures 11.3 and 13.4) were taken again.

## Checks

- `verify/verify_round17_screen_text_v1.py` (160 checks, 0 failed, for the sixteen programs together; its output is beside it). For ExhibitLab: the build makes this file byte for byte; of its 2,248 lines of code 2 differ, each only inside quotation marks; with the round's replacements made in the old help pages, the two versions' 8 help screens read the same, and nothing on them is cut or overlaps at the glyph widths GlyphProbe_v1 measured on the Virtual Calculator; **every changed text was seen on a screen of the new version** ("SD, divisor (n - 1), grams" 8 times; "t SE, t on (n - 1)" 11 times); the tightest of them has 96 px to spare in its line; and over 30 seeds of the monkey the old and the new version show the same 2,710 screens and 286 boxes, menus and forms, text for text once the replacements are made (runs that ended OK: 30).
- `tools/ppl_gate_v1e.py` against ExhibitLab beta 1h (`verify/round17/gates/ExhibitLab_beta1i.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 6 reports, as in ExhibitLab beta 1h; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round17/helpcheck_r17.json` (Round 11's `helpcheck_r11.py`): 8 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`, the new version beside the old (`verify/round17/overlap_ExhibitLab.txt`): the same report.
- The monkey's 1,000 runs were not made again: nothing the calculator runs differs but the words it shows, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 17 Nov 2026: Program Catalog > Edit > Check said "No errors in the program" (`verify/round17/vc_checks.txt`). The program was not run there in this round.

## On a G1 or a G2

Not yet run on a G1 or a G2. Only words on the screen changed; the program should behave exactly as beta 1h.
