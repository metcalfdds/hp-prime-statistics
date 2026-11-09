# StatDist v2.7l: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes StatDist v2.7l from StatDist v2.7k. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1, 2 and 3 reworded: the menus, the drag, the zoom keys and the three sets of soft keys in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 4 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, st_show_help 24.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 3 of 4 screens changed; 1 kept their words.

### Before (v2.7k)

```text
StatDist help 1/4: Gallery, touch and keys
Probabilities for 27 distributions.
Gallery: tap a family (or arrows),
Menus: the tail first, then the form.
Tap or drag in the plot = move x (k);
  on lift x snaps to the grid.
Left/Right = x by one grid step.
Up = upper tail, Down = lower tail;
  in a<X<b, Up = move b, Down = a.
+/- = zoom, 0 = refit the window.
Esc = back to the menu.
any key or tap = next page
```

```text
StatDist help 2/4: Soft keys, pages 1 and 2
Soft keys, page 1:
P≤x, P>x = which tail is shaded.
a<X<b: tap a, then tap b; after that
  a drag moves the nearer line.
Zoom-, Zoom+ = about x.
More (slot 6) = the next page:
Edit = the form (in a<X<b it resets
  a and b), Numbers = the numbers
  page, CDF = the S-curve, Approx /
  N(0,1) = the overlay (else Refit),
  Menu = back to the menu.
any key or tap = next page
```

```text
StatDist help 3/4: Soft keys, page 3; Ent
More again = page 3: Formula = the
  CAS works out E[X], E[X²], Var
  (and F(x) for Exponential, Weibull,
  Pareto; an exact P for discrete),
  each checked against the program;
  Help = these pages.
Ent = options: numbers page, Formula
  page, CDF, normal approx., N(0,1)
  behind t.
any key or tap = next page
```

### After (v2.7l)

```text
StatDist help 1/4: Gallery, touch and keys
Probabilities for 27 distributions.
Gallery: tap a family (or arrows), Then two menus:
choose the tail first, then fill in the form.
Tap or drag in the plot = move x (k); when you lift your
  finger, x moves to the nearest grid value.
Left/Right = x by one grid step.
Up = upper tail, Down = lower tail; in a<X<b, Up = move
  b, Down = a.
+/- = zoom, 0 = redraw the plot to fit.
Esc = back to the menu.
any key or tap = next page
```

```text
StatDist help 2/4: Soft keys, pages 1 and 2
Soft keys, page 1:
P≤x, P>x = which tail is shaded.
a<X<b: tap a, then tap b; after that a drag moves the
  nearer line.
Zoom-, Zoom+ = zoom out or in around x.
More (the 6th soft key) = the next set of keys:
Edit = the form (in a<X<b it resets a and b),
  Numbers = the numbers page, CDF = the S-curve, the
  4th key = Approx (the normal approximation, for the
  binomial and Poisson), N(0,1) (behind t), or Refit (the
  others), Menu = back to the menu.
any key or tap = next page
```

```text
StatDist help 3/4: Soft keys, page 3; Ent
More again = the third set of keys: Formula = the CAS
  works out E[X], E[X²], Var (and F(x) for Exponential,
  Weibull, Pareto; an exact P for discrete), each checked
  against the program's own numbers;
  Help = these pages.
Ent = options: numbers page, Formula page, CDF,
  normal approx., N(0,1) behind t.
any key or tap = next page
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in v2.7k; lint_ppl 4 problems, as in v2.7k (4); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 4 screens; one report: the harness cannot call st_ABHelp without its argument; its pages are checked through the menu.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
