# AnovaLab beta 1c: changes (4 November 2026)

Round 8: the monkey test's 1,000 runs on the programs that had not had them. Made from beta 1b by `make_round8.py` and `make_round8b.py` (exact replacements; a miss stops the build).

## What changed

1. **Every field of the 5 forms takes a real number only**, `{name,[0]}` (Lessons Learned §4). On the Prime a list typed there is refused by the form ("Invalid input") and the field keeps its value; before, the list went into the arithmetic.
2. A list of D1-D9 holding a number of more than 50 digits is left out, with a sentence (lists of 1E300 overflowed when squared), and every s and sigma0 is from 1E-50 to 1E50 (sigma0 = 1E-300 squared is 0, and the one-sigma test divided by zero).
3. The version on the opening screen now reads "AnovaLab - beta 1c".
4. **"t test" now reads "t-test"** on every screen and in the comments (1 places), as in the book (Roger, 4 Nov 2026). The same number of characters, so no line moves.

## The monkey test

`tools/monkey_v1b.py`, 1,000 runs of random keys, taps, menu picks and typed values (lists and 1E300 among them):

- **beta 1b:** 942 OK, 57 met a typed list or a list of 1E300, and 1 crashed (sigma0 = 1E-300).
- **beta 1c:** 1000 of 1,000 OK.

## Checks

- `verify/verify_round8_v2.py` (output `verify_round8_v2_output.txt`): 63 PASS, 0 FAIL. For AnovaLab: T1 (the forms typed), T2 (beyond the typing, and with every "t test" of the old version read as "t-test", only the routines named in the script differ), T3 (the header).
- `tools/ppl_gate_v1d.py` against beta 1b: pass.

## The Virtual Calculator

Virtual Calculator 2.4.2 (build 2026-09-09), running in the cloud workspace under Wine, 4 Nov 2026 (Lessons Learned §16): the file built from `AnovaLab_beta1c.txt` was copied into the calculator's folder with the calculator closed, opened in the editor and Checked: **"No errors in the program"**. The file the calculator wrote back on Exit reads back as `AnovaLab_beta1c.txt` exactly; it is the one in starter pack v13 and the Prime Loader v1k. Not yet run on a G1 or a G2.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] Type {1,2} into a number field of a form: "Invalid input", and the field keeps its value.
- [ ] Every "t test" on the screen reads "t-test", and no line runs off the screen.
