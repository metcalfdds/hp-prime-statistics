# FitCheck beta 1f: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes FitCheck beta 1f from FitCheck beta 1e. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 3, 5 and 6 reworded: when the chi-square p can be trusted, the Q-Q line, Anderson-Darling's tails and the Castaneda reasoning in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 8 screens, as the PC harness counts them.

3. **Outside the help** only these lines changed (the version on screen, and the page numbers the help's callers ask for):

```text
fc_Opening     -  fc_Frame("FitCheck - beta 1e");
fc_Opening     +  fc_Frame("FitCheck - beta 1f");
```

Routines touched, with the number of new or changed lines in each: (comments) 7, fc_Help 4, fc_Opening 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 3 of 8 screens changed; 5 kept their words.

### Before (beta 1e)

```text
FitCheck help 3/8: Small counts and Merge
The curve is only a fair guide when the E are 
not too small: every E ≥ 5, or Cochran's rule 
(at most 20% of the E below 5 and none below 
1).  FitCheck checks EVERY cell.  If the rule 
fails, Merge joins neighboring cells, the 
smallest E first, and the Test page names 
exactly which cells were merged (Unmrg undoes 
it).
page 3 of 8, any key or tap = next, Esc = menu
```

```text
FitCheck help 5/8: Normality
NORMALITY.  Q-Q plot: each value against its 
normal score z (Blom: the N(0,1) quantile at 
(i - 3/8)/(n + 1/4)); a normal sample hugs the 
line x̄ + s z.  Shapiro-Wilk W (Royston 1995): 
close to 1 for normal data.  Anderson-Darling 
A² with the correction for estimated μ and σ 
(D'Agostino & Stephens 1986): weights the 
tails.  Lilliefors D: the largest gap between 
the ECDF and the fitted normal CDF (ECDF 
page), p by Dallal & Wilkinson (1986), given 
for n ≥ 5 and only below 0.10.  χ² on bins: df 
= k - 3.
page 5 of 8, any key or tap = next, Esc = menu
```

```text
FitCheck help 6/8: Reading p; the exact test
A small p is evidence against normality; a 
large p is NOT proof of it.  With a big n, 
tiny departures give tiny p: the Q-Q plot 
shows how big the departure is.
EXACT BINOMIAL TEST.  X ~ Binomial(n, p₀).  
The two-sided p adds P(X = k) over every k no 
more likely than the observed x (R's 
binom.test, SciPy's binomtest).  Everything is 
done in logs, so a p of 10^-145 (Castaneda) is 
still printed as a number.  The plot puts x on 
a scale of SDs from E (the Castaneda 
reasoning).
page 6 of 8, any key or tap = next, Esc = menu
```

### After (beta 1f)

```text
FitCheck help 3/8: Small counts and Merge
The χ² curve gives a trustworthy p only when 
the E are not too small: every E ≥ 5, or 
Cochran's rule (at most 20% of the E below 5 
and none below 1).  FitCheck checks EVERY 
cell.  If the rule fails, Merge joins 
neighboring cells, the smallest E first, and 
the Test page names exactly which cells were 
merged (Unmrg undoes it).
page 3 of 8, any key or tap = next, Esc = menu
```

```text
FitCheck help 5/8: Normality
NORMALITY.  Q-Q plot: each value against its 
normal score z (Blom: the N(0,1) quantile at 
(i - 3/8)/(n + 1/4)); a normal sample lies 
close to the line x̄ + s z.  Shapiro-Wilk W 
(Royston 1995): close to 1 for normal data.  
Anderson-Darling A² with the correction for 
estimated μ and σ (D'Agostino & Stephens 
1986): gives extra weight to the tails.  
Lilliefors D: the largest gap between the ECDF 
and the fitted normal CDF (ECDF page), p by 
Dallal & Wilkinson (1986), given for n ≥ 5 and 
only below 0.10.  χ² on bins: df = k - 3.
page 5 of 8, any key or tap = next, Esc = menu
```

```text
FitCheck help 6/8: Reading p; the exact test
A small p is evidence against normality; a 
large p is NOT proof of it.  With a big n, 
tiny departures give tiny p: the Q-Q plot 
shows how big the departure is.
EXACT BINOMIAL TEST.  X ~ Binomial(n, p₀).  
The two-sided p adds P(X = k) over every k no 
more likely than the observed x (R's 
binom.test, SciPy's binomtest).  Everything is 
done in logs, so a p of 10^-145 (the Castaneda 
jury preset) is still printed as a number.  
The plot shows how many SDs x is from E, the 
reasoning the Supreme Court used in Castaneda 
v. Partida (1977).
page 6 of 8, any key or tap = next, Esc = menu
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1e; lint_ppl 9 problems, as in beta 1e (9); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 8 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
