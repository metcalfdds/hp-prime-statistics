# FitCheck beta 1h: changes (15 November 2026)

Round 15. Built from beta 1g by exact replacements (`verify/round15/make_fitcheck_1h.py`; a replacement that does not match exactly once stops the build).

## Why

Three reasons, in the order they came up.

1. **A standard error beside the skewness and the kurtosis.** Roger, 15 November 2026, asked whether Stan Brown's statistics programs for the TI-83/84 (MATH200A and MATH200B, brownmath.com) do anything useful that ours do not. Their descriptions on that site were compared with what our programs do, and two things that MATH200B has were missing here: a confidence interval for a correlation (now in ScatterLab beta 2l) and a standard error beside the skewness and the kurtosis. Roger: "1 and 2 would be great". This is 2. Only the descriptions of those programs were read. No line of their code was read, and the two standard errors are written from their formulas.
2. **The credits.** Roger, 14 November 2026: "IS there an issue with 'reworking' the TI and Triola and Lloyd programs?" The record (the TI sweep of 20 October 2026) is that the TI-83/84 programs were decoded and read to see what each one computes and where it goes wrong, and that FitCheck was then written new in PPL; none of the TI code is in it. The credits used a verb that says more than that. They now say what was done, as the last paragraph of the book's Appendix F does.
3. **The closing summary after a sample in bins.** Found on the Virtual Calculator while the new lines were being looked at: after the crimtab preset the program's closing line was "FitCheck: nothing computed", although its Tests page had just shown a skewness and a kurtosis. A binned sample has no Shapiro–Wilk W, and W was all the summary knew about a normality sample. This is beta 1g's code, not something this round broke.

## What changed

| What | Where (line numbers in `FitCheck_beta1h.txt`) |
| --- | --- |
| **The Tests page gives each shape number its standard error.** The one line "Skewness g₁ = …, excess kurtosis g₂ = …" is now three: "Skewness g₁ = +1.388  (SE 0.117)", "Excess kurtosis g₂ = +1.344  (SE 0.232)" and, in gray, "SE: the standard error in normal samples." (the Rossi ages). | `fc_NTestLines` (2375 to 2377) |
| **The arithmetic**, one new routine, called where g₁ and g₂ are set, for a raw sample and for a binned one. | `fc_ShapeSE` (1357, with its comment from 1347); called at 1394 (`fc_NormSet`) and 1445 (`fc_NormSetBin`); `fcSeS`, `fcSeK` (248, 251) |
| **Help page 5 of 8 (Normality)** ends with one sentence more: "Tests page: skewness g₁ and excess kurtosis g₂, each with its SE if the data are normal." | `fc_Help` (3173) |
| **Help page 8 of 8 (Credits)**: "FitCheck does on the Prime what Triola's TI-83/84 goodness-of-fit and normality programs do (…).  It was written new for the Prime, with none of their code and without their bugs: the header lists them." It began "FitCheck reworks …". | 3186 |
| **The header's note on those programs** begins "Does on the Prime what these TI-83/84 programs do.  They were decoded and read … to see what each one computes; FitCheck was then written new in PPL, and none of their code is in it." It began "Replaces / reworks". | 160 to 163 |
| **The closing summary after a binned sample** names its two shape numbers: "FitCheck: binned sample, skewness +0.050, excess kurtosis +0.170;" (crimtab). With a χ² fit on the bins it follows that fit's part of the summary. A raw sample's summary is its W, as before, and a session with no fit, no sample and no test still returns "FitCheck: nothing computed". | `FitCheck` (3383 to 3387) |
| The opening page names the version, "FitCheck - beta 1h". | 3196 |

**The two standard errors.** The page prints the moment forms, g₁ = m₃/m₂^1.5 and g₂ = m₄/m₂² − 3. Their standard errors in samples of n from a normal population are exact, not large-sample approximations:

- SE(g₁) = √( 6(n − 2) / ((n + 1)(n + 3)) )
- SE(g₂) = √( 24n(n − 2)(n − 3) / ((n + 1)²(n + 3)(n + 5)) )

They are the ones SciPy's `skewtest` and `kurtosistest` start from (D'Agostino, Belanger & D'Agostino 1990; Anscombe & Glynn 1983, Eq. 1). For n = 3, g₂ is −1.5 whatever the data, and its SE is 0. In a normal sample g₁ averages 0 and g₂ averages −6/(n + 1), a little below 0.

**They are the standard errors of the numbers FitCheck prints.** A statistics package usually prints the *adjusted* skewness and kurtosis, G₁ and G₂, with the standard errors that belong to those: for the Rossi ages 1.393 (SE 0.117) and 1.374 (SE 0.234), against FitCheck's 1.388 (SE 0.117) and 1.344 (SE 0.232). With 432 values the two pairs nearly agree. With 10 values they do not (SE 0.579 against 0.687 for the skewness, 0.755 against 1.334 for the kurtosis), because the statistics themselves differ. A reader who compares FitCheck with a package should expect that.

