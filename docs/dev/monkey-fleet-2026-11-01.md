# The monkey test, first pass over the book's programs (1 November 2026)

*Claude, for Roger Metcalf. Round 2 added 1 November 2026, evening; round 3, at the end, the same night. `tools/monkey_v1a.py` (`monkey_v1.py` for this pass; v1a adds the matrices M0–M9 and `--writes`), 400 runs per program, 150 random events per run, seed 11, random Statistics lists in some runs, 30 seconds per run. The programs are the ones the companion book uses (its Chapter Plan), as they are in `programs/` on 1 November 2026. None of them changed today except TTestLab and TTestLabG, which were done first and now pass (below).*

## Why

Roger, 1 November 2026: the book's programs "simply must work—they have to be bulletproof so uninterested students can use them easily". The verify scripts drive the paths a careful student takes. The monkey drives the paths a student who doesn't want to be there takes:

- it presses random keys, taps anywhere and drags;
- it picks menu items at random or cancels them;
- it types random values into forms: ordinary numbers, 0, negatives, 1E300, 1E−300, a 13-digit number, and a list where a field takes any type.

Each run gets one verdict:

| Verdict | What it means |
| --- | --- |
| CRASH | a calculator error |
| GUARD | a built-in called where its answer on the calculator has never been seen |
| FREEZE | no end within 30 s |
| STALL | waiting for something Esc does not end |
| STATE | Home's variables changed |
| HARNESS | something the PC harness cannot model; so far nearly always a program fault seen from the outside |
| OK | the run ended normally |

## The results, by program

| Program | OK of 400 | What broke (runs) |
| --- | --- | --- |
| Norm3 (three starts) | 400, 400, 400 | nothing |
| TestChooser | 400 | nothing |
| BiNorm3D | 398 | a typed list (2) |
| RankLab | 398 | huge lists, ROUND of a non-number (2) |
| FitCheck | 396 | a typed list (4) |
| DataLoad (v1a) | 382 | huge lists overflow (12); ROUND of a non-number (6) |
| AnovaLab | 382 | a typed list (12); huge lists overflow (5); a typed 1E300 overflows (1) |
| ResampLab | 364 | a typed list (14); `RANDSEED`, which the harness does not model (12); huge lists overflow (10) |
| NormExplorer | 356 | a typed list (29); ROUND of a non-number after huge values (3); **division by zero** at μ = −1E300 (1); **one page ignores taps** (5, `ne_DiagPage`); D2 changed (6: its "z-scores into D2", intended) |
| GaltonBoard | 355 | **no end within 30 s** (22, to check: probably long pours in the harness); a typed list (6); D1/D2 changed (17: "put the bins in D1/D2", intended) |
| BayesTree | 352 | a typed list (47); **division by zero** in `bt_NodeInfo` after a sensitivity of 7 was typed (1) |
| ChiTable | 349 | a typed list (29); ROUND of a non-number (22, 12 of them after a typed 1E300 or huge lists; the other 10 to look at) |
| StatDist | 343 | a typed list (45); 1E300 overflows (8); **no end within 30 s at a Poisson λ of 1E300** (1); **`BINOMIAL_CDF` with n = 1E300** (1) |
| ScatterLab | 324 | a typed list (8); overflows (2); C1/C2 changed (66: its "Save to C1, C2", intended) |
| CICatcher | 288 | a typed list (111); **division by zero** at σ = 1E−300 (1) |
| PowerViz | 283 | a typed list (113); a typed 1E300 overflows (4) |
| SampDist | 253 | a typed list (123); **division by zero** in the plot window at μ = 1E300 or σ = 1E−300 (20); a typed 1E300 overflows (4) |

CentralLimit is an app and not yet harness-testable this way. The two TTestLabs were run first:

| Program | Before | After the fix |
| --- | --- | --- |
| TTestLabG | beta 1: 987 of 1,000 | beta 1a: 1,000 of 1,000 |
| TTestLab | beta 1b: 988 of 1,000 | beta 1c: 1,000 of 1,000 |

## The causes

