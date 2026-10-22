# TrendTest beta 3f: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 22 October 2026. Built on beta 3e; every page, every line of text and every Home export is unchanged. Two assignments changed and one routine was added. Passed the gate; run in the PC harness (ppl_run_v3e); not yet on the emulator or a calculator.*

## Why

The independent review of 22 October 2026 (`docs/dev/independent-review-2026-10-22.md`) noted, as a nit, that the Pearson and departure-from-linearity p-values were still computed as `1 - CHISQUARE_CDF(df, x)`. On the Prime's 12-digit reals that difference is exactly 0 once the tail is below about 5E-13, a chi-square above about 55 at 2 df, so an extreme table prints `p = 0` where the true value is, say, 3E-52. Beta 3d had already moved the trend p to a form that keeps its digits (2 P(Z < -√X²), 1 df); these two were left on the old form because they have k - 1 and k - 2 df, where that trick does not apply.

## What changed (line numbers: beta 3e → beta 3f)

1. **New routine `trUpper(upDF, upX)`** (→ 835-857, before `trCompute`): P(χ²(df) > x) as a finite sum of positive terms, so nothing cancels. Even df, m = df/2: e^(-h) (1 + h + h²/2! + … + h^(m-1)/(m-1)!), h = x/2. Odd df, m = (df-1)/2: 2 P(Z < -√x) + √(2x/π) e^(-h) (1 + x/3 + x²/15 + …), m terms. These are the textbook closed forms of the chi-square survival function. x ≤ 0 returns 1; the sum is capped at 1. `^0.5` is the house square root; π is written as 3.14159265359, the Prime's 12 digits, so the code stays ASCII (ppl_check_v4's E5).
2. **trCompute** (857 → 900, 862 → 906): `trPP := trUpper(trK - 1, trX2P)` and `trPD := trUpper(trDFD, trX2D)` replace the two `1 - CHISQUARE_CDF` lines. The trend p (`trPT`) is as in beta 3d.
3. **The header** (4, 32-49): version and this note.
4. **Nothing else.** No text on screen, no page, key or tap, no Home export; `trPStr` prints the new values the same way it printed the old.

## Verification

`verify/verify_TrendTest_beta3f.py`, output beside it; it runs from `verify/` as is and reads beta 3e from git history when the file is absent.

- **A.** `trUpper` against SciPy's `chi2.sf` at df 1 to 12 and x from 0.5 to 400: worst relative error 5.4E-14.
- **B.** `trCompute` on six 2 × k tables. Three ordinary tables: beta 3e and 3f give the same p to every digit. Three extreme tables (Pearson χ² 237 at 2 df, 369 at 3 df, 435 at 5 df): beta 3f gives 2.9E-52, 1.4E-79 and 1.0E-91, matching SciPy; beta 3e gives 0 (the harness's `1 - CDF` loses the tail just as the Prime does).
- **C.** On every table the trend χ² and p, the Pearson and departure χ², the slope, the Wilson limits and the odds ratios are identical in 3e and 3f.
- 0 failures.

## Gate

`ppl_gate_v1c.py TrendTest_beta3f.txt TrendTest_beta3e.txt`: PASS. hp-prime-kit lint 0 errors; ppl_check_v4 clean, original clean; lint_ppl the same 14 problems as beta 3e; fleet names 19 files, 1133 routine names (trUpper is new), 0 collisions, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. **An ordinary table** (the snoring example): Pearson and departure p unchanged from beta 3e, to every printed digit.
2. **An extreme table**: levels 0, 1, 2 with cases 5, 95, 5 of 100 each. Pearson χ² = 237.36 at 2 df; the p should print as `p < 0.000001` (or the program's smallest form), not `p = 0`. Home's `TR_X2` is 237.363; the p is not exported, so check it on the page.
3. **Odd df**: four levels, cases 2, 98, 2, 98 of 100 each: departure 3 df, χ² = 295.1; again a tiny p, not 0.
4. **Zero chi-square**: three levels with cases 10, 10, 10 of 20: Pearson χ² = 0, p = 1.0000 on both versions.
5. **Speed**: the sums are at most df/2 terms; no visible change.

## Unresolved

- The HSD-style question of whether `trPStr` should print anything below 1E-6 differently is not touched; it prints what it printed.
