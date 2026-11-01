# TTestLab beta 1b: changes

*31 October 2026, night. Built from beta 1a by `make_ttl1b.py` (exact replacements). 1,319 lines. The fixes from the independent second review of beta 1a (`REVIEW2_TTestLab_beta1a.md`, 31 Oct 2026: a reviewer that had not seen the program, with its own SciPy, the harness, the gate tools and the author's verify script). Six of the review's calculator items have run on the Virtual Calculator (below).*

## Where beta 1a had run

`TTestLab_beta1a_CHANGES.md` and the NOTES said "harness only". The review pointed out that beta 1a had in fact run on the Virtual Calculator 2.4.2 the same evening: Check clean and example 1 to the end from the starter pack v1 (`StarterPack_v1_NOTES.md`), and the two financial-aid groups DataLoad had put in D1 and D2 (t(421.19) = −1.68, p = 0.094; `DataLoad_beta1_NOTES.md`). beta 1b's header says so.

## What changed (the review's finding numbers)

1. **Tails and α change together** (`tt_AskTails`, lines 1039–1061). The new tails waited in a local until an α was chosen; a cancelled α list now leaves both as they were. Before: Tails → one-tailed → Esc at the α list left "one-tailed" on screen over the two-tailed t crit (±1.993) and p (0.031); the right one-tailed values are −1.666 and 0.016. The menu now calls `tt_Calc` after the dialog whatever it returned (line 1217).
2. **The data source, the names and the example change only once new numbers are in** (`tt_AskData`, lines 1065–1130). `ttSRC`, `ttG1`/`ttG2`, `ttEX` and `ttDV` are set after each form's OK or a successful D1/D2 read. Before: a refused pairs read after a typed summary left `ttSRC = 2` with no pairs, and the next page read past an empty list; a cancelled form stripped the example's names and its step-4 note. (Review 2 and 6.)
3. **"Pooled or separate?" refuses numbers that gave no t** (`tt_Compare`, lines 849–853): "The numbers on screen give no t: Edit the numbers first." Before: N₁ = 1, or both SDs 0, divided by zero in `tt_Ind`.
4. **p never prints 0.000** (`tt_FmtP`, lines 223–231): anything below the floor, a 0 from an underflowing `STUDENT_CDF` included, prints "< 0.001"; exactly 1 prints "1.000" (t = 0). Before, 10,000 pairs at d = 0.5 (t = 50) printed "p = 0.000".
5. **The decision line prints t obt to 3 decimals** (lines 809, 819), like the t crit beside it. Before: "t obt = 2.23 is not beyond t crit = ±2.228". The Report line keeps 2 (APA).
6. **A typed N is its whole part** (line 1089, `IP`), as the pairs form did. Before: N₁ = 10.5 gave df 18.5 and "t(18.5)".
7. **t crit beyond the plot's window** (`tt_Curve`, lines 582–591; `tt_Step3`, line 709): the dashed line sits at the window's edge with a red "t crit" label, and the rule reads "(t crit lies beyond the plot.)" instead of promising a red region. Happens with 2 pairs (t crit 12.706) and at df 1–3 in the last column. The "t obt" label is kept inside the plot at the conservative character width (line 598).
8. **A negative typed sD** gets "An SD cannot be negative." (line 444); sD = 0 keeps its own message.
9. **The pairs guard runs before the SD of the differences is formed** (lines 441–443): one pair is refused instead of dividing by zero (unreachable through the forms; `tt_Calc` called directly).
10. **Text:** help 1 "sample 1 (or x₁) in D1" (line 1180); the pairs print with one decimal count per column, the most any value in the column needs (`tt_NDec`, `tt_ColDec`, `tt_FixD`, lines 245–271; step 1 lines 638–646): 1.30, 1.00, 1.10 as the lecture's Table 11.3; the table-row line "(Table row 120, ±1.980, decides the other way.)" (line 829; 47 characters); step 4's SE and t lines sit right under a typed summary (line 796; they were 100 px below it); Help from the start menu returns to that menu (lines 1299–1305; it used to go on to example 1 unasked).

**Considered and left:** the dependent form's prefill (the current differences' mean and SD, rounded as `tt_Num` shows them) stays: "Edit the numbers" edits the numbers on screen. `tt_Num` rounds a typed SD of 0.000001 to "0" on step 1 while the arithmetic uses it: extreme inputs only.

