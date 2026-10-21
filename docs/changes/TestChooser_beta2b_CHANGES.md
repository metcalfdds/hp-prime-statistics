# TestChooser beta 2b — changes

*20 October 2026. Built on beta 2a. Text on screen only.*

## What changed

**Symbols instead of spelled-out names** (Roger, 20 Oct 2026: "use the symbols we developed"). In the text the student sees, spelled-out symbols now use the house glyphs: χ² (`CHAR(967)` `CHAR(178)`, device-verified on the G2 and G1 since ChiTable, 10 Oct 2026), ² (`CHAR(178)`), √ (`CHAR(8730)`), and HP's private-use x̄ (`CHAR(57344)`) and p̂ (`CHAR(57345)`). All of these render on the 2026-09-09 firmware (GfxProbe T14 and the fleet's earlier pages).

Untouched: every string the CAS receives (it must stay ASCII), Home variable names (`CS_X2`, `TR_X2`, `EP_chisq`), comments, numbers, positions and logic. Each replacement is shorter than or as long as the text it replaces, so no line can newly overflow. (The second pass, below, adds the rest.)

Version strings swept (rule 13): the banner.

| Line (old) | Before | After |
| --- | --- | --- |
| 241 | `IF fnI == 6 THEN RETURN "Chi-square 2x2, or Fisher's exact"; END;` | `IF fnI == 6 THEN RETURN "χ² 2x2, or Fisher's exact"; END;` |
| 242 | `IF fnI == 7 THEN RETURN "Chi-square for an r x c table"; END;` | `IF fnI == 7 THEN RETURN "χ² for an r x c table"; END;` |
| 245 | `IF fnI == 10 THEN RETURN "Relative risk, odds ratio, chi-square"; END;` | `IF fnI == 10 THEN RETURN "Relative risk, odds ratio, χ²"; END;` |
| 257 | `IF fnI == 22 THEN RETURN "One-proportion z / chi-square GOF"; END;` | `IF fnI == 22 THEN RETURN "One-proportion z / χ² GOF"; END;` |
| 272 | `IF clI == 6 THEN RETURN {"chi-sq./", "Fisher"}; END;` | `IF clI == 6 THEN RETURN {"χ²/", "Fisher"}; END;` |
| 273 | `IF clI == 7 THEN RETURN {"chi-sq.", "r x c"}; END;` | `IF clI == 7 THEN RETURN {"χ²", "r x c"}; END;` |
| 276 | `IF clI == 10 THEN RETURN {"RR, OR,", "chi-sq."}; END;` | `IF clI == 10 THEN RETURN {"RR, OR,", "χ²"}; END;` |
| 329 | `"Inference > X2 test > 2-way (matrix).",` | `"Inference > χ² test > 2-way (matrix).",` |
| 335 | `"Inference > X2 test > 2-way (matrix).",` | `"Inference > χ² test > 2-way (matrix).",` |
| 336 | `"Ordered groups?  TrendTest (X2 for trend).",` | `"Ordered groups?  TrendTest (χ² for trend).",` |
| 342 | `"By hand, 1 df: X2 = (\|b-c\| - 1)^2/(b+c).",` | `"By hand, 1 df: χ² = (\|b-c\| - 1)²/(b+c).",` |
| 346 | `"Extends McNemar; chi-square, k - 1 df.",` | `"Extends McNemar; χ², k - 1 df.",` |
| 353 | `"Fleet: EpiStats > Risk; Inference X2.",` | `"Fleet: EpiStats > Risk; Inference χ².",` |
| 364 | `"Rank one-way ANOVA; chi-square, k - 1 df.",` | `"Rank one-way ANOVA; χ², k - 1 df.",` |
| 394 | `"Chi-square, k - 1 df; prop. hazards.",` | `"χ², k - 1 df; prop. hazards.",` |
| 425 | `"Inference > Z-Test: 1 pi; X2 > Goodness.",` | `"Inference > Z-Test: 1 pi; χ² > Goodness.",` |
| 427 | `"Report p-hat with its CI (Z-Int: 1 pi)."}; END;` | `"Report " + CHAR(57345) + " with its CI (Z-Int: 1 pi)."}; END;` |
| 1698 | `TEXTOUT_P("     chi-square, odds ratios.", G1, 12, 78, 1, tcORNG);` | `TEXTOUT_P("     χ², odds ratios.", G1, 12, 78, 1, tcORNG);` |

## Second pass, same day: all 20 programs checked

Roger: "9 apps? check 20 please." The first pass looked only for χ², ², √, x̄ and p̂. The second looked for every symbol the fleet has a glyph for — ≥ ≤, ±, ×, →, ∞, the Greek letters, the subscripts — in all 20 programs. This file had not yet been loaded on a calculator or put in the repository, so it is revised under the same version rather than given a new one. All of these render on the 2026-09-09 firmware (GfxProbe T14 on the Virtual Calculator: ≥ ≤ ≠, θ ρ λ, √ ∞, the arrows and subscripts; ± and φ are already on screen in EpiStats; × and μ σ α in most of the fleet).

