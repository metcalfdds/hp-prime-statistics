# PowerViz v2.5g: changes

*Superseded the same day by v2.5h to v2.5k, which carry everything here; v2.5g was not committed on its own. Its verify script, `verify_PowerViz_v2.5g.py`, is in the author's folder; `verify_PowerViz_v2.5k.py` runs every one of its checks on v2.5k (test 5's expected texts updated to the new readout box and "40, 20").*

*31 October 2026. Built from v2.5f by `make_v25g.py` (66 exact replacements, each required to match once). 2,941 lines: 1,806 of code and 993 of comments (v2.5f: 2,608 lines, 1,630 and 843).*

## Why

Roger, 31 Oct 2026: "the way we have PowerViz set up now, it accommodates a two-sample means test where there is equal variance and equal sample sizes -- we need to add another menu item for unequal variances and unequal n."

The same version carries a fix that Lessons Learned v7m (20 Oct 2026) had left "for the next version". The critical z was worked out as `NORMALD_ICDF(0,1,1-AL/TL)`. A typed α of about 1E-12 or less makes 1 − α exactly 1 in the Prime's 12 digits, and `NORMALD_ICDF(0,1,1)` is ∞ on the G1, with no error message.

## What changed (line numbers are v2.5g's)

### The fifth test: two means, unequal σ and n (z)

- **The test menu** (`pv_SelTest`, 2223) has five items.
  - The new one is third, beside the other two-means test: **"Two Means, unequal σ & n (z)"**.
  - The old second item now says what it assumes: "Two Means, equal σ & n (z)". Only the label changed.
  - Every item is at most 30 characters (round 1 on the emulator cut longer CHOOSE lines at the box edge).
  - Inside the program the new test is `TT = 5` (`tmap := {1,2,5,3,4}`, 2232), so tests 1–4 keep their numbers and their code.
