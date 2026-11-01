# TTestLabG beta 1: notes

*31 October 2026, night. New: the **general version** of TTestLab, the first of the intro-statistics companion guide's general versions. Built from TTestLab beta 1b by `tools/make_tlg1_v1.py` (exact replacements; the build stops if any text is not found exactly as expected). 1,298 lines. **Ran on the Virtual Calculator** the same night (below); not yet on a G1 or G2.*

## Why

Roger, 31 October 2026, planning the companion guide for a wide general audience: "how about general versions and advanced versions?" The **advanced version** is the program as it stands, with Roger's lecture rules, his examples and his SPSS output, for his own courses and this repository. The **general version** is a separate, simpler program built from the same routines, for the guide, Statisticles and any intro course. Where the textbooks differ, Roger asked for "your best judgment about what would work best"; the guide's Conventions section records the choices, and TTestLabG is the first program built to them. He also asked for government data wherever possible, really old data sometimes, and said criminal-justice data is welcome.

## What differs from TTestLab beta 1b

| | TTestLab beta 1b (advanced) | TTestLabG beta 1 (general) |
|---|---|---|
| Name and tags | `TTESTLAB`, `tt_`, `tt` | `TTESTLABG`, `tz_`, `tz`: both can sit on one calculator (one pool of routine names, Lessons Learned §5) |
| Test at the start | pooled | **separate variances (Welch)**: it does not need equal population variances and loses little when they are equal (Delacre, Lakens & Leys 2017) |
| The flowchart | Figure 11.2; hint: "the problem says so, or Levene's test (SPSS)" | "Which t test?"; hint: "Not sure the variances are equal? Answer No: the separate t needs no such assumption." |
| t critical | the exact value and the lecture's printed-table row (df 73 → row 60), with the lecture's five misprinted cells | **the exact value only**; a gray note: a df the table lacks takes the next smaller row it lists (a larger t crit), a fractional df is rounded down first. No row is claimed, because the books' tables differ past df 30. No note at df 30 and below |
| Step 2, separate variances | Welch's df worked, and SPSS's row named | the same, plus **the hand shortcut**: df = the smaller of N₁ − 1 and N₂ − 1, and its t crit ("larger, so a safer test") |
| Step 4 | the lecture's rounding notes and SPSS's printed values | no notes |
| Step 5 | "(Table row …, decides the other way.)" when the row and the exact df disagree | **a p that rounds to α at 3 decimals also prints to 4 significant digits**: "(p = 0.04970: just below α = 0.050.)" |
| Means and SDs from raw scores | as typed numbers, up to 5 decimals (206.32418) | **4 significant digits** (206.3); typed numbers still print as typed |
| "Pooled or separate?" page, last lines | "The lecture: pooled if the population variances are equal …" | "Pooled needs equal population variances; separate does not, and loses little when they are equal, so it is the default (Delacre 2017)." |
| Help | the lecture's table row; rounding as in example 1 | the printed-table rule; "A long data set: DataLoad fills D1 and D2." |
| Examples | age at arrest (JDCC, pooled); matched jails (Census of Jails, dependent); drug use by sex (Roger's SPSS output, separate) | **Darwin's plants** (Darwin 1876, 15 pairs of *Zea mays*, crossed and self-fertilised; dependent); **the 1970 draft lottery** (Selective Service; births Jan–Jun against Jul–Dec; separate); age at arrest (JDCC, pooled); matched jails (Census of Jails, dependent) |

Everything else (the arithmetic, the five screens, the curve, the forms, the D1/D2 reads, every refusal and cancel path, the drains) is TTestLab beta 1b's, under the new tags: the 84 checks and the independent review behind beta 1b carry over.

**The examples' data.** Darwin's heights are RankLab's copy (`rk_LdDarwin`); eight times the differences are Fisher's (1935) figures 49, −67, 8, 16, 6, 23, 28, 41, 14, 29, 56, 24, 75, 60, −48. The draft numbers are PowerViz's list (`pv_Draft`, AnovaLab's, after Fienberg 1971, *Science* 171:255), copied by the build script from `programs/PowerViz_v2.5k.txt`. The verify script checks them again: the numbers 1–366 once each, 1 on September 14, 2 on April 24, 366 on June 8.

