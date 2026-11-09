# SampDist v2.3j: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes SampDist v2.3j from SampDist v2.3i. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 and 2 reworded: the standard error written with a root sign, and the graph's keys in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 2 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 5, sd_showHelp 25.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 2 of 2 screens changed; 0 kept their words.

### Before (v2.3i)

```text
SampDist help 1/2: The sampling distribution
The sample mean x̄ of n draws from a
Normal(μ, σ) population is itself Normal,
centered on μ with standard error
σx̄ = σ / SQRT(n).
Find probability
   Choose left, right, between or outside,
   then enter the bounds.
Find critical value
   Enter α; get the x̄ cutting off that tail.
Compare sample sizes
   Three curves, shared axes: 4× n halves σx̄.
Watch sample means
   40 simulated means fall onto the axis,
   then become a histogram under the curve.
Results persist in Home as EP_SD_*
any key or tap = next
```

```text
SampDist help 2/2: The result graph
   gray = the population N(μ, σ); blue = x̄,
   on ONE scale: at n = 30 the population's
   peak is 18% of x̄'s.
Soft keys
   n− n+  step n through 1, 2, 4 ... 400
   n×4  quadruples n: σx̄ halves
   μ,σ  edit;  Tail  next region;  Menu
Touch
   drag in the plot: the nearer bound moves
   ⇆ nudge it, ⇅ the other bound, +/- = n,
   Ent = more, Esc = menu
Compare sample sizes
   drag = a cursor with P(x̄ < x) for each n;
   tap a curve to pick it.
Critical values: a new n moves them (α kept).
any key or tap = menu
```

### After (v2.3j)

```text
SampDist help 1/2: The sampling distribution
The sample mean x̄ of n draws from a Normal(μ, σ) population is
itself Normal, centered on μ with standard error
σx̄ = σ / √n.
Find probability
   Choose left, right, between or outside, then enter the bounds.
Find critical value
   Enter α; get the x̄ cutting off that tail.
Compare sample sizes
   Three curves on the same axes: four times the n gives half the
   standard error.
Watch sample means 40 simulated means fall onto the axis, then
   become a histogram under the curve.
Results are kept in Home as EP_SD_ names.
any key or tap = next
```

```text
SampDist help 2/2: The result graph
   gray = the population N(μ, σ); blue = x̄, on ONE scale: at n = 30
   the population curve's peak is only 18% as high as the
   x̄ curve's.
Soft keys n− n+  step n through 1, 2, 4 ... 400 n×4  quadruples n:
   σx̄ halves μ,σ  edit;  Tail  the next kind of region (left, right,
   between, outside);  Menu
Touch drag in the plot: the nearer bound moves ⇆ nudge it, ⇅
   the other bound, +/- = n, Ent = more, Esc = menu
Compare sample sizes drag = a cursor with P(x̄ < x) for each n;
   tap a curve to pick it.
Critical values: changing n moves them; α stays the same.
any key or tap = menu
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in v2.3i; lint_ppl 18 problems, as in v2.3i (18); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 2 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
