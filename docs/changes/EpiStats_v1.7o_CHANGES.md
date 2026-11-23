# EpiStats v1.7o: changes (23 November 2026)

Round 19. Round 18's monkey typed a person-time of 1E−300 into the stratified rates grid, and `es_MHCalc` divided by zero working the Mantel–Haenszel rate ratio's variance, `mcPR / (mcR * mcSS)`. With two strata of 1 case in 100,000 person-time on one side and 0 cases in 1E−300 on the other, the other way round in the second, mcR and mcSS are each 1E−305 and their product underflows to 0. With 0.001 in place of 1E−300 the variance is 200,000,000 and the interval's EXP overflows (`verify/round18/probes/probe_epistats_mh.py`). The grid took any person-time from 0 to 100,000; the Incidence Rates module's own form already refused one below 0.001. Roger, 23 Nov 2026, 06:37: "EpiStats--change the smallest number it asccepts".

**Why 1.** `verify/round19/floor_sweep_r19.py` works the interval for every pair of strata built from cases 0, 1, 2, 5, 100 and 100,000 and person-times 0, the floor, 1.5 and 2 times the floor, 5, 10, 100, 1,000, 10,000 and 100,000: 12,960,000 tables for each floor tried. The number of intervals with an end past the Prime's range (1E499) was:

| Floor | Ends past 1E499 |
| --- | --- |
| 0.001 | 64,460 |
| 0.1 | 5,730 |
| 0.5 | 2 |
| 1 | 0 |

Its output is beside it. Zero stays, because a cell the student has not typed is 0, and an empty cell is what the grid starts with; a 0 adds nothing to the sums and divides nothing.

## What changed

1. **The four-value form of the stratified rates grid** (`es_AskAll`):
   - line 1,850: the two person-time fields' help lines are "Person-time exposed, 0 or 1 to 100,000" and "Person-time unexposed, 0 or 1 to 100,000" (they were "Person-time exposed" and "Person-time unexposed");
   - lines 1,881 to 1,888: after the check against 100,000, a person-time between 0 and 1 in either field is refused with "A person-time can be 0, or from 1 to 100,000, so give one of less than 1 in smaller units (person-months instead of person-years, say).", and the grid does not change.
2. **The one-cell form of the grid** (`es_Grid`):
   - line 2,071: the help line for a person-time cell is "Exposed+ person-time, 0 or 1 to 100,000" (with its row's name; it said "0 to 100,000");
   - lines 2,082 to 2,087: a person-time between 0 and 1 is refused with the same sentence, and the cell keeps its value.
3. **The header, a history note and the version** (line 3; lines 31 to 36; the main menu's title, line 767, and help page 1, "About EpiStats", line 5,967, which show "EpiStats v1.7o").

Nothing else changed: the other grids (case-control, cohort, the 2 × 2 tables) and their counts, the Incidence Rates module (0.001 to 100,000 as before) and the arithmetic.

## For the book

- The version in the table of "How to use this book" becomes v1.7o, and Appendix F's count of lines becomes 6,313 (it was 6,294).
- The help pages are word for word the same, but for the version on help page 1 ("About EpiStats"), which reads EpiStats v1.7o. A book page that shows the stratified rates grid's forms would now show the range in their help lines.

## Checks

- `verify/verify_round19_v1.py` (its output is beside it): B, the build makes the filed program byte for byte; T1, every changed line is the build's; G, the gate against v1.7n (`verify/round19/gates/EpiStats_v1.7o.txt`); E1, the four-value form: person-times of 1E−300, 0.5 and 0.999 refused with the sentence and the grid unchanged, 0, 1 and 100,000 taken, 100,000.5 refused with the cap's sentence as before, Cancel changes nothing, and the case-control grid takes 0.5 and rounds it as v1.7n does; E2, the one-cell form: 0.5 refused and the cell keeps its value (v1.7n took 0.5), then 1 taken; E3, the help lines give the range and fit (at most 47 characters show; the longest is 40); E4, `es_MHCalc` on 3,134 tables at the floor gives the rate ratio and its interval as worked in Python, to 1E−9; R, round 18's seed 18000612 replayed: OK; M, `EpiStats()` and `EpiStats2x2(10,20,30,40)` with no warnings; N, the fleet's names and the screen text.
- The monkey (`verify/round19/monkey_r19.py`, base 19, `--lists`): 1,000 runs, 1,000 OK (`verify/round19/monkey_r19.txt`).
- The Virtual Calculator 2.4.2, 23 Nov 2026 (`verify/round19/vc_record.txt`, `verify/round19/screens/`): the Check said "No errors in the program". In the stratified rates grid, 0.5 typed as a person-time, in the one-cell form and in the four-value form, brought up the sentence in a box of five lines with nothing cut, and the grid kept its 0; both forms' help lines show the range.

## On a G1 or a G2

Not yet run on a G1 or a G2. The check, which takes two minutes:

1. EpiStats, Stratified Analysis (M-H), Incidence Rates (IRR_MH).
2. Right, Enter: the help line reads "Exposed+ person-time, 0 or 1 to 100,000". Type 0.5, Enter: the box with the sentence. OK: the cell still reads 0.
3. Enter again, type 2.5, Enter: the cell reads 2.5.

## Unresolved

- The harness keeps numbers to about 1.8E308 and the Prime to 1E499. At the floor, 20 of the 12,960,000 tables have an interval's end between e^709.8 and e^877 (10^308 to 10^381): the harness cannot work their EXP, and the Prime can. The monkey would call such a run HARNESS, not CRASH. What the results page draws for an end of 10^380 was not looked at.
- The Incidence Rates module's own form still takes a person-time from 0.001, as before. It works one table and has no Mantel–Haenszel variance, so the product that underflowed is not in it.
