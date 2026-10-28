# FitCheck beta 1 -- second review (independent)

Reviewer: Claude (second reviewer; did not write the program), 21 Oct 2026.
File reviewed: `/home/claude/new6/FitCheck_beta1.txt` (2,987 lines, as assembled). Read in full against
`ref/HP_Prime_Lessons_Learned_v7n.md` and `BRIEF_NEW6_v1.md`. My own scripts are in my scratchpad
(`r2/drv.py`, `t1.py`, `t2.py`, `data_chk.py`, `stat_chk.py`, `awk_chk.py`, `cnt_chk.py`,
`listarith/scan.py`). All reference values come from scipy 1.18.1 / statsmodels 0.15.0 or a
simulation I ran, not from the builder's verify script.

Findings are ranked, most serious first.

---

## 1. Runtime error: the Bars page after Unmrg on a normal fit on bins (HIGH, CONFIRMED)

**Line 1490** (`fc_DrawBars`):
```
IF fcKind == 6 THEN
  dbS := fc_I((fcMid(fcMS(dbI)) + fcMid(fcME(dbI))) / 2);
  IF fcMrg == 0 THEN dbS := fc_I(fcMid(dbI)); END;
END;
```
The merged-label expression runs before the `fcMrg == 0` test. After Unmrg, `fcMrg = 0` but `fcMS`/`fcME`
still hold the *merged* grouping, which is shorter than `fcK`, so `fcMS(dbI)` is read past its end.

**Failure scenario.** Load a preset → crimtab → (any key) → Bins → Unmrg. The harness stops with
`PPLError: index 19 out of range in fcMS (1..16)`. Rossi → Bins → Unmrg gives `index 13 out of range in fcMS (1..12)`.
Unmrg on the Table or Test page does not crash, but the next tap on Bars does, and so does
"χ² goodness of fit → The last fit again" afterwards. This is the documented flow ("Unmrg shows every bin",
help page and NOTES), and on the calculator it opens the Program Editor in front of a class.

**Fix.** Put the merged label inside an ELSE:
`IF fcMrg == 0 THEN dbS := fc_I(fcMid(dbI)); ELSE dbS := fc_I((fcMid(fcMS(dbI)) + fcMid(fcME(dbI))) / 2); END;`.
Also add a verify case that runs Bins → Unmrg → Bars for crimtab, Rossi and a D1 sample. The builder's
verify script never pressed Unmrg on a kind-6 Bars page.

## 2. Draft lottery: the 2-cell goodness-of-fit test is the wrong model, so p is about 45 times too large (MEDIUM-HIGH, CONFIRMED)

**Lines 2536-2554** (`fc_PreDraft`) and the H₀ text at line 1654. The 183 low numbers are 183 draws
*without replacement* from 366 dates, so the Jan-Jun count is hypergeometric(366, 182, 183), not
binomial(183, 182/366). The finite-population factor is (366-183)/365 = 0.50, so the multinomial χ²
understates the evidence by half:

| test | statistic | p |
|---|---|---|
| FitCheck GOF (multinomial, N = 183) | χ² = 7.082, df 1 | 0.0078 |
| 2×2 table, low/high × Jan-Jun/Jul-Dec (Pearson) | χ² = 14.164, df 1 | 0.000168 |
| Fisher exact (= two-sided hypergeometric) | | 0.000243 |

The verdict (reject) is the same, but the p on screen is wrong for the design, and it teaches the
multinomial model where it does not apply.

**Fix.** Either (a) present the halves as the 2×2 table, the χ² test of independence (14.16, p = 0.00017;
ChiTable already does this), or (b) keep the GOF picture but say on the Test page: "Draws without
replacement: the exact (hypergeometric) p is 0.00024; this χ² is conservative by a factor of about 2
in χ²." Option (a) is the honest one. The Fienberg "capsules not mixed" sentence is already flagged
"not checked against the paper", which is fine.

## 3. Lilliefors for n = 3 prints "p > 0.10" when the true p can be about 0.002 (MEDIUM, CONFIRMED)

**Lines 1169-1179** (`fc_LFcalc`), shown at 1968-1969 and 2055-2057. For n = 3, `fcPD` stays at -1, which
every page reads as "p > 0.10" (in green), and the verdict counts it as not rejecting.

