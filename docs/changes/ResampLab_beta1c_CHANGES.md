# ResampLab beta 1c -- changes from beta 1b (28 Oct 2026)

**Layout only.** No number, formula, key handling or logic changed; verify_ResampLab_beta1c.py (the beta
1b script with the file name and the header's version string updated) passes 767 checks, 0 failures, the
same numbers as beta 1b.  Gate: PASS (the 10 lint notes are beta 1b's).  Pure ASCII, LF.

## Rows moved (routine: old y -> new y)

| Routine | What | Old | New |
|---|---|---|---|
| rs_Axis | x tick labels (every axis) | a label within 30 px of the last TICK was skipped, so 11-character labels (`-0.0000000002` ... on 1E-10 data, `20000000000` on 1E10 data) 61 px apart overlapped | a label is skipped when it would land within 4 px of the last LABEL drawn, 7 px per character; the last label stops 4 px short of the screen's right edge (was 2) |
| rs_DrawRows | the big A / B letters (font 2) of the lab page | row baseline - 26 (1 px short of the group name row at baseline - 12) | baseline - 27 |
| rs_SampRow | the same letters on the sampling rows | baseline - 26 | baseline - 27 |
| rs_Splash | copyright / version line | beta 1b 26 Oct 2026 | beta 1c 28 Oct 2026 |

## Overlap counts (tools/text_overlap_v1.py on the verify script)

| | Overlaps (firm) | Tight rows | Frame straddles (firm) | Overruns |
|---|---|---|---|---|
| beta 1b | 6 (6) | 2 | 1 (0) | 0 |
| beta 1c | 0 (0) | 0 | 0 (0) | 0 |

Nothing remains (build/ResampLab/overlap_ResampLab_beta1c.txt).  All six overlaps were the stress data's
long tick labels; the shipped data sets never produced one.

## Device checklist
1. Lab page (any preset): the big blue A and magenta B sit clear of the group names under them.
2. Null-distribution plot with Your data of order 1E-10 or 1E10 (the stress case): the x labels no longer run into each other -- some ticks go unlabelled.
3. Compare page (the CI bars): the right-most x label stays inside the screen.
