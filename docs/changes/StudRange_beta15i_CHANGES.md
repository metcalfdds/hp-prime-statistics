# StudRange beta 15i: changes

*2 Nov 2026, night. Made from beta 15g by exact replacements (`make_r6.py`; round 6: sensible ranges for what a student types, and menu items that fit their box). 2,710 lines.*

## Why

- Roger, 2 Nov 2026: "Well for alpha we dont need like 0.00001 or something—use real world values like 0.001, 0.01, 0.05, 0.1, 0.2 and so forth".
- Roger, 2 Nov 2026, after BurrLab's S was capped at 1,000: "cap at 1,000 is just right--what about in our other programs? Maybe we need to check for "reasonable" caps on data a student would enter".

## What changed

1. Alpha: a typed alpha was clamped without a word to 0.0001 ... 0.5 (Critical value, Tukey HSD; 0.001 ... 0.5 on the plot), so a student who typed 5 for 5 % got alpha = 0.5. Alpha now keeps to AnovaLab beta 1b's range, **from 0.001 to 0.2**: outside it, a sentence that begins "α must be from 0.001 to 0.2", and nothing is computed or changed. The help lines read "From 0.001 to 0.2; 0.05 is usual", the sentence "α must be from 0.001 to 0.2 (0.05 is usual)." The plot's alpha drag stops at 0.2, and its alpha key refuses a value outside the range with the same sentence.
2. k (the number of means): no upper limit in P-value, Critical value and Tukey HSD (the caps probe gave it 1E9), and a fraction was cut to a whole number without a word. It is now a whole number from 2 to 100, the reach of the printed tables ("k must be a whole number from 2 to 100."). The plot's k, clamped to 2 ... 20 without a word, is refused with a sentence outside them, on its form and its k key.
3. df (error degrees of freedom): no cap. On the PPL engine, df 1E12 gave q crit 3.6232 for k = 4, alpha = .05 (the right value, the infinite-df one, is 3.6332), and df 1E300 stopped the program with a division by zero; on the calculator's 12 digits the PPL engine loses digits sooner than in the PC harness. Now df is from 1 to 100,000, or 0 for infinity ("df must be from 1 to 100,000, or 0 for ∞."): the program's own stand-in for infinity is already 100,000 (`SR_DF`), and there q crit is the infinite-df value to four decimals. A negative df, or one between 0 and 1, which became infinity without a word, is refused. The help line reads "df error, 1 to 100,000 (0 = ∞; PPL: 3+)". The plot's df key keeps the same range.
4. Tukey HSD: m (per group) is a whole number from 2 to 1,000 ("m must be a whole number from 2 to 1,000."), so the automatic df, k(m − 1), stays below 100,000; an m below 2 was made 2 without a word. A typed df above 100,000 is refused ("df must be from 1 to 100,000, or 0 for auto: k(m-1).").
5. The plot's H0 simulation: m, clamped to 2 ... 30 without a word, is refused with a sentence outside them.
6. Header: the beta 15i block. Beta 15h, a first build of the same night with the alpha and k caps only, was never shipped: its verify script found the df problem, so the repository goes from beta 15g to beta 15i.

## Verification

`verify_StudRange_beta15i.py`, output `verify_StudRange_beta15i_output.txt`: **15 PASS, 0 FAIL**, run from a repository layout with beta 15g read from `programs/`, an `_superseded_*` folder or git history. G is static, X the program's own checks in the harness (`tools/ppl_run_v3e.py`), R the monkey (`tools/monkey_v1b.py` through `tools/comma_check_v1.py`), 30 seeds on both versions:

