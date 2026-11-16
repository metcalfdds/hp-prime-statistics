# CICatcher beta 2l: changes (15 November 2026)

Round 16. Built from beta 2k by exact replacements (`verify/round16/make_cicatcher_2l.py`; a replacement that does not match exactly once stops the build). 2,482 lines (beta 2k: 2,200).

## Why

Roger, 15 November 2026, had a book of tables checked against fresh calculations (Zwillinger & Kokoska, 2000; the report is `docs/dev/crc-table-check-2026-11-15.md`). Its table of tolerance factors (p. 186) has its two headings exchanged against the book's own definitions, and its numbers are an approximation: 171 of the 216 differ from the exact factor, by 3 % at n = 2. The report's fifth suggestion for our programs was "Tolerance intervals with exact factors, in CICatcher", and of the six suggestions Roger said: "Add all please."

CICatcher answers "95 % of what?" for five confidence intervals by drawing many of them and counting those that catch the truth. A tolerance interval gets the same question and the same answer, so it fits the program as a sixth interval: x̄ ± k s is made to hold at least 90 % (or 95 %, or 99 %) of the whole population, and the level is the share of samples whose interval does.

**What was read.** The library in `D:\HP-Prime` was searched on 15 November 2026: no program there computes a tolerance factor. The interval is written from the formulas below (Wald & Wolfowitz, 1946, set the problem up this way; Howe, 1969, gives the starting value).

## What changed

| What | Where (line numbers in `CICatcher_beta2l.txt`) |
| --- | --- |
| **A sixth interval.** "Which interval?" has six items; the sixth is the tolerance interval x̄ ± k s. It asks "Tolerance: hold how much?" (90 %, 95 % or 99 % of the population) and then shows the t run's form (μ, σ, n, level). | `cqSetup` (2018 to 2124) |
| **The page of a tolerance run.** Its samples are a t run's. A line is blue when it holds at least the chosen share of the population and red when it holds less. A light green band, the middle 90 % (95 %, 99 %) of the population, stands where the other runs have the green line of the truth. The header names the run ("tol. 90 %, μ = 100, σ = 15, n = 10"). The panel of a tapped line says how much it holds: "x̄ = 98.7, s = 18.1: 37.4 to 160.1, holds 100.0 %". A red line that holds 89.996 % says so with enough decimals to read below 90. | `cqDrawPanel` (1666 to 1782), `cqDrawAxis` (1540 to 1587), `cqTolBand` (1147 to 1160), `cqTolHold` (1139 to 1142), `cqDesc` (1454 to 1473), `cqWindow` (1293 to 1325) |
| **The factor k, exact.** The confidence of a factor is an integral over where the sample mean fell, done by 12-point Gauss–Legendre; k is the factor whose confidence is the level, found by the secant rule from Howe's approximation. | `cqTolG` (1086 to 1095), `cqTolK` (1103 to 1119), `cqTolRho` (1041 to 1053), `cqTolSet` (1060 to 1081), `cqCrit` (709 to 728) |
| **The slider still moves the tally exactly.** Each sample keeps its catch level, the lowest level at which its interval holds the share: the integral at the sample's own k. Dragging the level recounts from those, as in the other runs. | `cqTolCat` (1128 to 1135), `cqCatch` (1208 to 1251), `cqReset` (1342 to 1366) |
| **Help has seven pages** (six before). Page 5, "Tolerance intervals", is new. Beta 2k's six pages are pages 1 to 4, 6 and 7, word for word (the count in the header aside). | `cqHelp` (2169 to 2298) |
| **The closing line of a tolerance run** says what was counted: "CICatcher: 105 of 111 held at least 95 % of the population (94.6 %) at 95 %, n = 10". The other five runs end as before. | `CICatcher` (2456 to 2482) |
| The new file-level names and their first values. | `cqInit` (2349 to 2391); the declarations from line 399 |

