# ScatterLab beta 2m: changes (17 November 2026)

Round 17 of 17 November 2026: the words on the screen. Roger, reading Draft 46 of the book that morning: "The p-value and t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". The book prints every program's help pages word for word, so the programs' own text had to follow; asked whether now or later, he answered "Now, as Round 17". A calculator's screen has no italics, so a program keeps the rest of each rule: a hyphen joins a statistic's letter to its noun (F-test, t-table, z-values), an expression like n - 1 stands in parentheses of its own (df = (n - 1)), and the p of p-value is a small letter. `tools/screen_text_v1.py` is the check: before the round it found 116 places in 16 programs (the quoted strings and the texts the generic walks drew; `verify/round17/screen_text_before.txt`), and now none. The build is `verify/round17/make_round17.py`: each change is an exact replacement inside a quoted string of ScatterLab beta 2l (a replacement that is not found the number of times the build names stops it), then the version (header, history note, version strings).

## What changed

1. The inference page writes "df = (n - 2) = ..." and help 7 of 7 "df = (n - 2);" (they said "df = n - 2").

| Line | Routine | It said | It says |
|---|---|---|---|
| 2272 | `slInfPage` | ,  df = n - 2 =  | ,  df = (n - 2) =  |
| 2421 | `slHelpPg` |   df = n - 2;  H |   df = (n - 2);  H |

2. **Nothing else changed.** With every quoted string taken out, the code of ScatterLab beta 2l and of ScatterLab beta 2m is the same line for line. The other differences are the header and its history note (line 4; lines 33-37); the program shows no version on its pages.

## For the book

- The book prints the help pages word for word. One of the 7 help screens changed: "ScatterLab help 7/7: Testing the slope". `helppages.json` takes them with the book's next draft.
- The book's Figure 13.4, the Inference page of the synthetic example, showed "df = n-2 = 14". It was taken again on the Virtual Calculator (`verify/round17/screens/ScatterLab_inference.png`; the book prints it enlarged three times). No other capture of ScatterLab in the book shows a changed wording.

## Checks

- `verify/verify_round17_screen_text_v1.py` (160 checks, 0 failed, for the sixteen programs together; its output is beside it). For ScatterLab: the build makes this file byte for byte; of its 1,901 lines of code 2 differ, each only inside quotation marks; with the round's replacements made in the old help pages, the two versions' 7 help screens read the same, and nothing on them is cut or overlaps at the glyph widths GlyphProbe_v1 measured on the Virtual Calculator; **every changed text was seen on a screen of the new version** ("df = (n - 2)" 8 times); the tightest of them has 82 px to spare in its line; and over 30 seeds of the monkey the old and the new version show the same 1,694 screens and 104 boxes, menus and forms, text for text once the replacements are made (runs that ended OK: 30).
- `tools/ppl_gate_v1e.py` against ScatterLab beta 2l (`verify/round17/gates/ScatterLab_beta2m.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 10 reports, as in ScatterLab beta 2l; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round17/helpcheck_r17.json` (Round 11's `helpcheck_r11.py`): 7 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`, the new version beside the old (`verify/round17/overlap_ScatterLab.txt`): the same report.
- The monkey's 1,000 runs were not made again: nothing the calculator runs differs but the words it shows, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 17 Nov 2026: Program Catalog > Edit > Check said "No errors in the program" (`verify/round17/vc_checks.txt`). After the checked file had been collected the program was run there, for the book's Figure 13.4: the Inference page of the synthetic example reads "ŷ = 16.64 + 1.020 x,  n = 16,  df = (n - 2) = 14", and every number is the one in the capture of beta 2l (`verify/round17/screens/ScatterLab_inference.png`).

## On a G1 or a G2

Not yet run on a G1 or a G2. Only words on the screen changed; the program should behave exactly as beta 2l.
