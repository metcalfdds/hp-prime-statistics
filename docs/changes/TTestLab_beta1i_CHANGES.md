# TTestLab beta 1i: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes TTestLab beta 1i from TTestLab beta 1h. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 and 2 reworded: the soft keys named, the menu items listed, the pairs in D1 and D2 explained, and "as the lecture" dropped (Roger, 9 Nov 2026).

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 2 screens, as the PC harness counts them. A statistic's name stays on one line: the first layout broke "3 crit (t" / "crit)"; the wrap now keeps a one-letter symbol with the "crit", "obt" or "obs" after it.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, tt_Help 20.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 2 of 2 screens changed; 0 kept their words.

### Before (beta 1h)

```text
TTestLab help 1/2: Keys
SOFT KEYS:  1 H, 2 df, 3 crit, 4 t, 5 end = the
five steps;  Menu = the menu
Left / Right = a step back / on
Enter = menu,  Esc = quit
MENU: edit the numbers, tails and α, pooled or
separate side by side, choose the test, examples
The flowchart: tap Yes or No; Run = run the test
Your own scores: Apps, Statistics 1Var, Num:
sample 1 (or x₁) in D1, sample 2 (or x₂) in D2
Teaching aid; not for clinical or legal use.
any key or tap = next page
```

```text
TTestLab help 2/2: The numbers
t crit: exact for your df, and the printed
table's row (df 73 -> row 60, as the lecture)
Step 4 keeps 4 significant digits on the way;
rounding sooner can move t obt (see example 1)
Separate variances: SE = √(s₁²/N₁ + s₂²/N₂),
Welch-Satterthwaite df, as SPSS
Group 1 minus group 2, as the lecture and SPSS
p, two-tailed, is SPSS's "Sig. (2-tailed)"
Cohen's d: pooled s (independent); sD (pairs)
Check on the Prime: Inference app, Hyp. test,
T-Test: μ₁-μ₂ (Pooled checked = pooled).  Pairs:
T-Test: 1 μ on the differences, with μ₀ = 0.
any key or tap = back
```

### After (beta 1i)

```text
TTestLab help 1/2: Keys
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
Teaching aid; not for clinical or legal use.
any key or tap = next page
```

```text
TTestLab help 2/2: The numbers
t crit: the exact value for your df, and the printed table's value (a
df the table lacks uses the next smaller row: df 73 uses row 60)
Step 4 keeps 4 significant digits at each step; rounding sooner
can change t obt (see example 1)
Separate variances: SE = √(s₁²/N₁ + s₂²/N₂), Welch-Satterthwaite
df, as SPSS prints them
The difference is group 1 minus group 2, as in SPSS
p, two-tailed, is SPSS's "Sig. (2-tailed)"
Cohen's d divides by the pooled s (two groups) or by sD (pairs)
Check on the Prime: Inference app, Hyp. test, T-Test: μ₁-μ₂ (tick
Pooled for the pooled test).  Pairs:
T-Test: 1 μ on the differences, with μ₀ = 0.
any key or tap = back
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1h; lint_ppl 4 problems, as in beta 1h (4); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 2 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