**What the SE is for.** A g₁ or g₂ within about two standard errors of 0 is what a normal sample of that size would give. The page says "in normal samples" because the standard errors are worked out under normality; they are not standard errors of the estimates when the data are not normal, and the page gives no test built on them (it already has three tests of normality).

## Checks

- `verify/verify_FitCheck_beta1h.py`: **31 checks, 0 failed** (output beside it).
  - The arithmetic (A1 to A6): `fc_ShapeSE` equals the two formulas to 10 digits for n from 3 to 5,000; a second reference, the standard deviations of g₁ and g₂ over 200,000 simulated normal samples at n = 4, 10, 30 and 100, is within 0.31% of them; at n = 3, SE(g₂) is exactly 0 and SE(g₁) is 0.5; on 60 random samples of 3 to 300 values g₁ and g₂ equal SciPy's and each SE is taken at the sample's own n; the two presets give the numbers above.
  - The page (P1 to P4): on a random sample every other line of the Tests page is beta 1g's and the shape lines are the three expected; the two presets show their numbers; no line is longer than 46 characters.
  - The edges (E1, E2): three values load and show "(SE 0.000)" beside g₂ = −1.5; two values, values all the same, and 5,001 values are each refused with their sentence, and the SEs are not touched.
  - The menus and their ways out (M1 to M10): the Tests page's own pages in turn; Esc at the main menu and at the Normality menu; the four soft keys; a refused D1; Help to its end and out with Esc; and the closing summary after crimtab (M8), after crimtab and its χ² fit on the bins (M9), and after crimtab followed by the Rossi ages (M10).
  - Against beta 1g (R1): over 30 seeds of the monkey the two versions give the same verdict, boxes and closing summary (but for the binned sample's two numbers, in 7 runs) and the same 988 screens text for text, apart from the 48 Tests and help-5/8 pages.
  - The help (H1 to H5): eight pages; pages 1 to 4, 6 and 7 word for word beta 1g's; page 5 with its two lines more; page 8's new credit; the old verb nowhere in the file; no help line over 46 characters and no page over 14 lines.
  - Layout (D1, D2): no firm overlap, no text off the screen, no number cut short on any screen.
- Gate (`tools/ppl_gate_v1e.py` against beta 1g; `verify/round15/gates/FitCheck_beta1h.txt`): **PASS**. hp-prime-kit lint 0 errors; `ppl_check_v5` clean; `lint_ppl` 9 reports, as in beta 1g; no name collision in the fleet.
- Harness smoke test: no error, 0 warnings. `tools/text_overlap_v1.py --walk`: the same report as beta 1g, with no collision.
- Help layout at the calculator's glyph widths (`verify/round15/helpcheck_r15.json`): 8 screens, no reports.
- Monkey test: **1,000 of 1,000 runs OK** (`verify/round15/mk/FitCheck.jsonl`; base 15, `--lists --writes D`), run on the file as filed.
- **HP Prime Virtual Calculator 2.4.2 (build 2026-09-09): Check "No errors in the program"; then, in a later session, a run** (`verify/round15/vc_checks.txt`, `verify/round15/screens/`). The Rossi ages' Tests page 2 of 3 and the crimtab heights' page 1 of 2 show the shape lines with the numbers above; help pages 5 and 8 show their new words; Quit after the crimtab sample shows the new summary in its box. The subscripts in g₁ and g₂ draw, and every line is inside its page. The file as filed was checked in its own session and collected before it was run.

## On a G1 or a G2 (not yet run)

1. Normality > Preset: Rossi ages, a key, the Tests soft key, then Down once. Page 2 of 3 should show "Skewness g₁ = +1.388  (SE 0.117)", "Excess kurtosis g₂ = +1.344  (SE 0.232)" and the gray line under them.
2. Menu, Normality > Preset: crimtab heights, a key, Tests. Page 1 of 2 should show +0.050 (SE 0.045) and +0.170 (SE 0.089).
3. Menu, Quit. The box should read "FitCheck: binned sample, skewness +0.050, excess kurtosis +0.170;".
4. Help, pages 5 and 8: the last two lines of page 5 and the first paragraph of page 8, each inside the frame.

## Unresolved

- Nothing has run on a G1 or a G2.
- The header's file map (the comment that lists the routines by line number) still carries an earlier version's line numbers.
- The page gives the standard errors and no z built on them; whether a "g₁/SE" line would help or only invite a fourth test of normality is the author's choice.
