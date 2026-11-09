# ResampLab beta 1h: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes ResampLab beta 1h from ResampLab beta 1g. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 and 3 reworded: the shuffle, "exchangeable", the stacked dots, the basic interval and small samples in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 5 screens, as the PC harness counts them.

3. **Outside the help** only these lines changed (the version on screen, and the page numbers the help's callers ask for):

```text
rs_Splash      -  rs_Ln("(C) 2026 Roger D. Metcalf; beta 1g 4 Nov 2026", 205, rsGRAY);
rs_Splash      +  rs_Ln("(C) 2026 Roger D. Metcalf; beta 1h 9 Nov 2026", 205, rsGRAY);
```

Routines touched, with the number of new or changed lines in each: (comments) 7, rs_Help 5, rs_Splash 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 2 of 5 screens changed; 3 kept their words.

### Before (beta 1g)

```text
ResampLab help 1/5: Shuffling labels
A permutation test asks: if the group labels
did not matter (H₀), how often would chance
alone give a difference as big as the one we
saw?
Once: the pooled values are dealt again into
groups of the same sizes, and their
difference d drops onto the histogram.  Red
line: the observed d; red dots: shuffles at
least as extreme.
p = (as extreme)/(shuffles).  Small p: the
labels seem to matter.  Large p: no evidence
that they do (not proof that they don't).
Assumes: under H₀ the labels are exchangeable
(random assignment).
Any key = page 2
```

```text
ResampLab help 3/5: The bootstrap
Treat the sample as the population: draw n
values WITH replacement (a stack = picked
more than once) and compute the statistic. 
Repeat B times: their spread estimates its
SE.
Percentile: the middle 95% of the B values. 
Basic: those ends reflected about the
estimate.  BCa: corrected for bias (z₀) and
skew (a); use B ≥ 1,000.  t: x̄ ± t s/√n, to
compare.
Two groups: each resampled from itself;
percentile, and Welch's t for means.
Small samples give too narrow intervals: n ≥
15 or so.
Any key = page 4
```

### After (beta 1h)

```text
ResampLab help 1/5: Shuffling labels
A permutation test asks: if the group labels
did not matter (H₀), how often would chance
alone give a difference as big as the one we
saw?
Once: the pooled values are shuffled into new
groups of the same sizes, and the new
difference d is added to the histogram.  Red
line: the observed d; red dots: shuffles at
least as extreme.
p = (as extreme)/(shuffles).  Small p: the
labels seem to matter.  Large p: no evidence
that they do (not proof that they don't).
Assumes: under H₀ the labels could be swapped
without changing anything, which is true when
the groups were made by random assignment.
Any key = page 2
```

```text
ResampLab help 3/5: The bootstrap
Treat the sample as the population: draw n
values WITH replacement (a stack of dots = a
value picked more than once) and compute the
statistic.  Repeat B times: their spread
estimates its SE.
Percentile: the middle 95% of the B values. 
Basic: the same two ends, mirrored around the
estimate.  BCa: corrected for bias (z₀) and
skew (a); use B ≥ 1,000.  t: x̄ ± t s/√n, to
compare.
Two groups: each resampled from itself;
percentile, and Welch's t for means.
With small samples the intervals are too
narrow: use n of about 15 or more.
Any key = page 4
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1g; lint_ppl 10 problems, as in beta 1g (10); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 5 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
