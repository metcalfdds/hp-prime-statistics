# PowerViz v2.5l: changes

*2 November 2026. Made from v2.5k by a script of exact replacements (32 edits). 4,050 lines. Fixes for what the monkey test found (the book's vetting point 6, "bulletproof under careless and random use"), and labels that keep to their places at the edges of what the forms take.*

## What the monkey test found

`tools/monkey_v1b.py` drives the program in the PC harness the way a careless student might: any key, any tap, menu picks and cancels, odd values typed into the forms (`docs/dev/monkey-fleet-2026-11-01.md`). In 1,000 runs v2.5k gave 736 OK and 264 broken:

1. **A typed list** (241 runs). The eight forms' fields were plain names, which take any type.
2. **A mean or σ of 1E300** (20 runs): numbers no plot can hold went on into the arithmetic; one ran into a division by zero on the "Would Levene notice?" page (`pv_LvPage` → `pv_FPow`).
3. **A σ of 1E−300** (3 runs): the numbers on the panel asked `STRING(x, 2, 302)`, and the Prime takes at most 12 decimals ("Invalid input").

The labels were checked at the same time (round 4: every program's labels), at the corners of what the forms take. With means of a million, or a σ of 0.000001, v2.5k's numbers ran off the right edge of the screen ("2000000", "0.0000010") and over each other: 29 firm overlaps on the verify script's runs.

## What changed (line numbers are v2.5k's)

1. **Every form field takes a real number only**: 29 fields in 8 forms are `{name,[0]}` (`pv_EditForm` 2360–2385, `pv_EditN` 2445 and 2453, `pv_EditEff` 2476). On the Virtual Calculator such a field refuses `{1,2}` with "Invalid input" and keeps its value (TTestLab, 1 Nov 2026).
2. **Means and σ the plot cannot hold are refused with a sentence** (new `pv_BadMsg`, above `pv_EditForm`), and every value goes back to what it was:
   - a mean or σ above 1,000,000: "Means and σ can be at most 1,000,000: use bigger units (thousands, millions)." A million is far beyond any power problem in the book, and it keeps every number on the panel and the axes to a width the screen can show;
   - a σ below 0.000001, or below a millionth of the larger mean: "σ is too small next to the means for the calculator's 12 digits. Use a larger σ or means nearer 0.";
   - for two means with unequal σ, σ₂ from 0.01 to 100 times σ₁: "σ₂ must be from 0.01 to 100 times σ₁.";
   - means that differ, but by less than a billionth of the larger σ: "The means differ by under a billionth of σ: no n could tell them apart." The n for 80% power is ((z_α u + z_β w)/|μ₁ − μ₀|)², and at μ₀ = 1E−300, μ₁ = 0, σ = 999,999 it is about 1E612, past the largest number the Prime holds (found by the monkey test's retest of this version; see below). Above the line n stays below about 1E25. Equal means are still taken: no effect, and the panel says no n is enough. The arrows and the drag snap μ₁ to the grid of the effect step, and with μ₀ = 1E−300 a step to 0 left the same difference of 1E−300: new `pv_Snap0`, called from `pv_StepEff` (3546) and the drag in `pv_Touch`, takes means that close as equal.
   The setup form (`pv_EditForm`) adds "Nothing changed." and keeps its last good values; the effect form (`pv_EditEff`) adds "The mean did not change." The check runs again after the form's own clamps (a σ₂ of 0 reset to 1 can then be too small next to σ₁ = 1000).
3. **Numbers keep to their places**:
   - new `pv_TxW` (a text's width at 5.5 px a character, 3 px a decimal point) and `pv_Fit` (a number too wide for its room is written in scientific form, 1.23ᴇ6), above `pv_DLbl`;
   - the distribution labels (`pv_DLbl`, 1438) and the panel's cells (`pv_Panel`, 1680) go through `pv_Fit`;
   - `pv_NumD` (993) writes values of 10,000,000 or more in scientific form;
   - the x-axis labels (`pv_Draw`, 1765) are left out when one would run into the one before it or past the right edge; the H₀ and H₁ labels stand side by side when the two curves are within 16 px;
   - the SE line (`pv_SELine`, 1457) shortens to its symbolic form, then to the value alone, when it would run into the n₈₀ text on its row, measured at 5.5 px for every character, decimal points included, as the overlap check measures (with 3 px a point, test 4's "SE₀ = √(2×0.975×0.025/4990) = 0.00313" seemed to fit and the check saw it reach "n₈₀ = 3826": round 4's label check under random use);
   - on the power curve (`pv_PCDraw`, 2062) "0.80" moves aside when the formula label would reach it;
   - the formula page (`pv_Formula`, 2536) wraps a line wider than the screen, keeping its colours, and "Round UP (whole people)" drops "(whole people)" when it would not fit.
   At everyday values every screen is as before.
4. Header: the name v2.5l and its "what changed" block.

Nothing else changed.

## Verification

`verify_PowerViz_v2.5l.py`, output `verify_PowerViz_v2.5l_output.txt`: **28 PASS, 0 FAIL**, run from a repository layout, with v2.5k read from `programs/` or git history (rule 18). Every run has `prime_facts_v1.py`'s device facts.

- **R** the five tests (first form, arrows, +/−, the n form, Power vs n, Power vs effect, the formula, Would Levene notice?, 1/2-sided, the exit box): 135 screens, every text, box and the returned power identical to v2.5k's.
- **M** each also run on v2.5k, where it fails:
  - the 29 typed fields;
  - eleven crash and edge inputs (σ = 1E300, μ₁ = 1E300, μ₀ = −1E300, σ = 1E−300, μ₀ = 10⁶ with σ = 0.5, σ₂ = 1E−300, σ₁ = μ₂ = 1E300, μ₀ = 1234567890123, σ₂ = 101 σ₁ and 0.009 σ₁, μ₀ = 1E−300 with μ₁ = 0 and σ = 999,999): each refused with its sentence, the values kept, the plot drawn;
  - the lines of `pv_BadMsg` (1,000,000 taken and above refused; σ = 0.000001 taken and 0.00000099 refused; at |μ| = 10⁶, σ = 1 taken and 0.99 refused; the σ₂/σ₁ range; means 1E−9 of the larger σ apart taken, closer refused, equal taken);
  - test 5 with σ₁ = 1000 and σ₂ = 0: the clamp's box, then the refusal;
  - the effect form: 1E300, −1E60, 1,000,001 and 1E8 refused, 3 at σ = 0.000002 refused, 106 and −1,000,000 taken;
  - eleven corners of the ranges run every page with no error and no refusal, and no firm overlap or text off the screen on any of their screens (v2.5k on the same runs: 27);
  - the arrows at μ₀ = 1E−300, σ = 999,999: μ₁ steps from 15 onto 0, is taken as μ₀, and the next step goes on to −50,000, with no error (v2.5k: an overflow in `pv_NCF`);
  - the SE line at p = 0.97 and 0.98 with n = 4990 and 5000: shortened to the value alone, no firm overlap (v2.5k: over n₈₀);
  - every new box within 4 lines of 32 characters.
- **G** only the forms, the new `pv_BadMsg`, `pv_Snap0` (with its calls in `pv_StepEff` and `pv_Touch`), `pv_TxW` and `pv_Fit`, and the layouts named above differ; every new routine is defined above its first call; no `!=`; no glyph on screen that v2.5k does not already show.
- **D** over every screen drawn (322 distinct): no firm overlap, straddle or overrun (v2.5k on the same runs: 32), and no number cut by its width argument.

**The monkey test again** (1,000 runs, 150 events each): v2.5l **1,000 OK** (v2.5k: 736), on the final build, run with a processor to itself. (A batch of the same build run beside three other jobs, when one of them was stopped for memory, gave 999 and one run with no end within 30 seconds, seed 1000463; replayed alone it ended in 4.2 seconds, and three copies at once in 12.5 seconds each.) The first two retests of this version each broke once, both at seed 1000164: 999 OK and an overflow in `pv_NCF`, means differing by 1E−300. The first was closed at the forms (`pv_BadMsg`), the second at the arrows and the drag (`pv_Snap0`).

## Gate

`ppl_gate_v1d.py PowerViz_v2.5l.txt PowerViz_v2.5k.txt`: **RESULT: PASS**.

## The Virtual Calculator

Virtual Calculator 2.4.2 on Rogers-HP, 2 November 2026, by Claude through computer use. **Check: "No errors in the program."** The checked file in starter pack v9 was collected after that Check and nothing else. Then the program was run and tried by hand: One-Sample Mean with σ = 1E−300 typed was refused with "σ is too small next to the means for the calculator's 12 digits. Use a larger σ or means nearer 0." and "Nothing changed."; with μ₀ = 1,000,000, μ₁ = 999,990, σ = 15 and n = 30 the plot drew every x label whole ("999940" to "1000040", none touching), power 0.291 and n₈₀ = 155, and the result box gave POWER = 0.2914 (β = 0.7086) with EP_PWR and EP_NPG exported.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] One-sample mean, σ = 1E300: the box ending "Nothing changed.", the old plot back.
- [ ] One-sample mean, σ = 1E−300: the "too small" box (v2.5k: "Invalid input").
- [ ] Means 1,000,000 and 999,990 with σ = 50: the plot, every label on the screen, none over another.
- [ ] Two means, unequal σ: σ₁ = 1000, σ₂ = 0: the reset box, then the σ₂ range box.
