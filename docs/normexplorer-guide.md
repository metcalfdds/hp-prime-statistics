# Norm Explorer — User's Guide

Sep 17, 2026 · Roger Dale Metcalf Sr

*HP Prime graphing calculator · beta 39a*

## What Norm Explorer is

Norm Explorer is a normal-distribution workbench for the HP Prime. It does the ordinary work of a normal table — probabilities, percentiles, critical values, z-scores — and draws every answer on the curve, shaded, so the number and the picture arrive together.

It is meant to be looked at as much as calculated with. Every result screen ends by showing the shaded region that produced the number, and three of its features exist mainly to be watched: the standardize animation, the two-curve effect-size view, and the simulated sample histogram.

### Why μ and σ, and not x̄ and s

Throughout this program you type μ and σ, never x̄ and s. That is deliberate. When you enter N(100, 15) you are *declaring a population* — stating that scores are distributed this way — and every probability the calculator returns is an exact area under that curve. Population parameters take Greek letters, so μ and σ are the correct symbols here.

x̄ and s are what you compute *from data you collected*, as estimates of a μ and σ you do not know. They appear in menu 6, which fits a curve to a sample — simulated, or your own data from the Statistics apps — and reports the sample's x̄ and s beside the μ and σ of the fitted curve.

### Installing it

The program ships as a plain text file. Open the HP Prime Connectivity Kit, create a new program in the Program Catalog, and paste the whole file in.

It needs no libraries and no setup. It will use the calculator's MicroPython to draw large samples quickly if the firmware has it, and fall back to pure PPL if not, so it runs on any Prime.

### Launching it

Run `NormExp()` from the Program Catalog, or type `NormExp()` in Home and press Enter. The main menu appears immediately.

Every launch starts from the standard normal, N(0, 1), with no shading, no sample and no second curve. Quitting resets it the same way, so the next person to open it does not inherit the last session's numbers.

## The main menu

The menu title always shows the distribution currently in force — for example **NormExp — N(100.00, 15.00)** — so you can see at a glance what the next calculation will be based on.

| # | Item | What it does |
| --- | --- | --- |
| 1 | Set μ and σ | Type the session distribution |
| 2 | Explore the curve | Live keys, and touch the plot to set a cut point |
| 3 | Probability from x | Area left, right, between, or outside |
| 4 | x from probability | Percentile, critical value, central interval |
| 5 | Z-formula solver | Any three of z, x, μ, σ → the fourth |
| 6 | Data & histogram | Your own data from the Statistics apps, or a simulated sample |
| 7 | Compare curves | Second curve and Cohen's d |
| 8 | Standardize animation | Morphs N(μ, σ) into N(0, 1) |
| 9 | Plot window & display | Range, band and reference toggles, reset |
| 10 | Help | Two on-screen reference pages |

Selecting **Quit**, or pressing Esc at the menu, leaves the program.

### One distribution, shared by everything

The program holds a single distribution for the whole session. Set μ and σ once and every module uses them: the probability calculations, the inverse calculations, the histogram, the plot. The solver in item 5 both reads it and writes back to it, so a value solved there becomes the distribution on the plot.

The practical consequence is that you rarely retype anything. Set N(100, 15) once and you can work through a dozen questions about it without touching μ or σ again.

Shading persists too. Compute a probability, go into the Explorer, and the shaded region is still there.

## 1 · Setting μ and σ

Two boxes, prefilled with the current values. Any mean works, and any positive standard deviation.

The plot window rescales itself to whatever you enter, so real distributions display properly: N(100, 15) for IQ, N(2.4, 0.6) for GPA, N(847, 220) for reaction times in milliseconds, N(0.5, 0.02) for a proportion. Axis labels and tick spacing adjust with the scale.

A negative or zero σ is rejected with a message rather than producing a broken plot.

**Changing the distribution clears any shading and any sample.** Those belonged to the old curve and would be misleading against the new one. This is deliberate, not a glitch — recompute the probability you want after changing μ or σ.

## 3 · Probability from x

Given a cut point, what is the area? Four choices:

| Choice | Computes | Shades |
| --- | --- | --- |
| P(X < x) | Left tail | Everything below x |
| P(X > x) | Right tail | Everything above x |
| P(a < X < b) | Between | The middle band |
| P(outside a, b) | Two tails | Both ends |

