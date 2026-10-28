# SeizureLab beta 1: second review (independent)

21 Oct 2026. Reviewer 2 did not write the program and did not edit `SeizureLab_beta1.txt`.

**Read in full first:**
- `ref/HP_Prime_Lessons_Learned_v7n.md`
- `BRIEF_NEW6_v1.md`
- all 2,559 lines of the program
- the builder's NOTES, gate output and verify output

**Where the checks are.** My scripts are in `/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad/rev2_sz/`:

| Script | What it checks |
|---|---|
| `ref_stats.py` | Exact-fraction references |
| `chk_numerics.py` | The PPL routines in harness v3e against those references |
| `enfsi_cmp.py` | The program against the published tables |
| `prime12.py` | A 12-digit decimal emulation of the Prime |
| `fpc_sim.py` | The FPC simulation |
| `bay_extreme.py`, `bay_search.py`, `timing*.py` | The Bayesian searches and their speed |
| `layout.py` | Text widths at extreme inputs |
| `oc_chk.py` | The OC curve |

**Source checked.** The ENFSI DWG guideline as UNODC published it: *Guidelines on Representative Drug Sampling*, ST/NAR/38, 2009, https://www.unodc.org/documents/scientific/Drug_Sampling.pdf (54 pages, read as text).

**Overall.** No formula is wrong, and every least n, bound and probability I recomputed agrees with exact arithmetic. 426 of the 427 ENFSI table cells I compared agree; the one that differs is ENFSI's error, not the program's (item 12).

The serious problems are elsewhere:
- G1 run time on inputs the form accepts (item 1).
- The weight FPC: D1 is confirmed, the factor should be (N − n)/N (item 2).
- How the Bayesian page relates to ENFSI's own tables (item 3).
- A tie tolerance too tight for the Prime's 12 digits (item 4).

---

## Findings, most serious first

### 1. A long, uninterruptible computation is reachable from the Set up form — CONFIRMED (harness timings; the G1 factor comes from the brief)

**Where.**
- `sz_BayMin`, lines 849–870, and `sz_BayMinL`, lines 873–892.
- Called from `sz_Recalc` (953–954, on every Set up and every N × 10 or N / 10), `sz_PrNext` (1528–1529) and `sz_TabCalc` (2211–2218).

**What is wrong.** Both searches start at the large-N guess `ceil(ln(1−c)/ln p0 − a)` and then step ONE n at a time until the answer is reached. Each step is a full beta-binomial sum, or an incomplete beta continued fraction of up to 300 terms.
- **Far from the guess.** When the answer is far from the guess (a strong prior, or p0 and c near 1 at large N), the number of steps grows into the thousands or more.
- **No way out.** None of these loops checks Esc.
- **Wrong reassurance.** The busy box says "(a few seconds on a G1 for large N)" (line 451).

**Measured in harness v3e.** The brief puts a G1 at 30 to 100 times slower than this.

| Inputs (all accepted by Set up) | Call | Steps | Harness | G1 estimate |
|---|---|---|---|---|
| defaults, N = 10000, Jeffreys | `sz_Recalc` | few | 0.51 s | 15–50 s |
| N = 10000, prior Beta(1, 10) | `sz_BayMin` | 116 | 7.4 s | 4–12 min |
| N = 10000, prior Beta(1, 100) | `sz_BayMin` | ~930 | 24 s | 12–40 min |
| N = 10000, c = 0.9999, p0 = 0.999, uniform | `sz_BayMin` | 3,537 | 6.1 s | 3–10 min |
| c = 0.9999, p0 = 0.999, prior (0.1, 100) | `sz_BayMinL` | 132,204 | 334 s | hours |
| Tables page, prior Beta(1, 10) | `sz_TabCalc` | | 2.1 s | 1–3.5 min |

**Failure scenario.** A student types a sceptical prior b = 10 at N = 10000. Roger's G1 then shows "Computing ... (a few seconds ...)" for several minutes, and Esc does nothing.

