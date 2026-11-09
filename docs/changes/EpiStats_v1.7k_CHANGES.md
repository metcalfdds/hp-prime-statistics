# EpiStats v1.7k: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes EpiStats v1.7k from EpiStats v1.7j. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1, 5, 6, 11, 13 and 14 reworded: the help-page numbers named as numbers, the confidence intervals, Mantel-Haenszel, the PPV plot and the forest plot in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 15 screens, as the PC harness counts them.

3. **Outside the help** only these lines changed (the version on screen, and the page numbers the help's callers ask for):

```text
EpiStats       -        CHOOSE(choice, "EpiStats v1.7j ══════════",
EpiStats       +        CHOOSE(choice, "EpiStats v1.7k ══════════",
```

Routines touched, with the number of new or changed lines in each: (comments) 7, EpiStats 1, es_Help_About 8, es_Help_CI 7, es_Help_Exact 9, es_Help_Forest 10, es_Help_MH 9, es_Help_Prev 9.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 6 of 15 screens changed; 9 kept their words.

### Before (v1.7j)

```text
EpiStats help 1/15: About EpiStats
EpiStats v1.7j
Comprehensive biostatistics and epidemiology
calculator.
Modules: 2×2 tables, risk analysis, diagnostic
tests, incidence rates, stratified (Mantel-
Haenszel) analysis, and sample size.
From Home: EpiStats2x2(a,b,c,d) opens the 2×2
results at once and returns Fisher's p.
EP_* results.  Touch: Help 9-D; exact: E, F.
any key or tap = back
```

```text
EpiStats help 5/15: Confidence intervals
Proportions: Wilson score interval (better
coverage than Wald, esp. for small n).
Exact (Clopper-Pearson) beside it: Help E.
OR/RR: log method - compute CI on ln(OR),
then exponentiate.  Its SE: Help F.
If a 95% CI for OR/RR excludes 1, the
association is significant at α = 0.05.
For RD, the CI excludes 0 when significant.
any key or tap = back
```

```text
EpiStats help 6/15: Mantel-Haenszel
Combine 2×2 tables across strata to control
for a confounder: OR_MH = sum(ad/n)/sum(bc/n).
95% CI: Robins-Breslow-Greenland for the OR,
Greenland-Robins (1985) for RR and IRR.
M-H χ² (1 df): is the common OR 1?
Breslow-Day (k-1 df): are the strata's ORs
alike?  Small p: report them separately.
Rule of thumb, not a test: if crude and
adjusted differ by 10 % or more, adjust.
Page 3, forest plot: tap a stratum (or
Up/Down) to drop it from the pool and watch
the M-H estimate change; tap again = back.
any key or tap = back
```

```text
EpiStats help 11/15: PPV vs prevalence, ROC
Diagnostic module, page 4: PPV (magenta) and
NPV (blue) for THIS test at every prevalence.
Drag along the plot or the slider, or use the
arrows (1 %; Up/Down 10 %); 0 = your sample's
prevalence, the red marker.  +/- = page.
PPV = sens×p / (sens×p + (1-spec)(1-p))
NPV = spec(1-p) / (spec(1-p) + (1-sens)p)
A rare disease makes most positives false.
Page 5: the test as a point on the ROC square:
LR+ = slope of the line from (0,0), LR- =
slope of the line from (1,1); dotted = chance.
any key or tap = back
```

```text
EpiStats help 13/15: Forest, risk bars, NNT
Stratified, page 3: one row per stratum, then
the crude and the M-H estimate, log scale.
Square size = M-H weight; bar = 95% CI;
magenta diamond = M-H and its CI; dotted = 1.
Tap a stratum (Up = 1, Down = 2): drop/restore.
Risk module, page 4: each group's risk with a
95% Wilson CI; the magenta bracket is the RD.
OR/RR = (1-Ru)/(1-Re): the OR overstates the
RR when the outcome is common.
Page 5: NNT = 1/|RD| rounded up: that many
people (blue); red = the one extra case,
green = the one case prevented.
any key or tap = back
```

```text
EpiStats help 14/15: Exact CIs, exact OR
Exact (Clopper-Pearson) CI of a proportion:
every p under which your count is in neither
2.5 % tail of Binomial(n, p). No normal curve,
and it never covers less than 95 % for any p,
so it is wider than Wilson (conservative).
mid-P counts half of P(X = k): nearer 95 %.
Where: 2×2 Diagnostic tab, risk bars (orange),
diagnostic module page 6 (tap a row).
Conditional MLE OR (2×2, page 7): the OR that
puts the mean of a at your a, all four totals
fixed. R's fisher.test reports it; it sits
nearer 1 than ad/bc when counts are small.
any key or tap = back
```

### After (v1.7k)

```text
EpiStats help 1/15: About EpiStats
EpiStats v1.7k
Comprehensive biostatistics and epidemiology calculator.
Modules: 2×2 tables, risk analysis, diagnostic tests, incidence
rates, stratified (Mantel- Haenszel) analysis, and sample size.
From Home: EpiStats2x2(a,b,c,d) opens the 2×2 results at once
and returns Fisher's p.
Results are kept in Home as EP_ variables (help page 8).  Touch
and keys: help pages 9 to 13; exact answers: pages 14 and 15.
any key or tap = back
```

```text
EpiStats help 5/15: Confidence intervals
Proportions: Wilson score interval (better coverage than Wald,
especially for small n).
Exact (Clopper-Pearson) beside it: help page 14.
OR/RR: the log method: find the CI for ln(OR), then take e to the
power of each end.  Where its SE comes from: help page 15.
If a 95% CI for OR/RR excludes 1, the association is significant
at α = 0.05.
For RD, the CI excludes 0 when significant.
any key or tap = back
```

```text
EpiStats help 6/15: Mantel-Haenszel
Combine 2×2 tables across strata to control for a confounder:
OR_MH = sum(ad/n)/sum(bc/n).
95% CI: Robins-Breslow-Greenland for the OR,
Greenland-Robins (1985) for RR and IRR.
M-H χ² (1 df): is the common OR 1?
Breslow-Day (k-1 df): are the strata's ORs alike?  A small p
means the strata's ORs differ: report them separately.
Rule of thumb, not a test: if crude and adjusted differ by 10 % or
more, adjust.
Page 3, forest plot: tap a stratum (or Up/Down) to drop it from
the pool and watch the M-H estimate change; tap it again to put
it back.
any key or tap = back
```

```text
EpiStats help 11/15: PPV vs prevalence, ROC
Diagnostic module, page 4: PPV (magenta) and NPV (blue) for
THIS test at every prevalence.
Drag along the plot or the slider, or use the arrows (1 %;
Up/Down 10 %); 0 = your sample's prevalence, the red marker.
+/- turn the page.
PPV = sens×p / (sens×p + (1-spec)(1-p))
NPV = spec(1-p) / (spec(1-p) + (1-sens)p) A rare disease makes
most positives false.
Page 5: the test as a point on the ROC square:
LR+ = slope of the line from (0,0), LR- = slope of the line from
(1,1); dotted = chance.
any key or tap = back
```

```text
EpiStats help 13/15: Forest, risk bars, NNT
Stratified, page 3: one row per stratum, then the crude and the
M-H estimate, log scale.
Square size = M-H weight; bar = 95% CI;
magenta diamond = M-H and its CI; dotted = 1.
Tap a stratum (or press Up for stratum 1, Down for stratum 2) to
drop it from the pool or put it back.
Risk module, page 4: each group's risk with a 95% Wilson CI; the
magenta bracket is the RD.
OR/RR = (1-Ru)/(1-Re): the OR overstates the RR when the
outcome is common.
Page 5: NNT = 1/|RD| rounded up: that many people (blue);
red = the one extra case, green = the one case prevented.
any key or tap = back
```

```text
EpiStats help 14/15: Exact CIs, exact OR
Exact (Clopper-Pearson) CI of a proportion:
every p for which your count is not in either 2.5 % tail of
Binomial(n, p). No normal curve, and it never covers less than 95
% for any p, so it is wider than Wilson (conservative).
The mid-P interval counts only half of P(X = k), so its coverage is
nearer 95 %.
Where: 2×2 Diagnostic tab, risk bars (orange), diagnostic module
page 6 (tap a row).
Conditional MLE OR (2×2, page 7): the OR that puts the mean of a
at your a, all four totals fixed. R's fisher.test reports it; it sits
nearer 1 than ad/bc when counts are small.
any key or tap = back
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in v1.7j; lint_ppl 8 problems, as in v1.7j (8); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 15 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
