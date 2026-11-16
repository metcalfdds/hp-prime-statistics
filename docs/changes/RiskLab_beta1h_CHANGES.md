# RiskLab beta 1h: changes (15 November 2026)

Round 16 of 15 November 2026, the wording. Round 15 reworded the credits of the six programs that follow TI-83/84 programs, so that each says what was done in plain verbs. Four more programs spoke of other programs in words that said more, or less, than the record: StatDist's "framework after S. Micciche", and the label "Replaces / reworks:" in BurrLab, RiskLab and AgreeLab. Asked whether these should be reworded too, Roger, 15 November 2026: "reword as the others---look, be consistent throughout the book". The build is `verify/round16/make_wording_r16.py`: each change is an exact replacement in RiskLab beta 1g (a miss stops it), then the version (header, history note, version strings).

## What changed

1. The header's note on the TI-83/84 program LOGIT begins "No Triola program does this.  The nearest TI-83/84 program, LOGIT ..." and ends "LOGIT was read to see what it computes; RiskLab was written new in PPL, and none of LOGIT's code is in it." (it began "Replaces / reworks:").

2. **Nothing else changed**, apart from the header, the history note and the version the program shows (one line of code, in `rl_Open`). The help is the same, screen for screen.

**What LOGIT is.** A TI-83/84 program that fits a one-predictor logistic model to grouped counts by weighted least squares. Its decoded listing (`LOGIT__257.txt`, from `logit.zip`, in the author's working folder) was read to see what it computes. RiskLab fits one to four predictors by Newton–Raphson, gives standard errors, tests and odds ratios, and detects separation; none of that is in LOGIT, and none of LOGIT's code is in RiskLab.

Lines of RiskLab beta 1h that differ from RiskLab beta 1g: line 17 (comment); lines 45-49 (comment); lines 153-154 (comment); lines 158-160 (comment); line 3077 (code).

## Checks

- `verify/verify_round16_wording_v1.py` (25 checks, 0 failed, for the four programs together; output beside it): the build makes this file byte for byte; its 2,644 lines that are not comments are RiskLab beta 1g's, but for the one with the version; the help dump is the old version's, screen for screen; no line of any of the 31 programs begins "// Replaces / reworks", and no author line says "(framework after"; the header says the new words; and over 30 seeds of the monkey the old and the new version show the same screens text for text (1,486 screens, all 30 runs OK).
- `tools/ppl_gate_v1e.py` against RiskLab beta 1g (`verify/round16/gates/RiskLab_beta1h.txt`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 6 reports, as in RiskLab beta 1g; `fleet_names_v2` over the 31 newest files: no collisions.
- `verify/round16/helpcheck_r16.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 8 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: the same report as RiskLab beta 1g's, as it must be with the same screens (screens 39/1079 collisions 8 (firm 8) straddles 0 overruns 0 ghosts 0).
- The monkey's 1,000 runs were not made again: only the version string differs among the lines the calculator runs, and 30 seeds show the same screens in both versions.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "No errors in the program"; the program was then started from the Program Catalog, its opening page ("beta 1h, 15 Nov 2026.  Help is in the menu.") and its menu were seen, and it was left with "RiskLab: COMPAS, AUC = 0.711, ≥ 5: sens 0.645, spec 0.670" (`verify/round16/vc_checks.txt`, `verify/round16/screens/RiskLab_*.png`).

## On a G1 or a G2

Not yet run on a G1 or a G2. Nothing on the screen changed but the version the opening page shows; the program should behave exactly as beta 1g.
