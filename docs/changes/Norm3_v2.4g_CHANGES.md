# Norm3 v2.4g: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes Norm3 v2.4g from Norm3 v2.4f. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Its help page reworded: "snaps" and "its quantile" in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 1 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, n3_Help 8.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 1 of 1 screens changed; 0 kept their words.

### Before (v2.4f)

```text
Normal  μ = 0.000, σ = 1.000
Norm3 help: Touch and keys
x₀ = 1.96, z = 1.96, pdf = 0.0584 (a height)
P(X ≤ x₀) = 0.9750
P(X > x₀) = 0.0250
TOUCH (in the plot)
1
Drag: x₀ follows your finger, with the blue
  area, both P values and the magenta point.
0.5
  Lift: x₀ snaps to a round value.
Press ON the magenta S-curve, or on the 0-1
0.4
  axis at the right: p is that height and
  x₀ its quantile. Drag up the curve to 0.900.
0.3
Press on the green dotted μ line: drag the mean.
.5
KEYS
0.2
Soft keys: μ− μ+ σ− σ+, View (4 views), Quit
⇆ = μ, ⇅ = σ (animated), +/- = x₀,
0.1
0 = re-center, Ent = menu, Esc = quit
READING IT
0
Blue = P(X ≤ x₀), light red = P(X > x₀).
x
-4
-3
-2
-1
0
1
2
3
4
The pdf is a HEIGHT, not a probability.
z
-3
-2
-1
0
1
2
3
tap or press any key to return
```

### After (v2.4g)

```text
Normal  μ = 0.000, σ = 1.000
Norm3 help: Touch and keys
x₀ = 1.96, z = 1.96, pdf = 0.0584 (a height)
P(X ≤ x₀) = 0.9750
P(X > x₀) = 0.0250
TOUCH (in the plot)
1
Drag: x₀ follows your finger, with the blue area, both P values and
  the magenta point. When you lift your finger, x₀ moves to the
0.5
  nearest round value.
Press ON the magenta S-curve, or on the 0-1 axis at the right: p
0.4
  is that height, and x₀ is the value with area p to its left. Drag up
  the curve to 0.900, for example.
0.3
Press on the green dotted μ line: drag the mean.
.5
KEYS
0.2
Soft keys: μ− μ+ σ− σ+, View (4 views), Quit
⇆ = μ, ⇅ = σ (animated), +/- = x₀, 0 = re-center, Ent = menu,
0.1
Esc = quit
READING IT
0
Blue = P(X ≤ x₀), light red = P(X > x₀).
x
-4
-3
-2
-1
0
1
2
3
4
The pdf is a HEIGHT, not a probability.
z
-3
-2
-1
0
1
2
3
tap or press any key to return
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in v2.4f; lint_ppl 4 problems, as in v2.4f (4); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py` (the old help with the approved changes applied, word for word against the new): the only difference is where the plot's axis numbers fall in the dump (the help is drawn over the plot, which the harness keeps underneath).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 1 screens; the reports are the plot's axis numbers and readouts, which the harness keeps underneath the help; the help clears the screen with a filled RECT_P first, so on the calculator they are not there.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
