# RankLab beta 1: second review (independent)

*Reviewer 2, 21 Oct 2026. I did not write RankLab and did not use `rk_ref.py` or the builder's verify script for expected values. My scripts are in `/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad/rv2rank/` (`mystats.py` has my own reference code; `t_*.py` are the runs). `RankLab_beta1.txt` was not edited.*

**Verdict:** no wrong formula, no runtime error, no list arithmetic, and no 12-digit precision problem. All six presets give the published or SciPy numbers on screen. The findings below concern small-sample inference, one summary bug, honest wording, and Esc/progress behaviour on the G1.

---

## Findings, most serious first

### 1. Spearman (and Kendall) p at small n: wrong verdicts, and "p < 0.0001" for 3 points. CONFIRMED
**Lines:** 1289-1291 (t), 1308-1316 (`rk_CorrP`: |rs| = 1 gives p = 0), 1250-1255 (Kendall z), 1976-1990 (Result page).

**What is wrong:** every Spearman p comes from t = rs √((n−2)/(1−rs²)) on n−2 df. Every Kendall p comes from the normal z. Nothing is exact and nothing warns, even at n = 3. SciPy does the same, so the builder's SciPy agreement could not catch it.

**Failure scenarios (harness, Use my data → Correlation):**
- **D1 = 1,2,3 and D2 = 2,4,9.** The page shows "a perfect rank correlation: p < 0.0001" and "p < 0.05: evidence against H₀". The exact permutation p is 2/3! = 0.333. On the same page Kendall shows p = 0.1172.
- **D1 = 1..5 and D2 = 1,2,3,5,4.** The page shows rs = 0.900, "p = 0.0374" and "evidence against H₀". The exact permutation p is 0.0833, so the verdict flips. Kendall shows p = 0.0500; its exact p is 0.0833.
- **Other n:** n = 4, rs = 0.8 gives t-approx 0.200 against exact 0.333. n = 6 gives 0.019 against 0.033.

**Fix:**
- **Perfect correlation, no ties:** exact p = 1/n! one-sided and 2/n! two-sided, since only one ordering reaches |rs| = 1.
- **Kendall with no ties:** the exact null is the Mahonian (inversion) distribution, Π(1 − q^i)/(1 − q). That is the Gaussian-binomial machinery `rk_MWNull` already has, about n³/6 steps, so it is cheap for n ≤ 50. Use it as the "exact" p and keep z as "normal", like the other tests.
- **Spearman:** an exact permutation p for n ≤ 7, which is 5,040 orderings. Otherwise add a grey line "t approximation: rough for n < 10" and base the verdict on the exact Kendall p when one exists.

### 2. The Quit summary reports the previous test's numbers under the new test's name. CONFIRMED
**Lines:** 3015-3031 (`rk_Open` sets `rkTest := opT` before `rk_Compute` can refuse), 3207-3222 (`rk_Summary` reads `rkTest` but the old fields).

**Failure scenarios:**
- **Wilcoxon, then a refused Groups test.** Run Wilcoxon (Darwin), Esc, then Use my data → Groups with D1 = 2,2 and D2 = 2,2,2 (refused: all equal), then Quit. Home gets "RankLab: Mann-Whitney U, n = 15, U₁ = 96, exact p = 0.0413 (two-sided)". Those are the signed-rank numbers.
- **Correlation, then a refused Paired test.** Run correlation (draft), then Paired with all d = 0, then Quit. Home gets "Wilcoxon signed-rank, n = 366, T+ = -0.2257, normal p < 0.0001".

**Fix:** keep the test number of the last successful run (`rkLastT := rkTest` when `rk_Compute() == 1`) and restore `rkTest` from it when a compute is refused. Alternatively, build the summary string at the end of every successful `rk_Compute` and return that string.

### 3. The USJudgeRatings Friedman design is not described honestly. CONFIRMED (text)
**Lines:** 1491-1497, 1515 (`rkFLab := "11 criteria (raters) rank 8 judges"`), 3135 (help), 1970 ("Assumes independent blocks"), header 108-111.

