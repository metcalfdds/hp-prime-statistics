# ResampLab beta 1a — notes (21 Oct 2026)

**beta 1a** applies every finding of the independent second review (`REVIEW2_ResampLab_beta1.md`); the list is in `ResampLab_beta1a_CHANGES.md`. Beta 1's notes follow, updated where beta 1a changed something. `ResampLab_beta1.txt` is kept unchanged beside it.

`/home/claude/new6/ResampLab_beta1a.txt` (2,921 lines, pure ASCII, LF). Entry `EXPORT ResampLab()` (no arguments, opens on its title page with the disclaimer, then the menu). Tag `rs_` on all 100 helpers; file-level LOCALs start with `rs`; Home exports `RS_...`. **Neither beta 1 nor 1a has run on hardware or the emulator; PC harness only.**

## What it does, menu by menu

| Menu item | Page |
| --- | --- |
| Permutation test: 2 groups | Two rows of dots (A teal, B amber, coloured by the group each value *came from*); null histogram below; observed d as a red line (mirror dotted when two-sided). **Once** deals the pooled values again (dots slide to their new rows in two frames), drops d onto the histogram with a green mark. **x10 / x100 / x1000**: progress panel, histogram redrawn every 2 s, bar between, Esc stops (the shuffles done are kept). Status: observed d and Ha; "random B shuffles: c with \|d\| ≥ obs"; p = c/B and the plus-one p (c+1)/(B+1). **More**: Ha (≠, A > B, A < B; counts for all three are kept, so switching costs nothing), Stat (mean ↔ median; restarts), Exact, Info (two pages), Help. |
| Permutation test: paired | One lollipop per pair from 0 to the signed difference (blue kept, amber flipped; >19 pairs: a dot plot). Once flips each sign with probability ½, animated. Same histogram, status, More (no Stat: the mean difference). |
| Bootstrap CI: one sample | The sample as grey ticks; after **Once**, the resample as stacks (a value picked k times = k dots), "last resample: 15 of 41 not picked", θ* on the right. Histogram of θ* with θ̂ red, percentile ends magenta, BCa ends dotted green (B ≥ 100). Status: estimate, B, SE* (SD of the B values), the percentile and BCa intervals (or why BCa is refused). **More**: Stat (mean → median → SD → 10% trimmed mean), CIs (percentile, basic, BCa, t side by side with widths and a bar picture), BCa (counts below/equal, share, z₀, jackknife range, a, α₁, α₂), Level (90/95/99%), Help. |
| Bootstrap CI: two groups | Both groups resampled from themselves; difference of means or medians; percentile (and basic) interval; Welch t for means. |
| Load a preset | MockJury (Unattractive v Beautiful; Unattractive v Average), Rossi, Darwin, BJS, 5 v 5 illustrative. Shows a data page (name, source line, n / x̄ / s per group, a strip plot), then opens the suitable lab page. |
| Use my data (D1, D2) | D1 = group A or the sample, D2 = group B (both read inside IFERR; up to 1,000 values each). Equal lengths: D1 − D2 serves as the paired differences AND is what the one-sample bootstrap resamples (as for Darwin); D2 empty: D1 is the one sample and the differences. |
| Seed, confidence level | INPUT: seed (0 = fresh; a whole number up to 999,999,999) and level (0.5–0.999). |
| Help | Five pages (shuffling labels; exact/random/paired; the bootstrap; keys, touch, seed; Home, sources, disclaimer). |
| Quit | RETURNs "ResampLab: <last page's summary>" (never PRINT). |

Keys on every lab page: + = Once, Enter = a CHOOSE of every action (keyboard-only route), Esc = back / stop. Taps: a dot (its value, current and original group), a lollipop (pair, d, kept/flipped), a resampled value (times picked), a histogram bin (its range, count, how many in the tail), the red line (the observed value), the status lines (open Info or CIs). Soft keys are read GETKEY + MOUSE style (y ≥ 218, slot `MIN(6, IP(x/53.4)+1)`), slot 6 "More" on both pages.

Home: `RS_P` (plus-one Monte Carlo p, −1 if none), `RS_PX` (exact p or −1), `RS_NB` (B), `RS_OBS`, `RS_PCT`, `RS_BCA` (interval ends, `{}` if none), `RS_STAR` (the bootstrap values).

