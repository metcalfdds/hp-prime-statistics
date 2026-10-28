# SurvLab beta 1: second review (independent)

Reviewer 2, 21 Oct 2026. I did not write SurvLab. I read `SurvLab_beta1.txt` (2,520 lines) line by line against `HP_Prime_Lessons_Learned_v7n.md` and `BRIEF_NEW6_v1.md`. I wrote my own checks, which do not import or reuse the builder's verify script. They are in the scratchpad:
- `rev2_check.py`: a KM / Greenwood reference in exact fractions, plus statsmodels `SurvfuncRight`, `quantile_ci` and `survdiff`, plus my own log-rank, Gehan-Breslow, HR and life table, compared with the program's engine in the harness. **5,931 checks, 0 failures.**
- `rev2_pages.py` and `rev2_rossi.py`: every menu path, run on all four Rossi presets and on awkward data typed into C1-C3.

`SurvLab_beta1.txt` was not edited.

**Bottom line.** I found **no wrong formula and no wrong number.** The one serious risk is a construct used nowhere else in the fleet (item 1). The other items are about wording and teaching, plus one speed concern.

---

## Findings, most serious first

### 1. Line 311: `DIMGROB_P` is called on a grob passed in as a parameter. Never tried on a device. **PLAUSIBLE (high impact)**

- **What.** `sv_Frame(frG, frT)` clears each page with `DIMGROB_P(frG, 320, 240, #FFFFFFh)`, where `frG` is the routine's parameter (`G1` or `G2`). Every page except Help comes through this routine: the opening page, KM base (G2), quantiles, the three log-rank pages, the life table and its plot, the load page and the busy page.
- **Why it is a risk.** Fleet routines that take a grob parameter only draw on it (`gbDisc(G1, …)`, `trDot`, `csDotV`), and that works on the emulator. No fleet program, nothing in hp-prime-kit, and nothing in the Community_Library zip *re-dimensions* a grob through a parameter. The harness treats G0-G9 as one shared object, so it cannot tell the difference.
- **Failure scenario.** Suppose the Prime binds the parameter to a copy, or to a new local grob. Then G1 and G2 are never cleared. Every page draws over the last one: KM curves pile up on each toggle, and log-rank page 2 is drawn over page 1. The student sees garbage on the first page change.
- **Fix.** The grobs are already sized in `sv_Init` (lines 2483-2484). Clear with the call the fleet has proved:
  ```
  RECT_P(frG, 0, 0, 319, 239, #FFFFFFh, #FFFFFFh);
  ```
  Alternatively, call `DIMGROB_P(G1, …)` / `DIMGROB_P(G2, …)` explicitly at the call sites.
- Either way, put "every page change clears the screen" first on the device checklist.

### 2. Lines 719-755 and 2413-2414: the life table's last Rossi interval runs past follow-up. **CONFIRMED (teaching, medium)**

- **What.** Intervals are [a, a+w). At width 4, the 318 men censored at exactly week 52 and the 4 arrests in week 52 land in a row [52, 56). That row assumes the withdrawals were at risk for half the interval, so n′ = 322 − 159 = 163 and q = 4/163 = 0.0245. Its "S end" (0.7271) is plotted at week 56.
- **Why it matters.** Nobody was followed past week 52, and nobody withdrew in the middle of that interval. The correct risk set for those 4 arrests is 322 (q ≈ 0.0124), and KM gives 0.7361.
- I reproduced 322 / 318 / 163 / 4 / 0.0245 / 0.7271 with my own code. The convention matches SAS's intervals, so the arithmetic is "right". But the screen gives the student an S at 56 and a life-table curve that dips below KM after the data end.
- Help page 4 says only that "the last interval holds the 318 withdrawals". The NOTES call the gap "the half-interval assumption" without saying that here the assumption is false.
- **Fix.** Any one of these:
  - (a) when every censoring in the last interval is at its start and equals the last follow-up time, end the table at that time and print "n′ = n here: all withdrawn at the end of follow-up";
  - (b) for the Rossi preset (whole weeks), use intervals (a, a+w] and say so;
  - (c) at minimum, put an orange line on that row and in the plot: "row 52-56: everyone left at week 52, so the half-interval rule overstates q here; KM S(52) = 0.736".

