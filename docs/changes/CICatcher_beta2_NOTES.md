# CICatcher beta 2: notes

*16 October 2026. Built on beta 1 and keeps every beta 1 feature. **Not yet run on hardware** (nor has beta 1), and **nothing about the CAS has run on our calculators**. Pure PPL: 1,931 lines, 69,239 bytes, 63 routines (beta 1 had 51). Tag `cq` (glued style).*

Files:
- `CICatcher_beta2.txt`: the program. Made from beta 1 by 21 counted, exact replacements (`make_cq2.py` in the session scratchpad). The shared exact-interval routines are **copied programmatically from EpiStats v1.7**, so they cannot drift apart.
- `verify_CICatcher_beta2.py` → `verify_CICatcher_beta2_output.txt`: **PASS, 49 checks, 0 failures.** It also runs beta 1's own suite (71 checks) against beta 2.
- `cicatcher-guide_beta2.md`: the user's guide.

## 1 · What changed (beta 1 line numbers → beta 2)

| # | Item | beta 1 | beta 2 | What |
| --- | --- | --- | --- | --- |
| 1 | Header | 4, 16-25, 77-105 | 4, 16-55, 107-145 | beta 2 banner; firmware ("nor has beta 1"; run CASProbe first); a dated beta 2 paragraph; "THE FIVE INTERVALS"; the exact pivot and catch level in "HOW THE COUNTS ARE KEPT"; companion files beta 2 |
| 2 | State | after 189 | 225-234 | `cqXCat` (catch level per count), `cqXLo`/`cqXHi`/`cqXLv` (the ends per count and the level they belong to), `cqBinOK`, `cqCasOK`, `cqCasT`, `cqCasK` |
| 3 | **The CAS kit** | — | `cqIStr` 469, `cqCas` 488, `cqTimes` 513 | BRIEF_CAS's shapes with the coordinator's update: one surrounding pair of `"` is stripped. The kit parameter `xxN` is `cqIN` here, because `cqN` is already the sample size. One line is added: `cqCas` sets `cqCasOK`. `cqTimes` shows `*` as `×`. |
| 4 | **The exact interval** | — | `cqBinCheck` 536, `cqCPB` 550, `cqCPInt` 606 | **The same lines as EpiStats v1.7's `es_BinCheck` / `es_CPB` / `es_CPInt`**: bisection on `BINOMIAL_CDF(n, p, k)` with a Newton step (slope n·`BINOMIAL(n−1, p, k)`) when it lands inside the bracket, closed forms at k = 0 and k = n, a relative 1E-9 stop. The verify script compares the two files line for line (80 lines). |
| 5 | **Coverage kept exactly** | — | `cqXBuild` 628 | The Exact interval for count k contains p at level L exactly when min(P(X ≥ k), P(X ≤ k)) under p ≥ (1000 − L)/2000. So its catch level is CEILING(1000·(1 − 2·min)), kept to 500..1000. That is a table of n + 1 values per run, at 2 BINOMIAL_CDF calls each. `cqCatch` (770) looks it up, so +50 costs no search at all. The beta 1 machinery (`cqHist`, `cqSetLevel`, `cqVisHits`) is unchanged and makes the long-run count follow the slider exactly. |
| 6 | **The ends drawn** | — | `cqXGet` 648; `cqLimits` 732 | The ends at the current level, cached per count. At a new level each end is solved again from where it was (9 BINOMIAL calls per count per level step, on average), so a drag re-solves only the counts on screen: about 6 different counts at p = 0.10, n = 20. In `cqLimits` and `cqCatch`, Wilson's `DEFAULT` branch became `IF cqType == 4`, and `DEFAULT` is Exact. |
| 7 | Setup | 1181-1186 | 1538-1550 | A fifth CHOOSE item, "Proportion: Exact (Clopper-Pearson)". If `cqBinCheck` failed at start, Exact is refused with a message ("Exact is off") instead of drawing wrong intervals. |
| 8 | Reset, desc, init, loop | 566-581, 669-681, 1452-1455, 1466-1467 | 908-913, 1018-1020, 1847-1849, 1862 | The Exact tables are rebuilt in `cqReset` (per run). The header reads "Exact, p = 0.10, n = 20". The BINOMIAL check runs at start. `cqCasPanel()` runs before each main-loop frame. |
| 9 | **The CAS's one job** | — | `cqCFKey` 670, `cqCasPanel` 687, `cqCFDraw` 707; panel 1211-1305 | When the picked line is an Exact interval for 0 (or n) "yes" answers, the panel's first line, in place of the all-white (or all-black) tiles, is the closed form of the end: `upper = 1-(1/40)^(1/20) = 0.1684` with "exact (CAS)". The template is `1-(50/2000)^(1/20)`, so the CAS reduces α/2 = (1000 − L)/2000 itself. It is asked **only on events**: by the main loop before a frame, never inside the slider drag, the line-browsing drag or the +1 animation, and cached by (end, n, level). Inside a drag the panel shows `upper = 1 - (α/2)^(1/n) = …` with "decimal". If the CAS fails, that decimal line stays, with no error. |
| 10 | **Help page 4 (new)**: "Exact intervals: never below" | — | 1715-1732; `cqXEngS` 1643 | Why exact is conservative, with the verified numbers. The help now has six pages (beta 1: five). |