- **Defaults** (2250): μ₁ = 100, μ₂ = 105, σ₁ = 10, σ₂ = 20, n₁ = 40, n₂ = 20, α = 0.05, 1-sided. Group 2 is twice as spread out, and the people are split the wrong way round on purpose, so the formula page's best-split line has something to teach: put more people where σ is larger.
- **New file-level values** (398):
  - `SG2`: the σ of group 2 (`SG` is group 1's).
  - `NN2` and `KN1`: the n₂ and the n₁ as the student typed them.
  - `NN` remains n₁ as it is now.
- **The model** (`pv_Model`, 1169): M₀ = 0, M₁ = μ₂ − μ₁, and SE = √(σ₁²/n₁ + σ₂²/n₂), the same under H₀ and H₁. It is a z test with the σs taken as known, like the other four tests.
  - The SE is computed as m √((σ₁/m)²/n₁ + (σ₂/m)²/n₂), where m is the larger σ. A typed σ of 1E-300 or 1E300 then never squares past the Prime's range (1E-499 to 1E499) into 0 or ∞.
  - σ′ (`pv_SigE`) and the closed-form n (`pv_NCF`) are scaled the same way.
- **How n₂ follows n₁** (`pv_N2`, 547): n₂ = max(2, round(n₁ × typed n₂ / typed n₁)). The arrows, a vertical drag and the Pow-n view change n₁, and n₂ keeps the typed ratio. G*Power and statsmodels call this the allocation ratio. Rounding never makes n₂ go down as n₁ goes up, so power still rises with n₁ and the n₈₀ search still works.
- **Taking typed sizes** (`pv_Set5`, 567), from the Edit form or the n cell's form:
  - n₁ and n₂ are each a whole number from 2 to 5000.
  - n₂ is kept between 0.1 and 10 times n₁.
  - Each changed value gets one box saying what was changed and why, as for every other clamp in PowerViz.
  - If the pair is what the screen already showed, nothing changes, so pressing OK on an untouched form never nudges the ratio by a rounding. Otherwise the typed pair becomes the new ratio.
- **Cohen's d** (`pv_SigE`, 532; `pv_EffSz`): d = (μ₂ − μ₁)/σ′, where σ′ = √((σ₁² + σ₂²)/2), "the square root of the mean of the two variances".
  - Source: Cohen (1988), *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed., p. 44, eq. 2.3.2, read on the page (Roger's copy, 31 Oct 2026).
  - The same page keeps the small/medium/large labels for d when σ_A ≠ σ_B.
  - The arrow step (σ′/20, pushed to 1-2-5) and the power-vs-effect view use σ′ too.
- **The readouts**:
  - The panel's n cell reads "n = 40/20" (n₁/n₂).
  - The SE line reads "SE₀ = √(10²/40+20²/20) = 4.74". It gives way to the n₈₀ text on the same row (`pv_SELine(slx)`, 1329): first to the symbols, then to the value alone.
  - n₈₀ reads "n₈₀ = 223/112 (222.6)"; the bracket is the formula's n₁.
  - Pow-n: the x axis is n₁, labelled "n₁ (n₂ = 0.5 × n₁)". The footer reads "n = 40/20: power = 0.277, …" and the n₈₀ line "n₈₀ = 223/112".
  - Pow-effect: the subtitle reads "n = 40/20, α = 0.050, 1-sided".
  - The drag hint reads "n = 55/28: drag up = larger n₁ (n₂ follows)".
  - The exit box reads "n₁ = 40, n₂ = 20". `EP_NPG` holds n₁. No export was added; the exit box names n₂.
- **The forms**:
  - The Edit form (2081) has seven fields: μ grp1, μ grp2, σ grp1, σ grp2, n grp1, n grp2, α. The two n fields go into LOCALs and then through `pv_Set5`. A σ₂ of 0 or less is reset to 1, with a box.
  - A tap on "n =" (`pv_EditN`, 2169) opens a two-field form, "Sample sizes".
- **The formula page** (`pv_Formula`, 2267):
  - **The equation:** (μ₂−μ₁ − zα SE₀)/SE₁ = zβ, with SE = √(σ₁²/n₁ + σ₂²/n₂) and n₂ = k n₁.
  - **The symbolic solve for n₁** (`pv_Eq`, 791). The CAS gets SE as √(k σ₁² + σ₂²)/√(k n₁), with √(k·pvn) kept apart. Desktop Giac 1.9 then answers with one clean root: ((√(k σ₁²+σ₂²) zα + √(k σ₁²+σ₂²) zβ)/(μ₂−μ₁))²/k. Written as √(σ₁²+σ₂²/k)/√n, the same equation brings in abs(k) and k².
  - **The solve with the student's numbers:** σ₁ and σ₂ go in as exact ratios, and k as n₂/n₁ from the two typed whole numbers, so no decimal ever goes into CAS text.
  - **PPL's line:** n₁ = ((zα + zβ) × √(σ₁² + σ₂²/k)/δ)².
  - **Rounding up:** "Round UP: n₁ = 223, n₂ = 112".
  - **The best split:** "Best split of n₁+n₂: n₂/n₁ = σ₂/σ₁ = 2.00 (yours 0.50)", shown when the 15-line page has room (2487).
  - **Without the CAS:** the textbook form (zα+zβ)²×(σ₁² + σ₂²/k)/(μ₂−μ₁)² with the "decimal" badge, and "(no CAS) σ₁ = …" on one line.
- **Help page 4** (2585, "unequal σ and n"), fourteen lines:
  - the SE;
  - n = n₁/n₂ on screen;
  - the kept ratio;
  - σ′;
  - the best split of a fixed total (n₂/n₁ = σ₂/σ₁);
  - **Cohen's warning from the same p. 44**: with unequal σ *and* unequal n, the pooled t test's α and power can be far off. This test does not pool: its SE is Welch's;
  - the z test takes σ₁ and σ₂ as known, while Welch's t test estimates them and has less power when n is small;
  - what n₈₀ = 40/20 means.

  Pages 1–3 are now titled 1/4 to 3/4, and page 3's footer says "next page".
- **The H₁ drag** works on the difference axis, as in test 2.
- **`pv_MeanT()`** (522) now answers "is this a means test?". Every v2.5f "TT<=2" became `pv_MeanT()==1`, and every "TT>=3" became `pv_MeanT()==0`.

### The mirrored critical z (all tests)

`-NORMALD_ICDF(0,1,AL/TL)` is now used at all five sites: `pv_NCF` (833), `pv_Model` (1185), `pv_Tails` (1462, 1464) and `pv_Formula` (2273). At every ordinary α it gives the same z as before, to 1E-12. At α = 1E-13 it gives 7.349, where v2.5f asked for ∞.

### Not changed

- **Tests 1–4:** every text of every screen the verify script reaches is identical to v2.5f's, apart from help pages 1–3's titles and page 3's footer. The only exceptions are four states where power is exactly α = 0.001 (no effect). There the two z forms differ in the last bit, so v2.5f printed "< 0.001" and v2.5g prints "0.001", the true value. The stopped review's own regression found the same thing, plus the matching β = 0.001 at α = 0.999 and a one-pixel shift of a flat Pow-n curve in no-effect scenes.
- The CAS kit (`pv_Cas`, `pv_Rep`, `pv_Strip`, `pv_CasUse`), the drawing passes, the soft keys, the other gestures and the exports.
- The formula page's "zα = z(…)" label still prints `pv_NumD(1-AL/TL)`. That is display only: at a typed α below 1E-4 it reads "z(1)", while the z itself is right.

## Verification

`verify_PowerViz_v2.5g.py` (it runs from the repository alone: tools/ and programs/ by relative path, and v2.5f from git history once it has left programs/). Output: `verify_PowerViz_v2.5g_output.txt`, **51 checks, 0 failures**.

- **A, tests 1–4 against v2.5f:**
  - The main view in 512 states: identical but for the four floor knife-edge states, which are listed.
  - Engine numbers (PW, ZC, XCL, XCU, N80, NCF, SE0, SE1) agree to 1.6E-14.
  - The Pow-n view, the Pow-effect view and the formula page (with and without the CAS), 48 runs: identical.
  - Help pages 1–3: identical apart from the titles and page 3's footer.
  - α = 1E-17: v2.5f asks `NORMALD_ICDF(0,1,1)`; v2.5g gives 8.494. In the harness's doubles 1 − α only becomes 1 below about 1E-16; on the Prime it is 1 from about 5E-13.
- **B, test 5's arithmetic, routine by routine:**
  - Power in 320 states (both directions, both tails) equals the z formula in SciPy (2.2E-16), equals statsmodels' NormalIndPower with the SE mapped, and agrees with a simulation of the z test itself (200,000 trials, within 4 SE).
  - `pv_N80` equals a brute-force search with the n₂ rule written independently.
  - `pv_NCF` equals (zα+zβ)²(σ₁²+σ₂²/k)/δ² and statsmodels' solve_power.
  - The symbolic CAS template, through Giac and SymPy, equals the closed form; the numeric templates equal `pv_NCF` in 15 cases; no CAS text contains a decimal point.
  - σ′, d, the step, `pv_N2` (rounding, never decreasing, never below 2), `pv_NStr` and `pv_Set5`'s clamps all check out.
  - σ of 1E-200 and 1E200 give the unscaled scene's power, d and n₁.
  - Help page 4's claims:
    - **Best split:** brute force over every split of five totals.
    - **Cohen's warning:** simulated under H₀ at a nominal 0.05, σ 10/20 with n 40/20 rejects 11.1 % with the pooled t test, 1.7 % with n 20/40, and 5 % with Welch's.
    - **Welch versus this z test:** Welch has less power at small n and about the same at n 200/100.
- **C, test 5's screens and forms:**
  - the main view at the defaults;
  - the menu;
  - the Edit form and its clamps;
  - the n cell's form;
  - Up, Up, Down (40/20 → 45/23 → 50/25 → 45/23);
  - a vertical drag;
  - the H₁ drag;
  - the Pow-n sweep, equal to SciPy in every column, and picking n by touch;
  - the Pow-effect sweep;
  - the formula page with the CAS and without;
  - help page 4;
  - the exit box and the exports.
- **D, layout:** the overlap recorder over every screen the script drew. v2.5g has no firm overlap, straddle or overrun that v2.5f lacks; the three v2.5f has are at absurd inputs and are unchanged. On the generic walk (`text_overlap_v1.py --walk`) both versions have the same nine firm "tight" rows and no overlaps.

**The independent review was stopped by a session interruption before it reported.** Its saved scripts were used:
- **Its regression of tests 1–4** found only the floor knife-edge described above.
- **Its crash sweep:** 720 runs of test 5 at extreme inputs, through every view: means 0 to 1E6, σ from 1E-200 to 1E150, ratios from 0.1 to 10, n from 2 to 5000, α at 1E-13, 0.05 and 0.999. It found no failure on the Prime's terms. Its one finding (σ 1E150 with δ 1E-9) is the harness's double overflowing in `pv_NCF` at about 6E318. v2.5f's test 2 fails identically, and the Prime's 1E499 range holds that value.

## Gate

`ppl_gate_v1c.py PowerViz_v2.5g.txt PowerViz_v2.5f.txt`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: no hard errors. The new E9s are `STRING(n,1,0)` on whole numbers, PowerViz's own pattern for n. The new E1s are list indexing that the checker reads as calls (`tmap(tsel)`).
- lint_ppl: the same four file-name notes as v2.5f.
- Full parse: the kit's known limit, as for v2.5f.
- fleet_names_v2 over 27 programs: 0 collisions, 0 untagged, 0 built-in matches.

None of the 22 new names matches a built-in or another name in the file when case is ignored. The file's two older case pairs (`dV`/`dv`, `dD`/`dd`) belong to different routines and are unchanged from v2.5f.

## Device checklist (G2 first, then G1)

Replace PowerViz in the Connectivity Kit by opening it and pasting over it; never add a second copy. Then go to Program Catalog → PowerViz → Check.

1. **Menu:**
   - Run POWERVIZ. Five items should appear, with "Two Means, unequal σ & n (z)" on one line.
   - Pick it, then OK the seven-field form. If the form doesn't fit on one screen, check that it scrolls and that all seven fields can be reached.
2. **Main view at the defaults:**
   - The title should read "PowerViz 2 Means, σ₁≠σ₂ (z) 1-sided".
   - The panel should show "n = 40/20", "μ₂ = 105", "d = 0.32, small", POWER 0.277, "β = 0.723", "SE₀ = √(10²/40+20²/20) = 4.74" and "n₈₀ = 223/112 (222.6)".
   - The ≠ and ² glyphs should render.
3. **Up, Up, Down:** n should read 45/23, 50/25, 45/23. Hold Up: n₂ should keep pace.
4. **Tap "n =":**
   - Type 30 and 45: n should read 30/45.
   - Then Edit, with n grp1 2 and n grp2 100: one box should say n₂ was set to 20.
5. **Edit, then OK without changing anything:** n must not change.
6. **Drags:**
   - Drag H₁ sideways: μ₂ should move in whole steps and the power should change.
   - Drag up on the plot: n₁ should rise, with the hint "drag up = larger n₁ (n₂ follows)".
7. **Pow-n:**
   - The axis should read "n₁ (n₂ = 0.5 × n₁)", with a green "n₈₀ = 223/112".
   - Touch the curve and lift: n should take that n₁ and its n₂.
8. **Menu → Sample-size formula:**
   - The badge should say "exact (CAS)", and the CAS line for n₁ should show σ₁, σ₂ and k (not pvs, pvt, pvk).
   - The numbers line should read "n₁ = 2×(3×√2×zα+3×√2×zβ)^2", followed by "Round UP: n₁ = 223, n₂ = 112" and the best-split line.
   - **Write down the CAS line exactly.** The Prime's Giac may print it differently from desktop Giac.
9. **Help:** page 4/4 should be readable, with Cohen's warning in orange and nothing running off the right edge.
10. **Tests 1–4:** test 2 should still open with its old values, and test 1's formula page should still show "exact (CAS)".
11. **Tiny α:** in test 1, Edit with α = 1E-13 (typed with EEX). The panel should show zcrit = 7.349. v2.5f's `NORMALD_ICDF(0,1,1)` was ∞.
12. **Esc:** the exit box should show "n₁ = 40, n₂ = 20". Then type EP_NPG in Home: it should be 40.

## Unresolved

- The new test is a z test, like the other four. Welch's t test (estimated σs, Satterthwaite df) would need the noncentral t, which the Prime does not have built in; help page 4 says so in plain words. A Welch page could follow if wanted.
- How the Prime's own CAS prints the test-5 solve (checklist item 8).
- No independent review reported in full (see Verification). If one is wanted before the device run, it can be run again.
