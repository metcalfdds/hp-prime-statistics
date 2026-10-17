# ScatterLab beta 2a — Student and Instructor Guide

A scatterplot you build with your finger on the HP Prime. Tap to place points; press a point and drag it, and the least-squares line, the correlation r, r², the residuals and SSE follow it live. A Guess mode lets students fit a line by eye and then see that least squares really does have the smallest SSE; a far-out point makes leverage something you feel rather than a definition. New in beta 2: a page where the calculator's CAS does the calculus behind least squares on the class's own points, and shows the slope and intercept as exact fractions. Pure PPL plus the CAS (no MicroPython: the regression is a few short passes over at most 40 points).

**Status:** written for the 2026-09-09 firmware (2.4.2); **not yet run on hardware**. Beta 1 passed a smoke test on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026. Beta 2a's CAS page has run only in the off-device harness. It uses the call form that CASProbe beta 1b found on the emulator, the one ErrorRate beta 1a has already shown working there. The arithmetic was checked against `scipy.stats.linregress` (beta 1) and, for the new page, against exact fractions, SymPy and statsmodels in desktop Giac on eleven data sets; the program's own PPL was run on the PC harness. The first device run follows the checklist in `ScatterLab_beta2_NOTES.md`; `ScatterLab_beta2a_CHANGES.md` adds what changed (`verify_ScatterLab_beta2a.py`: 0 failures).

beta 2a (17 Oct 2026): the CAS call form. CASProbe beta 1b showed that `CAS(s)` hands back the text of `s` unevaluated, so beta 2's CAS page would always have shown the decimal version. `slCas` now sends the text through `EXPR` and asks the CAS for a string; the Prime prints the solution as `{[a,b]}`, which the page already reads. Nothing else changed. beta 2 (16 Oct 2026): least squares as calculus (the CAS page). beta 1 (16 Oct 2026): first version.

Run `ScatterLab()` from the Program Catalog. Install as `.txt` through the Connectivity Kit editor.

## The screen

| Where | What |
|---|---|
| Top line | what the data are: "Your points", "SYNTHETIC: …" (orange) for the built-in example, or "From Statistics 2Var: x = C1, y = C2" |
| Plot (left) | blue squares = your points; **magenta** = the least-squares line; **green cross** = the mean point (x̄, ȳ); **orange** segments = residuals (when Resid is on); **red** line and handles = your own line (Guess). The selected point has a red frame, the far-out point an orange one |
| Panel (right) | n, r, r², the equation y-hat = b₀ + b₁x with its numbers, SSE, x̄ and y-bar, the mode, residuals on/off. **Tap the equation** for "least squares as calculus" |
| Two note lines | what just happened, or the selected point's coordinates, residual and leverage h, or what to do next; the second line is the key legend |
| Bottom strip | soft keys **Add · Del · Resid · Guess · Data · Menu** |

The window starts at 0–10 by 0–10. Loading data fits it to the data; **Fit** (in the menu, or the 0 key) fits it again. While you drag, the window never moves — otherwise a moving point would look like a moving axis.

With fewer than 3 points, or with every point on the same x, there is no line: the panel says **"need at least 3 points with different x"** instead of r and the line. If every y is the same, the line is flat and the panel says **"r undefined: every y equal"** (r would be 0/0).

## Touch and soft keys

| Soft key | Does | From the keys |
|---|---|---|
| **Add** | tap empty plot = a new point (40 at most); press a point = select it; press and drag = move it | Menu > Type a point |
| **Del** | tap a point = delete it | Menu > Delete the selected point |
| **Resid** | residual segments on/off | Menu > Residuals on / off |
| **Guess** | your own line, on/off (below) | Menu > Guess the line |
| **Data** | example, load from C1/C2, save to C1/C2, clear | Menu > Data |
| **Menu** | the full menu | Enter |

A press within 7 pixels of a point grabs it. A tap that does not move only selects the point; once the finger travels more than 8 pixels, the point follows it. A new point placed by a tap can be dragged into place in the same gesture. Points snap to a tenth of the tick spacing (0.1 in the default window), so the numbers stay tidy when you save them.

A tap on the **equation in the panel** (outside Guess mode) opens *least squares as calculus*, the same page as the menu item.

**Any key ends a drag** — a safety valve if the touch screen ever sticks.

## Keys

