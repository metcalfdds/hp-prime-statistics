# NormExplorer beta 42g: changes

*2 Nov 2026, night. Made from beta 42f by exact replacements (`make_r6.py`; round 6: sensible ranges for what a student types, and menu items that fit their box). 4,212 lines.*

## Why

- Roger, 2 Nov 2026: "Well for alpha we dont need like 0.00001 or something—use real world values like 0.001, 0.01, 0.05, 0.1, 0.2 and so forth".
- Roger, 2 Nov 2026: "Also, some of the menu items run out of the box".

## What changed

1. Alpha now keeps to AnovaLab beta 1b's range, **from 0.001 to 0.2**: outside it, a sentence that begins "α must be from 0.001 to 0.2", and nothing is computed or changed. The three critical-value forms and the power picture took any alpha between 0 and 1 before; their help lines now give the range ("Area in the RIGHT tail: 0.001 to 0.2" and so on), the sentence "α must be from 0.001 to 0.2 (0.05 is usual)." "x at a percentile" keeps any area between 0 and 1: that is not an alpha.
2. The menu box (`CHOOSE`) sizes itself to its longest item up to about 214 px, so an item of more than about 30 characters is cut (Virtual Calculator, 2 Nov 2026: BurrLab's box 214 px with items of 38 characters, 191 px once they were shortened). Items now keep to 30. Two items of 32 and 34 characters now read "My data: D1 (Statistics 1Var)" and "Regression residuals: C1, C2".
3. Header: the beta 42g block.

## Verification

`verify_NormExplorer_beta42g.py`, output `verify_NormExplorer_beta42g_output.txt`: **12 PASS, 0 FAIL**, run from a repository layout with beta 42f read from `programs/`, an `_superseded_*` folder or git history. G is static, X the program's own checks in the harness (`tools/ppl_run_v3e.py`), R the monkey (`tools/monkey_v1b.py` through `tools/comma_check_v1.py`), 30 seeds on both versions:

- G1 only the critical values (ne_InvCalc), the power picture (ne_Compare2) and the data menu (ne_Histo) differ from beta 42f: ['ne_Compare2', 'ne_Histo', 'ne_InvCalc']
- G2 the header names beta 42g
- G3 no new "!=" and nothing new for the CAS
- X1 the critical values and the power picture refuse alpha 0.5 and 0.0005 and take 0.2 and 0.001; a percentile of 0.9 is still taken
- X2 beta 42f took alpha 0.5
- XM every menu item at most 30 characters: 45 items, the longest 30 ("Critical value: right tail (α)")
- R0 the runs ran: 30 of 30 new-version runs ended OK or by the clock ({'OK': 30})
- R1 30 seeds ({'OK': 30}): each run takes the old version's path: the same ending, number of screens, boxes and summary once the commas are out (2 accepted as the script says)
- M every number of four or more digits drawn is grouped: 1 different grouped numbers drawn (847,220 …); 0 drawn without their commas or with them twice, 0 of them accepted as the script says
- C every text handed to the CAS or EXPR is the old version's, call for call (0 calls on the new version's runs; a run that took another path is R1's)
- Y no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")
- D no new firm overlap, straddle or overrun (old 3, new 3) and no new number cut (old 0, new 0)

Information lines:

- R1: 2 seed(s) take another path; 2 of them because the new version refused a value with this round's sentence ([5012, 5019]), 0 because a message is rewritten on purpose ([])
- INFO R2 every screen's texts the old version's once the commas are out, but 0 screen(s): where a number with its commas no longer fit and the program wrote it another way, or where this version changes a text on purpose (its change note says which); the first: []

R1 accepts a seed whose path differs only when the new version showed one of this round's refusal sentences, which the old version did not (a value it took is now refused, and that is the change), or when the only difference is a message this round rewrites on purpose; the script prints which seeds, and why.

## Gate

`tools/ppl_gate_v1d.py NormExplorer_beta42g.txt NormExplorer_beta42f.txt`: **PASS**. hp-prime-kit lint 0 errors; ppl_check_v5 5 E5, 6 W3, as beta 42f, no hard code; lint_ppl 69 problem(s) (beta 42f: 69); the full parse stops at the √ character, as beta 42f's does (a tool limit); fleet names over the 30 programs: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Checked on the Virtual Calculator 2.4.2 (build 2026-09-09), 2 Nov 2026, night: "No errors in the program". The checked file, collected after the Check alone, is 389,075 bytes (the source plus the calculator's compiled block of 19,937 bytes); starter pack v11 and the Prime Loader v1i carry it.

## Device checklist

- A critical-value form: alpha 0.5 (refused), 0.001 (taken). Open the data menu: both items whole.
