# BurrLab beta 1r: changes (15 November 2026)

Round 16 of 15 November 2026, the wording. Round 15 reworded the credits of the six programs that follow TI-83/84 programs, so that each says what was done in plain verbs. Four more programs spoke of other programs in words that said more, or less, than the record: StatDist's "framework after S. Micciche", and the label "Replaces / reworks:" in BurrLab, RiskLab and AgreeLab. Asked whether these should be reworded too, Roger, 15 November 2026: "reword as the others---look, be consistent throughout the book". The build is `verify/round16/make_wording_r16.py`: each change is an exact replacement in BurrLab beta 1q (a miss stops it), then the version (header, history note, version strings).

## What changed

1. The header's line "Replaces / reworks: Burr3 v2.4c (fleet).  No TI program is replaced." now reads "Takes the place of Burr3 v2.4c, the fleet's own earlier program, and reuses the parts of it named above ...  It follows no TI program."  The paragraph above it, which names the code carried over from Burr3, is unchanged: Burr3 is the author's own program, and the rule asks only that a credit say which code was carried over.

2. **Nothing else changed**, apart from the header, the history note and the version the program shows (one line of code, in `bu_Opening`). The help is the same, screen for screen.

**Why this one keeps the word "reuses".** Burr3 is the author's own earlier program, and parts of it were carried over: its header, its drag idiom and its log-domain pdf and CDF. The rule asks that a credit say which code was carried over where any was, and this one does.

Lines of BurrLab beta 1r that differ from BurrLab beta 1q: lines 17-24 (comment); lines 333-335 (comment); line 4662 (code).

## Checks

- `verify/verify_round16_wording_v1.py` (25 checks, 0 failed, for the four programs together; output beside it): the build makes this file byte for byte; its 3,781 lines that are not comments are BurrLab beta 1q's, but for the one with the version; the help dump is the old version's, screen for screen; no line of any of the 31 programs begins "// Replaces / reworks", and no author line says "(framework after"; the header says the new words; and over 30 seeds of the monkey the old and the new version show the same screens text for text (9,889 screens, all 30 runs OK).
- `tools/ppl_gate_v1e.py` against BurrLab beta 1q (`verify/round16/gates/BurrLab_beta1r.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 27 reports, as in BurrLab beta 1q; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round16/helpcheck_r16.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 6 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: the same report as BurrLab beta 1q's, as it must be with the same screens (screens 1166/7100 collisions 0 (firm 0) straddles 6 overruns 0 ghosts 0).
- The monkey's 1,000 runs were not made again: only the version string differs among the lines the calculator runs, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "No errors in the program"; the program was then started from the Program Catalog, its opening page ("BurrLab beta 1r: the long right tail") and its menu were seen, and it was left with "BurrLab: no fit; explorer at C = 2.00, K = 1.50, S = 10.00" (`verify/round16/vc_checks.txt`, `verify/round16/screens/BurrLab_*.png`).

## On a G1 or a G2

Not yet run on a G1 or a G2. Nothing on the screen changed but the version the opening page shows; the program should behave exactly as beta 1q.
