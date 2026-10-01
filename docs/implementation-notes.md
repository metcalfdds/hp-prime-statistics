# Implementation Notes

## Norm Explorer, StudRange and StudRangePy

*Annotated excerpts for people who write PPL*

## What this is

Three programs ship with this bundle, and they are heavily commented already. This document is for the reader who wants the reasoning behind the code rather than the code itself — why a routine is shaped the way it is, what was tried first, and which decisions were forced by the machine rather than chosen.

It assumes you write PPL. Nothing here explains what a `LOCAL` is.

It also assumes you have the other two documents, and deliberately does not repeat them:

| Document | Covers |
| --- | --- |
| *Lessons Learned* | The rules, as a checklist. Hard limits, reserved names, verified key codes. |
| *MicroPython on the HP Prime* | The Python side as a general topic — what the interpreter is, what breaks. |
| **This document** | Why *this* code looks like this. Annotated excerpts. |

Everything below was found on a physical G1 and G2, as well as on the emulator from HP (all with 20260909 update), across roughly forty build iterations, not derived from documentation. Where something remains unexplained, it says so.

**Free for educational and personal use.** Share these notes, teach from them, quote them with attribution. Not for sale or commercial redistribution. Provided as is--no guarantees. Your mileage may vary.

## Architecture: state in globals, not parameters

Norm Explorer began as a single loop that drew a curve and read keys, with every feature bolted onto the same `CHOOSE` tree. By about the fifteenth build that was unmaintainable, and the rebuild took a different shape: a thin menu dispatcher, a dozen small modules, and all shared state in exported globals.

```
EXPORT NE_MU, NE_SG;             // the distribution
EXPORT NE_XM, NE_XO, NE_XB;      // shading: mode, bound a, bound b
EXPORT NE_CFG;                   // {bands, refcurve, mu2, curve2 on}
EXPORT NE_WA, NE_WLO, NE_WHI;    // window mode and range
```

Globals rather than parameters, and that is a PPL constraint rather than a preference. **A PPL function cannot modify its caller's variables.** Parameters are passed by value, so a module that needs to change the session distribution has no way to hand it back except through a global. The alternative — returning a list and having the caller unpack it — was tried and abandoned; every call site grew three lines of bookkeeping.

The price is that any routine can write any state, so **every write path has to be audited together**. This bit us: a distribution can be changed from the Set menu *or* by the z-solver writing back, and for several builds only one of them cleared the now-stale shading and sample. The app behaved differently depending on how you got there.

```
// ZSStore: same clean-up as menu 1, because this is the other
// route to a changed distribution and the two must leave the
// session in the same state.
IF stChg == 1 AND stS > 0 THEN
  NE_MU := stM; NE_SG := stS;
  NE_XM := 0;                            // old shading, old curve
  NE_HN := 0; NE_BINS := MAKELIST(0, K, 1, NBINS+2, 1);
  NE_CFG(4) := 0;
  IF NE_WA == 0 THEN NE_WA := 4; END;
  AutoWin();
END;
```

A second consequence worth knowing: a program with parameters gets an auto-generated argument form when launched from the catalog. Menu-driven tools therefore take **zero arguments** and hold their defaults internally. Plot explorers launched from Home with values — Burr3, Norm3 in the same fleet — keep their parameters for exactly the opposite reason.

## Drawing: compose once, blit once

`NormDraw` builds a frame in six passes — grid, empirical bands, tail shading, curve overlap, axes, histogram, curves, markers, readouts. Drawing those straight to `G0` tears visibly, because the user watches each pass arrive. The whole frame is therefore composed off-screen and blitted in one operation:

```
DIMGROB_P(G1, 320, 240, NWHITE);     // off-screen buffer, cleared
...                                  // every pass targets G1
BLIT_P(G0, 0, 0, G1);                // one copy to the screen
```

Every drawing call in the routine takes `G1` as its first argument. Miss one and that element flickers while the rest is stable — which is a useful diagnostic if you ever see it.

### The y-flip

Screen coordinates run downward from the top left; a density runs upward from the axis. Every plotted point goes through the same conversion, and getting it wrong produces a curve reflected about the horizontal axis:

```
py := BOT - IP(MIN(density/ymax, 1) * H);
IF py < TOP THEN py := TOP; END;     // clamp, do not let it escape
```

The `MIN(..., 1)` matters more than it looks. Without it, a histogram bar taller than the plot box produces a negative `py` and draws off the top of the screen — or, on some builds, somewhere unpredictable.

### Shade by pixel column, not by math sample

This one cost two programs before the rule stuck. The intuitive approach — walk x in mathematical steps and draw a vertical line at each — leaves white gaps, because consecutive x values can map to the same pixel column while others get skipped entirely.