Boundary boxes start at 0 — type your own value. If you enter b below a in the two-boundary modes, they are swapped for you.

The result panel gives the raw score, its z-score, the probability, and the complement. Press any key and the same result appears shaded on the curve, with the numbers repeated in the corner.

**Worked example.** IQ is N(100, 15). What proportion scores above 130?

1. Menu 1 → μ = 100, σ = 15
2. Menu 3 → P(X > x) → x = 130
3. Panel reads z = 2.0000, P(X > x) = 0.0228
4. Any key → the top 2.28% shaded orange, with a red line at 130

The two-tail option is the one to reach for with a two-tailed test: enter the two critical values and the shaded region is the rejection region.

*Note:* leaving both boundaries at 0 in the between/outside modes gives an interval of zero width — P(between) = 0, P(outside) = 1. Correct, but not interesting until you enter real bounds.

## 4 · x from probability

The inverse direction: given an area, what is the score? Three choices.

**x at a percentile.** Enter the area to the *left*, get the raw score and its z. Default 0.90. On N(100, 15), an area of 0.90 returns x = 119.22 — the 90th percentile.

**Critical value.** Enter α as the area in the *right* tail, get z\* and x\*. Default 0.05, which returns the familiar z\* = 1.6449. The shaded region is the one-tailed rejection region.

**Central interval.** Enter a central proportion and get ±z\* and both endpoints. Accepts either 0.95 or 95. At 0.95 you get z\* = ±1.9600 and both bounds marked on the curve.

This is *not* a confidence interval, and the difference matters. What you get here is the middle 95% of the distribution itself — the range a single observation falls in 95% of the time. A confidence interval is built from a sample to estimate an unknown parameter, and uses a standard error in place of σ. The ±1.96 looks the same in both, which is exactly why they are so easily confused.

Note the asymmetry, which trips people up: percentile asks for the area to the **left**, critical value asks for the area to the **right**. That matches how each is normally used and how printed tables present them, but they are easy to confuse. The help line under each box tells you which one it wants.

Each of these ends with the shaded picture, so the interval or tail is visible, not just tabulated.

## 5 · The z-formula solver

z = (x − μ)/σ has four quantities. Know any three and the fourth follows. This module solves for whichever one you choose.

**It works in two steps.** First a menu asks which quantity is *unknown*. Then three boxes appear — for the three you did not pick. That is why you see only three fields: the fourth is the answer.

Press OK and a full-screen panel shows all four values, with **the solved one in red**, and underneath it the rearranged formula with your numbers substituted in:

| Solving for | Formula shown |
| --- | --- |
| z | z = (x − μ)/σ |
| x | x = μ + zσ |
| μ | μ = x − zσ |
| σ | σ = (x − μ)/z |

The rearrangement is worth reading, not skipping. Finding a z-score is easy enough; rearranging the same formula to recover μ or σ is where most of the difficulty lives, and the panel shows you the algebra rather than only the answer.

### Values carry over

μ and σ arrive from the session distribution, so whatever you set in menu 1 is already in the boxes. x and z persist from your last visit. Anything you enter or solve for flows back out to the session, so the plotted curve follows along.

In practice: solve for z with x = 115, μ = 100, σ = 15 → z = 1. Go back in, switch to solving for x, and μ, σ and z are still filled in. Change z to 1.96 and you get x = 129.4 without retyping anything.

At launch all four sit at x = 0, μ = 0, σ = 1, z = 0 — values that satisfy the formula exactly.

### Two guards

σ must be positive. And σ cannot be found when z = 0, since that divides by zero; the message says so. If your entries give a negative σ, the program explains that the sign of z must match the sign of x − μ — a common and instructive student error.

## 2 · Exploring the curve

This is the live view. The keys act immediately and the plot redraws on each press.

| Key | Effect |
| --- | --- |
| ← → | Move the mean, in round steps |
| ↑ ↓ | Change the std dev, in round steps |
| **Tap or drag on the plot** | **Set the cut point where you touch** |
| + | Toggle the 68–95–99.7 bands |
| − | Toggle the N(0,1) reference curve |
| 0 | Re-centre the window on the current curve |
| Esc or Enter | Back to the menu |

