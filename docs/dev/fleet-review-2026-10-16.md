# HP Prime Fleet Review — graphics, touch and teaching expansions
*Roger Metcalf & Claude · v1 · 16 October 2026 · reviewed against HP_Prime_Lessons_Learned v7e*

**What this is.** A sweep of all nineteen fleet programs in `D:\HP-Prime` (plus the MicroPython twin), read in full from the masters, looking for three things in this order: (1) ways to show off the Prime's colour screen and touch screen, (2) ways to teach the statistical idea better, (3) bugs and rulebook drift. Five independent reads were made, one group of programs each; the main findings were then re-checked against the source. Line numbers refer to the current master files (the versions in §1's table). The API facts in §4 were checked against HP's *Commands.pdf*, the *Command tree* and Jsather's WaitLab notes through `Library_Index.db`, not from memory.

**How to use it.** §2 is the list to clear before the programs go in front of a class. §3 is the once-over-everything sweep. §4–§5 are the new capabilities and the house touch standard. §6 is the program-by-program plan, §7 the new programs, §8 the order of work. §10 lists what this review found that belongs in Lessons Learned v7f. §11 is the short list of things only you can answer.

---

## 1 · Where the fleet stands

| Program | Touch today | Soft keys | Composes in G1 | Self-numbered CHOOSE | Palette | Footer form | Exit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NormExplorer beta 40 | Explorer only: tap/drag x₀ | – | plots yes; ZPanel, Diag, Help to G0 | **yes** 1706-1715 | own hex set | own | resets, no summary |
| Norm3 v2.2 | – | – | yes | n/a (arguments) | §13 (panel orange off) | §13 | RETURN |
| Burr3 v2.2 | – | – | yes | n/a | §13 (panel orange off) | §13 | RETURN |
| SampDist v2.1 | – | – | yes | **yes** 588-591 | §13 | three wordings | RETURN |
| StatDist v2.4 | – | – | nothing drawn (62 MSGBOX) | no | none | none | RETURN |
| PowerViz v2.2 | – (held keys via ISKEYDOWN) | – | yes | no | §13 + own fills | no spaces round `=` | RETURN |
| EpiStats v1.3 | – | – | **G0 throughout** | **yes** circled ①-⑦ 117-123 | own navy set | own | RETURN |
| ConTable2 v1.2 | – | – | nothing drawn (6 MSGBOX) | n/a | none | none | RETURN p |
| FEP v1.3 | – | – | nothing drawn (3 MSGBOX) | n/a | none | none | RETURN p |
| TrendTest beta 1a | tap a level on both plots; tap to advance | – | yes | **yes** 742-747 | §13 exactly | colons | RETURN |
| ChiTable beta 1k | grid, pages, bars, mosaic, curve | **yes** | yes | no | §13 — the reference | §13 | RETURN |
| BayesTree beta 5 | tap a node | – | **G0 throughout** | no | two magentas, ad-hoc ROC colours | mixed | falls off END |
| StudRange beta 13 | tap/drag q on the plot | – | plot yes; result pages G0 | no | off-house (navy, firebrick) | spaces | – |
| StudRangePy beta 14b | – | – | Python `hpprime` drawing | n/a | §13 | – | PRINT (Terminal) |
| CentralLimit beta 1a (app) | tap top panel = resample, bottom = curve | – | yes | values only (item 10 shows "A") | §13 exactly | §13 | app |
| GaltonBoard beta 1a | tap pegs = drop, tap bar = numbers | – | yes (G2 scene + G1 frame) | no (items 10-12 show A, B, C) | §13 exactly | spaces, CHAR arrows | RETURN |
| TestChooser beta 1a | buttons, path, table | – | yes | **yes** 688-690 | §13 + two extras | colons | falls off END |
| DNAMixLR beta 1 | – | – | plots yes; locus panel, table, help to G0 | **yes** 898-906 | §13 with off fills; grey footers | "any key" | falls off END |
| FDAES v3.4 | – | – | nothing drawn (35 MSGBOX) | **yes** 264-269, 281-287, 670-673 | none | none | 9-line MSGBOX |

In numbers: touch in 8 of 19; labelled soft keys in 1; fully double-buffered in 10; self-numbered menus in 7 (the pending list in CLAUDE.md names six — **TrendTest is the seventh**); four programs draw nothing at all; five programs have message boxes the 5-line MSGBOX limit will have been cutting off. Nothing in the fleet uses `FILLPOLY_P`, `TRIANGLE_P`, alpha blending, the scaled `BLIT_P`, pinch, rotate or long-press.

---

## 2 · Fix before the next class

Ordered by what it costs in front of students. Everything here was confirmed in the source.

**A. Runtime errors that open the Program Editor (the reset-to-escape failure, §7)**

| Program | Lines | Trigger | Fix |
| --- | --- | --- | --- |
| EpiStats | 785, 790 | Risk page 1 with c = 0 or a = 0: `Rexp/Runexp` or `Runexp/Rexp` divides by zero | guard both branches; print "undefined (no events in one group)" |
| EpiStats | 1605, 1615, 1706 | stratified RR/IRR: `/RR_crude`, `/MIN(RR1,RR2)`, `/IRR_crude` with a zero | same guard; the OR branch at 1509 multiplies and is safe |
| ConTable2, FEP | 148-156; 108-116 | `COMB(N, r1)` overflows the real range near N ≈ 1,600 with balanced margins | cap at N ≤ 2000 and use EpiStats' log-space Fisher (211-257), or fold both into EpiStats (§6) |
| Burr3 | 171, 183 | C = K = 0.25 gives xmax ≈ 6.5·10³⁶·S: 37-digit tick labels, a blank plot | clamp xmax, or raise the floors so K·C ≥ 0.5, and say so on screen |
| BayesTree | 147-149 | the GETKEY drains round `WAIT(-1)` do not drain touch, so the finger lift that opened a node page can close it; the 60-s timeout closes it mid-lecture | capped `bt_Drain()` before 148; GETKEY+MOUSE polling instead of `WAIT(-1)` |
| StatDist | 629 | Poisson "between" with k_lower = 0 calls `POISSON_CDF(λ, −1)` — behaviour unverified | guard k ≥ 1 |

**B. Wrong numbers on screen**

| Program | Lines | What shows | Fix |
| --- | --- | --- | --- |
| SampDist | 385 | comparison title prints σ as `semax·√n₁` — right only when n₁ is the smallest n (n = 100, 30, 5 prints σ = 67.08 for σ = 15) | pass σ into `sd_drawCmp` |
| EpiStats | 321-329 → 605, 808, 815, 1115 | `es_FmtCI` blanks only `{0,0}`; the `{0,999}` sentinel from `es_CalcRRCI` prints "(0.00-999.00)" | blank any CI containing 999 |
| EpiStats | 737, 1220 → 827, 1311 | `ERR := RR − 1` on the 999 sentinel prints "998.000 (99800.0%)" | same sentinel check |
| EpiStats | 1006-1010, 928-958 → 1045, 1152 | `EP_chisq`, `EP_sens_CI` only set inside guards, then printed — can be last run's values | clear at module entry |
| DNAMixLR | 353, 372 → 476-477, 651-653, 731, 895 | a locus with LR = 0 (an exclusion) is skipped and the combined LR is shown without qualification: "EXCLUDED at locus 2" reads "moderately strong support for Hp" | show the exclusion in red where the combined LR goes; note that only dropout models rescue it |
| DNAMixLR | 116-127 → 456 | `dmBig` prints "0.000" for 10⁻⁴ ≤ v < 5·10⁻⁴ (threshold at 120, three decimals at 126); P(E\|Hd) for two unknowns at p = 0.05 reads "impossible" | scientific below 0.01, or four decimals |
| FDAES | 449-480 | the M3 module never reads the sex set in Setup, though Mincer's figures are sex-specific | read it; see also §11 on the stage-H figure |
| NormExplorer | 1652-1653 vs 1687, 1731 | help promises `NE_Z, NE_X, NE_P` in Home; `ne_ResetAll` on exit zeroes them | keep those three, or `RETURN` a summary string |
| StudRange | 673 | plot mode overwrites `EP_QCRIT` with the fast-grid interpolation, replacing CritMode's full-precision value | do not store, or label it |

