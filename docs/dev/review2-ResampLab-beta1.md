# ResampLab beta 1: second review (independent)

21 Oct 2026. Reviewer: Claude (independent second reviewer; did not write the program).
File reviewed: `/home/claude/new6/ResampLab_beta1.txt` (2,722 lines), not edited.
My scripts: `/tmp/claude-0/-home-claude/6157958e-03ce-51f4-bf77-e038db8d37e9/scratchpad/rev2_resamp/` (`p1`..`p10`, `common.py`). Harness: `ppl_run_v3e.py`, HPKIT = hp-prime-kit-HEAD. Reference values come from my own Python (itertools, Fractions with decimal parsing, numpy, SciPy 1.18.1), not from the builder's verify script.

Tags: **CONFIRMED** = reproduced here (in the harness or by reading the data). **PLAUSIBLE** = follows from the code and the Lessons Learned, but needs the device to settle.

---

## Findings, most serious first

### 1. A MSGBOX opened from a soft key leaves its key behind, so the Actions menu pops up (CONFIRMED in the harness's stale-key model)
**Lines 2449-2475** (lab loop). The keys are drained only on the key path (line 2469), and that happens *before* `rs_Do`. When an action opens a MSGBOX, the Enter that closes it is still in the buffer. The next pass of the loop reads it at line 2450 and opens `rs_KeyMenu`. Actions that open a MSGBOX from the lab page:
- Exact on MockJury or Rossi (both presets; `rs_Exact` line 1833);
- CIs or BCa with B < 100 (lines 2061, 2120);
- a run at the 9,000 maximum (1870, 1922).

**Scenario:** load MockJury, tap More, then Exact. The "C(76, 37) = ... too many to list" box appears. Press Enter, and the "Actions" CHOOSE opens without being asked for. Harness `stale_keys=True`: chooses = [..., 'Actions', ...], and stale_skips logs "a wait loop in rs_Lab ended on the key left over from the last dialog". If the box is closed with a finger instead, the finger can still be down when the loop's MOUSE poll runs, and a tap at y ≥ 169 opens the Info or CIs page.

**Fix:** at the top of the `WHILE lbGo == 1` body, or right after `rs_Do(lbA)`, add:
```
REPEAT lbK := GETKEY; UNTIL lbK == -1;
rs_Drain();
```

### 2. The jackknife is O(n²), with no progress display and no Esc, and up to 999 values are accepted (CONFIRMED harness time; G1 time PLAUSIBLE)
**Lines 913-917** (`rs_BtStart`). For each i the code builds a MAKELIST of n − 1 values, and for the median and trimmed mean it also sorts them. `rs_Mine` accepts up to 999 values (line 2558). `rs_BtStart` runs on opening the page, on every Stat press and on every Stat change.

Harness times: n = 999 took 19.3 s (mean) and 12.3 s (median); n = 200 took about 0.9 s. At the brief's ×30–100 for a G1, that is 10–30 minutes at n = 999 and 30–90 s at n = 200. The screen shows nothing and Esc does nothing, so in front of a class it looks frozen.

**Fix:**
- Use the closed forms: mean J_i = (S − x_i)/(n − 1); the median of the sorted x with one value removed is x(m) or x(m+1) according to which side i is on; the SD comes from leave-one-out sums. Only the trimmed mean then needs a loop.
- Or show a progress bar with Esc, as `rs_PmExact` does.
- And/or cap the one-sample n for BCa (for example, BCa only for n ≤ 200).

### 3. `COMB(N, k)` overflows for large user groups (PLAUSIBLE; the harness stops with Unsupported)
**Line 742**: `rsXC := COMB(rsN, rsK)`. C(2m, m) passes 1E500 at m ≈ 835 (log10 C(1670, 835) = 501). Both lists may hold 999 values, so 835 v 835 and larger reach this.

Lessons §3 says an overflow returns +∞ with no error. In that case `rs_Big(∞)` at line 744 takes LOG(∞) and computes ∞/∞, which may be a runtime error (the Program Editor opens) or garbage text. The harness run of 900 v 900 stopped in `rs_PmStart` ("COMB(1800, 900) ...").

**Fix:** only "is it ≤ rsExLim?" is needed. Build C(N, k) term by term and stop as soon as it passes 2,000. For the message, use log10 C from a sum of LOGs ("about 10^540 splits").

### 4. During a bulk bootstrap run, the 2-second redraw recomputes every interval, so the 60-second cap does not hold (PLAUSIBLE; harness ratio CONFIRMED)
**Lines 1656-1657, 1515-1516, 1588.** `rs_Busy` redraws through `rs_DrawHist(0)` and `rs_DrawStat()`. Both call `rs_BtCI()`, and because rsB has changed since the last redraw, the cache misses every time. Each miss copies, sorts and makes two passes over all B values.