1. **A list typed into a number field** (13 of 17 programs; the most runs by far). INPUT's plain-name fields accept any type, so `{1,2}` typed as a mean reaches the arithmetic. On the calculator that is an error dialog or nonsense on screen. **The fix:** write each number field as `{name,[0]}`, which takes real numbers only. On the Virtual Calculator such a field refused `{1,2}` with "Error: Invalid input" and kept its value (TTestLab beta 1c, Lessons Learned v7zg §4).
2. **1E300 and its square** (10 programs). On the Prime a square past 1E499 is ∞ with no error, and ∞ then fills the screen or a later `ROUND` fails. **The fix:** refuse numbers too large to square, with a sentence, as TTestLab beta 1c does (more than 50 digits), or scale before squaring (§11).
3. **Division by zero** (SampDist 20, BayesTree, CICatcher and NormExplorer 1 each). `1/0` is "Error: X/0" on the calculator, so these are real crashes.
   - In SampDist, CICatcher and NormExplorer, an extreme μ or σ leaves the plot window with zero width (1E300 + 4σ is 1E300).
   - In BayesTree, a sensitivity of 7 was accepted. That is the realistic one: a student types 7 for 70 %.
   - **The fix:** refuse values outside the range that makes sense (a sensitivity in [0, 1], a σ the window can show), with a sentence.
4. **No end within 30 s.**
   - StatDist's Poisson with λ = 1E300 needs a limit on λ.
   - GaltonBoard's 22 are probably long animations at the harness's speed, not hangs. To check by replay.