**What the CAS does here, honestly:** only the closed form for 0 or n "yes" answers, as the brief asked. Nothing else in CICatcher has an exact or symbolic answer worth the CAS: the bounds for 0 < k < n are numbers, so PPL computes them (BRIEF_CAS rule 8). The idea *not* built, because it was not asked for and belongs to ErrorRate Lab, is the limit n·(1 − (α/2)^(1/n)) → −ln(α/2) = ln 40 = 3.69: the two-sided "rule of three".

**No "More" key:** the six soft keys are unchanged, and the new interval is chosen in setup.

## 2 · Verification (`verify_CICatcher_beta2.py`: PASS, 49 checks, 0 failures, 125 s)

```
A. the program's own cqCPInt / cqCPB in ppl_run_v3
   cqCPInt vs statsmodels proportion_confint(method='beta'): 3,798 intervals (n 5-30, 50, 100;
     every k; 50, 80, 90, 95, 99, 99.9 %): worst |diff| 6.1e-15
   the drag path, each level started from the last level's ends, 8 counts x 499 levels: 3.8e-15
     BINOMIAL_CDF + BINOMIAL calls per count per level step: mean 9.3, max 20
   cqBinCheck passes; with BINOMIAL_CDF reading (n, k, p) it fails and setup refuses Exact
B. the bookkeeping
   cqXBuild: catch level <= L  <=>  statsmodels' interval contains p, every k, every level
     500..999, for (p, n) = (0.1, 20) (0.5, 5) (0.38, 100) (0.01, 5) (0.99, 50) (0.25, 37): 0 mismatches
   1,500 PPL samples x 8 levels, n = 20 / 5 / 100: cqLimits vs statsmodels worst 4.7e-15;
     colour from the catch level == contains the truth: 0 mismatches; long-run tally after
     cqSetLevel == direct recount at all 8 levels
C. coverage by exact enumeration      80 %     90 %     95 %     99 %
   p = 0.10, n = 20   exact          0.9568   0.9568   0.9887   0.9976
                      Wilson         0.7455   0.9568   0.9568   0.9887
                      Wald           0.8352   0.8672   0.8760   0.8780
   worst exact coverage over p (n = 20, 95 %): 0.9580 at p = 0.49; mean 0.9770
   k = 0 upper end at n = 20, 95 %: 1 - 0.025^(1/20) = 0.168433 (= statsmodels)
   mean width at p = 0.10, n = 20, 95 %: exact 0.292, Wilson 0.263
   help page 4 quotes 95.8, 98.9, 95.7 (Wilson), 87.6, 95.7 (exact at 80 and 90 %), 0.168: all as computed;
   as drawn: 14 lines, the longest 47 characters
D. the PPL sampler, 20,000 Exact intervals: coverage 0.9895 vs exact 0.9887 (4 SE = 0.0030)
E. sessions
   cas = giac: setup Exact, +50, tap the line with 0 yeses (row 36), drag the slider, Up, Help
     (6 pages), Quit -> 'CICatcher: 49 of 50 caught the truth (98.0 %) at 99.5 %, Exact, p = 0.10,
     n = 20; see CQ_COVER'.  Panel: 'upper = 1-(1/40)^(1/20) = 0.1684' + 'exact (CAS)'.
     CAS calls: 1-(50/2000)^(1/20), 1-(10/2000)^(1/20), 1-(5/2000)^(1/20) -- one per event
     (the tap, the lift, Up), none twice; badges frame by frame d C C d d C C C: the frames drawn
     at the drag's intermediate levels show the decimal form only
   cas = fail: the same session, 'upper = 1 - (α/2)^(1/n) = 0.1684' + 'decimal' throughout, no error
   1,728 CAS templates (n 5-100; L 500, 503, 800, 900, 950, 953, 990, 995, 999; both ends) through
     icas: every one = the closed form to 1E-12, no 'Root of', no error; longest answer 20
     characters (the panel shows up to 20 with the decimal, 28 without)
   one frame with 50 Exact intervals: 130 shapes, 19 texts (beta 1's budget: < 200, < 25)
   Exact n = 5 and n = 100 sessions with drags and keys run clean; with BINOMIAL_CDF failing
     its check Exact is refused with a message
F. beta 1's suite (verify_CICatcher.py) on beta 2: PASS, 71 checks (one script change: six help
   pages, so six Enters)
```

## 3 · Gate

