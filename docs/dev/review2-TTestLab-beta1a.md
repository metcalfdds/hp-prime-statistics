# REVIEW2: TTestLab beta 1a (independent second review, 31 Oct 2026)

Reviewer did not write the program. Checked with own Python (SciPy 1.18 `t.isf/cdf/sf`, `ttest_ind_from_stats`,
`ttest_rel`, hand formulas, mpmath for the table), the PC harness `ppl_run_v3e` (routines called directly with
`h.execute`, full runs scripted with taps and keys, every page read back), `text_overlap_v1` over 409 distinct
screens, the kit linter (0 errors), `ppl_check_v4`, `lint_ppl`, `case_scan_v1`, `fleet_names_v2` over the four
programs (0 collisions, 0 untagged, 0 built-in matches), and the author's `verify_TTestLab_beta1a.py` re-run here
(59 PASS). Scratch files: `/home/claude/pv25g/review_ttl/chk1.py` (arithmetic), `chk2.py` (the t table and the
row rule), `chk3.py` + `chk3_out.txt` (every screen on every path), `chk4.py` (state after cancelled dialogs),
`chk5.py` (the curve's shading), `chk6.py` (the table-row line, number formats, the underflowing p), `chk7.py`
(2-dp vs 3-dp on the decision line), `chk8.py` (the examples' numbers), `rv.py` (shared setup).

One correction to the paperwork first: `TTestLab_beta1a_CHANGES.md` and the NOTES say "harness only", but Lessons
Learned v7zc (lines 12 and 24) records beta 1a compiling ("No errors in the program") and running example 1 to the
end on the Virtual Calculator, and reading DataLoad's lists (t(421.19) = −1.68). So the syntax questions below are
settled on the emulator; the findings are logic, state and wording.

## Findings, most serious first

### 1. Cancelling the α menu after choosing new tails leaves a one-tailed label on two-tailed numbers (CONFIRMED, harness)
- Lines 963–979 (`tt_AskTails`): `ttTL` is assigned at line 966, before the α `CHOOSE`; a cancelled α returns 0
  (line 978) with the new tails already committed. Lines 1125–1127 (`tt_Menu`): `tt_Calc()` runs only when
  `tt_AskTails()` returns 1, so nothing is recomputed.
- The case: example 1 → Menu → Tails and α → "One-tailed: μ₁ < μ₂" → α menu → Esc. Then step 3 reads "α = 0.050,
  one-tailed, df = 73", "exact, df = 73: t crit = −1.993", "Rule: if t obt < −1.993"; step 5 reads "Report t(73) =
  −2.20, p = 0.031, one-tailed", and the Home line on Quit is "TTestLab: t(73) = −2.20, p = 0.031, one-tailed".
  Right one-tailed values at df 73, α .05: t crit = −1.666, p = 0.0157. Every number on the screen is the
  two-tailed one under a one-tailed heading.
- Scenario in class: a student hesitates at the α list and presses Esc; the test is now labeled one-tailed and
  reports the wrong p, and copies it down.
- Fix: make the change atomic. In `tt_AskTails` hold the tails in a local and commit both together:
  ```
  at := IFTE(ak == 1,0,IFTE(ak == 2,-1,1));
  IF at == 0 THEN CHOOSE(aa,"α (two-tailed)",{...}); al := {...}; ELSE ... END;
  IF aa > 0 THEN ttTL := at; ttAL := al(aa); END;
  ```
  (the α list must then be chosen on `at`, not `ttTL`). Belt and braces: `IF ms == 2 THEN tt_AskTails(); tt_Calc(); END;`.

### 2. A refused D1/D2 read after a typed dependent summary leaves `ttSRC = 2` with `ttX1 = {0}`: the next page indexes past the end of the list (CONFIRMED, harness; on the calculator a run-time error, PLAUSIBLE)
- Lines 1019–1025 (`tt_AskData`, dependent, "Pairs in D1 and D2"): `ttSRC := 2` is set at 1019 before the size
  check at 1021 refuses and returns 0. `ttX1`/`ttX2` keep their old contents (the file-level initial `{0}` if no
  pairs were ever read). Lines 576–577 (`tt_Step1`) then read `ttX1(sj)` for sj up to `MIN(ttNP,7)`, and lines
  711–713 (`tt_Step4`) `ttXD(sj)` up to `MIN(ttNP,5)`, with `ttNP` still the typed count.
- The case: Choose the test → No (dependent) → OK → "Type mean, SD of differences" → 0.5, 1, 5 → tails → steps
  shown → Menu → Edit the numbers → "Pairs in D1 (x₁) and D2 (x₂)" with D1 empty → the box "Put the pairs in D1
  and D2 …" → menu returns → step 1 is drawn: the harness stops with `index 2 out of range in ttX1 (1..1)`.
  Neither Lessons Learned nor hp-prime-kit records what the Prime does with a list read past its end (the kit
  measured only `L(0)`, which answers the last element); a run-time error is the likely answer, and Lessons
  Learned §7 records that such a dialog opens the Program Editor and, from there, needed a reset. If instead it
  answers something, step 1 shows five "pairs" of stale values. Wrong either way.
- Scenario in class: a student who typed a summary, then tries the D1/D2 route before filling the lists, gets the
  helpful box and then a crash on the very next screen.
- Fix: assign `ttSRC` (and the names) only on success. Move `ttSRC := 2;` below the `IF SIZE(dl1) < 2 …` block,
  after `ttX1 := dl1; ttX2 := dl2;`. The same at line 1005 (independent raw scores) for tidiness, and line 1029
  (`ttSRC := 1` before a form that can be cancelled: after example 2 → Edit → Type → Cancel the state is
  consistent only by luck, because `tt_Pairs` had already filled `ttMD`, `ttSDv`, `ttNP`).

### 3. "Pooled or separate?" with refused numbers divides by zero (CONFIRMED, harness; the calculator's reaction PLAUSIBLE: an error dialog or ∞ on the page)
- Lines 766–777 (`tt_Compare`): no test of `ttOK`. Line 331: `(ca/ttN1)^2/(ttN1-1)` with N₁ = 1; line 322:
  `ttS1/cm` with both SDs 0 (cm = 0).
- The case: Choose the test → independent → typed N 1 = 1 (the rest 5, 2, 4, 2, 10) → "Each group needs N of at
  least 2." → the menu → Pooled or separate? → the harness stops with `division by zero` in `tt_Ind(2)`.
- Scenario in class: the refusal box sends the student to the menu, and the third item on it crashes.
- Fix: at the top of `tt_Compare`, after the dependent-samples box:
  `IF ttOK == 0 THEN MSGBOX("The numbers on screen give no t: Edit the numbers first."); tt_Settle(); RETURN 0; END;`

### 4. A p that underflows prints "p = 0.000" (CONFIRMED, harness; on the calculator when `STUDENT_CDF` returns 0 below 1E−499, PLAUSIBLE)
- Line 196 (`tt_FmtP`): `IF pv <> 0 AND ABS(pv) < thr THEN RETURN "< 0.001"`. A p of exactly 0 falls through to
  line 198 and prints "0.000". A true p is never 0; a returned 0 is an underflow, and Lessons Learned §3 says a
  probability prints "< 0.001", never "0.000".
- The case: dependent, typed x̄D 0.5, sD 1, N pairs 10,000 (d = 0.5, t = 50): the harness's doubles give p = 0 and
  step 5 reads "Report t(9999) = 50.00, p = 0.000, two-tailed". The Prime's reals reach 1E−499, so the same line
  appears once `STUDENT_CDF(df, −t)` is below that (about t ≥ 48 at large df; 2·t.sf(50, 9999) ≈ 1E−540). Two
  groups of 10,000 at d = 0.5 (t = 35.4, p ≈ 1E−265) still print "< 0.001" in doubles and would on the Prime.
- Scenario in class: a large-N data set (DataLoad can hold thousands of rows) reports p = 0.000, the one thing a
  statistics course tells students never to write.
- Fix: drop the first condition: `IF pv < thr THEN RETURN "< "+STRING(thr,2,pd); END;`. α never reaches the floor
  (its pd is 4 below 0.001), so `tt_AlS` is unaffected.

### 5. The decision line prints t to 2 decimals beside t crit to 3, so a retained t can read as beyond (CONFIRMED, harness)
- Line 746 (`tt_Step5`, retain): `"t obt = "+tt_Fmt(ttT,2)+" is not beyond t crit = "+tt_CritS(ttTC)`;
  `tt_CritS` (line 442) prints 3 decimals.
- The case: pooled, N 6 and 6, SDs 1, means 1.2852 and 0 (t = 2.2261 on df 10, t crit 2.2281 two-tailed .05):
  step 5 reads "t obt = 2.23 is not beyond t crit = ±2.228: RETAIN H₀." and "p = 0.050". Any t in
  (t crit − 0.005, t crit) does this.
- Scenario in class: the student reads 2.23 > 2.228 and concludes the program contradicts itself.
- Fix: 3 decimals on that line (`tt_Fmt(ttT,3)` at lines 736 and 746); keep 2 in the Report line (APA style).

### 6. A cancelled form or a refused read strips the example's names, outcome and step-4 note while keeping its numbers (CONFIRMED, harness)
- Line 995 (`tt_AskData`): `ttEX := 0; ttG1 := "Group 1"; ttG2 := "Group 2"; ttDV := "";` runs as soon as the
  source `CHOOSE` is answered, before the form (lines 999, 1031) or the D1/D2 read (1006, 1020) can fail.
- The case: example 1 → Menu → Edit the numbers → Type → Cancel: step 1 shows "Group 1 / Group 2" over 15.89,
  1.45, 44 … with no "Outcome:" line; step 4's gray note about the lecture's rounding is gone; `ttM1` is still
  15.89. The same after Choose the test → No → OK → Type → Cancel (`ttTY` is restored to 1, the names are not).
- Scenario in class: the age-at-arrest example turns anonymous after a cancel, and the lecture's −2.34 note the
  student was comparing with disappears.
- Fix: do the reset at the success points only (just before each `RETURN 1` path sets its own names), or save the
  four values at the top and restore them on every `RETURN 0`.

### 7. The independent form accepts a fractional N uncorrected (CONFIRMED, harness)
- Line 999: `INPUT({ttM1,ttS1,ttN1,ttM2,ttS2,ttN2}, …)` with no `IP()`, where the dependent form does
  `ttNP := IP(dn)` (line 1035). Line 391 refuses only N < 2.
- The case: N 1 = 10.5, N 2 = 10, means 5 and 4, SDs 2: `ttOK = 1`, df = 18.5, step 2 "= 10.5 + 10 − 2 = 18.5",
  the pooled t is reported as "t(18.5)", and the table row is 18. A typed N 1 = 1.5 is refused ("needs N of at
  least 2") although it is 2 after rounding, and 2.5 is accepted (df 2.5).
- Fix: after a successful form, `ttN1 := IP(ttN1); ttN2 := IP(ttN2);` (or refuse a non-integer with a reason).

### 8. When t crit lies past the window's cap there is no red region and no dashed line, but the page still says "Red = the rejection region (α)" (CONFIRMED, harness; the off-screen `LINE_P` is clipped on the calculator, PLAUSIBLE)
- Lines 481–483: `cxr := MIN(MAX(4, ttTC + 0.8), 12)`. Line 522: the dashed line's x is computed from `ttTC`
  without a clamp, so for t crit > 11.2 it lands off the GROB (x = −7691 and 8011 at df 1, α .001).
- The case: N = 2 pairs (df 1) at two-tailed .05 (t crit 12.706), or at .001 (636.619); df 2 at .001 (31.598).
  Step 3 draws a flat curve shaded all pale blue, nothing red, no dashed line, under "Rule: if t obt > 12.706 …
  reject H₀. Red = the rejection region (α)." Two pairs is a thing a student will try.
- Fix: when `ttTC + 0.8 > 12`, draw the dashed line at the window's edge (clamp as line 528 does for t) and add a
  line "(t crit lies beyond the window shown)"; or widen the cap for df ≤ 2.

### 9. A negative typed sD gets the "sD = 0" explanation (CONFIRMED, harness)
- Line 384: `IF ttSDv <= 0 THEN … "Every pair differs by the same amount (sD = 0): there is no t."`.
- The case: dependent, typed x̄D 1, sD −1, N 5: the box says every pair differs by the same amount.
- Fix: a separate `IF ttSDv < 0 THEN ttMSG := "An SD cannot be negative."` first, as line 392 does for the groups.

### 10. `tt_Pairs` divides by N − 1 before `tt_Calc` tests N < 2 (CONFIRMED by direct call; unreachable through the forms)
- Line 382 calls `tt_Pairs()` (whose line 351 is `(ttSSq/(ttNP-1))^.5`) before line 383's `IF ttNP < 2`. With
  `ttX1 = {5}`, `ttX2 = {3}`, `ttSRC = 2`, `tt_Calc()` stops with `division by zero`. The pairs form refuses
  fewer than 2 (line 1021), so no student path reaches it today; finding 2's fix touches the same lines, so order
  the guard first: `IF ttSRC == 2 THEN ttNP := SIZE(ttX1); END; IF ttNP < 2 THEN … END; IF ttSRC == 2 THEN tt_Pairs(); END;`.

### 11. Small text and layout items (CONFIRMED, harness, unless marked)
- Line 1089, help 1: "sample (or x₁) in D1, sample 2 (or x₂) in D2" — "sample 1" lost its 1.
- Lines 576–577: the pairs print as typed by `tt_Num`, so Table 11.3's 1.30, 1.00, 1.10 show as "1.3", "1",
  "1.1" beside "1.25" and "0.76"; a common decimal count per column (the most any value needs) would match the
  lecture's table.
- Line 756: "(Table row 120, ±1.980, would decide the other way.)" is 52 characters from x = 8: 320 px at 6 px per
  character, 346 at 6.5 (marginal: the device decides). Shorter: "(Table row 120, ±1.980, decides the other way.)".
  Likewise line 542 at α .0005: "Separate-variances t test, one-tailed, α = 0.0005", 49 characters (302 / 327 px).
- Lines 722–725: the dependent summary's step 4 has one line at y = 40 and the next at y = 141, a 100-px blank.
- Line 1030: the dependent form is prefilled with the last computed `ttMD`, `ttSDv`, `ttNP` (after example 2:
  0.182, 0.30622, 5), the computed-prefill pattern Lessons Learned §4 warns about; the independent form shows the
  previous example's numbers (e.g. 3.28798). "Edit the numbers" wants the current ones; "Choose the test" could
  start from flat defaults.
- Lines 1218–1221: Help from the start menu ends in example 1's step 1 with nothing saying so.
- Line 197: p = 1 exactly (t = 0) prints "p > 0.999"; "p = 1.000" is more honest for a t of 0.
- Line 218: `tt_Num` rounds a typed value to 5 decimals, so a typed SD of 0.000001 shows as "s₂ = 0" on step 1
  while the arithmetic uses it; `tt_Sig` prints 1E−11 as "0.0000000000" and 6E13 as "6ᴇ13" (step 2's a and b
  with such SDs). Extreme inputs only.

## Checked and found right
- **Pooled and Welch SE, t, df** (`tt_Ind`): 206 cases (random N 2–59, SD 0.01–20, plus N = 2, one SD 0, N 2 vs
  1000, N 1000 vs 10,000) against my own formulas, worst relative difference 6.6E−16; the scaling by the larger SD
  gives the right Welch df when one SD is 0 (s₁ 0, s₂ 3, N 10/10: df 9, SE 0.9487).
- **Paired t** (`tt_Pairs` + `tt_Calc`): 20 random sets, N 2–50, against `ttest_rel`, worst 1.8E−15; identical
  differences and all-zero differences refused with the sD = 0 message; N = 2 pairs with t = 0 gives t(1) = 0.00.
- **p values** (`tt_PVal`): 270 (df, t, tail) combinations, df 1 to 10,000, t −50 to 40, all three tails, equal
  to SciPy to the last digit; lower tails only (`2*STUDENT_CDF(df,-|t|)`, `STUDENT_CDF(df,t)`,
  `STUDENT_CDF(df,-t)`), no `1 −` anywhere; H₁ μ₁ < μ₂ uses the lower tail and rejects below −t crit, μ₁ > μ₂
  the upper; sign is group 1 minus group 2 throughout (`tt_Ind`, `tt_Pairs`, Cohen's d, "sample 1 (…) is lower").
- **t critical** (`tt_Crit`): every α the program offers, both tails, df 0.5, 1, 1.5, 2, 3, 4.6, 7.5, 29.6, 30,
  60, 73, 120, 265.924, 1000, 10,000, 1E6: 288 values equal to `t.isf` to the last digit; `STUDENT_ICDF` is only
  ever given α/2 or α (0.0005–0.1), never p near 0 or 1; the fallback's bracket cap (1E6) cannot bite because the
  Welch df is at least min(N₁, N₂) − 1 ≥ 1.
- **Decision logic**: on a grid of 4 df × 18 (tail, α) × 9 t values, `tt_Beyond` and "p < α" never disagree
  except at t exactly critical, where both retain (strict inequality, as the lecture's rule reads); exact and
  table decisions are compared and the "(Table row …, would decide the other way.)" line appears when they
  differ (t = −1.975 at df 265.92: exact 1.969 rejects, row 120's 1.980 retains).
- **The row rule** (`tt_TabDF`): 27 df values; ties go to the smaller row (1.5 → 1, 35 → 30, 50 → 40, 90 → 60),
  30.001 → 30, 35.01 → 40, 90.01 → 120, 121 and 999 → 120, 73 → 60 as the NOTES quote the lecture.
- **The printed table**: all 198 cells against `t.isf` rounded to 3 decimals; exactly the five the author lists
  differ (rows 2, 3, 5, 7, 23 of the last column: 31.598 / 31.5991, 12.941 / 12.9240, 6.859 / 6.8688, 5.405 /
  5.4079, 3.767 / 3.7676). These are the classical Fisher–Yates .001 column that most textbook tables copy (from
  memory, not checked against that source), so they are the lecture's table's values, not transcription slips.
  `ttTB` equals the printed figure in all 198 cells, both tails; the step-3 note appears only in the five cells.
- **The examples**: age at arrest sp² 1.74480, 75/1364 = 0.054985, SE 0.30974, t −2.1954 (lecture −2.34 via
  √1.74 × √.05 = .29), p 0.0313, t crit 1.993 (row 60: 2.000), d −0.515, reject; matched jails differences
  0.30, 0.49, −0.13, −0.16, 0.41, x̄D 0.1820, SS 0.37508, sD 0.30622, SE 0.13695, t 1.3290 (lecture 1.29), p
  0.8727 one-tailed, t crit −2.132, retain, "differ the other way from H₁"; drug use SE 0.36918, t −4.3507
  (SPSS −4.351), df 265.924, p 1.9E−5, pooled t −4.5237 on 414 df, d −0.465. The step-4 notes name the lecture's
  rounding and give the exact value; they show only while the example's own test is on screen.
- **The curve** (`tt_Curve`): column by column in all three tail settings, pale red exactly where t is beyond
  t crit on the H₁ side(s), magenta exactly on the p area (|x| ≥ |t| two-tailed; x ≤ t or x ≥ t one-tailed),
  dashed line(s) at the right pixel on the right side(s) only, t-obt line at the right pixel, window widened
  (cxr 5.87) when t = 5.07.
- **Touch geometry**: the four tested rectangles equal the drawn boxes (Q1 Yes 60–120 × 62–80, No 200–260;
  Q2 Yes 10–70 × 124–142, No 110–170); the strip formula is §6's; Back undoes one answer; OK before an answer does
  nothing; Esc leaves; Enter = OK. Soft keys 1–5 and Left/Right move between steps, 6 and Enter open the menu.
- **D1/D2**: 7 and 10 scores (pooled t 3.3067 = SciPy), 14 and 10, 12 pairs ("… and 5 more pairs", the outcome
  line under them), D1 of one value and D2 of one value refused, unequal pair counts refused, D1 absent refused
  (IFERR → {}). Speed: `tt_MSN` and `tt_Pairs` are two passes of 2 statements, about 0.7 s per 1,000 values on a
  G1 at 0.17 ms per statement; each curve page is 297 columns × ~15 statements + 297 `STUDENT` calls, about 1 s.
- **PPL**: no `!=`, no `//` inside an open bracket (E12 0), no `LOCAL` over 6 names or mid-block, `STRING(x,1,0)`
  only on integers (14 sites), every `CHOOSE` tested on its index, both `INPUT`s tested on their return, no
  `FREEZE`, no `WAIT`, drains (`tt_Settle`) after every form, menu and box, the capped finger drain of §7, no
  non-ASCII outside strings (E5 0), only verified glyphs (± ² × α μ ₁ ₂ √ ≠ and CHAR 57344), `CHAR(34)` for
  quotes, `DOWNTO` (line 216) measured by hp-prime-kit on the Virtual Calculator, 45 routines all `tt_`, 51
  file-level variables all `tt`, no name matching a built-in ignoring case, no collision with DataLoad, PowerViz or
  TestChooser.
- **Wording**: "REJECT H₀" / "RETAIN H₀", never "accept"; "no support for H₁"; the compare page's direction of
  the pooled test's error is right (smaller group with the larger SD → rejects too often; the reverse → too
  cautious), and "same t either way" holds when N₁ = N₂ or s₁ = s₂; Cohen's d uses the pooled s for both
  independent tests (§12) and x̄D/sD for pairs.
- **Layout**: `text_overlap_v1` over 409 distinct screens from every path: no firm overlap, straddle or overrun;
  the only marginal items are those in finding 11 and lines produced by extreme inputs (t = −3,904,046,174).

## Could not check here
- The lecture note itself: whether its "closest row" rule is what it does between 30 and 120 and below 30 for a
  fractional df (TTestLab's tie rule is the author's choice); where its ".38" comes from (each squared deviation
  rounded to 2 decimals gives .38; the exact sum is .3751); how Table 11.3 prints 1.30 / 1.00 / 1.10; which
  separate-variances formulas it teaches (TTestLab uses Welch's).
- On the calculator: what `STUDENT_CDF(9999, −50)` returns (0 or a denormal), which decides whether finding 4
  shows; what Home does with x/0 inside a program and with a list read past its end (findings 2 and 3 are wrong
  states either way); whether `LINE_P` at x = −7691 is clipped silently (finding 8); the width of 49–52
  characters of font 1 (finding 11); the glyphs μ₁ ≠ μ₂ inside `CHOOSE` items (lines 963, 991; none of the three
  fleet programs supplied here puts a glyph in a menu item); a non-numeric element in D1 (the Statistics app should not allow one).
- The Prime's Inference app (checklist 10 in the NOTES).

## Device checklist additions
13. Example 1 → Menu → Tails and α → one-tailed μ₁ < μ₂ → Esc at the α list: step 3 must still show the
    two-tailed heading, or (after the fix) "t crit = −1.666" and "p = 0.016, one-tailed" on step 5.
14. Dependent samples typed (0.5, 1, 5) → Menu → Edit the numbers → Pairs in D1 and D2 with D1 empty: after the
    box, step 1 must draw without an error dialog.
15. Independent, N 1 = 1 typed → the refusal box → Menu → Pooled or separate?: no error dialog, no ∞.
16. Dependent typed x̄D 0.5, sD 1, N pairs 10000: step 5's Report line must read "p < 0.001", not "p = 0.000";
    note what Home gives for `STUDENT_CDF(9999,-50)`.
17. Dependent, 2 pairs in D1/D2 (1, 2.5 and 1.5, 2) at α .05: step 3 with t crit ±12.706 — what the curve shows
    (expect no red and no dashed line until finding 8 is fixed), and that nothing is drawn wrongly elsewhere.
18. Pooled, N 6/6, SDs 1, means 1.2852 and 0: step 5 reads "2.23 is not beyond ±2.228" (before the fix).
19. The Tails menu's items show μ₁ ≠ μ₂, μ₁ < μ₂, μ₁ > μ₂ (glyphs in a CHOOSE list; not seen in the three programs supplied).
20. Step 5 with t = −1.975 at example 3's N and SD (type mean 2 = 5.5476): the "(Table row 120, ±1.980, would
    decide the other way.)" line fits the screen whole.
21. Step 1 at one-tailed α .0005: the heading "Separate-variances t test, one-tailed, α = 0.0005" fits whole.
22. The tick labels under the curve print the Prime's minus (−4 … 4) and "−12 … 12" when the window is capped.
