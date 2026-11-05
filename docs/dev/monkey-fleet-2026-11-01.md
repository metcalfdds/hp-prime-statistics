# The monkey test, first pass over the book's programs (1 November 2026)

*Claude, for Roger Metcalf. Round 2 added 1 November 2026, evening; round 3, at the end, the same night; round 4 on 2 November. `tools/monkey_v1a.py` (`monkey_v1.py` for this pass; v1a adds the matrices M0–M9 and `--writes`), 400 runs per program, 150 random events per run, seed 11, random Statistics lists in some runs, 30 seconds per run. The programs are the ones the companion book uses (its Chapter Plan), as they are in `programs/` on 1 November 2026. None of them changed today except TTestLab and TTestLabG, which were done first and now pass (below).*

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

## Round 4 (2 November 2026): PowerViz, ScatterLab, ChiTable and GaltonBoard, and every program's labels

`tools/monkey_v1b.py`, seed 1, 150 events per run, 30 seconds per run (GaltonBoard 120: below), `--lists` for all four; `--writes C` for ScatterLab and `--writes D` for GaltonBoard (their "save to the Statistics app" features). GaltonBoard's runs were taken with `tools/monkey_chunks_v1.py`, which runs the same seeds and writes each run as it ends.

| Program | Before | After (1,000 runs) |
| --- | --- | --- |
| PowerViz | v2.5k: 736 of 1,000 (a typed list 241; a mean or σ of 1E300 20, one of them a division by zero on the "Would Levene notice?" page; σ = 1E−300 3, where `STRING` was asked for 302 decimals) | v2.5l: 1,000 OK. Its first two builds gave 999 each, both at seed 1000164: means 1E−300 apart, closed first at the forms and then at the arrows (2 below) |
| ScatterLab | beta 2d: 978 of 1,000 (a typed list 9; a typed 1E300 13) | beta 2f: 1,000 OK (beta 2e, the same fixes before the side panel's: 1,000 OK) |
| ChiTable | beta 3e: 894 of 1,000 (a typed list 106) | beta 3f: 1,000 OK |
| GaltonBoard | beta 3e: 255 of the first 281 (a typed list 8; no end within 30 seconds 18, every one slow, not stuck: 4 below) | beta 3f: 1,000 OK |

1. **A typed list, again the commonest finding.** Every field of the four programs' 16 forms is now `{name,[0]}` (51 fields: PowerViz 29, ChiTable 18, ScatterLab 2, GaltonBoard 2).
2. **One limit, drawn the same way, on every path that changes the value.**
   - PowerViz refuses means and σ above 1,000,000 ("use bigger units"), a σ below 0.000001 or below a millionth of the larger mean, σ₂ outside 0.01 to 100 times σ₁, and means that differ by less than a billionth of σ (the n for 80% power reached 1E612 at μ₀ = 1E−300, μ₁ = 0, σ = 999,999). The last was refused at the forms, and the 1,000-run retest still broke once: the arrows snap μ₁ to the grid of the effect step, and a step to 0 left the same difference. `pv_Snap0`, called from the arrows and the drag, takes such means as equal.
   - ScatterLab refuses a point, typed or loaded from C1 and C2, of 50 digits or more, or closer to the others than 12 digits can tell apart (`slTiny`: a spread below max(1E−9, |the larger value| × 1E−8)).
   - ChiTable keeps a typed α from 0.0001 to below 1: below about 5E−13, 1 − α is 1 in 12 digits and the critical value is infinite.
   - GaltonBoard's board holds at most 5,000 balls (Roger: "put a reasonable limit on number of balls a student can collect--above the threshold just display the results", then "maybe limit to 5,000 or so?"). Every drop takes at most what is left, a pour stops when the board is full, and a full board shows its results with both overlays on. The MicroPython drop is "Fill to 5,000".
3. **Labels, checked under random use** (`docs/dev/label-check-2026-11-02.md`). The new `tools/label_fit_v1.py` finds a number cut short by `TEXTOUT_P`'s width argument, which `text_overlap_v1` cannot see. ScatterLab beta 2d cut 70 axis labels over its verify runs ("100000" as "10000"); beta 2f labels such an axis in units of a power of ten ("×1ᴇ5") or from its lowest tick ("y = 1000000 + label"), and leaves out the bottom y label where the first x label would run into it. Its side panel had the same fault: on the Virtual Calculator beta 2e printed an SSE of 18,053,333,333 as "SSE = 1805333333", one digit cut off, because `label_fit_v1` then looked only at labels that are a number alone; it now looks at every line, and beta 2f writes such a number in the scientific form ("SSE = 1.8053ᴇ10"). Then `tools/monkey_labels_v1.py` ran every program 100 times with both checks recording: 15 of 30 programs showed firm overlaps or cut numbers at values their verify scripts never tried. ChiTable's χ² label past the right edge, GaltonBoard's bin panel and peg counts, and PowerViz's SE line reaching n₈₀ were fixed in this round's versions; the other eleven are listed there for their own rounds. Run again with `label_fit_v1` reading every line, the same runs found three more cut lines (ChiTable beta 3f's "Row 3" in a narrow mosaic column, a DNAMixLR formula line, an EpiStats odds-ratio line), listed there for the next round.
4. **Slow is not stuck.** GaltonBoard's drops and pours wait at least 25 ms a frame, as on the calculator. Eighteen of beta 3e's first 281 runs had no end within 30 seconds; six of them, run again with 300 seconds, all ended (26.8 to 43.8 s, one at a typed list). Beta 3f's runs got 120 seconds each. A single 1,000-run job of GaltonBoard outlived the two-hour limit for a background task and, `monkey_v1b.py` writing only at the end, left nothing: hence `monkey_chunks_v1.py`.

