# StatDist v2.6 -> v2.7: what changed, and what to test on the calculator

*16 October 2026. The CAS version (BRIEF_CAS; `CAS_Python_Ideas_2026-10-16_v1.md` §4, StatDist row: a "Formula" page per distribution). Built on v2.6, with every v2.6 change kept. **v2.7 has not been run on hardware, and nothing about the CAS has run on our calculators.** CASProbe beta 1a decides the call form; every CAS call goes through `st_Cas`, so its verdict is a one-line change there.*

Files (all in `/home/claude/work/out/`):

- `StatDist_v2.7.txt` (4,039 lines; v2.6 had 3,176);
- `verify_StatDist_v2.7.py` and its output, `verify_StatDist_v2.7_output.txt`;
- this note.

Line numbers: "v2.6 n" is the old file, "v2.7 n" the new one.

## (a) The changes

1. **Header** (v2.6 1-144 → v2.7 1-190):
   - v2.7 in the title;
   - the firmware line says nothing about the CAS has run and that CASProbe goes first;
   - a new "What changed in v2.7" block;
   - the file map lists sections 3b and 7b.

   The v2.6 and v2.5 blocks, the licence, the AI-assistance line and the firmware line are kept. The help page's title string is now "Statistical Distributions v2.7" (v2.6 1938).
2. **File-level state** (after v2.6 190 → v2.7 237-251): `stCasOK` (the badge), `stFmL`/`stFmC`/`stFmOK` (the kept page), `stFmK` (the plot state it was built for), `stFmSy`/`stFmR`/`stFmXR`/`stFmPT` (the symbolic-parameter bookkeeping). They are set in `st_Init`, as the v2.6 state is. LOCAL lines have 6 names or fewer.
3. **Section 3b, the CAS kit** (new, v2.7 615-810, after `st_gompMom`):
   - `st_IStr` (637) and `st_Cas` (655) are BRIEF_CAS's kit, copied exactly with xx → st, including the coordinator's quote-stripping lines.
   - `st_IVal` reads a whole number back digit by digit (no EXPR, so no separator or Home format is involved). `st_CasNum` asks for `round(evalf(answer)*10^E)`, with `st_Scale` choosing E.
   - `st_Rat` asks whether a value is a **simple ratio** (a whole number over 10^d, d ≤ 6). `st_RTxt` writes it as CAS text, (85/10^3). `st_LTxt` writes ANY real as its 12-digit ratio, which is used only to check a symbolic answer at the user's value.
   - `st_Repl`, `st_Wrap` and `st_Digits` support the display. LEFT is never asked for 0 characters.
4. **Section 7b, the Formula page** (new, v2.7 3068-3642, before `st_Options`). It is built by `st_FmBuild` when the page opens and kept until the plot's state (`st_FmKeyNow`: the family, the three parameters, the tail, x, a, b) changes. An "Asking the CAS ..." screen comes first. The page shows:
   - the parameters (`st_ParStr`) and the density or pmf in words (`st_FmF`);
   - **continuous families**:
     - E[X] = integral of x f(x), E[X^2] = integral of x^2 f(x), and Var(X) = E[X^2] − E[X]^2, made from those two answers;
     - for the Exponential, Weibull and Pareto, also F(x) = integral of f(t) from the lowest value to x, checked at the plot's x (at b in a<X<b);
     - the templates are `st_FmDens`, one per family. Laplace is split in two halves (no |x| reaches the CAS); the Triangular is two pieces, leaving out a side of zero width;
   - **a moment that does not exist** (Cauchy; t with df ≤ 1 or ≤ 2; Pareto α ≤ 1 or ≤ 2; F df2 ≤ 2 or ≤ 4; Burr KC ≤ 1 or ≤ 2): the CAS should find the integral infinite, from the centre up for the symmetric t and Cauchy. The page then says "infinity (CAS) ... So there is NO mean (the program: undef)";
   - **discrete families** (`st_FmPmf`): the probability on the plot as an exact sum for every tail (upper = 1 − the sum; a<X<b from a to b); the red bar's P(X = k); and for the Binomial and Hypergeometric the mean as a finite sum. Exact sums are only asked for at moderate sizes: Binomial n ≤ 200, Poisson k ≤ 150, Geometric k ≤ 500, Negative binomial k and r ≤ 200 (the Hypergeometric is already capped at N = 1000). Beyond those the page says the numbers are too large and shows the program's value.
