# AgreeLab beta 1h: changes (15 November 2026)

Round 16 of 15 November 2026, the wording. Round 15 reworded the credits of the six programs that follow TI-83/84 programs, so that each says what was done in plain verbs. Four more programs spoke of other programs in words that said more, or less, than the record: StatDist's "framework after S. Micciche", and the label "Replaces / reworks:" in BurrLab, RiskLab and AgreeLab. Asked whether these should be reworded too, Roger, 15 November 2026: "reword as the others---look, be consistent throughout the book". The build is `verify/round16/make_wording_r16.py`: each change is an exact replacement in AgreeLab beta 1g (a miss stops it), then the version (header, history note, version strings).

## What changed

1. The header's note on TI programs begins "Follows no TI-83/84 program" and says that AgreeLab was written new in PPL from the papers it lists (it said "Replaces / reworks: no TI program ... nothing is ported").

2. **Nothing else changed**, apart from the header, the history note and the version the program shows (one line of code, in `ag_Hello`). The help is the same, screen for screen.

**What was looked for.** The decoded TI programs in the author's working folder (`ref/triola_ti_programs/`) hold no agreement program (a search for kappa finds only Bayesian posterior programs). AgreeLab was written from the papers its header lists.

Lines of AgreeLab beta 1h that differ from AgreeLab beta 1g: line 17 (comment); lines 52-56 (comment); line 168 (comment); lines 170-171 (comment); line 3015 (code).

## Checks

- `verify/verify_round16_wording_v1.py` (25 checks, 0 failed, for the four programs together; output beside it): the build makes this file byte for byte; its 2,515 lines that are not comments are AgreeLab beta 1g's, but for the one with the version; the help dump is the old version's, screen for screen; no line of any of the 31 programs begins "// Replaces / reworks", and no author line says "(framework after"; the header says the new words; and over 30 seeds of the monkey the old and the new version show the same screens text for text (2,187 screens, all 30 runs OK).
- `tools/ppl_gate_v1e.py` against AgreeLab beta 1g (`verify/round16/gates/AgreeLab_beta1h.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 6 reports, as in AgreeLab beta 1g; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round16/helpcheck_r16.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 9 screens, one known report, as in Round 11: the d̄ drawn on help page 7 (the check measures the bar's d as a plain letter beside the next text; the Virtual Calculator shows the line correctly).
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: the same report as AgreeLab beta 1g's, as it must be with the same screens (screens 83/1192 collisions 25 (firm 19) straddles 0 overruns 0 ghosts 0).
- The monkey's 1,000 runs were not made again: only the version string differs among the lines the calculator runs, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "No errors in the program"; the program was then started from the Program Catalog, its opening page ("AgreeLab - beta 1h") and its menu were seen, and it was left with "AgreeLab: no analysis run" (`verify/round16/vc_checks.txt`, `verify/round16/screens/AgreeLab_*.png`).

## On a G1 or a G2

Not yet run on a G1 or a G2. Nothing on the screen changed but the version the opening page shows; the program should behave exactly as beta 1g.
