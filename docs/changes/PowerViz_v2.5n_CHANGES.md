# PowerViz v2.5n: changes

*2 Nov 2026, night. Made from v2.5m by exact replacements (`make_r6.py`; round 6: sensible ranges for what a student types, and menu items that fit their box). 4,146 lines.*

## Why

- Roger, 2 Nov 2026: "Well for alpha we dont need like 0.00001 or something—use real world values like 0.001, 0.01, 0.05, 0.1, 0.2 and so forth".

## What changed

1. Alpha now keeps to AnovaLab beta 1b's range, **from 0.001 to 0.2** (the edit forms took any alpha between 0 and 1). An alpha outside it is reset to 0.05 with the sentence "α must be from 0.001 to 0.2 (you entered ...): reset to 0.05", as an alpha outside 0 to 1 was. The help lines read "From 0.001 to 0.2; 0.05 is usual". 0.001 and 0.2 are the ends of the alpha ladder (ALAD) the arrows step through.
2. Header: the v2.5n block.

## Verification

`verify_PowerViz_v2.5n.py`, output `verify_PowerViz_v2.5n_output.txt`: **11 PASS, 0 FAIL**, run from a repository layout with v2.5m read from `programs/`, an `_superseded_*` folder or git history. G is static, X the program's own checks in the harness (`tools/ppl_run_v3e.py`), R the monkey (`tools/monkey_v1b.py` through `tools/comma_check_v1.py`), 30 seeds on both versions:

- G1 only the edit form (pv_EditForm) differ from v2.5m: ['pv_EditForm']
- G2 the header names v2.5n
- G3 no new "!=" and nothing new for the CAS
- X1 the five edit forms: alpha 0.3 and 0.0005 reset to 0.05 with a sentence, 0.2 and 0.001 kept
- X2 v2.5m kept 0.3
- R0 the runs ran: 30 of 30 new-version runs ended OK or by the clock ({'OK': 30})
- R1 30 seeds ({'OK': 30}): each run takes the old version's path: the same ending, number of screens, boxes and summary once the commas are out (8 accepted as the script says)
- M every number of four or more digits drawn is grouped: 40 different grouped numbers drawn (1,000, 2,000, 2,500, 3,000 …); 0 drawn without their commas or with them twice, 0 of them accepted as the script says
- C every text handed to the CAS or EXPR is the old version's, call for call (20 calls on the new version's runs; a run that took another path is R1's)
- Y no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")
- D no new firm overlap, straddle or overrun (old 0, new 0) and no new number cut (old 0, new 0)

Information lines:

- R1: 8 seed(s) take another path; 8 of them because the new version refused a value with this round's sentence ([5003, 5009, 5010, 5012, 5014, 5015, 5019, 5025]), 0 because a message is rewritten on purpose ([])
- INFO R2 every screen's texts the old version's once the commas are out, but 0 screen(s): where a number with its commas no longer fit and the program wrote it another way, or where this version changes a text on purpose (its change note says which); the first: []

R1 accepts a seed whose path differs only when the new version showed one of this round's refusal sentences, which the old version did not (a value it took is now refused, and that is the change), or when the only difference is a message this round rewrites on purpose; the script prints which seeds, and why.

## Gate

`tools/ppl_gate_v1d.py PowerViz_v2.5n.txt PowerViz_v2.5m.txt`: **PASS**. hp-prime-kit lint 0 errors; ppl_check_v5 19 E1, 341 E7, 32 E9, as v2.5m, no hard code; lint_ppl 12 problem(s) (v2.5m: 12); the full parse stops where v2.5m's does (a tool limit); fleet names over the 30 programs: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Checked on the Virtual Calculator 2.4.2 (build 2026-09-09), 2 Nov 2026, night: "No errors in the program". The checked file, collected after the Check alone, is 374,199 bytes (the source plus the calculator's compiled block of 18,369 bytes); starter pack v11 and the Prime Loader v1i carry it.

## Device checklist

- Edit alpha to 0.5: the sentence, and alpha 0.05. Edit it to 0.2: taken.
