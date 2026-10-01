# StudRange — User's Guide

Sep 27, 2026 · Roger Dale Metcalf Sr

*The studentized range (Tukey's q) on the HP Prime — p-values, critical values, and Tukey HSD*

*Describes StudRange beta 12 (PPL) and StudRangePy beta 14a (MicroPython), tested on an HP Prime G2 running the 2026-09-09 firmware — the G1 now runs the same build*

## What this is for

A one-way ANOVA tells you that at least one group mean differs from the others. It does not tell you **which** ones.

That is the question the studentized range answers. Its statistic, Tukey's q, is the distance between the largest and smallest of k sample means, divided by the standard error — the range of the means, studentized. Its distribution depends on two things: k, the number of groups being compared, and the error degrees of freedom from the ANOVA.

The practical payoff is **Tukey's HSD** — Honestly Significant Difference — a single number you compare against every pairwise difference of means. Any pair further apart than the HSD differs significantly, with the family-wise error rate held at α across all comparisons at once. That last part is why you use it instead of running a pile of t-tests: doing every pair separately at α = .05 inflates the chance of a false positive well past .05, and the studentized range distribution is built to absorb exactly that inflation.

So the usual sequence is: run the ANOVA, get a significant F, come here for the HSD, and compare your mean differences against it.

The program also works in both directions on the distribution itself — a p-value from an observed q, or a critical value from an α — which is what you need if you are checking a textbook table, or teaching where the numbers in that table come from.

## Two versions, same mathematics

There are two programs on the calculator. They compute the same quantities by the same algorithm; they differ in what runs the arithmetic.

|  | StudRange beta 12 | StudRangePy beta 14a |
| --- | --- | --- |
| Engine | PPL | MicroPython |
| Launch | `StudRange()` | `StudRangePy()` |
| Interface | CHOOSE menus, graphical | Terminal menu, typed choices |
| Modes | 5, including Help / About | 4 |
| Degrees of freedom | **3 or more** (0 means ∞) | **1 or more** |
| Groups k | 2–20 | 2–50 |
| p-value | about 1 second | near-instant |
| Critical value | around a minute | about 1.5 seconds |
| Needs Python firmware | No | Yes |
| Exports to Home | `EP_QPVAL`, `EP_QCRIT`, `EP_HSD` | — |

**Use StudRangePy for anything involving a critical value or an HSD.** The difference is not subtle: the PPL version finds a critical value by 60 steps of bisection, each step a full double integration. The Python version uses a secant solver that converges in about nine, and each one runs in compiled C rather than interpreted PPL. A minute becomes a second and a half.

**Use StudRange when you want the plot**, when you are on firmware without Python, or when you want the results left in `EP_QPVAL`, `EP_QCRIT` and `EP_HSD` for further work in Home.

**Use StudRangePy when df is below 3.** The PPL version inherits the 1977 program's restriction and will raise any df of 1 or 2 to 3, telling you it has done so. The Python version handles low df directly, which is what the u² substitution was added for.

Both accept the same inputs and report the same numbers, so you can move between them freely.

One practical note on the Python version: it runs in the **Terminal**, not on the graphics screen. Answers appear as printed text, and you type your choices at a `choice:` prompt rather than picking from a menu box.

## Working on the distribution

The first two menu options move in opposite directions across the same distribution.

### 1 · P-value from q

You have an observed q and want to know how extreme it is.

Enter **k**, the number of groups (2 to 50); **df**, the error degrees of freedom from your ANOVA table; and **q**, the observed statistic. You get back the upper-tail probability — the chance of a range this large or larger if every group mean were really the same.

A check worth running once, because it appears in every textbook table: k = 3, df = 10, q = 3.877 returns p = .05. That value is one of the classic Harter table entries, and seeing it come back confirms the engine is behaving.

### 2 · Critical value

The inverse, and the one you want more often.

Enter **k**, **df**, and **α** (between 0.000001 and 0.5). You get q\* — the cut-off your observed q must exceed.

For a class demonstration, k = 4, df = 36, α = .05 gives roughly 3.81. Solve for that, then compute p-values for an observed q just above and just below it, and the relationship between the two directions becomes concrete rather than abstract.

Ranges differ between the versions: StudRangePy takes k from 2 to 50 and df from 1 up; StudRange takes k from 2 to 20 and df of 3 or more, with 0 meaning infinite df. Either way, k = 3 to 5 covers nearly every design a course will actually meet.

## 3 · Tukey HSD

This is the option you will use most. It asks for five numbers, all of which come straight off an ANOVA table, and returns one.

| Prompt | Where it comes from |
| --- | --- |
| k groups | How many groups you compared |
| df error | The ANOVA's error (within-groups) degrees of freedom |
| MS error | The ANOVA's error mean square |
| n per group | Sample size in each group |
| alpha | Your family-wise error rate, usually .05 |

It computes q\* for your k, df and α, then returns

```latex
\text{HSD} = q^{*}\sqrt{\dfrac{MS_{error}}{n}}
```

Any two group means further apart than the HSD differ significantly.

### A worked example

Four teaching methods, six students each, and an ANOVA giving MS error = 12.5 on 20 degrees of freedom. Enter k = 4, df = 20, MS error = 12.5, n = 6, alpha = .05.

The program returns **q crit = 3.9583** and **HSD = 5.7133**.

Now compare every pair of group means:

| Comparison | Difference | Verdict |
| --- | --- | --- |
| A vs B | 6.50 | Significant |
| A vs C | 0.90 | Not significant |
| A vs D | 8.70 | Significant |
| B vs C | 5.60 | Not significant |
| B vs D | 2.20 | Not significant |
| C vs D | 7.80 | Significant |

Notice **B vs C at 5.60** against an HSD of 5.71. A difference of 5.6 units, and it does not clear the bar — by about a tenth of a unit.

That pair is worth dwelling on with a class. It is not that the two groups are the same; it is that this design, with six students per group and this much within-group variability, cannot distinguish them. Increase n and the HSD shrinks. The verdict is a statement about the study, not only about the groups.

### Unequal group sizes

The HSD as computed here assumes equal n. With unequal group sizes you want the Tukey-Kramer adjustment, which replaces n with the harmonic mean of the two group sizes for each comparison separately. The program does not do this — take q crit from option 2 and finish the arithmetic yourself.

## The distribution plot

Both versions plot the distribution. In StudRange it is menu option 4; in StudRangePy you are asked "plot it? (y/n)" after each result.

What you see:

|  |  |
| --- | --- |
| Navy curve | The density of q for your k and df |
| Green curve | The CDF, overlaid |
| Light yellow fill | The α tail |
| Dotted orange-red line | q critical |
| Dotted firebrick line | Your observed q |

The two dotted lines are the point of the picture. When the observed q sits right of the critical line, it is in the tail; when it sits left, it is not. "Significant" stops being a verdict handed down by a table and becomes a position on a curve.

**Live controls, StudRange only.** ← and → move the observed q, in round steps on a NiceNum grid so the readout stays legible. ↑ and ↓ climb a five-rung α ladder — .10, .05, .025, .01, .005 — starting at .05. Esc leaves. Both redraw immediately, so you can slide q across the critical line and watch the p-value cross .05, or change α and watch the critical line move to meet a fixed q. Beta 12 adds touch: tap or drag anywhere in the plot box and the observed q follows your finger, with the tail probability sweeping as you drag. Touch has so far been tested on the emulator only.

StudRangePy's plot is a static picture of the result you just computed, held until you press a key. It shades the upper tail beyond your q and prints P(Q > q) in the corner.

**One warning about StudRange's plot.** It builds a cached grid first, showing "Building distribution cache…" while it works. Once built, the arrow keys are instant — the wait is one-time, not per-frame. Build it before the class starts rather than in front of them.

StudRangePy's plot uses a coarser integration than its result calculations — Simpson 32×48 rather than 64×96 — which is why it appears quickly. The curve is for looking at; the numbers printed above it are the accurate ones.

## Accuracy, origins and limits

### Where the algorithm came from

The engine descends from a 1977 FORTRAN IV subroutine by Dunlap, Powell and Konnerth, published in *Behavior Research Methods & Instrumentation* 9(4):373–375. That original hand-rolled the normal CDF using Abramowitz & Stegun polynomial approximations, because native distribution functions did not exist on the machines of the day.

The Prime versions replace those approximations with native functions — `NORMALD_CDF` in PPL, `erf` and `lgamma` in Python — and add a substitution in the outer integral that the 1977 authors explicitly declined to attempt. Their paper notes that low degrees of freedom "have unique problems" and excludes them. Substituting s = u² fixes the low-df tail: at k = 4, df = 3, α = .005 the program returns 15.4499 against a true value of 15.4503. Before the substitution the same calculation was off by 0.34.

### How accurate

| Version | Agreement with `scipy.stats.studentized_range` |
| --- | --- |
| StudRange beta 12 | maximum absolute error about 1.3×10⁻⁵ |
| StudRangePy beta 14a | p-values under 1×10⁻⁷ relative; critical values under 1×10⁻⁶; density under 1×10⁻⁹ relative to peak |

Both reproduce the classic Harter table values — 3.877, 3.958, 4.102, 5.270 — to every tabled digit.

### Limits

**Equal group sizes.** The HSD option assumes them; see the Tukey-Kramer note above.

**Degrees of freedom below 3.** StudRange does not support them — it inherits the 1977 program's restriction, raises any df of 1 or 2 to 3, and says so in a message. Use StudRangePy, which handles them properly. Above about df = 25,000 both switch to the infinite-df limit, which is correct behaviour rather than a shortcut.

**The plot needs its cache.** 15 to 45 seconds on first build. Not a fault, but plan around it.

**StudRangePy needs Python firmware.** On a Prime without it, use the PPL version.

### Credit

The concept, the source material and the direction of both programs are Roger Metcalf's, as is the classroom judgement about what they needed to do and every round of testing on real hardware. Claude did the implementation, the numerical work, the expansion beyond the original scope, and these guides. The underlying algorithm is Dunlap, Powell and Konnerth's, and the accuracy figures above were verified against SciPy.

**Free for educational and personal use.** Share it, teach with it, adapt it for your own classroom. Please keep the attribution with the files and credit the author if you pass them on or build on them. Not for sale or commercial redistribution. Provided as is, with no warranty — check any result you intend to rely on.

© 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). The programs are distributed as `StudRange_beta12.txt` and `StudRangePy_beta14a.txt`.