**C. Output the student never sees (MSGBOX shows about five lines, §3)**

| Program | Boxes | Note |
| --- | --- | --- |
| StatDist | every result box (e.g. 247-258: ten `CHAR(10)`s), help 213-217 | the probability is the **last** line — if §3 holds, the answer has never been visible. Verify on the G2 before anything else in StatDist. |
| FDAES | 20 of 35 boxes (320-328, 419-430, 470-478, 495-506, 524-535, 562-575, 617-632, 681-690, 702-713, 798-810, 811-824, 838-850, 897-909, 910-922, 923-936, 943-954, 955-970, 971-989, 990-1004, 1009-1017) | every result, the report template, the threshold table and all of About |
| EpiStats | all eight help boxes (About 7 lines, Table 8, SensSpec 11, RiskOdds 13, CI 8, MH 10, Kappa 13, Variables 11) | the Landis-Koch scale at 2061-2067 is never seen |
| PowerViz | help 595-603 (9 lines) | the key legend and Cohen benchmarks are below the fold |
| ConTable2, FEP | long single lines wrap (161-164, 183-186; 132-138) | past five once wrapped |
| StudRange | `sr_HelpMode` 460-470 passes 10 lines at 22 px: lines 9-10 land at y 206 and 228, under the footer | 8 lines, or tighter spacing |
| EpiStats | 625-630 | "Quick Reference" on page 3 is drawn under the footer and below y = 240 — dead on screen; 583 and 826-827 also run 2-4 px into the footer |

**D. Screens skipped by a stale keypress (§7 drain-wait-drain)**
SampDist 329, 400, 574 · EpiStats `es_WaitKey` 333-343 · Norm3 294 · Burr3 326 · BayesTree 194, 234, 299, 361. Each is `UNTIL kk > −1` straight after an INPUT or CHOOSE; the OK press can satisfy it. One drain line each. NormExplorer's device-observed case (572) is why this rule exists.

**E. The verification pipeline itself**

| Where | Finding |
| --- | --- |
| `fleet_names_v1.py` line 65 | the tag regex `^[a-z0-9]{2,4}_\w+$` reads `calc_` as a tag, so StatDist's ten `calc_*` stubs (787-796) pass as tagged — the v7d "0 untagged" result was a false pass. Require the file's own tag (or a known list). |
| NormExplorer 470 | the Python sampler does `from random import random`; §8 says `random` is absent and `urandom` present, so the xorshift fallback (471-490, three bridge crossings to seed) runs on every call. Try `urandom` first; the comment at 463-468 is stale. |
| DNAMixLR 410, 417-425 | `LOCAL g1 … g6` and `INPUT({g1 … g4})` — `G1…G6` are the graphics variables this program uses at 688 and 768. Variables are case-sensitive so it probably parses, but `ppl_check_v2.py` only scans file-level LOCALs. Rename before the first paste. |
| BayesTree 370, 450 | `LOCAL fp` / `INPUT({tp, fn, fp, tn})` — the documented exception §2 says never to rely on |
| EpiStats, FDAES | no `#pragma mode( separator(.,;) integer(h32) )` line; every other program carries it |

---

## 3 · Fleet-wide sweeps (once, across every file)