**Fix.**
1. **Bisection instead of stepping.** P(claim | n all positive) is monotone in n. I checked it on:
   - 1,500 random cases with typed priors from 0.1 to 100 and N up to 1000, with 0 non-monotone;
   - uniform and Jeffreys at N = 10000.

   So replace both stepped searches with doubling followed by bisection, as `sz_BinMin` already does. That costs at most about 2·log₂(N), roughly 30 evaluations; `sz_BayMinL` needs about 40 with doubling.
2. **Let Esc stop it.** Poll `GETKEY == 4` inside `sz_TabCalc`'s loop and inside the searches. Return −1 so the page prints "stopped".
3. **Say the truth.** Change the busy line, or warn at Set up when b > a·10 or c > 0.999 that it may take minutes.

All the values themselves are right: 5668, 5046, 9746, 323, 957, 142 and 505 agree with a SciPy scan.

### 2. DECISION D1: the finite-population factor should be √((N − n)/N) — CONFIRMED (theory, simulation and ENFSI)

**Where.**
- The calculation: `sz_WtCalc`, line 1963.
- The text: the page at 2042, help page 5 at 2494, and the header at 158–165.

**The builder's argument is right.** Under simple random sampling without replacement, Var(x̄) = (1 − n/N)·S²/n, where S² is the population variance with divisor N − 1 (Cochran). E[s²] = S² for the sample variance with divisor n − 1. So N²·s²/n·(N − n)/N is unbiased for Var(T). The program's (N − n)/(N − 1) overstates it by exactly N/(N − 1).

**Simulation** (`fpc_sim.py`): a fixed gamma-shaped population of weights, 200,000 samples per row. E[estimate]/Var(T) for each factor:

| N | n | (N−n)/N | (N−n)/(N−1) |
|---|---|---|---|
| 10 | 4 | 1.0000 | 1.1111 |
| 10 | 8 | 0.9997 | 1.1108 |
| 20 | 5 | 0.9989 | 1.0515 |
| 100 | 10 | 1.0002 | 1.0103 |
| 100 | 50 | 1.0001 | 1.0102 |
| 30 | 25 | 0.9998 | 1.0343 |

Coverage of the 95% t interval differs by at most 0.3 percentage points, because the t interval for a skewed small sample dominates the error.

**ENFSI agrees.** §7 (pp. 34–35) uses the correction √((N − n)/N). Its worked example (N = 100, n = 23, x̄ = 0.265 g, s = 0.023 g) prints the factor as 0.877, which is √(77/100) = 0.8775; √(77/99) would be 0.8819.

**Failure scenario.** A student types ENFSI's example on the weight page (Type: n = 23, mean 0.265, SD 0.023).
- The program gives a half-width of **0.877 g**; ENFSI prints **0.873 g** (26.500 ± 0.873).
- The page and the guideline disagree in the third digit, and the student cannot tell which is wrong.

**Fix.**
1. In line 1963, change `(szN - szWn) / (szN - 1)` to `(szN - szWn) / szN`.
2. Change "(N - 1)" to "N" at lines 2042 and 2494, and in the header (160–165).
3. Update the verify script.

The illustrative example then reads: SE 0.3134 g (was 0.3150), bound ≥ 49.96 g (was 49.95), FPC 0.9487 (was 0.9535).

**Optional additions.**
- ENFSI's Pcorr (n − r)/n with t on n − r − 1 df, for when r tested units were negative. The page's total is the weight of all N units, not of the drug-positive ones; say so on the page.
- ENFSI's RSD < 10% acceptance rule.

### 3. The Bayesian page's headline contradicts ENFSI's table and worked example — CONFIRMED (read ENFSI pp. 20–24)

**Where.**
- The page: lines 1463–1471, and line 1469 in particular.
- The header: 133–148, which attributes the finite-N beta-binomial at every N to "Aitken 1999; ENFSI 2009".
- Help page 2: lines 2450–2457.

