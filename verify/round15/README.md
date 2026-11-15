# Round 15: an interval for ρ, standard errors for the shape numbers, and the credits (15 November 2026)

Two additions and one change of wording.

- **ScatterLab beta 2l**: the page Menu > Inference for the slope ends with a 95% confidence interval for ρ, the population's correlation, by Fisher's z.
- **FitCheck beta 1h**: the Tests page of the normality checks gives the skewness and the excess kurtosis each its standard error in normal samples; the closing summary after a sample in bins names the two numbers; the credits are in new words.
- **RankLab beta 1i, AnovaLab beta 1h, ResampLab beta 1i, ExhibitLab beta 1h, SurvLab beta 1g** (and FitCheck): the credits say what was done with the TI-83/84 programs these six follow. Those programs were read to see what each one computes; ours were written new in PPL, with none of their code.

Roger asked for the two additions on 15 November 2026 ("1 and 2 would be great"), after our programs had been compared with the descriptions of Stan Brown's MATH200A and MATH200B for the TI-83/84 (brownmath.com). Only the descriptions were read, no code. The wording follows his question of 14 November ("IS there an issue with 'reworking' the TI and Triola and Lloyd programs?") and the paragraph of thanks that now ends the book's Appendix F.

## What is here

| File | What it is |
| --- | --- |
| `make_scatterlab_2l.py`, `make_fitcheck_1h.py` | The two builds. Each change is an exact replacement in the version before, read from git (`BASE`, the commit before this round); a replacement that does not match exactly once stops the build. |
| `make_wording_r15.py` | The build of the five programs whose only change is their credits: the replacements, then each program's next version (the header line, a history note, the version strings in literals). It stops if the old verb is left anywhere in a file. |
| `records_r15.py` | Gathers the round's other records for all seven: `gates/` (`tools/ppl_gate_v1e.py` on each new version against its old one), `helppages_before_r15.json` and `helppages_r15.json` (every help screen of the old and the new versions as the PC harness draws them), `helpcheck_r15.json` (every new help screen laid out at the glyph widths GlyphProbe_v1 measured), and `checks_r15.txt`: S, the harness smoke test beside the old version's; T, `tools/text_overlap_v1.py --walk` on both versions, the two reports kept in `overlap_<Name>.txt`; F, `tools/fleet_names_v2.py` over the fleet. |
| `make_changes_r15.py` | Writes `docs/changes/<Name>_<version>_CHANGES.md` for the five wording versions from those records. (ScatterLab's and FitCheck's notes are written by hand.) |
| `mk/` | The monkey's runs (`tools/monkey_chunks_v1.py`, base 15, `--lists`; ScatterLab with `--writes C`, FitCheck with `--writes D`): 1,000 of 1,000 OK for ScatterLab, FitCheck, RankLab, AnovaLab and ResampLab. ExhibitLab and SurvLab changed in comments only and were not run again. |
| `vc_checks.txt` | The Checks and the runs on the Virtual Calculator, with what was seen. |
| `screens/` | What the Virtual Calculator showed (320 × 240, enlarged three times): ScatterLab's Inference page for the example and for Anscombe's set 1, its help page 1; FitCheck's Tests pages for its two normality presets, its help pages 5 and 8, its closing summary; the changed help page of RankLab, AnovaLab and ResampLab. |
| `../verify_ScatterLab_beta2l.py`, `../verify_FitCheck_beta1h.py`, `../verify_round15_wording_v1.py` | The three verify scripts (42, 31 and 39 checks, 0 failed); their saved output is beside them. |

## To run again

From the repository's root, with hp-prime-kit at `$HPKIT` (see `CLAUDE.md`):

```
python3 verify/round15/make_scatterlab_2l.py OUTDIR
python3 verify/round15/make_fitcheck_1h.py OUTDIR
python3 verify/round15/make_wording_r15.py OUTDIR
cd verify && python3 verify_ScatterLab_beta2l.py && python3 verify_FitCheck_beta1h.py && python3 verify_round15_wording_v1.py
python3 verify/round15/records_r15.py          # from the root again; about ten minutes
```

## A note on reading `checks_r15.txt`

The T lines give `text_overlap_v1.py`'s one-line summary, whose "collisions (firm)" count includes rows of small text 11 px apart. For AnovaLab (57) and SurvLab (14) that is all they are: the tool's full report (`--json FILE`, then `--md FILE`) lists them as tight rows and counts 0 overlaps, and each program's version before this round gives the same report.

## Not done

Nothing in this round has run on a G1 or a G2.
