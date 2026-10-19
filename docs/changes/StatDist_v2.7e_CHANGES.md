# StatDist v2.7e: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on v2.7d; every v2.7d feature is kept, and every ordinary display is unchanged. Run only in the PC harness (ppl_run_v3e), not yet on the emulator or a calculator.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`; `findings_B.md`, StatDist) and Roger's decision on it:

- **D9, the right tail: "implement `st_sf` per family (27 formulas listed and checked to 2.7E-11 in findings_B.md; removes the '= 0.000000 vs < 0.000001' inconsistency and the Formula page rejecting correct exact tails)". Roger: the full fix.** v2.7d took every right tail as 1 − F(x) (`st_Prob` 2514, `st_CutCalc` 2536-2538). The Prime keeps 12 significant digits, so far out F(x) is 0.999999999999… and 1 − F(x) is exactly 0 once the tail is below about 5E-13. Two findings followed:
  - **B4:** "a positive right tail is shown as exactly '= 0.000000' where the left tail reads '< 0.000001'". Under the review's 12-digit model this happened in 9 of 20 far-tail cases; on the device, by the reviewer's reasoning, in all 20 (1 − EXP(−30) is exactly 1 in 12-digit BCD).
  - **B3:** "a correct exact upper tail is thrown away for discrete tails below about 1e-6". The Formula page checks the CAS's exact answer against the program's number to 6 significant digits. Binomial(20, 0.1), P(X > 11), read "no closed form shown" under 12 digits.
  - The Negative binomial's **lower** tail (`st_cdf` 1364, also a 1 − …) had the same loss: "CDF: 0.000000" on the Numbers page for NegBin(30, 0.3), P(Y ≤ 0) = 2E-16.
- **B1. WRONG NUMBER (extreme inputs): "`st_gammaP` stops at 500 iterations; wrong for shape ≳ 10,000."** Gamma(20000, 1), P(X ≤ 20000) = 0.500729 where SciPy gives 0.500940. The fix asked for: "refuse k, df > 5000 at the form".
- **B2. WRONG TEXT: "the 'approximation poor' note is wider than the screen"** (2883): 58 characters, about 319 px at font 1.
- **B5. COSMETIC: menu spellings** (4208-4210): "ChiSquare" and "MaxwellBoltzmann" on the Advanced menu, "Chi-square" and "Maxwell-Boltzmann" everywhere else.
- **B7. WRONG TEXT (edge): "a typed x below 0.0001 puts a relation inside the label"**: `P(X <= < 0.0001) = 0.500020` for x = 0.00005, on the panel, the Numbers page and the summary returned to Home.

Roger's addition of 19 October (12:48 CDT): the disclaimer line beside the distribution terms.

## What changed (line numbers: v2.7d → v2.7e)

