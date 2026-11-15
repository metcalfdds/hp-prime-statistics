# RankLab beta 1i: changes (15 November 2026)

Round 15 of 15 November 2026, the wording. Roger, 14 November 2026: "IS there an issue with 'reworking' the TI and Triola and Lloyd programs?" The record (the TI sweep of 20 October 2026) is that the TI-83/84 programs were read to see what each one computes and where it goes wrong, and that our programs were then written new in PPL; none of the TI code is in them. The earlier credits used a verb that says more than that. The book's Appendix F now ends with a paragraph in the author's words ("we did not reuse any of that code ... wrote our own version for the Prime ... to compute similar results"), and this version says the same where the program spoke of those programs. The build is `verify/round15/make_wording_r15.py`: each change is an exact replacement in RankLab beta 1h (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 7/7 ends "Does what Michael Lloyd's TI-83/84 programs for Triola do (...), without their tie, zero, rs errors.  Written new for the Prime: none of their code." (four lines; it was three).  The header's note on those programs begins the same way.

2. **Nothing else changed**, apart from the header, the history note and the version strings. No line of code changed but the help text.

Lines of RankLab beta 1i that differ from RankLab beta 1h: line 17 (comment); lines 59-64 (comment); lines 209-211 (comment); lines 3757-3760 (code); line 3774 (code). Routines whose code changed, with the number of lines: rk_Help 4, rk_Welcome 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screen that changed.

### Screen 7, before (beta 1h)

```text
RankLab help 7/7: Data, Home, credits
Presets (source on every page): Rossi
recidivism, the 1970 draft lottery, Darwin's
Zea mays, judges' ratings, a mock jury (KW
uses attractiveness only; Crime is ignored).
Your data: Statistics 1Var D1..D9; groups =
columns; paired D1 - D2; one sample D1 vs m₀;
correlation D1, D2; Friedman: rows = blocks.
Home: RK_STAT, RK_P (exact when there is
one), RK_PN, RK_EFF, RK_HL, RK_RANKS.
Reworks Michael Lloyd's TI-83/84 programs
for Triola (SRTEST, RSTEST, KWTEST, SRCORR,
ZZRANK) without their tie, zero, rs errors.
Page 7/7: key = next, ← = back, Esc = leave
```

### Screen 7, after (beta 1i)

```text
RankLab help 7/7: Data, Home, credits
Presets (source on every page): Rossi
recidivism, the 1970 draft lottery, Darwin's
Zea mays, judges' ratings, a mock jury (KW
uses attractiveness only; Crime is ignored).
Your data: Statistics 1Var D1..D9; groups =
columns; paired D1 - D2; one sample D1 vs m₀;
correlation D1, D2; Friedman: rows = blocks.
Home: RK_STAT, RK_P (exact when there is
one), RK_PN, RK_EFF, RK_HL, RK_RANKS.
Does what Michael Lloyd's TI-83/84 programs
for Triola do (SRTEST, RSTEST, KWTEST, SRCORR,
ZZRANK), without their tie, zero, rs errors.
Written new for the Prime: none of their code.
Page 7/7: key = next, ← = back, Esc = leave
```

## Checks

- `verify/verify_round15_wording_v1.py` (39 checks, 0 failed, for the five programs together; output beside it): the build makes this file byte for byte; only the replacements, comments and version strings differ from beta 1h; the help dump is the saved one, and screen 7 is the only one that changed; the old verb is nowhere in the file; and over 30 seeds of the monkey the old and the new version show the same screens, boxes and Quit summary, apart from that page and the version string.
- `tools/ppl_gate_v1e.py` against RankLab beta 1h: PASS. lint_ppl 5 problems, as in RankLab beta 1h; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round15/helpcheck_r15.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 7 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version: screens 82/1200 collisions 0 (firm 0) straddles 0 overruns 0 ghosts 0.
- The monkey (`tools/monkey_chunks_v1.py`, base 15, with `--lists`): 1,000 of 1,000 runs OK.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "No errors in the program"; the help page that changed was then looked at there (`verify/round15/screens/`).

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Help page 7/7: four lines of credit at the foot of the page, the last one ("Written new for the Prime: none of their code.") clear of the footer.
