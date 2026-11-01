# The monkey test, first pass over the book's programs (1 November 2026)

*Claude, for Roger Metcalf. `tools/monkey_v1a.py` (`monkey_v1.py` for this pass; v1a adds the matrices M0–M9 and `--writes`), 400 runs per program, 150 random events per run, seed 11, random Statistics lists in some runs, 30 seconds per run. The programs are the ones the companion book uses (its Chapter Plan), as they are in `programs/` on 1 November 2026. None of them changed today except TTestLab and TTestLabG, which were done first and now pass (below).*

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

## Next

Each program gets a version with the fixes for its causes. Each finding becomes a check in its verify script that fails on the old version (Lessons Learned §14 rule 25), and the program then runs 1,000 monkey runs with 0 broken. The `{name,[0]}` change is the same edit everywhere and was confirmed on the Virtual Calculator first, on TTestLab.

Reproduce any run with `python3 tools/monkey_v1a.py programs/<file> "<CALL>" --lists --events 150 --seconds 30 --replay SEED`. The summary files (`out/<Name>.txt`, `.json`) are in the author's working folder. Each broken run is kept with its seed and its last 12 dialogs.