Step sizes scale with σ, so the arrows feel the same whether you are on N(0, 1) or N(500, 100).

### Why the window holds still

On entry the window locks to roughly ±6σ around the starting distribution and stays there while you explore. This is deliberate. If the window followed μ, the bell would sit dead centre forever and moving the mean would look like nothing was happening. With the window held, μ visibly slides and σ visibly reshapes — which is what you want a class to see.

Wander too far and press **0** to re-centre.

## 6, 7 and 8 · The demonstration modules

### 7 · Compare curves and Cohen's d

Enter a second mean, μ₂, and a green curve appears alongside the first, sharing the same σ. The overlap is shaded pale green, and the readout gives **d = (μ₂ − μ)/σ**.

This turns effect size from a number into something you can see. Set μ = 0, σ = 1, then try μ₂ = 0.2, 0.5 and 0.8 in turn — the conventional small, medium and large — and watch the overlap shrink. If you have only ever met Cohen's d as a figure in a results table, the picture is usually more convincing.

### 6 · Data & histogram

This is where the program reaches into the calculator's built-in Statistics apps and works with real data, rather than only with a distribution you describe. Seven options.

**My data from D1.** Reads list D1 of the Statistics 1Var app — the same list the Technology Corner activities use — computes x̄ and s, fits N(x̄, s) to them, and draws your values as bars against that curve. Data already entered to make a Normal probability plot needs no retyping.

**Two groups from C1, C2.** Reads two groups from the Statistics 2Var app, fits a curve to each, and reports Cohen's d. Both curves are drawn with the **pooled** standard deviation, sp = √(((n₁−1)s₁² + (n₂−1)s₂²)/(n₁+n₂−2)) — the standard denominator for d, and the only thing the plot can show, since it draws one σ. The histogram is cleared, because one set of bars under two curves would look like it belonged to both.

**Regression residuals from C1, C2.** Fits the least-squares line of C2 on C1 and runs the residuals through the same normality view. Inference about a slope assumes the residuals are roughly normal, and this is the assumption students are usually told about rather than shown. A useful check: the residual mean should read 0.0000.

**Write z-scores of D1 into D2.** Standardizes your data and stores the result in D2, where every other app can reach it. A message confirms n, x̄ and s.

**Normal probability plot of D1.** Opens Statistics 1Var with your data in place. Set Plot1 to Normal Probability in Symbolic view, then Plot and Autoscale. This *leaves* NormExplorer — control passes to the Statistics app.

**Simulate a sample.** The original behaviour: a random sample of n = 200, 1000 or 5000 drawn from the current distribution. The point is sampling variability — at n = 200 the bars wobble around the curve, at n = 5000 they hug it, and drawing the same n repeatedly gives a different picture every time.

**Clear histogram.** Removes the bars.

Whichever route the data came from, the plot reports the sample's own **x̄ and s** stacked beneath the population μ and σ — x̄ under μ, s under σ, each estimate under the parameter it estimates. The readout says "your data" for real values and "sample" for simulated ones. Bins are 32 intervals across μ ± 4σ, so bar width scales with the distribution.

### 8 · Standardize animation

Animates your N(μ, σ) transforming into the Standard N(0, 1) in two labelled stages: first the curve slides until μ = 0, then it rescales until σ = 1. A pause between the two marks where subtracting the mean ends and dividing by the standard deviation begins.

It runs about eleven seconds. Watch the μ and σ readouts change as it goes — that is the substance of the demonstration, not the motion itself. There is no key to press; it advances on its own.

## Reading the plot

| What you see | Meaning |
| --- | --- |
| Blue curve | The session distribution N(μ, σ) |
| Dark blue vertical line, marked μ | The mean, drawn from the axis up to the peak |
| Blue bands, three shades | ±1σ, ±2σ, ±3σ — darkest nearest the mean |
| Orange fill | The region whose probability was just computed |
| Red vertical lines | The boundaries of that region |
| Green curve | The comparison curve N(μ₂, σ) |
| Pale green fill | Overlap of the two curves |
| Green outline bars | The sample — simulated, or your own data |
| Grey curve | N(0, 1) reference, when it fits |

