# TDist3D beta 1a: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes TDist3D beta 1a from TDist3D beta 1. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 to 4 reworded: "row" is now "curve", "stacks", "the price of estimating sigma", "climb a ladder" and "raises the eye" in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 4 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, tdHelp 42.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 4 of 4 screens changed; 0 kept their words.

### Before (beta 1)

```text
TDist3D help 1/4: What the surface is
When σ is unknown, s takes its place in
t = (x̄ − μ) / (s/√n), and s is a different
number in every sample: t varies more than
z does, and the extra variation goes into
the tails.
Student's t has one parameter, the degrees
of freedom ν = n − 1.  This surface stacks
the curves: t runs across, ν runs away from
you, 0.5 at the front to 10 at the back; the
height is the density f(t; ν).
Every row has area 1.  The front rows are
low in the middle and lifted in the tails;
the back rows rise toward N(0,1), the gray
dots past the back edge: ν = ∞ is the
normal curve itself.
1/4, tap or key = next page, Esc = back
```

```text
TDist3D help 2/4: What ν does
The smaller the sample, the less we know about
σ, and the heavier the tails:
ν      peak f(0)   t crit (2.5 %)   P(|t| > 2)
1       0.318       12.706         0.295
2       0.354        4.303         0.184
5       0.380        2.571         0.102
10      0.389        2.228         0.073
30      0.396        2.042         0.055
∞ (z)   0.399        1.960         0.046
With one degree of freedom a value beyond ±2
turns up almost 30 % of the time, and the 95 %
critical value is 12.7, not 1.96.  By ν = 30,
the price of estimating σ is small.
2/4, tap or key = next page, Esc = back
```

```text
TDist3D help 3/4: The slice and its numbers
Slice marks one row, ν = ν₀, in red, and the
corner gives its numbers:
peak: f(0; ν₀), the height at t = 0;
t crit: the t with 2.5 % beyond it, the number
that replaces 1.960 in a 95 % interval or a
two-sided test at α = 0.05 (STUDENT_ICDF);
beyond ±2: P(|t| > 2), the chance of a value
past 2 in either direction, 0.046 for z.
The red posts stand at ±t crit when they fall
inside t = ±6; at ν = 1 they do not (12.7).
ν− and ν+ climb a ladder: 0.5, 1, 1.5, 2, 2.5,
3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 100, 1,000.
Menu > Set ν exactly takes values in between.
3/4, tap or key = next page, Esc = back
```

```text
TDist3D help 4/4: Keys and touch
Drag: sideways turns, downward raises the eye.
Arrows: Left, Right turn; Up, Down raise and
lower the eye; 10° a step.
ν− ν+ (or the − and + keys): the next ν.
Curves: the family seen end on; 3-D goes back.
In Curves, Up and Down move the slice, and a
tap on a curve picks it.
Slice: on or off.  Reset: θ = 35°, φ = 30°,
ν = 3.
Menu (Enter): set ν exactly, the views, the
slice, reset, the grid while dragging, frame
timing, help, quit.  Esc = quit.
Home after a run: TD_NU holds ν.
4/4, tap or key = back to the surface
```

### After (beta 1a)

```text
TDist3D help 1/4: What the surface is
When σ is unknown, s takes its place in t = (x̄ − μ) / (s/√n), and
s is a different number in every sample: t varies more than z
does, and the extra variation goes into the tails.
Student's t has one parameter, the degrees of freedom ν = n − 1.
This surface puts the curves one behind another: t runs across,
ν runs away from you, 0.5 at the front to 10 at the back; the
height is the density f(t; ν).
Every curve has area 1.  The front curves (small ν) are low in the
middle and high in the tails; the back curves come close to
N(0,1), the normal curve, drawn as gray dots beyond the back
edge (ν = ∞).
1/4, tap or key = next page, Esc = back
```

```text
TDist3D help 2/4: What ν does
The smaller the sample, the less we know about σ, and the
heavier the tails:
ν      peak f(0)   t crit (2.5 %)   P(|t| > 2)
1       0.318       12.706         0.295
2       0.354        4.303         0.184
5       0.380        2.571         0.102
10      0.389        2.228         0.073
30      0.396        2.042         0.055
∞ (z)   0.399        1.960         0.046
With one degree of freedom a value beyond ±2 turns up almost
30 % of the time, and the 95 % critical value is 12.7, not 1.96.
By ν = 30, using s in place of σ makes little difference.
2/4, tap or key = next page, Esc = back
```

```text
TDist3D help 3/4: The slice and its numbers
Slice draws one curve, ν = ν₀, in red, and the corner gives that
curve's numbers:
peak: f(0; ν₀), the height at t = 0;
t crit: the t with 2.5 % beyond it, the number that replaces
1.960 in a 95 % interval or a two-sided test at α = 0.05
(STUDENT_ICDF);
beyond ±2: P(|t| > 2), the chance of a value past 2 in either
direction, 0.046 for z.
The red posts mark ±t crit when it lies inside t = ±6; at ν = 1 it
does not (12.7).
ν− and ν+ step ν through 0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 15,
20, 30, 50, 100, 1,000.
For a value in between, use Menu > Set ν exactly.
3/4, tap or key = next page, Esc = back
```

```text
TDist3D help 4/4: Keys and touch
Drag sideways to turn the surface; drag down to look at it from
higher up.
Arrows: Left and Right turn it; Up and Down look from higher or
lower; 10° a press.
ν− ν+ (or the − and + keys): the next ν.
Curves: all the curves seen flat, from the front; 3-D goes back to
the surface.
In Curves, Up and Down move the slice, and tapping a curve
makes it the slice.
Slice: on or off.  Reset: θ = 35°, φ = 30°, ν = 3.
Menu (Enter): set ν exactly, the views, the slice, reset, the grid
while dragging, frame timing, help, quit.  Esc = quit.
After a run, TD_NU in Home holds the last ν.
4/4, tap or key = back to the surface
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1; lint_ppl 5 problems, as in beta 1 (5); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 4 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