## Formulas and sources

* Two-group permutation (Pitman 1937; Ernst 2004 *Stat Sci* 19:676): d = stat(A) − stat(B). One shuffle = a partial Fisher–Yates shuffle of the **smaller** group only (k draws: `j = i + MIN(N − i, IP(RANDOM (N − i + 1)))`), and for the mean only its sum S is needed: d = S_A/n_A − (Tot − S_A)/n_B. Medians use the sorted pooled values, so the drawn indices sorted give that group in order; the other group's order statistics come from a complement walk (`rs_CompAt`). The observed d is computed by the same code from the observed split, so ties are exact; a tolerance absorbs rounding: beta 1a makes it relative, 1E−9 × the pooled range (paired: × mean |d|); beta 1's "+ 1" tied every split of data on a 1E−10 scale.
* Tails: upper d ≥ obs, lower d ≤ obs, two-sided |d| ≥ |obs| (stated on Help/Info). Monte Carlo p = c/B; plus-one (c+1)/(B+1) (Phipson & Smyth 2010, *SAGMB* 9(1) art. 39); MC SE √(p(1−p)/B) on the Info page.
* EXACT two groups: every split, lexicographic over the drawn group's indices with the sum updated, when C(N, k) ≤ 2,000 (`rsExLim`). Cost justification below. beta 1a: C(N, k) is never formed (`rs_Splits` builds it term by term and stops past the limit; its size above that from logs), so 1,000 v 1,000 cannot overflow.
* Two-sided is |d| ≥ |obs| (Pitman; the textbooks). This is NOT SciPy's `permutation_test` default (2 × the smaller one-sided p): they agree for symmetric designs such as 5 v 5, differ for unbalanced or tied ones (2 v 9: 24/55 v 26/55).
* Paired (Fisher 1935, *Design of Experiments* sec. 21): each sign flips with probability ½; statistic the mean difference. EXACT: if the |d| become whole numbers after ×f (f from 1, 2, 4, 5, 8, 10, … 1000) with Σ|d|f ≤ 9,998, n ≤ 39 and (beta 1a) n·Σ|d|f ≤ 20,000 (Darwin 15 × 544 = 8,160), the 2ⁿ patterns are **counted by their sums** (subset-sum recursion `cnt(U + a) += cnt(U)`, U counted down; the signed total is A − 2U, so tails are integer comparisons). Darwin's eighths: Σ = 544, about 4,000 additions instead of 32,768 × 15. Otherwise, n ≤ 12: all 2ⁿ patterns in Gray-code order (one sign flipped per step). Otherwise random flips.
* Histogram bins are centred on the observed value; when the statistic lives on a lattice of step δ (whole-number data after ×f: means (1/n_A + 1/n_B)/f, medians 0.5/f, paired 2/(nf), bootstrap mean 1/(nf), …) the bin width is an **odd** number of lattice steps, so no possible value sits on a bin edge and no bin is empty by accident. The plot range uses the exact permutation SD of the mean difference, σ²N²/(n_A n_B (N − 1)) (σ² with divisor N); values beyond the ends go in the end bins with a "<" / ">" mark (the p-value counters do not use the bins).
* Bootstrap (Efron 1979; Efron & Tibshirani 1993): n draws with replacement, `MIN(n, 1 + IP(RANDOM n))`, in order. Statistics: mean, median, SD (n − 1, two-pass), 10% trimmed mean (IP(n/10) cut from each end, = `scipy.stats.trim_mean(x, 0.1)`). Quantiles "linear" (Hyndman–Fan 7, numpy's default, what `scipy.stats.bootstrap` uses).
  * percentile: q(α/2), q(1 − α/2); basic: 2θ̂ − q(1 − α/2), 2θ̂ − q(α/2) (Davison & Hinkley 1997 ch. 5);
  * beta 1a: the jackknife is one pass (closed forms; prefix sums for the trimmed mean), with a progress bar and Esc above n = 300.
  * BCa (Efron 1987 *JASA* 82:171; E&T 1993 ch. 14): z₀ = Φ⁻¹((#below + #≤)/(2B)) (ties count half, as SciPy); a = Σ(J̄ − Jᵢ)³ / (6[Σ(J̄ − Jᵢ)²]^1.5) from the jackknife; α₁,₂ = Φ(z₀ + (z₀ ± z)/(1 − a(z₀ ± z))), z = Φ⁻¹(α/2). Refused, with the reason on screen, when a = 0/0, when θ̂ lies outside every bootstrap value (share 0 or 1), or when 1 − a(z₀ ± z) ≤ 0.
  * t (mean): x̄ ± t(n−1) s/√n with t = −STUDENT_ICDF(n − 1, α/2) (right-tail quantile as a mirrored lower one, Lessons §3). Welch for two groups (fractional df: STUDENT_ICDF takes any df).
* Speed guard: every bulk run times its first 20 with TICKS, and (beta 1a) again at every 2-s redraw on the time used; if the whole run would take over 75 s **on this calculator**, it is cut to about 60 s' worth, in whole hundreds, and the status line says "capped at N: about 60 s on this calculator". beta 1a: the redraw during a run no longer recomputes the intervals (it sorted every value every 2 s).
* Randomness: bare `RANDOM` (device-verified). **RANDSEED**: in `HP_Prime_Builtin_Names.txt`; hp-prime-kit measured on the emulator that `RANDSEED(1); A := RANDOM(); RANDSEED(1); RETURN A - RANDOM();` gives 0; **not yet run on our G1/G2**, and the harness lacks it (the verify script supplies one that reseeds the harness RNG). Called inside IFERR at every Reset/start when a seed is set; a failure is reported. `RANDINT` exists in the names list and the harness but its bounds are unverified, so it is not used.
* No CAS, no Python.

## Presets (data/DATASETS.md; source line shown on the data page and the Info page)

| Preset | Values | Source shown |
| --- | --- | --- |
| MockJury U v B | Years: Unattractive 37, Beautiful 39 (A − B = 1.477) | Plaster (1989) M.A. thesis, East Carolina Univ.; data via R heplots (Friendly) |
| MockJury U v Avg | Unattractive 37, Average 38 | same |
| Rossi | week of first arrest, the 114 arrested: aid 48, no aid 66 (d = 0.392) | Rossi, Berk & Lenihan (1980) *Money, Work, and Crime*; data via Allison (1995), R carData. Caveat on screen: only the arrested — timing, not whether. |
| Darwin | 15 crossed and 15 selfed heights (in), 15 pairs in 4 pots (the CSV's `pot`); d = cross − self = Fisher's eighths 49, −67, … (checked) | Darwin (1876); Fisher (1935) *The Design of Experiments*, sec. 21 (15 pairs in 4 pots) |
| BJS | 41 months served (mean 155.07, median 150, s 25.86, skewness 0.46: only mildly skewed) | BJS, NCJ-153858 (1995), via R crimedatasets |
| 5 v 5 | A = 14, 18, 12, 16, 15; B = 10, 13, 9, 14, 11 | labelled "ILLUSTRATIVE NUMBERS (not data)" everywhere |

Darwin: this program (and an independent itertools enumeration) counts **1,726 of 32,768** sign patterns with |d| ≥ observed (p = 0.0527) and **863** with d ≥ observed (0.0263). Fisher's own figure is in *The Design of Experiments*; it was **not checked against the book** and the screen says so.

## Reworked TI programs and the bugs not repeated

* Triola, *Elementary Statistics Using the TI-83/84 Plus* 2nd ed., the bootstrap CI project (about p. 393) — here as the one-sample bootstrap page, with resamples shown.
* **BOOT** (`ref/triola_ti_programs/BOOT__133.txt`): its jackknife acceleration and BCa percentile formula are kept. Not repeated: z₀ from values **≤** θ̂ (biased with ties — medians); the `While ʟBOOT(I) ≤ θ` loop running past the list end when all values ≤ θ̂, and invNorm(0) when none are; division by zero in a when all jackknife values are equal; `log(abs(θ))` for rounding digits (error at θ = 0); list typed by name and DelVar'd.
* **RANDSAMP** (sorting on random keys for sampling without replacement): replaced by a partial Fisher–Yates shuffle, O(k), no sort.
* TI "Resampling" activity (named in the brief; not found in `ref/triola_ti_programs/`, so not checked): the two-group page.
* Triola's page "about p. 393" is from the brief, not checked against the book.

## What was checked (verify_ResampLab_beta1.py; output beside it)

beta 1: 687 checks, 0 failures (`verify_ResampLab_beta1_output.txt`). beta 1a: see `verify_ResampLab_beta1a_output.txt` — **767 checks, 0 failures**. Part R adds one section per review item (R1 stale-key drain on every action; R2 jackknife; R3 1,000 v 1,000; R4 redraw and cap; R5 1E−10 and 1E10 scales; R6 Darwin's pots; R7 no "= <"; R8 the lesser items), and Part A adds: MSGBOX ≤ 100 characters, no "= <" anywhere.

* **E — exact**: two-group exact counts (C, ≥, ≤, |≥|) against itertools.combinations in exact Fractions on 29 designs × mean and median (5 v 5, n = 2 v 2, ties, decimals, negatives, a 1,000,000 outlier, an all-equal group, d = 0, 15 random designs up to C(14, 7) = 3,432, run through the engine directly); the exact histogram sums to C; `scipy.stats.permutation_test` exact one-sided p on 8 designs. Paired: 17 designs (Darwin, n = 2, zeros, decimals, off-grid floats by the Gray route at n = 8 and 12, 7 random) against itertools.product.
* **M — Monte Carlo**: the harness's RANDOM numbers are logged and the program's shuffles/flips replayed in Python; counts identical (5 v 5, MockJury mean and median, Rossi, MockJury U v Avg, Darwin, a paired set). MC p within 3.3 binomial SE of the exact p or of a 200,000-shuffle numpy run.
* **B — bootstrap**: resample indices rebuilt from the logged RANDOM numbers; the program's θ* equal numpy's on those indices; percentile, basic, BCa equal `scipy.stats.bootstrap` **given the same resamples** (a numpy Generator subclass whose `integers()` returns them), and α₁, α₂, a equal SciPy's `_bca_interval` and a direct computation; t against `scipy.stats.t.interval`; SE* against numpy; 4 statistics × 17 data sets + BJS at 90/95/99%; BCa refusals (median with ties: a = 0/0; SD of near-constant data) agree with SciPy's NaN. Two groups: θ*, percentile against SciPy with two samples, Welch against `ttest_ind(...).confidence_interval`.
* **H — menus in the harness**: every preset; Once, x10, x100, x1000, Reset, More, Ha ×3, Stat, Exact, Info, Help, CIs, BCa, Level; the Enter menu and +; taps on bins, dots, lollipops, resampled values, the title, the status lines; Use my data (D1+D2, D1 only → Gray route, no D1, all-equal data, one value); Settings (seed repeats a run, different seed differs, bad seeds and levels refused); Esc during x1000 ("stopped by Esc after N"); Esc during a 1,716-split exact count (marked unused; a second count completes); 7 v 7 (3,432 splits) refused with the reason; the 60-s cap (TICKS sped up to 5 s per reading); stale-key mode; Quit's summary. Page numbers checked against the values above (e.g. "exact p = 12/252 = 0.0476", "exact p = 1,726/32,768 = 0.0527", the BJS percentile and BCa lines against SciPy on the same 1,000 resamples, the Welch line).
* **S / A — static and audits**: pure ASCII; every routine defined before its first use; no two file-level names equal ignoring case (beta-1 drafts had `rsB` twice and `rsHa`/`rsHA` — both found here and fixed); no `PRINT`; over every run: no runtime error, `h.sci_strings` empty, no text past 320 px or its width at 6.5 px per font-1 character, text-page lines above the footer, MSGBOX ≤ 5 lines, CHOOSE lines ≤ 30 characters (main menu ≤ 27).
* Gate: `gate_ResampLab_beta1_output.txt` — kit lint 0 errors; ppl_check clean; fleet_names 0 collisions / 0 untagged / 0 built-in matches; full parse stops at the second `EXPORT` line (the known tool limit, as for ChiTable); lint_ppl's remaining items are its known noise (no function named after the file, EXPORT-discipline lines, "bare" concatenations that are already strings from `rs_Fmt`).

## G1 speed (estimates — nothing has run on a calculator)

Harness time per item after warm-up (PC), and the brief's ×30–100 rule for a G1:

| Page / statistic | harness ms per item | x1000 on the PC | G1 by ×30–100 |
| --- | --- | --- | --- |
| 5 v 5, mean shuffle | 0.79 | 0.8 s | 24–79 s |
| MockJury, mean shuffle | 2.7 | 2.7 s | 80–270 s |
| MockJury, median shuffle | 3.6 | 3.6 s | 110–360 s |
| Rossi, mean / median shuffle | 3.4 / 5.6 | 3.4 / 5.6 s | 100–560 s |
| Darwin, sign flips | 0.53 | 0.5 s | 16–53 s |
| BJS bootstrap: mean / median / SD / trimmed | 1.7 / 1.7 / 2.8 / 2.0 | 1.7–2.8 s | 50–280 s |
| MockJury two-group bootstrap: mean / median | 2.5 / 2.5 | 2.5 s | 75–250 s |
| exact split, mean / median (5 v 5) | 0.47 / 0.51 | — | 2,000 splits: 28–100 s |
| Darwin exact by sums (whole count) | 270 ms in all | — | 8–27 s |

(`timing.py`, `timing_output.txt`; the PC was shared with other jobs, so the harness numbers vary by about 2× between runs.)

A second estimate from GaltonBoard's measured G1 speed (×100 balls ≈ 0.5 s for ≈ 2,500 simple statements, i.e. roughly 5,000 statements/s) puts a MockJury mean shuffle (37 draws × 5 statements + bookkeeping ≈ 200) at about 40 ms, so x1000 ≈ 40 s. The two estimates disagree by up to 5×; by the brief's rule most x1000 runs would pass 60 s on a G1. That is why the program **measures itself** (TICKS after the first 20) and cuts a run that would exceed ~75 s to what fits in ~60 s, saying so on screen; a G2 (faster) will usually run all 1,000.

The exact limit is **2,000 splits** (C(12, 6) = 924, C(13, 6) = 1,716 fit; C(14, 7) = 3,432 does not): 0.47–0.51 ms a split in the harness ⇒ 28–100 s on a G1 by the ×30–100 rule (about 8 s by statement count), with a progress bar and Esc. 5,000 (the spec's example) would be 70–255 s by the rule, too long for a class.

## Left out / open

* RANDSEED unverified on our hardware (checklist item 2). The second review found it in a library program (BlackJack.hpprgm), so it should paste. If it is missing at paste, delete `rs_Seed`'s IFERR line and the program still runs (seeding off).
* Data below about 1E−6 display as 0.000000 (the fleet never prints scientific notation); the tests are right, the numbers on screen are not readable. Rescale such data.
* Two-group bootstrap has no BCa (the spec asks for percentile); basic is shown on its CIs page.
* No CAS (exact p is shown as a count over a count, which is already exact).
* A tap on a dot finds the nearest value by x in the tapped row; stacked dots of equal value are not told apart.
* G1 drawing speed of the Once animation (two in-between frames of up to ~120 dots) is unknown; skipped above 160 pooled values.

## DEVICE CHECKLIST (in order; G1 first, then G2)

1. Paste `ResampLab_beta1a.txt` (the staging copy `ResampLab.txt`) in the Connectivity Kit; on the calculator Program Catalog → ResampLab → Edit → **Check**. Expected: no syntax error. If the cursor stops at `RANDSEED`, report it (fallback: remove that one line).
2. Run ResampLab. The title page shows the red DISCLAIMER paragraph. Any key → menu with 9 items, none cut off. In Home after quitting, type `RANDSEED(1); RANDOM` twice — the two answers should match (confirms RANDSEED).
3. Load a preset → 5 v 5 → data page (label "ILLUSTRATIVE NUMBERS (not data)") → any key → two-group page; the bottom line reads "+ = Once, Enter = actions, Esc = back". More → Exact: status "exact: 12 of all 252 with |d| ≥ 3.60", "exact p = 12/252 = 0.0476". Ha (×1): 6/252 = 0.0238; Ha again: 249/252 = 0.9881; Ha again: back to 12/252. **Time the Exact count** (252 splits; the 2,000-split limit assumes about 15–50 ms per split on a G1).
4. More → Once: two dots-moving frames, a green ∨ over the new histogram dot. Then x1000: progress bar grows, histogram redraws every ~2 s, "about N s left". **Time it**; p should land near 0.048 (two-sided).
5. Back (Esc) → menu → Load a preset → MockJury Unattr. v Beaut. Status "observed x̄A − x̄B = +1.477". x1000: **time it**. If it would take > 75 s the run stops at about 60 s, at a whole hundred, with "capped at N: about 60 s on this calculator" (beta 1a: check the run really ends near 60 s). p (two-sided) near 0.10 (numpy, 200,000 shuffles: 0.105). More → Stat (median): observed medA − medB = +2.00; x100; p near 0.25.
6. Tap a dot in row A, a histogram bar, the red line, and the status lines: each gives a one-line note (or the Info page). Press + (Once) and Enter (Actions menu) from the keys.
6a. **beta 1a key drain:** on MockJury, More → Exact: a box says the splits are too many ("C(76, 37) = about 10^21 splits ..."). Close it with Enter: the page must come back WITHOUT the Actions menu. Repeat closing it with a finger tap: no Info page should open. Same on BJS: More → CIs before any resample ("Run at least 100 resamples first").
7. Esc during a x1000 run: it stops within a second and the status reads "stopped by Esc after N".
8. Load Darwin → the data page says "(15 pairs in 4 pots)" → paired page with 15 lollipops; before a shuffle the status says "Each shuffle flips each pair's sign at random". More → Exact: "exact p = 1,726/32,768 = 0.0527" — **time it** (expected a few seconds: about 4,000 additions). Info page 2: "Fisher (1935, sec. 21) worked this test on these data".
8a. Use my data with D1 = 1, 2, ..., 15 (D2 empty) → paired → More → Exact: "exact p = 2/32,768 (p < 0.0001)"; nowhere "= <" (Info page; Quit's Home line too).
9. Load BJS → one-sample bootstrap (the status names it: "mean of months = 155.07, n = 41"); Darwin's bootstrap says "mean of differences cross - self". Once: stacks over some ticks, "last resample: k of 41 not picked". x1000 (**time it**; during the run the status says "intervals at the end"; after x1000 a tap on a value says "(a value in the sample)"): 95% percentile about (147, 163), BCa about (147.5, 164); the t-interval on CIs is (146.910, 163.236) exactly (no randomness). More → BCa: z₀ near 0, a ≈ +0.01; More → Stat ×3 (median, SD, trimmed mean 153.70); Level (99%, then 90%).
10. Menu → Bootstrap CI: two groups with MockJury loaded: x100; Welch t 95% = (−0.321, 3.276) exactly.
11. Seed, confidence level (help lines "0 = fresh; a whole number repeats a run", "0.5 to 0.999 (0.95 = 95%)" fully visible): seed 2026 → load 5 v 5 → x100 → note p; Reset → x100 → the same p (and the same on a second calculator). Seed −1 or level 1.2: refused.
12. Use my data: put 6 values in D1 and 6 in D2 (Statistics 1Var). Two-group page and paired page both give an exact p; with D1 only, the paired page treats D1 as differences.
12a. **beta 1a:** put 1,000 values in D1 and 1,000 in D2; two-group page opens (no error); More → Exact says "about 10^600 splits"; x10 works. One-sample bootstrap on 1,000 values: a "Jackknife for BCa" bar for a moment (**time it**; Esc there gives "BCa: jackknife stopped by Esc" and the page still works).
13. Quit: Home shows "ResampLab: <the last page's summary>"; `RS_P`, `RS_PX`, `RS_NB`, `RS_OBS`, `RS_PCT`, `RS_BCA`, `RS_STAR` hold values.
14. Look for: any text cut at the right edge (font 1 assumed 6.5 px per character), the two "<"/">" end-bin marks, the dotted mirror line for a two-sided test, glyphs x̄ ≥ ≠ ≤ ± √ ₀ ₁ ₂ α.
