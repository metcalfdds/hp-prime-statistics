# SurvLab beta 1a — notes (21 Oct 2026)

Beta 1a applies the second review (`REVIEW2_SurvLab_beta1.md`, items 1-15). `SurvLab_beta1a_CHANGES.md` has one line per item. Everything below describes beta 1a.

`/home/claude/new6/SurvLab_beta1a.txt`: 2,651 lines, pure ASCII, LF. It starts with `EXPORT SurvLab()`, takes no arguments and opens on a menu. Every helper carries the tag `sv_`. Home exports use `SV_`. It is pure PPL: no CAS, no Python.
**Beta 1a has run only in the PC harness (ppl_run_v3e, with the updated `hpkit/interp.py`, which raises an error on `+` with a list operand; SurvLab has no list arithmetic). It has not run on the emulator or a calculator.**

**Grob pattern (review item 1).** No routine takes a grob parameter.
- Every helper draws on **G1 by name**, and every page clears with `DIMGROB_P(G1, 320, 240, #FFFFFFh)`. This is the fleet's verified pattern (ChiTable, TouchKit).
- The Kaplan-Meier plot is composed in G1, cached with `BLIT_P(G2, 0, 0, G1)` and restored each frame with `BLIT_P(G1, 0, 0, G2)`. That is GaltonBoard's device-run `BLIT_P(G2, 0, 0, G3)` / `BLIT_P(G1, 0, 0, G2)` shape.
- G2 is sized once, by name, in `sv_Init`.

## What it does, menu by menu

The opening page explains what the program is for and names the Rossi data and its source. It shows the DISCLAIMER in an orange panel. The Rossi fit runs while the student reads this page.

1. **Kaplan-Meier plot**
   - Draws one or two step curves: group 1 in blue, group 2 in magenta, everyone together in green. Each step is flat at the old S up to the event time, then drops straight down there, two pixels thick. Each curve stops at its group's last observed time.
   - The 95% CI band is shaded pale blue or pale magenta, and lavender where the two bands overlap.
   - A censor tick marks every censoring time. In Rossi every censoring is at week 52.
   - The numbers at risk at each tick time sit under the axis, in the group colours, as in a published KM figure.
   - A red cursor shows S(t), its CI and n at risk for each curve. The finger moves it to any time, and the readout follows a drag. Left and Right move it from event time to event time. Past a group's last follow-up the readout says so.
   - Soft keys, page 1: CI (log-log ↔ linear), Band, Zoom (y axis zoomed to the curves, with a red "zoomed: y from 0.60" warning), H(t) (the Nelson-Aalen view, whose readout gives H and exp(−H)), Back, More.
   - Soft keys, page 2: Pool/Split, Median, Test, Life, Back, More.
   - A tap on the title explains the band and the ticks.
   - With more than 150 steps, a "Drawing N steps ... (Esc = no band)" page shows while the plot is drawn, and Esc skips the band.
   - Enter opens a menu with every action, for keyboard use.
   - The plot without the cursor is cached in G2, so a cursor move costs one blit.
2. **Median and quantiles**
   - Soft keys Median, 25%, 20% and 10% pick the proportion re-arrested; ←→ cycle through them. CI switches log-log ↔ linear.
   - The picture shows the curves and a red dotted line at S = 1 − p. Each group's quantile is marked where its curve drops below the line, with a dotted line down to the time axis. Its Brookmeyer-Crowley 95% CI is a bar along the line, with an arrow when the upper end is not reached.
   - The text gives each group and "all": the estimate (or n.r.) and the CI.
   - When a quantile is not reached, the page says why: S stays at or above 1 − p, and S at the end. For the median it adds "try 25%, 20%, 10%". Rossi's median is not reached for any group.
   - Page titles read "Time by which 25% are re-arrested" (or "Median: time by which 50% …").
   - Headings name the percentile of the time to re-arrest: "25th percentile (Q1): first time S(t) < 0.75".
   - The rule "first time S < 1 − p" is statsmodels'; SAS and R average when S sits exactly on 1 − p (help page 2).
   - The CI's upper end, the next event time, is not included.
   - A group with no events gets "no events, so no quantile can be estimated".