5. **A page that ignores taps** (NormExplorer's diagnostics page reads keys only). A student taps and nothing happens. **The fix:** read taps as "any key", as every other page does (point 7: consistent controls).
6. **A built-in called where it has never been tried**: StatDist hands `BINOMIAL_CDF` an n of 1E300. **The fix:** a limit on n.
7. **Not faults:** ScatterLab's C1/C2, NormExplorer's D2 and GaltonBoard's D1/D2 are their own "save to the Statistics app" features, each announced on screen. DataLoad's lists are its purpose. ResampLab's `RANDSEED` is the harness's gap.

## Round 2 (1 November 2026, evening): SampDist and BayesTree

| Program | Before (1,000 runs, seed 11) | After |
| --- | --- | --- |
| SampDist | v2.3d: 648 OK under `monkey_v1a.py`; 628 under `monkey_v1b.py` (33 runs stopped on `STRING`'s 13 decimals or more) | v2.3e: 1,000 OK under both |
| BayesTree | beta 8e: 860 OK under `monkey_v1b.py` (139 a typed list, 1 the division by zero) | beta 8f: 1,000 OK |

Their change notes (`docs/changes/SampDist_v2.3e_CHANGES.md`, `BayesTree_beta8f_CHANGES.md`) have the details. Trying the fixes on the Virtual Calculator found three faults no harness run could show, and two of them reach other programs:

1. **`STRING(x, 2, d)` takes at most 12 decimals**: "Invalid input" from 13 on, whatever x. SampDist v2.3d stopped so at σ = 10¹². `tools/prime_facts_v1.py` now teaches the harness this, and `tools/monkey_v1b.py` applies it, so the next monkey runs of every program will show any decimals worked out from the data that can pass 12. **Rerun the first pass's programs under v1b before their next versions.**
2. **`!=` is a factorial and a test on the Prime**, not "not equal" (`{3!=0, 0!=0}` = `{0, 0}`; `999!=0` "Numerical overflow"). The harness cannot show it, so a static check does. Still in the code: **Norm3 v2.4b** (its display floor, line 255) and **StatDist v2.7f** (its floor, line 547, and `IF TYPE(vv) != 0` at line 575, a type test that is never true as written). Their next versions use `<>`.
3. **A stepped loop can stall in 12 digits** (`x + step` rounding back to x): SampDist v2.3d at μ = 10⁹, σ = 0.001. CICatcher and NormExplorer draw the same kind of window and had the same kind of division by zero; their fixes should keep the step far above the 12th digit, as SampDist v2.3e's limit on σ/√n does.


## Round 3 (1 November 2026, night): CICatcher, Norm3, NormExplorer and StatDist

`tools/monkey_v1b.py` (the device facts applied), seed 1, 150 events per run, 30 seconds per run; `--lists` for NormExplorer and StatDist, and `--writes D` for NormExplorer (its "z-scores into D2" is a feature).

| Program | Before | After (1,000 runs) |
| --- | --- | --- |
| CICatcher | beta 2d, first pass: 288 of 400 (a typed list 111, a division by zero at σ = 1E−300) | beta 2e: 1,000 OK |
| Norm3 | v2.4b, first pass: 400 of 400 at each of three starts | v2.4c: 1,002 OK (334 at each start); v2.4d: 1,002 OK |
| NormExplorer | beta 42c: 353 of 400 (a typed list 30; the Diagnostics page ignores taps 9; `STRING` asked for 13 decimals at σ = 1.23 × 10¹² 5; a division by zero at μ = ±1E300 3) | beta 42d: 1,000 OK; beta 42e: 1,000 OK |
| StatDist | v2.7f: 344 of 400 (a typed list 43; an overflow from 1E300 or 1E−300 10; a Poisson with λ = 1E300 never finished 2; `BINOMIAL_CDF` with n = 1E300 1) | v2.7g: 1,000 OK; v2.7h: 1,000 OK |

Norm3 v2.4c, NormExplorer beta 42d and StatDist v2.7g were replaced the same night by v2.4d, beta 42e and v2.7h, after the Virtual Calculator showed their density labels running over the axis (5 below). Their change notes (`docs/changes/CICatcher_beta2e_CHANGES.md`, and two each for the other three: `Norm3_v2.4c_CHANGES.md`, `Norm3_v2.4d_CHANGES.md`, `NormExplorer_beta42d_CHANGES.md`, `NormExplorer_beta42e_CHANGES.md`, `StatDist_v2.7g_CHANGES.md`, `StatDist_v2.7h_CHANGES.md`) have the details. What this round adds to the method:

1. **One limit, drawn the same everywhere.** Each program refuses, with a sentence and before anything changes, a number of 50 digits or more, a σ above 10¹⁰ (where density labels would need 13 decimals), and a scale below 0.000000001 or below |location|/100,000,000 (where the window's tick step is lost in the 12th digit). SampDist v2.3e drew this line first; CICatcher, Norm3 and NormExplorer use the same sentences.
2. **StatDist: test the window, not each parameter.** The monkey reaches a family only now and then, so every parameter of all 27 families was swept over the decades 1E−300 … 1E300 (`verify/sweep_StatDist_v2.7g.py`). v2.7f broke in 204 of 1,794 sweep runs, in 26 of the 27 families. v2.7g computes the window the plot would fit and refuses one that reaches past 1E50 or is too narrow for 12 digits: one test for every family's scale. Shape parameters whose formulas overflow get a range of their own, and four densities were rewritten so they cannot overflow (the same numbers, checked against SciPy). v2.7g: 0 of 1,794 sweep runs broken (851 refused with a box, 943 drawn); v2.7h, the same sweep: 0 of 1,794 broken, the same tally.
3. **Two numerical faults that random use alone would not have found**, both seen while checking the limits at the large end: NormExplorer took s from Σx² − n x̄², which loses its digits when the mean is large next to s (s = 2.98 for 3.03 at a mean of 10⁸; s = 0.00 for a sample from N(10⁹, 10)). beta 42d takes s from the deviations, and the samples add up z (Lessons Learned v7zi §11).
4. **`!=` is gone from the fleet's PPL**: Norm3 and StatDist were the last two programs with it. (BurrLab's one `!=` is inside its MicroPython block, where it does mean "not equal".)
5. **A label over a line passes the PC overlap check**, which compares text with text. On the Virtual Calculator the density labels left of the axis ran over it: Norm3 at any σ above about 50 ("0.0005" at σ = 1000), NormExplorer above about 2000, and StatDist cut "4000000" to "400000" with `TEXTOUT_P`'s width limit, a wrong number, and printed its x labels over each other at σ = 1E−7. Norm3 v2.4d writes such labels in units of a power of ten (1 2 3 4 5 under ×1ᴇ-4), NormExplorer beta 42e and StatDist v2.7h in the scientific form (6ᴇ-5), as SampDist v2.3e already did; no label is clipped. **The other programs' axes need the same look** (in the first pass's order below), and the overlap check should learn the axis lines.

## Next

Each program gets a version with the fixes for its causes. Each finding becomes a check in its verify script that fails on the old version (Lessons Learned §14 rule 25), and the program then runs 1,000 monkey runs with 0 broken. The `{name,[0]}` change is the same edit everywhere and was confirmed on the Virtual Calculator first, on TTestLab. Then the fixes, and the largest and smallest values the new version accepts, are tried on the Virtual Calculator (rule 25). Next in line: PowerViz, ScatterLab, ChiTable, GaltonBoard (its 22 long runs first, by replay), then the rest by the table above.

Reproduce any run with `python3 tools/monkey_v1b.py programs/<file> "<CALL>" --lists --events 150 --seconds 30 --replay SEED` (v1b's runs are v1a's, with the device facts). The summary files (`out/<Name>.txt`, `.json`) are in the author's working folder. Each broken run is kept with its seed and its last 12 dialogs.