### 3. Help page 2 (lines 2374-2379) and header lines 66-69: SAS is misquoted, and the quantile is misnamed. **CONFIRMED (against SAS/STAT LIFETEST documentation, statug 68162, "Breslow, Fleming-Harrington, and Kaplan-Meier Method")**

- **The SAS rule.** The screen calls "the first time S(t) < 0.5" "SAS's and statsmodels' rule". SAS **averages** when S(t) equals 1 − p exactly over an interval: "If Ŝ(t) is exactly equal to 0.75 from t_j to t_{j+1}, the first quartile is taken to be (t_j + t_{j+1})/2". Only statsmodels uses the strict rule with no averaging.
- **The name.** The help line "25%: S = 0.75, the '75th-percentile survival time'" contradicts SAS, which calls this "the first quartile (or the 25th percentile)". So do Collett, Stata and statsmodels (`quantile(0.25)`). A student who carries the term to SAS or SPSS output will read the wrong row.
- **Scenario.** C1 = 1, 3, 4, 6, 2, 3, 5, 7; C2 = 1, 0, 1, 1, 1, 1, 0, 0; C3 = 1, 1, 1, 1, 2, 2, 2, 2.
  - Group 2's S sits at exactly 0.500 from week 3 to the end.
  - SurvLab prints "n.r." beside "S(7) = 0.500; 50.0% had the event". That is correct under its stated rule, but the help attributes the rule to SAS.
- **Fix.**
  - Help: "Median: the first time S(t) < 0.5 (statsmodels' rule; SAS and R average when S sits exactly on 0.5)".
  - Help: "25%: S = 0.75, the 25th percentile (first quartile) of the time to re-arrest".
  - Header: the same wording.

### 4. Lines 2276-2326, 637-648, 1058-1104 and 1376-1471: big data is slow and Esc cannot stop it. **PLAUSIBLE (speed, medium-low)**

I counted interpreted statements in the harness. The 2,000-row data was random, with times up to 100,000:

| Work | Rossi | 2,000 rows | Factor |
|---|---:|---:|---:|
| Load / fit | 18,074 | 342,106 | 19× |
| KM base redraw | 6,166 | 213,490 | 35× |
| CI toggle (`sv_CIs`) | 1,598 | 65,299 | |
| Quantile page | 4,169 | 89,400 | |

- **Scenario.** A student loads 2,000 rows and taps Band, Zoom or CI. Each tap redraws the base with no busy page and no Esc. If the G1 runs about 10k statements per second (untimed), that is roughly 20 s per tap.
- The quantile page also computes `sv_QCI` twice per row (lines 1402 and 1431).
- **Fix.**
  - Cap the rows at 500, or show `sv_Busy` and poll `GETKEY == 4` inside `sv_KMBase` / `sv_CIs` above about 300 distinct times.
  - Compute each row's `sv_Quant` / `sv_QCI` once per `sv_QDraw`.
  - The brief asks for Esc on anything over about 2 s on a G1.

### 5. Lines 2260-2261: one row in C1 is called "no data". **CONFIRMED (low)**

- **Scenario.** C1 = {7}, C2 = {1}. The MSGBOX says "C1 holds no data yet. Open Statistics 2Var (Apps): …".
- **Fix.** When `mdN == 1`, say "Need at least 2 rows; C1 has 1."

### 6. Lines 2168-2171 with line 2327: a wrong note on the "one group code" load page. **CONFIRMED (low)**

- When C3 holds a single code, `svOwn` = "C3 holds one group code only: one group". Line 2170 then always adds "An observed grouping, not an experiment.", which makes no sense when there is no grouping.
- **Fix.** Print line 2170 only for SurvLab's own splits, for example with a flag set in `sv_Preset`.

### 7. Line 1171: "exp(-H) is close to it" is not always true. **CONFIRMED (arithmetic)**

- exp(−H_NA) ≥ S_KM always, and the gap is large when few are at risk.
- **Scenario.** Two people, both events at t = 3: S = 0 and exp(−H) = e⁻¹ = 0.368.
- **Fix.** "exp(-H) is close to S while many are at risk; never below it."