## Verification

`verify_TTestLab_beta1b.py`, output `verify_TTestLab_beta1b_output.txt`: **84 PASS, 0 FAIL**. beta 1a's 59 checks and a new section R with one check per finding: tails chosen then α cancelled (nothing changes) and both chosen (both change); the refused pairs read after a typed summary (ttSRC stays 1, step 1 redraws); compare with N₁ = 1 and with both SDs 0; `tt_FmtP` at 0, 1E−320, 0.0004, 0.0005, 0.0314, 0.9994, 0.9996, 1; 10,000 pairs ("p < 0.001"); t = 0 ("p = 1.000"); 2.226 vs ±2.228; a cancelled form after example 1 and after Choose the test → dependent (names, outcome and test kept); N₁ = 10.5 → df 18; 2 pairs (the rule's wording, two "t crit" labels, the dashed line's columns at x = 12 and 308) and example 1 (no label, the red-region wording); a negative sD; one pair to `tt_Calc`; help 1; the pairs' decimals; `tt_ColDec` and `tt_FixD`; the table-row line; step 4's y's for a typed summary (60, 73) and for pairs (141, 154); Help from the start menu. **Run on beta 1a, 16 of the R checks fail** (every finding), and beta 1a's own checks still pass.

text_overlap_v1 over 92 distinct screens from every path: no overlap, straddle or overrun, firm or marginal.

## Gate