5. **Never a wrong formula** (`st_FmAsk`, v2.7 3320). A CAS answer is shown only if:
   - `st_FmGood` passes: it is not an unevaluated `integrate`/`sum`/`seq`/`limit`, not conditional or piecewise, and not infinite;
   - **and** the CAS's own decimal of that very answer (re-fed, through `st_CasNum`) agrees with the program's value to 1E-6 relative. The program's values come from `st_Mom`, `st_cdf`, `st_Prob` and `st_pdf`.

   Otherwise the page says "no closed form shown" and gives the program's decimal. Desktop Giac was tested on every family:
   - the check rejects the Logistic's E[X^2], which Giac gives as −π²/3 with the wrong sign;
   - Giac leaves undone the Gumbel, Fréchet and Gompertz moments, the Logistic with s = 2, and the Burr with non-integer shapes;
   - **0 wrong answers reached a page.**
6. **Exact ratios and symbols** (`st_FmPars`, `st_FmAsm`, `st_FmSub`).
   - A simple parameter goes into the CAS text as its exact ratio, so the answers are exact: Exponential(1/2): 2, 8, 4; Normal(100, 15): 100, 10225, 225; Binomial(20, 1/2): 308333/524288.
   - A parameter that is not a simple ratio (1/3 typed as 0.333333333333, or π) stays a symbol (stqa, stqb, stqc), with " | stqa>0" for a scale or shape. The page says so in grey and shows the symbolic result: Exponential: 1/λ, 2/λ^2, 1/λ^2, F(x) = −exp(−λ×x)+1. Normal σ: σ^2+4. Poisson λ: (λ^2+2×λ+2)/(2×exp(λ)).
   - The decimal shown is the program's. The check substitutes the 12-digit ratio for each symbol.
7. **Display** (`st_FmShow`, `st_FmRes`, `st_FmPage`):
   - `*` is shown as × and ^ and / are kept; the tagged names are shown as x, t, k or the parameter's name;
   - a fraction longer than one line becomes "an exact fraction of 78 digits", and any other form longer than three lines "an exact form of N characters", with the program's decimal below; it is never cut;
   - pages hold 16 font-1 lines a screen, turning over if there are more, with the house footer and the badge "exact (CAS)" or "decimal" in dodger blue;
   - an infinite answer is read as "+infinity" or the ∞ glyph, CHAR(8734), since CASProbe T41 asks which the Prime prints. A minus infinity is never read as one.
8. **Soft keys: "More" turns three pages** (`st_Draw` v2.6 2500-2520 → v2.7 2775-2801; `st_Plot` v2.6 2856-2877 → v2.7 3715-3742). Page 3 is **{Formula, Help, , , Menu, More}**:
   - Menu sits in slot 5 as on page 2, and More stays in slot 6;
   - nothing destructive is under the finger after a page turn;
   - Help on page 3 also fills a v2.6 gap: Help was not on any soft key, so a touch-only student had no route to it from the plot.

   Pages 1 and 2 are unchanged, and More from page 3 returns to page 1.
