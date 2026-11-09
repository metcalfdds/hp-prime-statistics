# BurrLab beta 1q: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes BurrLab beta 1q from BurrLab beta 1p. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** The help is now 6 pages (was 4): pages 1 and 2 each became two. Help pages 1, 2 and 4 reworded: the mean that never settles, the plot during a drag, the map's colors, the fit's limits and the Python engine in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is 6 screens (was 4), as the PC harness counts them.

3. **Outside the help** only these lines changed (the version on screen, and the page numbers the help's callers ask for):

```text
bu_Opening     -  bu_Frame("BurrLab beta 1p: the long right tail");
bu_Opening     +  bu_Frame("BurrLab beta 1q: the long right tail");
```

Routines touched, with the number of new or changed lines in each: (comments) 8, bu_Help 13, bu_Opening 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 5 of 6 screens changed; 1 kept their words (1 of them with a new page number).

### Before (beta 1p)

```text
BurrLab help 1/4: The Burr XII model
The Burr XII is a flexible model for a long
right tail: sentences served, waits to
re-arrest, insurance losses, incomes. Two
shapes C and K and a scale S. Its tail is a
power law: P(X > x) falls like x^(-K C).
The mean exists only if K×C > 1, the variance
only if K×C > 2: with a heavy enough tail the
sample mean never settles (menu 4).
Explore: soft keys choose C, K, S or x₀; arrows
step it; drag sideways in the plot to slide it;
tap to put x₀ there; it stops at the right
edge. The window freezes while a finger is down
and refits on the lift. A yellow hourglass at
the top right: still computing.
Right/tap = next page, Esc = back
```

```text
BurrLab help 2/4: Family, fit, pictures
Family tree: C = 1 is Pareto II (Lomax); K = 1
is the log-logistic (Fisk); K → ∞ with S = Sw
K^(1/C) is the Weibull. Tap the map to set (C,
K); its colors are the moment cases.
Fit: maximum likelihood (a profile Nelder-Mead
over C and S with K solved exactly), SEs from
the observed information, then lognormal,
Weibull, gamma, exponential and Lomax by their
own MLEs, compared by AIC. A fit that runs to
the Weibull or Pareto limit is named as such.
Pictures: histogram, Q-Q (tap a point),
survival on log-log axes (a heavy tail is a
straight line), hazard, Anderson-Darling (a
statistic, honestly without a p).
Right/tap = next page, Esc = back
```

```text
BurrLab help 4/4: Fit engines
Fit engines (Fit menu, Engine). Both engines
run the SAME algorithm on the same data: the
profile simplex, the box, the Hessian.
Auto: the MicroPython engine first; if it fails
or disagrees with the PPL likelihood, the PPL
engine answers and the badge says so.
PPL only: the PPL engine alone (slow on a G1:
about 45 s for 300 values).
Python only: no fallback; a bridge failure
shows a message, and BU_PZ in Home holds the
script's last step or its error.
Both: Python, then PPL, both timed; a line
compares C, K, S; Python's kept. Explore's
curves: PPL in Auto (More > Timing).
Right/tap = next page, Esc = back
```

### After (beta 1q)

```text
BurrLab help 1/6: The Burr XII model
The Burr XII is a flexible model for a long
right tail: sentences served, waits to
re-arrest, insurance losses, incomes. Two
shapes C and K and a scale S. Its tail is a
power law: P(X > x) falls like x^(-K C).
The mean exists only if K×C > 1, the variance
only if K×C > 2: with a heavy enough tail the
sample mean never settles down to one value
(menu 4).
Right/tap = next page, Esc = back
```

```text
BurrLab help 2/6: Explore
Explore: soft keys choose C, K, S or x₀; arrows
step it; drag sideways in the plot to slide it;
tap to put x₀ there; it stops at the right
edge. The plot holds still while your finger is
on the screen and is fitted again when you lift
it. A yellow hourglass at the top right: still
computing.
Right/tap = next page, Esc = back
```

```text
BurrLab help 3/6: Family tree and fit
Family tree: C = 1 is Pareto II (Lomax); K = 1
is the log-logistic (Fisk); K → ∞ with S = Sw
K^(1/C) is the Weibull. Tap the map to set (C,
K); its colors show whether the mean and the
variance exist there.
Fit: maximum likelihood (a profile Nelder-Mead
over C and S with K solved exactly), SEs from
the observed information, then lognormal,
Weibull, gamma, exponential and Lomax by their
own MLEs, compared by AIC. If the best fit is
at the Weibull or Pareto limit, the fit is
named that.
Right/tap = next page, Esc = back
```

```text
BurrLab help 4/6: Pictures
Pictures: histogram, Q-Q (tap a point),
survival on log-log axes (a heavy tail is a
straight line), hazard, Anderson-Darling (the
statistic only, with no p-value).
Right/tap = next page, Esc = back
```

```text
BurrLab help 6/6: Fit engines
Fit engines (Fit menu, Engine). Both engines
run the SAME algorithm on the same data: the
profile simplex, the box, the Hessian.
Auto: the MicroPython engine first; if it fails
or disagrees with the PPL likelihood, the PPL
engine answers and the badge says so.
PPL only: the PPL engine alone (slow on a G1:
about 45 s for 300 values).
Python only: no fallback; if the Python engine
fails, a message says so, and BU_PZ in Home
holds the script's last step or its error.
Both: Python, then PPL, both timed; a line
compares C, K, S; Python's kept. Explore's
curves: PPL in Auto (More > Timing).
Right/tap = next page, Esc = back
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1p; lint_ppl 27 problems, as in beta 1p (27); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 6 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".
  On the Virtual Calculator all six help pages were opened from the menu and read (`verify/round11/screens/`), after the page titles were made to say what each page is about (Explore, Family tree and fit, Pictures): every line inside its page, nothing cut.
- `tools/monkey_v1b.py --lists`, 1,000 runs of 120 random keys, taps, menu picks and typed values (1,212 s): OK 971, FREEZE 1, HARNESS 28.
  The one FREEZE is the 20-s limit, not a hang: run 1000536 fits all 2,156 Danish fire losses, and replayed alone (`--replay 1000536`) it ended OK in 13.3 s; the batch had shared the processor with StudRange's test. The HARNESS runs are the harness's own gap: `RANDSEED` is on HP's list of names and the harness does not model it, as in beta 1l and beta 1p.

Not yet run on a G1 or a G2.
