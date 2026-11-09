# TrendTest beta 3m: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes TrendTest beta 3m from TrendTest beta 3l. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1, 2 and 3 reworded: why one df has more power, what the departure from a line means, the Scores key, the plots and the keys in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 3 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, trHelp 38.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 3 of 3 screens changed; 0 kept their words.

### Before (beta 3l)

```text
TrendTest help 1/3: χ² for trend, the idea
Exposure levels have an ORDER (dose, hours,
grade).  Pearson's χ² (k-1 df) asks
only 'do the proportions differ?'.  The trend
test (1 df) asks 'do they rise or fall
steadily with the score?'
1 df concentrates the evidence: more power
than Pearson when the line really fits.
Pearson - trend = departure from linearity
(k-2 df); large means 'not a straight line'.
Scores: use the doses themselves when known;
otherwise 1, 2, 3 ...  The trend answer depends
on the spacing; Pearson's does not.  Press
Scores: 1,2,3 / as entered / midranks.
any key = page 2, Esc = menu
```

```text
TrendTest help 2/3: Reading the plots
Proportions plot: a dot per level, p = cases/n
with its 95% Wilson bar; the weighted (WLS)
line in magenta with its 95% band; overall p
dotted.  Dots: blue above the line, red below,
gray within 1 SE of it (SE² = P(1-P)/n).
Drag a dot up or down (or Up/Down) to change
its cases: the line tilts, the band and the
tests follow.  Restore puts the data back.
Odds ratio plot: each level against level 1,
log scale: 0.5 and 2 lie equally far from 1;
Woolf 95% intervals; dotted line = OR 1.
Band: fit ± 1.96 SE, SE² = P(1-P) times
(1/N + (x - x̄)² / sum n(x - x̄)²).
Results page 4: where the line comes from.
any key = page 3, Esc = menu
```

```text
TrendTest help 3/3: Keys; the same test elsewhere
Soft keys: Prop and OR = the two plots;
Scores = 1,2,3 / as entered / midranks; Data
= type new counts; Restore = undo the drags;
Menu = back.  Keys: ⇆ = level, ⇅ = cases,
+ = Scores, 0 = Restore, - = other plot,
Esc = menu.  Results: 4 pages, ⇆ or tap.
The proportions plot animates the fit as it
opens (any key or tap skips).  Page 4: the CAS
finds the line's slope as an exact fraction.
Same test elsewhere: Epi Info StatCalc prints
Mantel's (1963) (N-1) r², as this page does;
R prop.trend.test and SAS PROC FREQ / TREND
print Armitage's (1955) N r²: 72.688 for
snoring, 72.659 here.  The ratio is N/(N-1).
any key = menu
```

### After (beta 3m)

```text
TrendTest help 1/3: χ² for trend, the idea
Exposure levels have an ORDER (dose, hours, grade).  Pearson's
χ² (k-1 df) asks only 'do the proportions differ?'.  The trend test
(1 df) asks 'do they rise or fall steadily with the score?'
With 1 df the trend test puts all its evidence into one question,
so it has more power than Pearson's when the proportions
really do lie near a straight line.
Pearson's χ² minus the trend χ² (k-2 df) measures how far the
proportions are from a straight line; a large value means they do
not follow one.
Scores: use the doses themselves when known;
otherwise 1, 2, 3 ...  The trend test's answer depends on how the
scores are spaced; Pearson's does not.  The Scores key switches
among 1, 2, 3 ..., the scores as entered, and midranks.
any key = page 2, Esc = menu
```

```text
TrendTest help 2/3: Reading the plots
Proportions plot: a dot per level, p = cases/n with its 95%
Wilson bar; the weighted least-squares (WLS) line in magenta,
with its 95% band; the overall proportion as a dotted line.  Dots:
blue above the line, red below, gray within 1 SE of it
(SE² = P(1-P)/n).
Drag a dot up or down (or Up/Down) to change its cases: the
line, its band, and the tests change with it.  Restore puts the
data back.
Odds ratio plot: each level's odds ratio against level 1, on a log
scale (so 0.5 and 2 lie equally far from 1), with Woolf 95%
intervals; the dotted line is OR = 1.
Band: fit ± 1.96 SE, SE² = P(1-P) times
(1/N + (x - x̄)² / sum n(x - x̄)²).
Page 4 of the results shows how the line is worked out.
any key = page 3, Esc = menu
```

```text
TrendTest help 3/3: Keys; the same test elsewhere
Soft keys: Prop and OR = the two plots;
Scores = 1,2,3 / as entered / midranks; Data = type new counts;
Restore = undo the drags;
Menu = back.  Keys: ⇆ = choose a level, ⇅ = change its
cases, + = Scores, 0 = Restore, - = other plot, Esc = menu.  The
results run to 4 pages; turn them with ⇆ or a tap.
The proportions plot draws the fit step by step as it opens (any
key or tap skips to the end).  Page 4: the CAS finds the line's
slope as an exact fraction.
Same test elsewhere: Epi Info StatCalc prints Mantel's (1963)
(N-1) r², as TrendTest does;
R prop.trend.test and SAS PROC FREQ / TREND print Armitage's
(1955) N r²: 72.688 for snoring, 72.659 here.  The ratio
is N/(N-1).
any key = menu
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 3l; lint_ppl 14 problems, as in beta 3l (14); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 3 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
