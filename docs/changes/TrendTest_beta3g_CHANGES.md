# TrendTest beta 3g — layout only (28 Oct 2026)

Source: Overlap_Sweep_2026-10-28_v1.md (TrendTest beta3f: 2 overlaps, 1 firm, the odds-ratio plot).
No number, formula, key handling or logic changed.

## Rows moved (trDrawOR, the odds-ratio page)

| Element | old y | new y |
|---|---|---|
| `ref` under the OR = 1 circle of level 1 | circle y + 6 | circle y + 3 |
| x tick labels (the scores) and `score:` | trPB + 5 = 157 | trPB + 6 = 158 |

Why: the OR = 1 line can sit as low as trPB − 10 (the log range always includes 0 with 8 % padding), so `ref` reached y 149 and its ink (to 159) crossed the tick row at 157. Now `ref` ends at 156 at the lowest and the tick row starts at 158; the tick row's ink ends at 168, two px above the readout row at 170, which is untouched (as are 182, 194 and the footer at 206).

## Overlap counts (tools/text_overlap_v1.py, --walk, 80 runs)

| | beta3f | beta3g |
|---|---|---|
| overlaps (firm) | 2 (1) | 1 (0) |
| tight rows | 3 | 3 |
| frame straddles (firm) | 1 (0) | 1 (0) |
| overruns (firm) | 0 (0) | 0 (0) |

The marginal overlap left (`level` beside `score` on the data page header) and the 3 tight rows are unchanged from beta3f.

Verify script (verify_TrendTest_beta3f.py with NEW pointed at beta3g; it checks the numbers only, no screens): failures 0, same as the beta3f run. Gate: ppl_gate_v1c PASS (the full-parse note is pre-existing); case_scan clean.

## Device checklist
1. OR page: `ref` sits just under the hollow circle at OR = 1 and clear of the score labels under the axis, for the snoring example and for a table whose ORs are all above 1 (OR = 1 at the bottom of the axis).
2. The score labels and `score:` line up one px lower than before and do not touch the red readout row.
3. Arrow keys / tap still select a level; the readout row updates.
