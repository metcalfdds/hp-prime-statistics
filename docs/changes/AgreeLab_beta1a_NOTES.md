# AgreeLab beta 1a — notes (26 Oct 2026)

Beta 1a applies every finding of the second review (see AgreeLab_beta1a_CHANGES.md). Everything below describes beta 1a.

`/home/claude/new6/AgreeLab_beta1a.txt`: 2,945 lines, pure ASCII, LF. Entry `EXPORT AgreeLab()` (no
arguments, menu first). Tag `ag_` on every helper (101 routines); file-level LOCALs start with
`ag`; Home exports `AG_K`, `AG_SE`, `AG_P`, `AG_ICC`, `AG_LOA`. No CAS, no Python.
**Runs only in the PC harness so far; not on the emulator, the G2 or the G1.**

## What it does, menu by menu

| Menu item | Pages (soft keys) | What the student sees and touches |
| --- | --- | --- |
| Two raters: categories | Tiles, Kappa, Null, Wts, Help, More → ToDiag, FromDg, Type, Menu, Back | **Tiles**: the k × k table (k = 2..6) as coloured tiles (diagonal green, off-diagonal red, deeper = more counts), row and column totals, the selected tile outlined red. Tap a tile to select it, tap it again to type a count; +/- add or remove 1; arrows move the selection; **drag from one tile to another to move one count** (the info line reports kappa before → after). ToDiag / FromDg move one count between the selected tile and its row's diagonal tile (row total kept). Right-hand panel: N, po, pe, kappa, 95% CI, kappa max, PABAK, one-sided z and p; tap any of them for a one-message explanation. A bar from 0 to 1 shows pe (magenta) and what was reached beyond it (green): kappa = green length / (1 − pe). **Kappa**: every number with its formula and source, 2 × 2 prevalence and bias indices, weighted kappas, and the Landis & Koch word **with the citation and "their convention, not a test"**. **Null**: N(0, SE₀) for kappa under H₀, the observed kappa in red with its tail shaded, its 95% CI (green) and kappa max (grey). |
| Two raters: ordered (weighted) | same view, opens on **Wts** | the weight matrix drawn on the tiles (linear or quadratic; +/- or Wts switches), linear and quadratic weighted kappa with SE and 95% CI, the z test for the selected weights, unweighted kappa beside them; "Unordered categories: use unweighted kappa" for nominal tables; tap a tile for its weight's meaning |
| Many raters: Fleiss' kappa | Kappa, Categ, Subj, Help, Menu, Back | **Kappa**: mean subject agreement P, chance Pe, Fleiss' kappa, SE under H₀, z, p, "No CI", the L&K line with citation, the P vs Pe bar; tap lines for explanations. **Categ**: kappa per category as coloured bars (overall kappa dotted), tap a bar or +/- for its share, kappa and z test. **Subj**: each subject's m ratings as a stacked colour bar, its agreement P_i underneath; tap or +/- to read counts and "x of m(m−1)/2 rater pairs agree" |
| Continuous: ICC, Bland-Altman | ICC, Data, B-A, Stats, Help, Back | **ICC**: forest plot of ICC(1,1), ICC(2,1), ICC(3,1) (blue) and ICC(1,k), ICC(2,k), ICC(3,k) (magenta) with their 95% F-based CIs; the mean squares; tap a row (or Up/Down) for its CI on the info line and a message saying what the form asks plus its F test. **Data**: one coloured line per rater across the targets (parallel = consistency, on top = agreement); tap a point to read it. **B-A**: difference vs mean, bias (green) and limits (red dotted) with their 95% CI bands, the trend line of d on the mean (magenta); tap a point; +/- steps through the rater pairs. **Stats**: bias, s, CIs, limits and their CIs, the 1986 2s version, the trend test with "no evidence of … (not proof of none)" wording, assumption checks |
| Load a preset | 7 presets | see below |
| Use my data (D1-D9) | 3 kinds | two raters: D1, D2 = codes 1-6 (k = largest code); many raters: D1-D9 = category counts, one row per subject, equal row sums m ≥ 2, ≤ 200 subjects; continuous: D1-D9 = raters, ≥ 3 targets, ≤ 1500 values. Every refusal says why |
| New two-rater table | INPUT k (2-6) | an empty table to fill on the tiles |
| Help | 9 pages | agreement beyond chance; SE, CI and the test; kappa max and the paradox; weighted kappa; Fleiss; which ICC; Bland-Altman; benchmarks are conventions; agreement vs accuracy in forensic work (+ disclaimer) |

