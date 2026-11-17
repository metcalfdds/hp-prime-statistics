# TDist3D beta 1b: changes (17 November 2026)

Round 17 of 17 November 2026: the words on the screen. Roger, reading Draft 46 of the book that morning: "The p-value and t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". The book prints every program's help pages word for word, so the programs' own text had to follow; asked whether now or later, he answered "Now, as Round 17". A calculator's screen has no italics, so a program keeps the rest of each rule: a hyphen joins a statistic's letter to its noun (F-test, t-table, z-values), an expression like n - 1 stands in parentheses of its own (df = (n - 1)), and the p of p-value is a small letter. `tools/screen_text_v1.py` is the check: before the round it found 116 places in 16 programs (the quoted strings and the texts the generic walks drew; `verify/round17/screen_text_before.txt`), and now none. The build is `verify/round17/make_round17.py`: each change is an exact replacement inside a quoted string of TDist3D beta 1a (a replacement that is not found the number of times the build names stops it), then the version (header, history note, version strings).

## What changed

1. Help 1 of 4: "Student's t has one parameter: degrees of freedom, nu = (n - 1)." (it said "... one parameter, the degrees of freedom nu = n - 1."; with the parentheses the old sentence was 299 pixels wide at the glyph widths measured on the Virtual Calculator, and the line holds 296: the new one is 285).  The opening page says "Every t-curve at once" (it said "t curve").

| Line | Routine | It said | It says |
|---|---|---|---|
| 949 | `tdHelp` | Student's t has one parameter, the degrees of freedom  ...  = n  ...  1. | Student's t has one parameter: degrees of freedom,  ...  = (n  ...  1). |
| 1093 | `tdWelcome` | Every t curve at once: t runs across, the degrees | Every t-curve at once: t runs across, the degrees |

2. **Nothing else changed.** With every quoted string taken out, the code of TDist3D beta 1a and of TDist3D beta 1b is the same line for line. The other differences are the header and its history note (line 4; lines 32-39); the program shows no version on its pages.

## For the book

- The book prints the help pages word for word. One of the 4 help screens changed: "TDist3D help 1/4: What the surface is". `helppages.json` takes them with the book's next draft.
- None of the book's screen captures of TDist3D shows a wording that changed: the figures of the sixteen programs were read for the changed lines, and the two that showed one (Figures 11.3 and 13.4) were taken again.

## Checks

- `verify/verify_round17_screen_text_v1.py` (160 checks, 0 failed, for the sixteen programs together; its output is beside it). For TDist3D: the build makes this file byte for byte; of its 797 lines of code 2 differ, each only inside quotation marks; with the round's replacements made in the old help pages, the two versions' 4 help screens read the same, and nothing on them is cut or overlaps at the glyph widths GlyphProbe_v1 measured on the Virtual Calculator; **every changed text was seen on a screen of the new version** ("has one parameter: degrees of freedom, ν = (" 4 times; "Every t-curve at once" 30 times); the tightest of them has 11 px to spare in its line; and over 30 seeds of the monkey the old and the new version show the same 1,247 screens and 43 boxes, menus and forms, text for text once the replacements are made (runs that ended OK: 30).
- `tools/ppl_gate_v1e.py` against TDist3D beta 1a (`verify/round17/gates/TDist3D_beta1b.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 5 reports, as in TDist3D beta 1a; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round17/helpcheck_r17.json` (Round 11's `helpcheck_r11.py`): 4 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`, the new version beside the old (`verify/round17/overlap_TDist3D.txt`): the same report.
- The monkey's 1,000 runs were not made again: nothing the calculator runs differs but the words it shows, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 17 Nov 2026: Program Catalog > Edit > Check said "No errors in the program" (`verify/round17/vc_checks.txt`). After the checked file had been collected the program was run there: the opening page shows "Every t-curve at once: t runs across, the degrees", and help 1 of 4 shows "Student's t has one parameter: degrees of freedom, ν = (n − 1)." whole in its box, ending at x = 295 of 308 (`verify/round17/screens/TDist3D_welcome.png`, `TDist3D_help1.png`).

## On a G1 or a G2

Not yet run on a G1 or a G2. Only words on the screen changed; the program should behave exactly as beta 1a.
