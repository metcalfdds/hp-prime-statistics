# Round 19: the two faults round 18's monkey left open, and PowerViz's h under an app's own angle setting (23 November 2026)

StatDist v2.7p, EpiStats v1.7o and PowerViz v2.5v. Roger, 23 Nov 2026, 06:37, on round 18's two open findings: "1) StatDist--fix as you suggest 2) EpiStats--change the smallest number it asccepts". PowerViz joined the round at 12:45, when the book's new example of the *Solve* app showed its fault on the Virtual Calculator; Roger's standing rule: "when you find a problem like that that needs to be fixed—FIX IT".

## StatDist v2.7p: the Formula page asks the CAS only where the calculator answers quickly

**What round 18 found.** The monkey chose Student's t with df = 206.3 and the Formula page (CAS), and the harness stopped the CAS call for E[X²] at its limit of 60 s. Giac 1.9.0 on the PC had not finished the same integral after ten minutes at df = 17.83; whole and half df took under a second (`../round18/probes/`). It had not been tried on a calculator.

**What round 19 found.**

- `probe_fm_families.py` asked Giac on the PC every continuous family's questions, E[X] and E[X²], with parameters typed to two decimals (its output is beside it). Three families waited: Student's t at df 17.83, Fisher F at df1 7.37 and df2 17.83 (31 and 35 s, then the integral back undone), and Burr XII at 2.37, 3.37 and 1.83 (not done in 60 s). The other 19 took under 3 s.
- `probe_fm_params.py` tried whole, half and two-decimal values for those three: t was quick at whole and half df; F was quick at whole dfs, took 7 and 24 s at 7.5 and 17.5, and had not finished at 7 and 17.83; Burr XII was quick with C and K whole or half, and had not finished at C = 2.37.
- **The Virtual Calculator** (`vc_record.txt`, `screens/`) did not follow Giac on the PC. With v2.7o:
  - t at df 17.83 and 206.3 gave "no closed form shown" in 2 and 5 s;
  - F at 7 and 17.83 was still "Asking the CAS" fourteen minutes on, and On did not stop it;
  - with Burr XII at 2.37, 3 and 1 the calculator's screen went black and its program ended about 14 s after the page was asked, twice.

  The first build of v2.7p let Burr XII ask at halves, as Giac on the PC had answered them at once; at 2.5, 3.5 and 1.5 the calculator was still asking after 3 minutes, so the rule became whole numbers.

**What changed** (`make_round19.py`; `../../docs/changes/StatDist_v2.7p_CHANGES.md` has the line numbers). In `st_FmCont`, the CAS is asked for the page's four integrals (E[X], whether E[X] is infinite, E[X²], whether E[X²] is infinite) only for Student's t when 2 df is a whole number, Fisher F when df1 and df2 are whole numbers, and Burr XII when C and K are whole numbers. Otherwise one gray line says so, and the page goes on as it always did when the CAS gave an integral back undone, with "no closed form shown" and the program's own values:

- "The CAS is asked here only when df is a whole number or a half."
- "The CAS is asked here only when df1 and df2 are whole numbers, because other values can keep it working for many minutes."
- "The CAS is asked here only when C and K are whole numbers, because other values can keep it working for minutes, or stop the calculator."

The t line gives no reason, because on the calculator t was quick; it is there because Giac on the PC, which the harness and the monkey use, waits, and a df that is not a whole number or a half got "no closed form shown" on the calculator anyway. Roger asked for the t rule; F and Burr XII are the same fault, found by the probes, with the rules the calculator showed.

## EpiStats v1.7o: the stratified rates grid's smallest person-time

**What round 18 found.** A person-time of 1E−300 in one stratum made `es_MHCalc` divide by zero in the Mantel–Haenszel rate ratio's variance, because the product of its two sums underflowed to 0; 0.001 made the interval's EXP overflow (`../round18/probes/probe_epistats_mh.py`). The grid took any person-time from 0 to 100,000.