The opening page carries the DISCLAIMER. Quit returns e.g. `"AgreeLab: Cohen's kappa = 0.208 (MS: 149 Winnipeg patients)"`.

## Formulas and sources (each is also in the routine's comment block)

- Cohen's kappa (Cohen 1960, *Educ Psychol Meas* 20:37-46); kappa max = (Σ min(pᵢ., p.ᵢ) − pe)/(1 − pe) (Cohen 1960).
- SE for the CI: Fleiss, Cohen & Everitt (1969) *Psychol Bull* 72:323-327 large-sample variance; SE₀ (under H₀) for the one-sided z test. Same as statsmodels `cohens_kappa` (`std_kappa`, `std_kappa0`).
- Weighted kappa (Cohen 1968, *Psychol Bull* 70:213-220), linear weights 1 − |i−j|/(k−1) (Cicchetti & Allison 1971, *Am J EEG Technol* 11:101-109), quadratic 1 − (i−j)²/(k−1)² (Fleiss & Cohen 1973, *Educ Psychol Meas* 33:613-619); FCE 1969 SEs.
- PABAK = (k·po − 1)/(k − 1); 2 × 2 prevalence index (a − d)/N, bias index (b − c)/N (Byrt, Bishop & Carlin 1993, *J Clin Epidemiol* 46:423-429); paradox: Feinstein & Cicchetti (1990) *J Clin Epidemiol* 43:543-549.
- Fleiss' kappa (Fleiss 1971, *Psychol Bull* 76:378-382), per-category kappa, SE under H₀ only (Fleiss, Nee & Landis 1979, *Psychol Bull* 86:974-977) — no CI is offered, and the page says why.
- ICCs (Shrout & Fleiss 1979, *Psychol Bull* 86:420-428; McGraw & Wong 1996, *Psychol Methods* 1:30-46, errata p 390) from two-way ANOVA mean squares; F-based CIs; ICC(2,1) with Satterthwaite's df v. ICC(2,k)'s bound L·k/(1 + (k−1)L) is shown as −∞ when L ≤ −1/(k−1) (pingouin and psych print the raw transform, which then exceeds the estimate). F tests: MSR/MSW for ICC(1), MSR/MSE for ICC(2), ICC(3) (McGraw & Wong Table 8).
- F quantile at a fractional df (built-in FISHER_ICDF refuses it): safeguarded Newton on the incomplete beta started from the rounded-df built-in (3-6 incomplete-beta calls); right tails as lower tails (mirror forms); probabilities clamped before every ICDF.
- Bland & Altman (1986) *Lancet* i:307-310: bias, limits bias ± 1.96 s, CI of bias ± t·s/√n; CI of a limit ± t·s·√(1/n + 1.96²/(2(n−1))) (Bland & Altman 1999, *Stat Methods Med Res* 8:135-160); trend: least-squares d on mean, t on n − 2 df.
- Landis & Koch (1977) *Biometrics* 33:159-174 bands appear only as "Landis & Koch 1977 (Biometrics 33:159-174): "fair": their convention, not a test" and on help page 8. The often-quoted "clearly arbitrary" wording was NOT checked against the paper and is not used.

## Presets (data/DATASETS_AGREE.md, a new file; DATASETS.md untouched)

