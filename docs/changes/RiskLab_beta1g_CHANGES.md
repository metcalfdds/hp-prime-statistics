# RiskLab beta 1g: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in RiskLab beta 1f (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 2/8: "penalized", in American spelling.

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of RiskLab beta 1g that differ from RiskLab beta 1f: line 17 (comment); lines 45-46 (comment); line 2947 (code); line 3070 (code). Routines whose code changed, with the number of lines: rl_Help 1, rl_Open 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 2, before (beta 1f)

```text
RiskLab help 2/8: Separation, collinearity
If some x (or a mix of x) puts every Y = 1 above every Y = 0, the
likelihood keeps rising as |b| grows: no finite estimate
(Albert & Anderson 1984).  RiskLab warns when the fit has not
converged in 25 steps, the fitted line orders Y perfectly, or I
turns singular.  Remedies: drop or merge that x, or a penalised
(Firth) fit, not offered here.
Collinear x (one a mix of the others) make I singular too: no SEs.
Speed: each step of the fit goes through every row; Rossi's 432
rows need about 7 passes.  On a G1 that is slow (a progress bar
shows it; Esc stops it).
Page 2/8, any key = next, Esc = leave
```

### Screen 2, after (beta 1g)

```text
RiskLab help 2/8: Separation, collinearity
If some x (or a mix of x) puts every Y = 1 above every Y = 0, the
likelihood keeps rising as |b| grows: no finite estimate
(Albert & Anderson 1984).  RiskLab warns when the fit has not
converged in 25 steps, the fitted line orders Y perfectly, or I
turns singular.  Remedies: drop or merge that x, or a penalized
(Firth) fit, not offered here.
Collinear x (one a mix of the others) make I singular too: no SEs.
Speed: each step of the fit goes through every row; Rossi's 432
rows need about 7 passes.  On a G1 that is slow (a progress bar
shows it; Esc stops it).
Page 2/8, any key = next, Esc = leave
```

## Checks

- `tools/ppl_gate_v1e.py` against RiskLab beta 1f: PASS. lint_ppl 6 problems, as in RiskLab beta 1f; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 8 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 39/1079 collisions 8 (firm 8) straddles 0 overruns 0 ghosts 0.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: the help page that changed.
