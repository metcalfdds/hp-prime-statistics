# StudRange beta 14 + StudRangePy beta 14c → StudRange beta 15: what changed

*16 October 2026. Sources: `StudRange_beta14.txt` (775 lines, "b14") and `StudRangePy_beta14c.txt` (500 lines, "py"). Output: `StudRange_beta15.txt` (2,228 lines, UTF-8, LF; "new"). **Not yet run on hardware.** Companion files: `studrange-guide_beta15.md` (the user's guide; no earlier StudRange guide was staged, so it was written from the programs), `verify_StudRange.py` and its output `verify_StudRange_out.txt`.*

**At staging: move `StudRangePy_beta14c.txt` (and `StudRange_beta14.txt`) to `_superseded_…`. StudRangePy is retired** — everything it did is in StudRange beta 15, and its `#PYTHON srng` block name is not reused (the new block is `srq`), so an old copy left on a calculator cannot collide.

## (a) Every change

### The merge

1. **One program, two engines.** New `#PYTHON srq` block (new 315-749). `Phi`, `prange`, `gpdf`, `outer`, `scdf`, `spdf`, `qsolve`, `qcrit` and the import lines are py 96-228 **byte-for-byte** (checked by `diff`, new 343-473). py's Terminal UI, its own plot and menu (py 230-493) are not carried over: PPL draws everything. The PPL engine (`sr_BuildZ … sr_SRCrit`, b14 180-301 → new 750-902) is the fallback; its only changes are items 5 and 6 below.
2. **The bridge** (new 555-588, 723-747): `ev`, `num` (reads a PPL real with `hpprime.eval`, never `argv`), `mark` (a trail in `SR_PZ`, hp-prime-kit's technique), `put` / `putel` (ONE value per eval, `"%.10f"` text built by concatenation; no `repr`, no `join`), `bar` (a progress bar through `hpprime.fillrect(gr,x,y,w,h,edge,fill)`, the order that ran on the G2, inside `try`). `main()` dispatches on `SR_MODE`: 0 probe, 1 p-value, 2 q crit, 3 plot cache, 5 k = 2 curve, 6 H₀ simulation. Top-level imports: `math` and `hpprime` only; `urandom` is imported inside `simulate()`.
   Payloads are fixed: one number to `SR_OUT`; 65 + 65 values to `EP_SRPDF` / `EP_SRCDF` plus `qmax` to `SR_OUT` (131 crossings ≈ 26 ms at hp-prime-kit's 0.2 ms); 65 to `EP_SRCD2`; 45 to `EP_SRSIM`.
3. **New EXPORTed globals** (new 280-303): `SR_K, SR_DF, SR_A, SR_Q, SR_MODE, SR_OUT, SR_M, SR_N, SR_TC, SR_ENGINE, SR_PZ`, lists `EP_SRCDF, EP_SRPDF, EP_SRCD2, EP_SRSIM`. ν = ∞ crosses as `SR_DF = 100000` (py's `v > 25000` branch).
4. **The three guards** (§9), exactly: `sr_PyRun` (new 1071) clears `SR_OUT := -1` (callers clear their lists with `MAKELIST(-1, K, 1, 65, 1)` / 45) and wraps `PYTHON(srq)` in IFERR; `sr_PyNum` (new 1088) validates by **using** `SR_OUT` inside IFERR against a range; `sr_Cache` (new 1153) reads `EP_SRCDF(65)` (the last value Python writes), `EP_SRPDF(65)` and `SR_OUT` inside IFERR and checks them; `sr_Cmp` reads `EP_SRCD2(65)`; `sr_SimRun` checks `EP_SRSIM(45) == 2000`. On failure the PPL engine runs (results, plot) or a MSGBOX says the Python-only feature needs Python (simulation, k = 2 curve).

### Numerics found by verification (not in the brief; flagged)

5. **The Python engine was wrong at both ends of the df range** — StudRangePy's u² grid (verify, before the fix): df 1, α = 0.01 gave q crit 1-14 % low (α = 0.001: up to 25 %); df 2, α = 0.001 up to 2 %; df 120, α = 0.001 2×10⁻⁴; **df ≥ ~500: garbage** (df 1000, α = 0.05: 1.3×10⁸). Beta 15 opens df 1-2 and the HSD's auto df can be large, so this had to be fixed. New `outer2` (new 476-536) integrates over s = eᵗ (t from ln 10⁻⁹ to ln 8, 4× the nodes) for df < 4, and over the spike 1 ± 12/√(2ν) (≥ 64 nodes) for 50 < df ≤ 25000; `scdf`/`spdf` are **rebound** to route those df there (`scdf_u2 = scdf` keeps the tested function under a new name; new 538-552). The pasted functions are not edited; `qsolve` picks up the routing by late binding. Result: q crit within 5×10⁻⁶ relative of SciPy over k 2-20, df 1-20000, α 0.1-0.001.
6. **The PPL engine had the same high-df failure** (df 240, α = 0.01: 4.123 vs 4.160; df 1000: −∞, a division by zero in the solver). `sr_SRCDF` gets the same spike window for df > 100 (new 834-856; new LOCALs `scSg, scLo, scHi` on the existing second LOCAL line, now 6 names). df ≤ 100 is unchanged code. And the menu modes use 48 inner intervals from **k = 6** (b14 428/461/497 → new 1277/1324/1374; was k = 11): at k 6-10 the 32-interval grid left q crit up to 0.05 off at α = 0.005. PPL worst case now k = 20, df = 3, α = 0.005: 0.008 (header "~4E-4" claim corrected).
7. **Plot pdf at q = 0** (new 600-606, 627-632): Python reads the density just right of 0, because for k = 2 it is not 0 (the grey k = 2 curve would otherwise start from the axis).

### Results, badge, diagnostics

8. **P-value / Critical value / HSD** (b14 411-512 → new 1280-1435): Python first, PPL fallback. df 1-2 are legal when Python answers; the PPL fallback keeps b14's message, now *"df below 3 is not supported: using df = 3. (PPL engine: MicroPython did not answer)"*. HSD "auto df" is df < 1 (b14 490: < 3). The INPUT help lines say *"df error (1+ with Python, 3+ PPL; 0 = ∞)"*.
9. **Engine badge** `sr_Badge` (new 1010): green panel *engine: MicroPython 1.9.4* or red *engine: PPL (Python unavailable)*, under the title of every result page (`sr_ShowRes(…, bdg = 1)`), on the plot (new header, y 29), the yardstick and the diagnostics page. `srEng` (file-level) and `SR_ENGINE` (EXPORT) record which engine produced the last result; `StudRange()` resets both at start.
10. **Diagnostics (Python)** — new menu item 5 (`sr_DiagMode`, new 2084): sets k = 3, df = 12, q = 3.5, runs mode 0 through the bridge, times it with `TICKS`, compares with SciPy's 0.9300045147 (tolerance 10⁻⁵): *"Python bridge OK (n ms)"*, *"…answered, but WRONGLY"* or *"…NOT answering"*; shows the last Python mark (`SR_PZ`) and the engine of the last result. Help moves to item 6, Quit to 7 (menu strings unnumbered, as before).
11. **`sr_ShowRes`** (b14 383-405 → new 1038-1063): composed on G1, one blit (review §3 sweep 4); held by the new `sr_WaitAny` (new 986, the house xxWaitAny: key OR tap, capped finger drains; review §3 sweep 3); takes a footer and a badge flag; returns the key (−1 for a tap). Footers *"any key or tap = menu"* etc. in dodger blue.

### The plot (b14 535-745 → new 1597-2072)

12. Cache build moved to `sr_Cache` (Python first; b14 566-598 are its PPL fallback, unchanged apart from the variable names `cbK, cbV, cbQo`); Python returns the **pdf itself** (`spdf`) instead of central differences.
13. **Two-colour tails**: beyond q crit light orange RGB(255,240,220), beyond q obs light red RGB(255,235,235), both RGB(250,190,160).
14. **α ladder** as five thin labelled ticks above the plot (q crits from the cache once per build, `pmLad`; current rung orange; an overlapping label is skipped).
15. **Soft keys** `DRAWMENU({"α−","α+","k−","k+","df","Menu"})` after the blit (new 1875); a tap at y ≥ 218 is slot `MIN(6, IP(x/53.4)+1)`. Hardware equivalents: Up/Down = α−/α+, − / + = k−/k+, Enter = Menu, 0 = q obs to q crit. The footer text is gone (the strip owns y 218-239).
16. **Free α**: a press on the right-hand CDF axis strip (x ≥ px2 − 4 = 286, y in the plot) and its drag samples set α = 1 − (CDF height), shown *α = 0.037*; an orange handle marks it on the axis and a dotted line runs from the CDF at q crit (`sr_InvC`, any α).
17. **Tap the q crit box** (x ≤ 186, y 12-27, a light-orange panel): q obs = q crit, p = α (harness: *α = 0.100, q crit = 3.204 | q obs = 3.204, p = 0.1000*).
18. **q obs drag kept exactly**: b14 726-735 (`WAIT(-1)`, types 0/1, `SIZE >= 3` check, no in-loop drain) is unchanged inside `IF pmDrag==1`; the type-0 press now decides what a touch is for (1 plot, 2 α strip, 3 q crit box, 4 soft keys) and the type-1 samples keep it. Drains (`sr_Drain`, `sr_DrainT`) run only after an action (`pmAct > 0`), never after a drag sample.
19. **Plot box** 34..306 × 34..200 → 34..290 × 54..200 (room for the header's three lines and the ladder labels; a wider CDF strip).
20. **Plot menu** (Enter or the Menu soft key): Set α, q obs = q crit, Change k, Change df, H₀ simulation, k = 2 curve on/off, Clear the simulation, Help for this plot, Leave the plot. The two Python items (and Clear) are **hidden** when the cache came from PPL (a 6-item CHOOSE instead of 9).
21. **H₀ simulation** (Python only; `sr_SimRun` new 1242, `simulate` new 636): asks m; the simulation's df is k(m − 1), and the plot is rebuilt for it if different (a MSGBOX says so). 2,000 replicates of k groups of m N(0,1) values (urandom, Marsaglia polar); per replicate q and whether ANY pairwise |t| > t crit (t crit from `sr_TCrit`: `STUDENT_ICDF` inside IFERR, checked with `STUDENT_CDF`, else bisection — CICatcher's pattern; q crit computed exactly by `qcrit` in Python). A teaching page (*"Of 2,000 replicates, 5.1 % exceeded q crit = 3.773 (α = 5.0 %)"*, the pairwise-t rate, *"Tukey's q holds the family at α; separate t tests do not."*), then a 40-bin magenta step histogram on the density and a 3-line panel top right.
22. **k = 2 comparison curve** (Python only; `sr_Cmp`, `curve2`): grey density for two means at the same df on the same grid; the y scale is refitted over both curves.

### Teaching and the rest

23. **HSD yardstick** (`sr_Yard`, new 1437): after the HSD page (Enter or a tap), up to six means (INPUT per group count; defaults an example set, remembered in `srYM`), number line with NiceNum ticks, staggered labels, an orange HSD-length bar from the lower chosen mean, bracket and verdict in green (`> HSD: significant`) or red (`≤ HSD: not significant`). Taps (nearest mean within 14 px) or ⇆ + Enter; Esc back.
24. **Help** (b14 514-530, one 10-line page → four 8-line pages, new 2145): formulas; **why q and not t** (k = 2: q = t·√2; family-wise error); the two engines (fast path, fallback, badge, diagnostics, *test with the Terminal open*); the plot's gestures. Plus "Help for this plot" in the plot menu.
25. **`StudRange()` returns** *"StudRange: q crit = …, p = …, HSD = … (engine: …)"* (house rule; b14 ended with nothing).
26. **Soft-key "More" pages** (Roger's new convention, 16 Oct 2026): **not applied** — the plot's soft-key actions fit in six (Menu opens the rest), and the yardstick and result pages have no soft keys. Stated in the header and the guide.
27. **Header** rewritten in the house shape: beta 15, the two-engine explanation, "NOT YET RUN ON HARDWARE", the dated *What changed in beta 15*, b14/b13/b12 history, file map, licence, AI line, firmware line; the "Companion: StudRangePy" line is gone (retired).
28. New tagged helpers: `sr_WaitAny, sr_Badge, sr_Busy, sr_PyRun, sr_PyNum, sr_InvC, sr_TCrit, sr_Cache, sr_Cmp, sr_SimRun, sr_Yard, sr_DiagMode`; new file-level LOCALs `srEng, srQmax, srTX, srTY, srYM`.

## Verification (`verify_StudRange.py`; full output in `verify_StudRange_out.txt`)

The script extracts the `#PYTHON srq` text from the shipped file and runs it with stub `hpprime`/`urandom`; mirrors the PPL engine; and runs the real PPL source in `ppl_run_v1` with `PYTHON(srq)` replaced by the real block reading and writing the harness's PPL globals (and, for the fallback, doing nothing, as on a calculator without Python).

```
1. MicroPython engine (the block as shipped) vs SciPy
  ok   python q crit, max relative error < 1E-5 (5.04e-06)        k 2-20, df 1..20000, alpha .1-.001
  ok   python p at the true q crit, max relative error < 1E-4 (2.42e-05)
  ok   Lessons s11 case k=4 df=3 a=.005 -> 15.4503 (15.4503)
  ok   df = infinity (100000) matches SciPy (0.0355570 vs 0.0355570)
  ok   Diagnostics probe value F(3.5;3,12) within 1E-5 of 0.9300045147 (0.9300045147)
2. PPL engine (mirror) vs SciPy, the menu resolution (64 x 32/48)
  ok   PPL q crit, max absolute error < 1E-2 (8.1e-03 at k=20 df=3 a=0.005)   df 3..1000
  ok   sr_LGAM (Lanczos) vs lgamma < 1E-12 (1.8e-15)
3. The plot cache (32 x 48) and spdf vs SciPy
  ok   cache CDF max abs error < 5E-4 (3.0e-04, k = 20, df = 2)
  ok   cache pdf max error relative to the peak < 1E-2 (5.7e-03)
  ok   cache(): 65 + 65 + 1 = 131 crossings
  ok   cache(): CDF monotone, last element in [0,1] (F(qmax) = 0.99981, qmax = 8.400)
4. The H0 simulation (simulate(), urandom -> random.random), 10,000 replicates each
  ok   k=3 m=5 a=0.05: q > q crit 5.19 %   any t > t crit 11.56 % vs theory 11.56 %
  ok   k=4 m=8 a=0.05: q > q crit 5.17 %   any t 19.64 % vs 19.49 %
  ok   k=6 m=4 a=0.10: q > q crit 10.10 %  any t 53.13 % vs 52.85 %
  ok   k=3 m=5 a=0.01: q > q crit 1.00 %   any t 2.49 % vs 2.51 %
5. k = 2: q = t * sqrt 2
  ok   q crit(k=2) = sqrt2 * t crit, SciPy and the Python engine (1.8e-08)
6. The real PPL source in the harness
  ok   harness sr_SRCDF(3.5,3,12) = 0.930005, (4,5,20) = 0.930413, (5,4,3) = 0.890110 (SciPy alike)
  ok   harness sr_SRCrit(.05,3,12) = 3.77293 (SciPy 3.77293)
  ok   P-value via Python and via PPL: EP_QPVAL 0.069995 (SciPy 0.069995), right badge, SR_ENGINE
  ok   Critical value df=2 via Python: 8.3308 (SciPy 8.3308), no MSGBOX
  ok   Critical value df=2 via PPL: raised to df 3 with the beta 14 message (5.9096)
  ok   HSD = 1.3652 (SciPy 1.3652); yardstick verdict |x̄1 − x̄3| = 2.500 > HSD: significant
  ok   plot via Python: badge, soft keys; q crit tap gives q obs = q crit and p = alpha
  ok   plot via PPL: red badge and a 6-item plot menu without the Python extras
  ok   simulation through the bridge (2,000 replicates); k = 2 curve arrived, legend drawn
  ok   Diagnostics with Python answering ('Python bridge OK') and failing ('NOT answering')
  ok   help: 4 pages, no line estimated clipped
FAILURES: 0
```
A layout pass over edge cases (k = 20, ν = ∞, α = 0.0001, df = 1; both engines; every page) found no text estimated clipped.

## Gate (`bash check.sh out/StudRange_beta15.txt out/StudRange_beta14.txt`)

```
--- 1. kit lint (errors) ---
out/StudRange_beta15.txt:2229: ERROR: unbalanced: unclosed blocks: 1 openings too many [no fact]
    -> the allowed Python-block case: with the #PYTHON block blanked, kit lint reports 0 errors
--- 2. ppl_check tally (NEW)  ---   1 E7
--- 2. ppl_check tally (ORIG) ---   1 E7          (the same E7 as b14: Home's X as the MAKELIST counter)
--- 2b. HARD errors in NEW (E2 E3 E6 E8 E10 E11) --- none
--- 3. lint_ppl structural ---
  PROBLEM line 749: block depth went negative       (the #END of the Python block; allowed)
  PROBLEM unbalanced blocks: final depth -1         (same cause; 0 with the block blanked)
  PROBLEM line 939: LINE_P targets 'dvG', not a GROB  (known noise: sr_DotV's GROB parameter)
  (EXPORT-discipline lines for SR_* are known noise: the bridge needs EXPORTed globals)
--- 4. full parse ---
  PARSE FAIL at the first prototype line (the tool's limit; b14 fails the same way at 153).
  With prototypes, EXPORTs and file-level LOCALs commented out: PARSE OK (30 functions).
--- 5. 2228 lines, 81,442 bytes (approx.); no non-ASCII in code; Python block ASCII, no tabs.
```
`fleet_names_v2.py` over the newest version of every program (24 files): 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## (b) DEVICE TEST CHECKLIST — least risky first

1. **Paste and compile.** The file is long (2,228 lines); paste, do not retype. If the paste fails, note the line: the Python block is 315-749.
2. **Diagnostics with the Terminal open** (menu item 5). Expect *"Python bridge OK (n ms)"*, F = 0.930005, SciPy 0.930005, *"Last Python mark: finished mode 0"*. Note the ms. If it says NOT answering: the Terminal's traceback, and `SR_PZ` in Home (empty = the script never started — an import or the block itself; `started` = reading `SR_MODE` failed; `read mode 0` = the computation or the write-back failed). This one probe tests every bridge piece the results use: `hpprime.eval` reading an EXPORTed real, writing one with `"%.10f"` text, and a string mark.
3. **Critical value** α = 0.05, k = 3, df = 12 → **3.7729** with the **green badge**; time it (expect ~1.5 s). Then df = 2 → **8.3308**, no message; df = 1 → **26.9755** (slower: ~4× the nodes; time it).
4. **P-value** q = 3.5, k = 3, df = 12 → P(Q ≥ q) = **0.07000** (0.0699955), green badge. In Home: `SR_ENGINE` = "Python".
5. **HSD** α = 0.05, k = 4, m = 8, MSE = 1, df = 0 → q crit **3.8612**, HSD **1.3652**. Enter → the yardstick: accept the example means; tap x̄1 and x̄3 → green *"|x̄1 − x̄3| = 2.500 > HSD: significant"*; tap x̄1 and x̄2 → red *"… = 1.000 ≤ HSD: not significant"*. Check the labels' glyphs (x̄ via CHAR(57344), −, ≤) and that close means do not overprint.
6. **The plot** k = 3, df = 12, q obs = 3.5: the red progress bar fills **from Python** (`hpprime.fillrect`) — time the build (estimate ~5 s); the green badge; two-colour tails (p region red from 3.5, α region orange from 3.773, darker beyond); ladder ticks .10 .05 .025 .01 .005 above the plot; the soft-key strip α− α+ k− k+ df Menu. **Text widths** are estimates: the q obs readout at x = 124, the badge panels (150/190 px), *"tap box: q to q crit"* at x = 192 and the sim panel are the ones to look at.
7. **Touch on the plot.** (a) Drag across the plot: q obs follows, p sweeps (beta 12's behaviour, unchanged). (b) Press on the right-hand edge strip (on the 0.25…1.00 labels) and drag up/down: α changes continuously (*α = 0.037*), the orange handle and the dotted line follow, the ladder tick turns grey. (c) Tap the orange q crit box: q obs jumps to q crit, p = α. (d) Lift after each: nothing else happens.
8. **Soft keys.** Tap α−, α+, k+, k−, df, Menu. **If tapping the strip does nothing**, WAIT(-1) is delivering strip taps as type 3 "Click" only (WaitLab's 2014 observation, not handled because type 3 is not device-verified) — every soft key has a hardware key (⇅, + / −, Enter), so the plot still works; tell Claude and the next version will read the strip with MOUSE instead. Keys: ⇆ q, ⇅ α, + / − k, 0 q to q crit, Enter menu, Esc leave.
9. **k+ rebuilds** with Python: the bar fills, the badge stays green, the plot redraws for k = 4.
10. **H₀ simulation** (Enter → H0 simulation, m = 5): no df message (3·4 = 12), a bar, then the page *"Of 2,000 replicates, ≈ 5 % exceeded q crit = 3.773"*, *"any pairwise t > t crit = 2.179: ≈ 11-12 %"*; back on the plot, the magenta histogram follows the blue density and the panel shows both rates. Time it. Try m = 8 (df 21: the MSGBOX, then a rebuild).
11. **k = 2 curve** (Enter → k = 2 curve on/off): a grey curve starting high at q = 0 (≈ 0.56 at df 12), the y scale refitted, "k = 2" in the legend; toggle it off.
12. **The fallback.** Force Python to fail: in the Connectivity Kit, edit StudRange ITSELF (not a second copy beside it — two programs with the same routine names share one pool on the calculator) and add the line `import nosuchmodule` straight after `#PYTHON srq`; paste the clean file back afterwards. A top-level import of a missing module stops the script silently — exactly the failure the guard is for. Then: Critical value df = 12 → 3.7729 with the **red badge** (about a minute); df = 2 → the *"df below 3 is not supported … (PPL engine: MicroPython did not answer)"* message, 5.9096; the plot builds with PPL, red badge, and the plot menu has 6 items (no simulation, no k = 2 curve); Diagnostics says NOT answering, last mark *none*.
13. **Help** (4 pages; any key or tap turns, Esc leaves) and **Quit**: Home shows *"StudRange: q crit = …, p = …, HSD = … (engine: Python)"*.

## (c) Not confirmed, or left as it was

- **Nothing of the bridge has run.** `hpprime.eval` reading EXPORTed reals and writing list elements (`EP_SRCDF(5):=0.1234567890`) one at a time is the documented pattern (NormExplorer writes a whole list in one eval; hp-prime-kit lists PPL→Python as unverified). Checklist 2 is the test. If list-element writes fail, the guard sends every plot to PPL and the badge shows it.
- **Soft-key taps through WAIT(-1)** (checklist 8): the plot keeps b14's `WAIT(-1)` loop as the brief required; whether a strip tap arrives as type 0 is unverified. Hardware keys cover every action.
- **Timings** for the Python cache (~5 s), df 1-3 (~4× nodes) and the simulation (~1 ms per replicate at k = 3, m = 5 — an estimate) are extrapolated from StudRangePy's 1.5 s q crit, not measured.
- **`STUDENT_ICDF`** is used only through `sr_TCrit`'s checked IFERR, with bisection on `STUDENT_CDF` as the fallback.
- **The "engine: MicroPython 1.9.4" text** is the brief's literal; the version is what PyProbe saw on the 2026-09-09 firmware, not read at run time.
- **PPL engine accuracy** at k = 20, df = 3, α = 0.005 is 0.008 (outer-grid limit); left, and stated in the header and guide. Python is exact there.
- **Unchanged on purpose:** `MAKELIST(0,X,1,…)` with Home's X in the PPL engine (b14; the E7), `BLIT_P(G0,G1)` two-argument form on the plot, the plot's `WAIT(-1)` loop, `sr_DotV`, the menu-mode result texts.
- **Soft-key "More" pages** not applied (item 26).
