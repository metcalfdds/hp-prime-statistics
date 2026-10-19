# BayesTree beta 8c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 8b; every beta 8b feature is kept, including the type-3 soft-key logic that the emulator confirmed. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

BayesTree beta 8b ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) in round 2 on 17 October 2026 (BRIEF_R2FIX_v1, §0 and §4). The round-1 fixes held: the soft keys fire, the counts add up, and every CAS page that ran showed real exact answers. Round 2 found these problems:

- **A real tap was skipped.** "Close the 2×2 view (or any page held by `bt_WaitAny`) by tapping the footer at the ROC key's spot, then tap ROC at the same spot: the first tap is ignored, the second works." `bt_WaitAny` reads its closing tap through MOUSE and adds that spot to `btTLX/btTLY` (8b line 638). **On the emulator, no click from a MOUSE-read tap ever reached WAIT(−1).** The list entry therefore stayed until a real tap landed on that spot (±2 px), and that tap was eaten.
- **The views ignored a tap on their footer.** In the PPV, ROC and Fagan views, a tap at y ≥ 218 reaches WAIT(−1) only as `{3, x, y}`, even though those views draw no DRAWMENU. Their type-0 test (`pvT`, `rcT`, `fgT == 0`) never saw it. Their footers say "Esc = back" and their comments say "outside = back".
- **INSTRING on an empty string stops the program.** Typed in Home: `INSTRING("", "a")` gives **Error: Invalid input**. `bt_Cas` sets `cR := ""` when the CAS fails and then tests `INSTRING(cR, "undef")`. Harness v3d stops beta 8b's verify script at B12 (`audit_v3d/BayesTree_beta8b.txt`).
- **Fixed decimals turn scientific below 10^−d.** `STRING(0.096, 2, 1)` gives `"9.6ᴇ-2"`.
- **Other findings:**
  - On the Diagnostics page, "use ConTable2" names a retired program.
  - On the two-test breadcrumb, each arrow was covered by the next number: "0.04 –0.42 –0.92".
  - On the Exact page with two tests, line 2 (`then test 2: TP = 28586225, FP = 2397500, FN = 5648775, TN = 45552500`) ran off the right edge.
  - The soft key "Forensic" showed as "Forensi".

## What changed (line numbers: beta 8b → beta 8c)

1. **A stale click must also have been already queued** (the main loop, 8b 2709–2729 → 8c 2863–2898).
   - The loop reads `TICKS` just before `kk := WAIT(-1)` and again just after it: `btWT := TICKS; kk := WAIT(-1); btWT := TICKS - btWT;` (8c 2866–2868).
   - A click that matches the next spot on the list is stale only if `btWT <= btQueuedMs` (8c 2892), that is, only if WAIT(−1) handed it over within 100 ms.
   - A real, later tap at the same spot now counts. A click that really was still queued is still skipped; that is the hardware case nobody has measured, and harness `mouse_tail` models it.
   - The threshold is one named constant, the new file-level `LOCAL btQueuedMs := 100;` (8c 358–363), with its comment.
   - The list logic is otherwise unchanged: what fills the list, the ±2 px match, and that any key, press, move or non-stale click forgets it.
   - `bt_WaitAny` is byte-identical: it still adds its tap's spot to the list, for the hardware case.
2. **A footer tap closes the PPV, ROC and Fagan views** (8b 1429–1451, 1560–1583, 1750–1771 → 8c 1571–1573, 1704–1706, 1899–1901). The new rule is `IF xxT == 3 THEN IF y >= 218 THEN close`. The coordinates are read only after the type is known to be 3, so a one-element lift is never indexed. A click has no press and no lift, so nothing of it is left queued and it needs no stale entry. The type-0 rule ("outside the plot = back") is kept as it was.
3. **INSTRING never sees "" (brief 2a).** The 9 INSTRING lines:
   - **`bt_Cas` (367 → 420–422).** The kit's `IF DIM(cR) > 0 THEN … END` guard was added. The IFERR call line and the quote strip are byte-identical.
   - **`bt_Rep`, the replace loop (443–455 → 495–516).** Now in the 2a shape:
     - an empty pattern returns the text unchanged;
     - the position is looked for only while text is left;
     - a pattern at the very end empties the rest explicitly.
   - **`bt_Strip` (469 → 532–534).** It looks for "list" only in a non-empty text. A failed CAS call hands it "".
   - **Safe as they were:**
     - `bt_Strip` 467, `bt_IsFr` 484, `bt_Dig` 495 and `bt_Wrap` 557: the first argument is a literal.
     - `bt_Wrap` 556: the first argument is `MID(wrT, wrI, 1)` with `IP(wrW/2) ≤ wrI ≤ wrW < DIM(wrT)` (the WHILE condition), so it is always one character long. The callers pass wrW = 50.

   **LEFT/MID with a computed count or start:**
   - `bt_Cas` applies them only when DIM ≥ 2; `MID(cR, 2, 0)` on `""""` is "", as measured.
   - `bt_Rep` applies `MID(…, 1, rpI−1)` only when rpI > 1.
   - `bt_Wrap` has a count ≥ 1 and starts ≥ 2.
   - The new `bt_Crumb` applies `LEFT(cbS, 2)` only when DIM ≥ 2, and its MID starts at 2.
   - There is no RIGHT in the file.
