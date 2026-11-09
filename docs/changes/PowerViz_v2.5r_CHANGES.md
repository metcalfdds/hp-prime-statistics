# PowerViz v2.5r: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes PowerViz v2.5r from PowerViz v2.5q. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 to 5 reworded: the alpha steps, the drag, the n formula and Levene's test in plain words.  The help is now 7 pages (was 5).

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is 7 screens (was 5), as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 11, pv_ShowHelp 75.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 7 of 7 screens changed; 0 kept their words.

### Before (v2.5q)

```text
PowerViz help 1/5: Keys
SOFT KEYS (the strip along the bottom):
Edit = all values,  Tails = 1- or 2-sided
α− / α+ = α ladder .001 .005 .01 .02 .05 .10 .20
Pow-n = power vs n (touch the curve to pick n)
Menu = effect-size view, n formula, test, help
LIVE CONTROLS (keys):
LEFT/RIGHT = effect size,  UP/DOWN = n per group
+/- = α ladder,  0 = re-fit the window
Enter = menu,  Esc = exit and export
d, h = Cohen's standardized effect
  .2 small  .5 medium  .8 large  (below .2: tiny)
SE₀ = the H₀ curve's SE, from σ (or p) and n
t(df) = t obtained if a sample had these values
Teaching aid; not for clinical or legal use.
any key or tap = next page
```

```text
PowerViz help 2/5: Touch
DRAG ON THE PLOT:
sideways near H₁ = move the alternative
the dashed red line = set α by hand; on lift
  it snaps to the ladder if within 15 %
up or down = n (one step per 12 px)
TAP THE READOUT:
n = type n;  μ, p, d or h = type the effect
α, zcrit = the α ladder;  σ, μ₀, p₀ = Edit form
THE PICTURE:
blue = H₀, magenta = H₁, pale magenta = H₁ before
red = α, yellow = β, green = power, dashes = crit
n₈₀ = smallest n per group with power of 0.80
  or more (a green dotted line in Pow-n)
magenta arrow: the effect, d (or h), on the plot
any key or tap = next page
```

```text
PowerViz help 3/5: The n formula
n₈₀ = 56 (55.6): 56 is found by TRYING n = 2, 3 ...
  with the power engine; 55.6 is the FORMULA's n.
Tap that line (or Menu, Sample-size formula):
  the power equation (μ₁−μ₀ − zα SE₀)/SE₁ = zβ,
  solved for n by the CAS with zα, zβ as symbols,
  then your σ and means put in exactly (CAS),
  then the z values put in (PPL): the number.
Round UP: 55.6 people means 56.
1-sided: the formula is exact, so they agree.
2-sided: it drops the far tail, so n₈₀ can be
  one smaller than the rounded formula.
exact (CAS) = the CAS did the algebra; decimal =
  no CAS: the formula is shown as texts print it.
any key or tap = next page
```

```text
PowerViz help 4/5: Unequal σ and n
TWO MEANS, UNEQUAL σ & n (the 3rd test):
each group has its own σ and n, so
  SE = √(σ₁²/n₁ + σ₂²/n₂); box: n, μ, σ by group
UP/DOWN, a drag and Pow-n change n₁; n₂ keeps
  the ratio n₂/n₁ you typed (Edit, or tap n =)
d = (μ₂−μ₁)/σ',  σ' = √((σ₁²+σ₂²)/2)  (Cohen)
BEST SPLIT of a fixed total: n₂/n₁ = σ₂/σ₁
  (more people where σ is larger)
Unequal σ AND unequal n: the pooled t-test's α
  and power can be far off (Cohen 1988, p. 44).
  This test does not pool: its SE is Welch's.
z test: σ₁, σ₂ taken as known. Welch's t-test
  estimates them: less power when n is small.
n₈₀ = 40, 20: smallest n₁, n₂ with power ≥ 0.80
any key or tap = next page
```

```text
PowerViz help 5/5: Levene, data
MENU, Would Levene notice? (unequal σ test):
  if σ₁ and σ₂ are as typed, how often would
  Levene's test notice at your n? (A plan.)
  It cannot give SPSS's Levene F: that F needs
  every score; PowerViz has means, SDs and n.
MENU, Two samples: data:
  Levene's test, the pooled and Welch t-tests
  and Cohen's d for two real samples: the 1970
  draft lottery, two insect sprays, or yours:
  group 1 in D1, group 2 in D2 (Apps,
  Statistics 1Var, Num).
The magenta arrow on the plot: the gap between
  the means; d is that gap in SD units.
any key or tap = back
```

### After (v2.5r)

