# StatDist v2.7f — changes

*20 October 2026. Built on v2.7e. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed"). In the text the student sees, spelled-out symbols now use the house glyphs: χ² (`CHAR(967)` `CHAR(178)`, device-verified on the G2 and G1 since ChiTable, 10 Oct 2026), ² (`CHAR(178)`), √ (`CHAR(8730)`), and HP's private-use x̄ (`CHAR(57344)`) and p̂ (`CHAR(57345)`). All of these render on the 2026-09-09 firmware (GfxProbe T14 and the fleet's earlier pages).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names (`CS_X2`, `TR_X2`, `EP_chisq`), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow. (The second pass, below, adds the rest.)

Version strings swept (rule 13): the banner and every on-screen title or About line that names the version.

| Line (old) | Before | After |
| --- | --- | --- |
| 1140 | `"Laplace", "Student t", "Chi-square", "Fisher F", "Burr XII",` | `"Laplace", "Student t", "χ²", "Fisher F", "Burr XII",` |
| 2242 | `okI := INPUT({df}, "Chi-square: goodness of fit",` | `okI := INPUT({df}, "χ²: goodness of fit",` |
| 2247 | `okI := INPUT({df, x_val}, "Chi-square: goodness of fit",` | `okI := INPUT({df, x_val}, "χ²: goodness of fit",` |
| 2763 | `st_Page("Statistical Distributions v2.7e", {` | `st_Page("Statistical Distributions v2.7f", {` |
| 2783 | `"  CAS works out E[X], E[X^2], Var",` | `"  CAS works out E[X], E[X²], Var",` |
| 3769 | `IF ffI == 1 THEN RETURN "f(x) = e^(-(x-μ)^2/(2σ^2)) / (σ sqrt(2 pi))"; END;` | `IF ffI == 1 THEN RETURN "f(x) = e^(-(x-μ)²/(2σ²)) / (σ √(2 pi))"; END;` |
| 3773 | `IF ffI == 5 THEN RETURN "f(x) = e^(-(ln x - μ)^2/(2σ^2)) / (x σ sqrt(2 pi))"; END;` | `IF ffI == 5 THEN RETURN "f(x) = e^(-(ln x - μ)²/(2σ²)) / (x σ √(2 pi))"; END;` |
| 3775 | `IF ffI == 7 THEN RETURN "f(x) = Gamma((df+1)/2) / (sqrt(df pi) Gamma(df/2)) (1 + x^2/df)^(-(df+1)/2)"; END;` | `IF ffI == 7 THEN RETURN "f(x) = Gamma((df+1)/2) / (√(df pi) Gamma(df/2)) (1 + x²/df)^(-(df+1)/2)"; END;` |
| 3777 | `IF ffI == 9 THEN RETURN "f(x) = sqrt((d1 x)^d1 d2^d2 / (d1 x + d2)^(d1+d2)) / (x B(d1/2, d2/2))"; END;` | `IF ffI == 9 THEN RETURN "f(x) = √((d1 x)^d1 d2^d2 / (d1 x + d2)^(d1+d2)) / (x B(d1/2, d2/2))"; END;` |
| 3781 | `IF ffI == 13 THEN RETURN "f(x) = (x/σ^2) e^(-x^2/(2σ^2)), x >= 0"; END;` | `IF ffI == 13 THEN RETURN "f(x) = (x/σ²) e^(-x²/(2σ²)), x >= 0"; END;` |
| 3782 | `IF ffI == 14 THEN RETURN "f(x) = e^(-z) / (s (1 + e^(-z))^2), z = (x - μ)/s"; END;` | `IF ffI == 14 THEN RETURN "f(x) = e^(-z) / (s (1 + e^(-z))²), z = (x - μ)/s"; END;` |
| 3790 | `IF ffI == 22 THEN RETURN "f(x) = sqrt(2/pi) x^2 e^(-x^2/(2a^2)) / a^3"; END;` | `IF ffI == 22 THEN RETURN "f(x) = √(2/pi) x² e^(-x²/(2a²)) / a^3"; END;` |
| 4106 | `st_FmAdd("E[X^2] = integral of x^2 f(x) dx, same limits:", #000000h);` | `st_FmAdd("E[X²] = integral of x² f(x) dx, same limits:", #000000h);` |
| 4125 | `st_FmAdd("Var(X) = E[X^2] - E[X]^2:", #000000h);` | `st_FmAdd("Var(X) = E[X²] - E[X]²:", #000000h);` |
| 4479 | `gdLb := {"Normal(0, 1)", "Exponential(1)", "Chi-square(4)",` | `gdLb := {"Normal(0, 1)", "Exponential(1)", "χ²(4)",` |
| 4632 | `{"Student t", "Chi-square", "Fisher F", "Gamma", "Beta",` | `{"Student t", "χ²", "Fisher F", "Gamma", "Beta",` |

