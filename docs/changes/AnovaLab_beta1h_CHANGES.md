# AnovaLab beta 1h: changes (15 November 2026)

Round 15 of 15 November 2026, the wording. Roger, 14 November 2026: "IS there an issue with 'reworking' the TI and Triola and Lloyd programs?" The record (the TI sweep of 20 October 2026) is that the TI-83/84 programs were read to see what each one computes and where it goes wrong, and that our programs were then written new in PPL; none of the TI code is in them. The earlier credits used a verb that says more than that. The book's Appendix F now ends with a paragraph in the author's words ("we did not reuse any of that code ... wrote our own version for the Prime ... to compute similar results"), and this version says the same where the program spoke of those programs. The build is `verify/round15/make_wording_r15.py`: each change is an exact replacement in AnovaLab beta 1g (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 9/9 begins "Does what Triola's TI-83/84 programs ANOVA, ... and FINTRVAL do.  Written new: none of their code." (four lines; it was three), and the nine lines under it each sit 13 px lower (the last at y 198).  The header's note on those programs begins the same way, and two section comments say "what Triola's S2TEST / S2INT do".

2. **Nothing else changed**, apart from the header, the history note and the version strings. No line of code changed but the help text.

Lines of AnovaLab beta 1h that differ from AnovaLab beta 1g: line 17 (comment); lines 51-57 (comment); lines 158-161 (comment); line 1840 (comment); lines 2543-2555 (code); line 3314 (comment); line 3823 (code). Routines whose code changed, with the number of lines: av_HelpPage 13, av_Hello 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screen that changed.

### Screen 9, before (beta 1g)

```text
AnovaLab help 9/9: Credits
Reworks Triola's TI-83/84 ANOVA, ANOVA2FD,
ANOVA2RB, RANOVA, TUKEY, SCHEFFE2, BONFRNI,
SDHYP, SDINT, STDTEST, STDEVCI and FINTRVAL.
Not repeated: 0 and negatives as missing,
the wrong n in Tukey's SE, swapped F bounds,
a solver that fails for n > 75, equal-n only.
Tukey's q: StudRange's PPL engine (Dunlap,
Powell & Konnerth 1977, with a u² step).
Data: Plaster 1989; Fienberg 1971; Beall 1942;
New Haven Register 1977 (R datasets).
A teaching aid: not validated for forensic,
clinical or legal use.
Any key or tap = next, ← = back, Esc = leave
```

### Screen 9, after (beta 1h)

```text
AnovaLab help 9/9: Credits
Does what Triola's TI-83/84 programs ANOVA,
ANOVA2FD, ANOVA2RB, RANOVA, TUKEY, SCHEFFE2,
BONFRNI, SDHYP, SDINT, STDTEST, STDEVCI and
FINTRVAL do.  Written new: none of their code.
Not repeated: 0 and negatives as missing,
the wrong n in Tukey's SE, swapped F bounds,
a solver that fails for n > 75, equal-n only.
Tukey's q: StudRange's PPL engine (Dunlap,
Powell & Konnerth 1977, with a u² step).
Data: Plaster 1989; Fienberg 1971; Beall 1942;
New Haven Register 1977 (R datasets).
A teaching aid: not validated for forensic,
clinical or legal use.
Any key or tap = next, ← = back, Esc = leave
```

## Checks

- `verify/verify_round15_wording_v1.py` (39 checks, 0 failed, for the five programs together; output beside it): the build makes this file byte for byte; only the replacements, comments and version strings differ from beta 1g; the help dump is the saved one, and screen 9 is the only one that changed; the old verb is nowhere in the file; and over 30 seeds of the monkey the old and the new version show the same screens, boxes and Quit summary, apart from that page and the version string.
- `tools/ppl_gate_v1e.py` against AnovaLab beta 1g: PASS. lint_ppl 5 problems, as in AnovaLab beta 1g; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round15/helpcheck_r15.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 9 screens, no reports.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version: screens 37/1035 collisions 57 (firm 54) straddles 0 overruns 0 ghosts 0. What the one-line summary counts as collisions here are rows of small text 11 px apart, which the tool's full report lists as "tight rows"; its count of overlaps is 0, and AnovaLab beta 1g gives the same report.
- The monkey (`tools/monkey_chunks_v1.py`, base 15, with `--lists`): 1,000 of 1,000 runs OK.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 15 Nov 2026: Check said "No errors in the program"; the help page that changed was then looked at there (`verify/round15/screens/`).

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Help page 9/9: thirteen lines now; the last ("clinical or legal use.", at y 198) clear of the footer.