**What the examples give** (SciPy): Darwin, t(14) = 2.148, p = 0.0497, two-tailed, reject at .05 (t crit 2.145): the p that prints "0.050" beside a rejection and so gets the new note. The draft lottery: means 206.3 and 160.9, SDs 106.1 and 100.8, N 182 and 184, Welch t(362.56) = 4.196, p < 0.001; the hand shortcut gives df 181 and t crit ±1.973. Age at arrest and matched jails: as in TTestLab (t(73) = −2.20, p = 0.031; t(4) = 1.33, p = 0.873 one-tailed).

## Verification

`verify/verify_TTestLabG_beta1.py`, output `verify_TTestLabG_beta1_output.txt`: **93 PASS, 0 FAIL** (about 7 s). It is TTestLab beta 1b's script with the names changed and its lecture-specific checks replaced:

- **A** the arithmetic against SciPy, as before (pooled and separate over 288 cases, SDs of 1E−200 and 1E200, pairs in all three tails, p, t crit in every column and its fallback); new **A5**: step 3's printed-table note in five cases (df 73 pooled, df 72.44 separate, pairs at df 4, 30 and 31) and step 2's hand-shortcut df and t crit in four (both tails, one-tailed either way).
- **B** the four examples against SciPy and NumPy, with their screens; the draft numbers against the published facts; the near-α note both ways (Darwin just below; 2.226 vs 2.228 just above).
- **C, E, F, R** TTestLab's screens, flowchart, forms, D1/D2 reads, refusals, menu, help, the pooled-or-separate page (with its simulation), the finger left on a form's OK, and every finding of TTestLab's review, re-aimed at the new menu positions.
- **N** the general version itself: separate is the start state; the start menu, the Examples menu and the menu's "Quit TTestLabG"; no string a student can see names the lecture, Figure 11.2, Table 11.x, Levene's test or the SPSS drug-use example.
- **G** static: no `!=`; 47 routines, all `tz_`; 48 file-level variables, all `tz`; one EXPORT, `TTESTLABG`.
- **D** text_overlap_v1 over 115 distinct screens: no firm overlap, straddle or overrun, and no marginal one (a first build's "Self-fertilized (x₂)" ran past the box at the conservative width; the label is "Self").

## Gate

`ppl_gate_v1c.py TTestLabG_beta1.txt TTestLab_beta1b.txt`: **RESULT: PASS** (kit lint 0 errors; no hard errors; the parse stops at the first file-level `LOCAL`, the kit tool's limit). `fleet_names_v2.py programs/*.txt`: 30 files, 2,251 routine names, 0 collisions, 0 untagged, 0 built-in matches. `case_scan_v1.py`: nothing to report. Its names against the built-in list, ignoring case: none.

## The run on the Virtual Calculator (31 Oct 2026, 23:08–23:15 CDT)

Virtual Calculator 2.4.2 (build 2026-09-09), calculator `Prime`, Rogers-HP; by Claude through computer use. `TTestLabG.hpprgm` (hp-prime-kit `hpprime write`) copied in while the calculator was closed, beside TTestLab beta 1b.

- **Check:** "No errors in the program", for the first build and again for the file filed here.
- **Darwin's plants:** step 1 as checklist item 2; step 3 "t crit = ±2.145   (exact, for df = 14)", no printed-table note; step 5 as item 3, the near-α note "(p = 0.04970: just below α = 0.050.)" whole.
- **The draft lottery** (from the menu's Examples): step 1 "x̄₁ = 206.3", "s₁ = 106.1", "N₁ = 182", "Born Jan-Jun"; step 2 "df = 13707 / 37.81 = 362.56", "By hand: df = the smaller of N₁-1, N₂-1 = 181,", "t crit = ±1.973: larger, so a safer test."; step 3 the exact ±1.967 and the note "Printed table?  Round df down to 362; if the / table lacks that row, take the next smaller."; step 5 "t obt = 4.196 is beyond t crit = ±1.967", "Report t(362.56) = 4.20, p < 0.001, two-tailed". The example opened with no visible delay.
- **The flowchart:** "Which t test?", the hint whole. **Help:** both pages whole, "A long data set: DataLoad fills D1 and D2."
- **Age at arrest:** step 3 "t crit = ±1.993   (exact, for df = 73)" and "Printed table without row 73?  Take the next / smaller row it lists (its t crit is larger)."; step 4 the working with no rounding note; "Pooled or separate?" the three new lines whole.
- **Quit:** "TTestLabG: t(362.56) = 4.20, p < 0.001, two-tailed" and "TTestLabG: t(73) = −2.20, p = 0.031, two-tailed" in Home. **TTestLab ran beside it** (its own start menu, Figure 11.2, "t(73) = −2.20" and "t(265.92) = −4.35"): the two versions share one calculator.
- **Found there and fixed before filing:** the menu's last item still read "Quit TTestLab" (the build renamed display strings that begin with "TTestLab", and this one begins with "Quit"). The build script now renames it and stops if any string names TTestLab without the G; verify N2 checks the item. The fixed file was copied in, checked and run (age at arrest, its menu reading "Quit TTestLabG").
- **Driving notes:** the name typed in Home must be the EXPORT's, `TTESTLABG` (typed as `TTestLabG` it gave "Error: Syntax Error"); typed quickly, the final G was once dropped and TTestLab ran instead. Launching the Virtual Calculator while it was already running opened second and third calculators, `Prime_1` and `Prime_2` (Lessons Learned §16); both were closed and their folders set aside.

## Device checklist (Virtual Calculator, G1, G2)

1. Starter pack v4 (or `TTestLabG.hpprgm`) copied in while the Virtual Calculator is closed; Check: "No errors in the program". TTestLab and TTestLabG both in the Program Catalog; each runs (one pool of names).
2. Start menu → Example: Darwin's plants: step 1 shows 7 pairs (23.500, 17.375 …), "... and 8 more pairs", "Crossed (x₁)", "Self (x₂)", "Outcome: plant height (inches), Darwin 1876".
3. Darwin, step 5: "t obt = 2.148 is beyond t crit = ±2.145:", REJECT, "(p = 0.04970: just below α = 0.050.)", "Report t(14) = 2.15, p = 0.050, two-tailed". Quit: "TTestLabG: t(14) = 2.15, p = 0.050, two-tailed".
4. Example: draft lottery: step 1 "x̄₁ = 206.3", "s₁ = 106.1", "N₁ = 182"; step 2 Welch's df 362.56 and "By hand: df = the smaller of N₁-1, N₂-1 = 181,", "t crit = ±1.973: larger, so a safer test."; step 3 "t crit = ±1.967   (exact, for df = 362.56)" and "Printed table?  Round df down to 362; if the"; step 5 "p < 0.001". (The draft lists are built when the example opens: note any delay on a G1.)
5. Example: age at arrest: step 3 "t crit = ±1.993   (exact, for df = 73)" and "Printed table without row 73?  Take the next"; no rounding note on step 4.
6. Example: matched jails: step 3 "t crit = -2.132   (exact, for df = 4)", no printed-table note.
7. Choose the test: the title "Which t test?"; the hint "Not sure the variances are equal?  Answer No:" fits whole; Yes, No → separate.
8. Menu → Pooled or separate? with age at arrest: the last three lines fit whole.
9. Help: both pages; "A long data set: DataLoad fills D1 and D2."; Help returns to the start menu.
10. TTestLab's own checklist (`TTestLab_beta1b_CHANGES.md` items 13–26) holds for TTestLabG with the examples renumbered (age at arrest is example 3).

## Unresolved

- Not yet independently reviewed as a program of its own (Lessons Learned §14 rule 22): its arithmetic and dialogs are beta 1b's, which had one; the new screens (A5, B, N) are checked by the verify script only.
- Not yet run on a G1 or a G2. On the Virtual Calculator, the checklist's items 1–5 and 7–9 ran (above); item 6 (matched jails) and item 10 did not.
- One-sample tests and the proportion tests (the companion guide's build order, steps 4 and 7) go into TTestLab first, then into TTestLabG.
