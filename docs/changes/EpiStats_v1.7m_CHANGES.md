# EpiStats v1.7m: changes (17 November 2026)

Round 17 of 17 November 2026: the words on the screen. Roger, reading Draft 46 of the book that morning: "The p-value and t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". The book prints every program's help pages word for word, so the programs' own text had to follow; asked whether now or later, he answered "Now, as Round 17". A calculator's screen has no italics, so a program keeps the rest of each rule: a hyphen joins a statistic's letter to its noun (F-test, t-table, z-values), an expression like n - 1 stands in parentheses of its own (df = (n - 1)), and the p of p-value is a small letter. `tools/screen_text_v1.py` is the check: before the round it found 116 places in 16 programs (the quoted strings and the texts the generic walks drew; `verify/round17/screen_text_before.txt`), and now none. The build is `verify/round17/make_round17.py`: each change is an exact replacement inside a quoted string of EpiStats v1.7l (a replacement that is not found the number of times the build names stops it), then the version (header, history note, version strings).

## What changed

1. Help 6 of 15 (Mantel-Haenszel): "Breslow-Day, (k-1) df:" (it said "Breslow-Day (k-1 df):"), and the line above it in the same form, "M-H chi-square, 1 df:" (it said "(1 df):").

| Line | Routine | It said | It says |
|---|---|---|---|
| 6018 | `es_Help_MH` | M-H χ² (1 df): is the common OR 1? | M-H χ², 1 df: is the common OR 1? |
| 6019 | `es_Help_MH` | Breslow-Day (k-1 df): are the strata's ORs alike?  A small p | Breslow-Day, (k-1) df: are the strata's ORs alike?  A small p |

2. **Nothing else changed.** With every quoted string taken out, the code of EpiStats v1.7l and of EpiStats v1.7m is the same line for line. The other differences are the header and its history note (line 3; lines 31-36), and the version the program shows (2 lines of code).

## For the book

- The book prints the help pages word for word. One of the 15 help screens changed: "EpiStats help 6/15: Mantel-Haenszel". `helppages.json` takes them with the book's next draft.
- None of the book's screen captures of EpiStats shows a wording that changed: the figures of the sixteen programs were read for the changed lines, and the two that showed one (Figures 11.3 and 13.4) were taken again.

## Checks

- `verify/verify_round17_screen_text_v1.py` (160 checks, 0 failed, for the sixteen programs together; its output is beside it). For EpiStats: the build makes this file byte for byte; of its 4,668 lines of code 4 differ, each only inside quotation marks; with the round's replacements made in the old help pages, the two versions' 15 help screens read the same, and nothing on them is cut or overlaps at the glyph widths GlyphProbe_v1 measured on the Virtual Calculator; **every changed text was seen on a screen of the new version** ("M-H χ², 1 df: is the common OR 1?" 4 times; "Breslow-Day, (k-1) df:" 4 times); the tightest of them has 35 px to spare in its line; and over 30 seeds of the monkey the old and the new version show the same 1,009 screens and 360 boxes, menus and forms, text for text once the replacements are made (runs that ended OK: 30).
- `tools/ppl_gate_v1e.py` against EpiStats v1.7l (`verify/round17/gates/EpiStats_v1.7m.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 8 reports, as in EpiStats v1.7l; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round17/helpcheck_r17.json` (Round 11's `helpcheck_r11.py`): 15 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`, the new version beside the old (`verify/round17/overlap_EpiStats.txt`): the same report.
- The monkey's 1,000 runs were not made again: nothing the calculator runs differs but the words it shows, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 17 Nov 2026: Program Catalog > Edit > Check said "No errors in the program" (`verify/round17/vc_checks.txt`). The program was not run there in this round.

## On a G1 or a G2

Not yet run on a G1 or a G2. Only words on the screen changed, and the version the opening page shows; the program should behave exactly as v1.7l.
