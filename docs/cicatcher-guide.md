# CICatcher beta 2a: User's Guide

Confidence intervals on the HP Prime: **"95 % confidence: 95 % of WHAT?"** Pure PPL, with one small, optional use of the CAS.

**Status:** written for the 2026-09-09 firmware (2.4.2). **Not yet run on hardware.** The five interval formulas were checked against scipy and statsmodels. Every coverage figure on the help pages was checked against exact binomial sums and simulations, and the program's own routines were run off-device in the fleet's run harness (`verify_CICatcher_beta2.py`, and for beta 2a `verify_CICatcher_beta2a.py`: 55 checks, 0 failures). The device-test checklist is in `CICatcher_beta2_NOTES.md`; `CICatcher_beta2a_CHANGES.md` adds what changed. Beta 1 passed a smoke test on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026. Beta 2a's CAS line has run only in the off-device harness. It uses the call form that CASProbe beta 1b found on the emulator, the one ErrorRate beta 1a has already shown working there.

- beta 1 (16 Oct 2026): first version, from the fleet review of 16 Oct 2026 (§7, item 4).
- beta 2 (16 Oct 2026): a fifth interval, **Exact (Clopper-Pearson)**, with its coverage kept exactly; a sixth help page on why exact intervals are conservative; and the closed form of an exact end, written by the CAS, when a sample has 0 or n "yes" answers.
- beta 2a (17 Oct 2026): the CAS call form. CASProbe beta 1b showed that `CAS(s)` hands back the text of `s` unevaluated, so beta 2 would have shown its own unreduced question under "exact (CAS)". `cqCas` now sends the text through `EXPR` and asks the CAS for a string. Nothing else changed.

Run `CICatcher()` from the Program Catalog. Install as `.txt` through the Connectivity Kit editor.

## The idea

A confidence level is a promise about a **method**, not about one interval. CICatcher knows the truth: the population mean μ or proportion p. It draws sample after sample, turns each one into an interval by the textbook recipe, and counts how many intervals catch the truth. At 95 %, about 95 of every 100 do. Any *one* interval either caught μ or did not; the 95 % is the method's long-run catch rate.

Some methods keep their promise (z and t, Wilson mostly). The textbook Wald interval for a small-sample proportion does not. The exact interval over-keeps it: its coverage never falls below the level, and the program shows by how much it exceeds it.

## Setting up

1. **Which interval?**
   - Mean, σ known (z): x̄ ± z* σ/√n
   - Mean, σ unknown (t): x̄ ± t* s/√n, df = n − 1
   - Proportion: Wald (textbook): p̂ ± z* √(p̂(1 − p̂)/n)
   - Proportion: Wilson (score): (p̂ + z*²/2n ± z* √(p̂(1 − p̂)/n + z*²/4n²)) / (1 + z*²/n)
   - **Proportion: Exact (Clopper-Pearson)**: every p under which your count k lies in neither tail of Binomial(n, p) that holds α/2 or less:
     - lower end: P(X ≥ k | p) = α/2;
     - upper end: P(X ≤ k | p) = α/2;
     - for k = 0 the interval runs from 0 to 1 − (α/2)^(1/n), and for k = n from (α/2)^(1/n) to 1.

     There is no critical value and no normal curve.
2. **Population and sample** (one form): μ, σ, n and the level for a mean; p, n and the level for a proportion. The defaults are chosen for teaching:
   - μ = 100, σ = 15, n = 10 (IQ-like scores);
   - p = 0.10, n = 20, where Wald falls well short and Exact over-delivers;
   - level 0.95.

   Type the level as 0.95 or as 95. n runs from 2 (means) or 5 (proportions) to 100.

At start the program checks that `BINOMIAL_CDF` and `BINOMIAL` give two known values. If they do not, Exact is refused with a message ("Exact is off") rather than drawing wrong intervals.

## The main screen

| What | Meaning |
|---|---|
| Green vertical line | the truth (μ or p), which the method never sees |
| Horizontal lines | the 50 most recent intervals, newest on top; the dot is the sample's estimate |
| **Blue** line | this interval caught the truth |
| **Red** line | this interval missed |
| Header, line 1 | "caught 47 of 50 (94.0 %), all 237: 95.4 %": the 50 on screen, and every interval this run |
| Header, line 2 | "target 95 %" (magenta) and the population and method (green), e.g. "Exact, p = 0.10, n = 20" |
| Right edge | the level slider, 50 % to 99.9 %, with a magenta knob |
| Grey zones (proportions) | values below 0 or above 1, which a proportion cannot take; only Wald lines reach them (Exact lines never do) |
| A notch at the edge | that line runs off the window |
| Bottom panel | the key legend, or the sample behind the picked line |

The x window is frozen for the whole run (the truth ± 6.5 standard errors), so changing the level visibly *lengthens* or *shortens* the lines.

## Keys, soft keys and touch