## Second pass, same day: all 20 programs checked

Roger: "9 apps? check 20 please." The first pass looked only for χ², ², √, x̄ and p̂. The second looked for every symbol the fleet has a glyph for — ≥ ≤, ±, ×, →, ∞, the Greek letters, the subscripts — in all 20 programs. This file had not yet been loaded on a calculator or put in the repository, so it is revised under the same version rather than given a new one. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Kept as words: the "+/-" that names the + and − keys, "Gamma" and "Beta" as names of distributions and functions, powers other than ² (`^k`, `^3`), and anything the CAS receives.

**Three code lines:** `st_FmShow` now turns the CAS's "+infinity" and "infinity" into ∞ (it dropped the + before), and `st_FmLimS` returns −∞ and ∞ instead of the words. Both only build text for the formula page.

| Line (first-pass v2.7f) | Before | After |
| --- | --- | --- |
| 1855 | `IF pr1 > 1 THEN mM := 0; ELSE mM := "undef (df<=1)"; END;` | `IF pr1 > 1 THEN mM := 0; ELSE mM := "undef (df≤1)"; END;` |
| 1856 | `IF pr1 > 2 THEN mV := pr1/(pr1 - 2); ELSE mV := "undef (df<=2)"; END;` | `IF pr1 > 2 THEN mV := pr1/(pr1 - 2); ELSE mV := "undef (df≤2)"; END;` |
| 1860 | `IF pr2 > 2 THEN mM := pr2/(pr2 - 2); ELSE mM := "undef (df2<=2)"; END;` | `IF pr2 > 2 THEN mM := pr2/(pr2 - 2); ELSE mM := "undef (df2≤2)"; END;` |
| 1864 | `mV := "undef (df2<=4)";` | `mV := "undef (df2≤4)";` |
| 1873 | `mM := "undef (K*C<=1)";` | `mM := "undef (K×C≤1)";` |
| 1879 | `mV := "undef (K*C<=2)";` | `mV := "undef (K×C≤2)";` |
| 1885 | `IF pr2 > 1 THEN mM := pr2*pr1/(pr2 - 1); ELSE mM := "undef (α<=1)"; END;` | `IF pr2 > 1 THEN mM := pr2*pr1/(pr2 - 1); ELSE mM := "undef (α≤1)"; END;` |
| 1886 | `IF pr2 > 2 THEN mV := pr1^2*pr2/((pr2 - 1)^2*(pr2 - 2)); ELSE mV := "undef (α<=2)"; END;` | `IF pr2 > 2 THEN mV := pr1^2*pr2/((pr2 - 1)^2*(pr2 - 2)); ELSE mV := "undef (α≤2)"; END;` |
| 1903 | `IF pr1 > 1 THEN mM := pr3 + pr2*EXP(st_lngamma(1 - 1/pr1)); ELSE mM := "undef (α<=1)"; END;` | `IF pr1 > 1 THEN mM := pr3 + pr2*EXP(st_lngamma(1 - 1/pr1)); ELSE mM := "undef (α≤1)"; END;` |
| 1907 | `mV := "undef (α<=2)";` | `mV := "undef (α≤2)";` |
| 1951 | `IF dId == 19 THEN RETURN "x0" + psA + ", scale" + psB; END;` | `IF dId == 19 THEN RETURN "x₀" + psA + ", scale" + psB; END;` |
| 1953 | `IF dId == 21 THEN RETURN "eta" + psA + ", b" + psB; END;` | `IF dId == 21 THEN RETURN "η" + psA + ", b" + psB; END;` |
| 1956 | `IF dId == 24 THEN RETURN "k" + psA + ", theta" + psB; END;` | `IF dId == 24 THEN RETURN "k" + psA + ", θ" + psB; END;` |
| 2004 | `IF dId == 3 THEN RETURN {"Lower >= 0 (default = 0)", "Upper > a (default = μ = 1/λ)"}; END;` | `IF dId == 3 THEN RETURN {"Lower ≥ 0 (default = 0)", "Upper > a (default = μ = 1/λ)"}; END;` |
| 2005 | `IF dId == 4 OR dId == 13 THEN RETURN {"Lower >= 0 (default = 0)", "Upper > a (default = μ)"}; END;` | `IF dId == 4 OR dId == 13 THEN RETURN {"Lower ≥ 0 (default = 0)", "Upper > a (default = μ)"}; END;` |
| 2009 | `IF dId == 8 THEN RETURN {"Lower >= 0 (default = df/2)", "Upper > a (default = 2 df)"}; END;` | `IF dId == 8 THEN RETURN {"Lower ≥ 0 (default = df/2)", "Upper > a (default = 2 df)"}; END;` |
| 2010 | `IF dId == 9 THEN RETURN {"Lower >= 0 (default = 0.5)", "Upper > a (default = 2)"}; END;` | `IF dId == 9 THEN RETURN {"Lower ≥ 0 (default = 0.5)", "Upper > a (default = 2)"}; END;` |
| 2013 | `IF dId == 12 THEN RETURN {"Lower >= x_m (default = x_m)", "Upper > a (default = 2 x_m)"}; END;` | `IF dId == 12 THEN RETURN {"Lower ≥ x_m (default = x_m)", "Upper > a (default = 2 x_m)"}; END;` |
| 2016 | `IF dId == 16 THEN RETURN {"Lower int >= 0 (default = λ - 2σ)", "Upper int (default = λ + 2σ)"}; END;` | `IF dId == 16 THEN RETURN {"Lower int ≥ 0 (default = λ - 2σ)", "Upper int (default = λ + 2σ)"}; END;` |
| 2017 | `IF dId == 17 THEN RETURN {"Lower int >= 1 (default = 1)", "Upper int (default = μ + 2σ)"}; END;` | `IF dId == 17 THEN RETURN {"Lower int ≥ 1 (default = 1)", "Upper int (default = μ + 2σ)"}; END;` |
| 2019 | `IF dId == 19 THEN RETURN {"Lower (default = x0 - scale)", "Upper (default = x0 + scale)"}; END;` | `IF dId == 19 THEN RETURN {"Lower (default = x₀ - scale)", "Upper (default = x₀ + scale)"}; END;` |
| 2020 | `IF dId == 20 THEN RETURN {"Lower >= m (default = m)", "Upper > a (default = m + 2s)"}; END;` | `IF dId == 20 THEN RETURN {"Lower ≥ m (default = m)", "Upper > a (default = m + 2s)"}; END;` |
| 2021 | `IF dId == 21 THEN RETURN {"Lower >= 0 (default = mean - sd)", "Upper (default = mean + sd)"}; END;` | `IF dId == 21 THEN RETURN {"Lower ≥ 0 (default = mean - sd)", "Upper (default = mean + sd)"}; END;` |
| 2022 | `IF dId == 22 OR dId == 23 OR dId == 24 THEN RETURN {"Lower >= 0 (default = 0)", "Upper > a (default = mean)"}; END;` | `IF dId == 22 OR dId == 23 OR dId == 24 THEN RETURN {"Lower ≥ 0 (default = 0)", "Upper > a (default = mean)"}; END;` |
| 2023 | `IF dId == 25 THEN RETURN {"Lower >= 0 (default = mean - sd)", "Upper <= 1 (default = mean + sd)"}; END;` | `IF dId == 25 THEN RETURN {"Lower ≥ 0 (default = mean - sd)", "Upper ≤ 1 (default = mean + sd)"}; END;` |
| 2024 | `IF dId == 26 THEN RETURN {"Lower int >= 0 (default = 0)", "Upper int (default = mean)"}; END;` | `IF dId == 26 THEN RETURN {"Lower int ≥ 0 (default = 0)", "Upper int (default = mean)"}; END;` |
| 2054 | `"Lower tail: P(X <= a)", "Upper tail: P(X > a)",` | `"Lower tail: P(X ≤ a)", "Upper tail: P(X > a)",` |
| 2151 | `{"Rate > 0", "Value >= 0"}, {1, 0});` | `{"Rate > 0", "Value ≥ 0"}, {1, 0});` |
| 2153 | `IF x_val < 0 THEN MSGBOX("Error: x must be >= 0"); RETURN 0; END;` | `IF x_val < 0 THEN MSGBOX("Error: x must be ≥ 0"); RETURN 0; END;` |
| 2174 | `{"k > 0", "λ > 0", "x >= 0"}, {2, 1, 1});` | `{"k > 0", "λ > 0", "x ≥ 0"}, {2, 1, 1});` |
| 2176 | `IF x_val < 0 THEN MSGBOX("Error: x must be >= 0"); RETURN 0; END;` | `IF x_val < 0 THEN MSGBOX("Error: x must be ≥ 0"); RETURN 0; END;` |
| 2254 | `{"0 < df <= 5000 (need not be whole)"}, {10});` | `{"0 < df ≤ 5000 (need not be whole)"}, {10});` |
| 2259 | `{"0 < df <= 5000 (need not be whole)", "Value >= 0"}, {10, 5});` | `{"0 < df ≤ 5000 (need not be whole)", "Value ≥ 0"}, {10, 5});` |
| 2261 | `IF x_val < 0 THEN MSGBOX("Error: x must be >= 0"); RETURN 0; END;` | `IF x_val < 0 THEN MSGBOX("Error: x must be ≥ 0"); RETURN 0; END;` |
| 2270 | `IF df > 5000 THEN MSGBOX("Error: df must be <= 5000 here" + CHAR(10) + "(the incomplete gamma stops after 500 steps)"); RETURN 0; END;` | `IF df > 5000 THEN MSGBOX("Error: df must be ≤ 5000 here" + CHAR(10) + "(the incomplete gamma stops after 500 steps)"); RETURN 0; END;` |
| 2289 | `{"Numerator df > 0", "Denominator df > 0", "Value >= 0"}, {10, 15, 1});` | `{"Numerator df > 0", "Denominator df > 0", "Value ≥ 0"}, {10, 15, 1});` |
| 2291 | `IF x_val < 0 THEN MSGBOX("Error: x must be >= 0"); RETURN 0; END;` | `IF x_val < 0 THEN MSGBOX("Error: x must be ≥ 0"); RETURN 0; END;` |
| 2356 | `{"x_m > 0", "α > 0", "x >= x_m"}, {1, 3, 2});` | `{"x_m > 0", "α > 0", "x ≥ x_m"}, {1, 3, 2});` |
| 2361 | `IF aTl <> 3 AND x_val < xm THEN MSGBOX("Error: x must be >= x_m"); RETURN 0; END;` | `IF aTl <> 3 AND x_val < xm THEN MSGBOX("Error: x must be ≥ x_m"); RETURN 0; END;` |
| 2376 | `{"Scale σ:", "X value:"}, {"σ > 0", "x >= 0"}, {1.5, 2});` | `{"Scale σ:", "X value:"}, {"σ > 0", "x ≥ 0"}, {1.5, 2});` |
| 2378 | `IF x_val < 0 THEN MSGBOX("Error: x must be >= 0"); RETURN 0; END;` | `IF x_val < 0 THEN MSGBOX("Error: x must be ≥ 0"); RETURN 0; END;` |
| 2424 | `IF stN < 1 THEN MSGBOX("Error: n must be >= 1"); RETURN 0; END;` | `IF stN < 1 THEN MSGBOX("Error: n must be ≥ 1"); RETURN 0; END;` |
| 2426 | `IF aTl <> 3 AND (k_val < 0 OR k_val > stN) THEN MSGBOX("Error: 0 <= k <= n"); RETURN 0; END;` | `IF aTl <> 3 AND (k_val < 0 OR k_val > stN) THEN MSGBOX("Error: 0 ≤ k ≤ n"); RETURN 0; END;` |
| 2446 | `IF k_val < 0 THEN MSGBOX("Error: k must be >= 0"); RETURN 0; END;` | `IF k_val < 0 THEN MSGBOX("Error: k must be ≥ 0"); RETURN 0; END;` |
| 2466 | `{"0 < p < 1", "Trial of 1st success (>=1)"}, {0.3, 3});` | `{"0 < p < 1", "Trial of 1st success (≥1)"}, {0.3, 3});` |
| 2469 | `IF k_val < 1 THEN MSGBOX("Error: k must be >= 1"); RETURN 0; END;` | `IF k_val < 1 THEN MSGBOX("Error: k must be ≥ 1"); RETURN 0; END;` |
| 2496 | `MSGBOX("Error: need min <= mode <= max, min < max"); RETURN 0;` | `MSGBOX("Error: need min ≤ mode ≤ max, min < max"); RETURN 0;` |
| 2510 | `{"Location (x0):", "Scale:"},` | `{"Location (x₀):", "Scale:"},` |
| 2515 | `{"Location (x0):", "Scale:", "X value:"},` | `{"Location (x₀):", "Scale:", "X value:"},` |
| 2558 | `{"Shape (eta):", "Rate (b):"},` | `{"Shape (η):", "Rate (b):"},` |
| 2559 | `{"eta > 0 (smaller = longer lives)", "b > 0 (doubling time ln2/b)"},` | `{"η > 0 (smaller = longer lives)", "b > 0 (doubling time ln2/b)"},` |
| 2564 | `{"Shape (eta):", "Rate (b):", "X value:"},` | `{"Shape (η):", "Rate (b):", "X value:"},` |
| 2565 | `{"eta > 0 (smaller = longer lives)", "b > 0 (doubling time ln2/b)", "x >= 0"},` | `{"η > 0 (smaller = longer lives)", "b > 0 (doubling time ln2/b)", "x ≥ 0"},` |
| 2568 | `IF x_val < 0 THEN MSGBOX("Error: x must be >= 0"); RETURN 0; END;` | `IF x_val < 0 THEN MSGBOX("Error: x must be ≥ 0"); RETURN 0; END;` |
| 2570 | `IF gmEt <= 0 THEN MSGBOX("Error: eta must be > 0"); RETURN 0; END;` | `IF gmEt <= 0 THEN MSGBOX("Error: η must be > 0"); RETURN 0; END;` |
| 2588 | `{"Scale (a):", "X value:"}, {"a > 0 (the sd of each axis)", "x >= 0"},` | `{"Scale (a):", "X value:"}, {"a > 0 (the sd of each axis)", "x ≥ 0"},` |
| 2591 | `IF x_val < 0 THEN MSGBOX("Error: x must be >= 0"); RETURN 0; END;` | `IF x_val < 0 THEN MSGBOX("Error: x must be ≥ 0"); RETURN 0; END;` |
| 2606 | `{"Whole number >= 1", "λ > 0"}, {3, 1});` | `{"Whole number ≥ 1", "λ > 0"}, {3, 1});` |
| 2611 | `{"Whole number >= 1", "λ > 0", "x >= 0"}, {3, 1, 2});` | `{"Whole number ≥ 1", "λ > 0", "x ≥ 0"}, {3, 1, 2});` |
| 2613 | `IF x_val < 0 THEN MSGBOX("Error: x must be >= 0"); RETURN 0; END;` | `IF x_val < 0 THEN MSGBOX("Error: x must be ≥ 0"); RETURN 0; END;` |
| 2616 | `IF erK < 1 THEN MSGBOX("Error: k must be >= 1"); RETURN 0; END;` | `IF erK < 1 THEN MSGBOX("Error: k must be ≥ 1"); RETURN 0; END;` |
| 2630 | `{"Shape (k):", "Scale (theta):"},` | `{"Shape (k):", "Scale (θ):"},` |
| 2631 | `{"0 < k <= 5000 (any, not just whole)", "theta > 0"}, {2.5, 2});` | `{"0 < k ≤ 5000 (any, not just whole)", "θ > 0"}, {2.5, 2});` |
| 2635 | `{"Shape (k):", "Scale (theta):", "X value:"},` | `{"Shape (k):", "Scale (θ):", "X value:"},` |
| 2636 | `{"0 < k <= 5000 (any, not just whole)", "theta > 0", "x >= 0"}, {2.5, 2, 4});` | `{"0 < k ≤ 5000 (any, not just whole)", "θ > 0", "x ≥ 0"}, {2.5, 2, 4});` |
| 2638 | `IF x_val < 0 THEN MSGBOX("Error: x must be >= 0"); RETURN 0; END;` | `IF x_val < 0 THEN MSGBOX("Error: x must be ≥ 0"); RETURN 0; END;` |
| 2645 | `IF gaK > 5000 THEN MSGBOX("Error: k must be <= 5000 here" + CHAR(10) + "(the incomplete gamma stops after 500 steps)"); RETURN 0; END;` | `IF gaK > 5000 THEN MSGBOX("Error: k must be ≤ 5000 here" + CHAR(10) + "(the incomplete gamma stops after 500 steps)"); RETURN 0; END;` |
| 2646 | `IF gaT <= 0 THEN MSGBOX("Error: theta must be > 0"); RETURN 0; END;` | `IF gaT <= 0 THEN MSGBOX("Error: θ must be > 0"); RETURN 0; END;` |
| 2664 | `{"α > 0", "β > 0", "0 <= x <= 1"}, {2, 5, 0.3});` | `{"α > 0", "β > 0", "0 ≤ x ≤ 1"}, {2, 5, 0.3});` |
| 2666 | `IF x_val < 0 OR x_val > 1 THEN MSGBOX("Error: 0 <= x <= 1"); RETURN 0; END;` | `IF x_val < 0 OR x_val > 1 THEN MSGBOX("Error: 0 ≤ x ≤ 1"); RETURN 0; END;` |
| 2681 | `{"Whole number >= 1", "0 < p < 1"}, {3, 0.4});` | `{"Whole number ≥ 1", "0 < p < 1"}, {3, 0.4});` |
| 2686 | `{"Whole number >= 1", "0 < p < 1", "Failures before the r-th success"},` | `{"Whole number ≥ 1", "0 < p < 1", "Failures before the r-th success"},` |
| 2690 | `IF k_val < 0 THEN MSGBOX("Error: k must be >= 0"); RETURN 0; END;` | `IF k_val < 0 THEN MSGBOX("Error: k must be ≥ 0"); RETURN 0; END;` |
| 2693 | `IF nbR < 1 THEN MSGBOX("Error: r must be >= 1"); RETURN 0; END;` | `IF nbR < 1 THEN MSGBOX("Error: r must be ≥ 1"); RETURN 0; END;` |
| 2717 | `{"Population size, 1 to 1000", "Positives in N, 0 to N", "Drawn, 1 to N", "Positives drawn, 0 <= k <= n"},` | `{"Population size, 1 to 1000", "Positives in N, 0 to N", "Drawn, 1 to N", "Positives drawn, 0 ≤ k ≤ n"},` |
| 2724 | `IF hgK < 0 OR hgK > hgN THEN MSGBOX("Error: 0 <= K <= N"); RETURN 0; END;` | `IF hgK < 0 OR hgK > hgN THEN MSGBOX("Error: 0 ≤ K ≤ N"); RETURN 0; END;` |
| 2725 | `IF hgM < 1 OR hgM > hgN THEN MSGBOX("Error: 1 <= n <= N"); RETURN 0; END;` | `IF hgM < 1 OR hgM > hgN THEN MSGBOX("Error: 1 ≤ n ≤ N"); RETURN 0; END;` |
| 2726 | `IF aTl <> 3 AND (k_val < 0 OR k_val > hgM) THEN MSGBOX("Error: 0 <= k <= n"); RETURN 0; END;` | `IF aTl <> 3 AND (k_val < 0 OR k_val > hgM) THEN MSGBOX("Error: 0 ≤ k ≤ n"); RETURN 0; END;` |
| 2782 | `"P<=x, P>x = which tail is shaded.",` | `"P≤x, P>x = which tail is shaded.",` |
| 3270 | `IF stTl == 1 THEN pnS := "P(X <= " + st_XStr(stXv, st_fmtx(stXv)) + ")" + st_Eq(st_fmtp(pnP, 6)); END;` | `IF stTl == 1 THEN pnS := "P(X ≤ " + st_XStr(stXv, st_fmtx(stXv)) + ")" + st_Eq(st_fmtp(pnP, 6)); END;` |
| 3274 | `pnS := "P(X > " + st_fmtx(stXv) + ") = P(X >= " + st_fmtx(stXv + 1) + ")" + st_Eq(st_fmtp(pnP, 6));` | `pnS := "P(X > " + st_fmtx(stXv) + ") = P(X ≥ " + st_fmtx(stXv + 1) + ")" + st_Eq(st_fmtp(pnP, 6));` |
| 3283 | `pnS := "P(" + st_fmtx(stAv) + " <= X <= " + st_fmtx(stBv) + ")" + st_Eq(st_fmtp(pnP, 6));` | `pnS := "P(" + st_fmtx(stAv) + " ≤ X ≤ " + st_fmtx(stBv) + ")" + st_Eq(st_fmtp(pnP, 6));` |
| 3418 | `DRAWMENU({"P<=k", "P>k", "a<X<b", "Zoom−", "Zoom+", "More"});` | `DRAWMENU({"P≤k", "P>k", "a<X<b", "Zoom−", "Zoom+", "More"});` |
| 3420 | `DRAWMENU({"P<=x", "P>x", "a<X<b", "Zoom−", "Zoom+", "More"});` | `DRAWMENU({"P≤x", "P>x", "a<X<b", "Zoom−", "Zoom+", "More"});` |
| 3651 | `nuL := CONCAT(nuL, {"CDF(b) = P(X <= " + STRING(stBv, 2, 0) + ")" + st_Eq(st_fmtp(nuFb, 6)),` | `nuL := CONCAT(nuL, {"CDF(b) = P(X ≤ " + STRING(stBv, 2, 0) + ")" + st_Eq(st_fmtp(nuFb, 6)),` |
| 3652 | `"CDF(a-1) = P(X <= " + STRING(stAv - 1, 2, 0) + ")" + st_Eq(st_fmtp(nuFa, 6)),` | `"CDF(a-1) = P(X ≤ " + STRING(stAv - 1, 2, 0) + ")" + st_Eq(st_fmtp(nuFa, 6)),` |
| 3654 | `"P(" + STRING(stAv, 2, 0) + " <= X <= " + STRING(stBv, 2, 0) + ")" + st_Eq(st_fmtp(nuP, 6))});` | `"P(" + STRING(stAv, 2, 0) + " ≤ X ≤ " + STRING(stBv, 2, 0) + ")" + st_Eq(st_fmtp(nuP, 6))});` |
| 3673 | `nuS := "P(X <= " + nuX + ")" + st_Eq(st_fmtp(nuP, 6));` | `nuS := "P(X ≤ " + nuX + ")" + st_Eq(st_fmtp(nuP, 6));` |
| 3676 | `nuS := "P(X > " + nuX + ") = P(X >= " + STRING(stXv + 1, 2, 0) + ")" + st_Eq(st_fmtp(nuP, 6));` | `nuS := "P(X > " + nuX + ") = P(X ≥ " + STRING(stXv + 1, 2, 0) + ")" + st_Eq(st_fmtp(nuP, 6));` |
| 3687 | `nuS := "P(X <= " + nuX + ")" + st_Eq(st_fmtp(nuP, 6));` | `nuS := "P(X ≤ " + nuX + ")" + st_Eq(st_fmtp(nuP, 6));` |
| 3745 | `IF nmI == 19 THEN RETURN {"x0", "scale", ""}; END;` | `IF nmI == 19 THEN RETURN {"x₀", "scale", ""}; END;` |
| 3747 | `IF nmI == 21 THEN RETURN {"eta", "b", ""}; END;` | `IF nmI == 21 THEN RETURN {"η", "b", ""}; END;` |
| 3750 | `IF nmI == 24 THEN RETURN {"k", "theta", ""}; END;` | `IF nmI == 24 THEN RETURN {"k", "θ", ""}; END;` |
| 3779 | `IF ffI == 1 THEN RETURN "f(x) = e^(-(x-μ)²/(2σ²)) / (σ √(2 pi))"; END;` | `IF ffI == 1 THEN RETURN "f(x) = e^(-(x-μ)²/(2σ²)) / (σ √(2 π))"; END;` |
| 3780 | `IF ffI == 2 THEN RETURN "f(x) = 1/(b - a) for a <= x <= b"; END;` | `IF ffI == 2 THEN RETURN "f(x) = 1/(b - a) for a ≤ x ≤ b"; END;` |
| 3781 | `IF ffI == 3 THEN RETURN "f(x) = λ e^(-λx) for x >= 0"; END;` | `IF ffI == 3 THEN RETURN "f(x) = λ e^(-λx) for x ≥ 0"; END;` |
| 3782 | `IF ffI == 4 THEN RETURN "f(x) = (k/λ) (x/λ)^(k-1) e^(-(x/λ)^k), x >= 0"; END;` | `IF ffI == 4 THEN RETURN "f(x) = (k/λ) (x/λ)^(k-1) e^(-(x/λ)^k), x ≥ 0"; END;` |
| 3783 | `IF ffI == 5 THEN RETURN "f(x) = e^(-(ln x - μ)²/(2σ²)) / (x σ √(2 pi))"; END;` | `IF ffI == 5 THEN RETURN "f(x) = e^(-(ln x - μ)²/(2σ²)) / (x σ √(2 π))"; END;` |
| 3785 | `IF ffI == 7 THEN RETURN "f(x) = Gamma((df+1)/2) / (√(df pi) Gamma(df/2)) (1 + x²/df)^(-(df+1)/2)"; END;` | `IF ffI == 7 THEN RETURN "f(x) = Gamma((df+1)/2) / (√(df π) Gamma(df/2)) (1 + x²/df)^(-(df+1)/2)"; END;` |
| 3790 | `IF ffI == 12 THEN RETURN "f(x) = α x_m^α / x^(α+1) for x >= x_m"; END;` | `IF ffI == 12 THEN RETURN "f(x) = α x_m^α / x^(α+1) for x ≥ x_m"; END;` |
| 3791 | `IF ffI == 13 THEN RETURN "f(x) = (x/σ²) e^(-x²/(2σ²)), x >= 0"; END;` | `IF ffI == 13 THEN RETURN "f(x) = (x/σ²) e^(-x²/(2σ²)), x ≥ 0"; END;` |
| 3797 | `IF ffI == 19 THEN RETURN "f(x) = 1 / (pi scale (1 + z^2)), z = (x - x0)/scale"; END;` | `IF ffI == 19 THEN RETURN "f(x) = 1 / (π scale (1 + z²)), z = (x - x₀)/scale"; END;` |
| 3799 | `IF ffI == 21 THEN RETURN "f(x) = b eta e^(eta + b x - eta e^(b x)), x >= 0"; END;` | `IF ffI == 21 THEN RETURN "f(x) = b η e^(η + b x - η e^(b x)), x ≥ 0"; END;` |
| 3800 | `IF ffI == 22 THEN RETURN "f(x) = √(2/pi) x² e^(-x²/(2a²)) / a^3"; END;` | `IF ffI == 22 THEN RETURN "f(x) = √(2/π) x² e^(-x²/(2a²)) / a^3"; END;` |
| 3802 | `IF ffI == 24 THEN RETURN "f(x) = x^(k-1) e^(-x/theta) / (Gamma(k) theta^k)"; END;` | `IF ffI == 24 THEN RETURN "f(x) = x^(k-1) e^(-x/θ) / (Gamma(k) θ^k)"; END;` |
| 4003 | `fwS := st_Repl(fwS, "+infinity", "infinity");` | `fwS := st_Repl(fwS, "+infinity", CHAR(8734));   // 2.7f: shown as ∞` |
| 4004 | `` | `fwS := st_Repl(fwS, "infinity", CHAR(8734));` |
| 4018 | `IF flT == "-inf" THEN RETURN "-infinity"; END;` | `IF flT == "-inf" THEN RETURN CHAR(8722) + CHAR(8734); END;` |
| 4019 | `IF flT == "inf" THEN RETURN "infinity"; END;` | `IF flT == "inf" THEN RETURN CHAR(8734); END;` |
| 4105 | `st_FmAdd("  from the centre up alone: infinity (CAS).", stMAG);` | `st_FmAdd("  from the centre up alone: ∞ (CAS).", stMAG);` |
| 4107 | `st_FmAdd("  = infinity (CAS).", stMAG);` | `st_FmAdd("  = ∞ (CAS).", stMAG);` |
| 4126 | `st_FmAdd("  = infinity (CAS): there is NO variance", stMAG);` | `st_FmAdd("  = ∞ (CAS): there is NO variance", stMAG);` |
| 4186 | `IF stTl == 1 THEN st_FmAdd("P(X <= " + st_IStr(stXv) + ") = the sum of P(X = k),", #000000h); END;` | `IF stTl == 1 THEN st_FmAdd("P(X ≤ " + st_IStr(stXv) + ") = the sum of P(X = k),", #000000h); END;` |
| 4188 | `IF stTl == 3 THEN st_FmAdd("P(" + st_IStr(stAv) + " <= X <= " + st_IStr(stBv) + ") = the sum of P(X = k),", #000000h); END;` | `IF stTl == 3 THEN st_FmAdd("P(" + st_IStr(stAv) + " ≤ X ≤ " + st_IStr(stBv) + ") = the sum of P(X = k),", #000000h); END;` |

## Checks

- `check_glyph_sweep.py` (the first pass, output beside it): with every string and comment blanked, the code was line-for-line identical to the previous version.
- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_StatDist_v2.7e.py`, with its menu item "Chi-square" renamed "χ²" in four places so that it can reach the χ² forms: every check passes but 19. The 19 look for the old text ("P(X <= 5) = 0.876911" where the screen says "P(X ≤ 5) = 0.876911", the soft keys "P<=x", the menu "Chi-square") or list the routines that changed. Every probability equals SciPy's.
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the input boxes and error messages (≥, ≤, θ, η, x₀), the soft keys P≤x / P≤k, the formula page (π, θ, η, z²), the parameter labels and the CAS pages (∞), and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
3. **New glyphs: π, η.** These have not been seen on the calculator's screen in a program before. If any shows as a box, tell Claude: the word goes back in, nothing else changes.