In the harness, one `rs_BtCI` at B = 4,000 costs 0.126 s, the time of about 97 resamples (0.0013 s each); at B = 9,000 it is about 230 resamples. On a G1 that is 4–13 s per redraw, repeated every 2 s of work. The cap is set from the first 20 items, before any redraw, so a run "capped at about 60 s" can take 3–7 times as long once B is large. The "s left" estimate is wrong for the same reason.

**Fix:** during a run, have `rs_Busy` draw the histogram without the interval bars and status intervals (pass a flag, or set a global so `rs_DrawHist`/`rs_DrawStat` skip `rs_BtCI`). Compute the intervals once, at the end of the run.

### 5. An absolute tie tolerance gives p = 1 on small-scale data (CONFIRMED)
- **Line 738** `rsEps := 1E-9 * (MAX(|x|) + 1)`; also lines 835, 944 and 984.
- **Line 401** (`rs_Grid`): `ABS(gdV - ROUND(gdV, 0)) > 1E-6 * MAX(1, ABS(gdV))`.

Both tolerances are absolute below 1.

Two-group example: A = {1, 2, 3, 4, 5}×1E-10, B = {6..10}×1E-10. Exact |d| ≥ |obs| gives 252 of 252 (p = 1). The true count is 2 of 252, and the same data ×1E10 gives 2. Paired example: d = {1, 3, 2, 4, −1}×1E-10. `rs_Grid` takes these as whole numbers (f = 1, every a_i rounds to 0), so every pattern ties: 32 of 32.

**Fix:**
- `rsEps := 1E-9 * MAX(ABS(rsV(1)), ABS(rsV(rsN)))`, with a floor such as 1E-300.
- In `rs_Grid`, use a relative test and refuse when `ROUND(gdV, 0) == 0` for a nonzero value.

### 6. The Darwin source line says "15 pairs, one pot each", which is wrong (CONFIRMED)
**Line 2528**, shown on the data page and on Info page 2. `data/HistData_ZeaMays.csv` has a `pot` column with values 1–4 (3, 3, 5 and 4 pairs); Darwin grew the pairs in four pots. This is a factual claim on screen (Lessons §14 rule 16).

**Fix:** "sec. 21 (15 pairs in 4 pots)."

### 7. "= < 0.0001" on screen and in the Home summary (CONFIRMED)
- **Lines 1556, 1570, 2020, 2424**: e.g. `"exact p = " + c + "/" + C + " = " + rs_PStr(...)`.
- **Line 2014**: the Info page's "give or take √(p(1 − p)/B) = " + rs_PStr(...).

Reproduced with D1 = 1..15 on the paired page:
- "exact p = 2/32,768 = < 0.0001";
- the Info page's "p = 2/32,768 = < 0.0001.";
- Home: "... exact p = < 0.0001".

The Info page shows "give or take ... = < 0.0001" whenever p is 0 or 1. The fleet removed "= <" on 18 Oct (Lessons v7j).

**Fix:** have `rs_PStr` return "< 0.0001" and let the callers drop the " = " when the value starts with "<". For SE = 0, write "0".

### 8. Text-page paragraphs can run into the footer (CONFIRMED with user data)
**`rs_Para` (1969-1995)** has no bottom limit, and the footer is at y = 222.
- Paired Info page 1 (heavy ties D1 = {1,1,1,2,2,2,2,1}, D2 = {1,2,2,2,2,2,1,1}): its last line "none)." is at y = 220, overlapping "Any key = page 2".
- BCa page with large values: "Ties count half ..." at y = 216.
- The Darwin and MockJury pages already reach y = 208, so longer counts or names can push them into the footer.

**Fix:** have `rs_Para` stop at y ≤ 208 (or start a second page). Shorten the "Meaning" paragraph.

### 9. The exact-by-sums limit is generous, and the 60-second cap does not cover it (PLAUSIBLE)
**Lines 840-841** allow n ≤ 39 and Σ|d|f ≤ 9,998. The worst case allowed (n = 39, Σ = 9,998) took 4.4 s in the harness, against 0.27 s for Darwin; on a G1 that is about 2–7 min. Esc is read once per pair, and the closing 10,000-step `rs_XAdd` loop (1794-1799) has no Esc check.

The arithmetic is right: 2^39 < 1E12, so the counts are exact; I got 23,860,599,080 of 549,755,813,888.

**Fix:** limit by work, n·Σ ≤ about 20,000 (Darwin is 15 × 544 = 8,160), or apply the TICKS cap. Add an Esc check to the final loop.

