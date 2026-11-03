# EpiStats v1.7g: changes

*2 Nov 2026, night. Made from v1.7f by exact replacements (`make_r6.py`; round 6: sensible ranges for what a student types, and menu items that fit their box). 6,179 lines.*

## Why

- Roger, 2 Nov 2026: "Well for alpha we dont need like 0.00001 or something—use real world values like 0.001, 0.01, 0.05, 0.1, 0.2 and so forth".
- Roger, 2 Nov 2026, after BurrLab's S was capped at 1,000: "cap at 1,000 is just right--what about in our other programs? Maybe we need to check for "reasonable" caps on data a student would enter".

## What changed

1. Alpha now keeps to AnovaLab beta 1b's range, **from 0.001 to 0.2**: outside it, a sentence that begins "α must be from 0.001 to 0.2", and nothing is computed or changed. The four sample-size forms took any alpha between 0 and 1 before. Their help lines read "From 0.001 to 0.2; 0.05 is usual", the sentence "α must be from 0.001 to 0.2 (0.05 is usual)."
2. A count took any size (the caps probe gave a cell 1E100), and a total of 100,000 or more was cut short on the results page's small table. A count is now at most 9,999,999, the most a grid cell shows whole and ChiTable's limit too; above it, a sentence that begins "Values above 9,999,999 do not fit the table". A total too wide for the small table's last column is left out, never cut.
3. Header: the v1.7g block.

## Verification

`verify_EpiStats_v1.7g.py`, output `verify_EpiStats_v1.7g_output.txt`: **14 PASS, 0 FAIL**, run from a repository layout with v1.7f read from `programs/`, an `_superseded_*` folder or git history. G is static, X the program's own checks in the harness (`tools/ppl_run_v3e.py`), R the monkey (`tools/monkey_v1b.py` through `tools/comma_check_v1.py`), 30 seeds on both versions:

- G1 only the four sample-size forms, the four-value form (es_AskAll), the one-cell form (es_Grid), the results page (es_ReadPage) and the menu's title (EpiStats) differ from v1.7f: ['EpiStats', 'es_AskAll', 'es_Grid', 'es_ReadPage', 'es_SS_OneMean', 'es_SS_OneProportion', 'es_SS_TwoMeans', 'es_SS_TwoProportions']
- G2 the header names v1.7g
- G3 no new "!=" and nothing new for the CAS
- X1 the four sample-size forms refuse alpha 0.3 and 0.0005 and take 0.2 and 0.001
- X2 v1.7f took alpha 0.3
- X3 the four-value form refuses 10,000,000 and 1E100 with a sentence and takes 9,999,999
- X4 rows of 110,000: v1.7g cuts nothing and leaves the two totals out of the small table (v1.7f cut ['110,000'])
- X5 the one-cell form refuses above 9,999,999 and says so in its help line
- R0 the runs ran: 24 of 30 new-version runs ended OK or by the clock ({'OK': 24, 'END Unsupported': 6})
- R1 30 seeds ({'OK': 24, 'END Unsupported': 6}): each run takes the old version's path: the same ending, number of screens, boxes and summary once the commas are out (7 accepted as the script says)
- M every number of four or more digits drawn is grouped: 6 different grouped numbers drawn (54,322, 999,999, 3,139, 9,999,999 …); 0 drawn without their commas or with them twice, 0 of them accepted as the script says
- C every text handed to the CAS or EXPR is the old version's, call for call (4 calls on the new version's runs; a run that took another path is R1's)
- Y no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")
- D no new firm overlap, straddle or overrun (old 20, new 8) and no new number cut (old 0, new 0)

Information lines:

- R1: 7 seed(s) take another path; 7 of them because the new version refused a value with this round's sentence ([5000, 5002, 5004, 5009, 5018, 5019, 5026]), 0 because a message is rewritten on purpose ([])
- INFO R2 every screen's texts the old version's once the commas are out, but 0 screen(s): where a number with its commas no longer fit and the program wrote it another way, or where this version changes a text on purpose (its change note says which); the first: []

R1 accepts a seed whose path differs only when the new version showed one of this round's refusal sentences, which the old version did not (a value it took is now refused, and that is the change), or when the only difference is a message this round rewrites on purpose; the script prints which seeds, and why.

## Gate

`tools/ppl_gate_v1d.py EpiStats_v1.7g.txt EpiStats_v1.7f.txt`: **PASS**. hp-prime-kit lint 0 errors; ppl_check_v5 66 E4, 36 E9, as v1.7f, no hard code; lint_ppl 8 problem(s) (v1.7f: 8); the full parse stops where v1.7f's does (a tool limit); fleet names over the 30 programs: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Checked on the Virtual Calculator 2.4.2 (build 2026-09-09), 2 Nov 2026, night: "No errors in the program". The checked file, collected after the Check alone, is 591,006 bytes (the source plus the calculator's compiled block of 27,204 bytes); starter pack v11 and the Prime Loader v1i carry it.

## Device checklist

- A sample-size form: alpha 0.5 (refused), 0.2 (taken). A 2 x 2 table with a cell of 10,000,000: refused; 9,999,999: taken, and the results page shows its numbers whole.
