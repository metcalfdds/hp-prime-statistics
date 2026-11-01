# TTestLabG beta 1a: changes

*1 November 2026. Built from TTestLab beta 1c by `tools/make_tlg1_v2.py` (exact replacements; rule 23). 1,393 lines. The general version of TTestLab, carrying the advanced version's fixes for the faults the first monkey test found in TTestLabG beta 1.*

## What the monkey test found in beta 1

`tools/monkey_v1a.py`, 1,000 random runs, 150 events each, seed 7, with random D1/D2 lists in some runs: **987 OK, 13 HARNESS**. There were two causes:

- **A list typed into a number field** (10 runs): `{1,2}` as a mean reached `IP`, `/`, `−` and `<`.
- **Numbers near 10³⁰⁰ in D1 or D2** (3 runs) overflowed when squared, which gives ∞ on the Prime, with no error.

Testing the fix on the Virtual Calculator then found a third: the Prime's `STUDENT_CDF` loses its digits at a huge df, so a typed N needs a limit. `TTestLab_beta1c_CHANGES.md` has the details and the calculator run.

## What changed

The build script's v2 reads TTestLab beta 1c and names beta 1a in the header. Every replacement is v1's. The new code in beta 1c needed none: its messages carry no program name, and its routines are renamed `tt_` → `tz_` with the rest. So beta 1a is beta 1 plus:

1. **Every form field takes a real number only** (`{tzM1,[0]}`, …, `{dm,[0]}`, …; lines 1088 and 1137). The form itself refuses a list.
2. **A number with more than 50 digits is refused** (`tz_Big`, `tz_BigL`, `tz_BigLMsg`, lines 394–419):
   - in D1/D2 (lines 1106 and 1127), with a box that names the list and the value; nothing changes;
   - typed (`tz_Calc`, lines 438–454), with a sentence before the menu.
3. **A typed N may be at most 1,000,000** (`tz_NMsg`, line 427; `tz_Calc`), with a sentence before the menu.
4. **Header:**
   - the beta 1a note;
   - that beta 1 ran on the Virtual Calculator on 31 October;
   - that on 1 November its checked file ran there with no Check;
   - the advanced version's count of checks, now 97.

The diff against beta 1 is exactly these lines.

## Verification

`verify_TTestLabG_beta1a.py`, output `verify_TTestLabG_beta1a_output.txt`: **106 PASS, 0 FAIL**. That is beta 1's 93 checks plus section M, taken from `verify_TTestLab_beta1c.py` with the names changed and with age at arrest as example 3. Every M check also runs on beta 1, read from git history in the saved run, and fails there as it should. text_overlap_v1 found no overlap, straddle or overrun on any screen drawn.

**The monkey test again** (`monkey_v1a.py`, 1,000 runs, same seed and settings): **1,000 OK**. beta 1 gave 987. The copy tested differed from this file only in the header's count of checks.

## Gate

`ppl_gate_v1d.py TTestLabG_beta1a.txt TTestLabG_beta1.txt`: **RESULT: PASS**.

- Kit lint: 0 errors. No hard errors.
- lint_ppl v3 shows only its 4 known-noise lines.
- `fleet_names_v2.py` over all 30 programs: 0 collisions.
- `case_scan_v1.py`: nothing to report.

## The run on the Virtual Calculator (1 Nov 2026)

- **Check:** "No errors in the program", for the build before item 3 and for this one.
- **The N box:** Choose the test → Yes → Yes → OK → type the numbers, with Mean 1 = 5 and N 2 = `10^7` (shown as "10,000,000"). Then OK → two-tailed → α .05 → "N can be at most 1,000,000: …" in 4 lines → the menu → Quit: "TTestLabG".
- **The checked file** (123,725 bytes, +9,707) is in starter pack v6.
  - It was collected after a Check and nothing else: the program was copied in, Checked, and the calculator closed.
  - A copy collected after a run of example 2 was 124,119 bytes. A checked file keeps the file-level values of its last run (Lessons Learned §3, v7zg), so an example's numbers would have greeted a student in the forms.

## Device checklist (G1 and G2)

`TTestLabG_beta1_NOTES.md`'s list, and items 27–30 of `TTestLab_beta1c_CHANGES.md` with "TTestLabG" for "TTestLab".
