# RankLab beta 1h: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in RankLab beta 1g (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 2/7: one key per line again (Round 11's re-wrap had run "Up / Down" into "Left / Right", "turn pages" into "+", and "upper" into "0").  Help page 5/7: the halo preset is "the first 8 of those judges", the 43 judges of the line before, which "the same 8 judges" did not say.  And a fix the monkey found (base 12, 3 of 1,000 runs): Your data > Groups with fewer than two columns filled emptied the groups but kept the old group count, so a Mann-Whitney after it asked for a group name that was not there ("index out of range" in rk_ChooseG).  The columns are now read into locals, and the groups change only when there are two or more.

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of RankLab beta 1h that differ from RankLab beta 1g: line 17 (comment); lines 59-66 (comment); lines 2067-2070 (code); lines 2075-2077 (code); line 2084 (code); lines 3664-3669 (code); lines 3714-3715 (code); line 3765 (code). Routines whose code changed, with the number of lines: rk_MyData 8, rk_Help 8, rk_Welcome 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 2, before (beta 1g)

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

### Screen 2, after (beta 1h)

```text
RankLab help 2/7: Keys and touch
Up / Down = the previous / next page
Left / Right = pick the next dot, group, cell, point or pair
  (on the Null page: the read-out line; on Result: turn pages)
+ = the 4th soft key (Exact/Normal, ranks/values, rs/tau-b)
- = Tails: two-sided, lower, upper
0 = this help;  Enter = a menu of every action
Esc = back to the main menu (Quit is there)
Tap a dot, group, cell, point, bar or pair:
the panel says what it is, its value, group and midrank, and for a
tie which ranks were averaged.  The 4th soft key's label shows
which choice is on now.
Page 2/7: key = next, ← = back, Esc = leave
```

### Screen 5, before (beta 1g)

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

### Screen 5, after (beta 1h)

```text
RankLab help 5/7: Friedman, W, correlation
FRIEDMAN: rank within each block (row); Q compares the
treatments' rank sums, p from χ²(k - 1).  Kendall's
W = Q/(b(k - 1)): 0 = the blocks disagree, 1 = every block ranks
the treatments the same.
Judges: 43 judges (blocks) x 3 criteria. Halo preset: the first 8
of those judges on 11 criteria; W only, no p (the same lawyers
rated every criterion).
SPEARMAN rs = Pearson's r of the midranks;
exact p over all n! orders for n ≤ 7, else t.
KENDALL tau-b = (concordant - discordant)
pairs / √((n₀ - n₁)(n₀ - n₂)); exact p without ties (n ≤ 30), else z
(tie-corrected).
Lower (one-sided) tests for a negative association.
Page 5/7: key = next, ← = back, Esc = leave
```

## Checks

- `tools/ppl_gate_v1e.py` against RankLab beta 1g: PASS. lint_ppl 5 problems, as in RankLab beta 1g; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 7 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 82/1200 collisions 0 (firm 0) straddles 0 overruns 0 ghosts 0.
- The monkey (`tools/monkey_chunks_v1.py`, base 12, with `--lists`): 1000 of 1000 runs OK.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Help pages 2/7 and 5/7: one key per line; every line inside the page. Load the jury preset, then Your data > Groups with only D1 filled: refused with its sentence, and a Mann-Whitney afterwards still offers the jury's three groups.
