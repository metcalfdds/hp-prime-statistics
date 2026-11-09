# AgreeLab beta 1g: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes AgreeLab beta 1g from AgreeLab beta 1f. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 2, 6 and 7 reworded: "a low bar", "rater offsets count" and "(.,k)" said in words, d-bar named as the mean difference, and the Bland-Altman trend in words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 9 screens, as the PC harness counts them.

3. **Outside the help** only these lines changed (the version on screen, and the page numbers the help's callers ask for):

```text
ag_Hello       -  ag_Band("AgreeLab - beta 1f");
ag_Hello       +  ag_Band("AgreeLab - beta 1g");
```

Routines touched, with the number of new or changed lines in each: (comments) 7, ag_Hello 1, ag_HelpPage 31.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 3 of 9 screens changed; 6 kept their words.

### Before (beta 1f)

```text
AgreeLab help 2/9: SE, CI and the test
Two different SEs (Fleiss, Cohen & Everitt
1969, Psychol Bull 72:323-327):
- the large-sample SE gives the 95% CI,
  kappa ± 1.96 SE (rough when N is small);
- SE₀, the SE if kappa were 0, gives the
  test: z = kappa/SE₀, one-sided p.
p = P(a kappa this big | H₀: kappa = 0).
It is not the chance that H₀ is true, and
'better than chance' is a low bar: raters
who agree on 1 in 3 can beat it easily.
Read the CI: how much agreement, how sure.
statsmodels' cohens_kappa uses the same SEs.
Any key or tap = next, ← = back, Esc = leave
```

```text
AgreeLab help 6/9: Which ICC?
n targets × k raters, measured values.
ICC = between-target variance / total
(Shrout & Fleiss 1979; McGraw & Wong 1996):
(1,1) different raters for each target;
(2,1) same raters, a sample: ABSOLUTE
      agreement, rater offsets count;
(3,1) these raters only: CONSISTENCY.
(.,k): the reliability of the MEAN of k.
CIs from F (S & F 1979; ICC(2,1) with
Satterthwaite's df).  Shrout & Fleiss's own
example (a preset): .17, .29, .71, .44, .62, .91.
Choose the form from the design, not the
value: they answer different questions.
Any key or tap = next, ← = back, Esc = leave
```

```text
AgreeLab help 7/9: Bland-Altman
Two methods on the same n targets (Bland &
Altman 1986, Lancet i:307): plot d = A - B
against the mean (A + B)/2.
bias = 
d
; limits of agreement = bias ±
1.96 s: about 95% of differences fall there.
CI of the bias: bias ± t s/√n.
CI of a limit: ± t s√(1/n + 1.96²/(2(n - 1))),
APPROXIMATE (Bland & Altman 1986 SE). In a
review's simulation (40,000 runs) it covered
about 92% at n = 3-5 and 94% at n = 17.
Trend: regress d on the mean; a slope says
the disagreement grows with the size.
A high r is not agreement: r ignores bias.
Any key or tap = next, ← = back, Esc = leave
```

### After (beta 1g)

```text
AgreeLab help 2/9: SE, CI and the test
Two different SEs (Fleiss, Cohen & Everitt 1969, Psychol Bull
72:323-327):
- the large-sample SE gives the 95% CI, kappa ± 1.96 SE (rough
  when N is small);
- SE₀, the SE if kappa were 0, gives the test: z = kappa/SE₀,
  one-sided p.
p = P(a kappa this big | H₀: kappa = 0).
It is not the chance that H₀ is true, and 'better than chance' is
easy to reach: raters who agree on only 1 item in 3 can reach it.
The CI says how much agreement there is, and how precisely it
is known.
statsmodels' cohens_kappa uses the same SEs.
Any key or tap = next, ← = back, Esc = leave
```

```text
AgreeLab help 6/9: Which ICC?
n targets × k raters, measured values.
ICC = between-target variance / total (Shrout & Fleiss 1979;
McGraw & Wong 1996):
(1,1) different raters for each target;
(2,1) same raters, a sample: ABSOLUTE agreement; a rater who
      scores every target higher lowers it;
(3,1) these raters only: CONSISTENCY.
(1,k), (2,k), (3,k): the reliability of the MEAN of the k raters.
CIs from F (S & F 1979; ICC(2,1) with Satterthwaite's df).
Shrout & Fleiss's own example (a preset): .17, .29, .71, .44,
.62, .91.
Choose the form from the design, not the value: they answer
different questions.
Any key or tap = next, ← = back, Esc = leave
```

```text
AgreeLab help 7/9: Bland-Altman
Two methods on the same n targets (Bland & Altman 1986,
Lancet i:307): plot d = A - B against the mean (A + B)/2.
bias = 
d
, the mean difference; limits of
agreement = bias ± 1.96 s: about 95% of differences fall there.
CI of the bias: bias ± t s/√n.
CI of a limit: ± t s√(1/n + 1.96²/(2(n - 1))), APPROXIMATE
(Bland & Altman 1986 SE). In a review's simulation (40,000 runs)
it covered about 92% at n = 3-5 and 94% at n = 17.
Trend: regress d on the mean; a slope means the two methods
differ more for larger (or smaller) values.
A high r is not agreement: r ignores bias.
Any key or tap = next, ← = back, Esc = leave
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1f; lint_ppl 6 problems, as in beta 1f (6); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 9 screens; one report, the drawn d̄ on page 7: the bar and the d are drawn separately, and the check measures the d as a plain d next to the text that follows it; on the Virtual Calculator the line reads "bias = d̄, the mean difference; limits of" as it should.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".
  On the Virtual Calculator all nine help pages were opened from the menu and read (`verify/round11/screens/`): every line inside its page, nothing cut.

Not yet run on a G1 or a G2.
