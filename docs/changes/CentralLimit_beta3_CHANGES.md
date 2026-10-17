# CentralLimit beta 3: changes from beta 2 (an APP program)

16 October 2026. The CAS version (BRIEF_CAS; `CAS_Python_Ideas_2026-10-16_v1.md` §4, CentralLimit row). It is built on beta 2 and keeps every beta 2 change. **It has not been run on hardware, and nothing about the CAS has run on our calculators.** CASProbe beta 1a decides the call form; every CAS call goes through `cltCas`, so its verdict is a one-line change there.

The app hooks keep their names exactly: `CentralLimit`, `START`, `Plot`, and the seven beta 2 VIEW entries. Two VIEW entries are new. The install notes are unchanged word for word.

Line references are `beta 2 → beta 3`.

## (a) Changes

1. **Header** (1-157 → 1-204; the what-changed block 1-103 → 1-146): beta 3, a "beta 3 - what changed" paragraph, the firmware line now says that nothing about the CAS has run and that CASProbe goes first. The Views list and the Curve/Menu lines of DASHBOARD CONTROLS name the new pages. The beta 2, 1b and 1a paragraphs, licence, AI-assistance and firmware lines are kept.
2. **File-level state** (after 232 → 281-295): `cltCasOK` (the badge), `cltExN`/`cltExD`/`cltExC0`/`cltExC1` (the exact-curve cache), `cltExPgN`/`cltExPgL`/`cltExPgC`/`cltExPgOK` (the exact-curve page, kept per n), `cltMgOn`/`cltMgL`/`cltMgC`/`cltMgOK` (the MGF page, kept), `cltPgL`/`cltPgC` (the page being built). Every LOCAL line has 6 names or fewer.
3. **The CAS kit and its helpers** (new section after `cltPause`, 546-740):
   - `cltIStr` (569) and `cltCas` (587) are BRIEF_CAS's kit, copied exactly with xx → clt, including the coordinator's later quote-stripping lines (one surrounding pair of `CHAR(34)` dropped before the undef/error test).
   - `cltIVal` (612) reads a whole number back from CAS text digit by digit, with no EXPR, so no decimal separator or Home number format is involved.
   - `cltCasNum` (704) asks the CAS for `round(evalf(answer)*10^E)` and reads it with `cltIVal`. **Every CAS answer is checked this way against the program's own number before it is shown.**
   - `cltRepl`, `cltShow` (`*` → `×`, the tagged names → s, t, n, u), `cltWrap` (breaks before + or −) and `cltScale` support the display. LEFT is never asked for 0 characters: the harness's LEFT("abc", 0) returns "abc", and the device's answer is not verified.
   - `cltIH` (725) is the Irwin–Hall density of the SUM of n uniform(0, 1) draws, by the closed form. It uses the **symmetry f(s) = f(n − s)**, so only s ≤ n/2 is summed, and a running binomial coefficient.
4. **The exact curve on the dashboard** (uniform population only):
   - `cltExCache` (new, 943) holds the exact density of the MEAN at each of the 301 pixel columns. It is built once per n and rebuilt after a new population (`cltPopStats` 589 → 849 sets `cltExN := 0`). Every frame only reads it.
   - The flat population used has the **population's own μ and σ**: U(μ − √3σ, μ + √3σ). The exact curve and the blue normal curve therefore share their centre and spread and differ only in shape (see decision 1).
   - `cltDash` (after 1030 → 1329-1346) draws the curve as black two-pixel dots on every other column, over the blue curve. Dots keep both curves visible where they agree, which they do from n = 16.
   - It is **not drawn**: while a finger previews n; above n = 49 (see 5); with the curve off; with no means yet; or for any shape but the uniform.
   - **Legend** (1052-1055 → 1366-1378): "exact" in black and "& N(μ, σ/√n)" in blue, right-aligned on the bottom panel's label row (x ≥ 202). It clears the longest left-hand label, "200 'means' of 1 member each", which ends at x = 178. Tapping there still toggles the curves.
5. **The n limit, 49.** The alternating closed form loses digits, so the program's 12-digit sum was replayed in 12-digit decimals against exact fractions (table below).
   - Error with the symmetry: 2.7e-4 of the peak (0.016 px) at n = 49, and 15 % at n = 64.
   - Error without the symmetry: 15 times the peak already at n = 36.
   - Above n = 49 the exact and normal curves differ by under 0.14 px anyway, so nothing visible is lost.
   - The CAS's own expanded polynomial, evaluated in 12 digits, is worse than the sum from n = 9 up (0.81 of the peak at n = 16). So **the program draws from its own sum, and the CAS polynomial appears only as text** (the fence's rule 3).