3. **Compare groups: log-rank**, three pages, with soft keys Prev, Next, KM, Median, Life, Back.
   - **Page 1:**
     - Table of O, E and O − E per group. V, the log-rank χ² = (O₁ − E₁)²/V and its p. Bars: solid O, pale E. Tapping a bar says what it is.
     - HR = (O₁/E₁)/(O₂/E₂) with its approximate 95% CI.
     - Peto's HR exp((O₁ − E₁)/V) with CI exp(± 1.96/√V), whose CI misses 1 exactly when p < 0.05.
     - Gehan-Breslow's χ² and p.
     - The verdict at 0.05, worded "evidence" or "no convincing evidence". A "Borderline" line when 0.04 ≤ p ≤ 0.06. When p and the O/E-ratio CI disagree, as they do for Rossi, that line says so instead: p = 0.0501 while the CI ends at 0.9988. Peto's ends at 1.0002.
     - The assumption line: "HR assumes proportional hazards (no crossing)".
   - **Page 2:** the χ²(1) density, with the log-rank statistic as a red line and the tail beyond it shaded (= p). Gehan-Breslow is a dotted magenta line, and 3.84 (5%) a dotted grey one. Tapping a line says what it is.
   - **Page 3, "Early or late?":** the running total of O₁ − E₁ over time, and the Gehan-Breslow weight n(t)/n(0) against the log-rank weight 1. It explains that G-B counts early times more. A data-driven line follows, labelled as SurvLab's rule of thumb (not a test): "suggests the gap is bigger early on" if G-B/LR > 1.15, "… grows later on" if it is below 0.87, otherwise "… builds steadily".
   - With one group, the soft key and the menu item say "One group only".
4. **Life table (actuarial)** asks for the interval width (default 4 weeks; at most 100 intervals).
   - Intervals are [a, a+w). **The last one is cut at the last follow-up time T and closed, [a, T]: nobody is followed past T.** Those still followed at T complete it; they are not halved.
   - The table gives from-to, n entering, wdrn (censored before T), n′ = n − wdrn/2, d, q = d/n′ and S at the end. On the last row it says "Ends at 52: the 318 still followed then complete it".
   - With no censoring before T (Rossi), the life-table S equals KM at every interval end; S(52) = 0.7361. It shows 12 rows at a time: Up/Down scroll by a page, ⇅ scroll by one row, and a tap on a row explains it.
   - Group cycles through group 1, group 2 and all. Width asks again.
   - Plot draws the life-table S at the interval ends (magenta) over the KM curve (pale), and q as orange bars (tap a bar, or ←→).
5. **Load a preset** offers four presets, each followed by a load page with n, events, the groups, S at the end, a small picture of the curves and the source line:
   - Rossi: aid vs no aid. This is the randomised experiment, and the page says so.
   - Rossi: all 432 men.
   - Rossi: priors 0-2 vs 3+.
   - Rossi: age under 23 vs 23+.

   The last two are labelled in red as "SurvLab's split at the median …" and "An observed grouping, not an experiment." That second line appears only for these splits (not when C3 holds one code).
6. **Use my data (Stat 2Var)**
   - Reads C1 = time (0 to 999,999), C2 = 1 for an event or 0 for censored, and C3 = group 1/2 (optional; empty means one group). **Up to 500 rows.** 2,000 rows cost about 213,000 statements per KM redraw; 500 rows cost about 54,000; Rossi costs 6,200.
   - The first read of each column is inside IFERR.
   - It refuses a bad row, a size mismatch or an app that has never been opened, with a ≤ 5-line MSGBOX, and keeps the old data.
   - When C3 holds a single code it runs as one group and says so.
   - With more than 150 rows it shows a "working" page.
   - One row in C1 gives "Need at least 2 rows".
7. **Help** has 5 pages. Esc leaves from any page.
8. **Quit** returns a summary, for example `SurvLab: Rossi, aid vs no aid, log-rank χ²(1) = 3.84, p = 0.0501, HR = 0.69`.

**Home exports:**
- `SV_T`: the distinct event times, all groups together.
- `SV_S1` and `SV_S2`: KM S of each group at those times. `SV_S2` is `{}` with one group.
- `SV_CHI`, `SV_P`: the log-rank χ² and p, −1 with one group.
- `SV_HR`: the hazard ratio (O₁/E₁)/(O₂/E₂), −1 when it cannot be estimated.
- `SV_HRP`: Peto's exp((O₁ − E₁)/V), −1 with no test.
- `SV_MED`: the median of each group, −1 = not reached.

## Formulas and sources

