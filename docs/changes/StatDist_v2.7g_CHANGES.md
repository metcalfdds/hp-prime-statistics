# StatDist v2.7g: changes

*1 November 2026. Edited from v2.7f by a patch script, every replacement checked to apply exactly once. 4,911 lines. Fixes for what random use found (the book's vetting point 6, "bulletproof under careless and random use"), and the `!=` the Virtual Calculator showed to be a factorial.*

## What was found

`tools/monkey_v1b.py` drives the program in the PC harness the way a careless student might: any key, any tap, menu picks and cancels, odd values typed into the forms (`docs/dev/monkey-fleet-2026-11-01.md`). Over 400 runs (150 events each) v2.7f gave:

| Verdict | Runs | Cause |
| --- | --- | --- |
| OK | 344 | |
| HARNESS | 43 | a list typed into a number field went on into the arithmetic (`<=`, `<`, `-`, `FP` of a list) |
| HARNESS | 10 | an overflow from a typed 1E300, 1E−300 or 1.23 × 10¹² (`^`, `EXP`, `ROUND` of a number past the harness's range) |
| FREEZE | 2 | a Poisson with λ = 1E300 never finished |
| GUARD | 1 | `BINOMIAL_CDF` called with n = 1E300 |

The monkey reaches a family only now and then, so every parameter of all 27 families was then swept over the decades from 1E−300 to 1E300, with the rest at their defaults, through the plot, a zoom, the arrows, the Numbers page and the Formula page. Of its 1,794 runs, v2.7f broke in 204, in 26 of the 27 families (only the hypergeometric came through): 180 stopped the harness on a number it cannot hold (an overflow past 1.8E308, or `ROUND` of a number near 1E300; on the Prime some of these may give ∞ without an error, Lessons Learned v7zg), 12 never finished (a binomial n, Poisson λ, negative binomial r or k of 1E49 or 1E300), 11 stopped with a calculator error (a division by zero at a scale of 1E−300; `STRING` asked for 49 or 300 decimals), and 1 asked `FISHER_CDF` for a value it has not got (df1 = 1E300). The outputs, with every broken run, are `verify/sweep_StatDist_v2.7f_output.txt` and `sweep_StatDist_v2.7g_output.txt`.

Two faults the harness cannot show:

- **`!=` is a factorial and a test on the Prime** (`{3!=0, 0!=0, 3<>0, 0<>0}` gave `{0, 0, 1, 0}` on the Virtual Calculator, and `999!=0` "Numerical overflow"). v2.7f had two: `st_fmtp`'s floor (547), "IF pv != 0 AND ABS(pv) < thr", which on the calculator is (pv!) == 0, never true, and "Numerical overflow" for a value of 254 or more; and `st_fmtv`'s "IF TYPE(vv) != 0" (575), never true, so an "undef ..." moment went on into `st_fmtp`.
- STRING's 12-decimal limit (v7zh): a typed σ of 1E−300 asked for 300 decimals.

## What changed (line numbers are v2.7f's)

1. **`<>`, not `!=`** (`st_fmtp` 547, `st_fmtv` 575).
2. **Every form field takes a real number only**: all 56 forms (two per family and the Between bounds) are `{name,[0]}`.
3. **What the plot cannot draw is refused with a sentence, before anything changes** (new section 4b: `st_BigMsg`, `st_LimX`, `st_Rng`, `st_FitWin`, `st_LimP`; `st_AskAB`, which every form ends in, asks them first, 2073):
   - a number of 50 digits or more, a parameter or x or a bound: "A number you typed has more than 50 digits: too large to work with.";
   - a discrete family's k (x, a or b) past 10⁹: "k can be at most 1000000000 here." At k = 10⁴⁹ a zoom centred the window there, and `st_Draw`'s tick counter, n + 1, never moved on (a Poisson, geometric or negative binomial never finished);
   - a shape outside the range where its family's formulas stay finite: Weibull k 0.05–100; LogNormal μ −100 to 100, σ at most 10; F df1, df2 at most 1,000,000; Burr C and K 0.2–100; Pareto α 0.05–100; Fréchet α 0.05–100; binomial n at most 100,000; Poisson λ at most 100,000; geometric p at least 0.000001; negative binomial r at most 1,000, p at least 0.001. Each in one sentence, e.g. "For the Weibull, k must be from 0.05 to 100 here.";
   - a window (the one `st_Fit` fits, now `st_FitWin`) that reaches past 1E50 ("These values spread the distribution past 1E50: too large to draw.") or is narrower than 0.000000001 or |edge|/100,000,000 ("These values make the distribution too narrow for the calculator's 12 digits. Widen it, or move it nearer 0."). This one test covers every family's scale: an exponential with λ = 1E49 or 1E−300, a normal with σ = 1E−300 or μ = 10⁴⁰ with σ = 1, a Gumbel, Laplace, logistic, Rayleigh, Pareto or Erlang squeezed or stretched past what 12 digits can draw. It is the line Norm3, NormExplorer, CICatcher and SampDist draw.
   - The form's sentence is shown, and the program goes back to the menu, as for the form's own errors.
4. **Four densities without overflow, the same numbers** (checked against SciPy and v2.7f below): the Burr XII density in logarithms (1301–1304); the Pareto density as (α/x)(x_m/x)^α (1312–1315), where x_m^α alone overflowed; the logistic density from |z| (1322–1326); the Fréchet density, CDF and right tail with u = z^(−α) in logarithms (1355–1359, 1494–1497, 1691–1693).
5. **Zoom− stops at 500 times the fitted window** (`st_Zoom` 3557, new `stFW`), where those formulas stay finite; the absolute limit of 10¹² stays.
6. `st_Fit` takes its continuous window from `st_FitWin` (the same lines, moved), and drops five locals it no longer uses.
7. The help page's title and the header say v2.7g.

Nothing else changed.

## Verification

`verify_StatDist_v2.7g.py`, output `verify_StatDist_v2.7g_output.txt`: **42 PASS, 0 FAIL**, run from a repository layout, with v2.7f read from git history (rule 18). Every run has `prime_facts_v1.py`'s device facts.

- **R** all 27 families, each with its default values and each of the three tails, through every key of the plot, the Numbers page and the Formula page: 2,349 screens, every text, box and result identical to v2.7f's. Help is identical but for the title on each of its 4 pages.
- **M** the typed fields (56 forms, 133 fields); no `!=` (v2.7f: 2); 31 refusals, one per kind of fault, each also run on v2.7f, where it fails (for μ = 10⁴⁰ with σ = 1, which the harness's 16 digits draw, v2.7f's window and tick counter are worked in 12-digit decimals: no width, and n + 1 = n); the ends of every new range, and values v2.7f could not draw, drawn with Zoom− twelve times and the Numbers page; every new box within 4 lines of 32 characters.
- **A** 148 values of the four rewritten densities (and the Fréchet CDF and right tail), inside the windows and far out, each within 1E−9 of SciPy; where v2.7f gave a finite number (144), v2.7g gives the same to 12 digits.
- **G** beyond the typed fields of the 27 forms, only 15 routines differ: `st_AskAB`, `st_BigMsg`, `st_Fit`, `st_FitWin`, `st_Init`, `st_LimP`, `st_LimX`, `st_Rng`, `st_Zoom`, `st_cdf`, `st_fmtp`, `st_fmtv`, `st_pdf`, `st_sf`, `st_show_help`; every routine tagged `st_`.
- **D** text_overlap_v1 over the same runs on both versions: no layout spot with a firm overlap, straddle or overrun that v2.7f does not also have.

**The sweep again**, on v2.7g (every parameter of all 27 families over 23 values from 1E−300 to 1E300, with Zoom− ten times): **0 broken** in 1,794 runs: 851 refused with a box, 943 drawn. Of v2.7f's 204 broken runs, v2.7g refuses 158 and draws 46. It also refuses 108 runs that v2.7f drew in the harness, and that is deliberate: 71 are too narrow for 12 digits (μ = 10¹² with σ = 1, say: on the Prime μ + 4σ rounds back to μ, which the harness's 16 digits do not show; or a window narrower than 1E−9, whose labels would need more than 12 decimals), 27 lie outside the new ranges (a binomial n or Poisson λ above 100,000, a Burr C or K below 0.2, a Weibull k of 10¹², a k above 10⁹, …), 6 reach past 1E50 (a t with df of 0.001 or less, a Cauchy scale or Gamma θ of 1E49), and 4 are numbers of more than 50 digits. v2.7g draws nothing that v2.7f refused.

**The monkey test again** (1,000 runs, 150 events each, `--lists`): v2.7g **1,000 OK**.

## Gate

`ppl_gate_v1d.py StatDist_v2.7g.txt StatDist_v2.7f.txt`: **RESULT: PASS**. ppl_check clean, as v2.7f.

## The Virtual Calculator

On the Virtual Calculator (2.4.2, build 2026-09-09, Rogers-HP; Claude through computer use, 1 Nov 2026, night). Check: "No errors in the program".

- Normal, **μ = 1E12, σ = 1**: the box "These values make the distribution too narrow for the calculator's 12 digits. Widen it, or move it nearer 0."
- Weibull, **k = 0.001**: "For the Weibull, k must be from 0.05 to 100 here."
- Normal, **σ = 1E−7**: drawn, but **its density labels 1000000 … 4000000 were cut by `TEXTOUT_P`'s width limit to "100000" … "400000"**, wrong numbers, and its x labels −0.0000003 … were printed over each other. **v2.7h** fixes both (`StatDist_v2.7h_CHANGES.md`); v2.7g was never committed.
- On v2.7h, in the same session: Burr XII with C = K = 100 through Zoom− twelve times, no error, the window stopping at about −15 … 15; Poisson with **λ = 100,000** drawn in under 10 seconds, P(X ≤ 100000) = 0.500841 (SciPy 0.5008410). 