1. **Strip the self-numbering from CHOOSE strings** — the item you asked for on the next sweep, now seven programs: DNAMixLR 898-906 (Quit is item 10, dispatched on `mnI == 10`, shown as "A"); EpiStats 117-123 (circled digits, which are also unverified glyphs); FDAES 264-269, 281-287, and the FDI tooth strings 670-673 ("11  Upper central incisor" → "Upper central incisor (11)" as 356-361 already do); NormExplorer 1706-1715 (Help is item 10 → "A", Quit "B"); SampDist 588-591; TestChooser 688-690; **TrendTest 742-747**. On-screen references that change with them: TrendTest 755, 701, 704; FDAES 741 ("methods 2, 4, 7, or 8" — 7 and 8 are internal codes the user never sees) and 834; ChiTable help 1294, 1313, 1315 (correct today, hard-coded).
2. **Message boxes over five lines become drawn pages** (§2.C). TrendTest `trHelp` 677-716 and ChiTable `csHelp` 1282-1323 are the pattern.
3. **One wait idiom everywhere**: capped `xxDrain()` + `xxWaitAny()` polling GETKEY and MOUSE (ChiTable 286-306, CentralLimit 705-726, GaltonBoard 176-198). Key-only holds that ignore taps today: EpiStats, StudRange result pages, BayesTree sub-views, DNAMixLR, Norm3, Burr3, SampDist, PowerViz's power-vs-n page. And record the finding that **a GETKEY drain does not drain touch**.
4. **Compose in G1, blit once**: EpiStats (327 `TEXTOUT_P` on G0 — a white flash per page), BayesTree (every frame), StudRange result pages 335-341, NormExplorer's ZPanel/Diag/Help and its animation captions (1525, 1535 — painted after the blit, so they flash each frame), DNAMixLR's three panels.
5. **Cache the density** (§6): PowerViz calls `pv_NPDF` four times per pixel column — 1,188 NORMALD evaluations plus 1,188 user-function calls per frame while an arrow is held (346-347, 361-362); Norm3 and Burr3 evaluate the same 290 points three times (870 calls; Burr3's pdf has two `^` each); NormExplorer recomputes the N(0,1) reference per frame (1931-1938); ChiTable `csCurve` twice per column (1185, 1194); SampDist twice (240, 252); DNAMixLR plot 2 recomputes three values already cached in `ptVals` (804). None of this is felt on a key press; all of it is felt the moment a finger drags.
6. **House footer and palette**: adopt CentralLimit's footer form exactly (`+/- = n, tap top = redraw, Ent = menu, Esc = quit` — commas, spaces round `=`, dodger blue). Off today: PowerViz 432 (no spaces), TrendTest 541/625/627 and TestChooser 399/455/511/604/664 (colons), GaltonBoard 324 and StudRange 637 (spaces), BayesTree 529 (green, no `=`), DNAMixLR (grey, "Any key"), SampDist (three wordings), NormExplorer (five wordings). Palette: NormExplorer's own hex set (its shading is orange where every other program's is blue); EpiStats' navy set; StudRange off on five colours; BayesTree's two magentas (200,0,200 vs 255,0,255 at 142, 191, 226-228, 528) and ad-hoc ROC colours; PowerViz's PowNView magenta 255,0,255 (448); Norm3/Burr3 panel border 255,165,0 (house 255,69,0); DNAMixLR fills #FFF8F0 / #FFE0E0 (house #FFF0DC / #FFEBEB). One arrow-glyph convention (ChiTable's `CHAR(8592)+CHAR(8594)` vs literal ⇆/⇅) and one subscript convention (`CHAR()` vs literal) — both render; pick one.
7. **Headers and version strings**: PowerViz still carries the old header (2-6: no licence, no AI note, no firmware line); FDAES likewise; StatDist has two header blocks (1-26, 28-68) and says v2.3 at 35 and 213; NormExplorer's file map says 2074 lines (25) for a 2086-line file; StudRange 57 says "bisection" for an Illinois regula-falsi solver and 73 says beta 12a; StudRangePy 25 and 46 likewise; BayesTree 21-23 says beta 4 has not run; EpiStats says v1.2 at 35, 116, 1992; NormExplorer 283-284 documents `NE_SRC` 0/1/2 while 3 is set at 1289.
8. **End with a summary**: BayesTree, TestChooser and DNAMixLR fall off `END`; FDAES ends with a nine-line box that needs a key. `RETURN "TestChooser: " + TC_TEST` and the like.
9. **LOCAL hygiene when next touched**: seven-name LOCAL lines (Norm3 131/134/135, Burr3 142-145, SampDist 198, BayesTree 241/367/368); bare lowercase `x, y, i, f, p, z` and `C, K, S` shadowing Home reals (Norm3, Burr3, StatDist 360/694, CentralLimit 119/121); `K` used as the `MAKELIST` dummy in ChiTable, GaltonBoard, CentralLimit and DNAMixLR, clobbering Home's K on every call — a tagged dummy costs nothing; FDAES's 100+ one-variable LOCAL lines (119-229).
10. **Fix the name checker** (§2.E) and re-run it across the fleet before any of this is pasted.

---

## 4 · What the Prime can do that the fleet does not use yet

Checked against `Library_Index.db` (HP's *Commands.pdf* and *Command tree 13217.pdf*, Jsather's WaitLab notes, the corpus). **Documented and corpus-used is not device-verified**: none of these is in Lessons Learned §3's confirmed list, so the probe in §7.1 comes before any program depends on them.

| Capability | Call | Documented behaviour | Corpus | Status |
| --- | --- | --- | --- | --- |
| Translucent fills | `FILLPOLY_P([G], {(x,y),…}, color, alpha)`, alpha 0-255 | fills a polygon with transparency | 91 files | documented, **not verified by us** |
| Translucent / gradient triangles | `TRIANGLE_P([G], x1,y1,x2,y2,x3,y3, c1,[c2,c3],[alpha])` | one triangle; three colours blend between the vertices; alpha | 90 files (ColorWheel, Colores) | documented, **not verified** |
| 3-D surfaces | `TRIANGLE_P([G], points, triangles, {rotmat,"N",eye,{xmin…zmax}}, zstring)` with `TRIANGLE_P(G)` for the z-buffer | a whole mesh in one call with rotation, perspective and per-pixel depth | Advanced Graph 3D (in the Project), 3ddrawing | documented, used, **not verified by us** |
| Zoom by copying | `BLIT_P(G0, dx1,dy1,dx2,dy2, G1, sx1,sy1,sx2,sy2)` | stretches the source rectangle into the target rectangle | 180 files | 4-arg form verified; 10-arg **not** |
| Two fingers | `MOUSE` → `{ {x,y,x0,y0,type}, {x,y,x0,y0,type} }`, one list per finger, empty when up | non-blocking; types 0 New · 1 Completed · 2 Drag · 3 Stretch · 4 Rotate · 5 LongClick | 427 files | first finger verified; second **not** |
| Gesture events | `WAIT(-1)` → `{type, x, y, [dx, dy]}` | 0 Down · 1 Move · 2 Up (no x, y) · 3 Click · 5 Stretch · 6 Rotate (angles in 1/32 circle) · 7 Long click (1 s) | WaitLab: a tap on the menu strip (y ≥ 219) arrives as `{3,x,y}` only; a drag is `{0,…} {1,…}… {2}`; a flick ends `{1,65535,y}`; a stretch is `{0,a} {0,b} {5,…,dx,dy}… {2}` | 0 and 1 verified (§7); 2, 3, 5, 6, 7 **not** |
| Python drawing | `hpprime.fillrect(gr,x,y,w,h,edge,fill)`, `line(gr,x1,y1,x2,y2,c)`, `pixon(gr,x,y,c)`, `textout(gr,x,y,text,c)` | — | StudRangePy 283-344 | **de facto verified**: StudRangePy's plot ran on the G2 (its header, line 16); §8 still says "not yet verified" |

**Record this trap now:** the type numbers in a `MOUSE` list are a *different table* from the type numbers in a `WAIT(-1)` list — Drag is 2 in one and 1 in the other, Stretch 3 versus 5. Any pinch or long-press handler must say which call it is reading.

**What it unlocks once probed:** a shaded region as *one* translucent polygon instead of 272 vertical `LINE_P` fills (faster, and α/β/power regions can finally overlap visibly instead of painting over each other); a 3-D bivariate normal a student rotates with a finger; pinch-to-zoom on any plot; long-press as the "what is this?" gesture on a plot element; a two-finger spread to set an interval width directly on the axis.

---

## 5 · The house touch standard

ChiTable beta 1k is the model — every idiom below has run on the G2 and the G1. Because the calculator pools every program's routines (§5), there is no shared library: each program carries its own tagged copy, and `fleet_names_v1.py` polices the names. The practical form is a **`TouchKit_template_v1.txt`** in `D:\HP-Prime` with an `xx` tag to search-and-replace, plus the fleet rule that new programs start from it.

| Idiom | Where it lives today | What it does |
| --- | --- | --- |
| `xxDrain()` | ChiTable 286-291; CentralLimit 705-710; GaltonBoard 176-181 | wait for the finger to lift, give up after one second via `TICKS` |
| `xxWaitAny()` | ChiTable 294-306; CentralLimit 715-726; GaltonBoard 186-198 | drain keys and touch, wait on GETKEY *and* MOUSE, drain again — the only page-hold the fleet should use |
| Soft-key strip | ChiTable 704, 711, 724-727, 745-747 | compose in G1, `BLIT_P`, then `DRAWMENU({…})` every frame; a tap with y ≥ 218 is slot `MIN(6, IP(x/53.4)+1)`; hardware keys stay as shortcuts; the footer string is emptied while the strip is up |
| Hit boxes recorded while drawing | ChiTable 1012-1013, 1068-1069, scanned 1135-1139 | the drawing code fills `xxTX1…xxTY2`; the handler scans them, so the two cannot disagree |
| Geometry as file-level constants | ChiTable 1340-1343; PowerViz 83-84; CentralLimit 107-109; GaltonBoard 84-90 | plot box, grid origin, cell pitch — shared by drawing and hit-testing (§6) |
| Palette as hex constants in `xxInit()` | ChiTable 1331-1336 | one place, §13 values, no `RGB()` calls inside draw loops (PowerViz builds eleven per frame, 292-302) |
| Press-vs-drag | ChiTable grid; TrendTest 652-662 | act on the first MOUSE sample as the press; treat > 8 px of movement as a drag; redraw per sample from a cached density |
| Engine badge | (needed by the StudRange merge, §6) | the header names which code produced the result — "engine: Python" / "engine: PPL" — with a diagnostics item that runs a trivial probe (§9) |
| Colour semantics | CentralLimit, GaltonBoard, ChiTable | blue = data / the distribution; magenta = theory / derived; green = mean marker / detected; red = "you are here"; orange = frames and totals; dodger blue = footers |

Two conventions to decide once and write into §13: arrow glyphs (`CHAR(8592)` style or literal ⇆/⇅) and subscripts (`CHAR(8320)` style or literal). Both render; the fleet has both.

---

## 6 · Program by program

Each entry: what to do first, the one showcase feature, then the touch, graphics and teaching expansions worth building, with effort (S = under an hour of code, M = an afternoon, L = a day or more; all before device testing).

### NormExplorer beta 40 — the flagship
*Fix first:* menu numbering; the `random` import; the `NE_Z/NE_X/NE_P` contradiction; cache the N(0,1) reference; captions onto G1.
*Showcase:* **drag either bound of a between/outside interval** with the area value riding the shaded region — today a tap collapses mode 3/4 to a left tail (657); compare the finger's pixel x to both bounds' pixel x and move the nearer one (~25 lines on the existing drag), plus a soft-key strip `{"Bands","Ref","Centre","Shade","Hist","Menu"}`.
*Touch:* grab μ by touching the mean line (±8 px) and σ at the shoulder, snapped on lift (M); make every result view live — in `ne_ShowCurve` (595) poll GETKEY+MOUSE and let a tap inside the plot drop straight into the Explorer with the shading kept (S); tap a histogram bar for its numbers (edges already at 1890-1891) (S).
*Graphics:* fill the histogram bars (`RECT_P` for three `LINE_P`, 1896-1898) (S); animated shading sweep from the edge to x₀ over ~10 frames with the running area (S); CDF overlay on a right-hand 0-1 axis with a dotted drop line (M); the standardize animation with a ghost outline, a skip key and captions composed on G1 (M); a power picture in Compare — shade curve 2 beyond a right-tail cut and print "power = …" from the cached `ndPdf2` (M).
*Teaching:* a z-ruler under the x-axis (needs room: NPBOT to ~200, or the footer into a soft-key strip); "height 0.242 is a density, not a probability; area to the left = 0.73"; left-tail and two-tailed critical values (931-950 do right-tail only).

### Norm3 v2.2 and Burr3 v2.2 — the pair
*Fix first:* cache the pdf (870 calls per frame become 290); a drain before the first wait; Burr3's xmax blow-up; 7-name LOCAL lines; panel orange.
*Showcase (Norm3):* **drag x₀ with a finger** and watch the blue area, the magenta point riding the S-curve with its drop line to a 0-1 right axis, and the readout move together; then **tap the S-curve for the inverse** — "drag up the S-curve to find the 90th percentile". Nothing like it exists in the fleet, and ~30 lines transplant from NormExplorer/ChiTable. **Norm3 is the best first touch upgrade in the whole fleet** (313 lines, one draw loop, named constants), and the result ports to Burr3 almost verbatim.
*Showcase (Burr3):* **three markers — mode (orange), median (magenta), mean (green) — sliding apart** as a finger drags C down, and "no finite mean" appearing in red the moment K·C crosses 1. Mode `S·((C−1)/(K·C+1))^(1/C)` for C > 1, median `S·(2^(1/K)−1)^(1/C)`, ICDF `x = S·((1−p)^(−1/K) − 1)^(1/C)` — verify all three against SciPy first.
*Touch:* parameter soft keys `{"C","K","S","x₀","View","Quit"}` (Burr3's S has no control today) (M); two-tap interval (M); tap "μ = undef" for "mean needs K·C > 1 (now 0.75)" (S).
*Graphics:* right-hand CDF axis (S); complement shading in light red (S); ghost of the previous parameter set (S); fitted-normal overlay with the Burr's own moments — skewed vs symmetric with the same mean and sd (S); log-x view for the heavy tail (M); a re-centre key for Norm3 (S).
*Teaching:* label "P(X ≤ x₀)" not "CDF"; name the three moment cases on screen; a CJ caption for Burr — "sentence lengths, time to re-arrest, claim sizes".

### SampDist v2.1
*Fix first:* the three missing drains (first thing to check on hardware); the σ in the comparison title; menu numbering; drop `sd_lblChars` (SIZE on strings is verified).
*Showcase:* **tap "n×4" on a soft-key strip** `{"n−","n+","n×4","μ,σ","Tail","Menu"}` and watch x̄'s curve snap to half its width while a **faint parent population N(μ,σ) stays put behind it** — the picture every textbook shows and this program never has (at n = 30 its peak is 18 % of x̄'s; label it so it does not read as an artefact). Then drag the bound and watch P(x̄ > a) collapse.
*Touch:* live result graph — split `sd_drawDist` into compose and wait, drag the nearer bound (M); a comparison cursor showing three P values at one x (M); tap a curve to select it (S).
*Graphics:* fill under the three comparison curves, widest first — "equal area, different spread" (S); animate n over ~8 frames (S); ~40 simulated means dropping as dots onto the axis (M); y-axis labels (S).
*Teaching:* print "σ = 15, σx̄ = 15/√30 = 2.74" on one line — σ versus σx̄ is *the* sampling-distribution misconception; the two-tailed critical value shades the central 1−α under the heading "Critical Values" (500-504) when students expect the tails — offer both and name what is shaded; the "4× n halves σx̄" slogan (395) with defaults 5/30/100 (519) does not show a 4× — use 10/40/160.

### StatDist v2.4 — the biggest rebuild
*Fix first:* confirm the MSGBOX cut-off on the G2 (§2.C); tag or fill the ten stubs; one header, one version string; ask the tail before the fields (x is asked then ignored in Between mode).
*Showcase:* **the drawn curve with a finger-dragged x** — blue pdf, the shaded area growing under the finger, "P(X ≤ x) = 0.8413" updating live, red x marker, green mean marker. It turns a text calculator into the thing the Prime is for.
*Foundation (M-L):* one `st_Plot(id, params)` and a `st_pdf / st_cdf (id, plist, x)` dispatch with parameters packed in a list (the 16-argument limit); everything else hangs off it. Then soft keys `{"P≤x","P>x","a<X<b","Zoom−","Zoom+","Edit"}` (S), two-tap intervals (S), tap-a-parameter-row to edit or drag the μ row / σ row (M), pmf bars with the chosen k red and a drag across bars for a range (M).
*Graphics:* a **family gallery** — six thumbnails (Normal, Exponential, Chi-square, t over N(0,1), Binomial, Poisson) drawn once, tap one to open it: the best single "look what the colour screen does" page in the suite and the answer to "which shape goes with which name" (M); normal-approximation overlays on Binomial, Poisson and t with the rule-of-thumb note when it fails (S each); 68-95-99.7 bands (S).
*The ten stubs* can mostly be filled from verified built-ins: Gamma(k,θ) CDF = `CHISQUARE_CDF(2k, 2x/θ)` (Erlang is the integer-k case; non-integer df in `CHISQUARE_CDF` is unverified), Beta(a,b) CDF = `FISHER_CDF(2a, 2b, b·x/(a(1−x)))` (same caveat), Maxwell(a) CDF = `CHISQUARE_CDF(3, x²/a²)`, Negative binomial P(Y ≤ k) = `1 − BINOMIAL_CDF(k+r, p, r−1)`, Hypergeometric by `COMB` in a short loop, Triangular / Cauchy / Fréchet / Gompertz closed-form. Verify each against SciPy.
*Teaching:* one "typical use" line per distribution in the INPUT title (Poisson: calls per shift; Binomial: convictions in n trials; Exponential: time to the next incident; t: small-sample means); "density at x (not a probability)"; P(X ≥ k) for discrete — the off-by-one that costs exam marks; the green mean marker right of the peak on Exponential, Chi-square and LogNormal is a one-glance lesson.

### PowerViz v2.2 — the best first touch upgrade among the plotters
*Fix first:* the per-frame cost (evaluate both curves once per column into two lists; inline NORMALD); help box to a drawn page; the header block; footer spacing; `IF kk == 7 OR ISKEYDOWN(7)` so a short tap is not lost; `LOCAL pv_Name()` routine heads — the only program using that form; either record it in §3 as verified by v2.1's hardware run or drop it.
*Showcase:* **drag H₁ with a finger** — the magenta curve follows, red/yellow/green re-shade live, the big POWER number turns red → orange → green as it crosses 0.5 and 0.8. The whole power lesson in one gesture. Then **drag the dashed critical line to set α** — red shrinks, yellow grows, green shrinks: the α-β trade-off as a physical motion, with "α = 0.037 (off the ladder)" until lift and a snap to the nearest rung.
*Touch:* vertical drag for n (S); soft keys `{"Edit","Tails","α−","α+","Pow-n","Menu"}` (S); tap a readout cell to edit it (S); in the power-vs-n view, drag along the curve to choose n from a cached sweep (M).
*Graphics:* n₈₀ for 80 % power drawn as a green dotted vertical and printed in the panel — the single most useful number for a methods student (S); a power-vs-effect-size view (S); area labels inside the fills, suppressed when narrow (S); a ghost of the previous H₁ for one frame (S); the α ladder as a graphic (S); an animated n sweep with an inset trail (M). Once alpha blending is probed, the three regions as translucent polygons that visibly overlap.
*Teaching:* "SE = σ/√n = 15/√30 = 2.74" with numbers (423); the Cohen word beside d/h ("d = 0.33, small"); one frame naming what Tails changed ("α split 0.025 each side, critical 1.96 instead of 1.645").

### EpiStats v1.3 — the most-used program, and the one with the most to fix
*Fix first:* §2.A and §2.B rows; the off-screen page-3 block; help boxes; `es_WaitKey` drains; the circled-digit menu; the stratified case-control table is transposed relative to modules 1-3 (b and c swap between 366-369 and 1402-1403 — the arithmetic is invariant, the student's "b" is not).
*Showcase:* **the prevalence drag on the diagnostic page** — a finger slides along a bar, PPV and NPV change in real time in big green digits, two curves sit behind them with a red marker riding the finger, and the student watches a "95 % accurate" test's PPV collapse to 16 % at 1 % prevalence. Two formulas per frame; the most-misunderstood idea in the module (drug tests, polygraphs, facial recognition) in one gesture.
*Touch:* **one `es_Grid(labels)` touch 2×2** ported from ChiTable's `csGrid`/`csEntry` (537-649, 698-796) replaces the INPUT forms at 362-371, 650-659 and 895-904, serves the stratified module with two calls, and makes the cell-layout inconsistency disappear (M); tap-to-page everywhere (S); tap a result row for its worked arithmetic — "OR = (a×d)/(b×c) = (12×30)/(5×8) = 9.00" (M); tap a stratum to drop it from the pool and watch OR_MH move (M); tap the power curve for n (M).
*Graphics:* a **forest plot** for the stratified module (log-OR axis as TrendTest 568-584, squares by weight b·c/n, Woolf bars, a magenta M-H diamond once the Robins-Breslow-Greenland CI is in) (M); the 2×2 mosaic (port `csMosaic`) (S-M); risk bars with a 10×10 icon array for NNT (M); the ROC point with LR slopes (S); PPV/NPV-vs-prevalence curves (S-M); the chi-square curve (S); the §13 palette and a dodger-blue footer so EpiStats, ChiTable and TrendTest look like one suite.
*Pending statistics, where they go:* the RBG variance of ln(OR_MH) after 1438 with the CI on page 2 (space from y ≈ 165 at 1506-1516); the M-H chi-square (1 df); Breslow-Day (per-stratum quadratic, k−1 df, Tarone optional); the Greenland-Robins variance for RR_MH after 1575. All against `statsmodels.StratifiedTable` before pasting.
*Teaching:* "OR overstates RR by X % here because the outcome is common (Ru = 40 %)" computed from the data; replace the red "Confounding likely present" verdicts (1509-1515, 1605-1613, 1706-1710) — a 10 % change-in-estimate presented as a finding in alarm red — with the heuristic stated as a rule of thumb beside the Breslow-Day p.

### ConTable2 v1.2 and FEP v1.3 — fold them in
Both are subsets of EpiStats module 1 plus ChiTable's 2×2 extras, except McNemar, Yule's Q and Y, the error rate (ConTable2) and the Fisher point probability (both). Put McNemar/Yule on a fourth 2×2 page, the point probability and a **hypergeometric bar plot** on page 2, keep a thin four-argument `EXPORT` wrapper for Home use (fleet-unique name), and move the two files to `_superseded`. That removes three copies of the Pearson/Yates code, two of the uncapped `COMB` Fisher, the "(+0.5 corr)" note on the wrong line (ConTable2 186), and FEP's silent "X² = 0, p = 1" on a zero margin (100-101).
*Two ideas worth carrying across:* **the three-reading tap selector** (Cohort / Diagnostic / Paired tabs relabel the same four counts and show only that reading's statistics — nothing else on the calculator makes the point that a 2×2 is three different questions depending on how the rows were sampled); and **the hypergeometric bars with tap-a-bar** — one bar per possible a′ with its probability, the observed a in red, every bar whose probability is ≤ the observed one filled magenta (their sum *is* the p), tap a bar to see that table in the corner. It turns Fisher's test from a formula into a counting argument in thirty seconds.

### TrendTest beta 1a
*Fix first:* menu numbering (plus 755, 701, 704); footer form; rename `trPT0` (plot top) away from `trPT` (p-value) — one typo from a silent wrong value; confirm `MAX(list)` (480) on device or take the max in the loop.
*Showcase:* **drag a dot and watch the test respond** — finger on level 3's dot, drag it down, the magenta line tilts, the Wilson bar shrinks, "X²t = 72.66, p < 0.0001" in the footer falls as the trend weakens; drag level 2 up and the departure-from-linearity statistic wakes up. `trA(sel) := ROUND(p·trN(sel))` from the finger's y, `trCompute` (O(k) plus three `CHISQUARE_CDF`), redraw; a Restore soft key; the originals kept in file-level LOCALs. Pure PPL at a few hundred pixel operations per frame.
*Touch:* soft keys `{"Prop","OR","Scores","Data","Help","Menu"}` (S); tap the score label to cycle 1,2,3 / entered doses / midranks — the warning on help page 1 (691-693) made live (M); hit-test y as well as x (656-662) so the strip is unambiguous (S).
*Graphics:* a confidence band round the WLS line (verify against R `prop.trend.test` / `glm`) (M); a weighted mosaic per level — level 1 (n = 1379) carries the line, level 3 (n = 213) barely counts (M); colour the dots by residual (S); two small chi-square curves, 1 df for trend and k−2 for departure (M); animate the fit from flat to fitted over ~15 frames (M).
*Teaching:* a non-monotone example so the departure test fires (snoring gives p = 0.94 and a student never sees it do anything); a CJ example — prior convictions 0 / 1 / 2 / 3+ against re-arrest within a year; one footer sentence on why the OR axis is logarithmic.

### ChiTable beta 1k — the model; next steps are refinements
*Fix first:* derive the menu numbers in help (1294, 1313, 1315); clamp the last results page instead of exiting on a right-half tap (960 — the footer says "tap = scroll output"); a tagged `MAKELIST` dummy.
*Showcase:* **drag an observed bar in the bars plot** — one finger moves one solid bar, every pale expected bar in the table moves with it, χ² and p change in the footer, the verdict colour flips at p = α. It shows that E depends on the whole table in under thirty seconds. Freeze `bcYmx` during the drag; `csCheck` on lift.
*Touch:* drag the dotted critical line on the χ² curve to set α (cache the density per df first; snap to the ladder on lift or show "custom α = 0.037") (M); a soft-key strip on the results pages and plots `{"Prev","Next","Bars","Mosaic","Curve","Menu"}` (S); tap a cell on the O/E page for "E = 483 × 68 / 674 = 48.73 — what this cell would hold if the variables were unrelated" (S); drag on an entry cell to nudge ±1 (S); a **"×10 N" soft key** — χ² ×10, p collapses, V unchanged: p depends on N, the effect size does not (S).
*Graphics:* the **independence morph** — animate the mosaic's tile heights from observed row % to the column shares over ~10 frames; every bar flattens into the grey reference bar as H₀ becomes visible (M); an adjusted-residual bar chart with dotted ±2 lines (S); the Fisher distribution bars from the weights `csFisher` already computes (M); a ghost χ² curve for the other df (S); row-% stacked bars (S); live χ² in the entry grid when the table is valid (S).
*Teaching:* the df = (r−1)(c−1) page — grey every cell but one with the margins fixed, "fill this cell and the other three follow"; a Simpson's-paradox item drawing examples 1 and 2 side by side (the data is at 1243-1250).

### BayesTree beta 5 — strongest pedagogy, least graphical today
*Fix first:* double-buffer (prerequisite for everything below); the node-page drain and timeout (§2.A); the sub-view drains; `fp`; the two magentas; `dor` at 209 divides by `cfn·cfp` — safe only because of the clamps.
*Showcase:* **a prevalence slider on the first branch with the tree and a mosaic inset re-flowing live** — one rectangle split at the prior, each column split by sens and spec: TP green, FN red, FP orange, TN light grey. Watching the orange FP block swallow the green TP sliver as the prior slides from 0.5 to 0.001 is the whole base-rate lesson in three seconds.
*Touch:* sens and spec by vertical drag on the second-level branches (M); tap a branch probability for "P(T+ \| D+) = sens — read along the row, not the column" (S); soft keys `{"Values","Counts","ROC","PPV","2×2","Diag"}` (S); tap the PPV curve to move the prior (M); tap the ROC curve to move the operating point — sens and spec change together, which is the threshold trade-off (M).
*Graphics (the two pending items):* the **Fagan nomogram** — three vertical axes (prior on a log-odds scale, LR on log10 from 0.001 to 1000, posterior), a magenta line prior → LR+ → PPV and a dodger-blue one through LR− → 1−NPV; drag the prior on the left axis (M). **Sequential evidence** — posterior₁ becomes prior₂, the tree redrawn with a breadcrumb strip "0.10 → 0.69 → 0.98" and the previous stage's leaves greyed; on the nomogram the lines chain (M-L). Also an icon array (Gigerenzer's 1000 people, a static page) (S-M) and a proportional bar inside each leaf box (S).
*Teaching:* a **forensic relabel toggle** — D+ → "source", T+ → "match", prevalence → "1 in the suspect pool of N": 1 − spec is the random-match probability and 1 − PPV is what the court wants; the prosecutor's fallacy is literally the row-versus-column confusion the 2×2 view already prints at 190-191, and it ties straight into DNAMixLR's LR. "Same test, three prevalences" as three mosaics side by side.

### StudRange beta 13 and StudRangePy beta 14b — merge them
This is the one program the rulebook says was worth converting (§1), and the two files are the same algorithm twice. One `StudRange` with a `#PYTHON` block holding `outer / scdf / spdf / qsolve` from StudRangePy 134-205 and the PPL engine as the fallback: inputs read from PPL globals with `hpprime.eval` (never argv), outputs fixed-size (the 65 cache values written one at a time to `EP_SRCDF(j)`, q crit to `EP_QCRIT`), the three guards from §9, a diagnostics item that runs a known value, and an engine badge in the header. Payoff: the cache build (about 104,000 `NORMALD_CDF` calls at k ≤ 5, df < 8, 511-530) drops from a progress bar to about a second; modes 1-3 from about a minute to about 1.5 s; df 1-2 become legal when Python ran; Python returns the pdf directly instead of central differences; and an H₀ simulation (k×m normals via `urandom`, 40 bin counts back) becomes affordable. StudRangePy then retires to `_superseded`.
*Showcase:* tap "Distribution plot", the cache appears in a second, then drag across the curve while **two tails slide — α in orange, p in red, overlap darker** — and the header reads "engine: Python". One program, two languages, with the PPL fallback proving itself if the bridge ever fails.
*Touch:* soft keys `{"α−","α+","k−","k+","df","Exit"}` (S); free α by a vertical drag on the right-hand CDF axis — α is a height on the CDF (S); tap the "q crit" readout to snap q obs onto it, so p = α exactly (S).
*Graphics:* the α ladder as labelled ticks (S); the simulated q histogram over the theoretical pdf (M, Python); a k = 2 comparison curve — "the more means you compare, the larger the biggest gap you expect by chance" (M, needs the Python cache).
*Teaching:* family-wise error by simulation — how often q > q crit (≈ α) versus how often *any* pairwise t exceeds t crit (≫ α); an HSD yardstick — k group means on a number line with an HSD-length bar, tap two means for a verdict (M).

### CentralLimit beta 1a — the app
*Fix first:* `x`/`f` names; the footer's missing "tap bottom = curve"; say when the 60,000-pick cap bites ("600 of 2000, kept quick"); the first hardware run should exercise the Plot key (`H1`/`H2` with `:24h` colours, `CHECK`/`UNCHECK`, `STARTVIEW(7,1)` are all untested).
*Showcase:* **tap once and watch one sample happen** — its n members light up as ticks on the population axis, collapse to their mean, and the mean falls into the magenta pile over 3-4 frames; tap again; press + and 200 of them rain in; then press the Plot key and **the app's own histogram appears with the right bin width** — the Prime running a real app, which no standalone program and no TI-84 can do.
*Touch:* drag on the top panel to choose n — the predicted N(μ, σ/√n) narrows *before* any data; release to resample (M); soft keys `{"Sample","+1","n−","n+","Curve","Menu"}` (`DRAWMENU` inside an app program is untested) (S); tap a bar for a tooltip on G1 (S).
*Graphics:* a **√n-law panel** — observed SD(x̄) against every n tried this session, as points on the σ/√n curve (M); colour the means bars by SE distance (green within 1, orange within 2, red beyond) — the 68-95 rule for the sampling distribution, not the population (S); the population's theoretical density on the top panel so "the population is NOT a bell" is drawn (S-M); redraw every sample for the first 20 — the first few means landing one by one is what teaches (S).
*Teaching:* caption the first sample "this is ONE sample's mean — the magenta pile is many of them"; force n = 1 first (the means *are* the population), then 4, 16; name "standard error" once at 466.
*MicroPython:* marginal — a variable-size payload (D2 must hold the raw means for the app's views) and `PYTHON()` inside an app program is untested. Only if you want the cap gone.

### GaltonBoard beta 1a — the demo reel
*Fix first:* split the "pegs" tap zone (623) from the readouts; legend to the house form and say that arrows clear the counts; check `gbToStats` (471) fits a box; first hardware run checks that `ARC_P` at r = 1-3 renders a solid disc and `WAIT(0.02)` does not swallow keys.
*Showcase:* **pour mode** — hold a finger on the funnel and a stream of red balls cascades through the pegs with faint trails, the blue bars climb toward the magenta squares and the green bell, x̄ and s settle beside Rp and √(Rp(1−p)). Lift the finger, **drag sideways, and the whole theory re-flows for a new p**. Per-ball state in parallel lists; per frame one G2→G1 blit, N discs, one blit — the cost barely rises with N; landed balls redraw only their bar on G2. (L)
*Touch:* drag p across the board (> 8 px of movement; a press with no movement still drops a ball) (M); soft keys `{"Drop","×10","×100","p","Rows","Menu"}` (S); tap a bar twice to highlight every lattice path to that bin, C(R,k) of them, capped at R ≤ 8 — shows *why* the middle bins are tall (M).
*Graphics:* ball trails as fading discs, paths persisting as light-red polylines on G2 (S); the **Bernoulli string** "R L R R L R L L → 4 rights → bin 4" printed as the ball falls (S); an empirical Pascal's triangle — per-peg pass counters printed beside the pegs when bw ≥ 28 (M); bars coloured by |k − Rp| in SD units (S); the normal as a filled area so bar-versus-area and the continuity correction are visible (S); a tilted board for p ≠ 0.5 (S). 3-D adds nothing here.
*MicroPython:* one honest case — a "drop 100,000" law-of-large-numbers item: `urandom.getrandbits(R)` and a bit count per ball, R+1 counts back, engine badge. Minutes in PPL, seconds in Python; it meets your rule and makes a clean "PPL animates, Python crunches" exhibit.
*Teaching:* the bell comes from the number of *rows* (de Moivre-Laplace), not the number of balls — more balls only make the bars match the squares; a rows 3 → 12 sweep shows it. Grey the curve and say "approximation poor" when Rp < 5.

### TestChooser beta 1a
*Fix first:* menu numbering; footer form; the table shows designs 2-6 while help (662-663) claims a one-sample column; "Interval"/"Survival" (581, 585) may clip at width 51; the unverified ↑↓← glyphs (399, 512); a `RETURN TC_TEST`.
*Showcase:* **the tappable flowchart with the path lighting up** — tap "Nominal", the other three scales fade, six design nodes drop in, tap "Two groups", the orange path draws itself across the screen and ends in "chi-square / Fisher", and a soft key opens the Inference app (`STARTAPP` — whether the caller continues afterwards is unrecorded; test). Two levels on screen at a time; `RECT_P` nodes, `LINE_P` connectors, the existing three-line arrowheads (483-485) until `FILLPOLY_P` is probed. (M-L)
*Touch:* soft keys `{"Guide","Table","Help","","Back","Quit"}` (S); a two-stage tap in the table — first selects and shows the full name, second opens (S); tap a row label or column heading to highlight the whole row or column, "what do all the rank tests have in common?" (S); **quiz mode** — a scenario sentence over the table, tap the cell, green or red with the right cell outlined, then the details page: the best pedagogy per line of code in the fleet (M).
*Graphics:* 14×12 cell pictograms (two bars, three bars, joined dots, a scatter, a step-down curve) (M); hatch the twelve "Not on the Prime" cells so the table also answers "what can I do on this calculator?" (S); a six-column table at 44 px (S-M).
*Teaching:* the quiz bank in your students' field — sentence length by judge (ANOVA / Kruskal-Wallis), recidivism by programme (χ² 2×2 with OR), examiner accuracy before and after training (paired t), time to re-arrest (log-rank); a paired-versus-independent pair ("the same officers measured before and after" versus "two different units"); Likert confidence in a bitemark match as ordinal → Mann-Whitney, with a line on what a mean of ranks means.

### DNAMixLR beta 1
*Fix first:* §2.B rows (the excluded locus; `dmBig`); `g1…g6`; menu numbering; green theta line omitted above 0.05 (791) while the legend still promises it; label collisions at 12 loci (bar pitch 21 px, labels 26-33); plot 2's three recomputed values (804); grey footers; a `RETURN`.
*Showcase:* **drag theta on plot 2 with an ENFSI verbal ladder beside it** — as the finger slides from 0 to 0.05 the green line follows, the LR readout counts down and the ladder marker drops from "very strong" into "strong". The 21 values are already cached (757) so it is smooth on a G1, and it teaches the one idea (population structure) students treat as a footnote. (M)
*Touch:* tap a locus bar for its alleles, P(E\|Hp), P(E\|Hd), LR and verbal — `dmPp`/`dmPd` are already computed and never read (350-351) (M); genotype entry by tapping allele tiles instead of "position in your allele list" integers (M); tap a results row to drop that locus — the combined LR is a product and the student sees which loci carry it (M); soft keys `{"Locus","Theta","Table","","Help","Menu"}` (S).
*Graphics:* the **ENFSI ladder** (bands at log10 LR −6…6 from `dmVerbal`, red marker at the combined value, ticks per locus) (S); a **waterfall by locus** — floating bars from cum(i−1) to cum(i), blue for Hp, red for Hd, which students read correctly as "logs add" (S); the allele-set picture per locus — victim green, suspect magenta, the alleles the unknown must supply outlined red, and under Hd the suspect's fill disappears and U grows: *why* the LR is what it is (M); on the theta plot, shade the 0.01-0.03 band and overlay the same loci with every frequency halved — theta bites hardest when p is small (M).
*Teaching:* a **prosecutor's-fallacy page** — prior odds from a tapped ladder (1 in 10 … 1 in 10 million) × LR = posterior odds → posterior probability as three stacked bars; the same LR 5333 gives P ≈ 0.998 at 1:1 and P ≈ 0.05 at 1:100,000; add "this is NOT the probability that the suspect contributed" at 470 and 653. Show the NRC II formula evaluated numerically for the next allele beside the plain p (0.15 becomes 0.157, and why). Say that preset 3 is 1/RMP.

### FDAES v3.4 — rebuild the output layer, then draw
*Fix first:* the 20 over-length boxes (§2.C) — until this is done the program's output is probably unreadable as shipped; menu and tooth-string numbering; the stale "methods 2, 4, 7, or 8"; the pragma line; the header; the M3 sex read; `STRING(x,1,0)` at 324, 421, 439, 544, 641, 722, 848; cancel on "teeth averaged" silently becoming 1 (608).
*Showcase:* **the odontogram** — six mandibular teeth (32-37) as tiles; tap a tooth, tap a stage picture (crown and root fraction drawn with `RECT_P`/`LINE_P`), the tooth colours in by stage and the age estimate with its interval moves on an age axis beside it; three taps later **the posterior N(pmu, psd) appears with the 18-year line and the tail shaded, and the finger drags the threshold**. For a forensic odontologist's audience, teeth you can tap on a calculator *is* the demo — and it is the honest picture of what this Willems adaptation computes (per-tooth ages averaged; the header's own caveat at 59-63). (M-L)
*Touch:* tap a method to toggle it in the Bayesian pool, with the precision floor shown live (M); Lamendin on a drawn root — drag two lines for periodontosis and transparency heights (M-L); a soft-key main menu over a status panel (S).
*Graphics:* the **posterior curve** with 68 % and 95 % bands, lines at 16, 18, 21 and the tail probabilities — the figure an expert witness shows, which the program has only as text (S-M); a **forest plot** of the stored methods ± 2 SE with the pooled posterior as a magenta diamond and a dotted line at the best single SE — the meta-analysis picture, and it teaches the independence problem (760-771) at a glance (S-M); M3 threshold bars D-H with the 50 % line and the uncertain zone shaded orange (S); a verdict band on every result — green "likely ≥ 18", orange "uncertain", red "likely < 18" (S).
*Teaching:* the transposed conditional in dental form — Mincer's figures are P(age ≥ 18 \| stage) in a reference sample with its own age mix, so a "prior" control (uniform 14-24 versus the reference mix versus a younger population) moves the posterior for the same stage H: the prosecutor's fallacy where students least expect it; Gustafson's claimed versus actual SE as two normal curves (SD 3.6 and 14.2) on one axis.

---

## 7 · New programs that would show the Prime off

1. **GfxProbe beta 1 (first, S).** A probe in the PyProbe tradition that exercises, on both calculators with the Terminal open: `FILLPOLY_P` with alpha over a drawn curve; `TRIANGLE_P` with three colours and with alpha; the 3-D `TRIANGLE_P` mesh form on a 10×10 grid with a rotation matrix; the 10-argument scaled `BLIT_P`; a second finger in `MOUSE`; `WAIT(-1)` types 2, 3, 5, 6, 7 printed as they arrive; `DRAWMENU` inside an app program; `ARC_P` at r = 1-3; `MAX(list)`; `SORT`; `WAIT(0.02)` with a key held. One afternoon, and it decides what §4 is allowed to promise. Results go to Lessons Learned v7f.
2. **BiNorm3D (M-L, after the probe).** A bivariate normal surface drawn with the mesh form of `TRIANGLE_P`, **rotated by dragging a finger** (type 1 events → rotation matrix), pinch to zoom, soft keys for ρ ±0.1 and a contour toggle. As ρ moves from 0 to 0.9 the bell stretches along the diagonal; a tap on the contour view draws the conditional distribution of Y at that x. Correlation and regression-to-the-mean in one object that no TI can draw. The one program in the fleet that is *about* 3-D.
3. **ScatterLab (M).** Tap to place points on a scatter; **drag a point and watch the least-squares line, r, r² and the residual segments update live**; a long-press deletes a point; a soft key adds a far-out point so leverage is felt rather than defined; export to C1/C2 and hand off to Statistics 2Var. Intro-stats gold (crime rate against poverty rate, by county), and pure PPL — the regression arithmetic is five sums.
4. **CICatcher (M).** The confidence-interval simulation: 100 intervals drawn as horizontal bars from repeated samples, the ones that miss μ in red, the coverage counted at the top; drag the confidence level and watch the bars lengthen; **tap any interval to see the sample it came from**; pure PPL (Marsaglia polar). It answers "95 % of what?", which a z-table never does.
5. **AnovaHSD (L) — the suite you asked for on 3 October.** One-way ANOVA from up to six groups in D1-D6 or typed, side-by-side box plots coloured by group, the F statistic on its curve, then Tukey HSD on the merged StudRange engine: **tap two boxes to see their difference against the HSD yardstick**, green or red; a "drag a group mean" what-if. Borrow the post-hoc menu ideas from Stat49 Pro and StatPack 49 as planned. This is where the Python engine earns its place twice.

Also worth a line: the Fagan nomogram and the prosecutor's-fallacy page are better *inside* BayesTree and DNAMixLR than as new programs; and a fleet "Gallery" launcher (one screen of thumbnails, tap to run, via `STARTAPP`/program calls) is the natural front door once the showcase features exist.

---

## 8 · Suggested order of work

**Phase 0 — this week, before anything is pasted.** Fix `fleet_names_v1.py`; clear §2.A, §2.B and §2.E; strip the CHOOSE numbering in all seven programs (new versions, old ones to `_superseded_2026-10-xx`); add the missing drains and pragma lines; write **GfxProbe** and run it on the G2 and the G1 with the Terminal open; record the results and §10's items in **Lessons Learned v7f**. Then the first hardware runs of the five programs that have never had one (CentralLimit, GaltonBoard, TrendTest, TestChooser, DNAMixLR) plus the re-runs the §15 table is still waiting for.

**Phase 1 — first touch upgrades, one per group, each a port of verified code.** Norm3 (drag x₀, tap the S-curve) → Burr3 by copy; PowerViz (cache, then drag H₁ and the critical line); EpiStats module 1 (the grid port, tap-to-page, and the G1 pass that also fixes the flashing and the hidden page); DNAMixLR (tap a bar, drag theta, the ladder). Each gets its new version, a guide update with the firmware line, and a device test before the next starts.

**Phase 2 — the showcase features.** GaltonBoard pour mode and trails; ChiTable bar-drag and the independence morph; BayesTree double-buffer, slider and mosaic, then the nomogram; TrendTest drag-a-dot; the StudRange/StudRangePy merge with the engine badge; SampDist's population ghost and n×4 key; NormExplorer's two-bound drag and soft keys.

**Phase 3 — new programs**, in the order of §7, each from `TouchKit_template_v1.txt`.

**Phase 4 — the two rebuilds.** StatDist (the drawn result screen, then the gallery, then the stubs) and FDAES (the output layer, then the odontogram and the posterior curve); fold ConTable2 and FEP into EpiStats; the EpiStats forest plot and the pending M-H statistics.

A paste-test loop that has worked: lint (`ppl_check_v2.py`, `lint_ppl.py`), the fleet check, paste one program, run it with the Terminal open, note anything unexpected in the Lessons Learned draft before the next paste, regenerate `FIXED_FOR_DEVICE`.

---

## 9 · Showing what the collaboration looks like

For HHC, HPCC and the repository README, the thing worth showing is not that an AI wrote PPL — it is **how a niche language with no real documentation got a verification culture**: a device-verified rulebook that grew from v3 to v7e by recording what the hardware actually did (including the disproved theories, labelled as disproved); a searchable index of 1,658 programs and 628 PDFs that answers "has anyone used `TRIANGLE_P` with alpha?" in a second; a fleet-wide name check that found the shared-routine-pool bug the User Guide says cannot happen; every statistic checked against SciPy or statsmodels before it goes near a calculator; the PPL fallback that kept a Python sampler's eleven-build silent failure from ever reaching a classroom; and the division of labour — concept, source material, classroom judgement and all hardware testing yours; implementation, numerics and the guides Claude's. Three short artefacts would carry that: a one-page **"How these programs were made"** in the repo; a **ten-minute demo script** (GaltonBoard pour → ChiTable bar-drag → BayesTree slider → StudRange "engine: Python" → one tap on the odontogram); and the **Lessons Learned document itself**, which is the most useful thing in the repo for anyone else writing PPL.

---

## 10 · Lessons Learned v7f candidates

- §3 confirmed list: the `hpprime` argument orders StudRangePy ran on the G2 — `fillrect(gr,x,y,w,h,edge,fill)`, `line(gr,x1,y1,x2,y2,c)`, `pixon(gr,x,y,c)`, `textout(gr,x,y,text,c)` (§8 still says unverified); the two-argument `BLIT_P(G0,G1)` form (StudRange 641, hardware through beta 11); `MAX` on a list and `SORT` once GfxProbe confirms them.
- §7: a GETKEY drain does not drain touch — a finger lift can satisfy the next `WAIT(-1)` (BayesTree 147-149); `WAIT(-1)` times out after about 60 s, so it is wrong for a page that must stay up; `MOUSE` and `WAIT(-1)` use different type-code tables (§4 above); WaitLab's observed event sequences, with the firmware they were seen on.
- §6: the `sr_ShowRes` budget is 8 lines at 22 px; a result page that advances on a tap must not exit on the last page's tap without saying so.
- §5: `fleet_names_v1.py` must require the file's own tag; `G1…G6` as LOCAL names; `K` as a `MAKELIST` dummy writes Home's K.
- §8/§9: `random` is absent and `urandom` present — a `from random import …` guard is a guaranteed fallback, not a precaution (NormExplorer 470).
- §13: adopt the CentralLimit footer form as canonical; add PowerViz's α/β/power fill triplet or replace it; decide the arrow-glyph and subscript conventions; the `LOCAL pv_Name()` routine-head form is either verified by PowerViz v2.1's run or to be avoided.
- §14: version strings and file maps inside a program are references too — sweep them with every rename (seven stale ones this review).
- §15: the seventh self-numbered menu (TrendTest); the false-pass note on the v7d "0 untagged" result.

---

## 11 · Questions only you can answer

1. **Mincer stage H.** FDAES uses 99 % for P(age ≥ 18 \| stage H) at 461 and 464. One reviewer's recollection of Mincer, Harris & Berryman (1993) is about 90 % (males 90.1 %, females 92.2 %). Please check against the paper; the header lists M3 under the arithmetic self-check rather than under "provenance not confirmed".
2. **MSGBOX on the device.** Does a ten-line StatDist result box really show five lines on the 2026-09-09 firmware, or does it scroll or wrap? The answer decides whether StatDist and FDAES have been showing their answers at all, and whether §3 needs a correction.
3. **Fold ConTable2 and FEP into EpiStats**, keeping a four-argument Home wrapper — yes or no?
4. **Merge StudRangePy into StudRange** with the Python engine and PPL fallback — yes or no?
5. **Which new program first** after GfxProbe: BiNorm3D (the 3-D showcase), ScatterLab (the intro-stats workhorse), CICatcher, or AnovaHSD (your 3 October request)?
6. **PowerViz's `LOCAL pv_Name()` routine heads** — did v2.1 run on hardware in that form? If so it goes in §3; if not, the heads come off in v2.3.
7. **Arrow glyphs and subscripts** — `CHAR()` builds or the literal palette characters, fleet-wide?

---

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
