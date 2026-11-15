# ScatterLab beta 2k: changes (14 November 2026)

Round 14. Built from beta 2j by exact replacements (`verify/round14/make_scatterlab_2k.py`; a replacement that does not match exactly once stops the build).

## Why

The book *Statisticles* teaches the slope's test and interval and the two intervals around the line in Chapter 13, and until now sent the reader to the *Inference* app for all of it; its picture of the two intervals and its Anscombe's quartet were drawn on a computer. Roger, 14 November 2026: "go ahead and do the program work"; "we're featuring the Prime"; and, of Anscombe's quartet, "they need to be in". With beta 2k the calculator draws all three itself.

## What changed

| What | Where (line numbers in `ScatterLab_beta2k.txt`) |
| --- | --- |
| **Menu > Inference for the slope.** A page with the line, H₀: β₁ = 0, s = √(SSE/(n − 2)), SE(b₁) = s/√(Sxx), t = b₁/SE(b₁) on n − 2 df, the two-tailed p, the 95% interval for the slope with its t critical value, and the decision at α = 0.05. Each line shows its own arithmetic. | `slInf` (929), called at the end of every `slFit` (1028); `slInfPage` (2217) with `slIL` (2190), `slIn` (2200), `slPS` (2208) |
| **Menu > Bands: mean and new case.** The 95% band for the mean of y at each x (inner, solid blue) and the wider one for one new case (outer, dotted orange), with a note that says which is which. | `slBandPt` (1321), `slBands` (1328), called from `slDraw` (1375) |
| **Data > Anscombe's quartet, set 1 to set 4.** Anscombe's (1973) four sets of 11 points, all drawn in one window (x 2 to 20, y 2 to 14) so that the four plots can be compared. The values are those of R's `anscombe`. | `slAnsc` (1798); the Data menu in `slData` (1827) |
| **Home.** `SL_SEB` (the slope's standard error), `SL_T` and `SL_P` (its t and two-tailed p), kept up to date like the six older results. | 331, 929 |
| **Help page 7 of 7, "Testing the slope".** The other six pages are beta 2j's, renumbered n/7; page 6 lists the three new Home results. | 2368 |
| **The menu has twelve items** (Quit shows as C), and the Data menu eight. Each is at most 30 characters. | `slMenu` (2413) |

The arithmetic: p is twice the lower tail at −|t| (`2 * STUDENT_CDF(n − 2, −|t|)`, never 1 − CDF); the t critical value is `-STUDENT_ICDF(n − 2, 0.025)`, kept from fit to fit and worked out again only when the df changes, because a drag refits every frame. There is no test when there is no line or when every point is on it (s = 0): the page says so, and nothing divides by zero. A p below 0.001 prints "p < 0.001"; a p that rounds to 0.050 gets its 4 significant digits beside the decision. A number on the page is never cut: it is held to 72 px or written in the scientific form, and each line has a short form to fall back on.

The wording about Anscombe: to three decimals the four r's are 0.816, 0.816, 0.816 and 0.817, so the note says "All four sets: r = 0.82 and the line 3.00 + 0.50 x", and the help says "nearly the same r and line".

## Checks

- `verify/verify_ScatterLab_beta2k.py`: **34 checks, 0 failed** (output beside it). The slope's test equals SciPy's `linregress` and `t.ppf` to 9 digits on the example (t = 4.2584, p = 0.000795), on Anscombe's four sets and on 300 random sets of 3 to 40 points; the edges (every point on the line, two points, every x the same); the page at the calculator's glyph widths with values near 1E8 and 1E−8 (widest line 274 px of 296); the bands inside the plot box, the inner one's half-width at x̄ to the pixel, the outer one outside it; every item of both menus, and Esc at each; a tour with no new feature draws beta 2j's 41 screens text for text; seven help pages; no firm overlap and no cut number on any screen.
- Gate (`tools/ppl_gate_v1e.py` against beta 2j): **PASS**. hp-prime-kit lint 0 errors; `ppl_check_v5` no hard error; `lint_ppl` beta 2j's reports and one of the same kind for the new `EXPORT` line; no name collision in the fleet. The first build's `slIn(inV)` was reported (`inV` is `INV`) and renamed.
- Monkey test: **1,000 of 1,000 runs OK** (`verify/round14/mk/ScatterLab.jsonl`; base 14, `--lists --writes C`).
- **HP Prime Virtual Calculator 2.4.2 (build 2026-09-09): Check "No errors in the program"; then run, and every new screen seen** (`verify/round14/vc_checks.txt`, `verify/round14/screens/`): the inference page for the example and for Anscombe's set 4, the bands alone and with residuals, the four Anscombe plots, help page 7. Every glyph drew (β, ρ, α, √, ±, ×, ≠, the subscripts), and every line was inside its page.

## On a G1 or a G2 (not yet run)

From least to most risky:

1. Data > Poverty vs crime. Menu > Inference for the slope: the page should read t = 4.258, "p < 0.001 (two-tailed, df = 14)", "95% interval for β₁: 0.5061 to 1.533", "reject H₀". Any key returns to the plot.
2. Menu > Bands: a solid blue band close to the line and a dotted orange one farther out, and the two notes under the plot. Can the dotted band be told from the solid one on the G1's screen?
3. With the bands on, drag a point: do the bands follow without a lag you can feel? (Each frame is about 190 pixel columns of arithmetic.)
4. Data > Anscombe's quartet, sets 1 to 4: each plot in the same window, the panel reading r = 0.816 (0.817 for set 4).
5. With no points: Menu > Bands and Menu > Inference each give a red sentence and change nothing.
6. Press and hold Enter on the plot for about half a second. Does the menu open and stay open, or does its first item (the far-out point) run at once? On the Virtual Calculator, driven by a script, the first item ran once after a 0.4-s Enter, and it could not be told whether the held key or lost arrow keys caused it. The menu code is beta 2j's.
7. Help page 7/7: every line inside the frame.

## Unresolved

- Nothing has run on a G1 or a G2.
- Item 6 above.
- The interval and the bands are at 95% only; there is no way to choose another level.
- `docs/scatterlab-guide.md` describes beta 2a; it has a new section for beta 2k's three features and is otherwise as it was.