| Key | Does |
|---|---|
| + / − | select the next / previous point |
| arrows | move the selected point one tick (one grid step) |
| 0 | fit the window to the data |
| Enter | the menu (in Guess: reveal or hide the least-squares line) |
| Esc | leave Del or Guess; in Add mode, quit |

In Guess mode: ← / → pick handle 1 or 2, ↑ / ↓ move it a fifth of a tick.

## The menu

| Item | What it does |
|---|---|
| Add a far-out point (leverage) | a point on the line, about three standard deviations of x to the right of x̄ (the window widens if needed) |
| Fit window to the data | refit the window |
| Residuals on / off | as the Resid soft key |
| Guess the line on / off | as the Guess soft key |
| **Least squares as calculus** | the CAS page (below); needs 3 points with different x |
| Data: example, C1/C2, clear | as the Data soft key |
| Type a point (x, y) | add a point by typing it; a point outside the window refits it |
| Delete the selected point | as Del, for keyboard users |
| Help | six pages (below) |
| Quit | back to Home with a summary line (the Prime labels this item **A**) |

## Least squares as calculus (the CAS page)

The magenta line is the one line y = a + b x that makes

  SSE(a, b) = Σ (y − a − b x)²

as small as it can be. SSE is a bowl over the (a, b) plane; at its bottom both slopes are zero. The page has the calculator's CAS do exactly that, on the points on the screen:

1. **Write the SSE out and put it in order** — a quadratic in a and b. For the example: SSE = 16a² + (2608/5)ab − (5321/5)a + (119443/25)b² − (36841/2)b + 373319/20.
2. **Differentiate it** in a and in b: ∂SSE/∂a = 32a + (2608/5)b − 5321/5 and ∂SSE/∂b = (2608/5)a + (238886/25)b − 36841/2.
3. **Set both to 0** (the *normal equations*) **and solve**: b = **2441/2394** and a = **3186173/191520** — shown beside the program's own decimals, 1.019632 and 16.63624.

The page's last lines connect it to the rest of the program: no line has a smaller SSE (Guess shows it), and the first normal equation says the line passes through the green cross, a = ȳ − b x̄.

**Exact means exact.** Every number goes to the CAS as a whole number or a whole number over a power of ten (10.4 is written 104/10), so nothing is rounded — the page says how one value was written. A value that needs more than six decimals (a typed 1/3, or data loaded from C1/C2) cannot be written that way; the page then shows the two normal equations with the program's decimal sums (n a + (Σx) b = Σy, (Σx) a + (Σx²) b = Σxy) and the program's decimal solution.

**The badge** at the top right says **exact (CAS)** when the CAS answered, or **decimal** when it did not (for example if the CAS is set to approximate mode); the decimal page is then shown, and nothing else changes. The CAS is asked only when the page opens and the points have changed since it last answered — never while you drag — and the screen says "asking the CAS …" while it works.

A good classroom sequence: Guess first; then reveal; then open this page and read off the two equations that the revealed line solves. With integer data typed in by the class (three or four points), the fractions are small enough to check by hand.

## Leverage — the far-out point

Menu > Add a far-out point puts one point well to the right of the others, **on** the least-squares line (so at first nothing changes — though r goes up, because the point stretches the x range). It is framed in orange, and the notes say what to try:

- drag the far-out point up or down: **the slope swings** (on the example, dragging it down 15 units takes b₁ from 1.02 to 0.71);
- drag a point near x̄ the same distance: **the line barely moves** — it lifts a little and hardly tilts (b₁ 0.71 → 0.74).

While a far-out point is on the plot, the second note line describes whichever point is selected: "High leverage (h > 4/n): it swings the slope", "Near x̄: the line barely moves (no tilt)", or "Low leverage". The first line shows its leverage h = 1/n + (x − x̄)²/Sxx.

## Data

| Item | What it does |
|---|---|
| Poverty vs crime (SYNTHETIC) | 16 imaginary counties: x = poverty %, y = property crimes per 1,000 residents. **Made-up numbers for practice, not real data** — the top line says SYNTHETIC the whole time |
| Load from C1, C2 | x from C1 and y from C2 of the Statistics 2Var app (up to 40 pairs) |
| Save to C1, C2 | your points into C1 (x) and C2 (y) |
| Clear all points | an empty 0–10 plot |

