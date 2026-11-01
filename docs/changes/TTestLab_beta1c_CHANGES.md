# TTestLab beta 1c: changes

*1 November 2026. Edited from beta 1b by hand. 1,420 lines. Fixes for the two faults the first monkey test found (the book's vetting point 6, "bulletproof under careless and random use"), and a third that testing the second on the Virtual Calculator turned up. The general version, TTestLabG beta 1a, is rebuilt from this file by `tools/make_tlg1_v2.py` (rule 23: a fix goes into the advanced version first).*

## What the monkey test found

`tools/monkey_v1a.py` drives a program in the PC harness the way a student who doesn't want to be there might:

- it presses any key, taps anywhere and drags;
- it picks menu items at random or cancels them;
- it types ordinary numbers, edge values (0, negatives, 1E300, 1E−300, a 13-digit number) and sometimes a list into the forms;
- some runs also get random Statistics lists D1 and D2: empty, one value, all equal, ordinary, unequal lengths, pairs, or enormous (±1E300).

Each run gets a verdict: CRASH, GUARD, FREEZE, STALL, STATE (Home's variables changed), HARNESS (something the harness cannot model) or OK. `docs/dev/monkey-fleet-2026-11-01.md` has the first pass over the book's programs.

TTestLabG beta 1, the first program tested (1,000 runs, 150 events each, seed 7), gave **987 OK and 13 HARNESS**. TTestLab beta 1b over the same 1,000 runs gave **988 OK and 12 HARNESS**. Both had the same two causes:

1. **A list typed into a number field went on into the arithmetic.** The "Two independent samples" form took `{1,2}` as Mean 1, and `IP`, `/`, `−` and `<` were then handed a list. On the calculator that ends in an error dialog or nonsense. The fields were plain variable names, which accept any type.
2. **Numbers near 10³⁰⁰ in D1 or D2 overflowed when squared.** On the Prime a square past 1E499 is ∞, with no error (Lessons Learned §3). The SD, SE and t become ∞ or undefined, and the screens fill with them. In the harness's doubles the squaring stops with an error.

## What changed

1. **Every form field takes a real number only** (lines 1170, 1219). The fields are written `{ttM1,[0]}`, …, `{dm,[0]}`, …. This is the User Guide's allowed-types form, "`{var_name, [allowed_types_matrix], [{pos}]}` to create an edit field", where type 0 is a real; 130 programs in the library use it. So the form itself refuses a list, text or a complex number. Both forms changed: "Two independent samples" (6 fields) and "Dependent samples" (3).
2. **A number with more than 50 digits is refused** (`tt_Big`, `tt_BigL`, `tt_BigLMsg`, lines 452–485).
   - **In D1 or D2** (lines 1188 and 1209), before any arithmetic. A box names the list and the value: "Value 2 in D1 has more than 50 digits: too large to work with. Check D1 in the Statistics 1Var app." Nothing changes: the source, the names, the example and the numbers stay as they were, as for beta 1b's other refused reads.
   - **Typed** (`tt_Calc`, lines 504–520). The numbers stay as typed and give no t, and the program says why before the menu: "A number you typed has more than 50 digits: too large to work with. Choose Edit the numbers to change it." Only typed numbers are checked here. Numbers worked out from D1/D2 come from values already checked, and an SD worked out from values below 1E50 can lie a little above it.
   - **Why 1E50:** it is far beyond any data a course meets, and the program's largest power still fits both the Prime's range (1E499) and the harness's doubles (1E308). That power is step 4's (s²/N)² for Welch's df. An infinity is refused too.
3. **A typed N may be at most 1,000,000** (`tt_NMsg`, line 493; `tt_Calc`, lines 513 and 518). "N can be at most 1,000,000: the calculator's t distribution loses accuracy far beyond it (and there t equals z)."
   - Found on the Virtual Calculator while testing item 2. Item 2 had let a typed N up to 1E50 through, and the Prime's `STUDENT_CDF` loses its digits at a huge df.
   - At t = −1.96 it is right to 8 digits at df 10⁶, gives 0.02498 at 10¹⁰ (true value 0.024998) and 0.5 from 10¹⁵ on (Lessons Learned v7zg §3). So a two-tailed p at a df like that would read 1.000.
   - An N of at most 1,000,000 keeps every df below 2×10⁶, where the CDF is right. There, t and z agree to 5 digits anyway.
4. Header: the beta 1c note. The new comment says "The program squares", not "TTestLab squares", so that the general version's copy reads right.

Nothing else changed. beta 1b's arithmetic, screens and messages are untouched, and its 84 checks all pass unchanged.

## Verification

`verify_TTestLab_beta1c.py`, output `verify_TTestLab_beta1c_output.txt`: **97 PASS, 0 FAIL**, run from a copy of the repository laid out as it will be after this commit. That is beta 1b's 84 checks plus a new section M with one check per finding.

Each M check also runs on beta 1b and fails there. The script reads beta 1b from `programs/` or, once it has left that folder, from git history (rule 18). The saved run used git history.

- **M1:** both forms' fields are all `{name,[0]}` (6 and 3); beta 1b's were bare names.
- **M2:** D1 holding 1E300 (independent), −1E300 last in D2 (independent), and −1E300 in D2 (pairs). Each time a box names the list and the value, and the run ends "TTestLab: cancelled". On beta 1b all three stop at the overflow. The box fits in 5 lines.
- **M3:** the line is at 1E50 in size. 1E50 in D2 and −1E50 in D1 are refused; 9.99E49 is accepted, with t equal to SciPy's.
- **M4:** example 1, then a refused D1 read: the example, its names, the typed source and its numbers are kept, and the run ends with example 1's result.
- **M5:**
  - A typed Mean 1 of 1E60 gets the sentence and then the menu, and stays as typed. beta 1b reported "t(73) = 3.23ᴇ60".
  - Every typed field is checked: SD 2 = 1E50, N 1 = 1E50, Mean 2 = −1E55, an infinite SD.
  - Dependent samples with N pairs = 1E50 get the same sentence; beta 1b reported "t(1E50)".
- **M7:**
  - N 1 = 1,000,001 and N 2 = 1E12 are refused, and N 1 = 1,000,000 is accepted with SciPy's t.
  - N pairs = 2,000,000 is refused, and 1,000,000 is accepted.
  - The whole flow with N 2 = 1E12 gives the box and then the menu. beta 1b went on to "t(1.00000000001E12) = 1.58, p = 0.114": right in the harness's SciPy, but on the Prime that p comes from a CDF that has lost its digits.
- **M6:** the largest numbers accepted draw all five steps for pooled, separate, dependent typed and pairs, with t equal to SciPy's. Those are means and SDs of 9.9E49, an SD of 1E−300, and pairs of ±9.9E49.

text_overlap_v1 found no overlap, straddle or overrun over 134 distinct screens.

**The monkey test again** (`monkey_v1a.py`, 1,000 runs, same seed and settings): TTestLab beta 1c **1,000 OK**; TTestLabG beta 1a **1,000 OK**.

## Gate

`ppl_gate_v1d.py TTestLab_beta1c.txt TTestLab_beta1b.txt`: **RESULT: PASS**.

- Kit lint: 0 errors. No hard errors.
- lint_ppl v3 shows only its 4 known-noise lines.
- The parse stops at the first file-level `LOCAL`, the kit tool's limit, as it did for beta 1b.
- `fleet_names_v2.py` over all 30 programs, with TTestLab beta 1c and TTestLabG beta 1a in place of the old versions: 2,259 routine names, 0 collisions, 0 untagged, 0 built-in matches.
- `case_scan_v1.py`: nothing to report.

The typed fields are new to the fleet, so the gate needed three tool changes:

- **`ppl_check_v5.py`:** its E10 ("INPUT target is not a plain variable name") read `{ttM1,[0]}` as the list's end and reported `[0]` as a target. It now reads each field's first item as the name. Over the other 28 programs its output is identical to v4's.
- **`ppl_gate_v1d.py`** runs ppl_check_v5.
- **`lint_ppl.py` version 3** (a fixed-name tool, edited in place; version 2 archived): its INPUT check now reads the call's own arguments. Version 2 compared the first three innermost `{…}` with each other, `{ttM1,[0]}` with `{ttS1,[0]}`, so it would have passed any typed form without looking at the labels. Over the other 28 programs its output is identical to version 2's.

## The run on the Virtual Calculator (1 Nov 2026, 15:54–16:05 CST)

Virtual Calculator 2.4.2 (build 2026-09-09), calculator `Prime`, Rogers-HP, by Claude through computer use. The files were built by hp-prime-kit and copied into its folder with the calculator closed.

1. **Check** (the build before item 3, then the final build): "No errors in the program", for both TTestLab and TTestLabG, each time.
2. **A typed list.** Choose the test → Yes → Yes → OK → type the numbers; `{1,2}` pasted into Mean 1, then Enter. The calculator said "Error: Invalid input", and Mean 1 kept its 0. After OK on the error box the form was still open. (Item 1.)
3. **A typed 1E60.** In the same form, `10^60` showed as "1ᴇ60". OK → two-tailed → α 0.05 → the box "A number you typed has more than 50 digits: too large to work with. Choose Edit the numbers to change it." (4 lines) → the menu. Edit the numbers → type showed Mean 1 = 1ᴇ60, as typed. Mean 1 = 5 → OK → two-tailed → .05 gave step 1 with x̄₁ = 5, and Esc: "TTestLab: t(18) = 11.18, p < 0.001, two-tailed". (Item 2.)
4. **`STUDENT_CDF` at a huge df**, typed in Home:
   - `STUDENT_CDF(2*10^49,-1.96)` = 0.5;
   - `MAKELIST(ROUND(STUDENT_CDF(10^K,-1.96),5),K,6,20,1)` began 0.025, 0.025, 0.025, 0.025, 0.02498, 0.02483;
   - from K = 11 on, rounded to 3 places: 0.025, 0.023, 0.014, 0, then 0.5 six times;
   - `STUDENT_CDF(10^6,-1.96)` = 0.024998033593 and `STUDENT_CDF(10^8,-1.96)` = 2.49978833554ᴇ−2;
   - `−STUDENT_ICDF(10^K,0.025)` for K = 5 to 8: 1.959988, 1.959966, 1.959964, 1.959964.

   So item 3 was added.
5. **The N box** (final build, TTestLabG): Mean 1 = 5, N 2 = `10^7` (shown as "10,000,000") → OK → two-tailed → .05 → "N can be at most 1,000,000: the calculator's t distribution loses accuracy far beyond it (and there t equals z)." (4 lines) → the menu → Quit: "TTestLabG".
6. `1/0` in Home: "Error: X/0" (for the fleet's division-by-zero findings).
7. **Checked files.** After Calculator → Exit, the calculator's folder held both programs larger by their compiled block: TTestLab 125,393 bytes (+10,101) and TTestLabG 123,725 (+9,707). Starter pack v6 carries them, and `make_starter_pack_v4.py --checked` read each source back and found it equal to `programs/`.
   - Both were collected after a Check and nothing else.
   - A TTestLabG file collected after a run of its example 2 was 394 bytes larger: a checked file keeps the file-level values of its last run, which then greet the next student in the forms (Lessons Learned v7zg §3).

## Device checklist (G1 and G2)

`TTestLab_beta1b_CHANGES.md` items 13–26, and:

27. Choose the test → independent → type the numbers → in Mean 1 type `{1,2}` and press Enter. The form refuses it ("Invalid input") and stays open. (Seen on the Virtual Calculator.)
28. The same form with Mean 1 = 1E60 (EEX 60): after tails and α, the box "A number you typed has more than 50 digits …", then the menu.
29. D1 holding a value of 1E60 (typed into the Statistics 1Var app), raw scores: the box "Value … in D1 has more than 50 digits …", and the program ends "TTestLab: cancelled".
30. N 2 = 10000000: the N box, then the menu. In Home, `STUDENT_CDF(10^10,-1.96)` should read about 0.02498, as on the Virtual Calculator: the same firmware, so the same digits are expected.
