# StudRange beta 15b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 15a. Every beta 15a feature is kept, including the type-3 soft-key logic the emulator confirmed. The #PYTHON srq block is byte-identical. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

StudRange beta 15a ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) in round 2 on 17 October 2026 (BRIEF_R2FIX_v1, §0 and §4). The plot's soft keys fire now. Round 2 also found:

- **A real tap was skipped.** "Plot menu → Help for this plot → close it by tapping the footer at the α− key's spot → tap α− at the same spot: ignored once, then works."
  - `sr_WaitAny` reads its closing tap through MOUSE and adds the tap's spot to `srTLX/srTLY` (15a line 1040).
  - **On the emulator no click from a MOUSE-read tap ever reached WAIT(−1).** So the list entry stayed until a real tap landed at that spot (±2 px) — and that tap was eaten.
- **The Quit summary missed the plot.** "The Quit summary says 'q crit not computed, p not computed, HSD not computed' after a session that used only the Distribution plot, which showed q crit 3.638 and p 0.0643."
- **Fixed decimals turn scientific below 10^−d** (typed in Home): `STRING(0.096, 2, 1)` = `"9.6ᴇ-2"`.
- **INSTRING on an empty string stops a program.** StudRange has no INSTRING, LEFT or MID; item 3 of the brief asks to confirm that.

## What changed (line numbers: beta 15a → beta 15b)

