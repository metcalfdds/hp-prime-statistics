# BayesTree beta 7 → beta 8: what changed

*16 October 2026 · the CAS version, built on beta 7 (every beta 7 change kept, the `WAIT(-1)` event model too).*
*Source: `/home/claude/work/out/BayesTree_beta7.txt` (1,828 lines) → `/home/claude/work/out/BayesTree_beta8.txt` (2,653 lines, UTF-8, LF). Verification: `/home/claude/work/out/verify_BayesTree_beta8.py` (output in `verify_BayesTree_beta8_output.txt`).*
*Not yet run on hardware. **Nothing about the CAS has run on a calculator**: every CAS call goes through `bt_Cas` (line 282), and every CAS feature falls back to the decimal. "new nnn" = a beta 8 line.*

## Design decisions to know about

- **The CAS answers events, never frames.** The tree asks the CAS only (a) when the values on screen differ from the cached ones, and (b) when no finger is dragging (`btGest == 0`, new 2326). So it asks after a key, a lift, a menu or a view, but never on a slider or branch drag sample. During a drag the panel says "exact: on lift" instead of showing a fraction for old values. When a drag ends, the existing lift branch now sets `btDirty` (new 2627). That one extra frame asks the CAS. Nothing else in the event model changed: same `WAIT(-1)`, same types 0/1, same `SIZE >= 3` rule.
- **The break-even prior is drawn from PPL and shown exactly by the CAS.** The mark's position comes from `bt_BEp` = 1/(1 + LR+) (new 714), the program's own number (BRIEF_CAS rule 3), so it follows a sens/spec drag live. The CAS's `solve` result ("1/20") is text on the Exact page. The CAS re-solves only when sens, spec or test 1 change (its own cache key `btBK`), never for a prior change. A slider drag therefore never asks for it (verified: B3).
- **Two tests: the break-even is defined on the slider's own prior** (the prior before test 1): the prior at which a person positive on BOTH tests is as likely to have it as not, 1/(1 + LR₁+ × LR₂+). For 0.9/0.95 twice that is 1/325 = 0.31 %. This matches what the slider sets in two-test mode. The alternative, test 2's own break-even 1/(1 + LR₂+), lives on an axis the tree does not show, so the PPV view (whose x-axis in two-test mode is test 2's prior) hides the mark and says "Two tests: the break-even is on the Exact page."
- **Integer ratios.** `bt_Rat` (new 328) writes each value as whole numbers, in one of three ways:
  - a decimal of at most 6 places (0.95 → 95/100). Every slider, ladder, drag, arrow and typed value is one of these;
  - a continued fraction with denominator at most 10⁶, for values from Enter counts (920/950 → 92/95), so the fractions are the student's own;
  - a value rounded to 6 places, which the Exact page says it did.

  No decimal point ever enters CAS text (verified over 1,188 templates).
- **Every answer is checked** (`bt_IsFr`, new 407): only the characters 0–9, / and - are accepted. That rejects an approximate-mode answer ("0.6666…"), Giac's "infinity", and a solve that comes back as "btq=1/20". All of these fall back to the decimal.
- **Natural frequencies.** The Exact page uses the smallest N = 1000 × 10ᵏ (k ≤ 6, N ≤ 10⁹) at which all four leaves are whole people, so the task's example reads "PPV = 95/590 = 19/118 = 0.161" at N = 10,000. Those counts are PPL arithmetic and stay exact even without the CAS. The CAS supplies the reduced fraction.
- **A slow CAS switches itself off on the tree.** If one update takes more than 1.5 s (`btCasMs`, timed with TICKS), `btCasAu` goes to 0. The panel then reads "tap for exact", and only the Exact page asks the CAS. The G1's CAS speed is unknown.
- **Names.** The kit's parameters are `bt_N` and `bt_S` (the literal tag replacement). With `btS`, the parameter would equal the CAS symbol `bts` ignoring case. No PPL identifier in the file equals a CAS symbol (btq, bts, btc, btl, btm) ignoring case, and no two names differ only by case (scripted check).

## (a) Every change

1. **Header** (new 1-69): "beta 8", the firmware line names beta 4-8 as not run and says "run CASProbe beta 1 first"; a dated "beta 8 - what changed" list; beta 7's and older notes kept; controls block lists the panel tap and the Exact soft key (new 222-227).
2. **File-level state** (new 248-249, 11 names, at most 6 per line): `btCasOK` (badge), `btXK` (cache key), `btXP/btXN/btXC` (exact PPV, NPV, 1 − PPV), `btBK/btBE` (break-even key and text), `btBS/btBSK` (symbolic solve and its test count), `btCasMs`, `btCasAu`. Initialised in `BayesTree()` (new ~2140).
3. **The CAS kit** (new 263-300): `bt_IStr` and `bt_Cas` exactly as BRIEF_CAS gives them, including the quote-strip step added on 16 Oct (one surrounding pair of `CHAR(34)` removed before the undef/error check).
4. **Helpers** (all `bt_`, new 306-490 and 1752-1810): `bt_Same` (list equality), `bt_Rat`, `bt_RT`/`bt_RC` (ratio and complement as CAS text), `bt_Rep` (replace all; never `LEFT(s, 0)`), `bt_Strip` (removes `list`, brackets, braces, spaces), `bt_IsFr`, `bt_Dig`, `bt_Disp` (CAS names to tree names: btq→p, bts→se, btc→sp, btl→LR₁, btm→LR₂, * → ×), `bt_NumS` (a number as typed, for displayed formulas), `bt_Pct`, `bt_Wrap` (breaks at a space, else after + × /), `bt_BEp`, `bt_XKey`, `bt_FrLn`/`bt_FrS` (a fraction line; one too long says "exact fraction has N digits", never cut), `bt_Rpt`, `bt_PageL` (a 15-line drawn page with the badge, held with `bt_WaitAny`).
5. **`bt_ExactUpd`** (new 755-810): builds Bayes' theorem as CAS text from the ratios for the stage on screen (D = prior × earlier sens; H = (1 − prior) × earlier (1 − spec)): PPV = D·se/(D·se + H·(1−sp)), NPV = H·sp/(H·sp + D·(1−se)), 1 − PPV when forensic, and `solve((btq*…)/(btq*…+(1-btq)*…)=1/2,btq)`. Returns at once if the cache key matches. Example: `(1/100*95/100)/(1/100*95/100+99/100*5/100)` → `19/118`.
6. **The tree** (`BayesTree()`):
   - new 2326: `IF btGest == 0 AND btCasAu == 1 THEN bt_ExactUpd(...)` before the frame is composed;
   - new 2366-2378: **the break-even mark**: two magenta pixels-wide lines above the track (y 2-8) at `bt_SlX(beP)`, and the track's inside tinted light red left of it ("here most positives are false"); no mark outside 0.001-0.999;
   - new 2459-2507: **the exact panel** in the empty gap between the FN and FP leaves (x 214, y 103/115/127): "PPV = 19/118", "NPV = 1881/1882" (forensic: "1−PPV = …"), and the badge "exact (CAS), tap" or "decimal, tap"; "exact: on lift" during a drag; "tap for exact" in slow mode. Then **the break-even lines** between FP and TN (y 167/179): "Most T+ are false / if prior < 5.0 %" ("Most T+T+ false" with two tests; forensic "Most matches false / below 1 in 20"), red while the prior is below the break-even, magenta otherwise;
   - hit boxes: id 24 twice (both gaps), from the same layout variables (new ~2172-2176);
   - press handler: id 24 opens the Exact page (new 2592);
   - lift branch: one redraw if a drag changed the values (new 2627);
   - exit summary: "BayesTree: PPV = 0.667 = 2/3, …" when the exact PPV is valid and short (new 2646).
7. **Soft keys**: page 3 slot 5 (was empty) is **Exact** → menu item 15 (`btSKA`).
8. **Menu**: "Exact answers (CAS)" is item 15 (shown as **F**); **Close is now G** (16). The menu has 16 items.
9. **`bt_ExactView`** (new 1811-2012), two pages. Page 1: natural frequencies, PPV/NPV (and 1 − PPV) as count fraction, CAS fraction and decimal, the break-even prior "1/20 = 0.0500 = 5.0 %", the sentence ("Below a prior of 5.0 %, a positive result is more likely wrong than right: most T+ are false"), the two-test note, the rounding note, and the CAS time. Page 2: Bayes' formula in symbols, the same with the student's numbers, the exact result, the CAS's symbolic solve ("p = (-sp+1)/(-sp+se+1)"; with two tests "p = 1/(LR₁×LR₂+1)"), LR+ and the numeric solve. Every line says "decimal" / "by hand" when the CAS did not answer.
10. **PPV view** (`bt_PrevView`): plot bottom 195 → 183. Below the tick labels (y 189) one line at y 199: "Below 5.3 %, most positives are false (PPV < 1/2)." (forensic: "Below 1 in 19, most matches are not the source."). The break-even point gets a dotted magenta crosshair at PPV = 1/2 with a square. The x mapping and the drag are unchanged.
11. **Help**: a fourth page, "exact answers (CAS)" (14 lines, ≤ y 211); page 1's soft-key line names Exact; "1/3 … 3/3" → "1/4 … 4/4".

## Gate output (final run)

```
=================== BayesTree_beta8.txt ===================
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW)  ---
      1 E4       2 E5       1 E9
--- 2. ppl_check_v2 tally (ORIG) ---
      1 E4       2 E5       1 E9
--- 2b. ppl_check_v2 HARD errors in NEW (E2 E3 E6 E8 E10 E11), must be empty ---
none
--- 3. lint_ppl structural ---
1858 checks, 17 problems
  PROBLEM line 2254: INPUT return discarded (cancel proceeds silently)     (beta 6/7's false positive: the IF tests it)
  + 12 x "STRING() with N args, want 3"                                      (see below)
--- 4. full parse (kit interpreter) ---
BayesTree_beta8.txt              PARSE FAIL PPLError: line 1148: unexpected character '√'
   ORIG: BayesTree_beta7.txt              PARSE FAIL PPLError: line 737: unexpected character '√'
--- 5. line count, size, non-ASCII in code (E5 list) ---
2653 lines, 117513 bytes
  1148  E5   non-ASCII in code: '√'      (beta 5's, bt_DiagView, unchanged)
  1352  E5   non-ASCII in code: '√'      (beta 5's, bt_RocView, unchanged)

ppl_gate_v1.py: 2. tally 1 E4, 2 E5, 1 E9 = original; hard errors none; 3. lint_ppl 1858 checks, 17 problems
                (the same lines); 5. fleet_names_v2: 0 untagged, 0 mixed-tag, 0 built-in matches

ppl_gate_v1a.py (absolute paths): 2. as above; 3. as above; 5. fleet_names_v2 over 27 files (newest of
                each program): 0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches.  RESULT: PASS
                (1. kit lint and 4. parse are skipped there -- no kit zip in out/; check.sh ran both above)
```
- **The ppl_check tally is unchanged** (1 E4 `bt_fmtc(v)`, 2 E5 `√`, 1 E9 `STRING(NP,1,0)`, all beta 5's).
- **The 12 "STRING() with N args" lint lines are a lint limitation, not code problems.** Its pattern `STRING\s*\(` also matches inside every `INSTRING(`, which the CAS kit and the string helpers use, and it counts the kit's one-argument `STRING(CAS(bt_S))` as wrong. A script confirmed that each flagged line is an `INSTRING` call, the kit line, or beta 5's `STRING(ROUND(v,0),1,0)`. Every CAS version of a fleet program will show these.
- The kit interpreter stops at `√` in both versions (the tool's limit); harness v3 loads and runs the whole program.
- **fleet_names_v2 over the newest version of each of 26 programs in `out/`** (including the parallel CAS versions: CASProbe beta 1, ErrorRate beta 1, ChiTable beta 3, …): **0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches.** (Over all 76 `.txt` files the only collisions are old/new versions of the same program.)

## Verification (`python3 verify_BayesTree_beta8.py`: 72 checks, ALL PASSED)

**Part A: every CAS template through desktop Giac 1.9 (`icas`) against Python `fractions` and SymPy.**
- A1: `bt_Rat` gives 95/100 and 14/1000, recovers 92/95, 7/9 and 2/3 from count ratios, and flags a value with more than 6 decimals.
- A2: **1,188 CAS texts**, built exactly as the program builds them, all equal to Python's fractions. They cover PPV, NPV, 1 − PPV and the break-even, for 11 priors × 9 tests × 1 and 2 tests × forensic on/off. **No CAS text holds a decimal point.**
- A3, the named examples:
  - prior 1 %, 95/95: PPV **19/118**, NPV **1881/1882**, break-even **1/20**;
  - the defaults: PPV 2/3; forensic 1 − PPV 1/3;
  - two tests: PPV **36/37**, break-even **1/325**;
  - Enter counts 45/5/30/920: PPV **3/5**;
  - natural frequencies at N = 10,000: 95/590 = 19/118 = 0.161.
- A4: the symbolic solves match SymPy. One test: `(-btc+1)/(-btc+bts+1)` = (1 − sp)/(se + 1 − sp). Two tests: `1/(btl*btm+1)`. The equation is linear in the prior, so there is one root.
- A5: `bt_BEp` (PPL, which places the mark) equals the CAS break-even (max diff 7e-17).

**Part B: the program in harness v3, with `cas='giac'`, `cas='fail'` and canned answers.**
- B1, defaults:
  - the panel reads "PPV = 2/3", "NPV = 171/173", "exact (CAS), tap", then "Most T+ are false / if prior < 5.3 %";
  - 3 CAS calls for the first frame;
  - the mark is at x 214 = `bt_SlX(1/19)`, with the tint left of it;
  - no text at y ≥ 218 or past x 318;
  - the summary reads "PPV = 0.667 = 2/3".
- B2, the task's example (Enter values 0.01/0.95/0.95): the panel shows 19/118 and 1881/1882. Exact page 1 shows every line: N = 10000, TP 95 FP 495 FN 5 TN 9405, 95/590, "= 19/118 = 0.161", "prior = 1/20 = 0.0500 = 5.0 %" and the sentence. Page 2 shows the formula, the numbers put in, and "p = (-sp+1)/(-sp+se+1)". Opening the page cost one CAS call (the symbolic solve); everything else came from the cache.
- B3, slider drag 0.1 → 0.001:
  - every drag frame says "exact: on lift";
  - the CAS calls are 3 at the start and **2 after the lift (no solve)**;
  - the break-even lines never change;
  - the four leaves re-count in every frame, the lift frame included;
  - exactly one extra frame (the lift);
  - then "PPV = 2/113".
- B4, sens drag: the mark moves in the drag frame (PPL) while the panel waits; 3 CAS calls after the lift.
- B5:
  - one key = one update (3 calls) → "PPV = 5/7";
  - tapping a box and closing its page = no CAS call.
- B6–B8:
  - forensic: "1−PPV = 1/3", "below 1 in 19";
  - two tests: 36/37, 19/23, "if prior < 0.31 %", mark at x 185, page 2 in the LR form;
  - Enter counts: 3/5, 184/185.
- B9/B10: a tap on the panel, and soft key page 3 slot 5, both open the Exact page.
- B11, PPV view: the magenta square sits at (53, 107), where PPV = 1/2 at prior 1/19. The sentence is at y 199 and the rows are at 189/199/212/226.
- B12, **`cas='fail'`**:
  - no runtime error;
  - the panel shows "PPV = 0.161", "NPV = 0.999", "decimal, tap";
  - the pages say "decimal", keep 95/590 (PPL counts) and give the break-even "by hand";
  - the summary has no fraction.
- B13, slow CAS (a copy with the threshold at −1): the tree switches to "tap for exact" and asks no more; a tap still opens the Exact page, which asks the CAS.
- B14: in stale-key mode, no page is skipped. B15: four help pages, all inside the screen.
- B17: answers wrapped in quotes are stripped by the new kit (still 2/3); an approximate-mode answer "0.666666666667" is refused, so the panel shows the decimal and "decimal".
- B16, **beta 7's own 52-check verification run against beta 8**: 48 pass. The 4 failures are the intended changes:
  - the summary now carries "= 2/3";
  - one extra lift frame after a drag (two of beta 7's frame-alignment checks; B3 re-checks every frame);
  - soft-key page 3 now has "Exact".

Desktop Giac took about 30 ms per call (one `icas` process each). That says nothing about the calculator.

## (b) DEVICE TEST CHECKLIST: least to most risky (G2 first; then repeat 7, 8 and 10 on the G1 with a stopwatch)

1. **Run CASProbe beta 1 first**, on both calculators.
   - If it reports a different call form, change only the IFERR line in `bt_Cas` (line 287).
   - Also note three of its answers:
     - how a `solve` answer is wrapped (`{1/20}`, `[1/20]`, `list[1/20]` or `btq=1/20`): `bt_Strip` handles the first three; the fourth would fall back to the decimal and needs a one-line change in `bt_Strip`;
     - whether fractions stay exact (not "0.0526…");
     - the G1's time per call.
2. **Paste and compile.** The new names are 22 `bt_` routines and 11 file-level LOCALs. Note the cursor line if the paste stops.
3. **Menu and soft keys (no CAS).** The menu has 16 items: F = "Exact answers (CAS)", G = Close. Soft keys page 3: "Test 2, Reset, Forensic, Leaves, Exact, More".
4. **The break-even mark and lines (PPL, no CAS).** On the first frame:
   - a magenta tick above the slider track at about x 214, with the track left of it pale red;
   - between the FP and TN leaves, magenta "Most T+ are false / if prior < 5.3 %";
   - slide the prior below about 0.05: the two lines turn red.

   Drag the D+ pair down: the mark moves right and the % rises as you drag.
5. **PPV view** (soft key PPV): a dotted magenta crosshair where the PPV curve crosses 1/2 (prior about 0.053), and under the tick labels "Below 5.3 %, most positives are false (PPV < 1/2)." Check that the tick labels and this line do not touch, and that tap/drag still move the prior.
6. **Help** page 4 (Esc leaves early): 14 lines, nothing cut off.
7. **The exact panel (first CAS step).** What you should see on the first frame, between the FN and FP leaves:
   - "PPV = 2/3", "NPV = 171/173", "exact (CAS), tap" in dodger blue;
   - if it reads "decimal, tap" with "PPV = 0.667": the CAS did not answer. Compare with CASProbe;
   - **G1: time the first frame.**
8. **Keys and drags with the CAS.**
   - Right (spec 0.96): you should see "PPV = 5/7", "NPV = 432/437" and "if prior < 4.3 %". **G1: time a key press.** If one update takes over 1.5 s, the panel switches by itself to grey "tap for exact"; that is the safety switch, so note the time.
   - Slide the prior: during the drag the panel says grey "exact: on lift" and the break-even lines do not move. **After the lift** the fraction appears. If it stays "exact: on lift" after the finger is off, the lift is not arriving as a `WAIT(-1)` event (beta 7's checklist item 8). Any key or tap then updates it; tell Claude.
9. **The Exact page.** Tap the panel (or Exact, or menu F).
   - Page 1 at the defaults: "Picture N = 1000 people", "TP = 90, FP = 45, FN = 10, TN = 855", "PPV = TP/(TP+FP) = 90/135", "= 2/3 = 0.667", "NPV … = 171/173 = 0.988", "prior = 1/19 = 0.0526 = 5.3 %", and two red lines of the sentence.
   - Key → page 2: "= 0.1×0.9 / (0.1×0.9 + 0.9×0.05)", "= 2/3 = 0.667", "p = (-sp+1)/(-sp+se+1)". **The Prime's Giac may print an equal formula in another arrangement**: note it.
   - Then Enter values 0.01 / 0.95 / 0.95 / 1000: the panel shows "PPV = 19/118"; page 1 shows "N = 10000 … 95/590 … = 19/118 = 0.161 … prior = 1/20 = 0.0500 = 5.0 %".
10. **Forensic, two tests, counts.**
    - Forensic (page 3): "PPV = 2/3", "1−PPV = 1/3", "Most matches false / below 1 in 19".
    - Test 2 (0.9/0.95): "PPV = 36/37", "NPV = 19/23", "Most T+T+ false / if prior < 0.31 %", mark near x 185; page 2 "p = 1/(LR₁×LR₂+1)".
    - Reset, then Enter counts 45/5/30/920: "PPV = 3/5", "NPV = 184/185".
11. **After the run:** open the CAS view. The CAS settings (exact mode, digits) should be as before, and `btq` should not be defined (a `solve` assigns nothing). Then Esc from the tree: Home shows "BayesTree: PPV = … = …/…, NPV = …".

## (c) Not confirmed / left as it was

- **Everything about the CAS on the device**:
  - the call form `STRING(CAS("…"))`;
  - how answers are wrapped and spaced;
  - whether `STRING()` of a CAS fraction gives "19/118";
  - whether a numerical-mode answer arrives quoted (the kit strips one pair);
  - whether HSeparator affects CAS text (the program's CAS text has no decimal point or comma).

  Every one of these falls back to the decimal with the "decimal" badge, so a wrong guess costs the student the fraction, not the program.
- **The Prime's Giac is older than 1.9.** The templates use only `/`, `*`, `+`, `-`, `solve` and whole numbers, and every answer is accepted only if it is a fraction.
- **Whether a PPL program's local variables are visible inside `CAS("…")`** is unknown. This is why no PPL name equals a CAS symbol, ignoring case.
- **The G1's CAS speed** (the 1.5 s safety switch is a guess at "too slow for a key press").
- **Whether a finger lift reaches `WAIT(-1)`** (beta 7's open question). If it does not, the fractions update on the next key or tap instead of on the lift.
- **Text widths are harness estimates** (5.5 px a character, font 1). The tight spots:
  - the panel's longest line, "Most T+ are false" (94 px from x 214);
  - "exact (CAS), tap" (88 px);
  - the Exact page's longest lines (≤ 50 characters).
- **Left as it was:** beta 5's `√` (2 lines), `bt_fmtc(v)`, `STRING(NP,1,0)`; `MAKELIST` with Home's `K` in the views (house rule until GfxProbe T19). New list-building code uses FOR loops (`bt_Rpt`).
- **Not added:** no `#cas` blocks, no `CAS.name()` calls, no Python `cas`, no `FILLPOLY_P`/`TRIANGLE_P`, no new `WAIT(-1)` types.
