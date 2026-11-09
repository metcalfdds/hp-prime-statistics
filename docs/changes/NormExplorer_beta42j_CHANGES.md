# NormExplorer beta 42j: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes NormExplorer beta 42j from NormExplorer beta 42i. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 2 and 3 reworded: "turns the page", the second set of soft keys, "held" and the drag in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 3 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, ne_HelpPages 12.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 2 of 3 screens changed; 1 kept their words.

### Before (beta 42i)

```text
NormExplorer help 2/3: Explorer soft keys
EXPLORER SOFT KEYS  (More turns the page)
Bands
68-95-99.7 bands on or off  (+)
Ref
N(0,1) → CDF S-curve → none  (−)
Center
re-center the window  (0)
Shade
left, right, between, outside, none
Hist
then tap a bar for its counts
PAGE 2: WHAT ← → MOVE
Bnd A, B
the lower bound (or x₀), the upper
μ, σ
μ; or σ, ← narrower → wider
Menu
back to the menu  (Esc, Enter)
Tap the chosen key again for the usual:
← → move μ, ↑ ↓ change σ, in round steps.
The window is held while you explore.
any key or tap = next page
```

```text
NormExplorer help 3/3: Touch in the Explorer
TOUCH IN THE EXPLORER
Tap or drag in the plot: the cut x₀ moves;
  with two bounds, the nearer one moves.
Press on the μ line and drag sideways: μ.
Press a small square (μ ± σ), drag outward:
  σ widens.  Lifting snaps μ and σ.
The area rides the shaded region; the
  height at x₀ is a density, not an area.
RESULT VIEWS
Tap the plot: explore it, shading kept.
Tap a histogram bar: its counts.
HOME: NE_Z, NE_X, NE_P keep the last result.
any key or tap = back to the menu
```

### After (beta 42j)

```text
NormExplorer help 2/3: Explorer soft keys
EXPLORER SOFT KEYS  (More shows the second set)
Bands
68-95-99.7 bands on or off  (+)
Ref
N(0,1) → CDF S-curve → none  (−)
Center
re-center the window  (0)
Shade
left, right, between, outside, none
Hist
then tap a bar for its counts
SECOND SET OF KEYS: WHAT ← AND → MOVE
Bnd A, B
A = the lower bound (or x₀), B = the upper
μ, σ
μ = the mean; σ = ← narrower, → wider
Menu
back to the menu  (Esc, Enter)
Tap the chosen key again to go back to the usual keys:
← → move μ, ↑ ↓ change σ, in round steps.
The plot's window stays fixed while you explore.
any key or tap = next page
```

```text
NormExplorer help 3/3: Touch in the Explorer
TOUCH IN THE EXPLORER
Tap or drag in the plot: the cut x₀ moves; with two bounds,
  the nearer one moves.
Press on the μ line and drag sideways: μ.
Press a small square (μ ± σ), drag outward: σ widens.  When
  you lift your finger, μ and σ move to round values.
The area's value is printed on the shaded region; the height
  at x₀ is a density, not an area.
RESULT VIEWS
Tap the plot: explore it, shading kept.
Tap a histogram bar: its counts.
HOME: NE_Z, NE_X, NE_P keep the last result.
any key or tap = back to the menu
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 42i; lint_ppl 69 problems, as in beta 42i (69); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 3 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
