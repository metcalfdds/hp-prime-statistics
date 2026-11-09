# RankLab beta 1g: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes RankLab beta 1g from RankLab beta 1f. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1, 2, 5 and 6 reworded: "slot 4", the Halo preset, the exact p and the keys in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 7 screens, as the PC harness counts them.

3. **Outside the help** only these lines changed (the version on screen, and the page numbers the help's callers ask for):

```text
rk_Welcome     -  TEXTOUT_P("RankLab - rank tests, beta 1f", G1, 8, 4, 3, #FFFFFFh, 304);
rk_Welcome     +  TEXTOUT_P("RankLab - rank tests, beta 1g", G1, 8, 4, 3, #FFFFFFh, 304);
```

Routines touched, with the number of new or changed lines in each: (comments) 6, rk_Help 35, rk_Welcome 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 4 of 7 screens changed; 3 kept their words.

### Before (beta 1f)

```text
RankLab help 1/7: What it does
Rank tests replace each value by its rank,
so an outlier counts no more than the next
value, and no normal population is assumed.
Tied values share the average of the ranks
they span: the MIDRANK.  Every test here uses
midranks and the tie-corrected variance.
Each test opens on its Result page.  ⇅ turn
the pages: Result, a picture, the null
distribution (and Dunn pairs for Kruskal-
Wallis).  Soft keys: Result, Plot, Null,
slot 4 (Exact/Normal or the page's toggle),
Tails, More (Help, Dunn or Data, Menu).
Page 1/7: key = next, ← = back, Esc = leave
```

```text
RankLab help 2/7: Keys and touch
Up / Down = the previous / next page
Left / Right = pick the next dot, group,
cell, point or pair (on the Null page: move
the read-out line); on Result: turn pages
+ = slot 4 (Exact/Normal, ranks/values, rs/
tau-b);  - = Tails: two-sided, lower, upper
0 = this help;  Enter = a menu of every action
Esc = back to the main menu (Quit is there)
Tap a dot, group, cell, point, bar or pair:
the panel says what it is, its value, group
and midrank, and for a tie which ranks were
averaged.  Slot 4 shows what is on now.
Page 2/7: key = next, ← = back, Esc = leave
```

```text
RankLab help 5/7: Friedman, W, correlation
FRIEDMAN: rank within each block (row); Q
compares the treatments' rank sums, p from
χ²(k - 1).  Kendall's W = Q/(b(k - 1)): 0 =
the blocks disagree, 1 = all rank alike.
Judges: 43 judges (blocks) x 3 criteria. Halo:
11 criteria order 8 judges, W only (no p).
SPEARMAN rs = Pearson's r of the midranks;
exact p over all n! orders for n ≤ 7, else t.
KENDALL tau-b = (concordant - discordant)
pairs / √((n₀ - n₁)(n₀ - n₂)); exact p
without ties (n ≤ 30), else z (tie-corrected).
Lower = a negative association.
Page 5/7: key = next, ← = back, Esc = leave
```

```text
RankLab help 6/7: Exact or normal; the p-value
EXACT: p from the statistic's whole null
distribution, counted.  NORMAL: z with the
continuity correction (0.5 toward the mean)
and, with ties, the tie-corrected variance.
They agree better as n grows: compare them.
A p-value is P(a statistic this extreme | H₀),
not the chance that H₀ is true.  p ≥ 0.05
is no evidence of a difference, not proof
of none.
Two-sided: twice the smaller tail (max 1).
Lower / upper: one tail, chosen BEFORE the
data.  Kruskal-Wallis, Friedman: upper only.
Page 6/7: key = next, ← = back, Esc = leave
```

### After (beta 1g)

```text
RankLab help 1/7: What it does
Rank tests replace each value by its rank, so an outlier counts no
more than the next value, and no normal population is assumed.
Tied values share the average of the ranks they span: the
MIDRANK.  Every test here uses midranks and the
tie-corrected variance.
Each test opens on its Result page.  ⇅ turn the pages: Result, a
picture, the null distribution (and Dunn pairs for Kruskal-
Wallis).  Soft keys: Result, Plot, Null, the 4th key (Exact/Normal,
or what that page switches), Tails, More (Help, Dunn or
Data, Menu).
Page 1/7: key = next, ← = back, Esc = leave
```

```text
RankLab help 2/7: Keys and touch
Up / Down = the previous / next page Left / Right = pick the next
dot, group, cell, point or pair (on the Null page: move the
read-out line); on Result: turn pages + = the 4th soft key
(Exact/Normal, ranks/values, rs/tau-b);  - = Tails: two-sided,
lower, upper 0 = this help;  Enter = a menu of every action
Esc = back to the main menu (Quit is there)
Tap a dot, group, cell, point, bar or pair:
the panel says what it is, its value, group and midrank, and for a
tie which ranks were averaged.  The 4th soft key's label shows
which choice is on now.
Page 2/7: key = next, ← = back, Esc = leave
```

```text
RankLab help 5/7: Friedman, W, correlation
FRIEDMAN: rank within each block (row); Q compares the
treatments' rank sums, p from χ²(k - 1).  Kendall's
W = Q/(b(k - 1)): 0 = the blocks disagree, 1 = every block ranks
the treatments the same.
Judges: 43 judges (blocks) x 3 criteria. Halo preset: the same 8
judges ranked on 11 criteria; W only, no p (the same lawyers
rated every criterion).
SPEARMAN rs = Pearson's r of the midranks;
exact p over all n! orders for n ≤ 7, else t.
KENDALL tau-b = (concordant - discordant)
pairs / √((n₀ - n₁)(n₀ - n₂)); exact p without ties (n ≤ 30), else z
(tie-corrected).
Lower (one-sided) tests for a negative association.
Page 5/7: key = next, ← = back, Esc = leave
```

```text
RankLab help 6/7: Exact or normal; the p-value
EXACT: p from the statistic's whole null distribution, counted.
NORMAL: z with the continuity correction (0.5 toward the mean)
and, with ties, the tie-corrected variance.
They agree better as n grows: compare them.
A p-value is P(a statistic this extreme | H₀), not the chance that
H₀ is true.  p ≥ 0.05 means no evidence of a difference; it is not
proof that there is none.
Two-sided: twice the smaller tail (max 1).
Lower / upper: one tail, chosen BEFORE the data.  Kruskal-Wallis,
Friedman: upper only.
Page 6/7: key = next, ← = back, Esc = leave
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1f; lint_ppl 5 problems, as in beta 1f (5); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 7 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