### 8. Lines 1604-1641: the HR CI line, and the assumption wording. **CONFIRMED (teaching, low)**

- **The HR CI.** The formula is the textbook one: (O₁/E₁)/(O₂/E₂), with SE(ln HR) = √(1/E₁ + 1/E₂). My Rossi reference gives 0.6918 (0.4792 to 0.9988).
  - The "p and the HR's CI disagree" line is honest.
  - A one-line pointer would teach more: Peto's estimate exp((O₁ − E₁)/V), with CI exp(±1.96/√V), agrees with the log-rank test by construction. For Rossi it is 0.692 (0.479 to **1.0002**).
- **The assumption line.** Line 1640, "HR: no crossing", is too terse. Suggest "HR assumes proportional hazards (curves should not cross)."

### 9. Lines 1782-1785: a heuristic is stated as a fact. **CONFIRMED (wording, low)**

- "the gap is bigger early on" / "the gap grows later on" come from G-B χ² / LR χ² > 1.15 or < 0.87. That is a rule of thumb, not a test.
- **Fix.** "suggests the gap is bigger early on". In Help, name it SurvLab's rule of thumb.

### 10. Lines 2072-2077 and 1328: what some taps do. **CONFIRMED (code reading, low)**

- **Line 2072-2077.** In the life-table plot, a tap off every bar leaves `svLSel` unchanged, so it shows the previously selected interval again.
- **Line 1328.** A tap on the KM title band (y < 19) explains the *censor ticks*, which is unexpected.
- **Fix.**
  - Set `svLSel := 0` before the hit test.
  - Make a title tap show the subtitle's meaning, or nothing.

### 11. Line 1454: the "try 25%" advice can be useless. **CONFIRMED (low)**

- With no events at all, the page says "So the median is not reached: try 25%, 20%, 10%". None of those can be reached either.
- **Fix.** When the row's events are 0, say "no events: no quantile can be estimated".

### 12. Lines 1440 and 2380-2382: the quantile CI's upper end is open. **CONFIRMED (low)**

- Brookmeyer-Crowley and SAS extend the CI "to but not including the next event time". The screen prints "95% CI 16 to 36" (aid, 10%) with no hint that 36 is excluded.
- **Fix.** Add a help line: "the upper end is the next event time, not included".

### 13. Lines 71-72: a garbled book title in the header comment. **CONFIRMED (low)**

- "Allison (1995) Survival Analysis Using SAS and R carData (Rossi)" reads as a book title that does not exist.
- **Fix.** "Allison (1995) *Survival Analysis Using the SAS System: A Practical Guide*, SAS Institute; and R package carData (Rossi)".

### 14. Text widths. **PLAUSIBLE (device check)**

- In the harness, ten strings estimate at 92-95% of their TEXTOUT_P width. Among them:
  - the "Borderline: p and the HR's CI disagree" line;
  - the life-table footer;
  - the load page's "Source: …" line;
  - five help lines.
- In the at-risk table, "no aid" ends at about x = 33 and the first count starts at x = 35.
- The NOTES' checklist covers this already. Add "no aid" / "216" at the y axis to it.

### 15. Style. **CONFIRMED (cosmetic)**

