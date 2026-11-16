# StatDist v2.7n: changes (15 November 2026)

Round 16 of 15 November 2026, the wording. Round 15 reworded the credits of the six programs that follow TI-83/84 programs, so that each says what was done in plain verbs. Four more programs spoke of other programs in words that said more, or less, than the record: StatDist's "framework after S. Micciche", and the label "Replaces / reworks:" in BurrLab, RiskLab and AgreeLab. Asked whether these should be reworded too, Roger, 15 November 2026: "reword as the others---look, be consistent throughout the book". The build is `verify/round16/make_wording_r16.py`: each change is an exact replacement in StatDist v2.7m (a miss stops it), then the version (header, history note, version strings).

## What changed

1. The header said "(framework after S. Micciche)".  It now says what StatDist shares with Salvo Micciche's "Statistic Distributions" (hpcalc.org, 2015), eleven of the 13 families it adds to the Prime's own, and that none of his code is in StatDist: his 494 lines were set beside v2.7m, v2.5 and v2.2 (the oldest copy kept) on 15 Nov 2026.

2. **Nothing else changed.** Every line that differs is a comment (the header and its history note): not one line the calculator runs is different, and the program shows no version on its pages.

**The record** (15 November 2026; `statistic.zip` from hpcalc.org, in `D:\HP-Prime`, set beside the StatDist files). Micciche's "Statistic Distributions" is 494 lines: 55 exported density and distribution functions, typed at Home, with no menus and no plots. Of its 134 distinct code lines not one is in StatDist v2.7m (5,091 lines), in v2.5 or in v2.2 (29 July 2026, the oldest copy kept); none of its function names or of its "Use: ..." messages is in them either. Eleven of the 13 families StatDist adds to the Prime's own are families his file has (not Burr XII, not the triangular). So the two programs do the same kind of thing for many of the same distributions, and share no code. "Framework after" said more than that.

Lines of StatDist v2.7n that differ from StatDist v2.7m: line 4 (comment); lines 8-19 (comment); lines 45-50 (comment).

## Checks

- `verify/verify_round16_wording_v1.py` (25 checks, 0 failed, for the four programs together; output beside it): the build makes this file byte for byte; its 3,636 lines that are not comments are StatDist v2.7m's; the help dump is the old version's, screen for screen; no line of any of the 31 programs begins "// Replaces / reworks", and no author line says "(framework after"; the header says the new words; and over 30 seeds of the monkey the old and the new version show the same screens text for text (1,719 screens, all 30 runs OK).
- `tools/ppl_gate_v1e.py` against StatDist v2.7m (`verify/round16/gates/StatDist_v2.7n.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 4 reports, as in StatDist v2.7m; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round16/helpcheck_r16.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 4 screens, one known report, as in Rounds 11 and 12: the harness cannot call `st_ABHelp` without its argument (its pages are checked through the menu).
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: the same report as StatDist v2.7m's, as it must be with the same screens (screens 23/228 collisions 11 (firm 11) straddles 0 overruns 0 ghosts 0).
- The monkey's 1,000 runs were not made again: not one line the calculator runs is different, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "No errors in the program"; the program was then started from the Program Catalog, its menu and its four help pages were seen, and it was left with "StatDist: no plot drawn yet" (`verify/round16/vc_checks.txt`, `verify/round16/screens/StatDist_*.png`).

## On a G1 or a G2

Not yet run on a G1 or a G2. Nothing on the screen changed; the program should behave exactly as v2.7m.