**Failure scenario.** D1 = {5, 5, 7} or {1, 1.1, 100} gives D = 0.3848 and "Lilliefors D = 0.3848, p > 0.10".
In 200,000 simulated normal samples of n = 3, P(D ≥ 0.3845) = 0.0018 and the 90th percentile is
0.367, so the statement is false for any D above 0.367. statsmodels refuses n < 4.

**Fix.** For n = 3 set `fcPD := -2` and print "p: not defined for n = 3 (Lilliefors needs n ≥ 4)",
leaving it out of the agreement count. Alternatively, start Lilliefors at n = 5, the lower end of
Dallal & Wilkinson's tabulated range.

## 4. Benford, first two digits: one-digit amounts are read as "d0" (MEDIUM, CONFIRMED)

**Lines 837-850** (`fc_FirstDig`, `fdTwo = 1`). The significand of 5 is 5.0, so 5 → cell 50, 7 → 70, 8 → 80.

**Failure scenario.** D1 = {5, 7, 3, 12, 15, 1.5, 0.3, 99, 250, 8, 8, 8} gives cells 30:2, 50:1, 70:1, 80:3.
Six of the twelve values are whole numbers below 10, and they all land in the "x0" cells. With
count-like data (small whole numbers) the x0 cells inflate, and χ² and the MAD flag a "departure"
that is an artefact. Nigrini's first-two-digits test uses only amounts of 10 or more; I am relying on
memory of his books here, since there is no copy in the library.

**Fix.** In the two-digit route, skip |v| < 10 and count those values like the zeros ("below 10 skipped: k").
State the rule on the Test page and in help.

## 5. A claim about Castaneda that is not in DATASETS.md: footnote 17 (MEDIUM, CONFIRMED against the brief)

**Line 2335** (and NOTES): "In footnote 17 the Court gave a rule of thumb ... two or three standard
deviations ...". DATASETS.md supports only 870 / 339 / 79.1 %, 11 years, Hidalgo County, expected 688.2
and "the Court's ~29 SD". The footnote's number and content are not in it. To my knowledge the
description is accurate (430 U.S. at 496 n.17), but the rule for this fleet is source-on-file.

**Fix.** Either add the footnote, with its page, to DATASETS.md after a check against the opinion, or
cut the sentence to what DATASETS supports. Line 2334 ("about 688 expected, an SD of about 12, about 29 SDs")
is supported.

## 6. Long computations have no Esc and no progress count (MEDIUM, PLAUSIBLE: G1 timing unknown)

**Lines 1188-1221** (`fc_NormSet`) and 1898-1905 (the Q-Q redraw). For n up to 5000, `fc_NormSet` makes
2,500 `NORMALD_ICDF`, 10,000 `LN(NORMALD_CDF)` and 5,000 `NORMALD_CDF` calls plus the SW, AD and LF loops,
behind a static busy box with no Esc. Every arrow press or tap on the Q-Q page redraws all n dots. The
brief (§2, Speed) asks for a progress count and Esc for anything over about 2 s on a G1. Rossi
(n = 432) is probably acceptable. A 5000-value D1 could take a minute or more per load and several
seconds per Q-Q keypress.

**Fix.** Update a count in the busy box every 250 values and poll `GETKEY == 4` there (abandon the
load cleanly). Draw the static Q-Q plot once into a spare GROB and blit it, redrawing only the selected
dot. Or cap n for the plot at, say, 1000 points (thinned) and say so on screen.

## 7. ln Φ relies on the built-in NORMALD_CDF down to about 1E-198 (LOW-MEDIUM, PLAUSIBLE)

**Line 550** (`fc_LnPhi`): `LN(NORMALD_CDF(0,1,z))` for any z > -30. The Castaneda two-category χ²
(z = -29.115, p = 2.32×10⁻¹⁸⁶) and every tiny W or A² tail go through it. Lessons §3 verifies only z = -8
(6.22E-16). If the firmware loses digits or underflows somewhere between -8 and -30, `LN(0)` follows.

**Fix.** Add to the device checklist: `NORMALD_CDF(0,1,-29.115)` should be about 1.161E-186, and
`NORMALD_CDF(0,1,-37.5)` about 4.6E-308. If either fails, move the asymptotic branch up and add terms
(at z = -10, seven terms of the series reach 12 digits).

