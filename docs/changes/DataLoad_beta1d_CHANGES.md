# DataLoad beta 1d: changes (4 November 2026)

Round 8: the monkey test's 1,000 runs on the programs that had not had them. Made from beta 1c by `make_round8.py` and `make_round8b.py` (exact replacements; a miss stops the build).

## What changed

1. **Every field of the 1 form takes a real number only**, `{name,[0]}` (Lessons Learned §4). On the Prime a list typed there is refused by the form ("Invalid input") and the field keeps its value; before, the list went into the arithmetic.
2. The D lists page works the SD in units of the largest deviation, so a list of 1E300 no longer overflows (the same SD otherwise).
3. Its third help page names ExhibitLab, SeizureLab's new name.

## The monkey test

`tools/monkey_v1b.py`, 1,000 runs of random keys, taps, menu picks and typed values (lists and 1E300 among them):

- **beta 1c:** 962 OK, 16 a typed list and 22 a list of 1E300 overflowing on the D lists page.
- **beta 1d:** 1000 of 1,000 OK.

## Checks

- `verify/verify_round8_v2.py` (output `verify_round8_v2_output.txt`): 63 PASS, 0 FAIL. For DataLoad: T1 (the forms typed), T2 (beyond the typing, and with every "t test" of the old version read as "t-test", only the routines named in the script differ), T3 (the header).
- `tools/ppl_gate_v1d.py` against beta 1c: pass.

## The Virtual Calculator

Virtual Calculator 2.4.2 (build 2026-09-09), running in the cloud workspace under Wine, 4 Nov 2026 (Lessons Learned §16): the file built from `DataLoad_beta1d.txt` was copied into the calculator's folder with the calculator closed, opened in the editor and Checked: **"No errors in the program"**. The file the calculator wrote back on Exit reads back as `DataLoad_beta1d.txt` exactly; it is the one in starter pack v13 and the Prime Loader v1k. Not yet run on a G1 or a G2.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] Type {1,2} into a number field of a form: "Invalid input", and the field keeps its value.
