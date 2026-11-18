# TTestLabG beta 1i: changes (17 November 2026)

Round 17 of 17 November 2026: the words on the screen. Roger, reading Draft 46 of the book that morning: "The p-value and t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". The book prints every program's help pages word for word, so the programs' own text had to follow; asked whether now or later, he answered "Now, as Round 17". A calculator's screen has no italics, so a program keeps the rest of each rule: a hyphen joins a statistic's letter to its noun (F-test, t-table, z-values), an expression like n - 1 stands in parentheses of its own (df = (n - 1)), and the p of p-value is a small letter. `tools/screen_text_v1.py` is the check: before the round it found 116 places in 16 programs (the quoted strings and the texts the generic walks drew; `verify/round17/screen_text_before.txt`), and now none. TTestLabG is the general version of TTestLab and is always built from it: `tools/make_tlg1_v4.py` made this file from TTestLab beta 1l (v3's blocks, two lines of which carry this round's words: `tools/tlg1_v4_blocks.txt`).

## What changed

1. Step 2 writes "Pooled variances:  df = (N1 + N2 - 2)", "One sample:  df = (N - 1)" and, for separate variances, "By hand: df = the smaller of (N1-1), (N2-1) = ..."; help 3 of 3 says "df = (N - 1)" (they said "df = N1 + N2 - 2", "df = N - 1", "the smaller of N1-1, N2-1").

| Line | Routine | It said | It says |
|---|---|---|---|
| 987 | `tz_Step2` | Pooled variances:  df = N ...  - 2 | Pooled variances:  df = (N ...  - 2) |
| 1002 | `tz_Step2` | By hand: df = the smaller of N ... -1, N ... -1 =  | By hand: df = the smaller of (N ... -1), (N ... -1) =  |
| 1272 | `tz_Step2N` | One sample:  df = N - 1 | One sample:  df = (N - 1) |
| 2036 | `tz_Help` |  - μ₀)/(s/√N), df = N - 1.  Type the mean, SD and N, |  - μ₀)/(s/√N), df = (N - 1).  Type the mean, SD and N, |

2. **Nothing else changed.** With every quoted string taken out, the code of TTestLabG beta 1h and of TTestLabG beta 1i is the same line for line. The other differences are the header and its history note (line 4; lines 20-27); the program shows no version on its pages.

## For the book

- The book prints the help pages word for word. One of the 3 help screens changed: "TTestLabG help 3/3: One sample, proportions". `helppages.json` takes them with the book's next draft.
- The book's one capture of TTestLabG, its flowchart (Figure 11.5), shows no wording that changed.

## Checks

- `verify/verify_round17_screen_text_v1.py` (160 checks, 0 failed, for the sixteen programs together; its output is beside it). For TTestLabG: the build makes this file byte for byte; of its 1,638 lines of code 4 differ, each only inside quotation marks; with the round's replacements made in the old help pages, the two versions' 3 help screens read the same, and nothing on them is cut or overlaps at the glyph widths GlyphProbe_v1 measured on the Virtual Calculator; **every changed text was seen on a screen of the new version** ("df = (N₁ + N₂ - 2)" 38 times; "the smaller of (N₁-1), (N₂-1)" 10 times; "df = (N - 1)" 12 times); the tightest of them has 24 px to spare in its line; and over 30 seeds of the monkey the old and the new version show the same 839 screens and 110 boxes, menus and forms, text for text once the replacements are made (runs that ended OK: 30).
- `tools/ppl_gate_v1e.py` against TTestLabG beta 1h (`verify/round17/gates/TTestLabG_beta1i.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 4 reports, as in TTestLabG beta 1h; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round17/helpcheck_r17.json` (Round 11's `helpcheck_r11.py`): 3 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`, the new version beside the old (`verify/round17/overlap_TTestLabG.txt`): the same 73 distinct screens, and one more overrun by the walk's own estimate (19 where the old version has 18, and the other 18 are the old version's): "By hand: df = the smaller of (N₁-1), (N₂-1) = 181," has 50 characters where it had 46, and at the walk's 6.5 px a character its right edge is put at 333. The finding is marginal (not there at 5.5 px a character), and at the calculator's glyph widths the line is 225 px wide and ends at x = 233 of 320 (`verify/round17/overlap_TTestLabG_detail.txt`, written by `walk_detail_r17.py`).
- The monkey's 1,000 runs were not made again: nothing the calculator runs differs but the words it shows, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 17 Nov 2026: Program Catalog > Edit > Check said "No errors in the program" (`verify/round17/vc_checks.txt`). The program was not run there in this round.

## On a G1 or a G2

Not yet run on a G1 or a G2. Only words on the screen changed; the program should behave exactly as beta 1h.
