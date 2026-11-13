# AnovaLab beta 1g: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in AnovaLab beta 1f (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 4/9: Scheffé with its accent (CHAR(233); GlyphProbe_v1 measured it, Round 11).  The menus keep "Scheffe".

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of AnovaLab beta 1g that differ from AnovaLab beta 1f: line 17 (comment); lines 51-53 (comment); line 2465 (code); line 3813 (code). Routines whose code changed, with the number of lines: av_HelpPage 1, av_Hello 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 4, before (beta 1f)

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

### Screen 4, after (beta 1g)

```text
AnovaLab help 4/9: Which pairs differ? (continued)
Scheffé: covers every contrast, widest CIs.
CIs are simultaneous (family 95%).
Pairs page: +/- or a tab = method; tap a pair.
Dots page: tap two groups, or ←→ for the next pair.
More > Tukey p: every pair's Tukey p.
Tukey vs SciPy: q crit within 0.03 %, pair p within 0.00001 (k
2-12, df 3-1,000, α .1-.001).
Any key or tap = next, ← = back, Esc = leave
```

## Checks

- `tools/ppl_gate_v1e.py` against AnovaLab beta 1f: PASS. lint_ppl 5 problems, as in AnovaLab beta 1f; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 9 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 37/1035 collisions 57 (firm 54) straddles 0 overruns 0 ghosts 0.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Help page 4/9: the é of Scheffé is drawn as an accented e.

## Unresolved

The menus, the Pairs page's method name and the message about Tukey still write "Scheffe" without the accent; only the help page's prose has it.