**The factor.** Work in σ from the true mean. A sample whose mean is d σ off needs its interval to reach ρ(d) each way, where Φ(d + ρ) − Φ(d − ρ) = p, and x̄ ± k s reaches that far when s ≥ σ ρ(d)/k. The mean and s are independent, so averaging over the mean's place (d = t/√n, t standard normal) gives the confidence of k:

g(k) = 1 − 2 ∫₀^∞ φ(t) · P( χ²(n − 1) < (n − 1) ρ(t/√n)² / k² ) dt.

Every term is a lower tail times a positive weight, so nothing cancels. The 12 nodes cover t from 0 to 6. Against adaptive quadrature the confidence is right to 10⁻⁶ and k to about 1 part in a million, for n from 2 to 100, p = 0.90, 0.95 and 0.99, and levels from 50 % to 99.9 %.

**Exact against the usual approximation.** At n = 10, for 90 % of the population at 95 % confidence, the exact factor is 2.8563. Howe's approximation, which many tables and guides give, is 2.8382. The help page prints 2.856 and says "printed tables often give an approximation that differs in the third digit."

**The closing line was shortened after it was seen on the Virtual Calculator.** Run from the Program Catalog, the calculator shows what a program returns in a box of five lines of about 26 characters. The first wording ("… tolerance intervals held at least 95 % of the population (96.4 %) at 95 %, tol. 95 %, μ = 100, σ = 15, n = 10; see CQ_COVER") lost its end there. The line as filed leaves out μ and σ, which a tolerance interval's rate does not depend on, and the pointer to `CQ_COVER`, which help page 7 gives. It takes four lines for 111 intervals and five for 1,000 and for 10,000, with the level at 99.9 %.

## Checks

- `verify/verify_CICatcher_beta2l.py`: **37 checks, 0 failed** (output beside it).
  - The build (T1): the script makes the filed file byte for byte.
  - The arithmetic (A0 to A10): the reference integral (400 nodes) equals SciPy's adaptive quadrature to 10⁻¹⁰; `cqTolRho` equals Brent's method to 10⁻¹⁰; `cqTolK` equals the reference at 198 cases with a worst relative error of 1.0 × 10⁻⁶, and `cqTolG` at the reference factor is within 4.4 × 10⁻⁷; a second reference, the definition simulated (400,000 samples at each of four cases), agrees within 4 standard errors; k(10, 0.90, 0.95) = 2.8563 and Howe's 2.8382; each of 600 samples' catch levels is the integral at its own k, and at six levels a sample is counted caught exactly when the interval drawn at that level holds the share; the window, the band and the panel's decimals; an interval of no width is never counted. A3b holds the two routines' comments to counts: Newton's rule for ρ takes 1 to 6 steps (8 at the most) and the secant rule for k takes 3 to 6 (40 at the most), over 2,079 and 990 calls in the PC harness.
  - A long run through the program's own sampler (S1, S2): of 1,000 samples of 10 at 95 %, 962 intervals held at least 90 % of the population (within 4 standard errors of 950); moving the level moves the tally exactly (80 %: 815; 90 %: 915; 99 %: 996; 99.9 %: 1,000; 50 %: 508).
  - The setup, the keys and every way out (V1 to V9, with V7b): Esc at "Which interval?", at "hold how much?" and Cancel on the form; the form's four refusals, each with its sentence; a whole session (+1, +10, +50, Conf and its Esc, Up and Down, the slider, a picked line and its neighbors, n cancelled, refused and changed, Menu and its Esc, Reset, the seven help pages); the closing line, and its fit in the Program Catalog's box as a model of five lines of 26 characters (the first wording took six lines and ended where the calculator cut it; the filed line takes four or five); from a tolerance run, New > t gives a t run again.
  - Against beta 2k (R1): a session of each of the five old intervals shows the same 290 screens, texts and shapes, and returns the same line.
  - The help (H1 to H4): seven pages; beta 2k's six word for word; page 5 as written; every line within 296 px at the measured glyph widths (widest 295), no page over 14 lines.
  - Static and layout (G1 to G4, D1 to D3): no `!=`; code ASCII; LOCAL lines of six names at most; the six nodes and weights written in `cqTolSet` are NumPy's 12-point Gauss–Legendre rule to 12 digits; no overlap, no text off the screen, no number cut short, no menu title over 31 characters.