9. **Enter → "Plot options"** (`st_Options` v2.6 2791 → v2.7 3648): "Formula page (CAS)" is item 2 in all three menus (action 10). The other items keep their order.
10. **Help** (`st_show_help` v2.6 1936 → v2.7 2197): "More again = page 3: Formula = ..." and a short "THE FORMULA PAGE (the CAS)" section on the badge and on "no closed form shown". It now runs to 40 lines on four pages.
11. **Untouched, as asked**: the plot, the drag, the caches (`st_Cache`, `st_Fit`, `st_Draw`'s frame), the dispatch (`st_pdf`, `st_cdf`, `st_icdf`, `st_Mom`), the forms, the gallery and the menus. **No frame and no drag calls the CAS.** For 5 distributions the harness found the plot frame identical to v2.6's: every text, shape and soft-key label.

## The gate

`check.sh NEW = v2.7, ORIG = v2.6`, and `ppl_gate_v1a.py` (the version CLAUDE.md now names):

```
kit lint: 0 errors
ppl_check_v3 tally NEW: clean           ORIG: clean
hard errors (E2 E3 E6 E8 E10 E11) in NEW: none
lint_ppl: 2626 checks, 27 problems = the 4 known noise lines (file name / EXPORT
  discipline, as in v2.6) + 23 "STRING() with N args": all false positives -- the
  lint's regex STRING\s*\( has no word boundary and matches INSTRING( on lines 671,
  685, 708, 717, 806, 3296-3299, 3312, 3338, 3339, 3406 -- plus 660, the kit's own
  STRING(CAS(stS)), which takes one argument.  (An earlier run also flagged "concatenates
  bare fdA": those are pieces of CAS TEXT, now marked as text with "" + .)
full parse: PARSE FAIL at <ppl>:201 (file-level LOCAL), as v2.6 at 155: the tool's limit;
  the harness loads and runs the whole file
fleet_names_v2 (ppl_gate_v1a, newest of each of 27 programs, incl. today's CAS
  versions and CASProbe beta 1a): 0 collisions, 0 untagged, 0 mixed, 0 built-in
ppl_gate_v1a: RESULT: PASS
```

## Verification (`verify_StatDist_v2.7.py`, ALL PASS; output pasted, shortened)

Every family at its defaults plus 50 other parameter sets: other values, moments that do not exist, symbols, the three tails, an oversize Binomial. Each was run through the program's Formula page with cas = 'giac'. Each answer the page SHOWS was then re-read independently: Giac's text parsed by SymPy at the user's values, against SciPy.

```
Normal (0,1)          mean ok; e2 ok; var ok          Exponential (1)     mean, e2, var, cdf ok
Weibull (2,1)         sqrt(pi)/2, 1, (4-pi)/4, cdf    LogNormal (0,1)     exp(1/2), exp(2), var ok
Laplace, t(10), chi2(10), F(10,15), Burr(2,2,1), Rayleigh, Triangular, Maxwell, Erlang,
  Gamma(2.5,2), Beta(2,5): mean, e2, var ok           Pareto (1,3)        3/2, 3, 3/4, cdf ok
Gumbel, Frechet, Gompertz: not shown (Giac leaves them undone) -> "decimal" badge
Logistic (0,1):  mean ok; e2 not shown: disagreed with the program (-pi^2/3)
Cauchy, t(1), F(4,2), Burr(1,1,1), Pareto(1,1): "infinite" -- no mean (and no variance)
t(2), Pareto(5,1.5): mean ok; E[X^2] infinite -- no variance
Binomial(20,1/2): 308333/524288, 46189/262144, 10    Poisson(5): 118/(3 exp(5)), 125/(6 exp(5))
Geometric(0.3): 657/1000, 147/1000   NegBin(3,0.4): 9064/15625   Hypergeom(50,40,6): 28696/37835,
  109668/264845, 24/5   Hypergeom(1000,400,50) ok   Binomial(20,0.37) a<X<b: "an exact fraction
  of 78 digits"   Binomial(500): "too large for an exact sum" (no CAS call)
symbols: Exponential(1/3), Normal sigma 1/3, Weibull lambda 1/3, Pareto alpha 1/3 (CDF),
  Rayleigh sigma = pi, Gamma theta 1/3, Binomial p 1/3, Poisson lambda 1/3: all ok

[ok] every CAS answer the page shows agrees with SciPy (no wrong formula)
     -- 197 shown and correct, 16 rejected, 0 wrong
[ok] exact comparisons (Python fractions for discrete; SymPy's own integrals, to 40
     digits, for 13 continuous families) agree -- 98 of 98
     Giac time over all 77 pages: 14.4 s; slowest page 396 ms (Chi-square(3))
[ok] cas = fail, all 27: "decimal" badge, the program's decimals, no runtime error
[ok] More, More: page 3 {Formula, Help, , , Menu, More}; page 2 unchanged; More x3 -> page 1
[ok] page 3: Formula opens and asks the CAS; Help opens; Menu leaves the plot
[ok] Enter -> "Plot options" item 2 = "Formula page (CAS)"; opened twice: built once
     (8 CAS calls), shown twice; new parameters rebuild it
[ok] a drag on the plot (6 frames) calls the CAS 0 times
[ok] the plot frame (texts, shapes, soft keys) is identical to v2.6 for 5 distributions
[ok] st_Cas drops one surrounding pair of quotes: "1/2" -> 1/2; "undef" -> ''
```

**Regression:** v2.6's own two scripts were run on v2.7.

- `verify_StatDist.py`, the dispatch against SciPy: **ALL PASS**, the same table as v2.6.
- `run_StatDist_v2.6.py`: **part A 81/81, part B 58/58**. The copy had three edits for the intended changes:
  - the options item numbers, shifted by the new item 2;
  - the help title v2.7;
  - four help pages instead of three.

## (b) DEVICE TEST CHECKLIST (G2 first; least risky first)

1. **Run CASProbe beta 1a first, on the G2 and then the G1.** If it reports a different call form than `STRING(CAS(s))` (T07 against T08/T09), change the IFERR line in `st_Cas` (v2.7 660) and nothing else. Note five of its answers for this program:
   - T21: `int(..., -inf, ...)`, the same input form as the Formula page;
   - T41: how an infinite answer prints. `st_FmInf` reads "infinity" or ∞; anything else fails safe;
   - T38: whether products print with `*`;
   - T35: how long a CAS text can be. This program re-feeds answers up to about 400 characters, for example the 78-digit fractions;
   - T26/T29: whether a CAS error is caught by IFERR.
2. **Paste and compile** v2.7 (`fleet_names_v2.py` first). New constructs the fleet has not run:
   - INSTRING and MID with three arguments in loops;
   - `STRING(v, 2, 12)`;
   - list literals with strings built across lines (`st_FmDens`);
   - the quote-strip comparison with CHAR(34).
3. Run v2.6's checklist items 3-13 once. They should be unchanged, except: More now turns to a third page; the Enter options have "Formula page (CAS)" second (8 or 9 items); Help is four pages.
4. **Soft keys.** On the Normal plot tap More twice: the strip reads **Formula, Help, (blank), (blank), Menu, More**. Help opens the four help pages. More once more returns to P<=x ... Then More, More, Menu leaves the plot.
5. **CAS steps** (each opens with "Asking the CAS ..."; **time it on the G1**). The badge should read **exact (CAS)** wherever an answer is shown.
   - **Normal(0, 1)** → Formula. What you should see: "= 0 / = 0.000000, the program's value: agree", then E[X^2] "= 1", then Var "= 1". Open it again: no Asking screen (kept).
   - **Exponential, rate 0.5, x = 1.5**: mean 2, E[X^2] 8, Var 4, and "F(x) = −exp(−1/2×x)+1, at x = 1.5: 0.527633".
   - **Weibull(2, 1)**: mean sqrt(pi)/2, Var (−pi+4)/4, F(x) = (exp(x^2)−1)/exp(x^2).
   - **Pareto(1, 3)**: 3/2, 3, 3/4, F(x) = (x^3−1)/x^3.
   - **Logistic(0, 1)**: the mean is shown, and **E[X^2] says "no closed form shown"**, with the program's 3.289868. Desktop Giac gives a wrong sign there, and the check catches it. If the Prime's Giac gets it right, it will be shown; either way it is never wrong.
   - **Cauchy**: "from the centre up alone: infinity (CAS). So there is NO mean".
   - **Gumbel, Fréchet, Gompertz**: "no closed form shown" and the "decimal" badge.
   - **Binomial(20, 0.5), P(X <= 10)**: "= 308333/524288 / = 0.588099 ... agree", the red bar 46189/262144, and E[X] = 10. In a<X<b with p = 0.37: "an exact fraction of 78 digits".
   - **Poisson(5), P(X <= 3)**: "118/(3×exp(5))".
   - **Hypergeometric(50, 40, 6), P(X > 5)**: 9139/37835 = 0.241549.
   - **A symbol**: Exponential with rate typed as 1/3. A grey line says it stays the symbol λ, and the answers read 1/λ, 2/λ^2, 1/λ^2.
6. **With the CAS failing** (or if CASProbe says the call form is wrong), every Formula page should show "no closed form shown", the program's values and the "decimal" badge, with no error box. If the Program Editor opens instead, note the routine and line.
7. **Speed on the G1.** A page makes up to 8 CAS calls. Desktop Giac took 60-400 ms per page; nothing is known about the G1. If a page takes more than about 10 s, say so: the next version can drop E[X^2] (2 calls) or the CDF.
8. Exit: Home shows "StatDist: P(...) = ..." as before.

## (c) Not confirmed, left as it is

- **Everything CAS-side, on both calculators**:
  - the call form, the quote stripping and `inf`;
  - `simplify`, `int`, `sum(seq())`, `subst`, `round(evalf(...)*10^(E))`, `Gamma`, `Beta` and `comb` on the Prime's older Giac;
  - the `| stqa>0` assumption form, used only for non-simple parameters (not in CASProbe; a failure shows "no closed form shown");
  - whether the Prime's CAS output, re-fed for the check, parses;
  - and the G1's speed.

  Every one of these fails safe, to "no closed form shown".
- **Results the Prime's Giac may handle differently from desktop Giac 1.9.** Desktop Giac could not do the Gumbel, Fréchet and Gompertz moments, the Logistic's E[X^2] (wrong sign), the Logistic with s ≠ 1, the Burr with non-integer shapes, or the Pareto mean with a symbolic α. The Prime may do better or worse; the check decides on the device.
- **Harness arithmetic is IEEE double; the device has 12 digits.** The 1E-6 relative check leaves room for the program's own accuracy (Lanczos ~1E-10, Gompertz Simpson ~3E-9).
- **Display**: the 6.5 px/character estimate for font 1 (46 characters a line) and the ∞ glyph are unverified. The × glyph is verified.
- Lint false positives, as listed in the gate.

## Decisions for Roger

1. **Page 3 of the soft keys holds Formula and Help** (with Menu in slot 5, as on page 2). Help was the one action a touch-only student could not reach from the plot; two slots stay empty. If you would rather keep page 3 to Formula alone, remove one line in `st_Draw` and one in `st_Plot`.
2. **Logistic E[X^2], Gumbel, Fréchet and Gompertz moments show "no closed form shown"**, although the textbook has closed forms (π²s²/3 + μ², μ + γβ, Γ(1 − 1/α) ...). They come out that way because the CAS cannot produce them reliably. If you want them, the honest route is a CAS substitution the student can follow, for example u = e^(−z) for the Gumbel. That is not done here.
3. **The exact-sum size limits** (Binomial n ≤ 200, Poisson k ≤ 150, Geometric k ≤ 500, Negative binomial k, r ≤ 200) are guesses for the G1's unknown CAS speed. Adjust them after timing step 7.
4. **E[X^2] is shown as well as Var(X)**, as the task asks. It costs 2 of the 8 calls a page if the G1 proves slow.