6. **The exact-curve page** (`cltExact`, new, 1959; Menu item "Exact curve (uniform)", `VIEW "Exact curve (uniform)"` 2547). It is built once per n and kept (a second opening makes 0 CAS calls). Contents:
   - The CAS's polynomial pieces with whole-number coefficients over (n − 1)!: all four for n = 4, the first and middle ones for n = 9, a description for larger n. Each piece is checked at the middle of its interval against `cltIH` before it is shown.
   - x̄ = μ + 2√3 σ (S/n − 1/2), the rescaling.
   - The peak as an exact fraction (n = 9: 259723/573440 = 0.452920968), or "fraction of 59 digits" when it is too long; it is never cut. The check: up to n = 49, against the program's sum to 1E-3 (the device keeps 3.7 digits at n = 49); above 49, within 1 % of the normal peak (the true gap is 0.23 % or less).
   - The normal curve's peak and how much lower the exact one is (n = 4: 3.5 %).
   - "program's sum: …, agrees to D digits", in red when D < 3. On the device this shows the digits running out: 10 at n = 16, 6 at 36, 3 at 49, 0 at 64.
   - Above 49, a red note that the dots are not drawn, and why.
   - For a population that is not uniform, two orange lines first: no exact curve is drawn for it.
   - A badge, "exact (CAS)" or "decimal".
7. **Why the bell?** (`cltMgf`, new, 2088; Menu item "Why the bell? (MGF)", `VIEW "Why the bell? (MGF)"` 2552). Text first:
   - coin flips, Z = (X1 + … + Xn)/√n, M(t) = E[e^(tZ)] = cosh(t/√n)^n;
   - CAS: `limit(cosh(cltqt/sqrt(cltqn))^cltqn,cltqn,inf)` → exp(t^2/2), "the MGF of N(0, 1)", checked at t = 1 against e^(1/2);
   - CAS: `expand(cltqn*subst(convert(series(ln(cosh(cltqu)),cltqu,0,5),polynom),cltqu,cltqt/sqrt(cltqn)))` → −1/12×t^4/n+1/2×t^2, "the t^4 term shrinks like 1/n", checked at t = 1, n = 4.

   Then a plot drawn from PPL numbers (`cltMgfAt`, cosh written with EXP so the angle mode never matters): M(t) for n = 1 (red), 4 (orange) and 16 (magenta) against e^(t^2/2) (blue, 2 px), for t from −2.5 to 2.5, with a grid, ticks and a legend in the empty middle of the box.

   If the CAS fails, the CAS lines are replaced by "M(1) = 1.5431, 1.6168, 1.6403, 1.6487 (n = 1, 4, 16, 10000) -> e^(1/2) = 1.6487" and the badge reads "decimal". The text is built once per session.
8. **The CAS is asked only when one of these two pages opens.** An "Asking the CAS ..." screen comes first (`cltAsking`), because the G1's CAS speed is unknown. No frame, drag, sampling run or one-sample animation calls the CAS: the harness counted 0 calls in each.
9. **Pages**: `cltCasPage` (1891) shows up to 15 coloured font-1 lines a screen, turns the page if there are more, puts the badge at the bottom right and lets Esc go straight back. `cltPgAdd` and `cltPgWrap` build the line lists. `cltDigits` counts the digits of a long fraction.
10. **Menu** (`cltMenu` 1614 → 2292): 12 items, with "Exact curve (uniform)" and "Why the bell? (MGF)" before Help. The Prime shows items 10, 11 and 12 as A, B and C, and nothing on screen refers to them by number. "Normal curve on / off" became "Curves on / off", because it turns both curves.
11. **Help** (`cltHelp` 1565 → 2221) has a third page: the exact curve (uniform only, black dots, agreement by n = 16, not drawn above 49, other shapes have none), the two CAS pages, and the badge. Page 2's footer leads to it, and Esc on page 2 goes straight back. Two page-2 lines were reworded: "Curve (or 0): the curves on / off." and "Menu (or Enter): settings, the CAS pages, Help."
12. Unchanged: sampling, the drag, the buttons, the one-sample animation, the square-root law, the population density overlay, the app plumbing (H1, H2, CHECK, STARTVIEW), and Home's K as the MAKELIST counter. No DRAWMENU (it is untested inside an app), no EXPR, no `#cas`, no `CAS.` dotted calls, no Python.

## Gate

`check.sh NEW = beta 3, ORIG = beta 2`, and `ppl_gate_v1a.py` (the version CLAUDE.md now names):

