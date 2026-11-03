# ChiTable beta 3f: changes

*2 November 2026. Made from beta 3e by a script of exact replacements. 3,616 lines. Fixes for what the monkey test found (the book's vetting point 6, "bulletproof under careless and random use"), and one α the calculator cannot hold.*

## What the monkey test found

`tools/monkey_v1b.py` drives the program in the PC harness the way a careless student might: any key, any tap, menu picks and cancels, odd values typed into the forms (`docs/dev/monkey-fleet-2026-11-01.md`). In 1,000 runs beta 3e gave 894 OK and 106 broken, every one the same finding:

1. **A typed list.** The five forms' fields (the four- and six-count forms, a single count, α) were plain names, which take any type, and a list typed there went on into the table.

Reading the α form for the same check found one more:

2. **An α so small that 1 − α is 1.** The Prime keeps 12 digits, so below about 5E−13 the critical value `CHISQUARE_ICDF(df, 1 − α)` is asked for the point with probability 1, which is infinite. Beta 3e took α = 1E−17 and 1E−300 and drew the table with no critical value.

## What changed (line numbers are beta 3e's)

1. **Every form field takes a real number only**: 18 fields in 5 forms are `{name,[0]}` (`csAskAll` 1722, 1727, 1732; `csEntry` 1822; `csSetAlpha` 3302). On the Virtual Calculator such a field refuses `{1,2}` with "Invalid input" and keeps its value (TTestLab, 1 Nov 2026).
2. **α is taken from 0.0001 to below 1** (`csSetAlpha`, 3303–3305); anything else is refused with "α must be from 0.0001 to below 1 (0.05 is usual, 0.01 is strict). It did not change." The form's help line reads "From 0.0001 to below 1; 0.05 is usual". At 0.0001 the critical value is still a plain number (15.1367 for df = 1).
3. **The observed χ²'s label on the curve page goes left of its line near the right edge** (`csCvDraw`, 2856), as the critical value's label already did. The window ends at 1.15 × χ² when the observed value sets it, so the line can stand 35 px from the edge, and "χ² = 67.20" ran past the screen's right edge. Found by round 4's label check under random use (`text_overlap_v1` with the monkey: "χ² = 12.91" and "χ² = 21.30" past x = 320).
4. Header: the beta 3f block.

Nothing else changed.

## Verification

`verify_ChiTable_beta3f.py`, output `verify_ChiTable_beta3f_output.txt`: **14 PASS, 0 FAIL**, run from a repository layout, with beta 3e read from `programs/` or git history (rule 18). Every run has `prime_facts_v1.py`'s device facts.

- **R** 10 sessions (the three shapes typed, a cell typed alone, α 0.01 and 0.10, the five examples, every page and plot): 109 screens, every text, box and the summary identical to beta 3e's.
- **M** each also run on beta 3e, where it fails: the 18 typed fields; α = 1E−17 and 1E−300 refused, α staying 0.05 with a finite critical value (3.8415; beta 3e: no box, and no critical value); the range's edges (0.0001 and 0.9999 taken; 0.00009999, 1, 0 and −0.05 refused, α unchanged); 0.0001 and 0.9999 on three example tables, every page and plot, with no error and a finite critical value; the new box within 4 lines of 32 characters; three tables whose observed χ² sets the window (50, 5, 5, 50; 30, 10, 10, 30; 40, 2, 3, 41), the label on the screen (beta 3e: past x = 320 at 40, 2, 3, 41).
- **G** only `csAskAll`, `csCvDraw`, `csEntry` and `csSetAlpha` differ; no `!=`; the code ASCII, as before.
- **D** over every screen drawn: no firm overlap, straddle or overrun, and no number cut by its width argument (`label_fit_v1`; beta 3e on the same runs: 1 and 0).

**The monkey test again** (1,000 runs, 150 events each): beta 3f **1,000 OK** (beta 3e: 894).

## Gate

`ppl_gate_v1d.py ChiTable_beta3f.txt ChiTable_beta3e.txt`: **RESULT: PASS**.

## The Virtual Calculator

Virtual Calculator 2.4.2 on Rogers-HP, 2 November 2026, by Claude through computer use. **Check: "No errors in the program."** The checked file in starter pack v9 was collected after that Check and nothing else. Then the program was run and tried by hand: "Set α", the form's help line "From 0.0001 to below 1; 0.05 is usual"; 1E−13 typed was refused with "α must be from 0.0001 to below 1 (0.05 is usual, 0.01 is strict). It did not change."

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] Type `{1,2}` into a count: "Invalid input", the count kept.
- [ ] Set α to 1E−17: the box, α still 0.05.
- [ ] Set α to 0.0001 on example 1: the table and the plot, a critical value of 15.1367.