**What is wrong.** At the defaults the page says "Least n, all +, for P ≥ 0.95: 22 (N → ∞: 28)", against a hypergeometric 23.

ENFSI tabulates the Bayesian answer from the *large-seizure* beta posterior P(θ > k), which does not depend on N. Its Table 4 note reads "A large seizure is assumed (N ≥ 50)". It uses the beta-binomial only for seizures under 50 units, and prints no table for it.
- ENFSI Table 4 (a = b = 1, 95%, k = 0.9, 0 negatives) = **28**, which equals the program's "N → ∞" value.
- ENFSI's Example 1 says the Bayesian approach needs 28, *more* than the hypergeometric 23.

The program's headline says the opposite (22 < 23). The arithmetic is right: the finite-N beta-binomial does give 22 (checked exactly). But a student holding the guideline is told the reverse of what the cited source says, and nothing on screen explains why.

**Fix.** Keep both numbers, and add one line on the page or help page 2. For example: "ENFSI tabulates the N → ∞ value for N ≥ 50 (28 here); the beta-binomial (22) counts the untested units of THIS seizure." Change the header's attribution to match.

**Checked equal to ENFSI Table 4** (the program's `sz_BayMinL`):
- all 18 cells, at 95% and 99%, k = 0.5, 0.7 and 0.9, for (a, b) = (1, 1), (3, 1) and (0.5, 0.5);
- the in-text a = 10, b = 1 → 19.

### 4. The tie tolerance 1E−9 is tighter than the Prime's own error — CONFIRMED in a 12-digit emulation, PLAUSIBLE on the device

**Where.** `sz_Le` and `sz_Ge`, lines 742–758, and the claim in the comment at 745–747.

**Direction.** Counting an exact tie as met matches exact arithmetic, and on the PC (binary doubles) 1E−9 is ample.

**The problem on the Prime.** Every tail is anchored by EXP of a difference of large ln-gammas.
- **ln Γ itself is fine.** I emulated the program's ln Γ, with its coefficients stored to 12 digits, at 12 significant decimal digits per operation. Absolute error was ≤ 4E−11 for z ≤ 10, 8E−10 at z = 1000 and 1.4E−8 at z = 10001: good enough for every displayed number.
- **The difference is not.** The difference of several such values costs relative accuracy in P:

| N | worst relative error of the hypergeometric tail (`sz_HypS`, emulated, 25 random cases) |
|---|---|
| 50 | 1.3E−9 |
| 200 | 9.4E−9 |
| 1000 | 3.1E−8 |
| 3000 | 2.3E−7 |
| 10000 | 1.9E−7 |

**Failure scenario** (an exact tie at large N). N = 5000, p0 = 0.0501, so Kr = 251 and K0 = 250; c = 0.95.
- At n = 1, P(X ≥ 1 | K0) = 250/5000 = 0.05 = 1 − c exactly.
- The emulation gives 0.0500000046777. `sz_Le` says "not supported", so the least n is 2 where exact arithmetic gives 1.
- The same tie at N = 100, 1000, 2000 and 10000 happened to round downwards.

The default tie in checklist item 10 (N = 10) is safe: the error there is 1E−10.

**Fix.** Use a relative tolerance of 1E−6. That is still invisible at the 4 decimals the pages show. Correct the comment and say the trade-off in it: a P up to 1E−6 (relative) above 1 − c also counts as met.

### 5. The OC drag loops have no key exit and no phantom-touch guard — PLAUSIBLE

**Where.** The n-knob loop at 1885–1900 and the θ loop at 1907–1913.

**What is wrong.**
- Both loops run until `SIZE(MOUSE(1)) == 0`. Neither exits on a key, and neither rejects off-screen coordinates.
- The θ loop also calls the full `sz_OCDraw(0)` on every pass, even when the finger has not moved.

Lessons §7 caps the finger-lift drain for exactly this hazard: a stuck reading, like PrimeSUD's phantom (2147483647, 0). The fleet's drag loops guard against it (ScatterLab `slDragPt`, lines 1146–1190).

**Failure scenario.** A stuck touch on the OC page. The knob loop clamps x to 300 and spins for ever (n jumps to the slider's top). The θ loop redraws for ever. Only a reset gets out.

**Fix.** Copy ScatterLab's three guards:
- read `GETKEY` in the loop and stop on any key;
- stop when x is outside 0..319 or y outside 0..239;
- redraw only when the value changed.

### 6. The red "outline" on the observed bar is a solid red block — CONFIRMED (HP forum)

**Where.** Line 1094: `RECT_P(G1, hdX1, ..., hdX2, szPB - 1, szRED)`.

**What is wrong.** With one colour, RECT_P fills with that colour. The HP Museum forum thread "RECT_P but without filling" (https://hpmuseum.org/forum/post-46546.html) reports this, and HP's Tim Wessman gives a transparent fill as the way to draw an outline. The harness only records the call, so it cannot see the difference.

The bar at x, which belongs to the magenta tail P(X ≥ x), is therefore painted solid red. That contradicts the legend "magenta = P(X ≥ x)", the comment at 1037, and the NOTES checklist item 3 ("the 23 bar magenta with a red outline").

**Fix.** Draw four `LINE_P` edges in red, which is verified. Do not use the RGB-alpha transparent fill: it is not on the fleet's verified list.

### 7. Two glyphs not on the brief's verified list — CONFIRMED (they are present); rendering untested

**Where.**
- `CHAR(8592)` (←): lines 1114, 2253 and 2507.
- `CHAR(8645)` (⇅): line 2508.

**The conflict.** Lessons §13 says both arrow sets "render; Roger to pick one". The v7n §5 symbol list and the brief's allowed list do not include either.

**Fix.** Use words, which are shorter than adding to the device checklist:
- footer at 1114: "+/- = n, arrows = x, tap = read, Ent = menu";
- footer at 2253: "arrows = table or plot, Ent = menu, Esc = back";
- help at 2507–2508: "Left/Right = x (OC: θ; binomial: N / 10, N × 10)" and "Up/Down = negatives allowed (OC, binomial)".

→ (8594) on its own is verified, if an arrow is wanted.

### 8. Lines longer than the program's own budget, and one clipped line with a grammar slip — CONFIRMED for one line; PLAUSIBLE for the rest

**The budget.** The header (189–190) sets font 1 at about 6.5 px per character, so at most 46 characters in width 308; help pages are 296 px wide, so about 45. The harness assumes 5.5 px and so passes lines the header's own rule rejects.

**CONFIRMED.**
- Line 2249 with a typed prior prints "Bayes with the your own prior Beta(0.25, 0.75); ∞ = the limit". It is 61 characters, so it is clipped even at the harness's 5.5 px, and "the your own prior" is ungrammatical.
- Fix: "Bayes: prior Beta(a, b), " + name; put the "∞ = the limit" text on its own line.

**PLAUSIBLE** (over 46 characters at the defaults):
- the binomial page at 1247: "n = 23, x = 23: hyper P = 0.0472, binom P = 0.0886" (50 characters);
- line 1252: "Binomial asks for 10 more (1 neg): the safe side" (48);
- the OC title in font 2 at 1709: 45 characters at the defaults and 48 at N = 9999 with d = 17;
- 24 help lines of 46–49 characters in width 296, e.g. "Home: SZ_N SZ_NMIN SZ_P SZ_LB SZ_PB SZ_TOT SZ_TLB" (49).

**Fix.** Shorten them, or have the device check confirm the real width of font 1 first.

### 9. Key help that does not match the keys — CONFIRMED

**What is wrong.**
- **The binomial page.** Left/Right are N / 10 and N × 10, and Up/Down are the negatives allowed (1390–1393). Its footer (1305) shows only a colour legend, and help page 6 (2507) says "← → = x" for every page.
- **The hypergeometric page.** Up/Down change n by 10 (1198–1199); this is documented nowhere on screen.
- **The OC page.** It never shows a key legend: `sz_Show("")` is called with `szInfo` always set (1782–1788). So "+/- = n, Left/Right = θ, Up/Down = negatives" appears nowhere on it.

**Fix.**
- Give each page its own key footer (the canonical form in Lessons §13).
- Put the OC page's worst-case line at y 180 and its keys at y 192.

### 10. The Set up form clamps two fields silently — CONFIRMED

**What is wrong.** The negatives allowed are clamped to 0..20, and the prior a and b to [0.1, 100] (1002–1003), with no message.
- The comment at 966–967 promises a message that says why.
- The NOTES say a and b are pulled in "each with a message".

Typing a = 200 silently gives 100.

**Fix.** Add the two clauses to `suMsg`.

### 11. Sources: a cited method paper has a published correction, and none of the papers was read — PLAUSIBLE

**What I could check.** The header and help page 6 cite Coulson et al. (2001), Tzidony & Ravreby (1992) and Frank et al. (1991) as sources of methods. Their volumes and pages match ENFSI's reference list.

**The correction.** That same list carries "Stoel and Bolck, A correction to Tzidony and Ravreby (1992)". Lessons rule 16 says to check the correction too, and the builder had no access to any of these papers.

**Fix.**
- Cite ENFSI 2009 §7 (now read) and Cochran for the weight interval.
- Mark Coulson, Tzidony & Ravreby and Frank as "not checked against the sources" on help page 6, or drop the ones the program does not implement. Frank et al.'s multi-container method is not implemented.

### 12. Information for the NOTES: one ENFSI table cell is wrong, and the program is right

ENFSI Table 2 (p. 14), N = 90, 99%, k = 0.7, 2 negatives, prints **21**. The program gives **22**.

Exact arithmetic: K0 = 62, and P(X ≥ 19 | N = 90, K0 = 62, n = 21) = 0.011150, which is above 0.01; at n = 22 it is 0.007561. So 22 is the least n. The neighbouring cells (N = 80: 21; N = 100: 22) agree with the program.

Record this in the NOTES and the device checklist, so that nobody "fixes" the program to match the table.

### 13. Small style points

- **Palette.** `szWRNG` #FFBEBE (line 268) is not a house colour. The house light red is 255,235,235; the darker shade is defensible for "wrongly supported", but say so in the comment.
- **Footers.** Most page footers omit "Esc = back"; the canonical footer ends with Esc.
- **Wording.** "95% lower bound: K ≥ 90 of 100" (1057) would read better as "95% lower confidence bound".

---

## What I checked and found correct

**(a) The claim and the test.**
- Kr = ⌈p0·N⌉ and K0 = Kr − 1, with p0·N rounded to 6 decimals.
- 12 boundary cases against exact fractions, among them N = 100 / p0 = 0.07, N = 15 / 0.9, N = 10 / 0.95 and N = 49 / 0.7.
- The screen says "at least" ("Claim: K ≥ 90 of 100", "'90%' of 100 units means at least 90"). That is ENFSI's H0: N1 < K, tested at K − 1 (pp. 16–17). When p0·N is whole (N = 100, p0 = 0.90), K = 90 counts as true and K0 = 89 is the worst false case, as ENFSI has it.

**(b) The least-n searches.**
- **Hypergeometric.** 700 grid cases against an exact-fraction brute force (N = 61..74, 5, 8, 11, 17, 33, 99, 101, 137; c from 0.8 to 0.99; six values of p0; d = 0, 1, 2, 3, 5): 0 mismatches.
- **Binomial.** 60 cases, exact: 0 mismatches.
- **Bayesian, finite N.** 300 cases against a SciPy scan, including N = 1000 and 0.99/0.99: 0 mismatches.
- **Bayesian, limit.** 24 cases against `beta.sf`: 0 mismatches.

**(c) The lower confidence bound.** 250 exact cases: 0 mismatches. In every case the bound agrees with the test: "supported" holds exactly when Kr ≤ K_L (750 checks).

**(d) The Bayesian posterior.** P(x + Y ≥ Kr), with Y ~ BetaBin(N − n, a + x, b + n − x), against exact rational sums for priors (1, 1), (1/2, 1/2) and (2, 3/2). 150 cases; worst relative error 4.8E−13.

**(e) The OC curve.** P(X ≥ n − d | N, n, ⌊θN⌋) and the binomial OC were checked at all 282 columns for 7 states (N from 5 to 10000, zoomed and unzoomed, d up to 5). 3,948 values; worst absolute error 6E−6.
- The only miss was column 71 at N = 1000 zoomed. There θN is 774.9999999999999 in binary, so `FLOOR` gives 774. That is a PC artefact; the Prime's decimals give 775.
- The ratio recursions, the K ≥ n closed start and the e^−700 cut-off bound all check.

**ENFSI tables against the program.**

| ENFSI table | Cells compared | Mismatches |
|---|---|---|
| Table 1 (21 values of N × 6 columns) | 126 | 0 |
| Table 2 | 252 | 1, the misprint in item 12 |
| Table 3 (binomial) | 18 | 0 |
| Table 4 (Bayesian, three priors) | 18 | 0 |
| a = 10, b = 1 example | 1 | 0 |
| Table 5 | 12 | 0 |

The defaults reproduce the guideline: hypergeometric 23 (Table 1), 36 and 46 with 1 and 2 negatives (Table 2), binomial 29 / 46 / 61 (Table 3), and Bayesian limit 28 (uniform) and 18 (Jeffreys) (Table 4).

**Device rules.**
- **Source.** Pure ASCII and LF. At most 6 names on a LOCAL line, every LOCAL at the head of its block. No `//` inside an open bracket (my own bracket scan).
- **Names.** No identifier clashes with `HP_Prime_Builtin_Names.txt` ignoring case, and there are no one-letter lowercase names.
- **No list arithmetic** anywhere: every list is read and written by index, or passed to MAX, SIZE or MAKELIST.
- **Keys and touch.** Only the verified GETKEY codes. Soft keys read with y ≥ 218, `MIN(6, IP(x/53.4)+1)`. Every pause drains keys, then waits, then drains again. Finger-lift drains are capped by TICKS.
- **Menus and output.** CHOOSE indices initialised to 0 and tested. The program ends with `RETURN`. Every number goes through `STRING(ROUND(x,d),2,d)`, and the harness shows no scientific strings at N = 10000, 9999 and 100.
- **Arithmetic safety.**
  - t quantiles are formed as −STUDENT_ICDF of a lower tail, with c clamped to [0.5, 0.9999] (no ICDF at 0 or 1).
  - There are no alternating sums. Every tail is built from positive terms by neighbour ratios from the mode.
  - The incomplete beta uses NR's continued fraction, with the 1 − mirror form only above the mean.
  - Densities cannot overflow, and logs below −1100 return 0.
- **ln-gamma accuracy** is adequate for the display (item 4 has the numbers). Only the tie tolerance is affected.

**Teaching wording.**
- The frequentist reading is stated correctly, on help page 1 and on the page: "rare if the claim were just false", "a statement about the PROCEDURE".
- The Bayesian reading is a statement about this seizure, given a prior, and the program says which prior it used.
- Help page 4 states the random-selection assumption, and lists homogeneity, perfect tests and a correct count of N.
- The one-line disclaimer is on every result page: hypergeometric, binomial, Bayesian, OC, weight, table and plot. The full DISCLAIMER is on the opening page.
- The papers are cited only "for the METHOD"; item 11 has the caveats.

**House style.**
- The header matches the brief: licence, DISCLAIMER, AI credit, sources, data, the reworked TI programs, and a file map whose ranges match the section banners.
- Routines carry the `sz_` tag and exports the `SZ_` tag.
- Every colour except `szWRNG` is from the house palette.
