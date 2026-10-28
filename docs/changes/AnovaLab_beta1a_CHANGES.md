# AnovaLab beta 1a: changes from beta 1 (21 Oct 2026)

`AnovaLab_beta1.txt` is untouched. `AnovaLab_beta1a.txt`: 3,771 lines, pure ASCII, LF.
Every finding of `REVIEW2_AnovaLab_beta1.md` (item numbers in brackets), plus the lead's decisions. Not run on hardware or the emulator; PC harness only.

## Tukey (R1, lead decision 1)
- [R1] **Holm is the default post hoc method.** Opening Pairs or Dots computes nothing of Tukey (verify C4: zero NORMALD_CDF calls).
- [R1] **Picking Tukey asks first.** Choosing it (tab, +/-, Menu) shows a one-line CHOOSE "Tukey q crit: about a-b s on a G1" with "Compute it now" or "Not now". "Not now" leaves q crit uncomputed, says so on the page, and does not ask again until α changes.
- [R1] **Tukey p for all pairs or one pair, on request.** More > Tukey p asks with its own estimate. Menu > "Tukey p for this pair" (new) computes only the selected pair, which is one CDF.
- [R1] **The engine tabulates the inner integral once per k.** P_k(x) is computed at x = 0, 0.1, …, 12 (121 points; StudRange's 33/49-node Simpson rule) and read by 4-point cubic Lagrange interpolation, with P_k = 1 for x ≥ 12. The outer 64-interval Simpson rule, the u² substitution and the spike window above df 100 are unchanged. The table survives Set α and the Tukey p button. New routines: `av_BuildT`, `av_PkI`, `av_PrgTick`, `av_TEst`, `av_TukeyAsk`, `av_TukeyP1`. `av_SRCDF` and `av_SRCrit` no longer take k.
- [R1] **Accuracy, re-measured** against `scipy.stats.studentized_range` over k 2–12, df 3–1000 (16 values) and α 0.10/0.05/0.01/0.001:
  - q crit: worst relative error 2.2E-4 (k 12, df 3, α 0.001);
  - tail P(Q > q crit): worst relative error 6.7E-4 of α (k 4, df 100, α 0.001);
  - pair p: worst absolute error 2.7E-6 over q 0.25–9.
  - Measured on a Python replica that matches the PPL to 1E-10 in the harness (verify C1, C2). Help page 3 states it: "q crit within 0.03 %, pair p within 0.00001".
- [R1] **Cost in statement counts** (verify C3; one interpolation is counted as about 3 inner steps):

  | Job | beta 1 NORMALD_CDF calls | beta 1a NORMALD_CDF + interpolations | Fewer by |
  |---|---|---|---|
  | jury q crit | 19,338 | 3,993 + 585 | 3.4 × |
  | insect q crit | 41,454 | 5,929 + 845 | 4.9 × |
  | draft q crit | 38,269 | 5,929 + 780 | 4.6 × |
  | draft q crit + 66 Tukey p | 248,479 | 5,929 + 5,070 | 11.8 × |

- [R1, R8] **Esc and an honest bar.** Esc is read inside the integration: every 8 outer nodes and every 8 table points, with a thin inner bar. The step bar counts every step, labelled "step n (q crit takes 6 to 23)" (the measured range, median 13), and fills at 23, not 12. Verify C4: draft at α 0.001 counts past 12, and Esc stops the job within one tick.

## Two-way (R2, R3; lead decisions 2 and 3)
- [R2] **Cells page re-laid out** for up to 6 × 6 levels.
  - No "x̄ " prefix inside a cell.
  - Numbers are fitted to the cell width (`av_Cmp`: as many decimals as fit, else whole, else "k").
  - Names are shortened to fit (`av_Cut`).
  - n is shown only when there is room.
  - Tap a cell, or use the arrows, for its x̄, n and s in full.
  - Verify C5: 6×6, 3×4, 4×6 and 6×2 designs with long negative means, no text wider than its field under a 6.4-px-per-character model.
- [R3] **Table page, non-significant interaction**: "No evidence of interaction at α = 0.05 / (p = 0.1293). Main effects are averages over / a pattern that may still be there: see Plot." Significant case: "Interaction p = …: evidence that the / effect of A depends on B: compare the cells / (Plot), not the main effects alone."
- [R3] **Plot page** (the plot box is shortened to make room):
  - When the lines cross: "Parallel = no interaction. These lines cross, / but p = 0.129 (n 17-21) cannot rule out chance."
  - When they do not cross: "Parallel lines would mean no interaction. / Here p = … (n …): chance not ruled out."
  - Significant: "Interaction p = …: evidence that / the lines are not parallel in the population."
  - New `av_TCross` and `av_TNs`.

## Variances (R4, R10.3; lead decision 4)
- [R4] **`av_ChiUp` uses the built-in where it is safe.** It returns 1 − CHISQUARE_CDF when x ≤ df, and above df while that keeps 6 digits (> 1E-6). Only the far tail goes to Q(a, x), and the series and fraction caps were raised from 500 to 5000. Verify C7: df 1E4–1E6 at −3 to +9 SD agree with SciPy to 1E-8 relative; n = 1E5 and 1E6, all three alternatives, are checked.
- [R10.3] **No ICDF(1 − p) for a tiny p.** New `av_ChiHi` is the chi-square right-tail quantile: CHISQUARE_ICDF(df, 1 − p) for p ≥ 1E-6, otherwise bisection on ln Q. Checked down to p = 1E-12.

## Checks page (R5; lead decision 5)
- [R5] **The unsourced rule is gone.** The s-ratio line now reads "Largest s / smallest s = 1.55 (a description)".
- [R5] **The bottom line follows Levene.** It reads "Levene: spreads differ, so read Welch's F." (jury), "Welch's F (Table page) is safe either way." (draft), or "Welch's F (Table page) does not assume them." when Levene cannot run.

## Large data (R6; lead decision 6)
- [R6] **Working page above 500 values.** The one-way computation and the two-way read show a Working page with a bar, and Esc stops them with a message; nothing is marked computed.
- [R6] **Medians in one pass.** Values go into a pre-sized block per group; there is no growing CONCAT.
- [R6] **The Dots page draws once into G2.** Later frames copy from G2 and draw the selection on top as orange frames. Verify C9: 2,997 dots drawn once, later frames under 100 RECT_P.
- [R6] The cap stays at 3,000 values; the messages and help page 7 state it. `av_Levels` stops after 7 levels.

## Smaller items (R7, R9, R10; lead decision 7)
- [R7] **CHOOSE with a list variable has a fallback.** It sits inside IFERR; on an error, `av_PickG2` pages through the groups with literal three-item CHOOSEs. It is still on the device checklist.
- [R9] **Factor codes print as integers** ("A=1", not "A=1.000") via `av_Lv`.
- [R10.1] **The header and help page 7 describe the Home exports exactly:**
  - two-way gives AV_F, AV_P and AV_ETA2 for the A×B interaction;
  - blocks gives them for treatments;
  - variances gives the statistic and its p.
- [R10.2] The "α < 0.005: may be a few % off" pairs warning is removed; help page 3 gives the measured accuracy instead.
- [R10.4] σ in the DRAWMENU labels is kept and listed on the device checklist.
- [R10.5] In `av_TCompute`, `tcR` holds only the row list; the Wald SS uses a new `tcSE`.
- [lead 7] The progress bar is honest (above). DATASETS.md's 17–21 matches the header.

## Wording to fit the screen
- **Every on-screen line now fits its field under a stricter width model** (6.4 px per font-1 character, from ChiTable's device note; the harness assumes 5.5).
- **Lines shortened** (beta 1's verify passed them):
  - the Welch line, "F < crit … (α = …)", the pair labels ("Beaut-Avg");
  - the block source and comparison lines;
  - the variance verdicts and the help lines.
- **Layout moves:**
  - the disclaimer is now 4 lines;
  - the band carries N and k on the one-way Table;
  - band titles longer than 38 characters end in "..";
  - the F column uses `av_Cmp(F, 6)`, so a huge F no longer overflows.

## Checks
- **Gate** (`ppl_gate_v1c.py AnovaLab_beta1a.txt AnovaLab_beta1.txt`): **PASS**.
  - kit lint 0 errors; ppl_check clean;
  - lint_ppl 5 known-noise problems;
  - full parse fails at the first file-level LOCAL, the kit's limit (beta 1 the same);
  - fleet_names: 0 collisions, 0 untagged, 0 built-in matches.
- **Verify** (`verify_AnovaLab_beta1a.py`): **8,712 checks, 0 failures**. That is beta 1's checks, adapted to the new defaults and wording, plus Part C, one section per fix.
