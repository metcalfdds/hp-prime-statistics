# BayesTree beta 6 → beta 7: what changed

*16 October 2026 · the touch and graphics version, built on beta 6 (every beta 6 fix kept).*
*Source: `BayesTree_beta6.txt` (680 lines) → `BayesTree_beta7.txt` (1828 lines, UTF-8, LF). Verification: `verify_BayesTree.py`.*
*Not yet run on hardware (beta 3 was the last version run, on the G2 and G1). "old" = beta 6, "new" = beta 7.*

## Design decisions to know about

- **Slider behaviour: continuous, not snapped.** While the finger drags, the prior follows on a log-odds track (0.001 … 0.999), rounded to two significant figures and never finer than 0.001 (`bt_Sig2`, new 269). On lift it stays where it is. `+`/`-` then go to the next ladder rung above or below (`bt_LadStep`, new 307), so the 17-rung ladder still works from any value. Below 0.01 the prior moves in steps of 0.001, so there the knob moves in jumps of up to 7 px.
- **One event source for every live view.** The tree keeps `WAIT(-1)` (old 643, device-tested at beta 3) and now also takes type 1 (move) events, after the `SIZE >= 3` check. The three new live views (PPV, ROC, Fagan) use `WAIT(-1)` with the same rules, **not** the house kit's MOUSE-polling drag. The reason: if the firmware queues touch events for `WAIT(-1)` while a program polls `MOUSE` (nobody knows yet whether it does), a MOUSE-polled drag in a view could be replayed onto the tree afterwards. With `WAIT(-1)` everywhere, each view uses up its own drag events. Static pages (node, branch, 2×2, Diagnostics, icons, three prevalences, help) still hold with `bt_WaitAny` (house shape).
- **Only types 0 and 1 are acted on.** Any other event (the one-element lift list, or a type the program does not use) only ends the current gesture. A pressed-and-released branch number that never moved more than 8 px counts as a tap and opens its page.
- **Taps vs drags.** Boxes, first-level numbers and the mosaic open their pages on the press, as beta 6 did. The second-level branch numbers are both tappable and draggable, so for them the decision waits until the finger moves (a drag) or lifts (a tap).
- **Second test.** It is capped at two tests (the breadcrumb has three numbers). The stage lists `btSSe`/`btSSp` and the loop in `bt_Book` allow more. Tree 2's root is the people who tested **positive** on test 1 (natural frequencies: 1000 → 135). This assumes the two tests err independently given D, and the help page says so.

## (a) Every change

1. **Header** (new 1-176): "beta 7"; firmware line now names beta 4-7 as not run (old 11-13); a dated "beta 7 - what changed" list; beta 6/5/4/3 notes, licence, AI line and credit lines kept. The controls block (new 157-174) lists every gesture and soft-key page.
2. **File-level state** (new 184-188, 20 names, at most 6 per line): `btPr/btSe/btSp` carry the values the views hand back; `btFor` is the forensic flag, `btPrb` the leaves flag, `btNS` the number of tests; `btSSe/btSSp` hold the earlier tests; `btLad` is the ladder (it was old 485, local `pl`); `btTX/btTY` hold the last tap; `btHX1…btHId` are the hit boxes; `btSX1/btSX2/btLGL/btLGH` describe the slider; `btSKP/btSK/btSKA` are the soft-key pages.
3. **`bt_WaitAny`** (old 137-149 → new 248-266) now has the house kit's `xxWaitAny` shape: it returns the key code, or −1 for a tap with the tap's x, y in `btTX/btTY`. Callers that ignore the return value are unchanged.
4. **New helpers** (all `bt_`-tagged):
   - `bt_fmtB`: the breadcrumb format.
   - `bt_Sig2`, `bt_SlX`, `bt_SlP`: slider rounding and the log-odds mapping.
   - `bt_LadStep`: the next ladder rung.
   - `bt_Hit`: the hit-box scan.
   - `bt_Mosaic`: four `RECT_P` blocks inside a black frame; every block keeps at least 1 px.
   - `bt_LeafBar`: the leaf bar.
   - `bt_Book`: the stage bookkeeping. It returns {prior, N, D+, D−, TP, FN, FP, TN} for the stage on screen.
   - `bt_LnClip`: a nomogram line clipped to y 24-206.