```text
PowerViz help 1/7: Keys
SOFT KEYS (the strip along the bottom):
Edit = all values,  Tails = 1- or 2-sided
α− / α+ = step α through .001 .005 .01 .02 .05 .10 .20
Pow-n = power vs n (touch the curve to pick n)
Menu = effect-size view, n formula, test, help
LIVE CONTROLS (keys):
Teaching aid; not for clinical or legal use.
any key or tap = next page
```

```text
PowerViz help 2/7: Keys (continued)
LEFT/RIGHT = effect size,  UP/DOWN = n per group
+/- = step α through those values,  0 = redraw the plot to fit
Enter = menu,  Esc = quit; the results stay in Home (EP_PWR
and the rest)
d, h = Cohen's standardized effect .2 small  .5 medium  .8 large
  (below .2: tiny)
SE₀ = the H₀ curve's SE, from σ (or p) and n
t(df) = the t that a sample with exactly these values would give
any key or tap = next page
```

```text
PowerViz help 3/7: Touch
DRAG ON THE PLOT:
sideways near H₁ = move the alternative the dashed red line = set
α by hand; when you lift your finger, α jumps to the nearest of
those values if it is within 15 % of it up or down = change n (one
step for every 12 pixels)
TAP THE READOUT:
n = type n;  μ, p, d or h = type the effect
any key or tap = next page
```

```text
PowerViz help 4/7: Touch (continued)
α, zcrit = step through the α values;  σ, μ₀, p₀ = Edit form
THE PICTURE:
blue = H₀, magenta = H₁, pale magenta = H₁ before your
last change
red = α, yellow = β, green = power, dashes = crit
n₈₀ = smallest n per group with power of 0.80 or more (a green
  dotted line in Pow-n)
magenta arrow: the effect, d (or h), on the plot
any key or tap = next page
```

```text
PowerViz help 5/7: The n formula
n₈₀ = 56 (55.6): 56 is found by TRYING n = 2, 3 ... with the power
  engine; 55.6 is the FORMULA's n.
Tap that line (or Menu, Sample-size formula):
  the power equation (μ₁−μ₀ − zα SE₀)/SE₁ = zβ, solved for n by the
  CAS with zα, zβ as symbols, then your σ and means put in
  exactly (CAS), then the program puts in the z values (PPL), giving
  the number.
Round UP: 55.6 people means 56.
1-sided: the formula is exact, so they agree.
2-sided: the formula leaves out the tail on the far side, so n₈₀ can
  be one smaller than the rounded formula.
exact (CAS) = the CAS did the algebra; decimal = no CAS: the
  formula is shown as textbooks print it.
any key or tap = next page
```

```text
PowerViz help 6/7: Unequal σ and n
TWO MEANS, UNEQUAL σ & n (the 3rd test):
each group has its own σ and n, so SE = √(σ₁²/n₁ + σ₂²/n₂); the
  box shows n, μ and σ for each group
UP/DOWN, a drag and Pow-n change n₁; n₂ keeps the ratio n₂/n₁
  you typed (Edit, or tap n =)
d = (μ₂−μ₁)/σ',  σ' = √((σ₁²+σ₂²)/2)  (Cohen)
BEST SPLIT of a fixed total: n₂/n₁ = σ₂/σ₁ (more people where σ
  is larger)
Unequal σ AND unequal n: the pooled t-test's α and power can
  be far off (Cohen 1988, p. 44). This test does not pool: its SE
  is Welch's.
z test: σ₁, σ₂ taken as known. Welch's t-test estimates them: less
  power when n is small.
n₈₀ = 40, 20: smallest n₁, n₂ with power ≥ 0.80
any key or tap = next page
```

```text
PowerViz help 7/7: Levene, data
MENU, Would Levene notice? (unequal σ test):
  if σ₁ and σ₂ are as typed, how often would Levene's test detect
  the difference at your n? (For planning a study.)
  It cannot give SPSS's Levene F: that F needs every score;
  PowerViz has means, SDs and n.
MENU, Two samples: data:
  Levene's test, the pooled and Welch t-tests and Cohen's d for
  two real samples: the 1970 draft lottery, two insect sprays,
  or yours:
  group 1 in D1, group 2 in D2 (Apps, Statistics 1Var, Num).
The magenta arrow on the plot: the gap between the means; d is
  that gap in SD units.
any key or tap = back
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in v2.5q; lint_ppl 12 problems, as in v2.5q (12); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py` (the old help with the approved changes applied, word for word against the new): the only difference is the order of the disclaimer line, which the build keeps out of the moved text and puts back at the foot of its page.
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 7 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".
- `tools/monkey_v1b.py --lists`, 1,000 runs of 120 random keys, taps, menu picks and typed values (912 s): OK 1,000.

Not yet run on a G1 or a G2.
