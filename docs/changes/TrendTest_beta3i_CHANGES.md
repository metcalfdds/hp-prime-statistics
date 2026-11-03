# TrendTest beta 3i: changes

*2 Nov 2026, night. Made from beta 3h by exact replacements (`make_r6.py`; round 6: sensible ranges for what a student types, and menu items that fit their box). 2,267 lines.*

## Why

- Roger, 2 Nov 2026, after BurrLab's S was capped at 1,000: "cap at 1,000 is just right--what about in our other programs? Maybe we need to check for "reasonable" caps on data a student would enter".

## What changed

1. The caps probe gave a level a total of 1E12, shown as "1E12", and the results table cut numbers short from about 5,000 people a level: with beta 3h's commas "1,250/5,000" needs 60 px of its column's 52, and "19,999.0" 42 of the fit column's 40.
2. The results table's columns are laid out again: score 48 px (for midranks), cases/n 74, fit 36, then p and the 95% CI further right (the CI ends at about x = 313.5, inside the page's frame at 315). The fit is a whole number from 1,000.
3. A level's total can be at most 99,999; above that, the sentence "A level's total can be at most 99,999: the results table shows its numbers whole up to there." The help line says so. The widest row then fits: "99,999/99,999", midrank "549,996.5".
4. Header: the beta 3i block.

## Verification

`verify_TrendTest_beta3i.py`, output `verify_TrendTest_beta3i_output.txt`: **12 PASS, 0 FAIL**, run from a repository layout with beta 3h read from `programs/`, an `_superseded_*` folder or git history. G is static, X the program's own checks in the harness (`tools/ppl_run_v3e.py`), R the monkey (`tools/monkey_v1b.py` through `tools/comma_check_v1.py`), 30 seeds on both versions:

- G1 only data entry (trEnter) and the results table (trPage1) differ from beta 3h: ['trEnter', 'trPage1']
- G2 the header names beta 3i
- G3 no new "!=" and nothing new for the CAS
- X1 six levels of 5,000, 12,345 and 99,999, as entered and as midranks: nothing in the results table cut or past the screen
- X2 beta 3h cut 5,000's table: ['1,250/5,000', '1,875/5,000']
- X3 a total of 100,000 is refused with a sentence; 99,999 is taken
- R0 the runs ran: 28 of 30 new-version runs ended OK or by the clock ({'OK': 28, 'END Unsupported': 2})
- R1 30 seeds ({'OK': 28, 'END Unsupported': 2}): each run takes the old version's path: the same ending, number of screens, boxes and summary once the commas are out (0 accepted as the script says)
- M every number of four or more digits drawn is grouped: 21 different grouped numbers drawn (1,120, 20,160, 1,360, 1,379 …); 0 drawn without their commas or with them twice, 0 of them accepted as the script says
- C every text handed to the CAS or EXPR is the old version's, call for call (32 calls on the new version's runs; a run that took another path is R1's)
- Y no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")
- D no new firm overlap, straddle or overrun (old 0, new 0) and no new number cut (old 0, new 0)

Information lines:

- R1: 0 seed(s) take another path; 0 of them because the new version refused a value with this round's sentence ([]), 0 because a message is rewritten on purpose ([])
- INFO R2 every screen's texts the old version's once the commas are out, but 0 screen(s): where a number with its commas no longer fit and the program wrote it another way, or where this version changes a text on purpose (its change note says which); the first: []

R1 accepts a seed whose path differs only when the new version showed one of this round's refusal sentences, which the old version did not (a value it took is now refused, and that is the change), or when the only difference is a message this round rewrites on purpose; the script prints which seeds, and why.

## Gate

`tools/ppl_gate_v1d.py TrendTest_beta3i.txt TrendTest_beta3h.txt`: **PASS**. hp-prime-kit lint 0 errors; ppl_check_v5 clean, as beta 3h, no hard code; lint_ppl 14 problem(s) (beta 3h: 14); the full parse stops where beta 3h's does (a tool limit); fleet names over the 30 programs: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Checked on the Virtual Calculator 2.4.2 (build 2026-09-09), 2 Nov 2026, night: "No errors in the program". The checked file, collected after the Check alone, is 219,818 bytes (the source plus the calculator's compiled block of 13,416 bytes); starter pack v11 and the Prime Loader v1i carry it. The snoring example's results page, on the same calculator: every 95% CI, "(0.012−0.026)" to "(0.084−0.164)", ends inside the page's frame. The verify script judges the table's right edge at the measured glyph widths for that reason (its docstring says so); `tools/text_overlap_v1`'s narrower estimate, 5.5 px for every character, put the CI 3.5 px over the frame.

## Device checklist

- Enter data with a level of 100,000 people: refused. A level of 99,999 with 99,999 cases: the results row whole. The snoring example's results page: every CI inside the frame.