```
FOR ndPX FROM LFT+1 TO RGT DO                    // iterate PIXELS
  ndXW := ndMin + (ndPX - LFT) / PW * ndSpan;    // then find the x
  ...
  LINE_P(G1, ndPX, BOT-1, ndPX, ndPY, ndCol);
END;
```

Iterate the pixels and solve for x, never the reverse.

### Evaluate the density once

The band pass, the tail pass and the curve pass all need the same pdf values. Early versions recomputed `NORMALD` in each — three times per pixel column, 272 columns, on every keypress. Caching it into a list first is a straightforward win:

```
ndPdf := MAKELIST(0, K, 0, PW, 1);
FOR ndIdx FROM 0 TO PW DO
  ndPdf(ndIdx+1) := NORMALD(ndMU, ndSG, ndMin + ndIdx/PW*ndSpan);
END;
```

## Auto-scaling, and knowing when not to draw

The first fifteen builds used a fixed window: x from −8 to 8, y from 0 to 0.85. That is fine for N(0,1) and useless for anything a statistics class actually meets. Enter N(100,15) and the curve is entirely off-screen.

`AutoWin` sets the window from the session state before every draw:

```
NE_YMX := NORMALD(NE_MU, NE_SG, NE_MU) * 1.15;   // peak is 1/(sigma*sqrt(2pi))
awlo := NE_MU - awsp * NE_SG;                    // awsp is 4, or 6 in wide mode
awhi := NE_MU + awsp * NE_SG;
```

Then it widens to take in anything else that must be visible — the comparison curve, and both shading bounds — so a critical value out at z = 3.5 is never off the edge. Tick steps and decimal places come from the span through `NiceNum`, which is why N(847,220) labels in hundreds and N(0.5,0.02) labels in hundredths without special-casing.

### Freezing the window inside the explorer

Auto-scaling has one place it must be switched off. In the live explorer, if the window tracked μ, the bell would sit dead centre forever and moving the mean would look like nothing happening. The explorer locks a ±6σ window on entry, and offers **0** to re-centre:

```
NE_WA := 6; AutoWin();
NE_WA := 0;                    // custom: AutoWin now leaves x alone
NE_YMX := NORMALD(NE_MU, NE_SG, NE_MU) / 0.62;   // headroom to grow
```

The `/ 0.62` leaves the curve filling about 62% of the box, so shrinking σ makes a visibly taller curve rather than one clipped at the frame.

### The reference curve, and a lesson about fit

The N(0,1) reference is drawn only when it genuinely fits — and the first version tested only the horizontal fit. That was not enough. The standard normal peaks at 0.3989; a σ = 7 curve peaks at 0.057, seven times shorter. Drawn on one vertical scale, N(0,1) clips flat at the top of the frame and reads as a grey rectangle. A user reported it as a stray artefact, which is exactly what it looked like.

```
IF ndRef == 1 THEN
  IF ndMin < 4 AND ndMax > -4 AND NORMALD(0, 1, 0) <= ndYmx THEN
  ELSE
    TEXTOUT_P("N(0,1) reference does not fit at this scale",
      G1, 62, 195, 1, NGRAY);
  END;
END;
```

Two things came out of that. **Test the fit on both axes before drawing any comparison curve.** And when you suppress something the user asked for, *say so* — otherwise the toggle appears broken, because from the user's side pressing the key does nothing at all.

## Input: the three things that cost the most time

### FREEZE is not a pause

This one shipped broken for several builds and was only caught because a user said "the result panel never appears — it goes straight back to the menu."

`FREEZE` suppresses the screen refresh **when the program terminates**. Mid-program it does nothing at all. A result panel followed by `FREEZE` draws, and is then instantly repainted by the next `CHOOSE`. It is on screen for about one frame.

The working idiom is three lines, and the order matters:

```
REPEAT kk := GETKEY; UNTIL kk == -1;   // drain what INPUT left behind
REPEAT kk := GETKEY; UNTIL kk > -1;    // wait for a REAL press
REPEAT kk := GETKEY; UNTIL kk == -1;   // drain that one too
```

The first line is not optional. `INPUT` and `CHOOSE` leave their dismissing keypress in the buffer, and without the drain it satisfies the wait immediately — so the screen you just drew is skipped.

Note also how similar `UNTIL kk == -1` and `UNTIL kk > -1` look, and that they do opposite things. A wait loop written with the wrong one is a silent no-op.

### Touch, polled alongside keys

The Prime has a touchscreen and the explorer ignored it for thirty builds. Adding it meant giving up the blocking `GETKEY` wait and polling both:

```
REPEAT
  exK := GETKEY;
  exM := MOUSE;
  exM1 := exM(1);
UNTIL exK > -1 OR SIZE(exM1) > 0;
```

`MOUSE` returns a list per finger; `m(1)` is the first, and `SIZE(m1) > 0` means it is touching. Elements 1 and 2 are the x and y of the touch.

Converting a touch back to a data value needs the same transform the drawing uses, inverted — which is why the plot box coordinates moved into shared constants rather than being locals of `NormDraw`:

```
NE_XO := NE_WLO + (exM1(1) - NPLFT) / (NPRGT - NPLFT) * (NE_WHI - NE_WLO);
```

Two constants that agree beat two copies of 38 and 310 that might not.

### There is no blank input field

A PPL real always holds a value, so a numeric `INPUT` box always displays one. The obvious workaround — a string variable initialised to `""` — does not work either: the Prime renders the quotation marks as editable text, the user sees `""`, and deleting them to type a number is a syntax error. That was tested on hardware and abandoned.

So every field shows a starting value, and the choice of value is a design decision rather than a placeholder. A prefill computed from other session state reads as a bug — `x := μ + σ` produced a solver that opened at 26 and generated a bug report. Flat constants, or state the rule in the field's help line.

## The bridge, as actually built

The general account is in *MicroPython on the HP Prime*. This is what the code does.

Norm Explorer's histogram sampler exists twice — once in PPL, once in MicroPython — running the same Marsaglia polar algorithm and returning the same 34 numbers: 32 bin counts, then the sum and the sum of squares.

```
EXPORT NEpmu, NEpsg, NEpn, NEplo, NEpw, NEpout;   // the bridge variables
```

PPL writes the inputs, calls Python, reads the output. Python reads them with `hpprime.eval` and writes back by assembling a PPL assignment as text. **Nothing crosses the bridge inside a loop** — the payload is fixed-size, so 5000 draws cost the same crossing as 200.

### The guard is the interesting part

A Python exception does not raise a PPL error. The traceback goes to the Terminal and PPL continues with whatever the bridge variable held before. `IFERR` around `PYTHON(...)` catches nothing.

So the guard does three things, and all three are necessary:

```
NEpout := 0;                      // 1. clear it: no stale value survives
IFERR
  NEpmu := NE_MU; NEpsg := NE_SG; NEpn := hsN;
  NEplo := NE_HLO; NEpw := NE_HW;
  PYTHON(SAMPBINSPY);
THEN
  NEpout := 0;
END;

hsOK := 0;                        // 2. validate by USING the result
IFERR
  hsChk := NEpout(NBINS+2) + 0;   //    if the last element reads, it worked
  hsOK := 1;
THEN
  hsOK := 0;
END;

IF hsOK == 1 THEN                 // 3. fall back, always
  NE_BINS := NEpout;
  NE_SRC := 1;
ELSE
  NE_BINS := SampBins(NE_MU, NE_SG, hsN, NE_HLO, NE_HW);
  NE_SRC := 2;
END;
```

An earlier version tested `TYPE(NEpout) == 6` for a list. That works, but it adds an assumption about firmware type codes, and if the assumption were ever wrong the program would silently use the slow path forever. Reading the value proves it directly and assumes nothing.

### Why `NE_SRC` exists

Because the guard works, a failure is invisible: the fallback runs, the histogram is correct, the statistics are correct, and the only symptom is that it took longer. In this program the Python path failed on **every run for eleven consecutive builds** and nothing on screen said so.

So the program records which sampler actually ran, and the diagnostics page reports it — alongside a live probe that runs a two-value sample and checks whether the result comes back. That is the difference between an invisible fault and a visible one.

Any program that crosses this bridge should carry something equivalent.

## Numerical decisions

### The u² substitution

StudRange's outer integral runs over s = √(χ²ᵥ/v). For small v the integrand is sharply peaked near zero, and evenly spaced Simpson nodes mostly land where nothing is happening. The 1977 paper's authors noticed this and dealt with it by excluding low degrees of freedom — their note says those "have unique problems."

Substituting s = u² clusters the nodes exactly where the mass is:

```
f = 2.0 * u * exp(lc + (v - 1.0) * log(s) - 0.5 * v * s * s)
```

The `2u` is the Jacobian. At k = 4, v = 3, α = .005 the result goes from 0.34 off to **15.4499 against a true 15.4503** — four decimal places, on a case the original program declined to attempt.

### Secant, not bisection

Both programs invert the CDF to find a critical value. The PPL version bisects: 60 iterations, each a full double integration. The Python version uses a secant iteration with a warm start and converges in about nine.

