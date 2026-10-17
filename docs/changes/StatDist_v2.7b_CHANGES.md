# StatDist v2.7b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on v2.7a; every v2.7a feature is kept, and the CAS call form (`st_Cas`) is byte-identical. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

StatDist v2.6 and GfxProbe beta 1 ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) on 17 October 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`). v2.7a computes the CDFs the same way.

- **Advanced Continuous → ChiSquare, df = 2.5: FAIL.** "The program stops with 'Error: Invalid input'."
- **GfxProbe T11 and the Home checks:**

  | Expression | Emulator | SciPy |
  |---|---|---|
  | CHISQUARE_CDF(3, 3) | 0.608374823729 | 0.6083748 |
  | CHISQUARE_CDF(2.5, 3) | **Invalid input** | 0.69415 |
  | CHISQUARE_ICDF(2.5, 0.5) | **Invalid input** | |
  | CHISQUARE(2.5, 1), the density | 0.281348225763 | 0.2813482258 |
  | FISHER_CDF(2.5, 7.5, 2) | **Invalid input** | 0.80043 |
  | FISHER_ICDF(2.5, 7.5, 0.5) | **Invalid input** | |
  | STUDENT_CDF / _ICDF / STUDENT at df 2.5 | all = SciPy | |
  | POISSON_CDF(2, −1), (2, −0.5) | **Invalid input** | 0 |

  The chi-square and F **CDF and ICDF** take whole-number df only; the densities and all of Student's t take any df.
- **Cosmetic.** "The INPUT label 'Degrees of freedom:' is cut to 'Degrees of fr…'."

## What changed (line numbers: v2.7a → v2.7b)

1. **Chi-square CDF with a fractional df** (st_cdf, v2.7a 1122–1125 → v2.7b 1167–1175). A whole df uses `CHISQUARE_CDF`, as before. Any other df uses the program's own regularized incomplete gamma, already there for the Gamma family: a chi-square with df degrees of freedom is a Gamma(df/2, scale 2), so F(x) = `st_gammaP(df/2, x/2)`.
2. **F CDF with a fractional df** (st_cdf, 1126–1129 → 1176–1184). The program already has a regularized incomplete beta (`st_betaI`, for the Beta family), so no df is refused. If both df are whole, `FISHER_CDF` is used. Otherwise F(x) = I_z(d1/2, d2/2) with z = d1·x / (d1·x + d2). If X is F(d1, d2), d1X/(d1X + d2) is Beta(d1/2, d2/2).
3. **F density with a fractional df** (st_pdf, 996–1000 → 1036–1045). Whole df keep `FISHER`. Otherwise the density is computed by the formula through `st_lngamma`:

   f(x) = d1^(d1/2) d2^(d2/2) x^(d1/2−1) / (B(d1/2, d2/2) (d1x + d2)^((d1+d2)/2))

   FISHER's density with a fractional df was not among the emulator's checks, so it is not relied on. The chi-square density stays `CHISQUARE`, which took df 2.5 on the emulator.
4. **The quantiles** needed no code change. The chi-square ICDF already used `CHISQUARE_ICDF` only for a whole df (v2.7b 1342); otherwise its bisection calls `st_cdf`, which now takes the incomplete gamma. The F quantile always bisected `st_cdf`. Comments say so.
5. **Every other call was checked:**
   - Erlang's `CHISQUARE_CDF(2k, …)` gets a whole 2k: `st_ask_erlang` rounds k down with `st_Int`, and the comment now says so.
   - Maxwell's `CHISQUARE_ICDF(3, …)` gets a whole 3.
   - Gamma and Beta already used the program's own routines.
   - `POISSON_CDF` is never asked for k < 0: v2.5's guard `IF dX < 0 THEN RETURN 0`, and T12 confirms the built-in would refuse.

   No other `CHISQUARE_CDF`, `FISHER_CDF`, `CHISQUARE_ICDF`, `FISHER_ICDF` or `POISSON_CDF` call exists in the file.
6. **Shorter INPUT labels.** Every label over 14 characters, plus one 14-character label of wide letters:

   | Form | Was | Now | Help line |
   |---|---|---|---|
   | Student t (1769, 1774) | Degrees of freedom: | df: | df > 0 |
   | Chi-square (1791, 1796) | Degrees of freedom: | df: | df > 0 (need not be whole) |
   | Fisher F (1814, 1819) | Numerator df:, Denominator df: | df1:, df2: | Numerator df > 0, Denominator df > 0 |
   | Cauchy (2041, 2046) | Scale (gamma): | Scale: | unchanged |
   | Hypergeometric (2236, 2242) | N (population):, K (positives in N):, k (positives drawn): | N (pop.):, K (pos. in N):, k (pos. in n): | Population size, 1 to 1000; Positives in N, 0 to N; Drawn, 1 to N; Positives drawn, 0 <= k <= n |

7. **Header.** A "WHAT CHANGED in v2.7b" paragraph, the status line, and the help page title "Statistical Distributions v2.7b" (2299).

Nothing else changed. The routines that differ from v2.7a are exactly `st_ask_cauchy`, `st_ask_chisquare`, `st_ask_fisher`, `st_ask_hypergeom`, `st_ask_student`, `st_cdf`, `st_pdf` and `st_show_help`; outside them only comments differ.

## Verification

`verify_StatDist_v2.7b.py` (built from the v2.7a script; harness **ppl_run_v3c**, whose CHISQUARE_CDF, CHISQUARE_ICDF, FISHER_CDF and FISHER_ICDF raise "Invalid input" for a fractional df, and POISSON_CDF for k < 0, as the emulator did). Output in `verify_StatDist_v2.7b_output.txt`: **RESULT: ALL PASS.**

- **Parts 1–4, kept:**
  - the Formula page with `cas='giac'` (197 CAS answers shown and correct, 16 rejected, 0 wrong; 98 of 98 exact comparisons agree);
  - `cas='fail'` for all 27 families;
  - the touch and key paths;
  - the infinity probe.

  The help-title check now looks for v2.7b.
- **5a, end to end (Advanced Continuous):**
  - **v2.7a in v3c: ChiSquare df 2.5 stops with "Invalid input"**, the emulator's finding, and so does F(2.5, 7.5);
  - v2.7b: ChiSquare df 2.5 gives P(X ≤ 5) = 0.876911 and P(X > 5) = 0.123089 (SciPy), with the plot drawn;
  - v2.7b: F(2.5, 7.5) gives P(X ≤ 2) = 0.800427 (SciPy; the emulator table says 0.80043);
  - v2.7b: F(4, 2.5) Between at its default bounds equals SciPy;
  - a whole df (4) still uses CHISQUARE_CDF and gives the emulator's 0.712703.
- **5b, a grid against SciPy:**

  | Quantity | Cases | Worst error |
  |---|---|---|
  | chi-square CDF | 7 fractional df × 8 x | 3.1E-12 |
  | chi-square density | the same | exact |
  | chi-square quantile, \|error\|/(1 + x) | | 1.0E-10 |
  | F CDF | 7 df pairs (one or both fractional) × 7 x | 1.1E-11 |
  | F density, relative | | 2.1E-11 |
  | F quantile | | 3.9E-11 |

- **5c, what the built-ins are handed:**
  - none of the 56 statistics calls passed a fractional df to CHISQUARE_CDF/_ICDF, FISHER_CDF/_ICDF or FISHER;
  - no unmeasured-density warning;
  - the plot (fit, cache, all three tails) runs for 5 fractional-df cases;
  - Erlang(3, 1.5) equals SciPy through CHISQUARE_CDF(6, …);
  - Poisson Between 0 and 5 equals SciPy with no negative k.
- **5d, labels:** none of the 133 INPUT labels is longer than 14 characters; the chi-square form reads "df:", "X value:" and the F form "df1:", "df2:".
- **5e:** the routine diff is as listed; `st_Cas` is byte-identical.

## Gate

`python3 ppl_gate_v1a.py StatDist_v2.7b.txt StatDist_v2.7a.txt` gives **RESULT: PASS**.
- ppl_check_v3: clean.
- lint_ppl: the same 26 problems as v2.7a.
- fleet_names_v2: 0 collisions, 0 untagged.

With the unpacked hp-prime-kit, the kit lint gives 0 errors.

## Device checklist (emulator first, then G2 and G1)

1. Advanced Continuous → ChiSquare → Lower tail, df **2.5**, x 5. There should be no error: P(X ≤ 5) = 0.876911 and the shaded plot. Then Upper tail: 0.123089.
2. Fisher F, df1 2.5, df2 7.5, x 2: P(X ≤ 2) = 0.800427.
3. ChiSquare with df 4, x 5: 0.712703, the same as the emulator's v2.6 result. Whole df still use the built-ins.
4. Look at the forms: "df:", "df1:", "df2:", "Scale:", "N (pop.):", "K (pos. in N):", "k (pos. in n):" should all show in full.
5. On the G1, time the plot of ChiSquare df 2.5 against df 4. The fractional df computes the incomplete gamma in PPL for every pixel column of the cache, which is slower. The Gamma family already does this.

## Not changed (borderline, listed for the device check)

These INPUT labels are 13–14 characters. They are shorter than the clipped one, but some letters are wide, so a few may still be cut:
- "Location (x0):" and "Location (m):" (Cauchy, Fréchet)
- "Scale (theta):" (Gamma)
- "k (successes):" and "r (successes):" (Binomial, negative binomial)
- "μ (log-mean):" (lognormal)

If any shows "…", shorten it the same way.
