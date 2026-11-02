# SampDist v2.3e: changes

*1 November 2026. Edited from v2.3d by hand. 1,849 lines. Fixes for what the monkey test found (the book's vetting point 6, "bulletproof under careless and random use"), and for three more faults that trying those fixes on the Virtual Calculator turned up.*

## What the monkey test found

`tools/monkey_v1a.py` drives a program in the PC harness the way a careless student might: any key, any tap, menu picks and cancels, odd values typed into the forms (`docs/dev/monkey-fleet-2026-11-01.md`). Over 1,000 runs (150 events each, seed 11) SampDist v2.3d gave:

| Verdict | Runs | Cause |
| --- | --- | --- |
| OK | 648 | |
| HARNESS | 307 | a list typed into a number field went on into the arithmetic (`<`, `<=`, `-`, `+` between a list and a number) |
| CRASH | 40 | division by zero: the graph's window had zero width |
| GUARD | 5 | `NORMALD_ICDF(0, 1, 1)` (4) and `NORMALD(0, 0, 0)` (1), values the calculator has never been seen to answer |

1. **A typed list.** The ten forms' fields were plain names, which take any type.
2. **A curve too narrow for the window's own arithmetic.** At μ = 1E300, σ = 1E−300 or n = 1E300 the window μ ± 4σx̄ has zero width in 12 digits, and the grid divides by it ("Error: X/0" on the calculator).
3. **`NORMALD_ICDF(0, 1, 1 − α)`.** For a tiny α, 1 − α is exactly 1 in 12 digits, and the upper critical value was ICDF(1), infinity.

## What the Virtual Calculator found (1 Nov 2026, evening)

The harness counts in 16 digits and prints any number of decimals, so it could show none of these. Each was seen on the Virtual Calculator in v2.3d:

4. **A tick loop that never ends.** μ = 10⁹, σ = 0.001, n = 1, left tail, a = 999,999,999.999: no graph for two minutes; On gave "Program interrupted". The window, 999,999,999.996 to 1,000,000,000.00, holds only a few 12-digit numbers; the tick step is 0.0005, and `xv := xv + stp` soon rounds back to `xv`, so `WHILE xv <= xhi` never ends.
5. **`STRING(x, 2, d)` takes at most 12 decimals.** Typed in Home: `STRING(0.5,2,13)`, `STRING(5*10^(-13),2,13)` and `STRING(2*10^(-44),2,44)` are "Error: Invalid input"; `STRING(5*10^(-12),2,12)` is "0.000000000005". The density axis's labels take more decimals the larger σ is: μ = 0, σ = 10¹², n = 1, left tail gave "SampDist Error: Invalid input". Under `monkey_v1b.py`, which teaches the harness this, v2.3d stops so in 33 of the 1,000 runs (628 OK).
6. **Labels in the margin.** At σ = 15,000 (an income, say) the density labels ("0.00015") ran into the axis; at σ = 10¹⁰ they were 13 characters long, and the panel's σ line was cut at its right edge.

## What changed (line numbers are v2.3e's)

1. **Every form field takes a real number only** (all 10 forms, 28 fields: 1092, 1097, 1117, 1120, 1406, 1430, 1435, 1478, 1533, 1583): `{mu,[0]}`, `{sg,[0]}`, …, the User Guide's allowed-types form. On the Virtual Calculator `{1,2}` pasted into μ got "Error: Invalid input", and the field kept its 0 (below).
2. **Numbers the graph cannot draw are refused with a sentence** (`sd_Big`, `sd_Narrow`, `sd_BadMsg`, 712–752), on every form, after the form's own checks (σ > 0, n ≥ 1 and whole):
   - a number with more than 50 digits: "A number you typed has more than 50 digits: too large to work with." Its square, which the densities take, would pass the Prime's 1E499;
   - σ above 10¹⁰ (cause 5; 745): "σ can be at most 1E10: a larger σ needs density labels with more decimals than the calculator prints." At σx̄ = 10¹⁰ the labels need 11 decimals. The limit is on σ itself, because n− in the live graph can go back to n = 1;
   - σx̄ = σ/√n below 0.000000001 or below |μ|/100,000,000 (causes 2 and 4): "σ/√n is too small next to μ for the calculator's 12 digits. Use a larger σ, a smaller n or a μ nearer 0." At that line the window still holds about 800 distinct 12-digit numbers.
   - In the live graph the μ, σ form (1105) refuses the same way and adds "Nothing changed."; n+, n− and n×4 stop where σx̄ would get too small, with "n stops here: σ/√n would be too small to draw" on the panel (1071).
   - A bound of 50 digits or more is refused: in Find probability (1441) the box, then the menu; in the live graph's bounds form (1128) "… The bounds did not change."
3. **The upper-tail critical values are `−NORMALD_ICDF(0, 1, α)`** (sd_crit 663 and 668, Mode 2 1505 and 1510), not `NORMALD_ICDF(0, 1, 1 − α)` (cause 3). The same numbers for every α the panel shows; finite for α = 1E−300 (37.0471, SciPy's).
4. **Labels** (cause 6, and the six firm overlaps v2.3d's change note left in sd_compose):
   - an x tick label that would touch the one before it is left out; its tick stays (sd_axes 594, sd_drawCmp 1308). At μ = 10⁹ the labels alternate: 999999600, 999999800, 1000000000, 1000000200;
   - a density label of 7 characters or more is written `STRING(x, 3, 1)`, "1.5ᴇ-4" (seen on the Virtual Calculator), a whole mantissa without its ".0" ("1ᴇ-11"), and left out if it still does not fit (618);
   - the panel's σ line, when longer than 50 characters (σ of 10⁸ and up), leaves out its σ/√n step (sd_compose 854, sd_watch 1717).
5. Header: the v2.3e block.

Nothing else changed.

## Verification

`verify_SampDist_v2.3e.py`, output `verify_SampDist_v2.3e_output.txt`: **33 PASS, 0 FAIL**, run from a repository layout, with v2.3d read from git history (rule 18). It is a new script in the repository's layout. Every run in it has `prime_facts_v1.py`'s device facts, so `STRING(x, 2, d)` with d ≥ 13 fails there as on the Prime.

- **A** the arithmetic against SciPy: `sd_prob` (216 cases), `sd_crit` (three tails, six α, and α = 1E−300), Find probability and Find critical value end to end (the exported `EP_SD_*`).
- **B** every mode and Help from the menu, no error.
- **M** one check per finding, each also run on v2.3d, where it fails:
  - M1: the 10 forms' 28 fields are all `{name,[0]}`; v2.3d's were bare names.
  - M2: the crash inputs (μ = ±1E300, n = 1E300, μ = 1E40 with σ = 1, σ = 1E−300, in every mode) get their sentence and the program is back at its menu; v2.3d stops with a division by zero. For μ = 10⁹, σ = 0.001, where v2.3d draws in the harness, the check runs v2.3d's tick loop in 12-digit decimals (stuck after 1 or 5 steps, whichever way a half rounds) and cites the Virtual Calculator's "Program interrupted".
  - M3: the lines (σx̄ 1E−9 accepted, 9.9E−10 refused; at μ = ±10⁹, 10 accepted and 9.99 refused; 9.99E49 accepted, −1E50 refused).
  - M4: the live graph at μ = 10⁹, σ = 100: n×4 goes 1, 4, 16, 64 and stops with the note; v2.3d went on to 1,024.
  - M5, M6: the live μ, σ form and a bound of −1E60.
  - M7: the largest and smallest numbers accepted draw in every mode with no error and no box (μ = 10¹⁸ with σ = 10¹⁰, a bound of 9.9E49, σ = 1E−9, n = 10¹²).
  - M8: every new box fits 4 lines at 32 characters.
  - M9: σ above 10¹⁰ refused in every mode and in the live form; v2.3d stops with "Invalid input" at σ = 10¹² and at 5E11 in Watch.
  - M10: every density label ends left of the axis and the σ line is at most 50 characters, at σ = 15,000, 10¹⁰ and 1E−9; v2.3d's labels ran into the axis and its σ line was 57 characters.
- **G** static: every routine tagged `sd_`, only the program's verified glyphs in strings, no `!=`.
- **D** text_overlap_v1 over every screen drawn (346 distinct): no firm overlap, straddle or overrun.

**The monkey test again** (1,000 runs, seed 11): v2.3e **1,000 OK** under `monkey_v1a.py` and under `monkey_v1b.py`.

## Gate

`ppl_gate_v1d.py SampDist_v2.3e.txt SampDist_v2.3d.txt`: **RESULT: PASS**. Kit lint 0 errors, no hard errors; lint_ppl v3's 18 lines are v2.3d's (GROB parameters of the drawing helpers) at their new line numbers. `fleet_names_v2.py` over all 30 programs with v2.3e and BayesTree beta 8f: 2,264 routine names, 0 collisions.

## Tools

- **`tools/prime_facts_v1.py`** (new): the device facts the harness does not model yet, applied to it by a patch, each with where and when it was seen: `STRING(x, 2, d)` is "Invalid input" for d ≥ 13; `STRING(x, 3, d)` writes the small capital ᴇ. The harness's next version is to absorb them.
- **`tools/monkey_v1b.py`** (replaces v1a): v1a with the device facts applied; the same seed gives the same run.

## The Virtual Calculator (1 Nov 2026, 17:46–18:13 CST)

Virtual Calculator 2.4.2 (build 2026-09-09), calculator `Prime`, Rogers-HP, by Claude through computer use. Programs were copied in with the calculator closed, built by hp-prime-kit.

1. **v2.3d** (the checked file already there): the stall (cause 4) and the σ = 10¹² stop (cause 5), as above.
2. **Home:** the `STRING` results of cause 5; `STRING(0.00015,2,1)` = "1.5ᴇ-4", `STRING(4*10^8,3,1)` = "4.0ᴇ8", `STRING(0.00015,3,1)` = "1.5ᴇ-4", `STRING(150000000,3,1)` = "1.5ᴇ8".
3. **v2.3e, Check:** "No errors in the program" (the build before change 4's last two items, then the final build).
4. **v2.3e, runs:**
   - `{1,2}` pasted into μ: "Error: Invalid input", μ kept its 0;
   - μ = 10⁹, σ = 0.001, n = 1: the σ/√n box at once (4 lines), then the menu;
   - σ = 10¹², n = 1: the σ box (4 lines), then the menu;
   - σ = 10¹⁰, n = 1, left tail: the graph, no error (the largest σ accepted; this build still wrote "0.00000000004" in the margin and cut the σ line, change 4's last items);
   - σ = 15,000, n = 30 (final build): density labels "1.5ᴇ-4", "1.0ᴇ-4", "5.0ᴇ-5", clear of the axis;
   - μ = 10⁹, σ = 100, n = 1, left tail: x labels 999999600, 999999800, 1000000000, 1000000200, none touching; n×4 five times: n = 64, σx̄ = 12.5, "n stops here: σ/√n would be too small to draw".
5. **The checked file** (163,692 bytes, +3,240) was collected after a Check and nothing else, and read back equal to `programs/SampDist_v2.3e.txt`. Starter pack v7 carries it.

## Device checklist (G1 and G2)

1. Find probability, μ = `{1,2}`: the form refuses it ("Invalid input") and stays open.
2. Find probability, μ = 1E9 (EEX 9), σ = 0.001, n = 1: the σ/√n box, then the menu, at once.
3. Find probability, σ = 1E12, n = 1: the σ box, then the menu.
4. Find probability, μ = 1E9, σ = 100, n = 1, left tail, OK; in the live graph tap n×4 five times: n goes 1, 4, 16, 64, then "n stops here: …" on the panel. The x labels under the axis must not touch each other.
5. Find probability, σ = 15000, n = 30: the density labels read 1.5ᴇ-4 and so on, clear of the axis.
6. Find critical value, α = 1E−300 (EEX −300), upper tail: a finite value (about μ + 37 σx̄).
7. Compare sample sizes and Watch sample means with ordinary numbers: as in v2.3d.

## Unresolved

- The harness still counts in 16 digits; a 12-digit model of the stalled loop is in the verify script, and the real case was seen on the Virtual Calculator only.
- A refused form opens again with the program's defaults, not the student's numbers (as in v2.3d).