MS diagnosis, Winnipeg (149) and New Orleans (69) patients (Westlund & Kurland 1953 via Landis & Koch 1977; R vcd = Friendly's msdiag.sas); Fleiss 1971 psychiatric diagnoses, 30 × 6 raters × 5 categories (R irr = statsmodels' copy; kappa 0.4302, z 17.65 = irr); peak flow, Wright vs mini Wright, 17 people (Bland & Altman 1986 Table 1 = MethComp PEFR); Shrout & Fleiss 1979, 6 × 4 (psych ICC.Rd = Howell's page); two 2 × 2 paradox tables labelled **illustrative numbers** on screen. No forensic examiner table: none with verifiable counts was found.

## What was checked (verify_AgreeLab_beta1a.py → verify_AgreeLab_beta1a_output.txt: **7383 checks, 0 failures**; beta 1 had 5734)

- Part A, through the program's own routines: Cohen/weighted kappa, SEs, p on the 4 presets, 10 edge tables (empty, pe = 1, one-category rater, total disagreement, perfect, N = 2, 3, counts of 99999, an empty category, uniform 6 × 6) and 40 random tables, against ag_ref.py (written from the papers) and statsmodels; kappa max against brute-force enumeration of every table with the same margins (30 cases); Fleiss on the preset (= irr's kappa and z), 25 random sets and 2 edge sets, per-category kappa against Fleiss' kappa of the collapsed 2-category table; ICCs, CIs and F tests on both presets, 25 random matrices and 4 edge sets (all equal, offset only, negative ICC, values ±1E6) against ag_ref (SciPy quantiles) and pingouin (values exact; CIs at pingouin's 2 decimals), Shrout & Fleiss's .17 .29 .71 .44 .62 .91 and Howell's −0.133 to 0.723; `ag_FQ` against SciPy at 30 fractional-df points (≤ 2E-7 relative, ≤ 1E-4 above 1000 df), `ag_FUp` at 15; Bland-Altman on the presets, 2 edge and 20 random sets against ag_ref and scipy `linregress`, and Bland & Altman's printed −2.1, 38.8, 9.4, t 2.12, −22.0 to 17.8 (their −79.7/75.5 come from the rounded bias and s); every preset against its downloaded source files.
- Part B, 30 harness runs of every menu path (both two-rater pages, the drag, +/-, arrows, ToDiag, FromDg, Type, Clear, Fleiss pages and taps, ICC/Data/B-A/Stats with taps and pair stepping, every preset, all three D1-D9 loaders with 11 refusals, degenerate data, new table, all 9 help pages; six runs again in stale-key mode): the numbers on the pages equal the references as displayed; no runtime error; no scientific-notation string; no MSGBOX over 5 lines; no text estimated off screen or past its width; no page skipped by a left-over key.
- Gate (`gate_AgreeLab_beta1_output.txt`): **PASS**. Kit lint 0 errors; ppl_check clean; fleet_names 0 collisions / 0 untagged / 0 built-in matches over 28 files. lint_ppl's 6 "problems" are its known noise (5 EXPORT-discipline lines; line 1319 flags `agK` inside a TEXTOUT_P *coordinate*, not a concatenation). Full parse fails at the file-level LOCAL before EXPORT, the known tool limit (AnovaLab beta 1a gives the same).
- Definition order: every `ag_` routine is defined before it is called (assemble.py checks; no forward declarations).

## Not done / left out, and why

- No CAS (nothing here needs an exact closed form) and no Python.
- Fleiss' kappa has no CI: the published SE holds only under H₀ (said on screen).
- Kappa CI is the large-sample Wald interval; the Kappa page flags N < 30 in red. No exact or bootstrap CI in beta 1.
- Fleiss' data need the same number of ratings per subject; ICC needs complete data (no missing cells).
- Only the 95% level is offered (no Set α).
- Krippendorff's alpha, Gwet's AC1, Scott's pi: not in the spec, not included.
- Glyph κ is not on the verified list, so "kappa" is spelled out everywhere.

## Bugs found and fixed during the build (for the reviewer)

1. `agBSel` (the selected B-A point) was also used for the SE of a limit → a red "selected" point appeared untapped; renamed the SE `agBSL` (a regression check now taps point 9).
2. An ICC lower bound of −99 or below was read as "no CI" (a −99 sentinel): replaced by a flag list `agICf`.
3. ICC(2,k)'s transformed lower bound exceeded the estimate when L ≤ −1/(k−1): now −∞.
4. Plain bisection for the F quantile (60 incomplete-beta calls, perhaps 10 s on a G1) replaced by safeguarded Newton.

