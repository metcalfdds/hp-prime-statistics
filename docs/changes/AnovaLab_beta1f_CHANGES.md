# AnovaLab beta 1f: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes AnovaLab beta 1f from AnovaLab beta 1e. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 2, 3, 4 and 7 reworded: Levene's "robust" and Bartlett's "misled" explained, Holm and Scheffe in words, Type III SS and effect coding in words, and the Home variables listed one by one.  The help is now 9 pages (was 8).

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is 9 screens (was 8), as the PC harness counts them.

3. **Outside the help** only these lines changed (the version on screen, and the page numbers the help's callers ask for):

```text
av_BView       -    IF bvA == 9 THEN av_Help(5); END;
av_BView       +    IF bvA == 9 THEN av_Help(6); END;
av_Hello       -  av_Band("AnovaLab - beta 1e");
av_Hello       +  av_Band("AnovaLab - beta 1f");
av_TView       -    IF tvA == 9 THEN av_Help(4); END;
av_TView       +    IF tvA == 9 THEN av_Help(5); END;
av_VView       -    IF vvA == 9 THEN av_Help(6); END;
av_VView       +    IF vvA == 9 THEN av_Help(7); END;
```

Routines touched, with the number of new or changed lines in each: (comments) 8, av_BView 1, av_Hello 1, av_Help 2, av_HelpPage 55, av_TView 1, av_VView 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 5 of 9 screens changed; 4 kept their words (4 of them with a new page number).

### Before (beta 1e)

```text
AnovaLab help 2/8: Welch and the checks
The F test assumes equal spreads (and roughly
normal groups).  Welch's F (1951) drops equal
spreads: each group is weighted by n / s².
Levene's test (Brown-Forsythe form) runs the
one-way F on |value - group median|: robust.
Bartlett's χ² compares the s² directly: it is
misled by non-normal data.
Insect sprays: s runs from 1.7 to 6.2, Levene
flags it; compare the ordinary F with Welch's.
A check that is not significant is not proof
of equal spreads: small groups miss a lot.
Dots page: look at the spreads yourself.
Any key or tap = next, ← = back, Esc = leave
```

```text
AnovaLab help 3/8: Which pairs differ?
Many t-tests inflate the chance of a false
alarm; these keep it at α for the family:
Tukey-Kramer: q = |diff|/√(MSW/2 (1/n₁+1/n₂))
  on the studentized range (asks first: slow).
Bonferroni: raw t p × m pairs (simple, safe).
Holm: step-down Bonferroni, never less power.
Scheffe: covers every contrast, widest CIs.
CIs are simultaneous (family 95%).
Pairs page: +/- or a tab = method; tap a pair.
Dots page: tap two groups, or ←→ for the next
pair.  More > Tukey p: every pair's Tukey p.
Tukey vs SciPy: q crit within 0.03 %, pair p
within 0.00001 (k 2-12, df 3-1,000, α .1-.001).
Any key or tap = next, ← = back, Esc = leave
```

```text
AnovaLab help 4/8: Two-way ANOVA
Two factors A and B, every A × B cell filled.
Main effects: do A's (or B's) levels differ?
Interaction: does A's effect depend on B?
Unequal cells (unbalanced): Type III SS,
by regression, effect coding: each effect
is tested after all the others.  They need not
add up to the total.  Balanced: classical SS.
Plot: one line per level of the other factor.
Parallel lines = no interaction.  Tap a point
for its cell mean and n; Swap turns the plot.
Mock jury: unattractive swindlers: 7.0 years;
other cells 3.5 to 4.8: striking, yet the
interaction's p is 0.13 (cells of 17 to 21).
Any key or tap = next, ← = back, Esc = leave
```

```text
AnovaLab help 7/8: Your data, and Home
Statistics 1Var app, lists D1-D9:
One-way: each non-empty list is a group.
Two-way: D1 = y, D2 = A codes, D3 = B codes
  (any numbers; 2 to 6 levels each).
Blocks: each list a treatment, one row per
  block (all lists the same length).
Home: AV_F, AV_P, AV_DF, AV_MSE, AV_ETA2 of the
last run (A×B; blocks: treatments); AV_TAB.
Soft keys: More turns to more keys (one-way).
Enter = a menu of every action; Esc = back.
Every tap has a key: ←→ ⇅ +/- Enter Esc.
p = P(data this extreme | H₀), not P(H₀).
Any key or tap = next, ← = back, Esc = leave
```

### After (beta 1f)

```text
AnovaLab help 2/9: Welch and the checks
The F test assumes equal spreads (and roughly normal groups).
Welch's F (1951) drops equal spreads: each group is weighted
by n / s².
Levene's test (Brown-Forsythe form) runs the one-way F on
|value - group median|; non-normal data affect it little.
Bartlett's χ² compares the s² directly: it is misled by
non-normal data.
In the insect-spray preset, s runs from 1.7 to 6.2 and Levene's
test flags it; compare the ordinary F with Welch's.
A check that is not significant is not proof of equal spreads: with
small groups the checks often miss real differences.
Dots page: look at the spreads yourself.
Any key or tap = next, ← = back, Esc = leave
```

```text
AnovaLab help 3/9: Which pairs differ?
Many t-tests raise the chance of at least one false alarm; these
keep that chance at α for the whole set (the family):
Tukey-Kramer: q = |diff|/√(MSW/2 (1/n₁+1/n₂)) on the
  studentized range (it asks before it runs, since it is slow).
Bonferroni: raw t p × m pairs (simple, safe).
Holm: Bonferroni done in steps; never less power than
Bonferroni.
Any key or tap = next, ← = back, Esc = leave
```

```text
AnovaLab help 4/9: Which pairs differ? (continued)
Scheffe: covers every contrast, widest CIs.
CIs are simultaneous (family 95%).
Pairs page: +/- or a tab = method; tap a pair.
Dots page: tap two groups, or ←→ for the next pair.
More > Tukey p: every pair's Tukey p.
Tukey vs SciPy: q crit within 0.03 %, pair p within 0.00001 (k
2-12, df 3-1,000, α .1-.001).
Any key or tap = next, ← = back, Esc = leave
```

```text
AnovaLab help 5/9: Two-way ANOVA
Two factors A and B, every A × B cell filled.
Main effects: do A's (or B's) levels differ?
Interaction: does A's effect depend on B?
Unequal cells (unbalanced): Type III SS, by regression, effect
coding: each effect is tested after all the others.  They need not
add up to the total.  Balanced: classical SS.
Plot: one line per level of the other factor.
Parallel lines = no interaction.  Tap a point for its cell mean and
n; Swap exchanges the two factors in the plot.
Mock-jury preset: unattractive swindlers got 7.0 years on
average, the other cells 3.5 to 4.8; striking, yet the interaction's p
is 0.13 (17 to 21 jurors a cell).
Any key or tap = next, ← = back, Esc = leave
```

```text
AnovaLab help 8/9: Your data, and Home
Statistics 1Var app, lists D1-D9:
One-way: each non-empty list is a group.
Two-way: D1 = y, D2 = A codes, D3 = B codes (any numbers;
  2 to 6 levels each).
Blocks: each list a treatment, one row per block (all lists the
  same length).
Home: AV_F, AV_P, AV_DF, AV_MSE, AV_ETA2 of the last run (A×B;
blocks: treatments); AV_TAB.
Soft keys: More shows the next set of soft keys (one-way).
Enter = a menu of every action; Esc = back.
Every tap has a key: ←→ ⇅ +/- Enter Esc.
p = P(data this extreme | H₀), not P(H₀).
Any key or tap = next, ← = back, Esc = leave
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1e; lint_ppl 5 problems, as in beta 1e (5); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 9 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".
- `tools/monkey_v1b.py --lists`, 1,000 runs of 120 random keys, taps, menu picks and typed values (333 s): OK 1,000.

Not yet run on a G1 or a G2.