**Statistics 2Var.** C1 and C2 exist only after the Statistics 2Var app has been opened once on the calculator; until then, Load says so instead of failing. After Save, quit ScatterLab and **open Statistics 2Var yourself** (Apps key): the Num view shows the data, the Symb view picks the fit (Linear), Plot draws it, Stats gives r. ScatterLab does not launch the app for you. Comparing the app's numbers with ScatterLab's is a good check, and a good habit.

The example, for reference: n = 16, x̄ = 16.30, ȳ = 33.26, **y-hat = 16.64 + 1.020x** (exactly a = 3186173/191520, b = 2441/2394), r = 0.751, r² = 0.564, SSE = 422.7, SST = 970.3 (p = 0.0008 for the slope, if a class asks — the program itself does not test it).

## The arithmetic

Three short passes over the points, so it can run on every sample of a drag:

1. x̄ = Σx / n, ȳ = Σy / n
2. Sxx = Σ(x − x̄)², Syy = Σ(y − ȳ)², Sxy = Σ(x − x̄)(y − ȳ)
3. b₁ = Sxy / Sxx, b₀ = ȳ − b₁x̄, r = Sxy / √(Sxx·Syy), r² = r², and SSE = Σ(y − b₀ − b₁x)²

Centring before squaring keeps every digit when the numbers are large (crime counts in the thousands, years). r² equals 1 − SSE/SST, the identity help page 2 teaches. Leverage h = 1/n + (x − x̄)²/Sxx. The guard tests the *range* of x, not Sxx, because with every x equal the computed x̄ can differ from x in its last digit and leave Sxx a hair above zero. The CAS page solves the same problem a second way, by calculus and exactly; its fractions equal these decimals.

## Help pages

1. **What r measures** — direction and strength of a straight-line pattern; no units; one far-out point can change it.
2. **r²: the share explained** — SST, SSE, r² = 1 − SSE/SST, and how Guess shows it.
3. **Residuals and least squares** — residual = y − y-hat; the line minimises SSE and passes through (x̄, ȳ); Menu > Least squares as calculus for the derivation.
4. **Leverage** — h, the 4/n rule of thumb, what to try with the far-out point.
5. **Correlation is not causation** — ice-cream sales and assaults both rise in summer because both follow the temperature (a lurking variable); county poverty and property crime also travel with density, policing, reporting and age mix; county figures describe counties, not people (the ecological fallacy); the example data are synthetic.
6. **Touch, keys and Statistics 2Var** — and "tap the equation: least squares as calculus".

← → or a tap on the left/right half turns the page; Esc goes back to the plot.

## Home exports

`SL_N` (points), `SL_B0` (intercept), `SL_B1` (slope), `SL_R` (r), `SL_R2` (r²), `SL_SSE` — kept up to date while you work, and left in Home after Quit. When there is no line, all but `SL_N` are 0; when r is undefined (every y equal), `SL_R` and `SL_R2` are 0. Quit also returns a summary line, e.g. "ScatterLab: n = 16, y-hat = 16.64 + 1.020 x, r = 0.7512, SSE = 422.7".

## Ideas for class

- **Build r by hand.** Start empty; place points in a rising band and watch r climb towards 1; spread them out and watch it fall; arrange a U shape and see r near 0 with an obvious pattern — "r measures *straight-line* association".
- **One point.** Load the example, add the far-out point, and ask the class to predict before you drag it.
- **Beat the computer.** Everyone guesses on the same data and reports their SSE; reveal; nobody wins, and that is the definition of least squares.
- **Where the line comes from.** Type three points with whole-number coordinates, open the CAS page, and have the class check the two normal equations and the fractions by hand.
- **Lurking variables.** After help page 5, ask what a third variable for the poverty–crime example might be, and why county data cannot answer questions about individuals.

## Credit

Concept, direction, classroom judgement and all hardware testing: Roger Metcalf. Implementation, the numerics and their verification against SciPy, SymPy, statsmodels and desktop Giac, the harness runs and this guide: Claude (Anthropic). The example data are synthetic, generated for this program.

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude). Keep this header with the file and credit the author if you pass it on. Not for sale or commercial redistribution. Provided as is, with no warranty. Firmware: written for 2026-09-09 (2.4.2); not yet run on hardware; beta 1 passed a smoke test on the HP Prime Virtual Calculator on 17 Oct 2026.*
