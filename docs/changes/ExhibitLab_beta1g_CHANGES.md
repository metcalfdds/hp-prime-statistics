# ExhibitLab beta 1g: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes ExhibitLab beta 1g from ExhibitLab beta 1f. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1, 2, 3 and 7 reworded: what the claim means, the two kinds of answer, the finite-population correction and the keys in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 8 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, sz_Help 35.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 4 of 8 screens changed; 4 kept their words.

### Before (beta 1f)

```text
ExhibitLab help 1/8: What the claim means
'At least 90% are drug, at 95% confidence':
if fewer than 90% of the N units held drug,
a random sample of this size would come out
this clean (this few negatives or fewer) at
most 5% of the time: the METHOD rarely backs
a false claim.  It does NOT mean: a 95%
probability that 90% are drug (a Bayesian
statement, page 2); that the untested units
were analyzed; that a given unit is drug;
anything about weight or purity.
'90%' of 100 units means at least 90 units.
Any key = page 2, Esc = menu
```

```text
ExhibitLab help 2/8: Frequentist or Bayesian?
Hypergeometric (frequentist): a statement
about the PROCEDURE.  Suppose the claim is
just false (K₀ drug units); if what you found
would then be rare (P ≤ 1 - c), it is
supported.  Bayesian (Aitken 1999; ENFSI
2009): about THIS SEIZURE: P(at least p₀N
are drug | what you found).  It needs a prior
: uniform Beta(1, 1) treats every proportion
as equally likely; Jeffreys Beta(0.5, 0.5)
leans to all or none.  The prior matters most
when n is small.  Say which one you used.
Any key = page 3, Esc = menu
```

```text
ExhibitLab help 3/8: Why N hardly matters
Taking n units out of N barely changes what
is left when N is much bigger than n: the
hypergeometric becomes the binomial, which
does not depend on N.  p₀ = 0.90, c = 0.95,
no negatives: least n 8 at N = 10, 23 at
N = 100, never more than 29 however big N is
(computed now; see Tables).
A small seizure needs a large FRACTION
tested; a large one about the same NUMBER.
On the OC page, as N grows, the magenta
staircase settles onto the blue binomial.
Any key = page 4, Esc = menu
```

```text
ExhibitLab help 7/8: Keys and Home
Soft keys on every page; Menu or Enter opens
the page menu (more, and Main menu); Esc =
back to the main menu.  Tap a bar or curve.
Hypergeometric: +/- = n, Up/Down = n by 10,
Left/Right = x.  Bayes: +/- = n, Left/Right
= x.  Binomial: Up/Down = negatives allowed,
Left/Right = N / 10, N × 10.
OC: +/- = n, Left/Right = θ, Up/Down = neg;
drag the red knob (n) or the red line (θ).
Tables: Left/Right = table or plot.
Long sums show a moving bar; Esc stops them.
Home: EX_N EX_NMIN EX_P EX_LB EX_PB
EX_TOT EX_TLB.
Any key = page 8, Esc = menu
```

### After (beta 1g)

```text
ExhibitLab help 1/8: What the claim means
'At least 90% are drug, at 95% confidence':
if fewer than 90% of the N units held drug, a random sample of
this size would show this few negatives (or fewer) at most 5% of
the time: the METHOD rarely supports a false claim.  It does NOT
mean: a 95% probability that 90% are drug (a Bayesian
statement, page 2); that the untested units were analyzed; that a
given unit is drug;
anything about weight or purity.
'90%' of 100 units means at least 90 units.
Any key = page 2, Esc = menu
```

```text
ExhibitLab help 2/8: Frequentist or Bayesian?
Hypergeometric (frequentist): a statement about the PROCEDURE.
Suppose the claim is false by the smallest margin (K₀ drug
units); if what you found would then be rare (P ≤ 1 - c), it is
supported.  Bayesian (Aitken 1999; ENFSI 2009): about THIS
SEIZURE: P(at least p₀N are drug | what you found).  It needs a
prior : uniform Beta(1, 1) treats every proportion as equally
likely; Jeffreys Beta(0.5, 0.5) gives more weight to proportions
near 0 and 1.  The prior matters most when n is small.  Say
which one you used.
Any key = page 3, Esc = menu
```

```text
ExhibitLab help 3/8: Why N hardly matters
Taking n units out of N barely changes what is left when N is
much bigger than n: the hypergeometric becomes the binomial,
which does not depend on N.  p₀ = 0.90, c = 0.95, no negatives:
the smallest n is 8 at N = 10, 23 at N = 100, never
more than 29 however big N is (computed now; see Tables).
A small seizure needs a large FRACTION tested; a large one about
the same NUMBER.
On the OC page, as N grows, the magenta steps (the
hypergeometric) come to lie on the blue binomial curve.
Any key = page 4, Esc = menu
```

```text
ExhibitLab help 7/8: Keys and Home
Soft keys on every page; Menu or Enter opens the page menu
(more, and Main menu); Esc = back to the main menu.  Tap a
bar or curve.
Hypergeometric: +/- = n, Up/Down = n by 10,
Left/Right = x.  Bayes: +/- = n, Left/Right = x.  Binomial:
Up/Down = negatives allowed, Left/Right = N / 10, N × 10.
OC: +/- = n, Left/Right = θ, Up/Down = negatives allowed;
drag the red knob (n) or the red line (θ).
Tables: Left/Right = table or plot.
Long sums show a moving bar; Esc stops them.
Home: EX_N EX_NMIN EX_P EX_LB EX_PB EX_TOT EX_TLB.
Any key = page 8, Esc = menu
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1f; lint_ppl 6 problems, as in beta 1f (6); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 8 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
