# TestChooser beta 2g: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes TestChooser beta 2g from TestChooser beta 2f. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 and 2 reworded: "tiny n", "linked", "light it up", the corner box and the hatched cells in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 2 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, tcHelp1 11, tcHelp2 11.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 2 of 2 screens changed; 0 kept their words.

### Before (beta 2f)

```text
TestChooser help 1/2: Two questions
1. What kind of number is the OUTCOME?
   Interval/ratio: measurements, about
     normal → t-tests, ANOVA, regression.
   Nominal: categories → proportions,
     χ², odds ratios.
   Ordinal, or skewed, or tiny n → ranks:
     Mann-Whitney, Kruskal-Wallis ...
   Survival: time to event, some censored.
2. What is the DESIGN?  Different people
   per group, or the same people again?
   How many groups?  Two variables linked?
The table is from Glantz's Primer of
Biostatistics, with a one-sample column.
tap or Ent = page 2, Back = menu
```

```text
TestChooser help 2/2: Touch, keys and the quiz
Guide: tap a scale, then a design; the
  orange path ends at the test.  Tap the
  test (or Ent) for its details page.
  Back = up a level; ⇆⇅ and Ent work too.
Table: tap a cell to select it, tap it
  again (or Ent) for the details.  Tap a
  row name or a heading to light it up
  (+ = row, - = column).  The corner key
  shows the one-sample column.
Hatched cells: not on the Prime (R, JMP).
Quiz: read the case, tap its test.  Green
  = right; red = wrong, and the right
  cell is outlined in green.
tap or Ent = menu, Left = page 1
```

### After (beta 2g)

```text
TestChooser help 1/2: Two questions
1. What kind of number is the OUTCOME?
   Interval/ratio: measurements, about normal → t-tests, ANOVA,
     regression.
   Nominal: categories → proportions, χ², odds ratios.
   Ordinal, or skewed, or a very small n → ranks:
     Mann-Whitney, Kruskal-Wallis ...
   Survival: time to event, some censored.
2. What is the DESIGN?  Different people per group, or the same
   people again? How many groups?  Are two variables related?
The table follows Glantz's Primer of Biostatistics, with a column
added for one sample.
tap or Ent = page 2, Back = menu
```

```text
TestChooser help 2/2: Touch, keys and the quiz
Guide: tap a scale, then a design; the orange path ends at the
  test.  Tap the test (or Ent) for its details page. Back = up a level;
  ⇆⇅ and Ent work too.
Table: tap a cell to select it, tap it again (or Ent) for the details.
  Tap a row name or a column heading to highlight it (or + for
  the row, - for the column).  The box in the top-left corner
  switches to the one-sample column (so does Left from the
  first column).
Hatched cells: tests the Prime does not run (use R or JMP).
Quiz: read the case, tap its test.  Green = right; red = wrong, and
  the right cell is outlined in green.
tap or Ent = menu, Left = page 1
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 2f; lint_ppl 52 problems, as in beta 2f (52); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 2 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
