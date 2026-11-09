# RiskLab beta 1f: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes RiskLab beta 1f from RiskLab beta 1e. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 2, 4, 5 and 6 reworded: the AUC, the cut-off, calibration and the fairness measures in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 8 screens, as the PC harness counts them.

3. **Outside the help** only these lines changed (the version on screen, and the page numbers the help's callers ask for):

```text
rl_Open        -  TEXTOUT_P("beta 1e, 2 Nov 2026.  Help is in the menu.", G1, 6, 184, 1, rlGRAY, 310);
rl_Open        +  TEXTOUT_P("beta 1f, 9 Nov 2026.  Help is in the menu.", G1, 6, 184, 1, rlGRAY, 310);
```

Routines touched, with the number of new or changed lines in each: (comments) 6, rl_Help 44, rl_Open 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 4 of 8 screens changed; 4 kept their words.

### Before (beta 1e)

```text
RiskLab help 2/8: Separation, collinearity
If some x (or a mix of x) puts every Y = 1
above every Y = 0, the likelihood keeps rising
as |b| grows: no finite estimate
(Albert & Anderson 1984).  RiskLab warns when
the fit has not converged in 25 steps, the
fitted line orders Y perfectly, or I turns
singular.  Remedies: drop or merge that x, or
a penalised (Firth) fit, not offered here.
Collinear x (one a mix of the others) make I
singular too: no SEs.
Speed: each pass touches every row; Rossi's
432 rows need about 7 passes.  On a G1 that is
slow (a progress bar shows it; Esc stops it).
Page 2/8, any key = next, Esc = leave
```

```text
RiskLab help 4/8: Cut-offs and trade-offs
A lower cut-off flags more people: more TP
(sensitivity up) and more FP (specificity
down).  No cut-off avoids both errors.
PPV = TP/(TP + FP): of those flagged, the
share with Y = 1.  It depends on the base
rate: the same sensitivity and specificity
give a lower PPV where Y = 1 is rarer.
NPV = TN/(TN + FN).
Choosing a cut-off chooses which error costs
more: the statistics show the trade, they do
not set the price.
COMPAS deciles: 1-4 low, 5-7 medium, 8-10
high; ProPublica took 5 and up as high risk.
Page 4/8, any key = next, Esc = leave
```

```text
RiskLab help 5/8: Calibration, H-L test
Calibrated: of people given P = 0.3, about
30% have Y = 1.  RiskLab sorts by predicted P
into 10 groups (ties kept together), or one
group per score level, and compares observed
O with expected E = sum of P in each group:
HL = sum of (O - E)²/(E(1 - E/n)), df = groups
- 2 (Hosmer & Lemeshow 1980).  Weaknesses: it
depends on the number of groups and on how
ties are cut (software differs); it has low
power with small n, and with large n a tiny
misfit is 'significant' (Hosmer et al. 1997).
A large p is no proof of good calibration.
Gray bars: pred ± 1.96 SE, a rough guide.
A score (COMPAS): pred = RiskLab's own fit.
Page 5/8, any key = next, Esc = leave
```

```text
RiskLab help 6/8: Fairness definitions
Predictive parity: the same score means the
same risk in both groups, so PPV is equal
(Northpointe: Dieterich et al. 2016, with
equal AUC, 'accuracy equity').
Error-rate balance: equal FPR and equal FNR
in both groups (ProPublica: Angwin et al.
2016).  When base rates differ and prediction
is not perfect, these cannot all hold at once:
Chouldechova (2017) for PPV, FPR and FNR;
Kleinberg, Mullainathan & Raghavan (2016) for
calibration vs equal average scores among Y=1
and among Y=0.  Both sides' numbers can be
right at once: different questions.
Page 6/8, any key = next, Esc = leave
```

### After (beta 1f)

```text
RiskLab help 2/8: Separation, collinearity
If some x (or a mix of x) puts every Y = 1 above every Y = 0, the
likelihood keeps rising as |b| grows: no finite estimate
(Albert & Anderson 1984).  RiskLab warns when the fit has not
converged in 25 steps, the fitted line orders Y perfectly, or I
turns singular.  Remedies: drop or merge that x, or a penalised
(Firth) fit, not offered here.
Collinear x (one a mix of the others) make I singular too: no SEs.
Speed: each step of the fit goes through every row; Rossi's 432
rows need about 7 passes.  On a G1 that is slow (a progress bar
shows it; Esc stops it).
Page 2/8, any key = next, Esc = leave
```

```text
RiskLab help 4/8: Cut-offs and trade-offs
A lower cut-off flags more people: more TP (sensitivity up) and
more FP (specificity down).  No cut-off avoids both errors.
PPV = TP/(TP + FP): of those flagged, the share with Y = 1.  It
depends on the base rate: the same sensitivity and specificity
give a lower PPV where Y = 1 is rarer.
NPV = TN/(TN + FN).
Choosing a cut-off is choosing which error matters more: the
statistics show the trade-off, but they cannot say which error
is worse.
COMPAS deciles: 1-4 low, 5-7 medium, 8-10 high; ProPublica
took 5 and up as high risk.
Page 4/8, any key = next, Esc = leave
```

```text
RiskLab help 5/8: Calibration, H-L test
Calibrated: of people given P = 0.3, about 30% have Y = 1.
RiskLab sorts by predicted P into 10 groups (ties kept together),
or one group per score level, and compares observed O with
expected E = sum of P in each group:
HL = sum of (O - E)²/(E(1 - E/n)), df = groups - 2
(Hosmer & Lemeshow 1980).  Weaknesses: it depends on the
number of groups and on how ties are cut (software differs); it
has low power with small n, and with large n a tiny misfit is
'significant' (Hosmer et al. 1997).
A large p is no proof of good calibration.
Gray bars: pred ± 1.96 SE, a rough guide.
For a score such as COMPAS's, pred is the P from RiskLab's own
logistic fit of Y on the score.
Page 5/8, any key = next, Esc = leave
```

```text
RiskLab help 6/8: Fairness definitions
Predictive parity: the same score means the same risk in both
groups, so PPV is equal (Northpointe: Dieterich et al. 2016, with
equal AUC, 'accuracy equity').
Error-rate balance: equal FPR and equal FNR in both groups
(ProPublica: Angwin et al.
2016).  When base rates differ and prediction is not perfect,
these cannot all hold at once:
Chouldechova (2017) for PPV, FPR and FNR;
Kleinberg, Mullainathan & Raghavan (2016) for calibration vs
equal average scores among Y=1 and among Y=0.  Both sides'
numbers can be right at once, because they answer different
questions.
Page 6/8, any key = next, Esc = leave
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1e; lint_ppl 6 problems, as in beta 1e (6); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 8 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