```
kit lint: 0 errors
ppl_check_v3 tally NEW: 9 E1, 23 E7        ORIG: 7 E1, 21 E7
  the +2/+2 are exactly the two new VIEW entries (the checker cannot read VIEW):
  E1 call to 'cltVExact' / 'cltVMgf' not defined, E7 never declared
hard errors (E2 E3 E6 E8 E10 E11) in NEW: none
lint_ppl: 1588 checks, 18 problems = the 4 known noise lines (file name, EXPORT
  discipline) + 14 "STRING() with N args": all false positives of one regex
  (STRING\s*\( with no word boundary matches INSTRING( ) -- lines 603, 619, 642,
  651, 1938, 1992, 1998, 2019, 2101, 2113 -- plus 592, the kit's own
  STRING(CAS(cltS)), which must have one argument
full parse: PARSE FAIL at #...:24h (1737), as beta 2 (1414): the tool's limit; the
  harness loads and runs the whole file
fleet_names_v2 (ppl_gate_v1a, newest of each of 27 programs, incl. today's CAS
  versions and CASProbe beta 1a): 0 collisions, 0 untagged, 0 mixed, 0 built-in
ppl_gate_v1a: RESULT: PASS
```

## Verification (`verify_CentralLimit_beta3.py`; full output in `verify_CentralLimit_beta3_output.txt`, 71 checks, ALL PASS)

```
cltIH (max |error| / peak)   12-digit sym   12-digit no sym   double   scipy irwinhall   convolution*
  n = 1..12                   <= 8.6e-11     <= 4.4e-7         <=5e-15  <= 5.4e-16        <= 1.6e-3
  n = 16 / 25 / 36            3.5e-10 / 1.5e-8 / 6.0e-7    5.8e-6 / 6.1e-3 / 15   ...
  n = 49                      2.7e-4 (0.016 px)            2.7e4
  n = 64 / 81 / 100           0.15 / 92 / 2.2e5            -> not drawn above 49
  (* grid h = 1/2000: agreement to the grid's own error)
at the peak, 12-digit digits kept: n=16 10.1, 25 8.2, 36 6.5, 49 3.7, 64 0.9
CAS polynomial in 12-digit Horner: n=4 5e-13, 9 9e-7, 16 0.81, 25 3e7  (why the sum draws)
exact vs normal, px on the 59-px panel: n=1 29.5, 4 2.08, 9 0.99, 16 0.56, 25 0.36,
  36 0.25, 49 0.18, 64 0.14, 81 0.11, 100 0.09; exact/normal peak n=4 0.9648, 9 0.9832
rescaled (mu 4.87, sigma 2.93): integral 1.00000, mean 4.87000, SD sigma/sqrt n, n = 1..49
Giac vs SymPy/fractions: 92 polynomial pieces identical; 19 exact peaks identical; every
  round(evalf(..)*10^E) check number exact; MGF limit and series identical; slowest 425 ms
harness, cas = giac: exact page n = 1..100, badge "exact (CAS)", peaks 1, 2/3,
  259723/573440, 2330931341/6810804000, then "fraction of 59 ... 297 digits"; kept per n
  (0 calls the second time); Exponential population: "no exact curve is drawn for it"
  MGF page: limit and series shown; the n = 16 curve sits on cosh(t/4)^16 to the pixel
  dashboard: dots at n = 1, 4, 16, 49 (292, 292, 212, 120); cache vs scipy < 1E-7 of the
  peak (doubles); every dot on its cache row; none at n = 64, in a drag preview, for an
  Exponential population or with the curves off; 0 CAS calls in sampling, drag, animation
harness, cas = fail: every page "decimal", "no closed form shown", the program's sums,
  the M(1) line; no error
menu: 12 items, both pages dispatch from the Menu button (giac and fail); Help 3 pages;
  layout: no text off the screen on any new page
```