## 8. Overflow with huge values: kurtosis is ∞/∞ (LOW, PLAUSIBLE)

**Lines 1199-1207** (also 1236-1242). `nsD^4` and `(nsM2/nsN)^2` pass 1E499 once |x - x̄| exceeds
about 1E125, and Σ(x - x̄)² does once it exceeds about 1E249. On the Prime that gives +∞ with no error
(Lessons §3), then ∞/∞ in `fcKur` and comparisons on an undefined value. The harness cannot show it
(doubles overflow earlier: D1 = {1E130, 2E130, 3E130, 5E130} raised Unsupported).

**Fix.** Standardise first: `nsD := (fcX(i) - fcXb) / sc` with sc = max |x - x̄|, accumulate the powers of
that, and rescale. Or refuse |values| > 1E100 with a message.

## 9. Source lines up to 566 characters (LOW, PLAUSIBLE)

Lines 2779 (566), 2772 (474), 2553 (454), 2776 (439), 1710 (422) and 21 others over 200. The longest line in
a fleet program that has run on the emulator or the calculator is 288 (ChiTable 3e; BiNorm3D 279). No
limit is documented, but none has been tested past about 290.

**Fix.** Split each long string over several lines with `+` at the end of a line, keeping every line under
about 250.

## 10. An INPUT label built inline (LOW, PLAUSIBLE)

**Line 2701**: `INPUT({mdP}, "Binomial fit", {"p" + CHAR(8320) + ":"}, ...)`. Lessons §3 confirms a label
from a string *variable* (as line 2718-2719 does), and DNAMixLR uses a parenthesised `{(CHAR(952) + ":")}`.
The bare inline concatenation in a label list has not been run.

**Fix.** Copy line 2718's form: `mdLb := "p" + CHAR(8320) + ":";` then `{mdLb}`.

## 11. Teaching and wording (LOW, CONFIRMED)

- Line 1710: "Triola's question (p. 653): what would one argument be if you were the attorney ..." paraphrases
  the page, which reads "What would be one argument that you might present if you were the attorney for the
  defendant?" (data/nelson_small.png). Quote it exactly or say "(paraphrased)". The teaching points that
  follow are labelled "teaching points, not the trial record", as required.
- Line 1633: "χ² is short of the critical value: keep H₀". The house wording is "do not reject H₀".
- Line 2837: "χ² goodness of fit → Preset: Castaneda, 2 cells" skips the source page that every other preset shows.
- Line 1704: "Phi(upper edge)" is spelled out on screen. Lines 2701 and 2719 (help text): "H0", "p0" are ASCII.
  Use the glyphs, as §5 asks.

## 12. Style (LOW, CONFIRMED)

- Footers use ";" separators ("page 1 of 3;  ⇅ or tap = page", "cells 1-9 of 9;  ⇅ = page, tap a row = pick it")
  rather than the canonical comma-separated `x = y, ...` form (Lessons §13).
- `fcPEXP := #FFC8A0h` (line 223, the expected-bar fill) is not a house colour; the house light orange is 255,240,220.
- The glyph names are swapped: `fcUp` is ⇅ and `fcDn` is ⇆ (line 242). The screen text is right; the names
  mislead readers.

## 13. List arithmetic (lead's request): NONE FOUND (CONFIRMED)

- A static scan of every list-valued variable (82 names: `fcO`, `fcPr`, `fcMS`, `fcTL`, `amX`, `pdC`, `mdPr` ...)
  for `+ - * / ^` next to the name without an index found no occurrence. So did a grep for an operator next
  to `{` or `}`. Every append is `CONCAT(L, {v})`; every list update is element-wise through an index.
- The builder's `verify_FitCheck_beta1.py` was re-run under the updated `interp.py`, which now refuses `+` with
  a list operand: **3810 checks, 0 failures**. All my own harness runs also passed under it.

---

## What I checked and found correct

**Data, against the files in data/:**
- Nelson's 23 amounts are identical to DATASETS.md, and in the same row order as the Triola p. 653 image.
- "Accused of issuing cheques to a vendor that did not really exist" is on that page (nelson_small.png).
- The draft lottery's 12 monthly lists are identical to vcdExtra_Draft1970.csv and to draft1970_triola.json:
  low counts 12, 12, 10, 11, 14, 14, 14, 19, 17, 13, 21, 26, so Jan-Jun 73 and Jul-Dec 110.