The corner readouts give μ and σ; the sample's x̄ and s when a histogram is drawn; μ₂ and Cohen's d when a second curve is on; the band ranges when bands are on and no second curve; and the current probability with its z-score when a region is shaded.

### The band percentages

The band labels read 68.27%, 95.45% and 99.73% rather than the rounded 68–95–99.7. These exact figures are what the calculator computes; the familiar rule is a rounding of them, not a separate fact.

The labels are hidden while a second curve is on, because they would overlap its μ₂ marker and because the ranges describe one distribution only. The shaded bands themselves stay.

### The footer line

On a result view the footer reads *Press any key to return to the menu*, because that is all any key does there. Inside the Explorer it lists the live keys instead. If the footer offers you arrow keys, they work; if it does not, they do not.

## 9 · Plot window & display

Everything about how the plot looks, gathered in one place. Seven options.

**Auto (μ ± 4σ)** is the default and suits almost everything. **Wide (μ ± 6σ)** brings more of the tails into view, or leaves room for a mean to move. **Custom** takes an explicit xmin and xmax — useful for putting two screens on identical axes, or zooming into a tail. A custom range is dropped automatically if you change μ or σ, since it would no longer fit.

In auto and wide mode the window also widens on its own to take in anything being shaded and any second curve, so a critical value far out in a tail is never off the edge.

**Bands 68-95-99.7** and **N(0,1) reference curve** switch those layers on and off. Each line shows its current state before you choose it, and the plot redraws straight away so you see the effect. These are the same two switches the Explorer's **+** and **−** keys drive — having them here means you can clear the bands off a busy result plot without detouring through the Explorer to do it.

**Show current window** reports the range, its width in units and in σ, and the vertical scale.

**Reset everything to N(0,1)** returns the session to its launch state: standard normal, no shading, no sample, no second curve, auto window, solver cleared. Handy between worked examples — it saves quitting and relaunching just to get a clean slate.

### Why the grey reference curve sometimes vanishes

The N(0, 1) reference curve is drawn only when it genuinely fits — horizontally *and* vertically.

The standard normal peaks at 0.3989. A distribution with σ = 7 peaks at 0.057, about seven times shorter. Drawn together on one vertical scale, N(0, 1) would be clipped flat at the top of the frame and appear as a grey box rather than a bell.

So the reference curve appears for σ up to about 1.15 and is suppressed above that. A comparison nobody can interpret is worse than no comparison.

The practical consequence: at large σ, both the Explorer's **−** key and the menu 9 toggle will seem to do nothing. They are still flipping the setting; there is simply nothing that can be drawn.

## Things to try

Six short exercises. Each takes a few minutes, and each shows you something the formula alone does not.

### The empirical rule is not three separate facts

Set any μ and σ in menu 1, then go into the Explorer and press **+** to turn on the bands. Now move μ with the arrows and change σ, and watch carefully: the *ranges* under the bands change every time, but the *percentages* never do — 68.27, 95.45, 99.73, always.

That is the whole rule. It is not about particular numbers; it is about how many standard deviations you are from the mean.

### Why we standardize

Set N(100, 15) in menu 1 — the IQ scale — then run the animation in menu 8. Your curve slides until its mean is 0, then shrinks until its spread is 1.

That is exactly what z = (x − μ)/σ does to a single score. Now go to menu 5, solve for z with x = 130, and you will get 2 — the same journey, done to one number instead of the whole curve.

### The same z, two different worlds

In menu 5, solve for x with z = 1.5, μ = 100, σ = 15. You get 122.5.

Now do it again with μ = 2.4, σ = 0.6 — a GPA. You get 3.3.

Same z, completely different raw scores. Look at the plot after each: the shape is identical, only the numbers on the axis changed. A z-score tells you *where you stand*, not *how big you are*.

### A sample is not its population

Go to menu 6, choose Simulate a sample, and draw n = 200. Draw it again. And again. The bars land differently every time, even though the distribution underneath never moved.

Now draw n = 5000. The bars settle onto the curve.

Nothing changed except how much data you collected. This is what people mean when they say a small sample is unreliable — and it is worth remembering the next time you read a study.

