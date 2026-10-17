# EpiStats v1.7: changes from v1.6

*16 October 2026. v1.7 is the EXACT version, built on v1.6. It keeps every v1.6, v1.5 and v1.4 change. **It has not been run on hardware** (nor have v1.6, v1.5 and v1.4), and **nothing about the CAS has run on our calculators yet**.*

File: `/home/claude/work/out/EpiStats_v1.7.txt`: 5,653 lines, 253,817 bytes, UTF-8, LF, 122 routines (v1.6 had 99). The file was made from v1.6 by 47 counted, exact replacements, each of which had to match once (`make_es17.py` in the session scratchpad). In this document, "v1.6" line numbers are the base's and "v1.7" line numbers are the new file's.

---

## (a) Every change

| # | Item | v1.6 | v1.7 | What changed |
| --- | --- | --- | --- | --- |
| 1 | Header | 3, 14-17, 175 | 3, 14-60, 223 | v1.7 banner. Firmware line: v1.6-v1.4 also untested, and "run CASProbe beta 1 first". A dated "What changed in v1.7" paragraph. Licence, AI-assistance and firmware lines are kept. |
| 2 | **New results** | after 254 | 302-312 | `EP_sens_CP`, `EP_spec_CP`, `EP_ppv_CP`, `EP_npv_CP`, `EP_risk_exp_CP`, `EP_risk_unexp_CP` (each `{low, high}`), `EP_OR_CMLE`, `EP_OR_CMLE_CI`. The value 999 means infinite or undefined, as `EP_OR` already uses it. All 46 v1.6 `EP_*` are kept. |
| 3 | File-level state | after 309 | 367-386 | Four `LOCAL` lines of 6 names or fewer, all tagged `es`. They hold the CAS flag, the BINOMIAL check, the conditional-OR cache, the exact-CI caches, the page-6 selection and CAS texts, the Help F caches and the page-7 picture. `es_Init` (390) sets every one. |
| 4 | **BINOMIAL self-check** | — | `es_BinCheck` 802 | At start, `BINOMIAL_CDF(20, 0.1, 2)` must give 0.676926805 and `BINOMIAL(19, 0.1, 2)` 0.285179807. If not (for example the arguments are read as (n, k, p)), every exact CI reads "unavailable" instead of showing a wrong number. |
| 5 | **The CAS kit** | — | `es_IStr` 720, `es_Cas` 739, `es_Swap` 765, `es_CasShow` 781 | Copied from BRIEF_CAS.md, including the coordinator's update that strips one surrounding pair of `"` (CHAR(34)). **One line is added** to the kit: `es_Cas` sets `esCasOK` where the answer is judged. The IFERR line is untouched, so CASProbe's verdict is still a one-line change. `es_CasShow` turns the tagged CAS variable `esq` into `p` and `*` into `×`. |
| 6 | **Exact interval, the fleet's one routine** | — | `es_CPB` 841, `es_CPInt` 900 | Clopper-Pearson, and mid-P from the same code. Lower end: P(X ≥ k \| p) = α/2. Upper end: P(X ≤ k \| p) = α/2. Each end is found by bisection on [0, 1] using `BINOMIAL_CDF(n, p, k)`. A Newton step is taken instead of the halving whenever it lands inside the bracket; the slope is n·`BINOMIAL(n−1, p, k)`. k = 0 and k = n use the closed forms 1 − (α/2)^(1/n) and (α/2)^(1/n). The stop is relative (1E-9 of p), which the Prime's 12-digit arithmetic can reach. A 100-pass guard was never reached in tests. The Wilson interval at the same level is the starting guess. **CICatcher beta 2's `cqCPB` / `cqCPInt` are the same lines** (checked by the verify script). |
| 7 | **Conditional MLE odds ratio** | — | `es_NCFill` 942, `es_NCEval` 965, `es_NCRoot` 1017, `es_CondOR` 1070, `es_CORTxt` 1095, `es_SigTxt` 915 | The log weights of every possible a′ under OR = 1 come from the ratio of neighbouring terms: one LN each, no factorials, no LNGAMMA. The estimate solves E[a′ \| ψ] = a, the CI ends solve P(a′ ≤ a \| ψ) = α/2 and P(a′ ≥ a \| ψ) = α/2. Each is found by bisection on ln ψ ∈ [−60, 60] with Newton steps. The slopes come from the same sums: the variance, and conditional means minus the mean. Each evaluation finds the peak by halving (the weights are log-concave) and sums outward only until a term is below e^−46 of the peak. A table with N = 1980 therefore costs 2,126 EXP terms in total, not 3 × 7 × 981. States: 0 inside, 1 a at its smallest (MLE 0), 2 a at its largest (MLE infinite), 3 an empty margin (undefined, as SciPy), 4 N > 2000 (not computed: Fisher's cap). |
| 8 | Module 1 page 1, **Cohort tab** | 1570-1585 | 2059-2075 | Under the OR line, in orange: `  cond. MLE OR = 8.56  (2.09-41.3): page 7`. To fit it, the two grey v1.6 notes share one line: "Rows = exposure: risks real; worked: page 5." There are still nine lines, the last at y 194. |
| 9 | Module 1 page 1, **Diagnostic tab** | 1595-1601 | 2097-2108 | A new orange line under Wilson's sensitivity and specificity lines: `Exact: sens (36.1-80.9%), spec (69.7-95.2%)`. It comes from `esX1`, worked out once per table. Wilson is kept. |
| 10 | **Module 1 page 7 (new): EXACT ODDS RATIO** | — | `es_CORFill` 2332, `es_CORPage` 2386 | The sample OR with its Woolf CI, beside the conditional MLE with its exact CI ("R's fisher.test and SciPy report it"). Orange bars show P(a′) at the MLE: their mean is your a, which is the red line. A grey line shows P(a′) when OR = 1 (page 4's bars), with its mean dotted at (a+b)(a+c)/N. The teaching lines: "Why two? This one fixes all four totals, as / Fisher's test does: nearer 1; big N: the same." The picture is worked out on the first visit for each table. States 1-4 get their own sentences. |
| 11 | Module 1 entry and pages | 1825, 1942-1976, 2027; headers 1522, 1725, 1425, 2037, 2086, 2140 | 2484, 2603-2621, 2652-2655, 2706 | `es_CondOR` and the two exact CIs are computed once per table and `EP_OR_CMLE(_CI)` is set. The module now has seven pages, so headers read n/7. A right tap on 6/7 now goes on to 7/7, and 7/7 is the last page. |
| 12 | Module 2 entry | after 2270 | 2951-2958 | `EP_risk_exp_CP`, `EP_risk_unexp_CP`, once per table. |
| 13 | **Module 2 page 4, the risk bars** | 2469-2562 | 3156-3255 | Wilson's black whisker moves 6 px left. The exact CI is an orange 2-px whisker to its right, and is always the taller of the two. The y scale includes the exact upper ends. Legend: "95% CIs: black = Wilson, orange = exact (C-P)". Without the BINOMIAL check, the page is as in v1.6. |
| 14 | Module 3 entry | after 3003 | 3850-3866 | `EP_sens_CP` … `EP_npv_CP` and `esXCP`, once per table. mid-P is computed later, on page 6's first visit. |
| 15 | **Module 3 page 6 (new): EXACT vs WILSON** | — | `es_XPx` 3622, `es_XBar` 3627, `es_XCas` 3645, `es_ExactPage` 3667 | One row each for Sens, Spec, PPV and NPV, each with three bars on a 0-100 % axis: Wilson (black), exact (orange), mid-P (green), plus a red tick at the estimate. A tap on a row, or Up/Down, fills the orange panel: the fraction, Wilson / exact / mid-P, and "coverage >= 95 %". When the count is 0 or n, it also shows the CAS line `exact lower = (1/40)^(1/30)` with the badge "exact (CAS)". The fallback is `exact lower = (α/2)^(1/n) = 0.8843` with "decimal". |
| 16 | Module 3 pages | 3075-3086; headers 3092, 3137, 3178, 2672, 2750, 2838; 3130 | 3940-3965, 4011 | Six pages (headers n/6). Page 6 keeps a tap on a row and Up/Down for itself; everything else turns pages. Page 1 gains the orange line "CIs above: Wilson.  Exact and mid-P: page 6." |
| 17 | **Help menu** | 4375-4408 | 5251-5296 | It has 16 items, so it uses **CHOOSE's list form** (the simple form stops at 14; ChiTable and BayesTree already use the list form). New items: **E "Exact CIs, Exact OR"** (`es_Help_Exact` 5485) and **F "Where the SE Comes From"** (`es_Help_SE` 5544, `es_CasPage` 5505, `es_SETerm` 5525). G = Back. |
| 18 | **Help F: the delta method, with the CAS** | — | 5544-5650 | The CAS differentiates ln(p/(1−p)) live (`diff(ln(esq/(1-esq)),esq)` → `1/p+1/(1-p)`) and checks that this equals 1/(p(1−p)) (`simplify(…)` → `0`). Then the page builds Var g(p̂) ≈ g′(p)² Var(p̂) = 1/cases + 1/non-cases, so the rows add up to 1/a + 1/b + 1/c + 1/d. The CAS adds the four fractions for your last table (`EP_table`), or an example table, exactly: `1/12+1/5+1/8+1/30` → `53/120`, so SE = sqrt(53/120) = 0.6646. When a cell is 0, every cell gets 0.5, written as 2/(2a+1) so CAS text stays whole numbers. The calculus is asked once per run and the fraction once per table. A fraction too long to show is described ("an exact fraction with N digits"), never cut off. |
| 19 | Help pages updated | 4422, 4432, 4483-4487, 4539-4541, 4575 | 5309, 5319, 5372-5375, 5428, 5465 | About (v1.7, "Touch: Help 9-D; exact: E, F"), CIs (exact beside Wilson: Help E; its SE: Help F), Variables (the new names), Result pages (page 7). |
| 20 | Menu title | 364 | 454 | "EpiStats v1.7". |

**No "More" soft key.** No v1.7 screen has more than six soft-key actions: the new pages use taps and Up/Down, as page 4 of module 1 does.

---

## Gate output (final run)

```
=================== EpiStats_v1.7.txt ===================   (bash check.sh NEW EpiStats_v1.6.txt)
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW)  ---       66 E4      36 E9
--- 2. ppl_check_v2 tally (ORIG) ---       66 E4      36 E9
--- 2b. HARD errors (E2 E3 E6 E8 E10 E11) ---   none
--- 3. lint_ppl structural ---
4513 checks, 21 problems   (v1.6: 18 -- the same 12 'a'/denom/center lines and noise, plus 3 lines
  that are the CAS kit's own text, which BRIEF_CAS says to copy exactly:
  PROBLEM line 744: STRING() with 1 args, want 3     <- STRING(CAS(esS))
  PROBLEM line 755: STRING() with 2 args, want 3     <- INSTRING(cR, "undef") / INSTRING(cR, "rror")
  PROBLEM line 755: STRING() with 2 args, want 3        (the lint reads INSTRING as STRING; every
                                                         CAS-version program in out/ shows them))
--- 4. full parse (kit interpreter) ---
EpiStats_v1.7.txt  PARSE FAIL <ppl>:320: expected a name after EXPORT   (the first file-level LOCAL:
   ORIG: EpiStats_v1.6.txt  PARSE FAIL <ppl>:263 (the same)              the kit's known limit)
--- 5. --- 5653 lines, 253817 bytes, no E5 lines

python3 ppl_gate_v1a.py EpiStats_v1.7.txt EpiStats_v1.6.txt
2. ppl_check_v3 tally: 66 E4, 36 E9 / original 66 E4, 36 E9; hard errors: none
3. lint_ppl: 4513 checks, 21 problems (as above)
5. fleet_names_v2 over 27 files (newest of each program): 1244 routine names, 0 collisions,
   0 untagged, 0 mixed-tag files, 0 built-in matches
RESULT: PASS
```
The gate caught two real name clashes in the new code before they reached a paste. They were renamed: `coL` matches `COL` and `coS` matches `COS` when case is ignored (now `coLg`, `coSd`). The kit's `hpprime lint` and full parse are skipped inside `ppl_gate_v1a.py` here because the kit zip is not in this container; `check.sh` ran both from the unpacked kit (above). The harness reads the whole file.

---

## Verification: `verify_EpiStats_v1.7.py` → `verify_EpiStats_v1.7_output.txt`

**ALL CHECKS PASSED: 91 checks, 0 failures (100 s).** Part E also runs the whole v1.6 suite (`verify_EpiStats.py`: 120 formula checks, 83 harness checks, 28 scripted runs, layout audit over 262 pages, 0 warnings) against v1.7, and it passes unchanged.

### A. The formulas as the PPL computes them, against statsmodels / SciPy

```
A1. Clopper-Pearson vs proportion_confint(method="beta")  (every k of n = 1..60, plus
    k in {0,1,2,3,5,n/10,n/3,n/2,n-3,n-1,n} for n = 100, 200, 500, 1000, 2000)
    level   intervals  worst |diff|   worst rel (low>0)  max passes  mean BINOMIAL calls/interval
    0.5          1945      1.89e-15           3.83e-15           5      15.7
    0.8          1945      3.33e-15           7.03e-15           5      17.6
    0.9          1945      3.66e-15           8.60e-15           6      18.4
    0.95         1945      3.22e-15           8.18e-15           6      18.3
    0.99         1945      3.66e-15           1.10e-14           7      19.6
    0.999        1945      5.94e-15           1.11e-13          13      22.5
  ok  Clopper-Pearson: 11,670 intervals, worst |difference| from statsmodels 5.9e-15 (target 1E-8)
A2. ok  mid-P vs an independent brentq on the mid-P tails: worst |difference| 6.7e-16 (5,490 intervals)
    ok  mid-P always lies inside Clopper-Pearson (0 exceptions)
A3. conditional MLE OR and exact CI vs scipy.stats.contingency.odds_ratio(kind='conditional')
    459 tables compared (22 chosen, 400 random up to 40 a cell, 40 random up to 500), plus empty-margin
    tables (undefined, CI (0, inf), as SciPy) and N > 2000 (not computed, by design)
    worst relative difference from SciPy: 3.6e-08; at most 5 passes per root; at most 2,126 EXP terms
    where they differ by more than 1E-9, our answer solves its own equation at least as well:
    SciPy's brentq stops at an ABSOLUTE 1E-13 in psi, which is coarse when psi is about 1E-6
    (12 5 8 30)          MLE 8.558485 (2.087486-41.317307)  scipy 8.558485 (2.087486-41.317307)
    (7 15 58 472)        MLE 3.783669 (1.251483-10.363494)  scipy 3.783669 (1.251483-10.363494)  [SciPy's doc example]
    (700 300 280 700)    MLE 5.827442 (4.783758-7.113846)   scipy 5.827442 (4.783758-7.113846)
```
(Halving alone would need about 33 passes per end at the same stopping rule.)

### B. The PPL routines themselves, in `ppl_run_v3`
- `es_CPInt` vs statsmodels: 1,569 intervals at 80, 95 and 99.9 %, n = 1-30 every k, plus 50, 100, 500 and 2000. Worst |diff| 5.9e-15. mid-P worst 6.7e-16. **BINOMIAL_CDF + BINOMIAL calls per interval: mean 19, max 38.**
- `es_CondOR` vs SciPy, 70 tables: worst relative difference 3.5e-8. All five states occur.
- `es_BinCheck` passes as written. When `BINOMIAL_CDF` is made to read (n, k, p), it fails, and the exact CIs read "unavailable".
- `es_BinCheck`, `es_CPB` and `es_CPInt` are **line for line** the same as CICatcher beta 2's `cq` copies (80 lines).

### C. Every CAS template through desktop Giac 1.9 (`icas`)
```
diff(ln(esq/(1-esq)),esq)                          -> 1/esq+1/(1-esq)   (= 1/(p(1-p)) by SymPy)
simplify(diff(...)-1/(esq*(1-esq)))                -> 0
1/12+1/5+1/8+1/30            -> 53/120          1/40+1/60+1/20+1/80     -> 5/48
2/1+2/11+2/7+2/21 (0 5 3 10) -> 592/231         1/700+1/300+1/280+1/700 -> 41/4200
1/1997+1/1993+1/1999+1/1987  -> 31712695576/15808695152273
1/999999+1/3+1/7+1/999998    -> 476191047617/999997000002        (all = Python Fraction)
1-(1/40)^(1/n), (1/40)^(1/n), n = 1..60, 100..2000: 130 templates, every one = 1 - 0.025^(1/n)
   or 0.025^(1/n) to 1E-12; n = 1 -> 39/40, n = 2 -> 1-sqrt(1/40), n = 20 -> 1-(1/40)^(1/20);
   longest answer 17 characters (page 6 shows up to 22)
```
**A Giac trap, now in the comments:** `simplify()` or `normal()` on these roots is unsafe. In Giac 1.9 they return "Root of 40*x^3-120*x^2+120*x-39" for n = 3, and "rootof minimal polynomial must be unitary Error" for (1/4)^(1/10) and others. The templates send the plain expression. The fraction sums use no simplify at all.

### D. End to end, `cas='giac'` and `cas='fail'`
- **Module 1, 12 5 8 30**, typed by grid taps. Cohort tab: `  cond. MLE OR = 8.56  (2.09-41.3): page 7` in orange, nine lines, the last at y 194. Diagnostic tab: `Exact: sens (36.1-80.9%), spec (69.7-95.2%)`, which equals statsmodels. Page 7/7, as drawn:
  ```
  y 27  Sample OR = ad/bc = 9.00, Woolf CI (2.45-33.11)
  y 39  Conditional MLE OR = 8.56  (2.09-41.3)                         (orange)
  y 51  (exact CI; R's fisher.test and SciPy report it)
  y 60  a = 12  (red, at the red line)     x ticks 0, 5, 10, 15
  y164  orange = P(a) at the MLE: its mean is your a
  y176  grey = P(a) if OR = 1 (page 4); its mean is 6.18
  y188  Why two? This one fixes all four totals, as
  y200  Fisher's test does: nearer 1; big N: the same.
  ```
  There are 10 orange bars. `EP_OR_CMLE` = 8.558485 and `EP_OR_CMLE_CI` = {2.087486, 41.317307}. **Module 1 makes no CAS calls.**
- **EpiStats2x2**, all five states:
  - (0,5,3,10): `0  (0-6.61)`, "MLE 0: your a is the smallest it can be";
  - (5,0,3,10): `infinite  (1.70-infinity)`;
  - (0,0,5,20): `undefined (a total is 0)`;
  - (700,300,600,500): `not computed (N > 2000)`;
  - (700,300,280,700): `5.83  (4.78-7.11)`.
- **Module 2, 40 60 20 80**, page 4: 8 orange whisker lines and the new legend. `EP_risk_exp_CP` = {0.3033, 0.5028} and `EP_risk_unexp_CP` = {0.1267, 0.2918}, which equal statsmodels.
- **Module 3, 12 0 8 30** (spec 30/30, PPV 12/12), page 6. Open, tap Spec, Down, Up, tap Sens.
  - The panel for Spec reads: Wilson (88.6-100.0%), exact (88.4-100.0%), mid-P (90.5-100.0%).
  - giac: `exact lower = (1/40)^(1/30)` with "exact (CAS)". The CAS is asked exactly twice, once for Spec and once for PPV; returning to Spec uses the cache.
  - fail: `exact lower = (α/2)^(1/n) = 0.8843` with "decimal", and no error.
- **Help F.**
  - giac: `CAS: g'(p) = 1/p+1/(1-p)`, `  = 1/(p(1-p))   (CAS: the difference is 0)`, `  = 53/120`, `SE = sqrt(53/120) = 0.6646`, "exact (CAS)". For 0 5 3 10: "(+0.5)" and `= 592/231`. Four CAS calls over three openings and two tables.
  - fail: `g'(p) = 1/p + 1/(1-p)  (textbook form)`, `= 0.441667`, `SE = sqrt(0.441667) = 0.6646`, "decimal". The CAS is asked 3 times in the run, not on every opening.
- **Static checks.** Nothing draws on G0 except `BLIT_P(G0, …)`. `CAS(` is on one code line, inside `es_Cas`. `es_Cas` is called only from `es_Help_SE` and `es_XCas`, both on events. Layout of the new and changed pages at 6.5/8/9.5 px a character: no problems (the "100%" axis label was moved left after the first run flagged it).

### Cost of the new numerics (harness counts, for the G1 timing on the device)
| Event | Work |
| --- | --- |
| Module 1 entry, 12 5 8 30 | 40 BINOMIAL calls (exact sens and spec) + the conditional OR (212 EXP terms, 17 LN) |
| Module 1 entry, N = 1980 | the conditional OR: 2,126 EXP terms + 980 LN, on top of v1.6's Fisher (about 4,000 `es_lngamma` calls) |
| Module 2 entry | about 40 BINOMIAL calls |
| Module 3 entry | 80 BINOMIAL calls (4 exact CIs) |
| Module 3 page 6, first visit | 144 more (mid-P for 4; mid-P costs about twice CP) |
| Help F, first open | 3 CAS calls; later opens of the same table, 0 |

---

## (b) DEVICE TEST CHECKLIST, least to most risky

1. **Run CASProbe beta 1 first**, on the G2 and the G1. If it reports a call form other than `STRING(CAS(s))`, change the one IFERR line in `es_Cas` (v1.7 line 744). If it reports that answers come back quoted, the kit already strips one pair of `"`. If the CAS cannot be used at all, change nothing: every CAS line falls back to its decimal with the "decimal" badge (steps 15-17 say what you should then see).
2. **Paste and compile.** If it stops, note the line. The likely spots, most likely first:
   - the list-form help `CHOOSE` at 5261 (16 items);
   - the new file-level `LOCAL` lines 368-371;
   - `es_Cas`'s IFERR around `CAS(…)` (744) and the `CHAR(34)` comparison (751);
   - `RETURN` inside `IF` inside `CASE`, which v1.2's main menu already does.
3. **Catalog and the BINOMIAL order.** EpiStats and EpiStats2x2 are listed. In Home:
   - `BINOMIAL_CDF(20,0.1,2)` should give 0.676926805…;
   - `BINOMIAL(19,0.1,2)` should give 0.285179807….

   If either differs, every exact CI will say "unavailable": tell Claude the values.
4. **Module 1, 12 5 8 30, page 1 Cohort.** Under the OR line, in orange: "  cond. MLE OR = 8.56  (2.09-41.3): page 7". The grey last line reads "Rows = exposure: risks real; worked: page 5." Nothing touches the footer.
5. **Diagnostic tab.** Under the Wilson lines, in orange: "Exact: sens (36.1-80.9%), spec (69.7-95.2%)". Check it is not cut at the right edge (43 characters).
6. **Pages 2-6** read n/7. A right tap on 6/7 goes to 7/7, and a right tap there stays put.
7. **Page 7/7 (Left from page 1).**
   - Ten orange bars rise to the right of the middle; the grey line peaks further left.
   - There is a dotted grey vertical at about a = 6, and a red line with "a = 12" near the right end.
   - The four lines under the plot read as in (D) above.
   - Check that "Fisher's test does: nearer 1; big N: the same." (46 characters) fits.
8. **EpiStats2x2 from Home**, page 7 for each table:
   - (0,5,3,10): "0  (0-6.61)", MLE 0 sentence, grey line only;
   - (5,0,3,10): "infinite  (1.70-infinity)";
   - (0,0,5,20): "undefined";
   - (700,300,600,500): "not computed (N > 2000)".

   Each table still returns Fisher's p to Home.
9. **Module 2, 40 60 20 80, page 4/5.** Each bar has a black whisker left of the middle and a taller orange whisker right of it. The legend reads "95% CIs: black = Wilson, orange = exact (C-P)". `EP_risk_exp_CP` in Home holds {0.3033…, 0.5028…}.
10. **Module 3, 12 0 8 30.**
    - Page 1/6 ends with the orange line "CIs above: Wilson.  Exact and mid-P: page 6.", and the headers read n/6.
    - Left from page 1 goes to page 6/6: four rows, each with black, orange and green bars and a red tick. Spec and PPV sit at the right edge (100 %).
    - Tap the Spec row: it turns light orange and the panel reads "Specificity d/(b+d) = 30/30 = 100.0%", "Wilson (88.6-100.0%)", "exact (88.4-100.0%)", "mid-P (90.5-100.0%)", "coverage >= 95 %".
    - Up/Down move the row. A tap outside the rows turns the page.
11. **Help menu.** 16 items, labelled 1-9 then A-G, with E = "Exact CIs, Exact OR", F = "Where the SE Comes From", G = Back. Item 1 says "v1.7" and "Touch: Help 9-D; exact: E, F". Item E: 12 lines, nothing cut.
12. **G1 timing.**
    - `EpiStats2x2(700,300,280,700)`: note the seconds before page 1 appears (Fisher plus the conditional OR, item (D) cost table), and the first visit to page 7.
    - Module 3 page 6, first visit: 144 BINOMIAL calls.
    - A forest-plot or bar tap should still redraw promptly.
13. **Glyphs.** α (CHAR(945)) in the page-6 fallback line; p̂ (CHAR(57345)) and ² (CHAR(178)) in Help F; × (CHAR(215)) in CAS text if it carries `*`.
14. **`MAKELIST(…, K, …)`** (es_NCFill, es_CORFill) writes Home's K, as v1.6's pages already do.
15. **CAS: Help F** with the example table (open it before any module, or after a fresh start). What you should see:
    - "CAS: g'(p) = 1/p+1/(1-p)". The Prime's older Giac may print an equivalent form: note it.
    - "  = 1/(p(1-p))   (CAS: the difference is 0)".
    - "  = 53/120", "SE = sqrt(53/120) = 0.6646", and "exact (CAS)" in dodger blue.

    Note the seconds on the G1. Open F again: it should be instant (cached).
16. **CAS: Help F after module 1 with 0 5 3 10:** "(+0.5)" and "  = 592/231". After 700 300 280 700: "  = 41/4200".
17. **CAS: module 3 page 6, 12 0 8 30.**
    - Tap Spec: "exact lower = (1/40)^(1/30)" with "exact (CAS)".
    - Down to PPV: "exact lower = (1/40)^(1/12)".
    - If the CAS fails: "exact lower = (α/2)^(1/n) = 0.8843" with "decimal", and no error box.

---

## (c) Not confirmed, or left as it was

- **Hardware.** None of v1.4-v1.7 has run on a calculator. In particular these are not device-observed:
  - the list-form `CHOOSE` in this program (it is corpus- and fleet-used);
  - `CAS("…")` in any form;
  - `STRING()` of a CAS answer;
  - `INSTRING`, which only ran in PyProbe on the emulator;
  - `MID` with a length past the end of a string (`es_Swap` relies on it returning the shorter remainder);
  - every new pixel position.
- **The Prime's arithmetic is 12-digit BCD; the harness is IEEE double.** The stopping rules are relative 1E-9 in p for the exact ends and 1E-9 in ln ψ for the conditional OR, chosen so that rounding noise near the root cannot stall them. A 100-pass guard bounds the worst case. The pass counts on the device are not known.
- **Prime Giac vs desktop Giac 1.9.** The derivative's printed form, whether `simplify(…)` of the difference prints exactly `0`, and the closed-form echo could all differ. The page compares the check's text with "0"; if the Prime prints something else equivalent, the page simply omits "(CAS: the difference is 0)".
- **One line added to the kit** (`es_Cas` sets `esCasOK`). The IFERR line is untouched.
- **R itself was not run here.** The conditional MLE and CI are checked against SciPy, which follows R's definitions: the two one-sided α/2 tails, ψ̂ with mean = a. R's source finds ψ̂ with `uniroot` at its default tolerance, so R's printed digits may differ from SciPy and EpiStats in the third or fourth significant figure. That is inferred from R's source, not observed. Roger can check in R with `fisher.test(matrix(c(12,8,5,30),2))`.
- **Font widths** are estimates (6.5 px a character, font 1). The longest new lines are 46-47 characters, at ChiTable's verified 48.
- **The exact CIs use 95 % throughout** (α/2 = 0.025), as all of EpiStats does. Woolf/Katz CIs still use 1.96, as in v1.6.
- **mid-P is not exported** (no `EP_*_MP`), and appears only on module 3 page 6.
- **Not changed:** modules 4, 5 and 6, the sample-size screens, and every v1.6 computation (the v1.6 suite passes unchanged).

## Decisions for Roger

1. **Exact = orange, program-wide** (whiskers, bars, text). Magenta was taken by module 2's RD bracket, and orange is the house frame/panel colour. Keep, or name another?
2. **The two grey notes on the Cohort tab now share one line** so that the conditional MLE can sit right under the sample OR. Acceptable?
3. **Mid-P**: shown on page 6 only. Export it as `EP_*_MP` too?
4. **The CAS on page 6 is small and honest.** For n ≥ 3 the CAS returns the closed form as given, and it simplifies only n = 1 (39/40) and n = 2 (1−sqrt(1/40)). It is shown because the closed form is the exact answer. An idea not built: for a small table, the CAS could show that the conditional MLE is the root of the polynomial Σ(i − a)·C(a+c, i)·C(b+d, a+b−i)·ψ^i = 0.
5. **N ≤ 2000 cap** for the conditional OR, the same as Fisher's. A lower cap would make module 1's entry faster on a G1 if step 12 is slow.
