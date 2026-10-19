# TrendTest beta 3d: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 3c; every beta 3c feature is kept. Mantel's (N − 1) r² stays the headline. Run on the PC harness only: not yet on the emulator or on hardware.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2, items 11 and 20; details in `findings_C.md`, section 3) found no crash and no wrong number on any screen ("ship"). It listed one wrong number in a Home export, which the brief makes a fix, and four wording items:

> **Improvement 1 (item 11). Exact tiny p for the trend test.** `:762` `trPT := 1 - CHISQUARE_CDF(1, trX2T)` is 0 in 12 digits above X² ≈ 50; the display floors at "p < 0.0001" (fine) but `TR_P` exports 0. For 1 df: `trPT := 2*NORMALD_CDF(0, 1, -SQRT(trX2T))`.

> **C-T1. WRONG TEXT (minor).** `:246-247` header: "the squared residuals add up to Pearson − Armitage, i.e. the departure statistic". The page's departure is Pearson − **Mantel** ((N−1) r²), so the residuals' sum of squares and the departure shown differ by trend/(N−1): 53.1141 vs 53.1149 on the sleep example.

> **C-T2. WRONG TEXT (minor; will look like a bug to a student).** `:1964-1968` help page 3 lists R `prop.trend.test`, SAS PROC FREQ TREND and JMP as "the same test elsewhere". R's `prop.trend.test` is the weighted-regression ANOVA, i.e. Armitage's N r²; for the snoring example it prints 72.688 where the program prints 72.659. […] Fix: "R and SAS print N r²: 72.688 for the snoring table".

> **C-T3. COSMETIC (guess).** `:2010-2011` main menu "Plot: proportions + trend line" (30) […]: the list-form box cut CICatcher's line after 31, so 30 is at the edge. […] or "Plot: proportions, trend line" (29).

> **C-T4. COSMETIC.** `:876-892` `trEnter` accepts non-integer counts (24.5 cases of 100.5): the arithmetic runs, the table prints `STRING(trA, 2, 0)` = "25/101" beside a p computed from 24.5. An `FP()` check with a message closes it.

And review item 22: `verify_TrendTest_beta3c.py` stops with `FileNotFoundError` in a folder holding only the current versions, because it opens beta 3, 3a and 3b beside itself.

## What changed (line numbers: beta 3c → beta 3d)

1. **The trend p as a lower tail** (`trCompute`, 762 → 821–831). `trPT := 1 - CHISQUARE_CDF(1, trX2T)` is now
   `trPT := 2 * NORMALD_CDF(0, 1, -(trX2T^0.5))`.
   - With 1 df, χ² = Z², so P(χ² > X²) = P(|Z| > √X²) = 2 P(Z < −√X²). The Prime's reals hold 12 digits: once the true tail is below about 5E-13 (X² above about 50), `CHISQUARE_CDF` rounds to exactly 1, and 1 − CDF is exactly 0. A lower tail is computed directly and keeps its digits. A ten-line comment above the line says this for a student.
   - `^0.5` is the house square root (no `√`, no SQRT); the brackets make the minus apply to the root.
   - `trPT` is the one place the trend p is computed. `TR_P := trPT` (the export) and every display of it read `trPT`: page 1's "Trend (1 df)" line, page 2's trend panel, the proportions plot's footer and the summary returned to Home. So all of them are computed the same way. They still print "p < 0.0001" below 0.0001 (`trPStr`, unchanged), and every p at or above it prints the same digits as before.
   - Pearson's p (k − 1 df) and the departure's (k − 2 df) stay 1 − CDF: there is no such identity for them.
   - The comment above `trPStr` (416–417 → 472–476) and the header's HOME EXPORTS entry for `TR_P` (297 → 351–353) say so.
2. **C-T1, the header's residual sentence** (245–247 → 296–301). It now reads: the squared residuals add up to Pearson − Armitage's N r²; the departure statistic the screens show is Pearson − Mantel's (N − 1) r², which is larger by trend/(N − 1): 53.1149 against the residuals' 53.1141 for the sleep example. No screen changed.
3. **C-T2, help page 3** (`trHelp`, 1964–1968 → 2045–2049). The five gray lines now say which program prints which form:
   ```
   Same test elsewhere: Epi Info StatCalc prints
   Mantel's (1963) (N-1) r^2, as this page does;
   R prop.trend.test and SAS PROC FREQ / TREND
   print Armitage's (1955) N r^2: 72.688 for
   snoring, 72.659 here.  The ratio is N/(N-1).
   ```
   Each is at most 45 characters. The header's ARITHMETIC note (233–234 → 281–285) says the same.
   - **JMP is no longer named.** The old line called it "the same test", with no claim about the form, and which form JMP prints was not checked here. The review checked R and SAS only.
   - **Mantel's form stays the headline** (decision D11 is open): page 1 still shows "Trend (1 df):  χ² = 72.659".