### 10. Lab-page lines likely clipped at their width (PLAUSIBLE; estimated at 6.5 px per character, Lessons §6/ChiTable measure)
- **1570**: Darwin with Ha A < B, "exact p = 31,933/32,768 = 0.9745 (Exact, on More)" is 50 characters, about 325 px in a 312-px field.
- **1596**: "BCa: a is undefined (every jackknife value is equal)" is 52 characters. It shows whenever the bootstrap median of an even n has tied middle values.
- **2299-2310**: tap notes such as "-0.250 to 0.000: 354 shuffles (354 in tail)" are 43 characters, about 280 px in 266.

**Fix:** shorter wording, e.g. "exact p = 31,933/32,768 = 0.9745", "BCa: a = 0/0 (jackknife all equal)", "-0.250..0.000: 354 (354 in tail)".

### 11. INPUT help lines are 62-63 characters; the longest in the fleet is 43 (PLAUSIBLE)
**Line 2620.** These will very likely be cut on the device. **Fix:** "0 = fresh; a whole number repeats a run" and "0.5 to 0.999 (0.95 = 95%)".

### 12. Long MSGBOX texts (PLAUSIBLE)
Lines 812 (130 characters), 2555 (115) and 845 (about 120 with numbers). The harness's 5-line check counts only "\n", so it cannot see wrapped lines. The fleet's longest that ran on the emulator is NormExplorer's 120. **Fix:** keep each under about 100 characters.

### 13. A bootstrap tap reports a stale "picked k times" (CONFIRMED)
**Lines 2353 and 2361.** After x100 with no Once, the top panel shows the sample, yet a tap on a value says "155 months: picked 0 times". After Once followed by x1000, the tap reports the Once's picks, which are no longer shown. **Fix:** when `rsShP == 0`, say "value 155 months (in the sample)".

### 14. The one-sample bootstrap does not say what it resamples (CONFIRMED)
**Lines 1411-1413 and 1579.**
- On Darwin the page reads "sample mean = 2.62 (n = 15)". These are the cross − self differences, and nothing on the page says so.
- On two-group data it resamples group A only, without naming it.
- With "Use my data" and lists of equal length it resamples D1, not D1 − D2. Darwin resamples the differences, so the two are inconsistent.

**Fix:** label it ("differences cross − self", or "group A (Unattr)"), and set `rsBoot1` the same way in `rs_Mine`.

### 15. The paired page describes the wrong mechanism (CONFIRMED)
**Lines 1562-1563** show "Each shuffle deals the labels again at random" in mode 2 too. For the paired test it should read "Each shuffle flips each pair's sign at random, as if H₀ were true."

### 16. Claims not checked against sources (PLAUSIBLE)
- **Line 2045** says "Fisher (1935, sec. 21) counted these by hand." That is a historical attribution with no page cited; say "worked this test on these data" or check the book.
- **Lines 100-101 and 2184** credit "the TI 'Resampling' activity". Nothing of that name is in `ref/triola_ti_programs/` (grep for resampl or shuffl finds nothing).
- **Line 84**: Triola "(about p. 393)" is unverified.

The BOOT and RANDSAMP claims are correct (checked against `BOOT__133.txt` and `RANDSAMP__333.txt`).

### 17. Seeded runs repeat only on calculators of the same speed (CONFIRMED by logic)
**Line 2178** (Help) says "a class pressing the same keys sees the same run". The TICKS cap (1893-1899) cuts the run at a number of draws that depends on the speed of each calculator, so a G1 and a G2 with the same seed can stop at different B and show different p. **Fix:** say so in Help, or make the cap a whole number of x100 blocks and note it.

### 18. Smaller items (CONFIRMED by reading)
- **1930:** in paired mode the animation is gated by `rsN`, which is the two-group N left over from an earlier page. Use `rsNd` in mode 2.
- **2101:** `LEFT(cpL, 5)` draws "perce", which reads as a typo; use "pct".
- **2110:** "Wide disagreement: a skewed, lumpy statistic" is always shown and reads as a verdict; write "If they disagree widely: ...".
- **2170:** Help says "the middle 95%" even after Level has changed.
- **2697:** the CHOOSE title is cut mid-word ("Rossi: week of first a").
- Lab pages have no key legend (+ = Once, Ent = menu, Esc = back); only Help mentions the keys. The brief's footer style is not applied there; there is no room, so a short line in the status block is an option.
- **NOTES** (not the program) give the Darwin Σ|d|×8 as 536; it is 544.

### 19. The two-sided convention differs from SciPy (information, not a bug)
The program counts |d| ≥ |obs|, and the Info page says so. `scipy.stats.permutation_test` defaults to 2·min(one-sided). They agree for the symmetric 5 v 5. They differ for unbalanced or tied designs:
- 2 v 9: 24/55 (0.436) against 26/55 (0.473);
- the ties set {1,1,1,2,2,2} v {1,2,2,2,3,3,3}: 133/1716 (0.078) against 0.132.

Keep the |d| rule (it is Pitman's and the textbooks'), but state in the NOTES that it is not SciPy's default.

---

## Checked and found correct