1. **New `st_sf(dId, dPl, dX)`, the right tail P(X > x) of each family** (→ 1527-1733, after `st_cdf`). Each tail is a LOWER tail of something, or a formula with nothing subtracted from 1 near 1. The 27 formulas are findings_B part I's:
   - **Mirrored about the centre:** Normal `NORMALD_CDF(μ, σ, 2μ − x)`; LogNormal `NORMALD_CDF(0, 1, −(LN x − μ)/σ)`; Laplace `st_lapCDF(2μ − x, μ, b)`; t `STUDENT_CDF(df, −x)`. Cauchy uses `st_atan(1/z)/π` for z > 1.
   - **Closed forms, g(x) itself:** Exponential `e^(−λx)`; Weibull `e^(−(x/λ)^k)`; Burr `(1 + (x/S)^C)^(−K)`; Pareto `(x_m/x)^α`; Rayleigh `e^(−x²/(2σ²))`; Logistic `1/(1 + e^z)`; Gompertz `e^(−η(e^(bx) − 1))`; Geometric `(1 − p)^k`; Uniform `(b − x)/(b − a)`; Triangular the mirror quadratic above the mode, and below it `((c − a)(b − c) + (c − x)(c + x − 2a)) / ((b − a)(c − a))`. That is part I's `1 − (x − a)²/((b − a)(c − a))` rewritten as two non-negative parts, because the subtraction cancels when the mode sits at or next to the maximum, where the tail below the mode can be tiny (prime12: 5.6E-8 relative at a 2E-9 tail, now under 1E-9). Maxwell is `2Φ(−z) + √(2/π) z e^(−z²/2)`. Gumbel and Fréchet are `1 − e^(−u)`, with the series `u − u²/2 + u³/6` for u < 1E-4.
   - **Counts turned round:** Binomial `BINOMIAL_CDF(n, 1 − p, n − k − 1)`; Negative binomial `BINOMIAL_CDF(k + r, p, r − 1)`; Hypergeometric the sum from k + 1 up.
   - **The incomplete gamma and beta, the upper part directly:** chi-square `Q(df/2, x/2)`, Gamma `Q(k, x/θ)`, Erlang `Q(k, λx)`, Poisson `P(k + 1, λ)`, F `I_z(d2/2, d1/2)` with z = d2/(d1 x + d2), Beta `I_(1−x)(β, α)`.
   - **Where the number comes from, differently from part I, at sizes the program's own loops cannot reach** (I decided these; neither form limits λ or the Erlang's k):
     - Poisson with k + 1 > 5000: `CHISQUARE_CDF(2k + 2, 2λ)`, the same P(k + 1, λ), from the built-in with a whole df;
     - Erlang with k > 5000: `POISSON_CDF(λx, k − 1)`, the same Q(k, λx). This is the Poisson-process identity the Erlang's CDF already uses.
     - The F with a df above 10,000 keeps v2.7d's 1 − F(x) (for whole df the built-in FISHER_CDF). `st_betaI`'s log-gamma terms are each about a ln a, and on 12-digit reals their difference loses digits. With all arithmetic rounded to 12 digits (prime12) the tail's relative error is 8E-8 at df 10,000 but 3.5E-6 at df 100,000, which is visible in the sixth decimal; and above df 1E6 the fraction's 300 passes run out (2.7E-3 at df 1E7). The far tail of so large an F is no classroom case, and there it can still read "= 0.000000", as in v2.7d.
2. **New `st_gammaQ(a, x)`, the upper incomplete gamma** (→ 773-814, after `st_gammaP`). It is st_gammaP's continued fraction, line for line, returning Q instead of 1 − Q. For x < a + 1 it is 1 − P, where Q is not small (at least Q(a, a + 1)). `st_gammaP` itself is byte-identical.
3. **New `st_SfAt(v)`** (→ 2867-2879, beside `st_CdfAt`): the right tail from the cache while a finger drags and for a bar on the plot, otherwise from `st_sf`.
4. **New file-level cache `stSv`** (→ 430-433) and **`st_Cache`** (2632-2697 → 3026-3112). It is built beside `stCd`:
   - **bars:** from the right, the exact P(X > last bar) plus the pmf bar by bar, positive numbers only. A `WHILE` counts down, so a one-bar window relies on no empty FOR.
   - **a curve:** `st_sf` where F(x) > 1/2, and 1 − F(x) elsewhere, where it is exact.
   - Its MAKELIST counts with a LOCAL (`caJ`), not Home's K.
5. **`st_Prob`** (2509-2517 → 2892-2910):
   - P(X > x) is `st_SfAt(x)`.
   - A Between that lies in the upper half (F(a) > 1/2) is S(a) − S(b), two small numbers, instead of F(b) − F(a). Normal(0, 1), P(8 < X < 9), read "= 0.000000" while P(−9 < X < −8) read "< 0.000001".
   - The panel, the Numbers page, the summary returned to Home and the Formula page's check all take their probability from here.
