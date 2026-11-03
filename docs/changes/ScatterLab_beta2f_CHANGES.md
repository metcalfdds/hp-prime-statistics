# ScatterLab beta 2f: changes

*2 November 2026. Made from beta 2d by a script of exact replacements (24 edits). 2,372 lines. Fixes for what the monkey test found (the book's vetting point 6, "bulletproof under careless and random use"), axis labels and panel numbers that are never cut, and ŷ and ȳ as letters.*

*Beta 2e, made earlier the same day, had items 1 to 6 below. On the Virtual Calculator its side panel printed SSE = 18,053,333,333 as "SSE = 1805333333": the last digit cut off by the panel's width, a number ten times too small. Beta 2e was never committed; beta 2f replaces it.*

## What the monkey test found

`tools/monkey_v1b.py` drives the program in the PC harness the way a careless student might: any key, any tap, menu picks and cancels, odd values typed into the forms (`docs/dev/monkey-fleet-2026-11-01.md`). In 1,000 runs beta 2d gave 978 OK and 22 broken, all at "Type a point":

1. **A typed list** (9 runs). The point form's two fields were plain names, which take any type.
2. **A point the plot cannot hold** (13 runs). A typed x or y of 1E300 went into the window and the fit. Points closer together than the calculator's 12 digits can tell apart (x = 0, 1E−300, 2E−300) gave a window of no width and a division by zero.

The labels were checked at the same time (round 4 of the monkey work: every program's labels), with the new `tools/label_fit_v1.py`:

3. **Labels cut short.** TEXTOUT_P draws at most its width argument (39 px for an x label, 28 px for a y label) and drops the rest. Beta 2d printed y = 100000 as "10000", and 0.0015 and −10000 the same way: a wrong number on the axis.
4. **The corner.** The bottom y label and the first x label share the bottom-left corner. With x from 100 to 300 beta 2d drew "50" over "15"; with x and y either side of 0, "−60" over "−30".
5. **The side panel cut its numbers too** (found on the Virtual Calculator, on beta 2e). Its lines are 86 px wide. With C1 = 1 to 6 and C2 = 100,000 to 500,000 the SSE is 18,053,333,333, and the panel printed "SSE = 1805333333". `label_fit_v1` had looked only at labels that are a number alone; since that evening it looks at every line with a digit in its cut-off part.

## What changed (line numbers are beta 2d's)

1. **The point form takes real numbers only**: `{{tpX,[0]}, {tpY,[0]}}` (`slTypePt`, 1457). On the Virtual Calculator such a field refuses `{1,2}` with "Invalid input" and keeps its value (TTestLab, 1 Nov 2026).
2. **A point the plot cannot hold is refused with a sentence and not added** (new `slPtMsg`), the line the fleet draws (Lessons Learned v7zi; SampDist, CICatcher, Norm3, NormExplorer, StatDist):
   - a number of 50 digits or more: "A number you typed has more than 50 digits: too large to work with. The point was not added.";
   - x or y values closer together than 1E−9, or than |value| × 1E−8 (new `slTiny`): "That point is too close to the others for the calculator's 12 digits. The point was not added."
3. **Loading C1 and C2 is refused the same way** (`slLoadC`, 1365), and nothing is loaded: "C1 or C2 holds a number of 50 digits or more: too large to work with. Nothing was loaded." or "The x or y values in C1, C2 are too close together for the calculator's 12 digits. Nothing was loaded."
4. **The window and the fit treat such a spread as none** (`slAutoWin` 633, `slFit` 693), as they already treated a spread of exactly 0.
5. **Axis labels are never cut** (`slAxes`, 813 and 828; new `slMeas`, `slLab`, `slLabMode`, `slLabNote`; the mode chosen once per window in `slSetRes`, 615). When a tick's label is wider than its room, measured at 5.5 px a character and 3 px a decimal point (Lessons Learned v7zi §6), the axis is labelled in one of two other ways:
   - in units of a power of ten, with a note at the axis: y = 100000 to 500000 is labelled 1 to 5 with "×1ᴇ5" (0.0011 to 0.0042: "×1ᴇ−4");
   - from its lowest tick, when the values sit far from 0 with a small spread: y = 1000001 to 1000006 is labelled 1 to 6 with "y = 1000000 + label".
   The x note sits at the bottom right inside the box, the y note at the top left. At everyday values (the example, the book's data) every label is as before.
6. **The bottom y label is left out** unless it ends before the first x label starts (the two rows overlap in height), measured at 5.5 px for every character, decimal points included, as `text_overlap_v1` measures a firm overlap. The "0" and "0" of an origin corner still fit, so everyday plots are unchanged.
7. **The side panel's numbers fit its 86 px** (new `slFitN`, `slFitT`; `slPanel`). A line is written as before when it fits. When it does not, or when its number is 1E12 or more (which `slSig` writes with no decimals, "4ᴇ12" for 3.78E12), the number is written in the scientific form with as many decimals as fit, up to four: "SSE = 1.8053ᴇ10".
8. **ŷ and ȳ are letters** (`slInit`): `CHAR(375)` and `CHAR(563)` (U+0177, U+0233), not the words "y-hat" and "y-bar" (Roger, 2 Nov 2026: a symbol the Chars menu lacks gets a custom character, as x̄ and p̂ did). The Prime's font holds both, so neither needed one: `SymProbe` beta 1 drew them in fonts 1 and 2 on the Virtual Calculator. The panel, the help pages, the calculus page and the summary in Home use them; lines that named them are shorter.
9. Header: the beta 2f block.

Nothing else changed.

## Verification

`verify_ScatterLab_beta2f.py`, output `verify_ScatterLab_beta2f_output.txt`: **21 PASS, 0 FAIL**, run from a repository layout, with beta 2d read from `programs/` or git history (rule 18). Every run has `prime_facts_v1.py`'s device facts.

- **R** 4 sessions: the example with every menu item (far point, fit, residuals, guess, the calculus page, help, a typed point, delete, C1/C2 saved, cleared and loaded) and three ordinary C1/C2 loads: 67 screens, every text, box and the summary identical to beta 2d's once ŷ and ȳ are read as the words they replace.
- **M** one check per finding, each also run on beta 2d, where it fails:
  - the form's two typed fields;
  - five typed points refused (1E300 as x, −1E300 as y, points 1E−300 apart in x and in y, 1E9 beside 1E9 + 0.001), each with its sentence, the points before them kept, no error (beta 2d: a division by zero, or the point taken);
  - the lines of `slTiny` (a spread of 1E−9 at 0 is enough and 9.9E−10 is not; at 1E9, 11 is enough and 10 is not, since 1E−8 of 1000000010 is 10.0000001);
  - C1/C2 loads refused (1E300; x 1E−300 apart; y within 5E−10), nothing loaded;
  - five datasets whose labels beta 2d cut: none cut, each axis noted as expected;
  - four corners where beta 2d's labels collided: no firm overlap;
  - the largest and smallest accepted (±9.9E49; a spread of exactly 1E−9 at 0; 11 at 1E9; a y spread of 2E−8 at 1) run the fit, a far point, guess and the calculus page with no error, no box, no overlap and no number cut;
  - the side panel at four datasets (C1/C2 as on the Virtual Calculator; y in the millions; x in the hundred-thousands; x and y near −1E9): no line cut short at a digit, the SSE in the scientific form when too long (beta 2d cut 38 lines);
  - ŷ and ȳ over the whole tour: ŷ 36 times, ȳ 32 times, the words never, and ŷ in the summary returned to Home (beta 2d: the words in 68 texts);
  - every new box within 4 lines of 32 characters.
- **G** only `slAutoWin`, `slAxes`, `slFit`, `slInit`, `slLoadC`, `slPanel`, `slSetRes`, `slTypePt` and the new `slFitN`, `slFitT`, `slLab`, `slLabMode`, `slLabNote`, `slMeas`, `slPtMsg`, `slTiny` differ; no `!=`; the code ASCII, as before.
- **D** over every screen drawn (229 distinct): no firm overlap, straddle or overrun (beta 2d on the same runs: 10), and no number cut by its width argument (beta 2d: 114).

**The monkey test again** (1,000 runs, 150 events each, C1 and C2 announced as written; `tools/monkey_chunks_v1.py`, the same seeds as `monkey_v1b.py`): beta 2f **1,000 OK** (beta 2e: 1,000 OK; beta 2d: 978).

## Gate

`ppl_gate_v1d.py ScatterLab_beta2f.txt`: **RESULT: PASS** (the kit's parser stops at `EXPORT` as it does on beta 2d: its known limit).

## The Virtual Calculator

Virtual Calculator 2.4.2 on Rogers-HP, 2 November 2026, by Claude through computer use. **Check: "No errors in the program."** The checked file in starter pack v9 was collected after that Check and nothing else. Then the program was run and tried by hand (beta 2f): with C1 = 1 to 6 and C2 = 100,000, 250,000, 180,000, 420,000, 390,000, 500,000 loaded, the y axis read 1 to 5 with "×1ᴇ5", nothing cut, and the side panel "ŷ = 40667", "+ 76000 x", "SSE = 1.8053ᴇ10", "x̄ = 3.500", "ȳ = 306667", every line whole; the calculus page ended "a = ȳ − b x̄."; the summary returned "ScatterLab: n = 6, ŷ = 40667 + 76000 x, r = 0.9211, SSE = 18053333333". ŷ and ȳ drew as letters. Beta 2e, the same afternoon, refused a typed x of 1E300 with "A number you typed has more than 50 digits: too large to work with. The point was not added." and labelled the same axis in units, but its panel printed the SSE as "SSE = 1805333333": the fault beta 2f fixes.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] Type a point with x = 1E300: the box, and the point not added.
- [ ] Clear, type (0, 0) then (1E−300, 1): the "too close" box.
- [ ] Load C1 = 1, 2, 3, 4, 5, 6 and C2 = 100000, 250000, 180000, 420000, 390000, 500000: y labelled 1 to 5 with "×1ᴇ5", nothing cut.
- [ ] Load C1 = 100, 150, 220, 300, 260 and C2 = 20, 35, 41, 50, 28: no label over another in the bottom-left corner.
- [ ] The example: labels as in beta 2d.
- [ ] With C1 = 1 to 6 and C2 = 100000 to 500000 loaded: the panel's "SSE = 1.8053ᴇ10", whole.
- [ ] ŷ and ȳ on the panel drawn as letters, not boxes (or run `SymProbe` from `_dev_2026-11-02`: its first two rows).
