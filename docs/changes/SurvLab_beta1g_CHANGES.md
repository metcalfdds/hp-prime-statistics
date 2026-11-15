# SurvLab beta 1g: changes (15 November 2026)

Round 15 of 15 November 2026, the wording. Roger, 14 November 2026: "IS there an issue with 'reworking' the TI and Triola and Lloyd programs?" The record (the TI sweep of 20 October 2026) is that the TI-83/84 programs were read to see what each one computes and where it goes wrong, and that our programs were then written new in PPL; none of the TI code is in them. The earlier credits used a verb that says more than that. The book's Appendix F now ends with a paragraph in the author's words ("we did not reuse any of that code ... wrote our own version for the Prime ... to compute similar results"), and this version says the same where the program spoke of those programs. The build is `verify/round15/make_wording_r15.py`: each change is an exact replacement in SurvLab beta 1f (a miss stops it), then the version (header, history note, version strings).

## What changed

1. The header's note on the TI-83/84 program KAPMEIT1 begins "Does on the Prime what ... does" and says that SurvLab was written new, with none of KAPMEIT1's code.  Nothing on screen changes.

2. **Nothing else changed.** Every line that differs is a comment (the header and its history note): not one line the calculator runs is different.

Lines of SurvLab beta 1g that differ from SurvLab beta 1f: line 17 (comment); lines 43-47 (comment); lines 159-162 (comment). Routines whose code changed, with the number of lines: none.

## Checks

- `verify/verify_round15_wording_v1.py` (39 checks, 0 failed, for the five programs together; output beside it): the build makes this file byte for byte; only the replacements, comments and version strings differ from beta 1f; the help dump is the saved one, and no screen changed; the old verb is nowhere in the file; and over 30 seeds of the monkey the old and the new version show the same screens, boxes and Quit summary.
- `tools/ppl_gate_v1e.py` against SurvLab beta 1f: PASS. lint_ppl 6 problems, as in SurvLab beta 1f; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round15/helpcheck_r15.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 5 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version: screens 42/1066 collisions 14 (firm 13) straddles 0 overruns 0 ghosts 0. What the one-line summary counts as collisions here are rows of small text 11 px apart, which the tool's full report lists as "tight rows"; its count of overlaps is 0, and SurvLab beta 1f gives the same report.
- The monkey was not run again: not one line the calculator runs is different (only comments changed).
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Nothing on screen changed; the program should behave exactly as beta 1f.