4. **No scientific fixed decimals (brief 2b).** Every `STRING(…, 2, d)` was reviewed:
   - **`bt_NumS` (527 → 595).** It now rounds first. 1 − 0.9 can come out a hair under 0.1; this is the one scientific result the v3d audit recorded: `STRING(0.1, 2, 1) → 1.0ᴇ-1`, at the PC's raw double, in `bt_NumS`.
   - **`bt_Pct` (541 → 611).** It now rounds first. With two near-perfect tests the break-even prior is about 1.0E−6, which beta 8b printed as "1.002ᴇ-4 %". It now reads "0.000 %", an honest "if prior < 0.000 %".
   - **`bt_fmtq` (830 → 952).** It now rounds again after the subtraction of two rounded shares.
   - **Safe as they were:**
     - `bt_fmtp`: its floor `10^-d` is never below `10^-d`, and its last line is reached only by 0 or |x| ≥ 10^-d.
     - `bt_fmtB`: 3 decimals only for v ≥ 0.001, 2 only for v ≥ 0.01.
     - The axis labels `STRING(i/5, 2, 1)`: 0, 0.2 … 1.
     - The mode-1 calls (counts, digits, N): unaffected.
5. **The two-test breadcrumb is laid out from measured widths** (8b 2491–2504 → 8c 2641–2659; new `bt_Crumb`, 8c 672–719).
   - `TEXTOUT_P` returns the x just after the text it drew. This is the BlackJack v11 way, cited in the brief; no fleet program had used it.
   - Each number and arrow therefore starts 3 px after the piece before it.
   - If the crumb ends past x 102 (the slider panel starts at 104), that try is painted white and drawn again without the leading zeros (".04 → .42 → .92"). If it still does not fit, it is drawn at two decimals at most, 2 px apart (">.99", "<.01").
   - The colours are as before: grey stages, a magenta posterior.
   - TEXTOUT_P's return value has not yet been seen on our calculators. If it ever hands back no position past the start, `bt_Crumb` assumes 7 px per character and 10 px for the arrow.
6. **The Exact page with two tests: the four counts take two lines** (8b 1982–1989 → 8c 2123–2138): "then test 2: TP = …, FP = …," and "  FN = …, TN = …", with a colour for each line.
7. **The Diagnostics page** (8b 1298 → 8c 1420–1421) now reads "For p-values / CIs on real data: EpiStats 2×2." That is 46 characters; the old line had 47.
8. **Soft key "Forensic" → "Forens"** (8b 2297 → 8c 2443–2447). It fits the strip's roughly 6 characters, and the brief suggested it. Help page 1's list of keys and the header's key list say the same (8b 2171 → 8c 2318; 8c 312). The menu item and help page 3 still say "Forensic labels".
9. **Header:**
   - a "beta 8c (17 Oct 2026)" paragraph with the emulator findings and 8b line numbers;
   - the status lines (beta 8b ran in round 2, and what it showed);
   - the banner, which now says beta 8c.

Nothing else changed. The verify script checks the routine diff. Only these routines differ from beta 8b:
- `BayesTree`, `bt_Cas`, `bt_DiagView`, `bt_ExactView`, `bt_FaganView`, `bt_HelpView`, `bt_NumS`, `bt_Pct`, `bt_PrevView`, `bt_Rep`, `bt_RocView`, `bt_Strip`, `bt_fmtq`;
- the new routine `bt_Crumb`.

Outside them, the only change is the one new line `LOCAL btQueuedMs := 100;`; everything else is comments.

## Verification

`verify_BayesTree_beta8c.py` was built from the 8b script. It runs on **harness v3d**; the output is in `verify_BayesTree_beta8c_output.txt`: **185 PASS, 0 FAIL**.