- Gate (`tools/ppl_gate_v1e.py` against beta 2k; `verify/round16/gates/CICatcher_beta2l.txt`): **PASS**. hp-prime-kit lint 0 errors; `ppl_check_v5` clean; `lint_ppl` 5 reports, as in beta 2k; no name collision in the fleet (31 files, 2,480 routine names).
- Harness smoke test: no error, 0 warnings. `tools/text_overlap_v1.py --walk`: 217 different screens against beta 2k's 136 (the new pages), no collision in either.
- Help layout at the calculator's glyph widths (`verify/round16/helpcheck_r16.json`): 7 screens, no reports.
- Monkey test: **1,000 of 1,000 runs OK** (`verify/round16/mk/CICatcher.jsonl`; base 16, `--lists`). None of its first 300 sessions reached a tolerance run (`mk/reach_r16.txt`), so two **directed** sets were added, each of 200 sessions that begin by choosing the tolerance interval and then take the monkey's random keys, taps and typed values: one accepts the form as it stands (**200 of 200 OK**, a tolerance run on the screen in all 200), the other lets the monkey fill the form (**200 of 200 OK**; the monkey cancelled the form or had a value refused in 132 sessions, and 68 went on to a tolerance run) (`tools/monkey_directed_v1.py`; `mk/directed/CICatcher_tolerance_95.jsonl`, `CICatcher_tolerance_99_form.jsonl`).
- **HP Prime Virtual Calculator 2.4.2 (build 2026-09-09): Check "No errors in the program", and a run** (`verify/round16/vc_checks.txt`, `verify/round16/screens/CICatcher_*.png`). "Which interval?" with its sixth item, "hold how much?", the form; an empty run with its green band; +1, +10 and +50 twice ("caught 47 of 50 (94.0 %), all 111: 94.6 %"); a tapped line's panel; the seven help pages, every line inside its frame; the closing line whole in its box after 111 and after 1,011 intervals.

The monkey tests and the run were made on the file before two comment lines were corrected (the step counts above `cqTolRho` and `cqTolK`). The lines that are not comments are the same (1,522 of them, compared), and the file as filed was Checked again on the Virtual Calculator, "No errors in the program" (23:26).

## On a G1 or a G2 (not yet run)

1. Start CICatcher, a key, "Which interval?" item 6, "90 %", OK on the form. The page should show a light green band from about 75 to 125 and "tol. 90 %, μ = 100, σ = 15, n = 10". Note how long the page takes to come up: the program computes the factor first.
2. +50 four times. "all 200" should settle near 95 %, with a red line here and there.
3. Tap a red line. The panel should read "…, holds nn.n %" with a number below 90.
4. Drag the level to 99 %. Every line should grow, and the tally should change at once.
5. Menu > Help, page 5: every line inside the frame.
6. Menu > Quit. The box should read "CICatcher: n of 200 held at least 90 % of the population (pp.p %) at 99 %, n = 10", whole.

## Unresolved

- Nothing has run on a G1 or a G2. The factor costs 12 chi-square tails for each trial k, and each sample's catch level costs 12 more; how long +50 takes on a G1 is not known.
- The step counts in the two comments are the PC harness's, which counts in 16 digits. The Prime keeps 12, where Newton's rule for ρ may not get its step under the 10⁻¹¹ it asks for and then runs its 8 steps; the value is the same to more digits than the page shows. This was reasoned, not run.
- The header line says "caught n of 50" for a tolerance run too. There "caught" means "held at least the share"; help page 5 explains the colors, and the word in the header was left as the other five runs have it.
- On the Virtual Calculator some key presses did nothing on pages that wait in the fleet's `GETKEY` and `MOUSE` loop (`verify/round16/keyprobe_r16.txt`). Whether a calculator loses presses is not known; nothing was changed for it in this round.