- **Device rules**:
  - pure ASCII;
  - every LOCAL line has 6 names or fewer, all at the top of their block;
  - no name matches a built-in when case is ignored, none differs from another only in case, and none spells rsolve;
  - no `//` inside an open bracket;
  - capital-E literals; CHOOSE index tested, never its return value; no numbered menu items;
  - INPUT into LOCALs; ROUND before STRING everywhere (`rs_Fmt`), and no `ᴇ` in any run (one at −1E12 with absurd user data);
  - GETKEY codes 4, 30 and 50 only; touch read only after `SIZE > 0`; finger-lift drains capped by TICKS;
  - Esc is read in the exact loops (every 25 or 32 items) and in bulk runs (every 10);
  - RETURN, no PRINT.
- **List arithmetic:** a static scan finds no `+`, `-`, `*` or `/` with a list operand. Every menu path below ran under the harness that refuses list `+`, with no error.
- **RANDSEED:**
  - in `HP_Prime_Builtin_Names.txt`; BlackJack.hpprgm in the library uses it in a PPL program; hp-prime-kit measured repeat-on-reseed on the emulator. So the IFERR line will paste.
  - IFERR cannot catch a compile error from an unknown name, so the NOTES' fallback ("delete the line") is the right advice.
- **RANDOM:**
  - `MIN(n, 1 + IP(RANDOM·n))` and the Fisher–Yates `MIN` guard keep the index in range if RANDOM ever returns 1. The bias at 0 or 1 is about 1E-12.
  - `RANDOM < 0.5` is fair.
  - `MAKELIST(RANDOM…)` is evaluated once per element (library: minehunt, Schrausser `MAKELIST(RANDOM,A,1,B)`).
- **TICKS:** differences only, and the wrap is guarded (`ruNow > ruT0`). A wrap after about 50 days of uptime would only freeze the "s left" text.
- **12 digits:** the Darwin counting route never passes 2^39 = 549,755,813,888 < 1E12. COMB fits for every preset (Rossi C(114, 48) ≈ 3.8E32).
- **Presets:** identical to the CSVs.
  - MockJury Unattractive 37, Beautiful 39, Average 38;
  - Rossi aid 48, no aid 66 (arrest = 1);
  - Darwin 15 pairs, eighths 49, −67, … (Σ 544);
  - BJS 41 values;
  - 5 v 5 labelled illustrative.
- **Exact two-group:** 16 designs × mean and median, in decimal-exact Fractions, all equal to the program. They cover 5 v 5, two kinds of heavy ties, decimals with floating ties, negatives with unequal n, 2 v 2, 2 v 9 and a 1,000,000 outlier. The histogram sums to C every time.
- **Exact paired:** equal to `itertools.product` on 7 designs: Darwin 1,726 / 863 / 31,933 of 32,768; zeros; ties; off-grid floats by the Gray route at n = 10 and 12; n = 2; and n = 20 on the grid (1,048,576).
- **Monte Carlo:** an independent replay of the harness's RANDOM stream gives identical counts (≥, ≤, |≥|) on 5 v 5, MockJury and Rossi (mean and median each) and on Darwin's flips. RS_P = (c + 1)/(B + 1) exactly.
- **Bootstrap (one sample):** θ* is identical to numpy on the replayed indices. Percentile, basic and BCa equal `scipy.stats.bootstrap` given the same resamples, max difference 2.9E-14, over 7 data sets × 4 statistics × 2 levels.
  - z₀ counts ties half, which is SciPy's `_percentile_of_score` convention (TI BOOT counted ≤).
  - a = Σ(J̄ − Jᵢ)³/(6[Σ(J̄ − Jᵢ)²]^1.5), as SciPy.
  - BCa is refused exactly where SciPy returns NaN.
  - The t interval equals `scipy.stats.t.interval`.
- **Bootstrap (two groups):** θ* identical; percentile and basic exact; Welch equals `ttest_ind(equal_var=False).confidence_interval`.
- **Awkward sets through the menus:** all equal (two-group and paired); n = 1 per group; 2 v 1; heavy ties; a group of size 0; D2 only; n = 3. Each is refused with a clear message or runs, with no runtime error.
- **Teaching:**
  - the plus-one rule is explained correctly ("the observed split is itself a possible split", Phipson & Smyth 2010);
  - a p-value is stated as P(this extreme | H₀), and a large p as "no evidence of a difference (not proof of none)";
  - Fisher's own Darwin figure is not claimed ("not checked here");
  - the Rossi caveat (only those arrested) is on screen.
- **Style:** the header matches the brief (DISCLAIMER, AI credit, sources, data, replaces, file map with correct line ranges); the disclaimer is on the opening page and Help page 5; the `rs_` tag is on every routine and `RS_` on every export; the house palette is used; the text-page footers are dodger blue.