**What is wrong:**
- **The blocks are not raters.** Each value is the mean rating that many lawyers gave a judge on one criterion, and the same lawyers rated every criterion.
- **The blocks are not independent.** The 11 criteria are strongly intercorrelated (a halo effect: the judges' ranks agree almost perfectly across criteria, W = 0.94).
- **The p-value is not valid inference.** The page prints "Assumes independent blocks" and then a p below 0.0001 for data that break that assumption. A student will read the p as strong evidence.

**Fix:**
- Relabel the preset as "11 rating criteria (blocks) order 8 judges; each value = lawyers' mean rating".
- On the preset's Result page, add "Blocks are not independent (same lawyers, every criterion): read W as agreement among criteria; the p is illustrative only".
- In help page 5, change "11 criteria rank 8 judges" in the same way.
- Optionally mention that MockJury's KW ignores the Crime factor (burglary/swindle).

### 4. "Esc = stop" is printed where Esc is never read, and there is no way out of the long non-DP loops. CONFIRMED (code); G1 times PLAUSIBLE
**Lines:**
- 434: `rk_Prog`'s fixed text "Esc = stop (the normal approximation stays)".
- Shown but not polled at 1366 (ranking), 1057 (KW summaries), 1218-1220 (Kendall merge sort) and 915-917 (MW exact null).
- Only `rk_SRNull` (822) polls GETKEY.

**How long these run:** interpreted-statement counts in the harness, scaled by GaltonBoard's G1 ×100 key (about 3,300 statements in about 0.5 s on the G1):

| Path | Statements | Estimated G1 time |
| --- | --- | --- |
| Draft day-vs-number (Kendall, 366) | ≈ 69,000 | ≈ 10-20 s |
| Rossi Mann-Whitney (ranking 432) | ≈ 35,000 | ≈ 5-10 s |
| Draft Kruskal-Wallis | ≈ 28,000 | ≈ 4-8 s |
| Signed-rank, n = 50 with ties | ≈ 196,000 | ≈ 30-60 s (has Esc) |

Each Left/Right on the 366-dot KW box page redraws about 4,000 statements, about 1 s per key on the G1.

**Failure scenario:** a student presses Esc on the Kendall bar, nothing happens for 10-20 s, and they press it again. The extra Esc is then drained harmlessly, so this is not a hang, but the screen's promise is false.

**Fix:**
- Poll `GETKEY == 4` once per merge pass (Kendall), every ~50 values (ranking) and once per stage (MW). On Esc, return 0 with "stopped by Esc".
- Or give `rk_Prog` a text argument so it says "Esc = stop" only where it works.

### 5. Chi-square approximations at tiny sizes have no caution, and Friedman accepts b = 1. CONFIRMED
**Lines:** 1051/1142 (χ² p), 1115 (`frB < 1` is the only guard).

**Failure scenarios:**
- **KW with groups of 1, 1 and 2** prints "χ² approximation: p = 0.8607" with no warning that the approximation needs about 5 per group.
- **Friedman with one block** (D1 = 1, D2 = 3, D3 = 2) prints "Kendall's W = 1.000 (… 1 = full)", Q = 2 and p = 0.3679. Concordance among one block is meaningless.

**Fix:**
- Refuse Friedman with b < 2.
- Add a grey line when any nᵢ < 5 (KW) or when b is small: "χ² approximation rough here".

### 6. CHAR(179), a superscript three, is unverified and outside the brief. CONFIRMED
**Line:** 1958, `"Ties within blocks: sum(t" + CHAR(179) + " - t) = "`.

**What is wrong:** the brief says not to use "other superscripts", and Lessons §5 says only ² has been checked.

**Fix:** write `"sum(t^3 - t)"`, as the help pages already do in ASCII.

### 7. The "Mean Spearman rs between blocks" is not a mean Spearman when there are ties. CONFIRMED
**Lines:** 1145, 1963.

**Failure scenario:** with b = 3, k = 2 and a fully tied block (D1 = 1,2,5; D2 = 1,3,4), the page shows "Mean Spearman rs between blocks = -0.500". The tied block's Spearman correlations are undefined.

**Fix:** show the value only when `rkTieS == 0`; otherwise write "≈" and add "(exact only without ties)". The judges preset (36 tie units) gives 0.933 against a true pairwise mean of 0.9333, so it is fine there.

### 8. Some lines exceed their TEXTOUT_P width at the house 6.5 px a character. PLAUSIBLE (device check)
**What is wrong:** these lines are 1-8 px over their width argument (304 or 300):
- "Mean of U = 18126, SD = 1123.74 (tie-corrected)" (1927);
- "Exact p: none with ties (normal, tie-corrected)" (1862);
- "n = 366 pairs: x = day of year, y = draft number" (1973);
- "Kendall's W = 0.939 (0 = no agreement, 1 = full)" (1961);
- "(the verdict is for the Spearman p, in magenta)" (1991);
- "k = 3 groups, N = 114, df = 2;  ties: 11 groups" (1944);
- the help footer "Page n/7: any key = next, ← = back, Esc = leave" (3052);
- the Dunn row "Beautifu v Unattrac" in its 120 px field (2312-2313).

The harness's own estimate says nothing is clipped, and the Prime's font-1 glyphs are probably narrower than 6.5 px.

**Fix:** look at these on the G1. If any is cut, shorten it ("SD = 1123.74, tie-corr.", "Exact p: none (ties): normal").

### 9. Small wording and style items. CONFIRMED
- **"ties: 1 groups"** (1925, 1944, 1974; seen with MW 2 vs 1): plural for one group. Use `IFTE(rkTieN == 1, " group", " groups")`.
- **"(two-sided, ties)"** after Kendall's p even when there are no ties (1987).
- **Unexplained abbreviation:** "(ties, cc)" (1911). Write "(ties, cont. corr.)".
- **INPUT in ASCII:** the label is "m0 = " and the help is "H0: …" (1637). The source line also says "m0" (1641). v7n wants m₀ and H₀ (CHAR(8320)), and a label built from a variable is device-verified.
- **Hodges-Lehmann has no wording:** "Hodges-Lehmann estimate = 3.125" (1914) does not say what it estimates. Suggest "HL estimate of the median d = 3.125 (inches)".
- **Unclear H₀:** the Friedman H₀ "within a block every order is alike" (1968). Suggest "within each block, every ordering of the treatments equally likely".
- **Colours:**
  - Group colour 2 (and d < 0 on the strip) is the same magenta as the p-tail colour on the Null page.
  - `rkLMAG` #F0B4F0 is not in the house palette (the shade is RGB(170,205,255)).
  - Both are cosmetic; consider a non-magenta second group colour.
- **Null page mismatch:** for a sign test with n > 1,500, the bars are skipped and the Null page draws the normal curve while slot 4 still reads "Exact". This is an edge case.

---

## Checked and found correct

- **List arithmetic (the harness's old `+` = concatenation):**
  - None in the program.
  - A static scan of all ~100 list-valued names and parameters next to `+ - * / ^` or a comparison found nothing.
  - Every interpreter arithmetic call with a list operand was logged across about 25 full menu runs and 4,259 routine calls: 0.
  - Every append uses `CONCAT(…, {x})`.
- **Presets:** Rossi (114/318, in file order), the draft lottery (vcdExtra = Triola JSON; months), Darwin (cross/self), the judges (first 8 judges, INTG..RTEN) and MockJury (39/38/37) all equal their CSV/JSON files exactly.
- **Numbers on screen** for every preset, against my own SciPy and brute-force values:

  | Preset | Values that match |
  | --- | --- |
  | Darwin | T+ 96, exact p 0.0413 / lower 0.9823 / upper 0.0206, normal p 0.0438 / upper 0.0219, r +0.600, HL 3.125; sign test exact p 0.0074, z +2.582 |
  | Rossi | R₁ 28174.5, U₁ 21619.5, SD 1123.74, z +3.108, p 0.0019 (lower 0.9991, upper 0.0009), r +0.193, PS 0.596 |
  | Draft KW | H 25.953, p 0.0066, ε² 0.071, every mean rank, Dunn Mar v Dec z +3.88 (Holm 0.0069), 1 of 66 pairs |
  | Draft correlation | rs −0.2257, tau-b −0.1489, z −4.251 |
  | Judges | Q 72.326, C 0.9935, W 0.939, mean Spearman 0.933 |
  | MockJury | H 2.876, C 0.9811, p 0.2374, the three Dunn/Holm pairs; MW Beautiful v Unattractive U₁ 592.5, z −1.347, p 0.1779, HL −1 |

- **4,259 random cross-checks, 0 failures** (`t_random.py`):
  - signed-rank exact p, all three tails, against brute enumeration of all 2^n sign patterns, with ties and zeros, n ≤ 14;
  - the signed-rank normal p against my own tie-corrected formula;
  - Walsh HL;
  - the sign test against `binomtest`;
  - MW asymptotic (3 tails) and exact (no ties) against `mannwhitneyu`, and HL;
  - KW against `kruskal`;
  - Dunn z and p, and Holm, from my own code;
  - Friedman from my own formula and `friedmanchisquare`;
  - Spearman against `spearmanr`;
  - tau-b against an O(n²) brute count;
  - Kendall p against `kendalltau(method='asymptotic')`.
- **12-digit precision** (Decimal at 12 digits):
  - The signed-rank DP and its tails are sums of non-negative counts divided by 2^n. Over 60 cases at n = 30-50 the worst relative error is 8.4E−11, so counts above 10¹² do not matter.
  - The MW Gaussian-binomial DP, which does subtract, is exact in 12 digits for every m n ≤ 400 (largest intermediate 1.47E9; C(40, 20) = 1.378E11).
  - There is no ICDF anywhere. Every upper tail is a lower tail (`NORMALD_CDF(0,1,−z)`, `STUDENT_CDF(df,−t)`, `BINOMIAL_CDF(n, ½, n − s)`, upper count sums), and `rk_ChiUp` is a sum of positive terms. No power can overflow.
- **Awkward data** (all ties, zeros, small groups, empty or equal groups): no runtime error, and the refusals are right.
  - All |d| tied with mixed signs: exact p 0.6875 = brute.
  - Zeros in the paired d: 2 dropped, exact p 0.25 = brute.
  - Mann-Whitney: 1 vs 1 gives exact p = 1; 2 vs 1 with a tie goes to the normal approximation.
  - Kruskal-Wallis with groups of 1, 1 and 2 runs.
  - D2 empty: the groups become D1 and D3.
  - A group with no values (forced through the globals): "Group B has no values." and "Each group needs at least one value.".
  - All values equal: refused.
  - One sample, n = 1.
  - n > 50: no exact p. n > 100: no HL.
- **Device rules:**
  - The gate re-run passes.
  - 720 defined names: 0 built-in clashes ignoring case, 0 names that differ only in case, no keyword or one-letter names.
  - ≤ 6 names per LOCAL, no LOCAL inside a block, no comment inside a bracket.
  - CHOOSE indexes start at 0 and are tested by index.
  - GETKEY codes are all on the verified list.
  - MOUSE lists are read only after a `SIZE` check, and drains are capped by `TICKS`.
  - `STRING(ROUND(x,d),2,d)` throughout, and `rk_Num` checks for a "." before stripping zeros. `h.sci_strings` was empty in every run.
  - Zero-trip `FOR` loops rely on the G1-confirmed behaviour.
  - No MSGBOX over 5 lines.
  - `DRAWMENU` with variable labels and `CHOOSE` with expression items follow emulator-run precedents (NormExplorer 42, BayesTree 8c, BiNorm3D). The `{cgN(1), cgN(2), …}` list-element form (1682-1692) has no exact precedent, so put "Mann-Whitney on the draft-by-month data: pick X and Y" on the device checklist.
- **Style:**
  - The header matches the brief: licence, DISCLAIMER, AI credit, sources, data lines and replaced TI programs. The file map line numbers are exact.
  - The DISCLAIMER is also on the welcome page.
  - Every helper carries `rk_`, and the exports are `RK_*`.
  - Footers use the house form, in dodger blue.
  - The source is pure ASCII with LF and no tabs.
  - Glyphs are built with `CHAR()` (CHAR(179) is the one exception, item 6). Each preset's source line appears on its Result page.