- **Kept from 8b, now on v3d:** A, B, B16, G (8b vs 8a, on those files), S, L and C.
  - B12 (`cas='fail'`) now also runs beta 8b and shows it **stops** with the INSTRING error.
  - S2 and L1 run beta 8a with `cas='giac'`, because under v3d it stops on a failed CAS call.
  - B16 (beta 7's checks) has one more intended difference: "I breadcrumb" expected the fixed x 2 / 38 / 74. R3 checks the new layout instead.
- **G (8c):**
  - The routine diff is exactly as listed above.
  - `bt_WaitAny` is byte-identical.
  - `bt_Cas` keeps its call line and quote strip.
  - The threshold is named once and used once.
  - The type-3 soft-key lines are unchanged.
- **R1, the stale spot, both ways.** The harness subclass `Timed` makes a fresh tap arrive 400 ms after WAIT(−1) is called; anything already queued comes back at once.
  - Beta 8b skips the first ROC tap after the 2×2 view is closed at that spot, and the second tap works. That is the emulator's finding, reproduced.
  - **Beta 8c opens ROC on the first tap.** The same holds at the Values, PPV and More spots.
  - **A click injected as already queued is still skipped.** This was run with `mouse_tail=True` and a clock that has not moved (plain v3d), and also with 400-ms taps. A real ROC tap after it then counts, once.
  - With the queued test patched out, that click would run ROC, so the skip is real.
  - Taps on the tree, a view closed by an outside tap, and a node page in the `mouse_tail` case all still behave as in 8b.
- **R2, the views.** The model: a tap at y ≥ 218 is only `{3, x, y}`, as in round 2.
  - PPV, ROC and Fagan close on a footer tap and nothing else opens; beta 8b in the same model stays open.
  - A tap at the PPV key's spot after ROC was closed there opens PPV.
  - The type-0 "outside = back" still works, and a drag in the PPV plot still moves the prior.
- **R3, the breadcrumb.** The width model is the brief's **6.5 px per character at font 1**, the arrow included.
  - For the emulator's tree (prior 0.041, 0.835 / 0.95 twice) it reads ".04 → .42 → .92" and ends at x 85.5. In v3d's own 5.5-px model it keeps the zeros: "0.04 → 0.42 → 0.92".
  - Across 72 two-test trees (12 priors × 6 test pairs, the extremes included), every crumb has five pieces, none overlaps the piece before it, and all end left of x 102. The forms used: 45 trees drop the leading zeros, and 27 (the extremes) use two decimals.
  - In a stress model with an **11-px arrow**, nothing overlaps either, and 42 of the 72 still end left of x 102. The other 30, whose crumbs have two or three "<.01" or ">.99" stages (extreme priors, near-perfect tests), end between x 103.5 and 110. Beta 8b's fixed layout overlaps in that model: the emulator's "0.04 –0.42 –0.92".
  - If TEXTOUT_P handed back no position, the fallback (7 px per character, 10 for the arrow) still lays the emulator's tree out without overlap, ending left of x 102.
- **R4, the Exact page with two tests.** The emulator's tree gives lines 2–3 exactly as above. Every line stays inside x 318, there are 13 lines (15 when forensic), and the last is at y ≤ 206. Beta 8b's line was 69 characters, reaching x 388.
- **R5 and R6.**
  - Diagnostics shows the new line inside x 318, and "ConTable2" appears nowhere in the code.
  - The soft keys on page 3 read Test 2 · Reset · Forens · Leaves · Exact · More, and every label has 6 characters or fewer.
- **R7, INSTRING.**
  - `bt_Rep` is right for a pattern at the end, at the start, the whole text, an empty pattern, an empty text, twice in a text, and not at all; beta 8b's `bt_Rep` stops on the first and the fifth.
  - `bt_Strip("")` is "".
  - `bt_Cas` returns "" with no error when the CAS fails, still answers 1/3, and refuses 1/0 (±∞).
  - **Every CAS page end to end with `cas='fail'`** (one test, two tests, forensic, and forensic with two tests through the Exact soft key): the tree badge reads "decimal, tap", both Exact pages read "decimal", and there is no error. **Beta 8b stops on each of these runs.**
- **R8, scientific STRINGs.**
  - Direct checks:
    - `bt_Pct(1.0E−6)` = "0.000 %" (8b: "1.002ᴇ-4 %");
    - `bt_NumS(1 − 0.9)` = "0.1";
    - `bt_fmtq` of 0.005 − 0.004 and of 0.1 − 0.099 = "0.001".
  - **`h.sci_strings` over every harness run of beta 8c in the script (387 runs): none.** For the record, beta 8b's runs in the same script gave `1.002ᴇ-4`.
  - A stricter check outside the script ran the whole script again and flagged any `STRING(x, 2, d)` whose raw PC double lies in (0, 10^−d), as if the calculator kept binary noise. It found nothing for beta 8c. For beta 8b it found `bt_NumS` at 0.09999999999999998 and `bt_Pct` at 1.002E−4.

## Gate

`python3 ppl_gate_v1b.py BayesTree_beta8c.txt BayesTree_beta8b.txt` (in `gate_r2`) gives **RESULT: PASS**.
- ppl_check_v4: the same tally as 8b (1 E4, 2 E5, 1 E9); no hard errors, E12 included.
- lint_ppl: 20 problems against 8b's 17.
  - The 3 new ones are the lint reading `STRING(ROUND(x, d), 2, d)` as four arguments (`bt_NumS`, `bt_Pct`, `bt_fmtq`). 8b's `bt_fmtc` line already shows the same noise.
  - The rest are 8b's known noise: INSTRING read as STRING, and the EXPORT discipline.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 built-in matches. The new names are `bt_Crumb`, `cbL`…`cbC`, `btQueuedMs` and `btWT`.
- `check.sh`: **kit lint 0 errors**. The full parse stops at the root sign (line 1399), as 8b's does at line 1277; that is the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. Paste. Then Program Catalog → BayesTree → Edit → Check: there must be no error.
2. **The stale spot:**
   1. Soft key 2×2.
   2. Tap the footer line at the ROC key's spot (about x 133, y 226): the tree comes back.
   3. Tap ROC **once**: the ROC view must open. Esc.
   4. Repeat at the Values spot: Values opens on the first tap.
3. **The views close on their footer:**
   1. Soft key PPV, then tap the footer (about x 150, y 226): back to the tree, with nothing else opening.
   2. The same in ROC (tap near x 100) and in Fagan (Enter → Fagan nomogram, then tap the footer).
   3. In PPV, a tap right of the plot (about x 300, y 205) also goes back.
4. **Diagnostics** (More → Diag): the last grey line reads "For p-values / CIs on real data: EpiStats 2×2." and stays inside the screen.
5. **Two-test breadcrumb:**
   1. Enter values 0.041 / 0.835 / 0.95 / 1000.
   2. Enter → Second test → 0.835 / 0.95.
   3. Top left: three numbers with whole arrows between them, nothing overlapping, all left of the slider box: "0.04 → 0.42 → 0.92" or ".04 → .42 → .92".
6. **Exact page, two tests:**
   1. With that tree: More, More, Exact.
   2. Lines 2–3 read "then test 2: TP = 28586225, FP = 2397500," and "  FN = 5648775, TN = 45552500", inside the screen and above the footer.
7. **Soft keys, page 3** (More twice): Test 2 · Reset · **Forens** · Leaves · Exact · More. Forens toggles the forensic labels.
8. **Fallback**, only if a CAS failure can be provoked: the tree reads "decimal, tap" and no error stops the program. On the emulator the CAS has always answered.
9. **G2 and G1, with a finger:**
   1. Repeat steps 2 and 3.
   2. Tap a box, then close its node page by tapping the bottom strip under a soft key: no soft key may run. This is the unmeasured hardware case, where a MOUSE-read tap's click reaches WAIT(−1). If a soft key runs here, report it.
   3. Then tap that soft key: it must run on the first tap.
10. **G1:** after closing a page at a soft key's spot, tap that soft key slowly, after the tree has finished drawing (see Unresolved).

## Unresolved

- **The 100 ms threshold** is the brief's figure. Two cases remain open:
  - The hardware case is unmeasured: a G1 or G2 might deliver a MOUSE-read tap's click to WAIT(−1). The design still skips such a click, because it comes back at once.
  - Some taps count as already queued and are skipped once. This happens when, while the tree is still being drawn, the student taps within 2 px of the tap that just closed a page; WAIT(−1) has not been called yet, so the tap is already queued when it is. On a slow G1 redraw a quick tap could do this. A second tap works.
- **OS dialogs.** Whether INPUT or CHOOSE leaves a click for the next WAIT(−1) is still unknown. If a CHOOSE OK tap on the strip leaked into a view opened from the Enter menu, that view would now close at once; it used to ignore such a click. Check this on the emulator by opening PPV from the Enter menu with a finger tap on OK.
- **The breadcrumb's widths are a model.** TEXTOUT_P's return value has not been observed on our calculators; the brief cites the corpus. With an 11-px arrow, 30 of the 72 trees end between x 103.5 and 110: those whose crumb has two or three "<.01" or ">.99" stages. That end sits under the slider panel, which is drawn on top. Under the brief's 6.5 px model all 72 fit.
- **The Exact page with forensic labels, two tests and a value of more than 6 decimals** has 16 lines. `bt_PageL` shows 15, so the last line (the CAS timing) is not shown. Only the new wrapped line made this case reach 16.
- **"Forens"** is the brief's suggestion. Other labels of 6 characters or fewer that would read well: "Court", "Source". Roger to choose.
