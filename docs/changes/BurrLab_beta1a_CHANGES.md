# BurrLab beta 1a — changes from beta 1 (28 Oct 2026)

Built from `parts/` (beta 1's parts archived in `parts_beta1/`); `BurrLab_beta1.txt` untouched.
Every finding of `REVIEW2_BurrLab_beta1.md` applied. Gate PASS (`gate_BurrLab_beta1a_output.txt`,
run against beta 1); fleet_names 0/0/0; case_scan clean over 30 files; `verify_BurrLab_beta1a.py`
2,667 checks, 0 failures (beta 1's 2,057 plus Part D below). Harness only; no hardware run.

1. **Weibull-limit detection (review finding 1).** `bu_Fit` now fits the rivals BEFORE the
   standard errors and flags the Weibull limit by its definition: a Burr ln L within
   1E-4 (1 + |ln L|) of the Weibull MLE's with K > 100 (the Weibull is the nested K → ∞ limit,
   so the Burr can never beat it by less than that without being it). The box-top test stays.
   Grouped path (no Weibull closed form): ln S within 1 of the box top, or K > 1E4. The Hessian
   runs only for flag 0. Verified on the reviewer's samples (6 Weibull(2.5) n = 30, 6 gamma(5)
   n = 40, Weibull(3) n = 30 seed 7, tinyK, floor, outlier) and 20 fresh samples: rev2, rev3,
   rev9, weib3, fresh15, fresh19 — all of which beta 1 left at flag 0 with K = 1E7..1E9 — are
   now flag 1; no flag-0 fit has K > 1E4, a missing Hessian, or an absurd K×C.
2. **No unclamped limit in Explore / simulation / CAS / Rare (finding 2).** Flag 1 installs the
   Weibull-equivalent at K = 50 with the same λ (S = λ 50^(1/C)); flags 2 and 3 leave the
   explorer's shape alone; the results page says which ("Explore, Rare and the CAS page show
   its Weibull-equivalent at K = 50" / "The explorer keeps its own shape"), and the Rare page
   labels its model ("model: Weibull-equivalent, K = 50" / "fit at a limit: the explorer's
   shape"). `bu_Median` is capped (ln 2/K > 500, or the final exponent > 500, returns 1E300),
   `bu_Num` prints "beyond range" from 1E12 (never ∞, never the scientific form), and the
   simulation refuses a shape whose median is beyond range.
3. **No file-level LOCAL matrix (finding 3).** The simplex is four file-level LOCAL lists
   `buSx1..buSx4` (3 elements each; element assignment into a file-level LOCAL list is
   ChiTable's hardware-proven shape) through `bu_SxG`/`bu_SxS`/`bu_SxRow`; the Hessian is a
   9-element row-major list. No MAKEMAT anywhere. The BJS optimum is reproduced to 1E-9.
4. **A-D page (finding 4).** Cites Stephens (1986, in D'Agostino & Stephens, Table 4.2) for
   the fully-specified points, states that no general table exists for fitted parameters, and
   says "above 2.5 fails even that lenient table; a smaller A² only ranks fits, it does not
   pass one". The unsourced "below 1.9 is reassuring" is gone.
5. **Wording (finding 5).** "the tail is not a power law"; both Danish screens: "1980-1990, in
   1985 prices (inflation-adjusted DKK); excess over 1M DKK", McNeil (1997) named. The
   "K×C = 202172937.96" display cannot arise now (finding 1). Finding 6 (a still progress bar
   during the Hessian and the Weibull bisection, a few seconds at n = 1,000) is accepted and
   noted; progress labels were re-spaced for the new order (rivals 0.55–0.9, SEs 0.9, A-D 0.96).

Header: version, date, the change list, the file map (about 3,090 lines; the map's own lines
shift it by about one).