| Quantity | Formula | Source |
|---|---|---|
| KM | S(t) = ∏ over u ≤ t of (1 − d/n); n = everyone with T ≥ u | Kaplan & Meier 1958, JASA 53:457-481 |
| Greenwood | SE = S·√V, V = Σ d/(n(n−d)); undefined from a time with n = d (as statsmodels) | Greenwood 1926 |
| CI, log-log (default) | S^exp(±z√V/\|ln S\|): always inside 0..1 | Kalbfleisch & Prentice 1980 (pages not checked); statsmodels "cloglog"; R "log-log" |
| CI, linear | S ± z·S√V, cut at 0 and 1 | statsmodels "linear" |
| Quantile p | first event time with S < 1 − p (statsmodels' rule; SAS and R average when S sits exactly on 1 − p). S = 0.75 is the 25th percentile (Q1) of the time to the event | statsmodels `quantile`; SAS LIFETEST docs |
| Its CI | event times with \|g(S) − g(1−p)\|/(g′(S)·SE) ≤ z; up to (not including) the next event time, or n.r. | Brookmeyer & Crowley 1982, Biometrics 38:29-41, in SAS/statsmodels form |
| Nelson-Aalen | H = Σ d/n | Nelson 1972; Aalen 1978 |
| Log-rank | E₁ = Σ d·n₁/n; V = Σ d(n₁/n)(1−n₁/n)(n−d)/(n−1) (n > 1); χ² = (O₁−E₁)²/V, 1 df | Mantel 1966; Peto & Peto 1972 |
| Gehan-Breslow | χ² = (Σ n(d₁−e₁))² / Σ n²v | Gehan 1965; Breslow 1970; statsmodels `weight_type='gb'` |
| HR | (O₁/E₁)/(O₂/E₂), CI exp(ln HR ± 1.96√(1/E₁+1/E₂)) | textbook approximation, e.g. Kirkwood & Sterne 2003 ch. 26 (pages not checked) |
| Peto HR | exp((O₁−E₁)/V), CI exp((O₁−E₁)/V ± 1.96/√V); misses 1 exactly when χ² > 3.84 | Peto et al. 1977 (pages not checked) |
| Life table | intervals [a, a+w), the last cut at T as [a, T]; n′ = n − c/2 for censorings before T; those censored at T complete the interval; q = d/n′; S = ∏(1−q) | Cutler & Ederer 1958; the closing date as in Lee & Wang 2003 ch. 4 and Collett 2015 §2.1.1 (pages not checked); the cut at T is SurvLab's stated convention |
| p of χ²(1) | 2·NORMALD_CDF(0,1,−√χ²): a lower tail, keeps its digits | Lessons Learned §3 |
| z | −NORMALD_ICDF(0,1,0.025) = 1.95996; the 5% critical value is z² = 3.8415 | |

**Data:** `data/rossi.csv`, all 432 rows and the columns week, arrest, fin, age and prio, stored as list literals in `sv_RData`. The source line on screen is "Rossi, Berk & Lenihan 1980 (via Allison 1995)". Aid is group 1, so HR < 1 means a lower hazard with aid.

## What was checked (`verify_SurvLab_beta1a.py`, output saved beside it)

**Result: 5,619 checks, 0 failures.** That is every beta 1 check, updated where beta 1a changes a page on purpose, plus Part E (review items 1-14) below.

**Gate** (`ppl_gate_v1c.py SurvLab_beta1a.txt SurvLab_beta1.txt`): PASS. Kit lint 0 errors; ppl_check_v4 clean; no hard errors; fleet_names: 26 files, 0 collisions, 0 untagged, 0 built-in matches. lint_ppl's 6 problems are the known file-name and EXPORT-discipline noise; the "not a GROB" lines are gone with the grob parameters. The full parse stops at the file-level LOCAL after the EXPORT line, a known tool limit (beta 1 and ChiTable fail the same way).

- **Part E, the review's items:**
  - static checks that no routine takes a grob parameter and that every drawing call names G0, G1 or G2;
  - the KM cache shape;
  - the life table ending at 52 with S = KM (Rossi, three rows, and 15 random sets);
  - the convention line and help page 4;
  - the quantile wording on help page 2 and the four quantile pages;
  - one call site each for sv_Quant and sv_QCI;
  - statement counts (Rossi fit 17,190 / KM plot 6,219; 500 rows fit 68,756 / KM plot 54,280; quantile page 4,169 → 3,296);
  - busy pages for 500 rows, and Esc stopping the band;
  - the "observed grouping" flag;
  - exp(−H) ≥ S;
  - Peto's HR on the page and in SV_HRP, its CI agreeing with p on every random set;
  - "suggests" and the rule-of-thumb help line;
  - the tap fixes;
  - the no-events message;
  - the open upper end;
  - the Allison citation;
  - the at-risk x position.

- **Part A, the engine.** It ran on the 4 presets and 35 random or edge sets. The random sets have 20 mixed sizes; the edge sets cover n = 2 and 3, all censored, all equal times, n = d at the end, S exactly 0.5, times up to 9×10⁹, events at time 0, no events in a group, fractional times, groups of 36 vs 4, a single code, heavy ties, one event, and n = 800. The engine was checked against two references:
  - an exact (fractions) reference written in the script: KM, Greenwood, n at risk, H, both pointwise CIs (inside 0..1 and around S), the quantiles and their CIs for p = 0.5, 0.25, 0.2, 0.1 in both methods, O/E/V, the HR and its CI, the life table under beta 1a's convention (last interval cut at T) at w = 1, 4, 5, 13, 0.5 (more than 100 intervals refused), and the exports;
  - statsmodels: surv_prob, surv_prob_se, n_risk, quantile, quantile_ci ("cloglog", "linear") and survdiff (log-rank and "gb").

  Where S equals 1 − p exactly at an event time (40 cases, listed as notes in the output), statsmodels' floating point can fall either side of the line. Those cases are checked against the exact rule only. SurvLab's rule there is the exact one: S = 0.5 exactly is not "below 0.5".
- **Part B, every menu path in the harness, with the page text compared against the reference:**
  - the opening page and its disclaimer;
  - the KM readout after arrows, a tap and a drag, in both CI types and the H(t) view;
  - the at-risk table;
  - the subtitles for band, zoom and pool;
  - both soft-key pages and More wrapping;
  - the quantile page for all 4 p in both CI types, and on the other presets;
  - the three log-rank pages, their taps and their verdicts;
  - the life table: rows, scroll, a tap, the group cycle, the plot, and widths 0 and 0.25 refused;
  - all 4 presets;
  - Use my data: valid, one group, codes all 2, 8 refusals (including one row and 501 rows);
  - edge data through every view: no events, no variance, HR not estimable, n = d;
  - Help and Esc out of it;
  - the Enter menus;
  - stale-key mode;
  - Quit's summary and the Home exports.
- **Part C, pixel geometry of the cached KM plot (S and H views):**
  - every step's flat stretch at the old value up to x(t), then its drop at x(t), and its 2-px partner;
  - the censor ticks at week 52;
  - 48 band rectangles at the CI ends, plus the lavender overlap;
  - the red cursor line.
- **Part D, all runs:**
  - no runtime error;
  - `h.sci_strings` empty;
  - no text past 320×240;
  - every MSGBOX ≤ 5 lines of ≤ 38 characters;
  - only 2 texts estimated to be cut: life-table "from" values like 249999.75, in a 42-px column.

## TI program reworked

KAPMEIT1 (zip 83, kaplanmeiertest1.zip) takes grouped data and gives S, Greenwood's variance and a step plot. Its bugs are not repeated here; the header lists them:
1. Greenwood's term divides by zero when n = d.
2. It reports a variance only: no SE, CI or median.
3. Censor marks sit half a day before the next event time.
4. It overwrites L1-L6 and lists A-E and V.
5. It takes whole-number, pre-grouped days only.
6. The plot runs 2 units past the last time.

There is no TI or Triola program for the log-rank test.

## Left out (beta 1a), and why

- **Confidence level fixed at 95%.** It keeps the pages simple.
- **No log-rank for more than 2 groups.** C3 takes 1 or 2.
- **No stratified test, no Cox model.**
- **No simultaneous (Hall-Wellner) bands.**
- **No Tarone-Ware or Fleming-Harrington weights.** One second opinion, as asked.
- **No "copy the preset to C1-C3".** It would overwrite the student's columns without a verified OK/Cancel MSGBOX.
- **No CAS.** Nothing here needs an exact answer.
- **Times capped at 999,999.** The labels and the table must fit the screen; the refusal message says to change the unit.
- **Rows capped at 500.** See review item 4.
- **Band colours.** The bands (#C3D7FF, #F3C8F3, #C8EBD2, overlap #D9C6F2) and the tail (#FFC8C8) are not the house shade RGB(170,205,255). The brief allows group colours; this is Roger's decision (review item 15).

## Things worth knowing when teaching with it

- **Rossi results:**
  - 26.4% are re-arrested in 52 weeks, so no median is reached.
  - Aid: S(52) = 0.778. No aid: 0.694.
  - Log-rank χ² = 3.84, p = 0.0501. Gehan-Breslow χ² = 3.75, p = 0.0528.
  - HR (O/E ratio) = 0.692, 95% CI 0.479 to 0.999.
  - Peto HR = 0.692, CI 0.479 to 1.000 (1.0002).
- **The two approximations disagree.** The O/E-ratio CI just excludes 1 while p is just above 0.05; Peto's CI, which agrees with the test by construction, just includes 1. Page 1 shows both: a good moment to teach "report the p-value".
- **The two extra splits are clear-cut but observational:**
  - Priors 0-2 vs 3+: χ² = 12.42, p = 0.0004, HR = 0.52.
  - Age under 23 vs 23+: χ² = 11.10, p = 0.0009, HR = 1.87.
- **The life table ends at the last follow-up.** At width 4 for "all", the last interval is [48, 52]: 332 enter, 14 arrests, and the 318 followed to week 52 complete it. So n′ = 332, q = 0.0422 and S(end) = 0.7361, equal to KM's S(52). Beta 1 had a [52, 56) row with the 318 halved, giving 0.7271.

## DEVICE CHECKLIST (in order; the numbers are the harness's and SciPy/statsmodels')

1. **Paste and Check.** Paste SurvLab_beta1a.txt into the Connectivity Kit, replacing beta 1 rather than adding a second copy. Then Program Catalog → Edit → Check. Expect no syntax error. If there is one, note the line.
2. **FIRST: every page change clears the screen (review item 1).**
   - Go KM → CI, Band, Zoom, H(t) and back: no curve or text from the previous frame may remain.
   - Log-rank Next ×2: page 2 must not show page 1's text underneath.
   - Load a preset, then return to KM: a fresh plot.
3. **Run `SurvLab`.**
   - The opening page shows the orange DISCLAIMER panel.
   - Note how long it takes from the keypress to the menu: this is the Rossi fit on a G1.
   - The menu title reads "SurvLab: Rossi aid/none" and has 8 items.
4. **Kaplan-Meier plot.**
   - Note the time to the first frame (G1).
   - Blue and magenta steps, pale bands, lavender overlap, ticks at week 52.
   - At-risk rows: aid 216 210 201 194 181 170; no aid 216 208 196 180 170 155 (at 0, 10, …, 50).
   - The cursor starts at t = 26:
     - aid: S = 0.8981, CI 0.849 to 0.932, n = 194;
     - no aid: S = 0.8519, CI 0.797 to 0.893, n = 187.
   - Right ×4 gives t = 27, 28, 30, 31.
   - Drag a finger along the plot: the red line follows; note whether it is smooth on the G1. Past week 52 the readout says "past its last follow-up (52)".
   - Check that the long readout lines are not cut at the right edge.
5. **Soft keys.**
   - CI: the subtitle reads "95% CI linear". At t = 30, aid's CI is 0.852 to 0.935.
   - Band hides the bands.
   - Zoom: "zoomed: y from 0.60" in red, and the y labels run 0.60 … 1.00.
   - H(t): at t = 30, aid H = 0.1120, exp(−H) = 0.8940.
   - More, then Pool: one green curve "all". At t = 30, S = 0.8611 and n = 374, and the second line reads "13.9% re-arrested by t = 30 weeks".
   - More again returns to page 1.
   - Tap the title: "Band = 95% CI of S(t); ticks = censored times".
   - A light tap on each soft key should register.
6. **Median and quantiles.**
   - Median: the title "Median: time by which 50% are re-arrested"; all three rows "n.r.", plus the red explanation "aid: S(52) = 0.778; 22.2% re-arrested."
   - The bottom line reads "B-C CI from the log-log band; upper end not included".
   - 25%: title "Time by which 25% are re-arrested", heading "25th percentile (Q1): first time S(t) < 0.75"; aid n.r. (CI 46 to n.r.); no aid 44 weeks (CI 35 to n.r.); all 50 weeks (CI 43 to n.r.).
   - 10%: aid 24 (16 to 36); no aid 21 (14 to 26); all 23 (18 to 27).
   - CI → linear, then 10%: aid 24 (19 to 36).
   - Check that the CI bars and arrows draw cleanly.
7. **Compare groups: log-rank.**
   - Page 1: aid O 48, E 58.4, −10.4; no aid 66, 55.6, +10.4; V = 28.32; χ² = 3.84; p = 0.0501.
   - "HR = (O₁/E₁)/(O₂/E₂) = 0.692, CI 0.479 to 0.999".
   - "Peto: exp((O₁ - E₁)/V) = 0.692, CI 0.479 to 1.000" and "Peto's CI misses 1 exactly when log-rank p < 0.05".
   - G-B χ² = 3.75, p = 0.0528.
   - The green "no convincing evidence" verdict, the orange line "Borderline: the O/E-ratio CI and p disagree", and "HR assumes proportional hazards (no crossing)".
   - Tapping the bars names them.
   - Page 2: the pink tail beyond the red line at 3.84.
   - Page 3: "G-B 3.75 vs log-rank 3.84 (rule of thumb):" then "suggests the gap builds steadily".
   - Check that χ², ₁, ₂, ≥, ±, √ and H₀ render.
8. **Life table, width 4.**
   - 13 rows for aid. The first column reads "from-to": 0-4: 216 0 216 0 0.0000 1.0000; 4-8: 216 0 216 1 0.0046 0.9954; 8-12: 215 0 215 6 0.0279 0.9676.
   - Down shows the last row: 48-52, 174, 0, 174, 6, 0.0345, 0.7778 (= KM), with the orange line "Ends at 52: the 168 still followed then complete it".
   - Group cycles to "no aid" (last row 48-52, 158, 0, 158, 8, 0.0506, 0.6944), then to "all" (48-52, 332, 0, 332, 14, 0.0422, 0.7361).
   - Width 13, all: 0-13 S 0.9560, 13-26 0.8819, 26-39 0.8171, 39-52 0.7361.
   - Plot: the magenta life-table line over the pale KM line, ending at 52; the orange q bars. Tapping a bar names its interval ("[48, 52]: d = 14 of n' = 332, q = 0.0422"); a tap off the bars clears it.
   - Plot: the magenta life-table line over the pale KM line, and the orange q bars; tapping a bar names its interval.
   - Width 0 is refused; 0.25 is refused (more than 100 intervals).
9. **Load a preset.**
   - Priors: load page group 1 = 0-2 priors, n = 251, events = 51; red "SurvLab's split …" and "An observed grouping, not an experiment.". Log-rank p = 0.0004, red verdict.
   - Age: p = 0.0009, HR = 1.87.
   - All 432: Test gives the MSGBOX "One group only: no test."
10. **Use my data.**
   - Type 6 rows in Statistics 2Var:
     - C1 = 2, 4, 6, 8, 10, 12;
     - C2 = 1, 0, 1, 1, 0, 1;
     - C3 = 1, 2, 1, 2, 1, 2.
   - Run Use my data: the load page shows n = 6, events = 4, two groups.
   - Then clear C3: one group.
   - Then put 2 in C2: the refusal names the row.
   - With only one row in C1: "Need at least 2 rows; C1 has 1."
   - On a calculator whose Statistics 2Var has never been opened: "C1 holds no data yet."
   - With 400 rows (any times): "Reading and checking …", "Sorting and fitting …", then "Drawing N steps ... (Esc = no band)". Time each one; press Esc during the drawing, and the plot appears without the band and with "Band skipped (Esc)".
11. **Help.** 5 pages; Esc on page 2 leaves. Check that the help text fits inside the blue frame.
12. **Quit.** Home shows `SurvLab: Rossi, aid vs no aid, log-rank χ²(1) = 3.84, p = 0.0501, HR = 0.69` (or the current data's line). `SV_MED` = {−1, −1}, `SV_CHI` = 3.8375695…, `SV_HRP` = 0.69233…, `SV_T` has 49 values.

**Most likely to go wrong on a real G1:**
1. **Speed, still untimed.** In harness statements: the Rossi fit 17,190, the KM plot 6,219, the quantile page 3,296; 500 rows of your data, fit 68,756 and KM plot 54,280. A 500-row redraw is several seconds if a G1 runs about 10,000 statements a second; there is a busy page, and Esc skips the band. The fit itself cannot be stopped.
2. **The G2 cache.** `BLIT_P(G2, 0, 0, G1)` copies into G2; GaltonBoard's `BLIT_P(G2, 0, 0, G3)` is the device-run precedent. Each MOUSE move during a drag redraws the frame with two full-screen blits plus DRAWMENU.
3. **Real glyph widths.** Long readout lines, the life-table columns and some help lines may be cut at the right edge; the harness only estimates widths.