6. **`st_CutCalc`** (2533-2540 → 2924-2934): the "% beyond >>" side is `st_sf(stHi)`.
7. **`st_cdf`, the Negative binomial's lower tail** (1360-1365 → 1506-1514): `BINOMIAL_CDF(k + r, 1 − p, k)`, at most k failures in k + r trials, the same number with no subtraction. It is the only line of `st_cdf` that changed.
8. **B1** (`st_ask_chisquare` 1896 → 2254-2260, help lines 1887, 1892 → 2244, 2249; `st_ask_gamma` 2266 → 2631-2635, help lines 2257, 2262 → 2621, 2626). A chi-square df or a Gamma k above 5000 is refused with a box: "Error: df must be <= 5000 here" / "(the incomplete gamma stops after 500 steps)". The help lines read "0 < df <= 5000 (need not be whole)" and "0 < k <= 5000 (any, not just whole)". The program's own incomplete gamma needs about 490 passes at a shape of 5000. Whole df above 5000 were fine in v2.7d (the built-in), but the right tail now uses `st_gammaQ` for every df, so the bound holds for all, as the review asked.
9. **B2** (2883 → 3299-3301): `"approx." + st_Eq(st_fmtp(pnA, 4)) + ": poor here, " + pnX`, giving `approx. = 0.7602: poor here, np or n(1-p) < 10` (46 characters, about 259 px).
10. **B5** (4207-4210 → 4628-4634): "Chi-square", "Maxwell-Boltzmann". The comment above the CHOOSE, not inside its brackets, says why.
11. **B7, new `st_XStr(v, text)`** (→ 585-613, after `st_fmtx`). A text that starts with a relation becomes the value's own digits:
    - the fewest decimals, 5 to 11, that hold it exactly (0.00005 → `0.00005`);
    - otherwise four significant digits.
    - It is ROUNDed before STRING, so it never turns scientific.

    It is used for x, a and b on the panel (2844, 2851, 2860 → 3260, 3267, 3276), on the Numbers page (3230-3233, 3250 → 3649-3652, 3670) and in the Formula page's "at x" line (3719 → 4140). Parameters keep v2.7d's `σ < 0.0001` (`st_ParStr`), which v2.7d chose deliberately.
12. **Header:**
    - the banner (4);
    - the disclaimer after the terms (→ 20-22). StatDist's help pages do not state the terms, so nothing was added on screen.
    - the tested-on lines (29-31 → 32-35);
    - a "WHAT CHANGED in v2.7e" paragraph (→ 37-98);
    - the file map names `st_XStr`, `st_gammaQ` and `st_sf`;
    - the help page's title reads v2.7e (2394 → 2763).

**Before and after** (harness ppl_run_v3e; "12 digits" is the review's `twelve_digits()`; "prime12" adds 12-digit rounding of every arithmetic step and EXP, LN, LOG, SQRT):

| Where (how) | v2.7d | v2.7e |
|---|---|---|
| Normal(0, 1), P(X > 7.5), panel and summary (12 digits) | `P(X > 7.5) = 0.000000` | `P(X > 7.5) < 0.000001` |
| Far right tails, review's 20 cases (12 digits / prime12) | "= 0.000000" in 9 / 16 of 20 | in none |
| Binomial(40, 0.5), P(X > 39) | `= 0.000000` | `< 0.000001` |
| Formula page, Binomial(20, 0.1), P(X > 11) and 4 more upper tails (12 digits, CAS answering) | "no closed form shown" in 2 of 5 | the exact answer in all 5, badge "exact (CAS)" |
| NegBin(30, 0.3), Numbers page, P(Y ≤ 0) | `CDF: 0.000000` | `CDF: < 0.000001` |
| Normal(0, 1), P(8 < X < 9) (12 digits) | `= 0.000000` | `< 0.000001` |
| Gamma, k = 20000, x = 20000 | accepted, `P(X <= 20000) = 0.500729` (SciPy 0.500940) | refused with the box |
| Binomial(18, 0.5), Approx | `approx. 0.7602: approximation poor here, np or n(1-p) < 10` | `approx. = 0.7602: poor here, np or n(1-p) < 10` |
| Advanced menu | `ChiSquare`, `MaxwellBoltzmann` | `Chi-square`, `Maxwell-Boltzmann` |
| Normal(0, 1), x = 0.00005 | `P(X <= < 0.0001) = 0.500020`; Numbers `At x < 0.0001:` | `P(X <= 0.00005) = 0.500020`; `At x = 0.00005:` |
| Every family × tail × setting (243 states), doubles | — | identical to v2.7d but for the far right tails |

## Verification

`verify_StatDist_v2.7e.py` was built from the v2.7d script, and every check is kept. It runs on v2.7e in harness ppl_run_v3e.

What changed in the old parts, and why:
- **part 3:** the help title it looks for is v2.7e's (the version sweep);
- **part 5:** the forms are reached through the menu item "Chi-square" (B5), while v2.7a is still reached as "ChiSquare";
- **part 6f:** `st_XStr`'s two rounded STRING calls join the safe list (18 calls, not 16);
- **part 7:** it stays v2.7d's change set, comparing v2.7d (not the newest file) with v2.7c, as part 6g keeps comparing v2.7c with v2.7b.

Output: `verify_StatDist_v2.7e_output.txt`: **196 [ok], 0 [FAIL]**. Parts 1-7 give 134, every check of the v2.7d script, and part 8 gives 62. The script was run as two processes side by side, parts 1-7 and part 8, because the machine was shared; `python3 verify_StatDist_v2.7e.py` with no arguments runs everything in one.

Part 8 is new:
- **8a. `st_sf`, all 27 families, on findings_B's grid** (the review's PARS and xgrid, plus the 1E-7 and 1E-10 right tails), against SciPy's sf:
  - **Under `twelve_digits()`, the worst relative error against SciPy's sf is 1.1E-9.** That is the Triangular (2, 5, 12) at its 1E-7 tail, where SciPy's own sf is 1 − cdf.
  - Against the best reference (exact fractions for the Uniform and the Triangular) the worst is **7.5E-11**: Poisson(40) at k = 63, the Lanczos log-gamma inside `st_gammaP`. Every other family is at or below 2.7E-11.
  - The same in doubles.
  - Under prime12 (every arithmetic step also rounded to 12 digits) the worst is 8.1E-9 (the F).
  - **8a1:** the Triangular with its mode at or next to the maximum, x within 1E-9 of the mode, under prime12: 1.9E-12.
  - `st_sf` = 1 − `st_cdf` wherever the tail is between 0.01 and 0.99 (714 points, 2.3E-11).