Change notes: `docs/changes/PowerViz_v2.5l_CHANGES.md`, `ScatterLab_beta2f_CHANGES.md`, `ChiTable_beta3f_CHANGES.md`, `GaltonBoard_beta3f_CHANGES.md`.

## Round 5 (4 November 2026): EpiStats and FDAES

EpiStats v1.7g: 838 of 1,000 OK, 161 HARNESS (a list typed into a number field) and 1 CRASH (δ = 1E−300 in the two-means sample size). v1.7h: 1,000 of 1,000. FDAES v3.9c: 977; v3.9d: 1,000 (FDAES is not in this repository). Notes: `docs/changes/EpiStats_v1.7h_CHANGES.md`; Lessons Learned v7zm.

## Round 6 (4 November 2026, night): the sixteen others

`tools/monkey_v1b.py --lists`, 1,000 runs each (StudRange with `--seconds 240` and ErrorRate with `--seconds 120`, because their pages are slow in the harness). RiskLab beta 1d and TestChooser beta 2d: 1,000 of 1,000, unchanged. The other fourteen:

| Program | Before | After |
| --- | --- | --- |
| AgreeLab | beta 1d: 975 of 1,000 OK, 25 met a list typed into a number field or a list of 1E300 overflowing | beta 1e: 1,000 of 1,000 |
| AnovaLab | beta 1b: 942 OK, 57 met a typed list or a list of 1E300, and 1 crashed (sigma0 = 1E-300) | beta 1c: 1,000 of 1,000 |
| BiNorm3D | beta 1c: 996 OK, 4 met a list typed into a number field | beta 1d: 1,000 of 1,000 |
| BurrLab | beta 1l: 941 OK; 44 met RANDSEED, which the PC harness did not model (it does now), 15 a typed list | beta 1m: 1,000 of 1,000 |
| DNAMixLR | beta 3g: 964 OK, 36 met a list typed into a number field | beta 3h: 1,000 of 1,000 |
| DataLoad | beta 1c: 962 OK, 16 a typed list and 22 a list of 1E300 overflowing on the D lists page | beta 1d: 1,000 of 1,000 |
| ErrorRate | beta 1g: 819 OK, 181 met a list typed into a number field | beta 1h: 1,000 of 1,000 |
| FitCheck | beta 1b: 989 OK, 11 met a typed list or a list of 1E300 | beta 1c: 1,000 of 1,000 |
| RankLab | beta 1c: 992 OK, 8 met a list of 1E300 | beta 1d: 1,000 of 1,000 |
| ResampLab | beta 1d: 934 OK; 24 met RANDSEED (not modelled then), 42 a typed list or a list of 1E300 | beta 1e: 1,000 of 1,000 |
| ExhibitLab (SeizureLab) | beta 1c: 924 OK, 76 met a typed list or weights of 1E300 | beta 1d: 1,000 of 1,000 |
| StudRange | beta 15i: 804 OK, 120 met a list typed into a number field, and 76 had not ended within 20 s (a slow plot in the PC harness: one replayed with 240 s ended normally after 154 s) | beta 15j: 1,000 of 1,000 |
| SurvLab | beta 1c: 978 OK, 22 met a list typed into a number field | beta 1d: 1,000 of 1,000 |
| TrendTest | beta 3i: 880 OK, 120 met a list typed into a number field | beta 3j: 1,000 of 1,000 |

The causes were round 4's: a list typed into a number field (each form now types its fields `{name,[0]}`), and 1E300 in a D list, which overflows when squared (a list holding a number of more than 50 digits is now left out or refused with a sentence). One crash: AnovaLab's one-sigma test at σ₀ = 1E−300. `RANDSEED`, which the harness did not model, stopped 44 of BurrLab's runs and 24 of ResampLab's; `tools/prime_facts_v1.py` fact 3 models it now. StudRange's 76 FREEZE verdicts were plots the harness draws slowly. The same night, PowerViz v2.5o, TTestLab beta 1f, TTestLabG beta 1d and TestChooser beta 2e (and AnovaLab, FitCheck and StudRange in the versions above) write "t-test"; the four new versions passed 1,000 of 1,000 too. SeizureLab was renamed ExhibitLab the same night. RankLab beta 1d's own run found two more faults, a typed m₀ of −1E300 and an exponent cut short on the screen, fixed before it shipped; ErrorRate's and StudRange's slow pages ran with a longer time budget. Checks: `verify/verify_round8_v2.py`; outputs: `verify/monkey_<Name>_<version>_output.txt`, before and after.

With that, every program but CentralLimit, an app, has passed.

## Next

Each program gets a version with the fixes for its causes. Each finding becomes a check in its verify script that fails on the old version (Lessons Learned §14 rule 25), and the program then runs 1,000 monkey runs with 0 broken. The `{name,[0]}` change is the same edit everywhere and was confirmed on the Virtual Calculator first, on TTestLab. Then the fixes, and the largest and smallest values the new version accepts, are tried on the Virtual Calculator (rule 25). Next in line: PowerViz, ScatterLab, ChiTable, GaltonBoard (its 22 long runs first, by replay), then the rest by the table above.

Reproduce any run with `python3 tools/monkey_v1b.py programs/<file> "<CALL>" --lists --events 150 --seconds 30 --replay SEED` (v1b's runs are v1a's, with the device facts). The summary files (`out/<Name>.txt`, `.json`) are in the author's working folder. Each broken run is kept with its seed and its last 12 dialogs.
