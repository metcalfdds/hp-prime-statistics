# TTestLab beta 1a: changes

*31 October 2026, evening. Built from beta 1 by `make_ttl1a.py` (6 exact replacements). 1,226 lines. Harness only. Beta 1 was filed the same afternoon and has not been loaded on a calculator; what it is and how it was checked is in `TTestLab_beta1_NOTES.md`, which still holds for 1a.*

## Why

Roger: TTestLab goes into the public repository. The repository's data notes ask that every preset show its source on screen. Example 1 already read "age at arrest (years), JDCC"; examples 2 and 3 named no source, and dependent samples showed no outcome line at all.

## What changed

- **Example 2's outcome:** "assault rate, Census of Jails" (the lecture's Table 11.3).
- **Example 3's outcome:** "amount of drug use experience (SPSS)" (Roger's SPSS output).
- **Dependent samples now show the outcome on step 1:**
  - from pairs: under the table, inside its box. The table shows 7 pairs (8 before), and "... and k more pairs" sits on the 8th row;
  - from typed summary numbers: under the summary box.

Nothing else changed.

## Verification

`verify_TTestLab_beta1a.py`, output `verify_TTestLab_beta1a_output.txt`: **59 PASS, 0 FAIL**. These are beta 1's 57 checks (with the new outcome texts) and two new ones:
- 12 pairs: 7 rows, "... and 5 more pairs", the outcome under them;
- a typed summary: the outcome under the box.

text_overlap_v1 over 71 distinct screens: no overlap, straddle or overrun, firm or marginal.

## Gate

`ppl_gate_v1c.py TTestLab_beta1a.txt TTestLab_beta1.txt`: **RESULT: PASS**. Its tallies are identical to beta 1's.

## Device checklist

`TTestLab_beta1_NOTES.md`, items 1-11, with one addition:

12. **Example: matched jails, step 1:** "Outcome: assault rate, Census of Jails" under the five pairs, inside the box. Then Choose the test → dependent → type the mean and SD of the differences: the outcome line is gone (typed numbers have none).