5. **Prevalence slider** (item 1). It replaces old 589-590's "prior = …, sens = …, spec = …" text. The strip is at x 104-315, y 1-21, with the label "prior 0.100" (forensic: "1 in 10"), a track at x 174-310, ticks at 0.01, 0.1, 0.5, 0.9 and 0.99, and a red knob. The hit box is x 168-316, y 0-25. Pressing makes the knob jump to the finger, and type-1 moves follow it (new main-loop touch handler). All six boxes, the mosaic, the bars and the readouts recount on every changed sample, and only on a change (the `btDirty` flag).
6. **Mosaic inset** (item 1): `bt_Mosaic(4, 24, 80, 96, …)` top left, for the stage on screen. TP green, FN red, FP orange, TN light grey RGB(220,220,220); T+ is the top row in both columns. At 1 % the TP column is 1 px wide (checked). Tapping it opens "Same test, three prevalences".
7. **Sens/spec by dragging** (item 2). The D+ pair zone is x 159-211, y 27-106 and sets sens; the D− pair zone is x 159-211, y 132-216 and sets spec. Up = more, at 0.005 per pixel, rounded to 3 dp and clamped to 0.01…0.999. A drag starts only after more than 8 px of type-1 movement, and it then measures from the crossing point, so the value does not jump. Grip marks (three short blue lines at x 161-165) sit left of each second-level number.
8. **Branch pages** (item 3): ids 8-13 in `bt_NodeInfo` (prior, 1−prior, sens, 1−sens, 1−spec, spec). Example: "P(T+ | D+) = sens — read along the ROW, not the column … It is NOT P(D+ | T+), which is the PPV". The page is now a list of short lines (≤ 50 characters, font 1, y 88-172) on a taller panel (y 26-212), because several of beta 6's lines (old 168, 186) ran past the panel. Count pages also show the share of N. The first-level numbers moved from y 146 to y 142 (room for "not source").
9. **Soft keys** (item 4, plus the "More" convention from the coordinator). `DRAWMENU(btSK(btSKP))` runs after every blit (new main loop). The pages are:
   - Page 1: Values, Counts, ROC, PPV, 2×2, **More**.
   - Page 2: Diag, Fagan, Icons, 3 prev, Help, **More**.
   - Page 3: Test 2, Reset, Forensic, Leaves, (blank), **More**.

   A press with y ≥ 218 gives slot `MIN(6, IP(x/53.4)+1)`. Slot 6 turns the page and wraps. Any other slot runs its menu item through the flat list `btSKA(6*(page−1)+slot)`. Reset is in slot 2, never under slot 6. The footer (old 633) is gone. The readouts are now a column at x 4 ≤ 82, y 126-174, plus "odds × LR+" at y 192 and a legend "⇆ = spec, ⇅ = sens, +/- = prior" at y 204. No tree text reaches y 218 (checked).
