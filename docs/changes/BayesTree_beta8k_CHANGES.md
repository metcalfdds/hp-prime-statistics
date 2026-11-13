# BayesTree beta 8k: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in BayesTree beta 8j (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 2/5: the three sets of soft keys on lines of their own, each key named as its label reads ("Test 2", not "Test2"), and "Esc quits BayesTree." in one piece.

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of BayesTree beta 8k that differ from BayesTree beta 8j: line 4 (comment); lines 26-29 (comment); lines 2657-2662 (code). Routines whose code changed, with the number of lines: bt_HelpView 6.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 2, before (beta 8j)

```text
BayesTree help 2/5: The tree (continued)
Mosaic: green TP, red FN, orange FP, gray TN.
Leaf bars: each leaf's share of N (a share below 1 % gets a short
bar on a log scale).
Soft keys: More (the 6th key) shows the next set of keys: Values
  Counts ROC PPV 2×2 | Diag Fagan Icons 3 prev Help | Test2
  Reset Forens Leaves Exact.
⇆ = spec, ⇅ = sens, +/- = prior, Ent = menu, Esc quits
BayesTree.
any key or tap = next page, Esc = done
```

### Screen 2, after (beta 8k)

```text
BayesTree help 2/5: The tree (continued)
Mosaic: green TP, red FN, orange FP, gray TN.
Leaf bars: each leaf's share of N (a share below 1 % gets a short
bar on a log scale).
Soft keys: More (the 6th key) shows the next set of keys:
  Values, Counts, ROC, PPV, 2×2
  Diag, Fagan, Icons, 3 prev, Help
  Test 2, Reset, Forens, Leaves, Exact
⇆ = spec, ⇅ = sens, +/- = prior, Ent = menu,
Esc quits BayesTree.
any key or tap = next page, Esc = done
```

## Checks

- `tools/ppl_gate_v1e.py` against BayesTree beta 8j: PASS. lint_ppl 4 problems, as in BayesTree beta 8j; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 5 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 101/486 collisions 16 (firm 13) straddles 0 overruns 21 ghosts 0.
- The monkey (`tools/monkey_chunks_v1.py`, base 12, with `--lists`): 1000 of 1000 runs OK.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Help page 2/5: the three sets of soft keys on three lines.
