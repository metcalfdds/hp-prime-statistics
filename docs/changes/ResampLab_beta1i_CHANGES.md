# ResampLab beta 1i: changes (15 November 2026)

Round 15 of 15 November 2026, the wording. Roger, 14 November 2026: "IS there an issue with 'reworking' the TI and Triola and Lloyd programs?" The record (the TI sweep of 20 October 2026) is that the TI-83/84 programs were read to see what each one computes and where it goes wrong, and that our programs were then written new in PPL; none of the TI code is in them. The earlier credits used a verb that says more than that. The book's Appendix F now ends with a paragraph in the author's words ("we did not reuse any of that code ... wrote our own version for the Prime ... to compute similar results"), and this version says the same where the program spoke of those programs. The build is `verify/round15/make_wording_r15.py`: each change is an exact replacement in ResampLab beta 1h (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 5/5: "Does what Triola's TI bootstrap project and the TI BOOT program do; written new, with none of their code."  The header's note begins the same way, and says that ResampLab uses the same published method as BOOT's BCa arithmetic (Efron's), where it said the arithmetic "is kept".

2. **Nothing else changed**, apart from the header, the history note and the version strings. No line of code changed but the help text.

Lines of ResampLab beta 1i that differ from ResampLab beta 1h: line 17 (comment); lines 47-52 (comment); lines 161-163 (comment); lines 167-169 (comment); line 2496 (code); line 2974 (code). Routines whose code changed, with the number of lines: rs_Help 1, rs_Splash 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screen that changed.

### Screen 5, before (beta 1h)

```text
ResampLab help 5/5: Home, sources, disclaimer
Home: RS_P (plus-one p), RS_PX (exact p or
-1), RS_NB (B), RS_OBS (observed), RS_PCT and
RS_BCA (interval ends), RS_STAR (the
bootstrap values).
Fisher 1935; Pitman 1937; Ernst 2004; Phipson
& Smyth 2010; Efron 1979, 1987; Efron &
Tibshirani 1993; Davison & Hinkley 1997;
Hesterberg 2015.  Reworks Triola's TI
bootstrap project and the TI BOOT program.
DISCLAIMER: a teaching and demonstration aid.
Not validated for forensic, clinical or legal
use; do not rely on its results for legal
purposes.
Any key = back
```

### Screen 5, after (beta 1i)

```text
ResampLab help 5/5: Home, sources, disclaimer
Home: RS_P (plus-one p), RS_PX (exact p or
-1), RS_NB (B), RS_OBS (observed), RS_PCT and
RS_BCA (interval ends), RS_STAR (the
bootstrap values).
Fisher 1935; Pitman 1937; Ernst 2004; Phipson
& Smyth 2010; Efron 1979, 1987; Efron &
Tibshirani 1993; Davison & Hinkley 1997;
Hesterberg 2015.  Does what Triola's TI
bootstrap project and the TI BOOT program do;
written new, with none of their code.
DISCLAIMER: a teaching and demonstration aid.
Not validated for forensic, clinical or legal
use; do not rely on its results for legal
purposes.
Any key = back
```

## Checks

- `verify/verify_round15_wording_v1.py` (39 checks, 0 failed, for the five programs together; output beside it): the build makes this file byte for byte; only the replacements, comments and version strings differ from beta 1h; the help dump is the saved one, and screen 5 is the only one that changed; the old verb is nowhere in the file; and over 30 seeds of the monkey the old and the new version show the same screens, boxes and Quit summary, apart from that page and the version string.
- `tools/ppl_gate_v1e.py` against ResampLab beta 1h: PASS. lint_ppl 10 problems, as in ResampLab beta 1h; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round15/helpcheck_r15.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 5 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version: screens 6/120 collisions 0 (firm 0) straddles 0 overruns 0 ghosts 0.
- The monkey (`tools/monkey_chunks_v1.py`, base 15, with `--lists`): 1,000 of 1,000 runs OK.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "No errors in the program"; the help page that changed was then looked at there (`verify/round15/screens/`).

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Help page 5/5: the sources paragraph is a line longer; the disclaimer under it still ends above the footer.
