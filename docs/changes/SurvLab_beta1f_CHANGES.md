# SurvLab beta 1f: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes SurvLab beta 1f from SurvLab beta 1e. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help page 2 reworded: "n.r. = open" in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 5 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, sv_Help 10.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 1 of 5 screens changed; 4 kept their words.

### Before (beta 1e)

```text
SurvLab help 2/5: CIs, median, quantiles
95% CI, log-log (default): S^exp(±1.96 √V/|ln S|),
V = sum of d/(n(n - d)); it stays inside 0..1.
Linear (soft key CI): S ± 1.96 SE, cut at 0 and 1.
Median: the first time S(t) < 0.5 (statsmodels;
SAS and R average if S sits exactly on 0.5).
If S never gets below 0.5 it is NOT REACHED: in
Rossi only 26% are re-arrested in 52 weeks.  Then
report the time by which 25%, 20% or 10% are
re-arrested (25%: S = 0.75, the 25th percentile,
or first quartile, of the time to re-arrest).
CI of a quantile (Brookmeyer & Crowley 1982): the
event times whose band reaches S = 1 - p, up to
the next event time (not included); n.r. = open.
Cumulative hazard H(t) = sum of d/n (Nelson-Aalen).
Page 2/5, any key = next, Esc = leave
```

### After (beta 1f)

```text
SurvLab help 2/5: CIs, median, quantiles
95% CI, log-log (default): S^exp(±1.96 √V/|ln S|), V = sum of
d/(n(n - d)); it stays inside 0..1.
Linear (soft key CI): S ± 1.96 SE, cut at 0 and 1.
Median: the first time S(t) < 0.5 (statsmodels;
SAS and R average if S sits exactly on 0.5).
If S never gets below 0.5 it is NOT REACHED: in Rossi only 26%
are re-arrested in 52 weeks.  Then report the time by which
25%, 20% or 10% are re-arrested (25%: S = 0.75, the 25th
percentile, or first quartile, of the time to re-arrest).
CI of a quantile (Brookmeyer & Crowley 1982): the event times
whose band reaches S = 1 - p, up to the next event time (not
included); n.r. (not reached) = no upper end.
Cumulative hazard H(t) = sum of d/n (Nelson-Aalen).
Page 2/5, any key = next, Esc = leave
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1e; lint_ppl 6 problems, as in beta 1e (6); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 5 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