### Effect size you can see

Set N(0, 1) in menu 1, then use menu 7 to add a second curve at μ₂ = 0.2. Note the d value in the corner. Try 0.5, then 0.8.

At each one, ask yourself: if someone handed you a single observation and asked which curve it came from, could you tell? That question is what effect size measures, and the overlap you can see is the honest answer.

Some figures to put against the picture. The shaded overlap is about **92%** of the area at d = 0.2, **80%** at d = 0.5, **69%** at d = 0.8, and still **32%** at d = 2. Even a very large effect leaves the two groups substantially overlapping — which is why an effect can be real, important, and still useless for telling one individual from another.

### Checking your own work

For any homework question of the form *what proportion is above / below / between*, use menu 1 to set the distribution and menu 3 to get the answer. Then look at the shaded picture and ask whether it matches what the question actually described.

If the question said "above" and your shading is on the left, you have carefully answered the wrong question. The picture catches that far faster than re-checking your arithmetic does.

### Is my own data normal?

Type a set of real values into list D1 of the Statistics 1Var app — heights, test scores, reaction times, anything you have collected. Then menu 6, *My data from D1*.

The program fits N(x̄, s) to your numbers and draws them against it. Ask whether the bars follow the curve: humped in the middle, thinning symmetrically at both ends. Then menu 6 again, *Normal probability plot of D1*, for the second opinion — the straighter that plot, the better the normal model fits.

Two tools, one question, and the answer is a judgement rather than a number.

## Notes, limits and troubleshooting

### Results available in Home

After any calculation, three variables hold the latest result and can be typed in Home:

| Variable | Holds |
| --- | --- |
| `NE_Z` | The last z-score |
| `NE_X` | The last raw score |
| `NE_P` | The last probability |

So a critical value can be computed in the program and then used in further arithmetic without copying it down. These are cleared when you quit.

### Known limits

**No blank input fields.** Every box shows a starting value, because the calculator cannot display an empty numeric field. Boundary and solver fields start at 0; area and confidence fields start at conventional values (0.90, 0.05, 0.95) because 0 is not a legal entry for them.

**One σ for both curves.** The comparison curve shares the main curve's standard deviation, so Cohen's d here assumes equal spread. When two real groups are loaded from C1 and C2 the pooled s is used, which is the standard approach; for a typed μ₂ the single session σ applies to both.

**Only D1, C1 and C2.** The data routes read those three lists specifically. Data in other columns has to be moved there first.

**The animation cannot be interrupted.** It runs its full course, about eleven seconds.

### If something looks wrong

**A stray grey shape on the plot** — that was the reference curve being clipped, fixed in this version. If you see it again, the N(0,1) suppression rule needs another look.

**"Invalid input" when drawing a histogram** — the MicroPython sampler failed and the fallback did not catch it. The Terminal (Shift-View) will show the Python error. Current versions validate the result and fall back to the PPL sampler, so this should not recur.

**A histogram that takes a long time** — the PPL fallback is running because the Python path failed. It works, but n = 5000 is slow. The Terminal will say why.

**A number you did not expect in a box** — check what the field's help line says it starts at. Prefilled values are deliberate, and several are 0 by design.

### Version

This guide describes beta 39a (the same code as beta 39). Menu numbering, key assignments and default values are as shipped in that build; earlier versions differ, particularly in the solver, the plot window and the menu order.

**Tested on:** an HP Prime G2 and G1, plus the desktop Virtual Calculator. Both calculators now run the 2026-09-09 firmware, though the G1 results recorded here were obtained before it was updated to that build. Behaviour on other firmware may differ — in particular, which characters render and which app variables a program can reach have both turned out to be firmware-dependent.

### Credit

The concept, the direction and the classroom judgement behind this program are Roger Metcalf's, as is every round of testing on real hardware — which is where most of what matters was found. Claude did the implementation, the numerical work, the expansion beyond the original scope, and this guide.

**Free for educational and personal use.** Share it, teach with it, adapt it for your own classroom. Please keep the attribution with the files and credit the author if you pass them on or build on them. Not for sale or commercial redistribution. Provided as is, with no warranty — check any result you intend to rely on.

© 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).
