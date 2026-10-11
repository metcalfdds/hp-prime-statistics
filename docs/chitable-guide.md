# ChiTable — User's Guide

Oct 10, 2026 · Roger Dale Metcalf Sr

*Chi-square for a 2 × 2, 2 × 3 or 3 × 2 table on the HP Prime — expected counts, percentages, the test, residuals, an interpretation in words, and three plots*

*Describes ChiTable beta 1k. Beta 1j was tested on an HP Prime G2 and G1, both running the 2026-09-09 firmware, on 10 Oct 2026 — the entry grid and its soft keys, the Values form, the results pages and all three plots; beta 1k changes only how the program waits for a finger to lift (a one-second limit) and how it quits (the summary is returned to Home rather than printed), and has not been re-run yet. The arithmetic was verified off-device against scipy and statsmodels on 4,900 random tables before the PPL was written.*

## What this is for

A two-way table counts people (or cases, or specimens) by two categorical variables at once: defendant's race against whether a death sentence was handed down, say, or gender against party identification. The chi-square test asks whether the two variables are **independent** — whether the column percentages are the same in every row — or **associated**. ChiTable does that for the three shapes a first statistics course meets, and shows the working: the expected counts, the row and column percentages, each cell's contribution to χ², the adjusted residuals that say *which* cells drive the result, and a plain-English interpretation with an APA-style line. For a 2 × 2 table it adds the classical extras — Yates, Fisher's exact test, the two-proportion z, risk difference, relative risk and odds ratio.

Pure PPL, no MicroPython: the arithmetic is light, and the live touch grid belongs in PPL.

### Installing it

The program ships as a plain text file. Open the HP Prime Connectivity Kit, create a new program in the Program Catalog, and paste the whole file in. Run `ChiTable()` from the Program Catalog.

## The menu

| Item | What it does |
|---|---|
| New table 2 × 2 / 2 × 3 / 3 × 2 | Draws the empty table and opens the touch grid with its soft keys |
| Edit the counts | Reopens the grid for the current table (your own or an example) |
| Results | Six pages (five for a 2 × 3 or 3 × 2) — see below |
| Plot: observed vs expected | Observed (solid) beside expected (pale), one pair per cell, coloured by column; tap a pair or use ← → for its numbers |
| Plot: mosaic | Bar width = row share of N, tile height = row %; tiles coloured by adjusted residual (blue = more than expected, red = fewer, darker beyond \|4\|); the grey "all" bar on the right is what every bar would look like under independence |
| Plot: χ² curve and p | The χ² curve for df with the p-value shaded beyond X² and the critical value as a dotted red line |
| Set alpha | Default 0.05 |
| Examples | Four built-in tables (below) |
| Help | Two pages |

## Typing the table

Tap a cell (or move the red frame with the arrows and tap **Edit**) and type its **observed count**. Row and column totals and N update as you go. The soft keys along the bottom (the calculator numbers the menu items itself, so the program does not):

| Soft key | Does | Key shortcut |
|---|---|---|
| Edit | type the count of the framed cell | Enter |
| Values | type every count in one form | + |
| Clear | zero the whole table | — |
| Cancel | back to the menu, counts kept, results marked stale | Esc |
| Run | run the checks and compute | — |

Counts are rounded to whole numbers; a negative count, an empty table, or a row or column that adds to 0 is refused by Run with a message that says why, and the grid stays open so it can be fixed.

## The results pages

1. **Observed and expected** — O in black, E = (row total × column total) / N in blue; a cell with E < 5 gets a red frame.
2. **Percentages** — row %, column % and % of N in every cell, with the marginal percentages in the totals.
3. **The test** — χ², df, p (right tail), the critical value at α, the two-line verdict (REJECT H₀ because the data show evidence of an association…, or DO NOT REJECT H₀ because the data do not show…), Cramér's V with Cohen's label, the contingency coefficient C, the likelihood-ratio G², the smallest expected count and how many cells fall below 5.
4. **Contributions** — (O − E)²/E per cell on top (they add to χ², shown in the corner) and the adjusted residual, blue when ≥ 2, red when ≤ −2.
5. **What it means** — an APA-style line (`χ²(1, N = 674) = 13.16, p < .001, V = .14`), the decision in words, the effect size, the cell that drives the result, and the expected-count check.
6. **2 × 2 only** — p₁ and p₂, the two-proportion z (z² = χ²), Yates' corrected χ², Fisher's exact two-sided p, risk difference, relative risk and odds ratio with 95% intervals, phi.

← → or a tap on the left/right half of the screen scrolls the output (the footer shows which page you are on); Esc returns to the menu.

## Conventions

- Rows are the groups (the explanatory variable); columns are the outcome. Row % compares the groups and is the percentage to report.
- The 2 × 2 measures take **column 1 as the outcome of interest**: p₁ = O(1,1)/row 1 total, p₂ = O(2,1)/row 2 total, RR = p₁/p₂, OR = ad/bc. If a cell is 0, 0.5 is added to every cell for RR and OR (Haldane–Anscombe) and the page says so.
- Fisher's exact p is two-sided in the R / scipy sense (every table no more probable than the observed one). It is skipped, with a note, when the table is too large for the loop (more than 3,000 possible tables with these margins).
- Cohen's benchmarks for V: 0.10 small, 0.30 medium, 0.50 large. These are the df* = 1 benchmarks, which apply to all three shapes because min(rows, columns) = 2 — so V = phi = Cohen's w here.
- Expected-count rule shown on screen: all E ≥ 5 is "fine"; otherwise the page says the approximation is shaky and points to Fisher (2 × 2) or merging categories.

## The arithmetic