## DEVICE CHECKLIST (in this order; expected numbers from SciPy/statsmodels)

New in beta 1a. Check these first:

- A. **Tap and drag.** On the MS Winnipeg Tiles page, tap A2,B1 near its right edge, letting the finger slide a pixel or two. The tap must only select the tile; no "1 moved" message. A deliberate drag of half a tile or more into A2,B2 moves one count (kappa 0.208 → 0.217). Report whether a real drag of less than half a tile is ever too short to register.
- B. **Edited preset.** After any change, the info line reads "edited from Landis & Koch 1977" in red once it is clear, and the Kappa page's first line says the same. The title ends "(edited)", and Quit ends ", edited from Landis & Koch 1977". Reload the preset: the mark is gone.
- C. **Kappa at the edges.** In D1 put 12 ones and then 9 twos; in D2 put 12 twos and then 9 ones. Use my data → Two raters: kappa −0.960, "95% CI (clipped):", "−1.000 to −0.728", "p > 0.9999". Then D1 = 1, 2 and D2 = 1, 2: "no SE, CI or p: N < 10" on Tiles, Kappa, Null and Wts.
- D. **ICC edge cases.** D1 = 1, 2, 3, 4 and D2 = 6, 7, 8, 9 gives ICC(1,1) −0.579, ICC(2,1) 0.118 (with its CI) and ICC(3,1) 1.000, with "no F interval (error MS = 0)". D1 = 1, 2, 1, 2, D2 = 2, 1, 2, 1, D3 = 1, 2, 1, 2 gives ICC(2,k) "--" and "undefined (denominator 0)", with no marker and no "ᴇ" anywhere.
- E. **Bland-Altman labels.** Stats shows "approx. SE of a limit (B & A 1986) = 16.40" and "approx. 95% CI, …". The line "with 2s (as in 1986): −79.65 to 75.41" is followed by "the paper, rounding, prints −79.7 to 75.5". Help page 7 has the coverage lines.

The checklist from beta 1 follows (its numbers still hold; in step 13 the CI lines now begin "approx."):

