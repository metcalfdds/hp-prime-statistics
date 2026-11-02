# CICatcher beta 2e: changes

*1 November 2026. Edited from beta 2d by hand. 2,131 lines. Fixes for what the monkey test found (the book's vetting point 6, "bulletproof under careless and random use").*

## What the monkey test found

`tools/monkey_v1b.py` drives the program in the PC harness the way a careless student might: any key, any tap, menu picks and cancels, odd values typed into the forms (`docs/dev/monkey-fleet-2026-11-01.md`). In the first pass (400 runs) beta 2d gave 288 OK, 111 runs where a list typed into a number field went on into the arithmetic, and 1 division by zero: a typed σ of 1E−300.

1. **A typed list.** The three forms' fields were plain names, which take any type.
2. **A window with no width.** At σ = 1E−300 (or μ = ±1E300, or μ = 1E40 with σ = 1) the window μ ± 6.5 σ/√n has zero width in 12 digits, and `cqWindow` (988) divided by it ("Error: X/0" on the calculator). Under `monkey_v1b.py`, which teaches the harness that `STRING(x, 2, d)` refuses 13 or more decimals on the Prime, σ = 1E−300 also stops there: "Invalid input" for 301 decimals.
3. **Axis labels over each other.** At a large μ the labels are long (1000000040 beside 1000000060) and ran into each other.

## What changed (line numbers are beta 2d's)

1. **Every form field takes a real number only**: the setup form (both layouts) and the n form, 8 fields, are `{name,[0]}` (1632, 1694, 1696). On the Virtual Calculator such a field refuses `{1,2}` with "Invalid input" and keeps its value (TTestLab, 1 Nov 2026).
2. **Numbers the window cannot hold are refused with a sentence** (new `cqBadMsg`, after `cqNice`), the line Norm3 v2.4c, NormExplorer beta 42d and SampDist v2.3e draw:
   - a μ or σ of 50 digits or more: "A number you typed has more than 50 digits: too large to work with.";
   - σ/√n below 0.000000001 or below |μ|/100,000,000: "σ/√n is too small next to μ for the calculator's 12 digits. Use a larger σ, a smaller n or a μ nearer 0." Above that line the window still holds about 1,300 distinct 12-digit numbers.
   - The setup form (`cqSetup`) shows the sentence and comes back with the values typed; the n form (`cqAskN`) adds "n did not change." and keeps the old n.
3. **An axis label that would touch the one before it is left out** (`cqDrawAxis`, 1229–1230); its tick stays.
4. Header: the beta 2e block.

Nothing else changed.

## Verification

`verify_CICatcher_beta2e.py`, output `verify_CICatcher_beta2e_output.txt`: **18 PASS, 0 FAIL**, run from a repository layout, with beta 2d read from git history (rule 18). Every run has `prime_facts_v1.py`'s device facts.

- **R** 8 sessions over all five interval types (+10, +1, +50, the level, a line picked, the n form, Help, Reset): 312 screens, every text and the summary identical to beta 2d's.
- **M** one check per finding, each also run on beta 2d, where it fails: the typed fields; six crash inputs refused with the form back, and a good σ typed after the box going on; the lines (σ/√n of 1E−9 accepted, 9.9E−10 refused; at μ = ±10⁹, 10 accepted and 9.99 refused; 9.99E49 accepted, 1E50 refused); the n form at μ = 10⁹, σ = 50 (n = 100 refused, n = 4 taken); the largest and smallest numbers accepted run with no error and no box; every new box within 4 lines of 32 characters.
- **G** only `cqAskN`, `cqSetup`, `cqDrawAxis` and the new `cqBadMsg` differ; every routine tagged `cq`; no `!=`; the code ASCII, as before.
- **D** text_overlap_v1 over every screen drawn: no firm overlap, straddle or overrun (beta 2d on the same runs: 6, the long labels at μ = 10⁹).

**The monkey test again** (1,000 runs, 150 events each): beta 2e **1,000 OK**.

## Gate

`ppl_gate_v1d.py CICatcher_beta2e.txt CICatcher_beta2d.txt`: **RESULT: PASS**.

## The Virtual Calculator

On the Virtual Calculator (2.4.2, build 2026-09-09, Rogers-HP; Claude through computer use, 1 Nov 2026, night). Check: "No errors in the program"; the file the calculator wrote back after that Check alone (177,484 bytes, 14,160 more than the kit's) holds the exact source and is the starter pack's.

- μ = 100, **σ = 1E−300**, n = 10: the box "σ/√n is too small next to μ for the calculator's 12 digits. Use a larger σ, a smaller n or a μ nearer 0.", and the form back (beta 2d divided by zero here).
- **μ = 1,000,000,000, σ = 32, n = 10** (σ/√n = 10.1, just inside the line): the window drew at once, its labels thinned (999999940, 999999980, 1000000020, 1000000060), and +50 drew fifty intervals, 47 of them catching μ.
- From Home the program runs as `CICatcher`; `CICatcher()` is "Syntax Error" there (a program with no arguments takes no brackets in Home).