4. **C-T3, the main menu** (`TrendTest`, 2010 → 2096). "Plot: proportions + trend line" (30) is now **"Plot: proportions, trend line"** (29), the review's wording. A comment above the CHOOSE (2088–2092), outside the list, says why.
5. **C-T4, Enter data** (`trEnter`, 876–887 → 946–962). Inside the existing check loop, a count or total with a fraction sets `enBad := 4`, and the message is **"Cases and totals count people: whole numbers only."** Nothing is loaded. Scores may still have fractions (a dose of 0.5). A comment above the loop says why.
6. **Header:**
   - the banner (4);
   - **Roger's disclaimer** (19 Oct 2026, 12:48), under the distribution terms (→ 15–17): "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes." A comment only. No page of the program states the terms (no on-screen string mentions them), so no page gets the short "Teaching aid; not for legal use." line;
   - the tested-on lines (16–24 → 19–30): beta 3d has run on the PC harness only, and beta 3c passed the emulator retest of 17 Oct;
   - a "beta 3d" paragraph (→ 32–73) with beta 3c's line numbers, the finding IDs and the disclaimer.
7. **Nothing else.** The routines that differ from beta 3c are exactly `TrendTest`, `trCompute`, `trEnter` and `trHelp`. The other 47 routines are byte-identical, comments included.

**The verify script** (review item 22) looks for each older file beside itself, then in `_old` and `_superseded*` folders beside it, then in `/home/claude/work/out` (or the folder named by `VERIFY_PRED_DIR`). A comparison that needs a file it cannot find prints SKIP and is not counted.

## Verification

`verify_TrendTest_beta3d.py`, built from the 3c script, in harness **ppl_run_v3e**. Output in `verify_TrendTest_beta3d_output.txt`: **PASS, 134 checks, 0 failures, 0 skipped** (the 3c script: 98).