10. **Live PPV view** (item 5; old 326-392 → new 774-901). The curves are cached once (every second column). A press inside the plot grabs the prior, and drags follow, at `ROUND((x−40)/250, 3)`. Left/Right step the ladder. Esc/Enter, or a press outside the plot, go back. The prior is handed back in `btPr`. With two tests the view only displays (its prior is test 1's PPV). The readout moved to y 212, the footer to y 226, and "x = prior" moved into the subtitle.
11. **Live ROC view** (item 5; old 395-458 → new 903-1028). The curve is cached once. The finger's x gives FPR, so spec = ROUND(1−FPR, 3) and sens = Φ(d′ − Φ⁻¹(spec)) with d′ fixed. Left/Right move the point by 0.01 in FPR. A live readout shows sens, spec and the PPV at the current prior. Values are handed back in `btSe/btSp`.
12. **Fagan nomogram** (item 6, new 1055-1213). The axes are at x 60/160/260 and centred on y 112, at 27 px per decade of odds:
    - prior: y = 112 + 27·log10(odds), with 0.001 at the top;
    - LR: y = 112 − 13.5·log10(LR), from 0.001 to 1000;
    - posterior: y = 112 − 27·log10(odds).

    The axis labels are literal strings, and there are short ticks at 2 and 5. The magenta line runs prior → LR+ → PPV and the dodger-blue line prior → LR− → 1−NPV; both are 2 px thick, with markers at the LR and posterior points. A drag on the left axis (±30 px) moves the base prior. `+`/Down move the knob down and `−`/Up move it up. The prior is handed back in `btPr`.
13. **Second test** (item 7). Menu item 8 opens `INPUT({se2, sp2}, "Second test", …)`, prefilled with the test on screen.
    - On OK: `btSSe := {sens}; btSSp := {spec}; btNS := 2`, and test 2's values become the current sens and spec.
    - `bt_Book` chains the stages: N₂ = N·P(T1+) and prior₂ = PPV₁.
    - The tree shows the breadcrumb "0.10 → 0.67 → 0.97" at the top left (earlier stages grey, the current posterior magenta) and a greyed root "T+ 135".
    - The nomogram draws test 1's line in grey, a dotted grey carry from post₁ back to the prior axis, and test 2's lines from there.
    - Item 9, "Reset to one test", restores test 1. Enter counts also resets to one test.
14. **Icon array** (item 8, `bt_IconView`):
    - The grid is 40 × 25 squares at a 6-px pitch (x 40-279, y 26-175).
    - The order is TP, FP, FN, TN, so the T+ people form one band.
    - The counts are whole people, rounded by largest remainder so they add to exactly 1000.
    - Each colour run per row is one `RECT_P`, and 63 white lines draw the gaps (about 100 calls instead of 1000).
    - Below the grid: a legend, "Of the 135 who test +, 90 have it:" and "PPV = 90 / 135 = 0.667" (forensic: 1 − PPV).
15. **Leaf bars** (item 9): `bt_LeafBar` draws a 2-px bar at y+13 in each leaf box in the mosaic colours. It is 92 px wide: linear from 1 % (8 px) to 100 % (92 px), with a log stub of 0.1 %…1 % in the first 8 px and a grey tick at 1 %.
16. **Forensic labels** (item 10, menu item C, soft key page 3):
    - Tree: the leaves read "match" and "no match", the D boxes are labelled "source" and "not source", the slider says "1 in 10", and the readouts become PPV, 1−PPV, RMP, LR+ and LR−.
    - Node and branch pages use forensic wording. The FP page and the 1−spec page say: "1 − spec is the random-match probability … 1 − PPV … is the probability the matching person is NOT the source — what the court needs."
    - 2×2 view: the "rows:" line becomes P(match | not source) = RMP and the "cols:" line P(not source | match) = 1 − PPV, followed by "Prosecutor's fallacy: swapping row and column".
17. **Same test, three prevalences** (item 11, `bt_ThreeView`): three mosaics (92 × 116 px each) at 1/1000, 1/100 and 1/10, with "PPV = 0.018 / 0.154 / 0.667" in font 2.
18. **Leaves toggle** (item 12, menu item D): the leaves and D boxes show joint probabilities (0.090 / 0.010 / 0.045 / 0.855 and 0.100 / 0.900). The D boxes then use font 1 so the text fits.
19. **Help** (item 13, `bt_HelpView`): three drawn pages (the tree; the views; reading it forensically) covering every gesture, the soft-key pages and "More". Any key or tap goes to the next page, Esc finishes. The 14 lines end at y 211.
20. **Menu** (old 512-519, 7 items → new, 15 items; items 10-15 appear as A-F): Enter values, Enter counts, ROC curve view, PPV vs prevalence, 2×2 table view, Diagnostics, Fagan nomogram, Second test, Reset to one test, Icon array: 1000 people, Same test three prevalences, Forensic labels on/off, Leaves: counts/probabilities, Help, Close. **Close is now F, not 7.** A GETKEY drain follows every dialog.
21. **Main loop restructured** (old 502-674):
    - Bookkeeping comes from `bt_Book`.
    - The frame is drawn only when `btDirty` is set. Ignored events, and the −1 timeout, cost nothing.
    - The `bt_Drain()` after every touch (old 671) is removed, because it would freeze a drag (StudRange beta 14's reasoning). Pages drain the finger themselves.
    - The ladder index logic (`pl/pidx/bestd/dtmp`, old 485-491, 530-535, 562-567) is replaced by `bt_LadStep`.
    - The unused counter `j` and the unused plot locals `px, py, lastpy, lastny` are gone.
22. **RETURN summary kept.** It is unchanged with one test. With two it appends ", after 2 tests from prior 0.100", and "prior" in the summary is then the stage's prior.

## Gate output (final run)

```
=================== BayesTree_beta7.txt ===================
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW)  ---
      1 E4       2 E5       1 E9
--- 2. ppl_check_v2 tally (ORIG) ---
      2 E4       2 E5       1 E9       2 W3
--- 2b. ppl_check_v2 HARD errors in NEW (E2 E3 E6 E8 E10 E11), must be empty ---
none
--- 3. lint_ppl structural ---
1316 checks, 6 problems
  PROBLEM line 1520: INPUT return discarded (cancel proceeds silently)   (pre-existing false positive: beta 6 line 550, the IF tests it)
  PROBLEM line 195: STRING() with 4 args, want 3                          (pre-existing false positive: bt_fmtc's ROUND(v,0))
--- 4. full parse (kit interpreter) ---
BayesTree_beta7.txt              PARSE FAIL PPLError: line 737: unexpected character '√'
   ORIG: BayesTree_beta6.txt              PARSE FAIL PPLError: line 297: unexpected character '√'
--- 5. line count, size, non-ASCII in code (E5 list) ---
1828 lines, 82266 bytes
   737  E5   non-ASCII in code: '√'     (beta 5's, in bt_DiagView, unchanged)
   916  E5   non-ASCII in code: '√'     (beta 5's, in bt_RocView, unchanged)
```
- The tally fell from 7 to 4. The remaining E4 is `bt_fmtc`'s parameter `v` and the E9 is `STRING(NP,1,0)` on an integer, both from beta 5.
- The kit interpreter stops at `√` in both versions, and it also cannot read file-level LOCAL (the tool's limits). The harness, which reads both, loads and runs the whole program.
- `fleet_names_v2.py`, newest version of each of 20 programs: **0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches**. Over all 45 .txt files in `out/`, no `bt_` name collides; the collisions it lists are other programs' old/new version pairs.

## Verification (`python3 verify_BayesTree.py`: 63 checks, ALL PASSED)

Part 1 checks the formulas and geometry against SciPy and Python:
- PPV/NPV in three cases.
- d′ = 2.926405 and AUC = 0.980740.
- Every drag point on the ROC keeps z(se) + z(sp) = d′ (max error 8.8e-11).
- **Fagan: in 347 (prior tick × LR) cases with the posterior on the axis, the straight line through the prior's pixel and the LR point ends within 0 px of the posterior's tick.** It crosses the LR axis within 0.38 px. The defaults end at y 104 = PPV 0.667's tick.
- Two tests: the chain gives the same result as the direct P(D | T1+, T2+) = 0.972973, and N₂ = 135.
- Slider round trip: worst 3 px.
- Icon counts add to 1000, each within 1 of the exact value.
- Leaf-bar lengths.

Part 2 runs the real program in the harness and compares what it prints:
- **A**: the defaults (six boxes, PPV, NPV, summary), soft-key page 1, nothing at y ≥ 218.
- **B**: a slider drag through 0.097 → 0.010 → 0.014 → 0.860 → 0.500, with one redraw per changed sample. All six boxes are correct at every sample. At 1 %: TP 9, FP 50, PPV 0.154, and the mosaic's TP sliver is 1 px wide.
- **C**: a D+ pair drag gives sens 0.800, and a D− pair drag clamps spec at 0.999.
- **D**: a tap on the sens number opens its "read along the ROW" page; a tap on the 1−spec number shows 1 − PPV = 0.333. Neither changes a value.
- **E**: the soft keys ROC, More → Fagan, and More cycling through three pages and back.
- **F**: a PPV-view drag gives prior 0.250 (PPV 0.857), handed back to the tree.
- **G**: a ROC tap at FPR 0.2 gives spec 0.800 and sens 0.981 (= Φ(d′ − Φ⁻¹(0.8))); Left gives 0.810 / 0.980; the PPV follows; both values are handed back.
- **H**: the magenta `LINE_P(G1, 60, 86, 260, 104)` matches Python. "LR+ = 18.000: 0.100 → PPV = 0.667". A left-axis drag to 0.01 gives PPV 0.154 and 1−NPV 0.001, handed back.
- **I**: the second test: root "T+ 135", breadcrumb 0.10 → 0.67 → 0.97, PPV 0.973, leaves TP 81 and FP 2. The nomogram chains from 0.667, with test 1's line grey. Reset brings back the one-test summary.
- **J**:
  - icons 90/45/10/855 and "PPV = 90 / 135 = 0.667";
  - three prevalences 0.018 / 0.154 / 0.667;
  - the forensic FP page, the forensic 2×2 (prosecutor's fallacy, 1 − PPV = 0.333) and the forensic tree;
  - the leaves as probabilities;
  - three help pages, all text at y ≤ 211;
  - a mosaic tap opening the three-prevalence page;
  - Enter counts 45/5/30/920 in stale-key mode with no skipped page.

A layout audit of every page (estimated widths) found no text past x 318 and no tree text reaching the soft keys.

## (b) DEVICE TEST CHECKLIST: least to most risky (G2 first, then repeat 3, 6, 9 and 12 on the G1)

1. **Paste and compile.** Only the routine names, file-level LOCALs and the menu are new. Note the cursor line if the paste stops.
2. **First frame.** The menu has 15 items, with 10-15 shown as A-F. Choose **F Close**. The tree appears in one piece, with:
   - the slider strip "prior 0.100" with its knob at about x 220;
   - a mosaic top left;
   - leaves T+ 90 / T− 10 / T+ 45 / T− 855, each with a thin bar along its bottom;
   - readouts PPV 0.667, NPV 0.988, LR+ 18.000, LR− 0.105;
   - the legend at y 204;
   - soft keys "Values Counts ROC PPV 2×2 More".

   Check that nothing overlaps the soft keys, and that "not source" / the first-level numbers do not touch (forensic mode, item 7).
3. **Keys.** ⇆ ⇅ +/- still work. From prior 0.1, `+` goes to 0.2 and `−` to 0.05.
4. **Static pages.** Through Enter: Icon array (A), Same test three prevalences (B), Help (E, three pages; Esc leaves early), 2×2, Diagnostics. Each appears in one piece and closes on a key or a tap. Check the icon grid's white gaps and the speed on the G1 (about 100 draw calls).
5. **Node pages.** Tap each box and the two first-level numbers. The text wraps on the panel, and the page stays up after the lift (beta 6's checklist item 5 applies again). A closing tap must not open anything behind it.
6. **Slider (the showcase).** Press on the track: the knob jumps there. Drag slowly from 0.1 to the far left. Every box, the mosaic, the bars and the readouts should follow live. At the 0.01 tick the orange FP block dwarfs a 1-px green sliver, and the PPV is 0.154. **On the G1, judge the lag:** does the knob trail the finger, or keep moving after you stop? (Each `WAIT(-1)` move event redraws the tree; there is no way to skip queued events.)
7. **Forensic and leaves toggles** (soft-key page 3, or menu C/D): match / no match, "source" / "not source", "1 in 10", RMP. Tap the FP leaf for the "what the court needs" page, and check the 2×2's prosecutor's-fallacy lines. Toggle Leaves: 0.090 …
8. **Branch numbers: tap vs drag.** Tap the sens number (0.900) without moving: its page opens **after you lift**. Then press on the D+ branches and drag down slowly: nothing changes for the first 8 px, then sens falls 0.005 per pixel. Do the same on the D− pair for spec. If a tap on a number never opens its page, the lift is not arriving as an event on this firmware. Tell Claude: the fix is to open on the press, as the boxes do.
9. **Live sub-views.** PPV view: tap/drag the plot and watch the prior follow; Left/Right follow the ladder; Esc returns the new prior to the tree. ROC view: tap on the curve; the red point jumps along the curve, and sens, spec and PPV change together. Fagan: the axes and labels are legible, the magenta line from 0.1 through LR 18 lands on about 0.667, and the blue line through 0.105 lands on about 0.012. Drag the left axis: both lines swing, and the readouts follow.
10. **Leaving a view by tapping outside it, then the tree.** After a drag in any live view, close it with Esc, then with a tap outside the plot. The tree must not change by itself, and no page may open. This tests whether left-over touch events reach the tree's `WAIT(-1)`.
11. **Second test.** Menu 8, OK with 0.9 / 0.95: the breadcrumb reads "0.10 → 0.67 → 0.97" (grey, grey, magenta), the root is grey "T+ 135", and the leaves are 81 / 9 / 2 / 43. Drag the slider: all three breadcrumb numbers move. Fagan: grey line 1, a dotted carry line, and magenta/blue for test 2. Menu 9 resets.
12. **Soft keys under `WAIT(-1)` (the riskiest item).** Tap Values, ROC, then More (twice) and a page-3 key. WaitLab's 2014 log says a menu-strip tap reaches `WAIT(-1)` only as type 3, which this program does not read. **If the soft keys do nothing on the tree** (they work on no other screen here), tell Claude. The fallback is to read y ≥ 218 taps with type 3 once GfxProbe T17 shows what it reports, or to switch the tree's wait to ChiTable's GETKEY + MOUSE polling. Every soft-key action is also in the Enter menu.
13. **Exit.** Esc: Home shows "BayesTree: PPV = …", with ", after 2 tests from prior …" if two tests are active.

## (c) Not confirmed / left as it was

- **Soft-key taps under `WAIT(-1)`** (checklist 12) and **whether a lift arrives as an event** (checklist 8) are inferred: the lift from beta 5's observed runtime error, the soft keys from WaitLab's 2014 notes. They are not confirmed on 2026-09-09 firmware.
- **Drag lag on the G1** (checklist 6, 9): moves are processed one event at a time. The drag cannot catch up by reading the live `MOUSE` position, because mixing `MOUSE` into a `WAIT(-1)` loop is unverified and the harness cannot model it.
- **Left-over touch events after a `bt_WaitAny` page** (checklist 5, 10): the same open question as beta 6's checklist item 5.
- **Glyphs**: `→` CHAR(8594) and `←→` (CHAR(8592)+CHAR(8594)) are listed as rendering in Lessons Learned §13. `∞` is still in GfxProbe T14.
- **Text widths** are harness estimates (5.5 px per character at font 1). The tightest spots:
  - the readout column (≤ 72 px of 80);
  - "not source" above the D− box;
  - "D+ 0.100" in the D boxes (font 1);
  - the breadcrumb slots (36 px each).
- `√` at new 737/916, the parameter `v` in `bt_fmtc` and `STRING(NP,1,0)` are beta 5's code, not in the task list, and are left as they were. `MAKELIST` uses Home's `K` as its counter (house rule until GfxProbe T19).
- Not added: no `FILLPOLY_P`/`TRIANGLE_P`, no alpha, no second finger, no `G2` background buffer, and no `WAIT(-1)` types other than 0 and 1.