- **8b2.** Under prime12 at the largest sizes the program trusts its own incomplete gamma and beta with (F df 10,000, Gamma k, chi-square df and Erlang k 5,000, Poisson 4,000, Beta 5,000): within 1.2E-7. This measurement set the F's 10,000.
- **8b.** The road changes: Poisson λ 2,000 to 100,000, Erlang k 5,000 to 20,000, Gamma k and chi-square df at 5,000, F up to df 1E9. All within 1E-6 relative at the 0.1 % to 1 − 1E-9 points, with the built-ins used exactly where stated. No CHISQUARE_CDF has a fractional df.
- **8c.** `st_gammaQ` against gammaincc, a from 0.001 to 5,000: worst relative error 1.9E-10. P + Q = 1.
- **8d. The review's `check_StatDist.py`:**
  - its one failing check (part H, B2) fails on v2.7d and passes on v2.7e;
  - its parts A, B, E (with B5's menu labels), F, G and I pass on v2.7e;
  - its parts C and D, which pass when the bug is there, are run on both versions with the expectation turned round (the table's rows), plus C(ii): 8 of 12 tails between 1E-6 and 1E-11 off by more than 1E-6 in v2.7d, none in v2.7e (worst 1.8E-11).
- **8e-8h.** B1 (refused at 5001, 5000.5 and 20000.5; accepted at 5000 and 4999.5 = SciPy), B2, B5 (end to end by the new labels), B7 (st_XStr's cases, the panel, the Numbers page, the Formula page, the parameters).
- **8i.** Betweens below and above the middle = SciPy (2.2E-12).
- **8j.** The cache: every bar (one-bar windows included) and every 17th column = `st_sf`, and the drag readout = the lifted one.
- **8k.** All 27 families × 3 tails × defaults, far left and far right, panel and Numbers page, in doubles and under 12 digits, against v2.7d. They are identical except a right tail (or upper Between) that read "= 0.000000" or moved by its last digit.
- **8l.** The routine diff. Changed: `st_cdf` (only the Negative binomial line), `st_Prob`, `st_CutCalc`, `st_Cache`, `st_Panel`, `st_Numbers`, `st_FmCont`, `st_ask_chisquare`, `st_ask_gamma`, `st_advanced_continuous`, `st_show_help`. Added: `st_gammaQ`, `st_sf`, `st_SfAt`, `st_XStr`. Outside them only comments and `LOCAL stSv;` differ. `st_gammaP`, `st_betaI`, `st_pdf`, `st_icdf`, `st_Mom` and the formatters are byte-identical.
- **8m.** The static rules:
  - the version strings and status line;
  - no `//` inside an open bracket;
  - at most 6 names per LOCAL;
  - no new name matches a built-in;
  - the new MAKELIST's LOCAL counter;
  - `st_sf` subtracts from 1 only where nothing near 1 is lost (listed);
  - INSTRING unchanged.
- **8n.** No scientific STRING result in the 208 part-8 runs of v2.7e (the review's runs included), with one justified exception: the review's case of a Cauchy with a typed x of 1E13. `st_fmtx`, byte-identical to v2.7d, prints that x with 0 decimals, which the Prime writes in scientific form from 1E12 on, and v2.7d does the same. Parts 1-6's own check (6h) finds none in their runs of v2.7e. (Its label still says "v2.7c", the old wording.)

## Gate

`python3 ppl_gate_v1b.py StatDist_v2.7e.txt _old/StatDist_v2.7d.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: clean, as v2.7d. No hard errors (E12 included).
- lint_ppl: 26 problems, as v2.7d (the tool's STRING-argument miscount, review item 21).
- Full parse: it stops at the first file-level LOCAL (399), as v2.7d does at the same line (331). This is the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`bash check.sh StatDist_v2.7e.txt StatDist_v2.7d.txt`: the same.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v2.7d (open it in the Kit), then Program Catalog → Check.
2. In Home, the review's two lines that settle the 12-digit argument: `1 - NORMALD_CDF(0,1,7.5)` (expect 0) and `NORMALD_CDF(0,1,-7.5)` (expect 3.19E-14). Also `CHISQUARE_CDF(42,10)` (expect 8.10925045989E-8, which is Poisson(5)'s P(X > 20)), which tells whether the built-ins keep a small lower tail's digits.
3. **D9:**
   - Common Continuous → Normal, Upper tail, μ 0, σ 1, x 7.5: the panel reads `P(X > 7.5) < 0.000001`. Esc → Exit: Home shows the same.
   - Exponential λ 1, Upper tail, x 30: `< 0.000001` (v2.7d: `= 0.000000` on the device, by the review's reasoning).
   - Discrete → Binomial, Upper tail, n 40, p 0.5, k 39: `P(X > 39) = P(X >= 40) < 0.000001`.
4. **B3:** Binomial, Upper tail, n 20, p 0.1, k 11 → More, More, Formula. The sum line shows the exact fraction `= 2907458992391/50000000000000000000` with "exact (CAS)", not "no closed form shown".
5. **Between:** Normal(0, 1), Between 8 and 9: `P(8 < X < 9) < 0.000001`.
6. **NegBin lower tail:** Negative Binomial, Lower tail, r 30, p 0.3, k 0 → Enter → Numbers page: `CDF: < 0.000001`.
7. **B1:**
   - Advanced → Gamma, k 20000: a box "Error: k must be <= 5000 here", and back to the menu;
   - k 5000, θ 1, x 5000 plots `P(X <= 5000) = 0.501881`;
   - Chi-square df 5001 is refused.
8. **B2:** Binomial n 18, p 0.5, k 10 → More → Approx: the red note reads `approx. = 0.7602: poor here, np or n(1-p) < 10`, whole.
9. **B5:** the Advanced menu shows `Chi-square` and `Maxwell-Boltzmann`.
10. **B7:** Normal, Lower tail, x 0.00005: `P(X <= 0.00005) = 0.500020`. Enter → Numbers page: `At x = 0.00005:`.
11. **Speed (G1):** pan the plot with the arrows on Gamma(2.5, 2) and on the chi-square: each cache rebuild now evaluates the right tail at about half the columns. Drags read from the cache, as before.

## Unresolved

- **B6** (the density at a support end: Exponential λ vs Erlang 0) is findings_B's decision D3, not in this pass.
- The reviewer's improvements (exports `ST_P`…, drawing the sd, `STUDENT_ICDF` for the t window, the Hypergeometric's Formula-page size guard, keeping x on a bounded support) are review section 4, not in this pass.
- Device: whether NORMALD_CDF, BINOMIAL_CDF, CHISQUARE_CDF and POISSON_CDF keep a small lower tail's digits on the Prime (checklist item 2). If they compute a lower tail as 1 − upper, the change is harmless but does not help for those families.
