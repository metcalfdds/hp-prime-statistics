# TTestLab beta 1j: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in TTestLab beta 1i (a miss stops it), then the version (header, history note, version strings).

## What changed

1. The figure number of the lecture note (Figure 11.2) is gone from the menu item (now "Choose the test (flowchart)", as in TTestLabG), the flowchart's title and the pooled-or-separate note: in the book, Figure 11.2 is a different picture.

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of TTestLab beta 1j that differ from TTestLab beta 1i: line 4 (comment); lines 21-24 (comment); line 1068 (code); line 1081 (code); line 1489 (code). Routines whose code changed, with the number of lines: tt_Compare 1, tt_DrawFlow 1, TTESTLAB 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

## Checks

- `tools/ppl_gate_v1e.py` against TTestLab beta 1i: PASS. lint_ppl 4 problems, as in TTestLab beta 1i; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 2 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 34/384 collisions 0 (firm 0) straddles 0 overruns 9 ghosts 0.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: The menu reads "Choose the test (flowchart)" and fits its box; the flowchart's title reads "Which t-test?".

## Unresolved

TTestLab is the version that follows the lecture, so its rounding notes and the pooled-or-separate note still begin "The lecture" (three places); TTestLabG has none.  The book uses both.