`ppl_gate_v1c.py TTestLab_beta1b.txt TTestLab_beta1a.txt`: **RESULT: PASS** (kit lint 0 errors; no hard errors; the parse stops at the first file-level `LOCAL`, the kit tool's limit). `fleet_names_v2.py` over all 29 programs: 2,203 routine names, 0 collisions, 0 built-in matches (a first build named a counter `ci`, which the gate caught as `Ci`). `case_scan_v1.py`: nothing to report.

## The run on the Virtual Calculator (31 Oct 2026, 21:36–21:43 CDT)

Virtual Calculator 2.4.2 (build 2026-09-09), calculator `Prime`, Rogers-HP; by Claude through computer use. beta 1a's `TTestLab.hpprgm` set aside to `Documents\HP Prime\_set_aside_2026-10-31\vc_before_ttestlab_beta1b`; beta 1b's built by hp-prime-kit (105,700 bytes) copied in; Check: "No errors in the program". (The file that ran differs from the one in `programs/` and the starter pack v3 in two header comment lines only, the firmware note written after the run.)

- **13 (tails cancelled):** example 1 → Menu → Tails and α → "One-tailed: μ₁ < μ₂" → Esc at the α list: step 1 reads "Pooled-variances t test, two-tailed, α = 0.050"; Quit gave "TTestLab: t(73) = −2.20, p = 0.031, two-tailed". The Tails menu's items showed μ₁ ≠ μ₂, μ₁ < μ₂, μ₁ > μ₂ (item 19: glyphs inside a `CHOOSE` list render).
- **14 (refused pairs read):** DataLoad had put M2's columns in D1 (9 values) and D2 (10). Choose the test → No → OK → Type mean, SD (0.5, 1, 5) → two-tailed, .05 → step 4 → Menu → Edit the numbers → Pairs in D1 and D2: the box "Put the pairs in D1 and D2 … the same number of values in each", then step 4 drew again with the typed summary, no error.
- **Step 4 for a typed summary:** "x̄D = 0.5, sD = 1, N pairs = 5" with "SE = sD/√N = 1.000/√5 = 0.4472" and "t obt = … = 1.12" right under it.
- **16 (p underflow):** Edit the numbers → 0.5, 1, 10000 → step 5: "t obt = 50.000 is beyond t crit = ±1.960", "Report t(9999) = 50.00, p < 0.001, two-tailed", the t obt label inside the plot at the right edge.
- **15 (compare after a refusal):** Choose the test → Yes → Yes → OK → Type, N 1 = 1 → "Each group needs N of at least 2." → Menu → Pooled or separate?: "The numbers on screen give no t: Edit the numbers first."
- **18 (2.226 vs 2.228):** Edit the numbers → 1.2852, 1, 6, 0, 1, 6 → step 5: "t obt = 2.226 is not beyond t crit = ±2.228: RETAIN H₀.", "Report t(10) = 2.23, p = 0.050, two-tailed"; Quit: "TTestLab: t(10) = 2.23, p = 0.050, two-tailed".
- Driving note: a form field took "1,000" when "10000" was typed quickly (a key press missed, Lessons Learned §16); typing the digits one at a time worked.

**Not run there:** 17 (2 pairs in D1/D2: the edge labels), 20–22 (line widths at α .0005, the tick labels), the cancelled form after an example (6), the fractional N (7), the negative sD (8), Help from the start menu (10). All ran in the harness.

## Device checklist (G1 and G2; the Virtual Calculator items above can be repeated there)

`TTestLab_beta1_NOTES.md` items 1–11, `TTestLab_beta1a_CHANGES.md` item 12, and from the review:

13. Example 1 → Menu → Tails and α → one-tailed μ₁ < μ₂ → Esc at the α list: step 1 still two-tailed, ±1.993, p = 0.031. Then the same with α .05 chosen: t crit −1.666, "p = 0.016, one-tailed".
14. Dependent samples typed (0.5, 1, 5) → Menu → Edit the numbers → Pairs in D1 and D2 with D1 empty or of another length than D2: after the box, the page draws again without an error dialog.
15. Independent, N 1 = 1 typed → the refusal box → Menu → Pooled or separate?: the "give no t" box, no error dialog, no ∞.
16. Dependent typed x̄D 0.5, sD 1, N pairs 10000: step 5 "p < 0.001", not "p = 0.000". In Home, note what `STUDENT_CDF(9999,−50)` returns (0 or a tiny number): it decides whether the Prime ever reaches the underflow.
17. Dependent, 2 pairs in D1/D2 (1, 2.5 and 1.5, 2) at α .05: step 3 reads "(t crit lies beyond the plot.)", a dashed red line at each edge of the plot with "t crit" beside it; step 5 the same lines with t obt inside.
18. Pooled, N 6/6, SDs 1, means 1.2852 and 0: step 5 "t obt = 2.226 is not beyond t crit = ±2.228".
19. The Tails menu's items show μ₁ ≠ μ₂, μ₁ < μ₂, μ₁ > μ₂ (seen on the Virtual Calculator; confirm on the G1).
20. Example 3 → Edit the numbers → mean 2 = 5.5476: step 5's "(Table row 120, ±1.980, decides the other way.)" fits whole.
21. Step 1 at one-tailed α .0005: "Separate-variances t test, one-tailed, α = 0.0005" fits whole (49 characters of font 1).
22. The tick labels under the curve print the Prime's minus (−4 … 4) and −12 … 12 when the window is capped.
23. Example 1 → Menu → Edit the numbers → Type → Cancel: step 1 still names Hispanic / Non-Hispanic white and "Outcome: age at arrest (years), JDCC"; step 4 still shows the lecture's rounding note.
24. Independent form with N 1 = 10.5: step 2 "= 10 + 10 − 2 = 18", "t(18)".
25. Dependent form with sD −1: "An SD cannot be negative."
26. The start menu → Help → both pages → the start menu again (not example 1).

## Unresolved

- The reviewer could not see the lecture note: whether its "closest row" rule is what it does between rows 30 and 120 for a fractional df (TTestLab's tie rule, to the smaller row, is the author's choice), and which separate-variances formulas it teaches (TTestLab uses Welch's). Roger's call.
- `STUDENT_CDF`'s behavior below 1E−499 on the firmware (item 16).
