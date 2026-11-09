# ScatterLab beta 2j: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes ScatterLab beta 2j from ScatterLab beta 2i. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help page 2 reworded: "the squared misses" in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 6 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, slHelpPg 7.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 1 of 6 screens changed; 5 kept their words.

### Before (beta 2i)

```text
ScatterLab help 2/6: r², the share explained
All variation in y: SST = sum (y - ȳ)²,
the squared misses of the flat line at ȳ.
What the line leaves: SSE = sum (y - ŷ)².
r² = 1 - SSE / SST: the share of the variation
in y that the line accounts for.  r² = 0.64
means 64% explained and 36% left over in
the residuals.  (It is also r times r.)
Try it: Guess starts flat, at ȳ, so
'your SSE' starts at SST.  The best line
brings it down to SSE; the drop, as a share
of SST, is r².
2/6  ←→ or tap = page, Esc = plot
```

### After (beta 2j)

```text
ScatterLab help 2/6: r², the share explained
All variation in y: SST = sum (y - ȳ)², the squared distances of
the points from the flat line at ȳ.
What the line leaves: SSE = sum (y - ŷ)².
r² = 1 - SSE / SST: the share of the variation in y that the line
accounts for.  r² = 0.64 means 64% explained and 36% left over
in the residuals.  (It is also r times r.)
Try it: Guess starts flat, at ȳ, so 'your SSE' starts at SST.  The best
line brings it down to SSE; the drop, as a share of SST, is r².
2/6  ←→ or tap = page, Esc = plot
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 2i; lint_ppl 9 problems, as in beta 2i (9); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 6 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