Kept as words: the "+/-" that names the + and − keys, "Gamma" and "Beta" as names of distributions and functions, powers other than ² (`^k`, `^3`), and anything the CAS receives.

| Line (first-pass beta 2b) | Before | After |
| --- | --- | --- |
| 266 | `IF fnI == 21 THEN RETURN "One-sample t test (z if sigma known)"; END;` | `IF fnI == 21 THEN RETURN "One-sample t test (z if σ known)"; END;` |
| 291 | `IF clI == 15 THEN RETURN {"Spearman", "rho"}; END;` | `IF clI == 15 THEN RETURN {"Spearman", "ρ"}; END;` |
| 322 | `"Hyp. test > T-Test: 1 mu, with mu0 = 0.",` | `"Hyp. test > T-Test: 1 μ, with μ₀ = 0.",` |
| 335 | `"Curved or ordinal?  Spearman's rho."}; END;` | `"Curved or ordinal?  Spearman's ρ."}; END;` |
| 338 | `"Expected counts >= 5; else Fisher's exact.",` | `"Expected counts ≥ 5; else Fisher's exact.",` |
| 344 | `"Expected < 5 in <= 20% of cells; none < 1.",` | `"Expected < 5 in ≤ 20% of cells; none < 1.",` |
| 395 | `"Many ties?  Kendall's tau instead."}; END;` | `"Many ties?  Kendall's τ instead."}; END;` |
| 429 | `"Inference > Hyp. test > T-Test: 1 mu.",` | `"Inference > Hyp. test > T-Test: 1 μ.",` |
| 430 | `"Also the T-Int: 1 mu confidence interval.",` | `"Also the T-Int: 1 μ confidence interval.",` |
| 434 | `"n pi0 and n(1-pi0) >= 10; GOF: exp. >= 5.",` | `"n π₀ and n(1-π₀) ≥ 10; GOF: exp. ≥ 5.",` |
| 435 | `"Inference > Z-Test: 1 pi; χ² > Goodness.",` | `"Inference > Z-Test: 1 π; χ² > Goodness.",` |
| 437 | `"Report " + CHAR(57345) + " with its CI (Z-Int: 1 pi)."}; END;` | `"Report " + CHAR(57345) + " with its CI (Z-Int: 1 π)."}; END;` |
| 461 | `IF ckI == 6 OR ckI == 7 OR ckI == 10 THEN RETURN "Check: expected counts >= 5 in ChiTable."; END;` | `IF ckI == 6 OR ckI == 7 OR ckI == 10 THEN RETURN "Check: expected counts ≥ 5 in ChiTable."; END;` |
| 1706 | `TEXTOUT_P("     normal -> t tests, ANOVA, regression.", G1, 12, 54, 1, tcBLUE);` | `TEXTOUT_P("     normal → t tests, ANOVA, regression.", G1, 12, 54, 1, tcBLUE);` |
| 1707 | `TEXTOUT_P("   Nominal: categories -> proportions,", G1, 12, 66, 1, tcORNG);` | `TEXTOUT_P("   Nominal: categories → proportions,", G1, 12, 66, 1, tcORNG);` |
| 1709 | `TEXTOUT_P("   Ordinal, or skewed, or tiny n -> ranks:", G1, 12, 90, 1, tcMAG);` | `TEXTOUT_P("   Ordinal, or skewed, or tiny n → ranks:", G1, 12, 90, 1, tcMAG);` |

## Checks

- `check_glyph_sweep.py` (the first pass, output beside it): with every string and comment blanked, the code was line-for-line identical to the previous version.
- `check_glyph_sweep2.py` (output beside it): with every `CHAR()` build folded back into its string, every changed line that is not a comment differs from the 19 Oct text only inside its string literals (five listed display lines excepted); no line that builds CAS text changed; no literal used in a comparison or a replace changed. 381 changed code lines in 17 files, 0 failures.
- The gate (`ppl_gate_v1c.py`, new against old, on Rogers-HP): **PASS**; kit lint 0 errors; lint_ppl reports the same number of problems as before (`Glyph_Sweep_2026-10-20_gate.txt`); the full parse stops where it stopped before (the tool's limit), a few lines further down because of the change note.
- The program's own verify script, run unchanged on the new text in the harness (ppl_run_v3e): `verify_TestChooser_beta2a.py`: 238 of 252 checks pass. The 14 that fail look for the old test names ("chi-square", "1 mu") or list the routines and lines that changed.
- Not yet on a calculator.

## Device checklist

1. Load it over the existing program (open it in the Kit and replace the text; never a second copy).
2. Open the test cards (1 μ, μ₀, σ, ρ, τ, π, π₀, ≥, ≤) and the scales help (→), and check that the symbols show as symbols, not boxes, and that no line runs into its neighbour.
3. **New glyphs: π, τ.** These have not been seen on the calculator's screen in a program before. If any shows as a box, tell Claude: the word goes back in, nothing else changes.