1. **A stale click must also have been already queued** (sr_PlotMode's touch handling, 15a 1926–1987 → 15b 2003–2083).
   - The plot reads `TICKS` just before `pmKey:=WAIT(-1)` and just after it (15b 2006–2008).
   - A click that matches the next spot on the list is stale only if `pmWT<=srQueuedMs` (15b 2066), that is, only if WAIT(−1) handed it over within 100 ms.
   - A real tap made later at the same spot now counts. A click that really was still queued is still skipped. Nobody has measured that hardware case; harness `mouse_tail` models it.
   - The threshold is one named constant: new file-level `LOCAL srQueuedMs:=100;` with its comment (15b 360–365).
   - Otherwise the list logic is unchanged. `sr_WaitAny` is byte-identical (it still adds its tap, for the hardware case).
   - This is the same design as BayesTree beta 8c.
2. **The Quit summary reports the last q crit and p the student saw** (15a 2153–2157, 2314–2326 → 15b 2243–2257, 2414–2434).
   - New file-level `srQS`, `srAS`, `srPS` (15b 355–358) hold three things, as their page showed them:
     - the q crit, as " = 3.8612", or " > 6.0" when the plot says "q crit > 6.0";
     - its α, as "0.0500";
     - the p, as "p = 0.07000", or "p < 0.00001" rather than 15a's "p = < 0.00001".
   - The menu modes set them: P-value (15b 1420–1423), Critical value (1473) and HSD (1526).
   - **The plot sets the q crit with its k, ν and α, and the p if q obs > 0, as they stood on the last frame when it is left** (15b 2255–2257). Esc and "Leave the plot" change nothing, so the last frame is the state the plot is left in.
   - The summary now names α too: "q crit (k = 3, ν = 12, α = 0.050) = 3.773, p = 0.0700, HSD not computed (engine: Python)".
   - Each value keeps its own page's decimals: 3 and 4 on the plot, 4 and 5 in the menu modes.
   - "not computed" stays for what was not.
   - **EP_QCRIT and EP_QPVAL are still written only by the full-precision menu modes** (beta 14's rule). The plot's values are curve-level.
3. **INSTRING / LEFT / MID: none in the code — confirmed.** The verify script searches the PPL code outside comments, strings and the #PYTHON block for INSTRING, LEFT, RIGHT and MID: none.
4. **No scientific fixed decimals (brief 2b).** Every `STRING(…, 2, …)` call and every `sr_FmtF` caller was reviewed.
   - **`sr_FmtF` rounds first** (15a 982–985 → 15b 1038–1045). A value a hair below 0 rounds to −0, which is set to 0 so it cannot print "-0.0".
     - Every `sr_FmtF` call is now safe.
     - The calls that could reach the case:
       - a tiny q obs typed in, a tiny MSE and the HSD that follows from it (shown as 0.0000);
       - a yardstick difference of means below 0.001.
     - The rest (α ≥ 0.001 at 3 places, α ≥ 1E−4 at 4, q crits, t crits, F at the diagnostics' 0.93) could not reach it and are unchanged in effect.
   - **Through `sr_FmtF` now:**
     - **the simulation's percents** (15a 1308–1311 → 15b 1370–1373; 15a 1907–1908 → 15b 1984–1985). One replicate in 2,000 is 0.05 %, and `STRING(0.05, 2, 1)` is "5.0ᴇ-2"; it now reads 0.1 %;
     - **the yardstick's means and tick labels** (15a 1549, 1558 → 15b 1623, 1632). A mean of 0.0004 printed "4.000ᴇ-4", and a tick summed across zero is a hair off 0;
     - **the summary's HSD** (15a 2325 → 15b 2433).
   - **F(q) (15a 1362 → 15b 1430)** is a probability, so it now uses `sr_FmtP`'s "< 0.00001", as P(Q ≥ q) on the line above does.
   - **Safe as they were:**
     - `sr_FmtP`: its floor 10^−d is never below 10^−d, and its last line is reached only by 0 or by p ≥ 10^−d;
     - the integer `STRING(n, 2, 0)` calls (k, m, ν, the index of a mean, ms);
     - the plot's axis labels: ticks from 0 in steps ≥ 10^−d, quarters 0–1, `pmJ*ysp` for pmJ ≥ 1;
     - α as a percent, 100α ≥ 0.1 (now through `sr_FmtF` anyway).
5. **Header.**
   - A "What changed in beta 15b" paragraph, with the emulator's findings and 15a line numbers.
   - The status lines (beta 15a ran in round 2; its soft keys fire).
   - The banner and the title line now say beta 15b.
   - The #PYTHON block's own comment still says beta 15, so the block stays byte-identical.

Nothing else changed. The routines that differ from beta 15a are exactly `StudRange`, `sr_CritMode`, `sr_FmtF`, `sr_HSDMode`, `sr_PlotMode`, `sr_PvMode`, `sr_SimRun` and `sr_Yard` (verify 7g, 15b). Outside them, only the four new file-level lines differ (`srQS`, `srAS`, `srPS`, `srQueuedMs`) and comments.

## Verification

`verify_StudRange_beta15b.py` was built from the 15a script and runs on **harness v3d**. Output is in `verify_StudRange_beta15b_output.txt`: **100 ok, 0 failures**.

- **Sections 1–7 are kept.**
  - Sections 1–6: the MicroPython engine and the PPL engine against SciPy, the plot cache, the H0 simulation, k = 2, and the real source in the harness.
  - Section 7: soft keys, stale clicks, the summary.
  - 7b and the "p = 0.00000" check now run beta 15, the version they are about.
  - 7f's expected summaries now carry α, e.g. "q crit (k = 4, ν = 28, α = 0.0500) = 3.8612, p not computed, HSD = 1.3652".
- **7g (15b):**
  - The routine diff against 15a is as listed.
  - `sr_WaitAny` is byte-identical.
  - The #PYTHON block is byte-identical to 15a and to 15.
  - Outside the routines, only the four new lines differ.
  - The threshold is named once and used once, and the clock is read around the wait.
  - The type-3 soft-key lines are unchanged.
- **8a, the stale spot, both ways.** The harness's `Bridge` delivers a fresh tap 400 ms after WAIT(−1) is called; anything already queued comes back at once.
  - Beta 15a skips the first α− tap after Help is closed at that spot (α stays 0.050), and the second tap works. This reproduces the emulator's finding.
  - **Beta 15b takes the first tap: 0.050 → 0.025.**
  - **A click injected as already queued is still skipped** (α stays 0.050). This holds with `mouse_tail=True` and a clock that has not moved, and with taps 400 ms apart. A real α− tap after it counts once.
  - With the queued test patched out, that click would step α.
  - Taps in the plot and repeated soft keys still behave as in 15a.
- **8b, the summary:**
  - After a plot-only session it equals the plot's own readouts ("α = 0.050   q crit = 3.773", "q obs = 3.500   p = 0.0700"): "StudRange: q crit (k = 3, ν = 12, α = 0.050) = 3.773, p = 0.0700, HSD not computed (engine: Python)". These match SciPy to the plot's decimals.
  - EP_QCRIT and EP_QPVAL stay 0, because the plot does not write them.
  - Beta 15a's summary for the same session says "not computed" three times, as the emulator showed.
  - After α− then k+, the summary has k = 4 and the last α and q crit.
  - With no q obs, p is "not computed".
  - α = 0.001 is reported as the header showed it.
  - P-value then the plot gives the plot's p. The plot then P-value gives the P-value page's p.
  - A p below 0.00001 reads "p < 0.00001".
- **8c, scientific STRINGs:**
  - `sr_FmtF` of 0.0004, 0.096, −1E−17, 0.05, 1E−6, 3.77293 and −2.5 gives "0.000", "0.1", "0.0", "0.1", "0.0000", "3.773" and "-2.50".
  - The yardstick with means −0.3, 0.0004, 0.2, 0.25 (ticks across 0) shows no scientific form and no "-0.0".
  - F(q) at q = 0.001 (F = 3E−7) reads "F(q) = < 0.00001".
  - A tiny MSE (1E−10, so HSD = 1.4E−5) gives HSD 0.0000 on the page and in the summary.
  - Beta 15a on that same run printed five scientific results: `-2.8ᴇ-17` (a tick), `1.0000ᴇ-10` (MSE), `1.3652ᴇ-5` (HSD), `2.75700ᴇ-7` (F) and `4.000ᴇ-4` (a mean).
  - **`h.sci_strings` over every harness run of beta 15b in the script (45 runs): none.**
- **8d:** no INSTRING, LEFT, RIGHT or MID in the PPL code.

## Gate

`python3 ppl_gate_v1b.py StudRange_beta15b.txt StudRange_beta15a.txt` (in `gate_r2`) gives **RESULT: PASS**.

- **ppl_check_v4:** 1 E7, the same as 15a. No hard errors, E12 included.
- **lint_ppl:** the same 18 problems as 15a, including the #PYTHON block's "depth went negative".
- **fleet_names_v2** over 25 files: 0 collisions, 0 untagged, 0 built-in matches. The new names are `srQS`, `srAS`, `srPS`, `srQueuedMs`, `pmWT` and `ffR`.
- **`check.sh`, kit lint:** 1 error, the "unbalanced" count from the #PYTHON block. That is the same single error beta 15a and beta 15 give; check.sh expects it for a Python-block file. There are 0 errors in the PPL.
- **Full parse:** it stops at the forward declarations, as 15a's does. That is the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. Paste. In the Program Catalog, Edit → Check shows no error.
2. **The stale spot:**
   1. Distribution plot (k 3, df 12, q obs 3.5), then Enter → Help for this plot.
   2. Close the help page by tapping its footer line at the α− key's spot (x about 26, y about 226).
   3. Back on the plot, tap α− **once**. α must go 0.050 → 0.025 on that first tap.
3. **The plot-only summary:**
   1. Run StudRange again: Distribution plot (k 3, df 12, q obs 3.5).
   2. Note the header ("α = 0.050   q crit = …", "q obs = 3.500   p = …").
   3. Esc, then Quit.
   4. Home should show "StudRange: q crit (k = 3, ν = 12, α = 0.050) = <the header's q crit>, p = <the header's p>, HSD not computed (engine: …)".
4. **The menu summary:** Tukey HSD (α .05, k 4, m 8, MSE 1), then Quit. Home should show "StudRange: q crit (k = 4, ν = 28, α = 0.0500) = 3.8612, p not computed, HSD = 1.3652 (engine: …)".
5. **G2 and G1, with a finger:**
   1. Repeat step 2.
   2. Close Help by tapping the strip under k−: no soft key may run. This is the unmeasured hardware case: a MOUSE-read tap's click reaching WAIT(−1).
   3. Then tap k− once: it must run.
6. **G1:** tap the soft key only after the plot has finished drawing (see Unresolved).

## Unresolved

- **The 100 ms threshold** is the brief's figure.
  - The hardware case is unmeasured: whether a G1 or G2 delivers a MOUSE-read tap's click to WAIT(−1). The design skips such a click, because it comes back at once.
  - One case is skipped once: a tap made *while the plot is still drawing*, within 2 px of the tap that just closed a page. WAIT(−1) has not yet been called, so the tap is already queued when it is. The plot is slow to draw on a G1, so a quick tap could hit this; a second tap works.
- **OS dialogs.** Whether an OS dialog (INPUT, CHOOSE) leaves a click for the next WAIT(−1) is still not known. The plot's checklist step 6 from 15a still applies: after a form's OK tapped with a finger, the plot must not take that tap as a soft key.
- **The summary's q crit is not always EP_QCRIT.** After a plot, the summary's q crit and p are the plot's fast-grid values (curve-level, 3 and 4 decimals). EP_QCRIT and EP_QPVAL keep the last full-precision menu values, so after a plot they can differ from the summary. Roger to say whether the summary should also show which kind of value it is quoting.