- G1 only the four forms that take alpha, k, df or m (sr_PvMode, sr_CritMode, sr_HSDMode, sr_PlotMode) differ from beta 15g: ['sr_CritMode', 'sr_HSDMode', 'sr_PlotMode', 'sr_PvMode']
- G2 the header names beta 15i
- G3 no new "!=" and nothing new for the CAS
- X1 22 typed values out of range are refused with a sentence and nothing is computed
- X2 the edges (alpha 0.001 and 0.2, k 2 and 100, df 1, 100,000 and 0, m 2 and 1,000, the plot's k 20 and df 100,000) are taken
- X3 beta 15g took those values without a word (alpha 5, k 1E9, the plot's k 25, df 1E12, m 1,001)
- X4 the plot: a typed alpha outside 0.001 ... 0.2 is refused, the drag stops at 0.2, a typed k outside 2 ... 20 is refused; the help lines say the ranges
- X5 the plot's df key refuses df outside 1 ... 100,000 (0 = infinity) and its H0 simulation m outside 2 ... 30, with a sentence (both were clamped without a word); every df help line says the range
- X6 q crit (k 4, alpha .05, the PPL engine) at df 100,000 is the infinity value to four decimals (q crit = 3.6332, q crit = 3.6332); beta 15g at df 1E12 gave q crit = 3.6232
- R0 the runs ran: 28 of 30 new-version runs ended OK or by the clock ({'END Unsupported': 2, 'OK': 28})
- R1 30 seeds ({'END Unsupported': 2, 'OK': 28}): each run takes the old version's path: the same ending, number of screens, boxes and summary once the commas are out (14 accepted as the script says)
- M every number of four or more digits drawn is grouped: 0 different grouped numbers drawn; 0 drawn without their commas or with them twice, 0 of them accepted as the script says
- C every text handed to the CAS or EXPR is the old version's, call for call (0 calls on the new version's runs; a run that took another path is R1's)
- Y no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")
- D no new firm overlap, straddle or overrun (old 0, new 0) and no new number cut (old 0, new 0)

Information lines:

- R1: 14 seed(s) take another path; 14 of them because the new version refused a value with this round's sentence ([5000, 5001, 5003, 5006, 5008, 5010, 5012, 5015, 5017, 5018, 5019, 5022, 5023, 5029]), 0 because a message is rewritten on purpose ([])
- R1: seed 5000, after the refusal, reached the harness's edge: < between a list and a number is not covered
- INFO R2 every screen's texts the old version's once the commas are out, but 0 screen(s): where a number with its commas no longer fit and the program wrote it another way, or where this version changes a text on purpose (its change note says which); the first: []

R1 accepts a seed whose path differs only when the new version showed one of this round's refusal sentences, which the old version did not (a value it took is now refused, and that is the change), or when the only difference is a message this round rewrites on purpose; the script prints which seeds, and why.

## Gate

`tools/ppl_gate_v1d.py StudRange_beta15i.txt StudRange_beta15g.txt`: **PASS**. hp-prime-kit lint 0 errors; ppl_check_v5 clean, as beta 15g, no hard code; lint_ppl 18 problem(s) (beta 15g: 18); the full parse stops where beta 15g's does (a tool limit); fleet names over the 30 programs: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Checked on the Virtual Calculator 2.4.2 (build 2026-09-09), 2 Nov 2026, night: "No errors in the program". The checked file, collected after the Check alone, is 253,593 bytes (the source plus the calculator's compiled block of 33,193 bytes); starter pack v11 and the Prime Loader v1i carry it. Then, on the same calculator: Critical value with df typed as 1,000,000 gave the sentence "df must be from 1 to 100,000, or 0 for ∞." and went back to the menu; with df 10,000 (k 3, alpha 0.05) the MicroPython engine gave q crit = 3.3150; the help line "df error, 1 to 100,000 (0 = ∞; PPL: 3+)" fits its line. (Digits typed fast at the PC keyboard were sometimes dropped: 1,000,000 and 10,000 are what the form showed.)

## Device checklist

- Critical value: alpha 5 (refused), k 101 (refused), df 1,000,000 (refused: seen on the Virtual Calculator), df 0 (infinity). Tukey HSD: m 1,001 (refused), m 1,000 (taken). Distribution plot: k 25 (refused), and the df key with 200,000 (refused).
