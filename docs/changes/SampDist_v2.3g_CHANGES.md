# SampDist v2.3g: changes

*2 Nov 2026, night. Made from v2.3f by exact replacements (`make_r6.py`; round 6: sensible ranges for what a student types, and menu items that fit their box). 1,920 lines.*

## Why

- Roger, 2 Nov 2026: "Well for alpha we dont need like 0.00001 or something—use real world values like 0.001, 0.01, 0.05, 0.1, 0.2 and so forth".

## What changed

1. Alpha now keeps to AnovaLab beta 1b's range, **from 0.001 to 0.2**: outside it, a sentence that begins "α must be from 0.001 to 0.2", and nothing is computed or changed. The Critical Values forms took any alpha between 0 and 1 before. Their help lines read "Tail area: from 0.001 to 0.2; 0.05 is usual", the sentence "α must be from 0.001 to 0.2 (0.05 is usual)."
2. Dragging a critical line gave any tail area from 1E-7 to 0.9999999; the line now stops where its tail area reaches 0.001 or 0.2 (`sd_fix`).
3. Header: the v2.3g block.

## Verification

`verify_SampDist_v2.3g.py`, output `verify_SampDist_v2.3g_output.txt`: **12 PASS, 0 FAIL**, run from a repository layout with v2.3f read from `programs/`, an `_superseded_*` folder or git history. G is static, X the program's own checks in the harness (`tools/ppl_run_v3e.py`), R the monkey (`tools/monkey_v1b.py` through `tools/comma_check_v1.py`), 30 seeds on both versions:

- G1 only the Critical Values forms (sd_modeCrit, sd_live) and the drag (sd_fix) differ from v2.3f: ['sd_fix', 'sd_live', 'sd_modeCrit']
- G2 the header names v2.3g
- G3 no new "!=" and nothing new for the CAS
- X1 Critical Values refuses alpha 0.5 and 0.0005 and takes 0.2 and 0.001
- X2 v2.3f took 0.5
- X3 a line dragged past either end: tail area and line agree at 0.2 or 0.001 [(1, 0.0, 0.2, np.float64(0.2)), (1, -5.0, 0.001, np.float64(0.001)), (2, 0.0, 0.2, np.float64(0.2)), (2, 5.0, 0.001, np.float64(0.001)), (3, -0.1, 0.2, np.float64(0.2)), (3, -6.0, 0.001, np.float64(0.001))]
- R0 the runs ran: 30 of 30 new-version runs ended OK or by the clock ({'OK': 30})
- R1 30 seeds ({'OK': 30}): each run takes the old version's path: the same ending, number of screens, boxes and summary once the commas are out (10 accepted as the script says)
- M every number of four or more digits drawn is grouped: 127 different grouped numbers drawn (1,000, 100,000, 999,999, 2,000 …); 0 drawn without their commas or with them twice, 0 of them accepted as the script says
- C every text handed to the CAS or EXPR is the old version's, call for call (0 calls on the new version's runs; a run that took another path is R1's)
- Y no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")
- D no new firm overlap, straddle or overrun (old 2, new 2) and no new number cut (old 0, new 0)

Information lines:

- R1: 10 seed(s) take another path; 10 of them because the new version refused a value with this round's sentence ([5001, 5008, 5009, 5012, 5018, 5019, 5023, 5024, 5025, 5028]), 0 because a message is rewritten on purpose ([])
- INFO R2 every screen's texts the old version's once the commas are out, but 76 screen(s): where a number with its commas no longer fit and the program wrote it another way, or where this version changes a text on purpose (its change note says which); the first: [(5017, 5, ['P(−1.130 < \ue000 < 1.130) = 1.000000', 'z = −6.1898 to 6.1898   = 100.000%'], ['P(−0.601 < \ue000 < 0.601) = 0.999000', 'z = −3.2905 to 3.2905   = 99.900%']), (5017, 6, ['P(−1.150 < \ue000 < 1.150) = 1.000000', 'z = −6.2988 to 6.2988   = 100.000%'], ['P(−0.600 < \ue000 < 0.600) = 0.998985', 'z = −3.2863 to 3.2863   = 99.898%']), (5017, 7, ['P(−1.150 < \ue000 < 1.150) = 1.000000', 'z = −6.2988 to 6.2988   = 100.000%'], ['P(−0.600 < \ue000 < 0.600) = 0.998985', 'z = −3.2863 to 3.2863   = 99.898%'])]

R1 accepts a seed whose path differs only when the new version showed one of this round's refusal sentences, which the old version did not (a value it took is now refused, and that is the change), or when the only difference is a message this round rewrites on purpose; the script prints which seeds, and why.

## Gate

`tools/ppl_gate_v1d.py SampDist_v2.3g.txt SampDist_v2.3f.txt`: **PASS**. hp-prime-kit lint 0 errors; ppl_check_v5 2 E4, 3 E9, as v2.3f, no hard code; lint_ppl 18 problem(s) (v2.3f: 18); the full parse reads all 30 functions, as v2.3f's does; fleet names over the 30 programs: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Checked on the Virtual Calculator 2.4.2 (build 2026-09-09), 2 Nov 2026, night: "No errors in the program". The checked file, collected after the Check alone, is 171,610 bytes (the source plus the calculator's compiled block of 3,328 bytes); starter pack v11 and the Prime Loader v1i carry it.

## Device checklist

- Critical Values: alpha 0.5 (refused), 0.2 (taken). Drag a critical line to either end: it stops there.
