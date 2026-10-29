# BurrLab: why the Burr XII, and how the fit works

*A student's guide to BurrLab beta 1i (HP Prime). Roger D. Metcalf, 2026; written with AI assistance. Every number in it was checked against SciPy and mpmath on a PC, and BurrLab has run on a G1 and a G2.*

## 1. Why a special distribution for a long right tail?

A lot of criminal-justice data has the same shape: most values are small, and a few are enormous.

- Months served for a homicide: most under ten years, a few over forty.
- Weeks until a released prisoner is re-arrested: many in the first months, some much later.
- Insurance claims after a fire: thousands of small ones, a handful that run to hundreds of millions.

Draw a histogram and it rises fast, peaks early, then trails off to the right for a long way. That trail is the **long right tail**, and it is where the trouble is. A normal curve is symmetric and its tail dies away almost at once, so it describes none of this. The usual skewed families (lognormal, Weibull, gamma) fit the body of such data well enough, but each one *decides in advance* how fast the tail dies away. If the data's tail is heavier than the family allows, the fit will underestimate how often the big values happen, which in a courtroom or a budget is exactly the mistake that matters.

## 2. What the Burr XII is

The Burr XII (Irving Burr, 1942; also called the Singh-Maddala distribution in economics, where it describes incomes) is a family of curves for positive values with **three dials**:

- **S**, the scale: the units, where the curve sits along the axis.
- **C**, the shape of the body: how the curve rises from zero and where it peaks.
- **K**, the weight of the tail.

Its formula is unusually simple. The probability of a value above x is

  P(X > x) = 1 / (1 + (x/S)^C)^K.

Far out in the tail this behaves like (x/S)^(−C·K): a **power law**, the signature of a heavy tail, with **tail index C × K**. The smaller C × K, the heavier the tail. That one number tells you which averages exist:

- C × K > 1: the mean exists.
- C × K > 2: the variance (and SD) exist.
- C × K ≤ 1: there is no mean at all. A sample's running mean never settles down, however many values you add (BurrLab's "The mean that never settles" page shows this live). The median, by contrast, always settles.

Two more things make the Burr XII a good teaching tool:

- **It contains the other families.** Set C = 1 and it is the Pareto II (Lomax); set K = 1 and it is the log-logistic; let K grow without limit (with S scaled to match) and it becomes the Weibull. So instead of guessing which family to use, you fit the Burr XII and *let the data choose*: the fit lands on a special case when a special case is right, and BurrLab names it on screen.
- **Its inverse is a formula too.** The value at any percentile p is x = S × ((1 − p)^(−1/K) − 1)^(1/C). That makes percentiles, "1 in N" return levels and simulation all exact and instant, which is why the "How rare is this?" page and the simulation page can run on a calculator.

## 3. How the fit is different from fitting a normal

For a normal curve the fit is two formulas: the sample mean estimates μ and the sample SD estimates σ. Done.

The Burr XII has no such formulas. Nothing you can compute directly from the data gives C, K and S. So BurrLab uses the general method that statisticians use when there is no formula, **maximum likelihood**:

1. **Write down how likely the data are** for any proposed C, K, S: multiply together the probability density at every data point. On a computer that product is far too small to hold (it underflows), so the program adds the *logarithms* instead: the log-likelihood, ln L. The pdf and CDF themselves are computed in logarithms too, so that a huge value of (x/S)^C never overflows the calculator's largest number.
2. **Search for the C, K, S that make ln L largest.** There is no formula for the maximum, so the program hunts for it. First it uses a shortcut: for any given C and S, the best K *does* have a formula (K̂ = n / Σ ln(1 + (xᵢ/S)^C)), which turns a three-dimensional search into a two-dimensional one over C and S. For that it uses the **Nelder-Mead simplex** (1965): a triangle of three trial points in the (ln C, ln S) plane. At each step the worst corner is reflected through the other two, stretched if that helps, pulled in if it does not, so the triangle walks uphill and shrinks onto the top. It starts from the best of 18 grid points, stops when ln L and the triangle stop changing, and gives up after 400 steps. On a G1 the PPL search takes a few seconds for 41 values and about 45 seconds for 300, so there is a progress bar and a blinking hourglass, and Esc stops it. The same search can run in MicroPython instead (Fit menu, Engine), and "Both" times the two side by side.
3. **Watch for the edges.** Because the Burr XII contains the Weibull as a *limit* (K → ∞), light-tailed data can send the search running off towards infinity: the likelihood keeps creeping up and K becomes absurd. BurrLab checks for this by fitting the Weibull as well and comparing: if the Burr fit cannot beat the Weibull's likelihood and K is large, the fit *is* the Weibull, and the screen says so instead of printing a meaningless K. The Pareto edge (C at its limit) is named the same way.
4. **Say how sure the fit is.** The standard errors come from the curvature of ln L at its peak: a sharp peak means the data pin the parameters down, a flat one means they do not. The program measures the curvature numerically (the observed information matrix) and inverts it. With 41 values the peak is flat and the SEs are wide; BurrLab says "n = 41 is small" for that reason.
5. **Compare with the rivals honestly.** Each rival family (exponential, lognormal, Weibull, gamma, Lomax) is fitted by maximum likelihood too, and all are ranked by **AIC** = 2 × (number of parameters) − 2 ln L. A family with more dials can always fit a little better, so AIC charges it for each dial. Burnham & Anderson's rule of thumb is used as stated: a difference under 2 is "about equal", over 10 is decisive. The Burr XII does *not* always win, and BurrLab shows that: on the 41 BJS sentences the lognormal wins by 4.4; on the Rossi re-arrest times the Burr runs to its Weibull limit and the plain Weibull wins by exactly 2, which is the price of one unneeded parameter.

Two more points of method:

- **Binned data.** For the 2,156 Danish fire claims the program carries the counts in 60 bins rather than every value. The likelihood then uses the probability of each bin (CDF at its top minus CDF at its bottom) raised to the count in it, the **grouped likelihood**, and the same simplex search finds its maximum.
- **Checking the fit.** The Q-Q plot compares each sorted data value with the value the fitted Burr predicts for its rank; points on the line mean a good fit, points curling away at the top mean the tail is wrong. The survival plot on log-log axes turns a power-law tail into a straight line with slope −C × K, so you can see the heaviness of the tail directly. The Anderson-Darling statistic measures the gap between the data's cumulative curve and the fitted one, weighting the tails; BurrLab gives the statistic but not a p-value, because the published tables do not cover a fitted Burr XII, and it says so.

## 4. What to try first

1. Load the BJS preset and fit it. Read the AIC table: which family wins, and by how much?
2. Open the survival plot on log-log axes. Is it straight?
3. Go to "The mean that never settles". Drag C and K down until C × K is below 1 and watch the running mean wander while the median holds still.
4. On "How rare is this?", type a sentence of 300 months and read its percentile under the fit, and the empirical one from the data. Which would you quote in court, and why?

**DISCLAIMER: BurrLab is a teaching and demonstration aid. It is not validated for forensic, clinical or legal use; do not rely on its results for legal purposes.**
