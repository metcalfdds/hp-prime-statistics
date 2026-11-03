# RiskLab beta 1d: changes

*2 Nov 2026, night. Made from beta 1c by exact replacements (`make_r6.py`; round 6: sensible ranges for what a student types, and menu items that fit their box). 3,162 lines.*

## Why

- Roger, 2 Nov 2026: "Also, some of the menu items run out of the box".

## What changed

1. The menu box (`CHOOSE`) sizes itself to its longest item up to about 214 px, so an item of more than about 30 characters is cut (Virtual Calculator, 2 Nov 2026: BurrLab's box 214 px with items of 38 characters, 191 px once they were shortened). Items now keep to 30. Two items of 34 and 35 characters now read "COMPAS, Broward (ProPublica)" and "D1 Y 0/1, D2 score, D3 group".
2. Header: the beta 1d block.

## Verification

`verify_RiskLab_beta1d.py`, output `verify_RiskLab_beta1d_output.txt`: **10 PASS, 0 FAIL**, run from a repository layout with beta 1c read from `programs/`, an `_superseded_*` folder or git history. G is static, X the program's own checks in the harness (`tools/ppl_run_v3e.py`), R the monkey (`tools/monkey_v1b.py` through `tools/comma_check_v1.py`), 30 seeds on both versions:

- G1 only the two menus (rl_PresetMenu, rl_MyData) and the title page (rl_Open) differ from beta 1c: ['rl_MyData', 'rl_Open', 'rl_PresetMenu']
- G2 the header names beta 1d
- G3 no new "!=" and nothing new for the CAS
- XM every menu item at most 30 characters: 19 items, the longest 30 ("D1 = Y 0/1, D2-D5 = predictors")
- R0 the runs ran: 30 of 30 new-version runs ended OK or by the clock ({'OK': 30})
- R1 30 seeds ({'OK': 30}): each run takes the old version's path: the same ending, number of screens, boxes and summary once the commas are out (0 accepted as the script says)
- M every number of four or more digits drawn is grouped: 34 different grouped numbers drawn (2,483, 2,795, 6,553, 7,298 …); 0 drawn without their commas or with them twice, 0 of them accepted as the script says
- C every text handed to the CAS or EXPR is the old version's, call for call (0 calls on the new version's runs; a run that took another path is R1's)
- Y no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")
- D no new firm overlap, straddle or overrun (old 0, new 0) and no new number cut (old 0, new 0)

Information lines:

- R1: 0 seed(s) take another path; 0 of them because the new version refused a value with this round's sentence ([]), 0 because a message is rewritten on purpose ([])
- INFO R2 every screen's texts the old version's once the commas are out, but 30 screen(s): where a number with its commas no longer fit and the program wrote it another way, or where this version changes a text on purpose (its change note says which); the first: [(5000, 0, ['beta 1c, 28 Oct 2026.  Help is in the menu.'], ['beta 1d, 2 Nov 2026.  Help is in the menu.']), (5001, 0, ['beta 1c, 28 Oct 2026.  Help is in the menu.'], ['beta 1d, 2 Nov 2026.  Help is in the menu.']), (5002, 0, ['beta 1c, 28 Oct 2026.  Help is in the menu.'], ['beta 1d, 2 Nov 2026.  Help is in the menu.'])]

R1 accepts a seed whose path differs only when the new version showed one of this round's refusal sentences, which the old version did not (a value it took is now refused, and that is the change), or when the only difference is a message this round rewrites on purpose; the script prints which seeds, and why.

## Gate

`tools/ppl_gate_v1d.py RiskLab_beta1d.txt RiskLab_beta1c.txt`: **PASS**. hp-prime-kit lint 0 errors; ppl_check_v5 clean, as beta 1c, no hard code; lint_ppl 6 problem(s) (beta 1c: 6); the full parse stops where beta 1c's does (a tool limit); fleet names over the 30 programs: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Checked on the Virtual Calculator 2.4.2 (build 2026-09-09), 2 Nov 2026, night: "No errors in the program". The checked file, collected after the Check alone, is 282,976 bytes (the source plus the calculator's compiled block of 25,752 bytes); starter pack v11 and the Prime Loader v1i carry it.

## Device checklist

- Open the data menu: both items whole.