```
bash check.sh CICatcher_beta2.txt CICatcher_beta1.txt
  kit lint: 0 errors
  ppl_check_v3 tally: none (beta 1: none); hard E2/E3/E6/E8/E10/E11: none
  lint_ppl: 1129 checks, 8 problems -- beta 1's 5 known-noise lines, plus the CAS kit's own text
    (BRIEF_CAS: copy exactly):  line 493 STRING() with 1 args (STRING(CAS(cqCS)));
    line 504 x2 STRING() with 2 args (the lint reads INSTRING as STRING)
  full parse: fails at 168, the first file-level LOCAL after the EXPORT list (beta 1: 131, the same
    construct) -- the kit's limit; the harness reads the whole file
  1931 lines, 69239 bytes
python3 ppl_gate_v1a.py CICatcher_beta2.txt CICatcher_beta1.txt
  ppl_check_v3: clean / clean; lint_ppl as above
  fleet_names_v2 over 27 files (newest of each program): 1244 routine names, 0 collisions,
  0 untagged, 0 mixed-tag files, 0 built-in matches        RESULT: PASS
```

## 4 · Device test checklist (least to most risky)

1. **Run CASProbe beta 1 first**, on the G2 and the G1. If it reports another call form, change the IFERR line in `cqCas` (line 493). If it shows quoted answers, the kit strips them. If the CAS is unusable, change nothing: step 12 then shows "decimal".
2. **Paste and compile.** Likely spots: the new `LOCAL` lines 225-226, `cqCas`'s IFERR around `CAS(…)` and the `CHAR(34)` test (500), and the five-item setup `CHOOSE` (1538).
3. **BINOMIAL order, in Home:** `BINOMIAL_CDF(20,0.1,2)` = 0.676926805…, `BINOMIAL(19,0.1,2)` = 0.285179807…. If either differs, Exact will say "Exact is off": tell Claude the values.
4. **Beta 1 behaviour unchanged.** Run t at the defaults, +50, drag the level, tap a line, then Help: there are now **six** pages, and page 2's engine line still names STUDENT_ICDF.
5. **Setup → Exact**, defaults p 0.10, n 20, 0.95. The header reads "target 95 %" and "Exact, p = 0.10, n = 20". +50: lines, blue or red, none entering the grey zones, and the all-rate settling near 99 %. Note the +50 time on the G1 (the catch levels are a table lookup).
6. **Tap a line with 1 or more yeses:** tiles and "p̂ = 2/20 = 0.10: 0.01 to 0.32, caught" (Clopper-Pearson 2/20 is 0.0123-0.3170).
7. **Up/Down and Conf:** at 80 % most lines still catch: coverage stays near 95.7 %, because exact is conservative.
8. **The drag (the showcase), on the G1:** slide the right edge slowly. Each new level re-solves the ends of about 6 counts (about 55 BINOMIAL calls a frame). **Note the frame rate**; if it is too slow, tell Claude (a coarser stop for drawing only is an option).
9. **Help page 4**, "Exact intervals: never below": 14 lines, the last "exact ends: bisection on BINOMIAL_CDF (checked)". Check that nothing is cut off on the right (47 characters).
10. **n = 5 and n = 100** with Exact: drags and taps run, and n = 100 tiles are 2 px.
11. **Quit:** the summary names "Exact, p = …".
12. **CAS: tap a line with 0 yeses** (a dot at 0; about 12 % of samples at the defaults). What you should see:
    - while the finger is down: "upper = 1 - (α/2)^(1/n) = 0.1684" with "decimal";
    - after lifting: "upper = 1-(1/40)^(1/20) = 0.1684" with "exact (CAS)" in dodger blue, and the numbers line under it.

    Drag the level with that line picked: "decimal" during the drag, then the CAS form for the new level after lifting (e.g. "1-(1/200)^(1/20)" near 99 %). Note the delay after the lift on the G1: that delay is the CAS. If the CAS fails, "decimal" stays and there is no error.

## 5 · Not verified, stated plainly

- **Nothing has run on a Prime.** That includes `CAS("…")`, `STRING()` of a CAS answer, `INSTRING` (emulator only), and `BINOMIAL(n − 1, p, k)` used as a slope (the 3-argument pdf form is verified; its use for very small values, where it can underflow to 0, falls back to halving).
- **12-digit BCD vs the harness's IEEE double:** the 1E-9 relative stop was chosen to be reachable under rounding noise; the device's pass counts are unknown, and the 100-pass guard bounds them.
- **The drag frame rate with Exact on a G1** is the open question; BINOMIAL_CDF's speed on the device has never been measured.
- **The Prime's Giac is older than desktop 1.9.** The closed form's printed shape may differ, for example `1-1/40^(1/20)`. Anything up to 28 characters is shown; longer falls back to the decimal line.
- **One line added to the kit** (`cqCas` sets `cqCasOK`); the kit parameter is renamed `cqIN`.
- **Font widths** are estimated; the longest new lines are 47 characters on help page 4, and the panel's CAS line is 32 at the defaults.
- **Wilson at 80 %** (74.6 % at the defaults) remains as in beta 1; the guide mentions it.