1. **Paste and Check** in the Program Catalog (Shift Program → AgreeLab → Check). Then run `AgreeLab` from Home without parentheses. Opening page: title, three blue lines, three magenta lines, red DISCLAIMER box. Any key → main menu with 9 items.
2. **Two raters: categories** (MS Winnipeg preset, loaded at start). Tiles page: 4 × 4 tiles, diagonal green (38 darkest), off-diagonal red (33 darkest); totals 44 47 35 23 (right) and 84 37 11 17 (below). Panel: N = 149, agree po = 0.430, chance pe = 0.280, kappa = 0.208, 95% CI 0.109 to 0.307, kappa max = 0.627, PABAK = 0.239, 1-sided z = 4.56, p < 0.0001. Check the font-2 "kappa = 0.208" fits, and the bar: magenta to 0.28, green to 0.43, labels "pe" and "po" not overlapping, "0" and "1" at the ends.
3. **Drag** a finger from tile A2,B1 (33) to A2,B2 (11): info line "1 moved A2,B1 to A2,B2: kappa 0.208 → 0.217"; the → glyph. Try a quick drag and a slow one; a plain tap on a tile must select it, a second tap opens the "Count in the selected tile" form. Report whether a light tap is ever read as a drag.
4. Arrows move the red outline; **+** and **−** change the selected count. Tap the panel's numbers: each gives a short message (count the lines: 5 or fewer, nothing cut). Tap a header number: the info line names the category ("row 1 = A said Certain MS").
5. Soft key **More**, then **ToDiag** / **FromDg** / **Type** on an off-diagonal tile. Enter → menu → "Clear the table": empty-table message; select A1,B1 and press + once: "kappa undefined: pe = 1".
6. **Kappa** page (MS Winnipeg reloaded from Presets): lines as in step 2 plus "SE₀ = 0.046, z = 4.56", "weighted kappa: linear 0.380, quadratic 0.525", "Landis & Koch 1977 (Biometrics 33:159-174):" / ""fair": their convention, not a test". Check the quote marks and that no line is cut at the right edge.
7. **Null** page: a tall narrow blue curve around 0, red line at 0.208 far in its tail, green CI bar from 0.109 to 0.307, grey dotted line at 0.627. Tap → message.
8. **Wts** page: tiles show 1, .67, .33, 0 (linear); right panel linear = 0.380 (SE 0.052, CI 0.279 to 0.481), quadratic = 0.525 (SE 0.060, CI 0.407 to 0.642), unweighted 0.208; + switches to quadratic tiles (1, .89, .56, 0). Check "1 - |i-j|/(k-1)" and the ² glyphs.
9. Presets → **Paradox: lopsided**: kappa 0.318, po 0.850, kappa max 0.773, PABAK 0.700, prevalence index 0.75, bias index 0.05, "ILLUSTRATIVE NUMBERS, not data" in red. **Paradox: balanced**: kappa 0.700 with the same po 0.850.
10. **Many raters** (Fleiss preset loaded at start): mean subject agreement 0.556, chance Pe 0.220, Fleiss' kappa = 0.430, SE under H₀: 0.0244, z = 17.65, p < 0.0001, "No CI: …". **Categ**: bars 0.24, 0.24, 0.52, 0.47, 0.57 in five colours, dotted red line at 0.430; tap bar 2: "share p = 0.144", "kappa = 0.245, z = 5.19". **Subj**: 30 stacked bars; tap subject 7: counts 0, 0, 4, 0, 2; "7 of 15 rater pairs agree: P = 0.467".
11. **Continuous** (peak-flow preset): a "Working" page first — **time it on the G1** (two F quantiles at a fractional df; not yet timed). ICC page: 0.946, 0.946, 0.943, 0.972, 0.972, 0.971; tap the ICC(2,1) row: info line "ICC(2,1) = 0.946, 95% CI 0.857 to 0.980" and a message ending "F = 34.03 on 16, 16 df, p < 0.0001 (H₀: ICC = 0)." MS line: targets 25572.3, raters 38.12, error 751.37.
12. **Data**: blue (Wright) and red (Mini Wright) lines over 17 targets; tap the first blue point: "target 1, Wright = 494.00 l/min". Tap twice more: the redraw should be quick (G2 cache).
13. **B-A**: "bias -2.118, 95% limits -78.10 to 73.86 l/min"; light green band around the bias, light red bands around both limits, red dotted limits, magenta trend line nearly flat; tap a point: its line, the point turns red. **Stats**: 95% CI for the bias −22.05 to 17.81 (t = 2.120); SE of a limit 16.40; lower limit CI −112.85 to −43.34; upper 39.11 to 108.62; "(B & A 1986 used 2s: −79.65 to 75.41)"; slope 0.0287 (SE 0.0882), t = 0.33 on 15 df, p = 0.7495, "no evidence of a trend at α 0.05 (not proof of none)". Check √ and ².
14. Presets → **Shrout-Fleiss**: ICCs 0.166, 0.290, 0.715, 0.443, 0.620, 0.909 (published .17 .29 .71 .44 .62 .91); ICC(1,1) CI −0.133 to 0.723, ICC(1,k) CI −0.884 to 0.912 (its bar runs nearly to the left edge, −1); B-A + steps J1-J2 → J1-J3 → J1-J4 ….
15. **Use my data**: put 1,2,2,3,1,1,3 in D1 and 1,2,3,3,2,1,1 in D2 (Statistics 1Var): Two raters → N = 7, kappa = 0.344 (3 × 3 table). Then an unequal-length D2: refusal message.
16. **Help** from the main menu: all nine pages; ← goes back, Esc leaves. Page 7 has √ and ±; page 8 lists the bands.
17. **Quit**: Home shows "AgreeLab: …" and `AG_K`, `AG_ICC`, `AG_LOA` hold values.
18. Timing to report (G1): the drag redraw on a 6 × 6 table, the Fleiss Subjects page, the ICC "Working" page with your own 500 × 3 data.
