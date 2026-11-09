# BiNorm3D beta 1f: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes BiNorm3D beta 1f from BiNorm3D beta 1e. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 and 5 reworded: "X says nothing about Y" and "raises the eye" in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 5 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, bnHelp 21.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 2 of 5 screens changed; 3 kept their words.

### Before (beta 1e)

```text
BiNorm3D help 1/5: What ρ does
X and Y each follow N(0, 1); ρ is their
correlation.  The surface is their joint
density f(x, y): the volume under it is 1.
ρ = 0: a round bell.  X says nothing about Y.
ρ > 0: it stretches along y = x (high x with
high y); ρ < 0: along y = −x.
The volume stays 1, so a narrower bell is a
taller one: the peak f(0, 0) is 0.159 at
ρ = 0, 0.199 at 0.6 and 0.365 at 0.9.
Color = height: blue low, then magenta, red
at the top.  The height scale never changes,
so the peaks can be compared across ρ.
1/5, tap or key = next page, Esc = back
```

```text
BiNorm3D help 5/5: Keys and touch
Drag: sideways turns, downward raises the eye.
Arrows: Left, Right turn; Up, Down raise and
lower the eye; 10° a step.
ρ− ρ+ (or the − and + keys): ρ by 0.1.
Cont: the view from above; 3-D goes back.
Slice: on or off.  From above, tap or drag
the plot (or Left, Right) to move x₀.
Reset: θ = 35°, φ = 30°, ρ = 0.60.
Menu (Enter): set ρ exactly, the views, the
slice, reset, the grid while dragging, frame
timing, help, quit.  Esc = quit.
A drag draws an 11×11 grid, 15×15 on lifting.
Home after a run: BN_RHO holds ρ.
5/5, tap or key = back to the surface
```

### After (beta 1f)

```text
BiNorm3D help 1/5: What ρ does
X and Y each follow N(0, 1); ρ is their correlation.  The surface is
their joint density f(x, y): the volume under it is 1.
ρ = 0: a round bell.  Knowing X tells you nothing about Y.
ρ > 0: it stretches along y = x (high x with high y); ρ < 0:
along y = −x.
The volume stays 1, so a narrower bell is a taller one: the peak
f(0, 0) is 0.159 at ρ = 0, 0.199 at 0.6 and 0.365 at 0.9.
Color = height: blue low, then magenta, red at the top.  The
height scale never changes, so the peaks can be
compared across ρ.
1/5, tap or key = next page, Esc = back
```

```text
BiNorm3D help 5/5: Keys and touch
Drag sideways to turn the surface; drag down to look at it from
higher up.
Arrows: Left and Right turn it; Up and Down look from higher or
lower; 10° a press.
ρ− ρ+ (or the − and + keys): ρ by 0.1.
Cont: the view from above; 3-D goes back.
Slice: on or off.  From above, tap or drag the plot (or Left, Right)
to move x₀.
Reset: θ = 35°, φ = 30°, ρ = 0.60.
Menu (Enter): set ρ exactly, the views, the slice, reset, the grid
while dragging, frame timing, help, quit.  Esc = quit.
A drag draws an 11×11 grid, 15×15 on lifting.
Home after a run: BN_RHO holds ρ.
5/5, tap or key = back to the surface
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1e; lint_ppl 5 problems, as in beta 1e (5); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 5 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
