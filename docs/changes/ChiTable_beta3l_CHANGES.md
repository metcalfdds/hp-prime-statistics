# ChiTable beta 3l: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes ChiTable beta 3l from ChiTable beta 3k. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1, 3 and 5 reworded: the expected count, the alpha steps and the exact answers in plain words.  The help is now 6 pages (was 5).

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is 6 screens (was 5), as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, csDfPage 2, csHelp 51.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 5 of 6 screens changed; 1 kept their words (1 of them with a new page number).

### Before (beta 3k)

```text
ChiTable help 1/5: χ² for a two-way table
Pick a table shape, then tap each cell and type
its OBSERVED count.  Run computes everything.
Expected count E = row total x col total / N:
what the cell would hold if the two variables
were independent.  χ² adds (O - E)² / E over
the cells: a big χ² means a big surprise.
df = (rows - 1)(cols - 1).  p is the right tail
of the χ² curve, drawn by the curve plot.
Assumption: every expected count is 5 or more
(the pages flag any E below 5).  If not: use
Fisher's exact (2x2) or merge sparse categories.
Pages: O and E, percentages, the test, the cell
contributions, meaning, 2x2, exact answers.
Any key = page 2
```

```text
ChiTable help 3/5: Touch, soft keys and plots
Soft keys on the results pages and plots: Prev
and Next turn the page (or go to the next plot);
Bars, Mosaic, Curve jump there.  Menu: ×10 N,
N / 10 (V stays, p moves), Restore the counts.
Bars: drag a SOLID bar up or down -- every pale
E bar moves, χ² and p follow; Up / Down do it too.
Mosaic: Morph (or +) melts O into E: H₀ itself.
Curve: drag the red dotted line to set α; near
.001 .005 .01 .02 .05 .10 .20 it snaps to them;
← → step that ladder; Reset = 0.05.
Results page 1: tap a cell to see how E is made.
Residual plot: one bar per cell, dotted at ±2.
Fisher plot (2×2): every table with these
margins; red = yours, red + magenta = p.
Any key = page 4
```

```text
ChiTable help 4/5: Why df = (r - 1)(c - 1)
Col 1
Col 2
Total
free
Row 1
forced
fixed
Row 2
forced
forced
fixed
Total
fixed
fixed
N
df = (2 - 1)(2 - 1) = 1: fill this white cell
and the rest follow.  With every total fixed, a
gray cell is its row (or column) total minus the
cells beside it: only df counts are free to vary.
Any key = page 5
```

```text
ChiTable help 5/5: Exact answers (CAS)
Results page 6, the last page and the Fisher
plot ask the CAS for EXACT answers on your own
counts: χ² as one fraction (from N(ad - bc)²
/ (r1 r2 c1 c2) for a 2×2, or from the sum of
(O - E)²/E), and Fisher's p as a fraction.
Fisher's test is COUNTING: with the totals
fixed, top-left count a happens in C(r1,a)
C(r2,c1-a) of the C(N,c1) equally likely ways.
Add the tables no likelier than yours.  Tea
tasting [[3,1],[1,3]]: 34 of 70, p = 17/35.
Badge 'exact (CAS)': the CAS worked it out.
'decimal': it could not, or the fraction is
too long: you see the program's own decimal.
Any key = menu
```

### After (beta 3l)

```text
ChiTable help 1/6: χ² for a two-way table
Pick a table shape, then tap each cell and type its OBSERVED
count.  Run computes everything.
Expected count E = row total x col total / N:
what the cell would hold if the two variables were independent.
χ² adds (O - E)² / E over the cells: a big χ² means the counts are
far from what independence predicts.
df = (rows - 1)(cols - 1).  p is the right tail of the χ² curve, drawn
by the curve plot.
Assumption: every expected count is 5 or more (the pages flag
any E below 5).  If not: use Fisher's exact (2x2) or merge sparse
categories.
Pages: O and E, percentages, the test, the cell contributions,
meaning, 2x2, exact answers.
Any key = page 2
```

```text
ChiTable help 3/6: Touch, soft keys and plots
Soft keys on the results pages and plots: Prev and Next turn the
page (or go to the next plot);
Bars, Mosaic, Curve jump there.  Menu: ×10 N, N / 10 (Cramér's
V stays the same; p changes), Restore the counts.
Bars: drag a SOLID bar up or down -- every pale E bar moves, χ²
and p follow; Up / Down do it too.
Mosaic: Morph (or +) changes the observed counts, step by
step, into the expected counts: what the table would look like if
H₀ were true.
Any key = page 4
```

```text
ChiTable help 4/6: Touch, keys, plots (continued)
Curve: drag the red dotted line to set α; near .001 .005 .01 .02
.05 .10 .20 it jumps to the nearest one; ← → step through those
values; Reset = 0.05.
Results page 1: tap a cell to see how E is made.
Residual plot: one bar per cell, dotted at ±2.
Fisher plot (2×2): every table with these margins; red = yours,
red + magenta = p.
Any key = page 5
```

```text
ChiTable help 5/6: Why df = (r - 1)(c - 1)
Col 1
Col 2
Total
free
Row 1
forced
fixed
Row 2
forced
forced
fixed
Total
fixed
fixed
N
df = (2 - 1)(2 - 1) = 1: fill this white cell
and the rest follow.  With every total fixed, a
gray cell is its row (or column) total minus the
cells beside it: only df counts are free to vary.
Any key = page 6
```

```text
ChiTable help 6/6: Exact answers (CAS)
Results page 6, the last page and the Fisher plot ask the CAS for
EXACT answers on your own counts: χ² as one fraction (from
N(ad - bc)² / (r1 r2 c1 c2) for a 2×2, or from the sum of
(O - E)²/E), and Fisher's p as a fraction.
Fisher's test is COUNTING: with the totals fixed, top-left count a
happens in C(r1,a) C(r2,c1-a) of the C(N,c1) equally likely ways.
p adds up the chances of every table no more likely than yours.
Tea tasting [[3,1],[1,3]]: 34 of 70, p = 17/35.
Badge 'exact (CAS)': the CAS worked it out.
'decimal': it could not, or the fraction is too long: you see the
program's own decimal.
Any key = menu
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 3k; lint_ppl 8 problems, as in beta 3k (8); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 6 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".
  On the Virtual Calculator all six help pages were opened from the menu and read (`verify/round11/screens/`): every line inside its page, nothing cut.
- `tools/monkey_v1b.py --lists`, 1,000 runs of 120 random keys, taps, menu picks and typed values (166 s): OK 1,000.

Not yet run on a G1 or a G2.
