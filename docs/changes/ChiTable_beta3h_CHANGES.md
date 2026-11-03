# ChiTable beta 3h: changes

*2 Nov 2026, night. Made from beta 3g by exact replacements (`make_r6.py`; round 6: sensible ranges for what a student types, and menu items that fit their box). 3,697 lines.*

## Why

- Roger, 2 Nov 2026: "Well for alpha we dont need like 0.00001 or something—use real world values like 0.001, 0.01, 0.05, 0.1, 0.2 and so forth".

## What changed

1. Alpha now keeps to AnovaLab beta 1b's range, **from 0.001 to 0.2**: outside it, a sentence that begins "α must be from 0.001 to 0.2", and nothing is computed or changed. Set alpha took 0.0001 to just below 1 before. Its help line reads "From 0.001 to 0.2; 0.05 is usual", its sentence "α must be from 0.001 to 0.2 (0.05 is usual, 0.01 is strict). It did not change."
2. The alpha drag on the curve page stops at 0.001 and 0.2 (it went from 0.0001 to 0.5), the line put back at the matching quantile; 0.001 and 0.2 are the ends of the arrows' ladder (0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2).
3. A count above 9,999,999 is still refused, but the sentence no longer suggests entering the data divided by 10: dividing a table by 10 changes its chi-square and p (the program's own N / 10 page shows it). It now reads "Counts above 9,999,999 do not fit the table."
4. Header: the beta 3h block.

## Verification

`verify_ChiTable_beta3h.py`, output `verify_ChiTable_beta3h_output.txt`: **13 PASS, 0 FAIL**, run from a repository layout with beta 3g read from `programs/`, an `_superseded_*` folder or git history. G is static, X the program's own checks in the harness (`tools/ppl_run_v3e.py`), R the monkey (`tools/monkey_v1b.py` through `tools/comma_check_v1.py`), 30 seeds on both versions:

- G1 only Set alpha (csSetAlpha), the curve page's drag (csCurve) and the two count forms' message (csAskAll, csEntry) differ from beta 3g: ['csAskAll', 'csCurve', 'csEntry', 'csSetAlpha']
- G2 the header names beta 3h
- G3 no new "!=" and nothing new for the CAS
- X1 Set alpha refuses 0.0005, 0.25, 0.5 (alpha stays 0.05) and takes 0.001 and 0.2
- X2 beta 3g took 0.5
- X3 the drag keeps alpha to 0.001 ... 0.2, the line put back at the matching quantile
- X4 a count above 9,999,999 no longer suggests dividing the data by 10 (that changes chi-square and p)
- R0 the runs ran: 30 of 30 new-version runs ended OK or by the clock ({'OK': 30})
- R1 30 seeds ({'OK': 30}): each run takes the old version's path: the same ending, number of screens, boxes and summary once the commas are out (8 accepted as the script says)
- M every number of four or more digits drawn is grouped: 22 different grouped numbers drawn (54,322, 999,999, 100,000, 12,345 …); 0 drawn without their commas or with them twice, 0 of them accepted as the script says
- C every text handed to the CAS or EXPR is the old version's, call for call (0 calls on the new version's runs; a run that took another path is R1's)
- Y no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")
- D no new firm overlap, straddle or overrun (old 0, new 0) and no new number cut (old 0, new 0)

Information lines:

- R1: 8 seed(s) take another path; 1 of them because the new version refused a value with this round's sentence ([5028]), 7 because a message is rewritten on purpose ([5002, 5008, 5010, 5014, 5016, 5018, 5029])
- INFO R2 every screen's texts the old version's once the commas are out, but 0 screen(s): where a number with its commas no longer fit and the program wrote it another way, or where this version changes a text on purpose (its change note says which); the first: []

R1 accepts a seed whose path differs only when the new version showed one of this round's refusal sentences, which the old version did not (a value it took is now refused, and that is the change), or when the only difference is a message this round rewrites on purpose; the script prints which seeds, and why.

## Gate

`tools/ppl_gate_v1d.py ChiTable_beta3h.txt ChiTable_beta3g.txt`: **PASS**. hp-prime-kit lint 0 errors; ppl_check_v5 1 W3, as beta 3g, no hard code; lint_ppl 8 problem(s) (beta 3g: 7); the one more is the lint's guess "INPUT return discarded" at Set alpha, whose `IF INPUT(...) == 1` it no longer sees past the new comment line above it: the return is used; the full parse stops where beta 3g's does (a tool limit); fleet names over the 30 programs: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Checked on the Virtual Calculator 2.4.2 (build 2026-09-09), 2 Nov 2026, night: "No errors in the program". The checked file, collected after the Check alone, is 368,856 bytes (the source plus the calculator's compiled block of 20,544 bytes); starter pack v11 and the Prime Loader v1i carry it.

## Device checklist

- Set alpha: type 0.5 (refused, alpha stays), then 0.2 (taken). On the curve page drag the alpha line far right and far left: it stops at 0.2 and 0.001.
