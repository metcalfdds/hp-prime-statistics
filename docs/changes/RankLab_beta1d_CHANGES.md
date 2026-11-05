# RankLab beta 1d: changes (4 November 2026)

Round 8: the monkey test's 1,000 runs on the programs that had not had them. Made from beta 1c by `make_round8.py` and `make_round8b.py` (exact replacements; a miss stops the build).

## What changed

1. **Every field of the 1 form takes a real number only**, `{name,[0]}` (Lessons Learned §4). On the Prime a list typed there is refused by the form ("Invalid input") and the field keeps its value; before, the list went into the arithmetic.
2. A list of D1-D9 holding a number of more than 50 digits is left out, with a sentence (lists of 1E300 overflowed).
3. **Two more, from the monkey test's run on this version** (`make_round8d.py`; seed 1000810, 1 run of 1,000, which typed m₀ = −1E300): the one-sample m₀ beyond 1E50 is refused with a sentence, "The m₀ you typed has more than 50 digits: too large to work with.", as a D list is; and `rk_Num` keeps the exponent of a number `STRING` writes in scientific form (1E300 had read "1.0000ᴇ3", 1.5E20 "1.5000ᴇ2"). Checked on the Virtual Calculator: −1E300 refused with that sentence; m₀ = 1.5E20 shown as 1.5ᴇ20 on the results page.
4. The version on the opening screen now reads "RankLab - rank tests, beta 1d".

## The monkey test

`tools/monkey_v1b.py`, 1,000 runs of random keys, taps, menu picks and typed values (lists and 1E300 among them):

- **beta 1c:** 992 OK, 8 met a list of 1E300.
- **beta 1d:** 1000 of 1,000 OK.

## Checks

- `verify/verify_round8_v2.py` (output `verify_round8_v2_output.txt`): 63 PASS, 0 FAIL. For RankLab: T1 (the forms typed), T2 (beyond the typing, and with every "t test" of the old version read as "t-test", only the routines named in the script differ), T3 (the header), X5 (m₀ and the exponent; it fails on beta 1c).
- `tools/ppl_gate_v1d.py` against beta 1c: pass.

## The Virtual Calculator

Virtual Calculator 2.4.2 (build 2026-09-09), running in the cloud workspace under Wine, 4 Nov 2026 (Lessons Learned §16): the file built from `RankLab_beta1d.txt` was copied into the calculator's folder with the calculator closed, opened in the editor and Checked: **"No errors in the program"**. The file the calculator wrote back on Exit reads back as `RankLab_beta1d.txt` exactly; it is the one in starter pack v13 and the Prime Loader v1k. Not yet run on a G1 or a G2.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] Type {1,2} into a number field of a form: "Invalid input", and the field keeps its value.