```
q0 = 2.0 + 0.5 * pow(k, 0.6) * (1.0 + 4.0 / max(v, 1.0))   # warm start
q1 = q0 * 1.2
```

Sixty evaluations against nine, and each one faster because it runs in compiled C. On a G2 that is the difference between about a minute and about 1.5 seconds. The warm start is worth the two lines — a bad initial bracket costs more iterations than the formula saves.

### Computational versus two-pass variance

The samplers accumulate Σx and Σx² and form s from them, rather than storing values and doing a second pass:

```
NE_HXB := NE_BINS(NBINS+1) / hsN;
NE_HS := √(MAX(0, (NE_BINS(NBINS+2) - hsN*NE_HXB*NE_HXB) / (hsN - 1)));
```

This is the formula every numerical analysis text warns about, because it subtracts two large nearly equal numbers. It is used here anyway, deliberately: the payload across the bridge must be fixed-size, and two running sums are two numbers whatever n is. Checked against a two-pass calculation it agrees to 14 decimal places at the scales this program uses.

The `MAX(0, ...)` is the guard against the one failure mode that matters — cancellation driving the result slightly negative and `√` then failing. It would begin to matter on something like N(100000, 0.5); nothing a classroom will meet.

### Pooled s, and what the plot can draw

When two real groups are loaded from C1 and C2, Cohen's d uses the pooled standard deviation:

```
tgSP := √(((tgN1-1)*tgS1 + (tgN2-1)*tgS2) / (tgN1 + tgN2 - 2));
```

That is the standard denominator, and it is also the only thing the plot can honestly show, since it draws both curves with one σ. Where the two constraints coincide, say so in the guide rather than letting the reader assume the statistics were chosen to suit the graphics.

## Reaching the built-in apps — and where the wall is

Norm Explorer's data module reads the user's own data out of the Statistics apps. This turns out to divide cleanly into what works and what cannot be done at all from a standalone program.

### What works

The data columns are ordinary globals. `D1` (Statistics 1Var) and `C1`, `C2` (Statistics 2Var) can be read and written directly:

```
dlN := 0;
IFERR dlN := SIZE(D1); THEN dlN := 0; END;    // D1 may not exist yet
IF dlN < 2 THEN
  MSGBOX("Put your data in list D1 of the Statistics 1Var app first...");
  RETURN;
END;
```

The `IFERR` around `SIZE(D1)` is needed because the variable does not exist until the Statistics app has been opened at least once.

Writing works too, which is what lets the program standardise a column and hand the result back:

```
D2 := MAKELIST((D1(K) - zdXB) / zdS, K, 1, zdN, 1);
```

`STARTAPP("Statistics 1Var")` then launches the app with the data in place.

### What does not

App *settings* are a different matter. `H1Type`, which selects the plot type, and `SetSample`, which binds a plot to a column, are Statistics 1Var app variables. Referencing either from a standalone program is a **syntax error at paste time** — not a runtime error, so `IFERR` cannot help.

The User Guide documents qualifying a variable as `Function.Xmin`. Both `Statistics1Var.H1Type` and `Statistics 1Var.H1Type` were tried on a G2 with the 2026-09-09 firmware and both error.

The confusing part, if you go looking, is that HP's own DiceSimulation example in the User Guide uses `SetSample` and `H1Type` freely — but that example *is* a Statistics-derived app, where those names are in scope. From outside, they are not.

So the hand-off does what it can and asks the user for the rest:

```
MSGBOX("Opening Statistics 1Var. In Symbolic view set Plot1 to
  Normal Probability, then press Plot and choose Autoscale.");
STARTAPP("Statistics 1Var");
```

One tap of the user's, and nothing that can break.

### The general shape of it

Data is reachable; configuration is not. If your program needs an app configured a particular way, plan on instructing the user rather than doing it for them — or write your program *as* a customised app, which is what HP's own example really demonstrates.

## Credit and terms

The concept, the direction, the classroom judgement and every round of hardware testing behind these programs are Roger Metcalf's. Claude did the incredible implementation, the numerical work and these notes. The studentized range algorithm is after Dunlap, Powell and Konnerth (1977); accuracy figures were verified against SciPy.

Tested on an HP Prime G2 and G1, both now running the 2026-09-09 firmware, as well as the desktop Virtual Calculator from HP.

**Free for educational and personal use.** Share these notes, teach from them, quote them with attribution. Not for sale or commercial redistribution. Provided as is--no guarantees. Your mileage may vary.

© 2026 Roger Metcalf. Written with extensive and incredible AI assistance from Anthropic Claude and Claude Code.
