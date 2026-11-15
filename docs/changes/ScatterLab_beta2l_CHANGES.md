# ScatterLab beta 2l: changes (15 November 2026)

Round 15. Built from beta 2k by exact replacements (`verify/round15/make_scatterlab_2l.py`; a replacement that does not match exactly once stops the build).

## Why

Roger, 15 November 2026, asked whether Stan Brown's statistics programs for the TI-83/84 (MATH200A and MATH200B, brownmath.com) do anything useful that ours do not. Their descriptions on that site were compared with what our programs do, and two things that MATH200B has were missing here: a confidence interval for a correlation, and a standard error beside the skewness and the kurtosis. Roger: "1 and 2 would be great". This is 1; FitCheck beta 1h is 2. Only the descriptions of those programs were read. No line of their code was read, and the interval below is written from the formula.

## What changed

| What | Where (line numbers in `ScatterLab_beta2l.txt`) |
| --- | --- |
| **A 95% confidence interval for ρ, the population's correlation, on the page Menu > Inference for the slope.** The page's last line now reads, for the example, "95% interval for ρ: 0.407 to 0.909 (Fisher's z)". | `slInf` (941; the arithmetic at 969 to 977); `slInfPage` (2245; the line at 2296 to 2306) |
| **The line above it shows r**: "r = 0.751.  The test of ρ = 0 gives the same t and p." (It was the second sentence alone.) | 2294, 2295 |
| **When there is no interval, the page says why**: "An interval for ρ needs at least 4 points." or "r is 1 or -1 to 12 digits, so ρ has no interval." | 2301 to 2305 |
| **Help page 1 of 7 has one line more**, above the footer: "Menu > Inference: a 95% interval for the population's r (ρ)." | 2335 |
| The page's last three lines sit at y 175, 188 and 204; they were two, at y 181 and 194. | 2293 to 2306 |
| Three new variables, `slRok`, `slRlo`, `slRhi`. No new Home variable, no new menu item. | 370, 378 |

The arithmetic (Fisher's z-transformation): z = ½ ln((1 + r)/(1 − r)) is close to normal with standard error 1/√(n − 3) when the pairs are a random sample from a bivariate normal population, so the limits z ∓ 1.95996398454/√(n − 3) are carried back to r by (e^(2z) − 1)/(e^(2z) + 1). It is worked out once in `slInf`, at the end of every fit, only when the slope has a test, n is at least 4 and |r| is below 1; otherwise `slRok` stays 0 and nothing is divided by zero and no logarithm of zero is taken. The limits are shown to three decimals, like r.

For the example (16 points, r = 0.751) the limits are 0.4071 and 0.9086. The interval is not symmetric about r: it reaches farther toward 0 than toward 1, which is what the transformation is for.

## Checks

- `verify/verify_ScatterLab_beta2l.py`: **42 checks, 0 failed** (output beside it). They are beta 2k's 34 and eight more. The interval equals SciPy's `pearsonr(...).confidence_interval(0.95)` to 9 digits on the example, on Anscombe's four sets and on 300 random sets of 4 to 40 points, with lo ≤ r ≤ hi inside −1 to 1 every time (A8 to A10); with r from 0.9 up to 1 − 10⁻⁹ the limits still equal SciPy's and stay at or below 1 (A11). The edges: three points give the slope its test and ρ the sentence about 4 points (E6); r equal to 1 in the machine's digits with points off the line gives the other sentence (E7). The page: its three last lines where the table above says (E8), no line past 296 px at the calculator's glyph widths with values near 1E8 and 1E−8 (P1 to P3). Against beta 2k: a tour that never opens the Inference page or the help draws the same 41 screens text for text and returns the same summary (R1); on the Inference page one line is reworded and one is new, and every other line is the same (R2); help pages 2 to 7 are word for word beta 2k's and page 1 has one line more (H2). No firm overlap, no text off the screen, no number cut short on any screen (D1, D2).
- Gate (`tools/ppl_gate_v1e.py` against beta 2k; `verify/round15/gates/ScatterLab_beta2l.txt`): **PASS**. hp-prime-kit lint 0 errors; `ppl_check_v5` no hard error, the same three warnings as beta 2k; `lint_ppl` 10 reports, the same ten as beta 2k; no name collision in the fleet.
- Harness smoke test: no error, 0 warnings. `tools/text_overlap_v1.py --walk`: the same report as beta 2k.
- Help layout at the calculator's glyph widths (`verify/round15/helpcheck_r15.json`): 7 screens, no reports.
- Monkey test: **1,000 of 1,000 runs OK** (`verify/round15/mk/ScatterLab.jsonl`; base 15, `--lists --writes C`).
- **HP Prime Virtual Calculator 2.4.2 (build 2026-09-09): Check "No errors in the program"; then, in a later session, a run** (`verify/round15/vc_checks.txt`, `verify/round15/screens/`). The Inference page for the example reads "r = 0.751.  The test of ρ = 0 gives the same t and p." and "95% interval for ρ: 0.407 to 0.909 (Fisher's z)"; for Anscombe's set 1 it reads r = 0.816 and "0.424 to 0.951". Help page 1/7 shows its new line. Every line is inside its page, and ρ draws.

## On a G1 or a G2 (not yet run)

1. Data > Poverty vs crime, then Menu > Inference for the slope. The last three lines before the footer should read "s is the typical miss of a point from the line.", "r = 0.751.  The test of ρ = 0 gives the same t and p." and "95% interval for ρ: 0.407 to 0.909 (Fisher's z)", each inside the frame, the footer clear below them.
2. Data > Anscombe's quartet, set 1, the same page: r = 0.816 and "0.424 to 0.951".
3. Clear the points and add three that are not in a line. The page should end "An interval for ρ needs at least 4 points."
4. Help, page 1/7: the new blue line above the footer.

## Unresolved

- Nothing has run on a G1 or a G2.
- The interval is at 95% only, like the slope's interval and the bands.
- The page does not say what Fisher's interval assumes (a random sample of pairs from a bivariate normal population); there was no room for another line. The book says it.
- Beta 2k's open item stands: a held Enter on the plot, tried with a finger (`ScatterLab_beta2k_CHANGES.md`, item 6).
- `docs/scatterlab-guide.md` has a paragraph for the interval and is otherwise as it was.