- The band colours (#C3D7FF, #F3C8F3, #C8EBD2) and the tail (#FFC8C8) are not the house shade RGB(170,205,255). The brief allows group colours, so this is acceptable. I note it only so it is a decision.

---

## Checked and found correct

**Rossi data**
- All 432 rows of week, arrest, fin, age and prio match `data/rossi.csv` exactly.
- 114 arrests; fin 216/216.
- Median prio = 2, so 0-2 holds 251. Median age = 23, so under 23 holds 206.
- Every censoring is at week 52, and 4 arrests are at week 52.
- The opening page (432 men, Maryland state prisons, 52 weeks, aid at random) and the load page ("assigned AT RANDOM: a real experiment") are right. The split presets are labelled as SurvLab's own and observational.

**Engine.** On the 4 Rossi presets and 8 awkward sets, everything below matches my exact fraction reference, and statsmodels where it applies:
- KM S;
- n at risk, counting a censoring tied with an event at the same time in that time's risk set;
- Greenwood V, which is −1 after n = d;
- Nelson-Aalen H;
- log-log and linear pointwise CIs;
- the quantile for p = 0.5, 0.25, 0.2 and 0.1, and its Brookmeyer-Crowley CI in both methods;
- O, E and V;
- log-rank χ² and p, checked against `survdiff`;
- Gehan-Breslow, checked against `survdiff(weight_type='gb')`;
- the HR and its CI;
- the life table at w = 1, 4 and 2.5.

The awkward sets were:
- events and censorings tied at the same times in both groups;
- everyone censored;
- a single subject, event and censored (engine level);
- last observation an event in one group and censored in the other;
- S exactly 0.5;
- two people in two groups;
- one group with no events.

**Formulas against the textbook definitions**
- The log-log CI is S^exp(±z√V/|ln S|). This is Kalbfleisch-Prentice, statsmodels "cloglog" and R "log-log". It equals inverting the B-C z-test, so "CI bars: every time whose band reaches the line" is an exact description.
- The B-C test statistic is identical to statsmodels' `quantile_ci`, which follows SAS's construction.
- The log-rank variance is hypergeometric.
- The Gehan weight is n(t).
- The HR variance is 1/E₁ + 1/E₂, as in Kirkwood & Sterne and Altman.
- The actuarial n′ = n − c/2 is Cutler-Ederer.
- p = 2Φ(−√χ²) is a lower tail.
- z comes from −ICDF(0.025). No other ICDF call appears, so there is no ∞ risk.

**Device checklist numbers.** I recomputed them independently:
- t = 26: aid S 0.8981 (0.849 to 0.932), n = 194; no aid 0.8519 (0.797 to 0.893), n = 187.
- t = 30, linear: aid 0.852 to 0.935; H = 0.1120, exp(−H) = 0.8940.
- Quantiles at 25%, 20% and 10%, with CIs, all as the NOTES list them.
- χ² 3.8376, p 0.0501, G-B 3.7495.
- Life table [52, 56): 322 / 318 / 163 / 4 / 0.0245 / 0.7271.

**Device rules**
- Every LOCAL is at the top of its routine, at most 6 per line.
- No comment sits inside a bracket.
- Every CHOOSE starts its index at 0, is tested by the index, and carries no numbers in its strings.
- INPUT takes a LOCAL name.
- Every MSGBOX is 5 lines or fewer, and each line 38 characters or fewer.
- `STRING(ROUND(x, d), 2, d)` is used everywhere (`sv_F`, `sv_TS`, `sv_I`, `sv_Sg`); harness `sci_strings` were empty.
- No fractional df: `CHISQUARE(1, …)` is the density.
- No INSTRING, no CAS, no Python.
- Bare `RETURN;` is used as in NormExplorer.
- No loop can run unbounded: grid and tick loops are capped at 16, and drains at 1 s via TICKS.
- Esc is honoured in every view, in Help, and as Cancel on the main menu.
- Soft keys are read on the press, with y ≥ 218 and `MIN(6, IP(x/53.4)+1)`, ChiTable's polling pattern.
- Lists stay under 10,000 elements: 3 × 2,000 = 6,000.
- The 1E−10 tolerance at S = 1 − p absorbs 12-digit product error.
- Stale-key mode: no skipped pages.

**Style**
- The header matches the brief byte for byte, including AI credit, DISCLAIMER, sources, data, replaces and file map. The file-map line ranges are correct.
- The DISCLAIMER is on the opening page.
- Every helper carries the `sv_` tag; there are 72 routines.
- The source is pure ASCII with LF line ends.
- Footers use the canonical "x = y, …" dodger-blue form.
- The quit summary is RETURNed.
- The citations (KM 1958, Greenwood 1926, Mantel 1966, Peto & Peto 1972, Gehan 1965, Breslow 1970, Nelson 1972, Aalen 1978, Cutler & Ederer 1958, B-C 1982) have the right journals, volumes and pages.
