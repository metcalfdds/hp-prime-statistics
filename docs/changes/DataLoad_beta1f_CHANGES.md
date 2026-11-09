# DataLoad beta 1f: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes DataLoad beta 1f from DataLoad beta 1e. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help page 1 reworded: "the fleet's programs" is now "our programs".

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 3 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, dd_Help 5.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 1 of 3 screens changed; 2 kept their words.

### Before (beta 1e)

```text
DataLoad help 1/3: What it does
Copies the columns of a matrix (M0-M9) into
the lists the fleet's programs read: D1-D9 of
Statistics 1Var, or C1-C9 of Statistics 2Var.
COLUMNS: column 1 to D1, column 2 to D2, ...
SCORES BY GROUP: a column of scores and one of
group codes, as SPSS keeps them; each group's
scores to its own list, lowest code to D1.
Blank cells (9.99999999999E499) are left out.
Then the lists: tap a row for its histogram.
Quartiles as the Prime's Statistics 1Var: the
median of each half (odd n: median left out).
any key or tap = next page
```

### After (beta 1f)

```text
DataLoad help 1/3: What it does
Copies the columns of a matrix (M0-M9) into the lists our
programs read: D1-D9 of Statistics 1Var, or C1-C9 of
Statistics 2Var.
COLUMNS: column 1 to D1, column 2 to D2, ...
SCORES BY GROUP: a column of scores and one of
group codes, as SPSS keeps them; each group's
scores to its own list, lowest code to D1.
Blank cells (9.99999999999E499) are left out.
Then the lists: tap a row for its histogram.
Quartiles as the Prime's Statistics 1Var: the median of each half
(odd n: median left out).
any key or tap = next page
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1e; lint_ppl 4 problems, as in beta 1e (4); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 3 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