- crimtab: 22 height bins summed over finger length equal the CSV (total 3000).
- Rossi: the age frequencies rebuild the CSV exactly (432, ages 17-44).
- Castaneda: 870, 339, 0.791 (E 688.17, SD 11.993, z -29.115).

**Statistics, against my own references:**
- Nelson. 9 cells: χ² = 129.952, p = 2.89e-24. Triola merge: 63.663, p = 1.50e-14. MAD = 0.16848.
- Castaneda. binomtest two-sided p = 4.1806e-145, shown as "4.18 × 10^-145". There is no underflow:
  everything is in logs, and EXP(-332) is inside the Prime's range. Two-category χ² = 847.68, p = 2.32e-186.
- Richmond: λ̂ = 0.3178, χ² = 1.5176, df 2, p = 0.46822 (scipy chisquare, ddof = 1, with a ≥ tail cell).
- Horse kicks: χ² = 1.9790, df 3, p = 0.57678.
- Illustrative binomial: χ² = 1.2060, p = 0.75158.
- Draft (as built): χ² = 7.0822, p = 0.007785.
- Rossi. Against scipy shapiro, anderson and stats.skew/kurtosis, and statsmodels normal_ad,
  lilliefors and pval_lf: W = 0.849916, p = 7.0914e-20; A² = 20.9405; D = 0.182430, p = 1.6595e-39;
  g₁ = 1.3882, g₂ = 1.3439.
- Awkward D1 samples, W, A², A²'s p, D and its p all match:
  - n = 3: {1, 2, 4} and {5, 5, 7} with ties;
  - n = 4 extreme;
  - 1E9 + small;
  - 60 rounded values with ties;
  - constant data, refused with a message.
- Counts:
  - a category with 0 observed, equal shares: χ² = 38.64, p = 2.07e-8;
  - D2 shares {1, 2, 1, 4}: normalised, χ² = 55.28;
  - Poisson with zero cells {10, 0, 5, 0, 2}: merged correctly by the documented rule, df = k - 2 after merging.
- Exact test against binomtest, all matching. Cases: 7/20 at 0.5 (0.26318), 13/20, 0/1 at 0.3,
  49700/100000 at 0.5 (0.058197), 3/1000 at 0.001, 999/1000 at 0.999. x > n is refused.
  For the symmetric case at large n, the "minlike" tie comparison stays exact in the Prime's
  decimal arithmetic: the two log-pmfs are sums of the same terms on aligned quanta.
- df rules: Benford and shares k-1; Poisson and estimated binomial k-2; typed p₀ k-1; normal on bins k-3,
  with the Chernoff-Lehmann note. All use the cell count *after* merging.
- Merge rule: adjacent cells only, smallest E first, stops at df = 1. Cochran's rule is checked on every cell.

**Device rules:**
- No `LOCAL` line over 6 names.
- No identifier matches a built-in, case-insensitively (797 names, `fcoeff` included).
- No comment inside a bracket (gate E12).
- `CHOOSE` index is initialised and tested; the 11-item list form is used.
- MSGBOX texts are single sentences.
- `STRING(ROUND(x,d),2,d)` everywhere through `fc_F`.
- No `_ICDF` at 0 or 1: only Blom positions, and `CHISQUARE_ICDF(df, 0.95)` with an integer df.
- No fractional df reaches a CDF.
- Upper tails are computed as lower tails or by the continued fraction.
- `EXP` is guarded below -1100.
- Touch: `SIZE` is checked before reading x and y; finger-lift drains are capped by `TICKS`; soft keys at
  y ≥ 218 with `MIN(6, IP(x/53.4)+1)`.
- Nested list literals and `IFTE` with string results are already in fleet programs
  (BayesTree, DNAMixLR, ErrorRate, FDAES).
- Pure ASCII, LF only.

**Style:**
- The header matches the brief: copyright, licence, DISCLAIMER, AI credit, sources, data, the TI programs
  reworked, and a file map whose line ranges are correct.
- The DISCLAIMER is on the title page and in help.
- The `fc_` tag is used throughout. `RETURN` ends the program with a summary line.