**Why 1.** `floor_sweep_r19.py` works the interval for 12,960,000 tables at each floor tried (two strata; cases 0, 1, 2, 5, 100 and 100,000; person-times 0, the floor, 1.5 and 2 times it, 5, 10, 100, 1,000, 10,000 and 100,000). Intervals with an end past the Prime's 1E499: 64,460 at 0.001, 5,730 at 0.1, 2 at 0.5, **none at 1**; past the harness's e^709.8: 20 at 1, none at 2. Its output is beside it.

**What changed** (`../../docs/changes/EpiStats_v1.7o_CHANGES.md`). In both of the grid's forms, the four-value form and the one-cell form, a person-time between 0 and 1 is refused with "A person-time can be 0, or from 1 to 100,000, so give one of less than 1 in smaller units (person-months instead of person-years, say).", and nothing changes. The two forms' help lines give the range ("Person-time exposed, 0 or 1 to 100,000"). Zero stays, because an empty cell is 0.

## PowerViz v2.5v: Cohen's h whatever unit the calculator's trigonometry is in

**What was found.** The book's Draft 74 adds an example of the *Solve* app to Appendix C: the angle of impact of a bloodstain, arcsin(width/length), worked in degrees in the app's own Angle Measure setting (Shift, Symb). On the Virtual Calculator, with *Solve* the current app and set to Degrees, Home Settings read "Angle Measure: See Symbolic Setup" with no choice, `ASIN(1)` in Home gave 90 before and after `HAngle:=0`, and the setting stayed through Calculator > Exit and a new start (`vc_record.txt`; `screens/solve_degrees_home_settings.png`, `solve_degrees_home_asin.png`). PowerViz v2.5u sets `HAngle := 0` when it starts and converted ASIN's answer by HAngle, so its One Proportion test showed "h = 11.54, large" for p₀ 0.5 and p₁ 0.6, where 0.20, small, is right (`screens/pv_h_degrees_v2.5u.png`). The fleet's other programs that use trigonometry measure the unit by `ASIN(1)` or `ATAN(1)` (BiNorm3D, TDist3D, FitCheck, StatDist) and were not affected.

**What changed** (`../../docs/changes/PowerViz_v2.5v_CHANGES.md`). A new routine, `pv_AngU`, returns `1.5707963267949/ASIN(1)`; `pv_AsinR` and `pv_SinR` use it in place of the four `IF HAngle==...` lines. No word on a page changed.

**The harness learned the fact the same day** (`tools/prime_facts_v1.py`, fact 7): `Harness.app_angle`, None for an app at System (the harness as before) or `'rad'`, `'deg'` or `'grad'`, which then decides the unit whatever HAngle says. With it the harness draws v2.5u's "h = 11.54, large" as the calculator did.

**On the Virtual Calculator** v2.5v, Checked and then run with *Solve* still at Degrees, showed "h = 0.20, small" and "at h = 0.20: power = 0.641"; with *Solve* set back to System the same two pages were the same pixel for pixel (`screens/pv_h_degrees_v2.5v.png`, `pv_effsize_degrees_v2.5v.png`, `pv_h_system_v2.5v.png`, `pv_effsize_system_v2.5v.png`).

## What is here

| File | What it is |
| --- | --- |
| `make_round19.py` | The build of the three programs, each from the version before, read from git (`BASE`, main after PR 33), by exact replacements; then round 11's bump (the header, a history note, the version in every quoted string that holds it). |
| `../verify_round19_v1.py` | The verify script, with its saved output beside it (`../verify_round19_v1_output.txt`). It also writes `gates/`. |
| `gates/` | `tools/ppl_gate_v1e.py` on each new version against its old one. |
| `probe_fm_families.py`, `probe_fm_params.py` | What Giac on the PC does with each family's questions, and with whole, half and decimal values of t, F and Burr XII; each with its output for v2.7o beside it. |
| `floor_sweep_r19.py` | The sweep that chose EpiStats' floor, with its output. |
| `monkey_r19.py`, `monkey_r19.txt`, `mk/` | The monkey: 1,000 runs for each of the two programs (base 19, `--lists`; StatDist 240 s a run), every run not OK replayed on the version before. |
| `vc_fm.py`, `vc_back.py`, `vc_fm_t.py` | The scripts that drove the Virtual Calculator for the Formula page, timed (they use `tools/vc_cloud_v1/vcdrive.py`). |
| `vc_record.txt`, `screens/` | What the Virtual Calculator did, and 23 of its screens, each 320 × 240 as it drew them. |

