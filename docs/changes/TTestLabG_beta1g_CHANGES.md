# TTestLabG beta 1g: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes TTestLabG beta 1g from TTestLabG beta 1f. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 and 2 reworded: the soft keys named, the menu items listed, the pairs in D1 and D2 explained, and the printed-table rule in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 2 screens, as the PC harness counts them. A statistic's name stays on one line: the first layout broke "3 crit (t" / "crit)"; the wrap now keeps a one-letter symbol with the "crit", "obt" or "obs" after it.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, tz_Help 21.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 2 of 2 screens changed; 0 kept their words.

### Before (beta 1f)

```text
TTestLabG help 1/2: Keys
SOFT KEYS:  1 H, 2 df, 3 crit, 4 t, 5 end = the
five steps;  Menu = the menu
Left / Right = a step back / on
Enter = menu,  Esc = quit
MENU: edit the numbers, tails and α, pooled or
separate side by side, choose the test, examples
The flowchart: tap Yes or No; Run = run the test
Your own scores: Apps, Statistics 1Var, Num:
sample 1 (or x₁) in D1, sample 2 (or x₂) in D2
A long data set: DataLoad fills D1 and D2.
Teaching aid; not for clinical or legal use.
any key or tap = next page
```

```text
TTestLabG help 2/2: The numbers
t crit: exact for your df; no table is needed.
A printed table: a df it lacks, the next smaller
row; a fractional df, rounded down first.
Step 4 keeps 4 significant digits on the way.
Separate variances (the default): Welch's SE
and df, as SPSS and R print them
Group 1 minus group 2, as SPSS and R do
p, two-tailed, is SPSS's "Sig. (2-tailed)"
Cohen's d: pooled s (independent); sD (pairs)
Check on the Prime: Inference app, Hyp. test,
T-Test: μ₁-μ₂ (Pooled checked = pooled).  Pairs:
T-Test: 1 μ on the differences, with μ₀ = 0.
any key or tap = back
```

### After (beta 1g)

```text
TTestLabG help 1/2: Keys
SOFT KEYS: the five steps, 1 H (the hypotheses), 2 df, 3 crit
(t crit), 4 t (t obt), 5 end (the decision);  Menu = the menu
Left / Right = the step before / the next step
Enter = menu,  Esc = quit
MENU: Edit the numbers; Tails and α; Pooled or separate? (the
two tests side by side); Choose the test; Examples
The flowchart: tap Yes or No; Run = run the test
Your own scores: Apps, Statistics 1Var, Num:
sample 1 in D1 and sample 2 in D2 (for pairs, each pair's x₁ in
D1 and its x₂ in D2)
A long data set: DataLoad fills D1 and D2.
Teaching aid; not for clinical or legal use.
any key or tap = next page
```

```text
TTestLabG help 2/2: The numbers
t crit: exact for your df; no table is needed.
With a printed table, a df it lacks uses the next smaller row, and
a fractional df is rounded down first.
Step 4 keeps 4 significant digits at each step.
Separate variances (the default): Welch's SE and df, as SPSS and
R print them
The difference is group 1 minus group 2, as in SPSS and R
p, two-tailed, is SPSS's "Sig. (2-tailed)"
Cohen's d divides by the pooled s (two groups) or by sD (pairs)
Check on the Prime: Inference app, Hyp. test, T-Test: μ₁-μ₂ (tick
Pooled for the pooled test).  Pairs:
T-Test: 1 μ on the differences, with μ₀ = 0.
any key or tap = back
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1f; lint_ppl 4 problems, as in beta 1f (4); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 2 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