| Action | Does | Key shortcut |
|---|---|---|
| **+1** | one new sample, animated: the stack slides down, the sample's values appear in the panel, its interval grows grey out of its estimate, then turns blue or red | − |
| **+10**, **+50** | more samples at once ("Sampling …" box) | + (= +10) |
| **Conf** | 80, 90, 95 or 99 % | — |
| **n** | a new sample size, which starts a fresh run (one run = one method) | — |
| **Menu** | new setup, reset the counts, Help, Quit | Enter |
| **Drag the right edge** | any level from 50 % to 99.9 %, live (snaps to 80/90/95/99) | Up / Down: 1 % at a time, then 99.5, 99.9 |
| **Tap a line** | its sample in the bottom panel; slide up and down the stack to browse; tap it again (or the panel) to close | Left / Right: the next line up / down |
| Quit | | Esc |

All six actions fit on one strip, so there is no "More" page key; Menu holds the rest.

### The showcase: drag the level

Put a finger on the right edge and slide it up. Every one of the 50 lines is recomputed as the finger moves, from its stored estimate (and s, for t). Nothing is resampled, so the lines grow, red lines turn blue, and both counts climb toward the new level. Slide down and the reverse happens.

The track is spaced by the critical value z*, not by the percentage, so equal finger travel means an equal change in length: 80 % is a quarter of the way up, 99 % about three-quarters.

For **Exact**, each new level re-solves the two ends of every *count* on screen. At the defaults that is about six different counts, each starting from the end it had at the previous level. It is the program's heaviest frame on a G1.

The long-run count ("all 237") follows exactly too, for *every* interval of the run, not just the 50 on screen. Each interval remembers the lowest level at which it would have caught the truth, so moving the level only needs a count, not a re-run. For Exact, that "catch level" depends only on the count k: 1 − 2·min(P(X ≥ k), P(X ≤ k)) under the true p. So it is a table of n + 1 numbers worked out once per run, and +50 costs no searching.

### The picked sample

- **Mean:** the sample's n values as black dots on the same axis (a value beyond the window is pulled to the edge in grey), the green truth tick, the interval and x̄ beneath them, and a line such as `x̄ = 103.2, s = 14.1: 93.1 to 113.3, missed by 1.3`. The dots spread much wider than the interval: the interval is for the *mean*, not for individual values.
- **Proportion:** n tiles, black = yes, and `p̂ = 3/20 = 0.15: -0.01 to 0.31, caught` (Wald). A Wald lower limit below 0 is printed as the formula gives it: an impossible value, and another sign of the method's trouble.
- **Exact, with 0 (or n) "yes" answers:** the tiles would all be one colour, so their place goes to the end that has a closed form. For example, `upper = 1-(1/40)^(1/20) = 0.1684` with the badge **exact (CAS)**, and the numbers line under it.
  - The CAS turns the level into α/2 = (1000 − L)/2000, here 1/40, and writes the end exactly. The 0.1684 is the program's own arithmetic.
  - While a finger is down, and whenever the CAS does not answer, the line reads `upper = 1 - (α/2)^(1/n) = 0.1684` with the badge **decimal**. The CAS is only asked after a tap, a key or a lifted finger, never during a drag, and each answer is kept for that n and level.

## What the help pages say (and the numbers behind them)

All numbers are checked in `verify_CICatcher_beta2.py`.

1. **95 % of WHAT?** The method's long-run catch rate. Say "we are 95 % confident", meaning the method catches the truth 95 % of the time, not "a 95 % chance μ is in this interval".
2. **Level, width, z and t.** A higher level uses a bigger critical value, so every line grows.
   - z lines all have the same length (true σ); t lines vary with each sample's s, and t* is larger than z* to pay for it: t(9) = 2.262 against 1.960.
   - Using z with s at n = 10 would catch only **91.8 %**.
   - The page ends with the **engine note**: which code produced t*.
3. **Wald and Wilson.** At p = 0.10, n = 20, Wald catches only **87.6 %** (exact binomial) while claiming 95 %; **12.2 %** of those samples have p̂ = 0, where the Wald interval has zero width and must miss. Wilson takes its standard error from the p being tested, never has zero width, and catches **95.7 %**. Wald wants n·p and n(1 − p) of at least 10; at n = 100 it reaches **93.2 %**.
4. **Exact intervals: never below** (new in beta 2).
   - A count has only n + 1 possible values, so no interval can catch exactly 95 % at every p. Exact makes sure it is **never less**: at n = 20 its worst case over every p is **95.8 %**.
   - At p = 0.10, n = 20 it catches **98.9 %** (Wilson 95.7 %, Wald 87.6 %). At 80 % or 90 % it still catches **95.7 %**.
   - The price is longer lines: at the defaults exact intervals average 0.292 wide, Wilson's 0.263.
   - With 0 yeses the interval runs from 0 to 1 − (α/2)^(1/n), **0.168** at n = 20 and 95 %.
   - The page's last line says what the exact ends run on: "bisection on BINOMIAL_CDF (checked)".
5. **A criminal-justice example.** A city asks 100 residents whether they are afraid to walk alone at night; 38 say yes.
   - The 95 % Wald interval is 0.38 ± 1.96 √(0.38 × 0.62/100) = 0.38 ± 0.095, **28.5 % to 47.5 %** (Wilson: 29.1 % to 47.8 %; exact: 28.5 % to 48.3 %).
   - Right: "We are 95 % confident the true share is between 28.5 % and 47.5 %."
   - Wrong: "There is a 95 % chance the true share is in this interval."
   - Try it: Wilson, p = 0.38, n = 100, then +50.