## To run again

From the repository's root, with hp-prime-kit at `$HPKIT` (see `CLAUDE.md`):

```
python3 verify/round19/make_round19.py OUTDIR                                   # the two programs, a second
python3 verify/verify_round19_v1.py                                             # about six minutes
python3 verify/round19/monkey_r19.py                                            # about twenty minutes on two cores, and 30 for PowerViz
python3 verify/round19/floor_sweep_r19.py                                       # about four minutes
python3 verify/round19/probe_fm_families.py programs/StatDist_v2.7p.txt         # up to half an hour (60 s a question)
```

## What the checks found

- **`verify/verify_round19_v1.py`: 62 checks, 0 failed.** The build, T1 and the gate for both. S1 to S3 drive StatDist's Formula page as a student does and time every CAS call: at the guarded values no integral goes to the CAS and the page has the gray line and "no closed form shown"; at the asked values every call ends within 5 s and the page is v2.7o's line for line; Normal, Gamma and Beta with two decimals are v2.7o's line for line; v2.7o at df 17.83 still runs past the harness's 60 s. E1 to E4: EpiStats' two forms refuse 1E−300, 0.5 and 0.999 with the sentence and change nothing, take 0, 1 and 100,000, refuse 100,000.5 as before, change nothing on Cancel; the case-control grid behaves as v1.7n's; the help lines fit; `es_MHCalc` agrees with the formula worked in Python on 3,134 tables at the floor. P1 to P3: PowerViz v2.5v's h and its sine are right to 1E−12 with the app at System, Degrees and Gradians (450 pairs of p₀ and p₁; 25 angles), and the 127 and 126 texts of four pages of One Proportion and Two Proportions are the same under all three; v2.5u at Degrees draws "h = 11.54, large". R: round 18's two stopped runs, replayed with their seeds, end OK. M: the start routines, no warnings. N: the fleet's names and the screen text.
- **The monkey** (`monkey_r19.txt`): 1,000 runs a program. EpiStats and PowerViz 1,000 OK; StatDist 999 OK and one HARNESS (a number past the harness's range) that v2.7o gives with the same seed.
- **The Virtual Calculator 2.4.2, 23 November** (`vc_record.txt`): the Check said "No errors in the program" for both. With v2.7p, F at 7 and 17.83 and Burr XII at 2.5, 3.5 and 1.5 gave the page with its gray line in 3 s or less; t at 2.5 and 17.5, F at 7 and 18, and Burr XII at whole C and K (with S = 1.83 too) asked the CAS and took 3 s at most. EpiStats refused 0.5 as a person-time in both forms, in a box of five lines with nothing cut, and the grid kept its 0.
- **The Virtual Calculator, 12:25 to 12:58**: PowerViz v2.5v's Check said "No errors in the program" at 12:54:52; its two pages under *Solve*'s Degrees, above.
- **Starter pack v25** holds the three newly checked files and v24's other 28, byte for byte (`../../docs/changes/StarterPack_v25_NOTES.md`); the Prime Loader v2o is built from it.

## What was not done

- **No G1 and no G2.** Whether a G1 or a G2 lets an app's own Angle Measure override HAngle in a program, as the Virtual Calculator did, was not tried; PowerViz v2.5v does not depend on it. How long a G1's CAS takes at the guarded values is not known, and neither is whether On stops it there. Each change note has the two-minute check for a real calculator.
- **F at halves on the calculator** was not tried (Giac on the PC took 24 s; the rule keeps F to whole numbers).
- **The rules come from the values tried.** A whole df, or a whole C and K, that the calculator takes long over has not been seen, but not every one was tried.
- **What EpiStats' results page draws for an interval's end near 10^380**, which the floor allows in 20 extreme tables of the sweep (the harness cannot work their EXP, and the Prime can), was not looked at.
- The text-overlap walks were not made again for the whole of either program; the changed screens were seen on the calculator (`screens/`).
