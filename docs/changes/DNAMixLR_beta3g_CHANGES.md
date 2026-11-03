# DNAMixLR beta 3g: changes

*2 Nov 2026, night. Made from beta 3f by exact replacements (`make_r6.py`; round 6: sensible ranges for what a student types, and menu items that fit their box). 3,459 lines.*

## Why

- Roger, 2 Nov 2026, after BurrLab's S was capped at 1,000: "cap at 1,000 is just right--what about in our other programs? Maybe we need to check for "reasonable" caps on data a student would enter".
- Roger, 2 Nov 2026: "Also, some of the menu items run out of the box".

## What changed

1. A yes/no answer ("1 = yes, 0 = no") other than 1 or 0 was read as "no" without a word (a typed 2, or the caps probe's 1,000,000), so the person silently left the hypotheses. It is now refused with the sentence "Each answer is 1 (yes) or 0 (no)." and nothing changes, as a bad count of unknowns already was.
2. An allele's name took any number (1,000,000 too). It is now 1 to 99, the repeat numbers of STR alleles, with decimals for microvariants (14.3); outside that, a sentence that begins "An allele's name is its repeat number".
3. The menu box (`CHOOSE`) sizes itself to its longest item up to about 214 px, so an item of more than about 30 characters is cut (Virtual Calculator, 2 Nov 2026: BurrLab's box 214 px with items of 38 characters, 191 px once they were shortened). Items now keep to 30. The hypotheses menu, 36 to 55 characters an item, now reads "V + S vs V + 1 unknown", "S + 1 unknown vs 2 unknowns", "S alone vs 1 unknown", "V+S+1 unknown vs V+2 unknowns" and "Custom: persons and unknowns", under the title "Hp vs Hd: V victim, S suspect".
4. Header: the beta 3g block.

## Verification

`verify_DNAMixLR_beta3g.py`, output `verify_DNAMixLR_beta3g_output.txt`: **13 PASS, 0 FAIL**, run from a repository layout with beta 3f read from `programs/`, an `_superseded_*` folder or git history. G is static, X the program's own checks in the harness (`tools/ppl_run_v3e.py`), R the monkey (`tools/monkey_v1b.py` through `tools/comma_check_v1.py`), 30 seeds on both versions:

- G1 only the hypotheses (dmSetHyp) and a new locus (dmEnterLocus) differ from beta 3f: ['dmEnterLocus', 'dmSetHyp']
- G2 the header names beta 3g
- G3 no new "!=" and nothing new for the CAS
- X1 yes/no answers of 2, 1,000,000, 0.5 (typed persons) and 7 (Hd) are refused, nothing changing
- X2 beta 3f read 2 as "no" without a word
- X3 an allele named 1,000,000 or 0.5 is refused with a sentence; 12, 14.3, 99.9 and 1 are taken
- XM every menu item at most 30 characters: 19 items, the longest 29 ("V+S+1 unknown vs V+2 unknowns")
- R0 the runs ran: 30 of 30 new-version runs ended OK or by the clock ({'OK': 30})
- R1 30 seeds ({'OK': 30}): each run takes the old version's path: the same ending, number of screens, boxes and summary once the commas are out (2 accepted as the script says)
- M every number of four or more digits drawn is grouped: 17 different grouped numbers drawn (1,000, 3,981, 3,982, 100,000 …); 0 drawn without their commas or with them twice, 0 of them accepted as the script says
- C every text handed to the CAS or EXPR is the old version's, call for call (0 calls on the new version's runs; a run that took another path is R1's)
- Y no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it ("x1000")
- D no new firm overlap, straddle or overrun (old 0, new 0) and no new number cut (old 0, new 0)

Information lines:

- R1: 2 seed(s) take another path; 2 of them because the new version refused a value with this round's sentence ([5012, 5028]), 0 because a message is rewritten on purpose ([])
- INFO R2 every screen's texts the old version's once the commas are out, but 0 screen(s): where a number with its commas no longer fit and the program wrote it another way, or where this version changes a text on purpose (its change note says which); the first: []

R1 accepts a seed whose path differs only when the new version showed one of this round's refusal sentences, which the old version did not (a value it took is now refused, and that is the change), or when the only difference is a message this round rewrites on purpose; the script prints which seeds, and why.

## Gate

`tools/ppl_gate_v1d.py DNAMixLR_beta3g.txt DNAMixLR_beta3f.txt`: **PASS**. hp-prime-kit lint 0 errors; ppl_check_v5 clean, as beta 3f, no hard code; lint_ppl 7 problem(s) (beta 3f: 7); the full parse stops where beta 3f's does (a tool limit); fleet names over the 30 programs: 2,326 routine names, 0 collisions.

## The Virtual Calculator

Checked on the Virtual Calculator 2.4.2 (build 2026-09-09), 2 Nov 2026, night: "No errors in the program". The checked file, collected after the Check alone, is 322,934 bytes (the source plus the calculator's compiled block of 15,088 bytes); starter pack v11 and the Prime Loader v1i carry it.

## Device checklist

- Answer a yes/no question with 2: the sentence, and the hypotheses as they were. Type an allele 150: refused; 14.3: taken. Open the hypotheses menu: every item whole.
