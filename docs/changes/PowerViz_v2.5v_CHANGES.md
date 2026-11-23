# PowerViz v2.5v: changes (23 November 2026)

Round 19, the same day as its other two programs. The book's new example of the *Solve* app (Draft 74, Appendix C: the angle of impact of a bloodstain, worked in degrees in the app's own setting) found it. The *Solve* app has an Angle Measure of its own, in its Symbolic Setup, and while that app is the current one and its setting is not System, its setting is the unit of SIN, ASIN and the rest, in Home and in a running program, whatever Home's HAngle says. On the Virtual Calculator 2.4.2, with *Solve* set to Degrees, Home Settings read "Angle Measure: See Symbolic Setup" with no choice, and `ASIN(1)` gave 90 before and after `HAngle:=0` (`verify/round19/vc_record.txt`). PowerViz v2.5u sets `HAngle := 0` when it starts and converted ASIN's answer by HAngle, so it took the 90 for radians: its One Proportion test showed **"h = 11.54, large"** for p₀ 0.5 and p₁ 0.6, where 0.20, small, is right (`verify/round19/screens/pv_h_degrees_v2.5u.png`). The power (0.641) and n₈₀ (153) were right, because they do not go through h. In the harness, with fact 7 below, the "Power vs effect size" page's line read "at h = 11.54" too, and with the app at Gradians h was 12.82.

Roger's rule, 23 Nov 2026: "when you find a problem like that that needs to be fixed—FIX IT". The fleet's other programs that use trigonometry (BiNorm3D, TDist3D, FitCheck, StatDist) already measure the unit by ASIN(1) or ATAN(1) and do not read HAngle, so PowerViz was the only one.

## What changed

1. **The unit is measured, not read from HAngle** (lines 1,232 to 1,259). A new routine, `pv_AngU`, returns `1.5707963267949/ASIN(1)`: 1 when the calculator's trigonometry is in radians, π/180 in degrees and π/200 in grads, as BiNorm3D's and TDist3D's `ASIN(1) / 1.5707963267949` does the other way round. `pv_AsinR(av)` is now `ASIN(av)*pv_AngU()` and `pv_SinR(srad)` is `SIN(srad/pv_AngU())`; v2.5u's four `IF HAngle==...` lines are gone. Nothing else in the program reads HAngle; the line at the head of `POWERVIZ` (line 4,141) that sets the book's four Home settings (round 18) stays.
2. **The header and a history note** (line 4; lines 35 to 40). The version is not on any screen.

No word on a page changed, and no other statement. With the comments, the program is 4,219 lines (v2.5u: 4,204).

## For the book

- The version in the table of "How to use this book" becomes v2.5v, and Appendix F's count of lines becomes 4,219.
- Draft 74's settings item 4 and its *Solve* section tell the reader to set the *Solve* app's Angle Measure back to System when finished; with v2.5v PowerViz is right either way, so the book needs no sentence about PowerViz. Cohen's *h* worked out by hand in Home (Chapter 10) still needs Radians, and the book says so.

## Checks

- `verify/verify_round19_v1.py` (its output is beside it; 62 checks, 0 failed, for the round's three programs). For PowerViz: B, the build (`verify/round19/make_round19.py`) makes the filed program byte for byte; T1, every changed line is the build's; G, the gate against v2.5u (`verify/round19/gates/PowerViz_v2.5v.txt`): PASS. **P**, with `tools/prime_facts_v1.py`'s new fact 7 (`Harness.app_angle`, the current app's own Angle Measure): P1, `pv_EffSz` for tests 3 and 4 on 450 pairs of p₀ and p₁ from 0.01 to 0.99 gives 2 asin √p₁ − 2 asin √p₀ to 1E−12 with the app at System, Degrees and Gradians (v2.5u is off by as much as 154 at Degrees and 172 at Gradians); P2, `pv_SinR` at 25 angles from −3 to 3 radians gives sin x to 1E−12 under all three; P3, every text of four pages (the plot, Power vs effect size, Power vs n curve, the sample-size formula) of One Proportion and of Two Proportions is at Degrees and at Gradians what it is at System (127 and 126 texts), and v2.5u at Degrees draws "h = 11.54, large", as the Virtual Calculator did. M, `POWERVIZ()` with no warnings (v2.5u: none). N, the fleet's names (`pv_AngU` is new) and the screen text.
- The monkey (`verify/round19/monkey_r19.py`, base 19, `--lists`): 1,000 runs, 1,000 OK (`verify/round19/monkey_r19.txt`).
- **The Virtual Calculator 2.4.2** (build 2026-09-09), in the cloud workspace, 23 Nov 2026 (`verify/round19/vc_record.txt`): Program Catalog > Edit > Check at 12:54:52 said "No errors in the program" (`check_PowerViz.png`), and the checked file was copied out before anything ran. Then, with the *Solve* app still the current app and set to Degrees: One Proportion with p₀ 0.5 and p₁ 0.6 showed **"h = 0.20, small"**, power 0.641 (`pv_h_degrees_v2.5v.png`), and Power vs effect size "at h = 0.20: power = 0.641" (`pv_effsize_degrees_v2.5v.png`). With *Solve* set back to System, `ASIN(1)` in Home was 1.57079632679, and the same two pages were the pages at Degrees pixel for pixel.

## On a G1 or a G2

Not yet run on a G1 or a G2. The check, which takes two minutes:

1. Apps, *Solve*; Shift, Symb; Angle Measure: Degrees. Home: `ASIN(1)` gives 90.
2. Shift, Program, PowerViz, Run; 4 One Proportion; OK with p₀ 0.5 and p₁ 0.6. The plot reads "h = 0.20" and "h = 0.20, small" (v2.5u read 11.54, large).
3. Esc out; Apps, *Solve*; Shift, Symb; Angle Measure: System. Home: `ASIN(1)` gives 1.57079632679.

## Unresolved

- Whether a G1 or a G2 lets an app's own Angle Measure override HAngle in a program the same way was not tried; the fix does not depend on it, because it measures the unit whatever decides it.
- The "Power vs effect size" curve for One Proportion at p₀ 0.5 runs flat at 1.0 from about h = 0.4 to its end, with a small step near h = 0.75; it is the same at System and at Degrees, so it is not this round's, and it was not looked into.