E = R·C/N; X² = Σ (O − E)²/E; df = (r − 1)(c − 1); p = 1 − CHISQUARE_CDF(df, X²) (note that `CHISQUARE` alone is the density); critical value = CHISQUARE_ICDF(df, 1 − α); G² = 2 Σ O ln(O/E); adjusted residual = (O − E)/√(E(1 − R/N)(1 − C/N)); V = √(X²/(N(min(r,c) − 1))); C = √(X²/(X² + N)); Yates X² = Σ (|O − E| − 0.5)²/E with the shrink floored at 0; z = (p₁ − p₂)/√(p̄(1 − p̄)(1/n₁ + 1/n₂)); RD with a Wald interval; RR and OR with log (Woolf) intervals.

## The examples

| | Table | Expected result |
|---|---|---|
| 1 | Death penalty × defendant's race, Florida murder cases 1976–87 (Radelet & Pierce 1991, as tabulated by Agresti): white 53/430, black 15/176 | X² = 1.47, df 1, p = 0.226 — no evidence of association |
| 2 | Death penalty × victim's race, same cases: white victim 64/451, black victim 4/155 | X² = 13.16, p = 0.0003, V = 0.14; RR 4.94 (1.83–13.35), OR 5.50 (1.97–15.35), Fisher p = 0.0001 |
| 3 | Gender × party identification, 1991 GSS (Agresti, *Introduction to Categorical Data Analysis*, Table 2.5): female 762/327/468, male 484/239/477 | X² = 30.07, df 2, p < 0.0001, G² = 30.02 |
| 4 | The same table transposed (3 × 2) | identical X², df and p — a transposed table is the same test |

Examples 1 and 2 together are the classic Simpson's paradox: conditioning on the victim's race reverses the defendant-race effect. Example 2 also shows RR and OR on the same data.

## Home exports (after a run)

`CS_X2`, `CS_DF`, `CS_P`, `CS_V`, `CS_N`, and the matrices `CS_OBS`, `CS_EXP` (expected counts) and `CS_RES` (adjusted residuals). On quitting, the program returns the summary line as its value, so it appears in the Home history and nothing is left open.

## First-run checks — all done

These were the things the off-device checks could not settle. All four were seen working on 10 Oct 2026: the G2 run computed a table and showed the results; the G1 run exercised the soft keys, the Values form and the three plots. Kept for the record:

1. Tap a cell on the entry grid, type a count and OK — confirm the grid redraws with the new count and the dialog's closing tap does not immediately reopen it (the drain after `INPUT` is meant to stop that). Then tap each soft key: the strip is read as y ≥ 218 in 53-px slots, and `DRAWMENU` is called after every blit so the labels should survive each redraw.
2. Tap **Values** — the four- or six-field `INPUT` form, then confirm the counts land in the right cells.
3. After a run, type `CS_EXP` and `CS_RES` in Home — these are built with `MAKEMAT` and element assignment on exported matrices.
4. Load example 2 and look at the mosaic and the curve — the two most layout-sensitive screens.

## Library check (10 Oct 2026)

Searched the fleet, about 940 hpcalc.org archives and a community library for every construct that is new to the fleet:

- **File-level `LOCAL` state** (the `cs…` variables above the first routine): documented in the command reference ("local to the program") and used by about 1,100 corpus programs, PrimeFX and the 2048 app among them. This is still the first *fleet* program to rely on it in a hardware run. (The beta 1a paste failed on that line, but at the name `csC`, not at `LOCAL` — the parser had accepted `LOCAL csR,` before it stopped.)
- **Element assignment into an EXPORTed matrix** (`CS_EXP(r, c) := …` after `MAKEMAT`): 13 corpus programs do exactly this (GameOfLife's `NextGen`, conway's `Lignes`, the astronomy demos' `statev`).
- **`INPUT` label lists built from a variable or by concatenation** (`{enLbl}`): Fingerspelling passes its title, labels and help as variables; Foundation, CostsReturn, Framework and Control Systems build labels with `STRING()` and `+`.
- **`CHISQUARE_ICDF`**: used by RANDO in the Community Library; `CHISQUARE` (the density) by StatDist v2.3.
- **FEP v1.2 and ConTable2 v1.1** use the same conventions as this program: two-sided Fisher as the sum of tables no more probable than the observed one, Yates with the `MAX(0, …)` clamp, Haldane +0.5, Woolf intervals, and a floor on printed p-values.

### Version

This guide describes beta 1k: beta 1f plus a two-line verdict in the author's words (beta 1i), the G2 and G1 runs recorded in its header (beta 1j), and the capped finger-lift drain and `RETURN` exit (beta 1k). The program was called ChiSquare until beta 1b, when it was renamed: the Prime matches built-in names case-insensitively, and `ChiSquare` is `CHISQUARE`, the density function the curve plot calls.

**Tested on:** an HP Prime G2 and G1, both running the 2026-09-09 firmware, on 10 Oct 2026. Behaviour on other firmware may differ — which characters render and which app variables a program can reach have both turned out to be firmware-dependent.

### Credit

The concept, the direction and the classroom judgement behind this program are Roger Metcalf's, as is every round of testing on real hardware. Claude did the implementation, the arithmetic and its verification against scipy and statsmodels, the off-device screen renderer, and this guide. The example data are Radelet & Pierce (1991) via Agresti, and the 1991 General Social Survey via Agresti.

**Free for educational and personal use.** Share it, teach with it, adapt it for your own classroom. Please keep the attribution with the files and credit the author if you pass them on or build on them. Not for sale or commercial redistribution. Provided as is, with no warranty — check any result you intend to rely on.

© 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).
