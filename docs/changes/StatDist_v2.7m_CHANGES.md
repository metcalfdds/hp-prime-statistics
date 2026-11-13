# StatDist v2.7m: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in StatDist v2.7l (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 1/4: "then", not "Then", after a comma.

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of StatDist v2.7m that differ from StatDist v2.7l: line 4 (comment); lines 38-39 (comment); line 3131 (code). Routines whose code changed, with the number of lines: st_show_help 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 1, before (v2.7l)

```text
StatDist help 1/4: Gallery, touch and keys
Probabilities for 27 distributions.
Gallery: tap a family (or arrows), Then two menus:
choose the tail first, then fill in the form.
Tap or drag in the plot = move x (k); when you lift your
  finger, x moves to the nearest grid value.
Left/Right = x by one grid step.
Up = upper tail, Down = lower tail; in a<X<b, Up = move
  b, Down = a.
+/- = zoom, 0 = redraw the plot to fit.
Esc = back to the menu.
any key or tap = next page
```

### Screen 1, after (v2.7m)

```text
StatDist help 1/4: Gallery, touch and keys
Probabilities for 27 distributions.
Gallery: tap a family (or arrows), then two menus:
choose the tail first, then fill in the form.
Tap or drag in the plot = move x (k); when you lift your
  finger, x moves to the nearest grid value.
Left/Right = x by one grid step.
Up = upper tail, Down = lower tail; in a<X<b, Up = move
  b, Down = a.
+/- = zoom, 0 = redraw the plot to fit.
Esc = back to the menu.
any key or tap = next page
```

## Checks

- `tools/ppl_gate_v1e.py` against StatDist v2.7l: PASS. lint_ppl 4 problems, as in StatDist v2.7l; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 4 screens, one known report: call st_ABHelp: st_ABHelp takes 1 arguments, got 0.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 23/228 collisions 11 (firm 11) straddles 0 overruns 0 ghosts 0.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: the help page that changed.