**Regression:** `verify_CentralLimit.py` (beta 2's script) run on beta 3 gives the same output as on beta 2, line for line, except the two intended changes: "12 items" and "Help: 3 pages". The copy pressed three keys for Help instead of two.

## (b) DEVICE TEST CHECKLIST (least risky first)

1. **Run CASProbe beta 1a first, on the G2 and then the G1.** If it reports a different call form than `STRING(CAS(s))` (T07 against T08/T09), change the IFERR line in `cltCas` (line 592) and nothing else. Note four of its answers for this app:
   - T17: the limit is exactly this program's MGF limit;
   - T39: the series/convert(polynom) shape;
   - T35: whether 300-character texts work (this app's longest is the n = 100 peak, re-fed for its check);
   - T38: whether products print with `*`.
2. **Install as in beta 2** (Save a copy of Statistics 1Var named CentralLimit, replace its program, Check). Expected: no syntax error. Then View: two new entries, "Exact curve (uniform)" and "Why the bell? (MGF)", before Help.
3. Run beta 2's checklist items 3-13 once. Everything there should be unchanged, except that the menu has 12 items and "Curves on / off".
4. **The dots.** Uniform population, defaults, at n = 1:
   - a flat row of black dots spans the pile;
   - the label row reads "exact & N(μ, σ/√n)" in black and blue;
   - press n+: at n = 4 the dots run close to the blue bell, and from n = 16 they sit on it;
   - at n = 64 and 100 the dots are gone and the label reads "curve = N(μ, σ/√n)";
   - Curve (or 0) removes both curves;
   - drag along the top panel: no dots while previewing;
   - Exponential population: never any dots.

   Watch the G1 at each new n for a pause on the first frame (the cache: about 110 columns × 25 terms at n = 49).
5. **Help**, three pages: the third explains the dots, the two pages and the badge. Esc on page 2 goes straight back.
6. **CAS steps** (each shows "Asking the CAS ..." first; time it on the G1):
   - **Menu → Exact curve, n = 4.** What you should see: four pieces, s^3/6, (−3×s^3+12×s^2−12×s+4)/6, (3×s^3−24×s^2+60×s−44)/6 and (−s^3+12×s^2−48×s+64)/6; "exact: 2/3 = 0.666666667"; "normal curve: 0.690988299; exact is 3.5% lower"; "program's sum: 0.666666667, agrees to 12 digits" (11 or 12 on the device); badge **exact (CAS)**. Open it again: no Asking screen (kept).
   - **n = 9**: two pieces, the middle one wrapping to three lines; "exact: 259723/573440 = 0.452920968"; "1.7% lower".
   - **n = 49**: "exact: fraction of 139 digits = 0.196819926"; the program's sum agrees to **about 3 digits on the device** (7 in the PC harness, which uses doubles). It should still be green, not red.
   - **n = 64, 100**: the sum agrees to 0 digits, in red, with the red note that the dots are not drawn above 49. This shows the 12-digit cancellation on the calculator itself.
   - **Exponential population → Exact curve**: two orange lines first, "no exact curve is drawn for it".
   - **Menu → Why the bell?** What you should see: "CAS: as n grows, M(t) -> exp(t^2/2):" and "CAS: ln M(t) = −1/12×t^4/n+1/2×t^2 + ..."; four curves, red under orange under magenta under the thick blue, all meeting at t = 0 near the bottom; badge **exact (CAS)**.
7. If the CAS fails anywhere, the same pages should show "no closed form shown" or the M(1) line, with the "decimal" badge and no error box. If an error box or the Program Editor appears instead, note the routine and line.

## (c) Not confirmed, or left as it was

- **Everything CAS-side**, on both calculators:
  - the call form, the quote stripping, `inf`, and `sum(seq(...))`;
  - `expand`, `convert(..., polynom)`, `series`, `subst`, `round(evalf(...)*10^(E))` and `comb` on the Prime's older Giac;
  - and how long any of it takes on a G1.

  Desktop Giac 1.9 did every template in under 0.5 s. If the Prime's Giac prints its answers differently (a dot for ×, or ∞), the checks fail safe: the page shows "no closed form shown".
- **Harness vs device digits**: the harness computes in IEEE doubles, so its "agrees to D digits" lines are more optimistic than the device's from n = 25 up. Part 1 replays the program's sum in 12-digit decimals for the device's numbers.
- **The CAS answers stand for the polynomial; the dots come from the program.** No CAS number is used for drawing, and EXPR is not used at all.
- `INSTRING`, `MID` with three arguments, `CONCAT` of lists of strings, and `CHAR(34)`/`CHAR(8722)` in comparisons are not on the device-verified list (INSTRING ran in PyProbe on the emulator).
- **Font-1 widths** (6 px a character) are an estimate. The longest new lines are 49 characters (about 294 px): check the wrapped polynomial lines and the legend on the device.
- **The MGF page's legend position** (x 126-234, y 112-136) relies on all four curves being low near t = 0. The program computes this from the same numbers, so it holds by construction.

## Decisions for Roger

1. **The exact curve uses a flat population with your population's μ and σ**, not the U(a, b) you typed. A population of N = 500 draws from U(0, 10) has μ and σ a little off 5 and 2.887. At n = 100 a curve centred on the typed 5 would sit 0.45 SE away from the pile and from the blue curve. The matched version differs from the blue curve only in shape, which is the lesson. The black density line in the top panel still shows the typed U(a, b). If you prefer U(a, b), the change is in `cltExCache`: ecA and ecW.
2. **The dots are drawn by the program's own sum, not from the CAS's polynomial.** That polynomial in 12-digit arithmetic is wrong by 81 % of the peak at n = 16. The fence says to draw from PPL numbers, and a CAS call on every n+ press would put the G1's unknown CAS speed into the dashboard. The CAS shows the exact pieces and the exact peak on its page, and checks itself against the program there.
3. **No exact curve above n = 49** (64, 81, 100). Above 49 the sum has lost its digits in 12-digit decimals, and the two curves are within 0.14 px anyway; the exact-curve page says so. A stable method exists (the B-spline recursion) but costs about 1.5 million operations at n = 100.
4. **The Curve button turns both curves on and off** (the menu item is now "Curves on / off"). A separate exact-curve toggle would have meant a 13th menu item.