6. **Keys and touch.**

| Default setting | Exact coverage at 95 % | Check |
|---|---|---|
| z, μ = 100, σ = 15, n = 10 | 0.9500 | 100,000-replicate simulation 0.9496 |
| t, same | 0.9500 | 0.9501 |
| Wald, p = 0.10, n = 20 | 0.8760 | 0.8760 |
| Wilson, p = 0.10, n = 20 | 0.9568 | 0.9571 |
| **Exact, p = 0.10, n = 20** | **0.9887** | the PPL's own sampler, 20,000 intervals: 0.9895 |

At p = 0.10, n = 20 the four Conf levels give (80, 90, 95, 99 %):

| Interval | 80 % | 90 % | 95 % | 99 % |
|---|---|---|---|---|
| Wald | 83.5 % | 86.7 % | 87.6 % | 87.8 % |
| Wilson | 74.6 % | 95.7 % | 95.7 % | 98.9 % |
| Exact | 95.7 % | 95.7 % | 98.9 % | 99.8 % |

Three lessons hide here:
- Wald at 99 % *still* catches under 88 %, because the p̂ = 0 samples can never be caught.
- Wilson's coverage jumps around with the level. For a count only a handful of p̂ values are possible, so every interval for a proportion has coverage that oscillates around its target.
- Exact never dips below its target, and pays for it by overshooting, most of all at low levels.

## The critical value t*, the exact ends, and the engine notes

- z* comes from `NORMALD_ICDF`, which is device-verified.
- For t*, the program first tries `STUDENT_ICDF(df, 1 − α/2)` inside `IFERR`. That is a documented built-in that hp-prime-kit saw working on the emulator, but it is not yet on our own verified list. The program keeps the answer only if `STUDENT_CDF` at that point gives the probability back. Otherwise it finds t* by bisection on `STUDENT_CDF` (verified). Help page 2 says which one ran.
- **The exact ends** come from bisection on `BINOMIAL_CDF(n, p, k)`, with a Newton step whenever it lands inside the bracket; the slope is n·`BINOMIAL(n − 1, p, k)`. That is about five steps to ten significant digits.
  - It is the same routine, line for line, as EpiStats v1.7's exact intervals.
  - Checked against statsmodels' Clopper-Pearson to 1E-14 over thousands of intervals.

## The CAS, behind the fence

The only CAS line in CICatcher is the closed form above, for 0 or n "yes" answers. The fleet's rules, which every CAS-using program follows:
- one call routine (`cqCas`), using the form CASProbe beta 1b found: `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))`, with the surrounding quotes dropped. An answer containing `undef`, an error, or ∞ is refused;
- CAS text built only from whole numbers;
- calls on events only, never in a drag or animation, with each answer cached;
- the answer is text for display, never a number the program draws with;
- a decimal fallback with a badge.

If the CAS is not available, everything works and the badge reads "decimal".

## Home exports

- `CQ_TOTAL`: intervals drawn.
- `CQ_HITS`: how many caught the truth at the final level.
- `CQ_COVER`: their ratio, the long-run catch rate.

On quitting, the program returns a summary line, e.g. `CICatcher: 49 of 50 caught the truth (98.0 %) at 99.5 %, Exact, p = 0.10, n = 20; see CQ_COVER`, so it appears in the Home history and no Terminal is left open.

## Classroom suggestions

- Start with z at the defaults and +50 a few times; ask what fraction is red. Then drag the level to 80 % and back to 99 %.
- Tap a red line: "this one missed by 1.3". Point out that nobody holding that one sample could have known.
- Switch to t, n = 5: the lines vary in length, and some short ones miss.
- Switch to Wald, p = 0.10, n = 20, and +50 several times: the "all" rate settles near 88 %, not 95 %. The red dots at 0 are samples where nobody said yes. Then Wilson, same settings.
- Then **Exact**, same settings: the rate settles near 99 %, above the promise. Drag the level down to 80 %: almost nothing turns red. Ask why a method that "promises 80 %" catches 96 %, and what the class pays for that (look at the lengths). Tap a line at 0 for the formula of its end.

## Credit

Concept, direction, classroom judgement and all hardware testing: Roger Metcalf. Implementation, the numerics (the catch-level bookkeeping, the checked `STUDENT_ICDF` with its bisection fallback, the fleet's exact-interval routine) and their verification against scipy and statsmodels, and this guide: Claude (Anthropic). The normal sampler is NormExplorer beta 40's Marsaglia polar method; the touch and drawing idioms are ChiTable's and GaltonBoard's; the CAS kit is the fleet's (BRIEF_CAS).

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). Keep this header with the file and credit the author if you pass it on. Not for sale or commercial redistribution. Provided as is, with no warranty. Firmware: not yet run on hardware (written for 2.4.2, 2026-09-09); beta 1 passed a smoke test on the HP Prime Virtual Calculator on 17 Oct 2026.*