- **Kept:** every 3c check: A (every CAS template against fractions, SymPy and statsmodels), B (page 4 with the CAS and without, the cache, the drag, a 1/3 score, the stale-key run), W (CHOOSE widths, solid dots), R1–R10 (the round-2 fixes, against beta 3b). G (round 2a) and G (3c) now compare the beta 3a/3b and 3b/3c files themselves, as their records.
- **D1, TR_P (the review's E1), with every statistics built-in rounded to the Prime's 12 significant digits:**
  - snoring: beta 3d `TR_P` = **1.54116E-17** = chi2.sf(72.6588, 1) to 2E-13 relative; **beta 3c `TR_P` = 0** in the same run;
  - 31 tables with X² from 0 to 168: beta 3d is chi2.sf to 4E-12 relative on every one; beta 3c gives exactly 0 on 16 of them (its largest X² with p > 0 was 47.6);
  - double precision, 200 random tables: beta 3d's `trPT` = chi2.sf to 6E-14, and **every displayed p string is the same as beta 3c's**.
- **D2:** `trPT` is set once, from `NORMALD_CDF`; `TR_P := trPT`; no `CHISQUARE_CDF(1, …)` is left; `trPStr` is only ever handed `trPT`, `trPP`, `trPD` or the panel's own argument, and page 2's trend panel gets `trPT`. Examples → Snoring → Quit returns "TrendTest: X2 trend = 72.6588 (1 df), p < 0.0001; …" with `TR_P` = 1.54E-17.
- **D3, C-T1:** for the sleep example, the program's own `trCompute` gives a residual sum of squares of 53.1141 = departure 53.1149 − trend/(N − 1); the header says so. Beta 3c's header had the old sentence.
- **D4, C-T2:** help page 3 as drawn has the five lines above; 72.688 is the program's own snoring trend (72.658824) × 2484/2483; page 1's headline is still Mantel's 72.659. Beta 3c's page named R and SAS without saying they print N r².
- **D5, C-T3:** the main menu shows "Plot: proportions, trend line" (29; no line over 29), and item 3 still opens the proportions plot. Beta 3c showed the 30-character line.
- **D6, C-T4:** 24.5 cases, and a total of 100.5, are refused with the message and nothing is loaded ("TrendTest: no table"); whole counts with scores 0.5, 1.5, 2.5 are accepted. **Beta 3c accepted 24.5 cases** ("X2 trend = 5.5486").
- **D7, the review's own `check_TrendTest.py`:** on beta 3c, 69 passed, 0 failed. On beta 3d, 66 passed and 3 failed, each by design, because each tests text this version changes on purpose: D1 (help page 3's old line "N r^2.  The two differ by N/(N-1) only." — C-T2), E2 ("the three p-values are 1 - CHISQUARE_CDF" — improvement 1) and F6 ("banner says beta 3c").
- **G (3d):** only `TrendTest`, `trCompute`, `trEnter` and `trHelp` differ, each by exactly its listed change; the other 47 routines are byte-identical, comments included; outside them only comments differ; the header carries Roger's DISCLAIMER line under the terms, and no on-screen string states the terms.
- **Item 22:** the same script, run in a folder holding only `TrendTest_beta3d.txt` and itself with no older version reachable (`VERIFY_PRED_DIR` pointing nowhere): **PASS, 94 checks, 0 failures, 12 skipped** (G 3a, G round 2a, R1–R4 and R6–R8's beta 3b comparisons, G 3c, D1's beta 3c half, G 3d), no FileNotFoundError.
- **R10, `h.sci_strings` over all 296 beta 3d runs:** no small number in scientific form. Two from 1E12 up, the same two as beta 3c: `7.00018ᴇ13` and `3.20000ᴇ17`, `trNum`'s sums of n x² on page 4's decimal page with midranks on a million people (`cas='fail'`). The Prime holds 12 digits, so scientific is its only form for them; six significant digits are kept (justified in beta 3c's CHANGES).

## Gate

In `gate_f19` (the newest version of every program; beta 3c moved to `gate_f19/_old`), `python3 ppl_gate_v1b.py TrendTest_beta3d.txt _old/TrendTest_beta3c.txt`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: clean, as beta 3c; no hard errors (E12 included).
- lint_ppl: 1451 checks, 34 problems, the same 34 as beta 3c (INSTRING read as STRING, bare concatenation in CAS text, the GROB parameter of `trDot`).
- Full parse: stops at the first file-level `LOCAL` after the EXPORT list (363), the same statement as beta 3c's (307): the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`check.sh TrendTest_beta3d.txt TrendTest_beta3c.txt`: kit lint 0 errors; ppl_check_v4 clean, no hard errors; the parse fails on the same statement as beta 3c's.

## Device checklist (emulator first, then G2 and G1)

1. Open TrendTest in the Connectivity Kit and paste over it (never a second copy). Program Catalog → Check: no errors.
2. **TR_P:** Examples → Snoring and heart disease; page 1 reads "Trend (1 df):  χ² = 72.659   p < 0.0001" as before. Esc, Quit. In Home type `TR_P`: expect about **1.54116E-17** (beta 3c gave 0). If it is 0, the Prime's `NORMALD_CDF` loses lower tails too; note it (the review's section 5 asks the same with `NORMALD_CDF(0,1,-8)`).
3. **C-T2:** Menu → Help, Enter, Enter (page 3). The last five gray lines read as above, each whole inside the frame.
4. **C-T3:** the main menu's third line reads "Plot: proportions, trend line", whole; with data loaded it opens the proportions plot.
5. **C-T4:** Enter data → 3 levels → scores 1, 2, 3 → cases 24.5, 30, 40 → totals 100, 100, 100: the message "Cases and totals count people: whole numbers only." and back to the menu. Then the same with 24 cases: the results open.

## Unresolved

- **D11 (open):** Mantel's (N − 1) r² stays the headline; help page 3 now states which programs print Armitage's N r². Whether to show both on a page, or to headline Armitage's, is Roger's call.
- **JMP** is no longer named on help page 3: which form it prints was not checked.
- **The device's `NORMALD_CDF` far in the lower tail** is unverified (the harness uses SciPy, rounded to 12 digits in D1). If the calculator computes it as 1 − upper, `TR_P` is 0 again on the device and the change is harmless but ineffective (checklist step 2).
- **Where the main menu's box cuts** is an estimate from character counts; the emulator decides (step 4).
- The review's improvements 2–6 (section 4) are not in this pass.
