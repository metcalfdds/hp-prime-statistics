# TestChooser beta 2 — changes from beta 1b

16 October 2026. The touch-and-graphics version from the fleet review (Fleet_Review_2026-10-16_v1.md §6, TestChooser), built on `TestChooser_beta1b.txt` with every beta 1b fix kept. **Not yet run on hardware.**

Line references are `beta 1b → beta 2`. The knowledge block (tcIdFor, tcScaleShort, tcDesignShort, tcFull, tcCell, tcDetail: 92-339 → 155-402) is byte-for-byte unchanged (checked with `diff`).

## (a) Changes

1. **Header** (1-130). "TESTCHOOSER - beta 2"; a dated "beta 2 — what changed" paragraph above beta 1b's (kept); licence, AI-assistance and firmware ("NOT yet been run on hardware") lines kept; "THREE WAYS IN", a SOFT KEYS section and the "how to check it" note added; the layout note says nothing is drawn in y 218-239.
2. **Guide = a tappable flowchart** (replaces `tcPick` 396-446 and `tcShowPath` 488-538 → `tcNodeBox` 900, `tcNode` 918, `tcDrawL0` 949, `tcDrawL1` 993, `tcAnimUp` 1092, `tcAnimPath` 1119, `tcMove` 1133, `tcGuide` 1147).
   - Level 0: root box "outcome scale?" (x 90-230, y 4-28), a trunk at x 160, four scale nodes in two columns (x 10-146 / 174-310, 50 px tall, name + two hint lines), horizontal LINE_P branches with the beta 1 three-line arrowheads (`tcHead`, the shape of 506-508). Q1 and a hint below.
   - Tap a scale (or arrows + Enter): one frame with the other three greyed, three frames of the chosen node rising to the breadcrumb place, three frames of the six design rows dropping in (7 frames, TICKS-based `tcPause`).
   - Level 1: breadcrumb (tap it = back to the scales), six design nodes (left column = different people / one group, right = same people / association).
   - Tap a design: the other five grey out and the orange path draws itself in six frames — trunk, branch, node lit (3-px orange frame), out and down the outside rail, across to the leaf, the leaf box (y 152-198) with the test's full name and "tap here or Ent = all the details" (or "not on the Prime, tap or Ent = details"). Tap the leaf or Enter → details. At level 2 the arrows move to another design and re-light its path.
   - Back/Esc = up one level (2 → 1 → 0 → menu). Every step has a key: arrows (Up/Down in a column, Left/Right across), Enter. Hit boxes recorded while drawing (`tcAddHit`/`tcHitAt`, ChiTable's pattern). No FILLPOLY_P / TRIANGLE_P.
3. **Soft keys `{"Guide","Table","Quiz","","Back","Quit"}` on every screen** (`tcShow` 646: BLIT_P then DRAWMENU; `tcSlot` 654 = `MIN(6, IP(x/53.4)+1)`; `tcSoftAct` 661). Each screen returns the next mode to the main loop (1745), so a soft key jumps straight between Guide, Table and Quiz; Back = Esc; Quit leaves the program. All footers moved above y 218 (y 197-206).
4. **`tcWaitAny`** (358-370 → 616) is now the house xxWaitAny: returns the key, or -1 for a tap with x, y in file-level `tcTX`, `tcTY`. `tcDrain` unchanged.
5. **Table** (`tcDrawTable`/`tcTable` 587-665 → `tcGeom` 1223, `tcCellDraw` 1236, `tcTblBG` 1262, `tcTblBase` 1311, `tcDrawTable` 1320, `tcTable` 1358):
   - first tap on a cell selects it (solid, red 2-px "you are here" frame) and puts its full name in the status line (y 183); a second tap on the same cell opens the details (beta 1b opened on the first tap, 645-655). Enter still opens.
   - tap a row label (x < 54) → the whole row lit in its scale colour, status "Ordinal row: rank tests - ranks, not means" etc. (`tcRowSum`); tap a column heading (y < 40) → the column lit, status "2 independent groups: different people" etc. (`tcColSum`). Tap again to clear. Keys: + = row, − = column.
   - **One-sample column**: 6 × 44-px cells do not fit — the cell labels are up to 8 characters (~52 px at 6.5 px/char), so a 44-px cell would clip them. Instead the table is a 5-column window: the corner key (x 1-51, y 4-36, "< show / 1 group") flips to designs 1-5, and Left from the first column slides there (Right past design 5 slides back). Cells stay 53 px; rows 35 px (was 38) to make room for the status, legend and footer above 218.
   - The background (headings, pictograms, row labels, all cells with their hatching, the corner key, the legend) is drawn once into **G2** and copied to G1 each frame (`BLIT_P(G1, 0, 0, G2)`, GaltonBoard's form); it is rebuilt only when the layout changes (`tcCK`). Measured in the harness: the G2 build is 1,339 PIXON_P + 116 other calls; a browsing frame is 17 drawing calls; a frame with a lit row is 565 (532 of them the hatching of the lit cells).
6. **Hatching** (`tcHatch` 728): the twelve tests whose detail line 3 starts "Not on the Prime" (4, 9, 11-14, 16, 17, 19, 20, 23, 24; `tcNotP` in `tcInit`, checked against `tcDetail` on the PC) get dotted 45° light-grey (#B4B4B4) PIXON_P lines, 6 px apart; on a lit cell the dots take the cell's light colour. Legend in G2 at y 195: a hatched swatch and "= not on the Prime (R or JMP; see details)". Test 18 ("(none)", before/after survival) is not hatched: its line 3 is "Re-think...", so it does not meet the rule as stated.
7. **Pictograms** (`tcPict` 748), 14 × 12 from RECT_P/PIXON_P/LINE_P: one bar under a dotted value line (1 group), two bars, three bars, two dots joined (paired), three dots joined (repeated), a scatter (association) — in the column headings (browsing); bell, yes/no boxes, ranked steps, step-down Kaplan-Meier curve with a censoring tick — beside the row labels. Not in the cells: beside two 8-character lines in a 53-px cell they would clip the text.
8. **Quiz** (new: bank `tcQ` 470, `tcQNew` 1456, `tcQuizDraw` 1476, `tcQFlash` 1511, `tcQEnd` 1526, `tcQuiz` 1566). Twenty cases (sentence length by three judges → one-way ANOVA, Kruskal-Wallis also accepted; re-arrest yes/no in two programmes → chi-square/Fisher, "give the OR", the RR/OR cell also accepted; examiner accuracy before/after training → paired t; Likert bitemark confidence, certified vs not → Mann-Whitney; days to re-arrest → log-rank; crime vs unemployment across 50 counties → Pearson/regression; plus BAC rural/urban, McNemar on repeated bitemark calls, plea by counsel type, injury severity by weapon, officer stress before/after, simulator reaction time under three lightings, mock-juror ratings, Cochran's Q on qualifications, Spearman on lab rankings, log-rank by supervision level, Cox with predictors, toxicology × accident ruling (RR/OR, 2×2 also accepted), intercanine width by sex, two odontologists measuring the same skulls → paired). They cover all 18 testable cells of designs 2-6, so the quiz table is Glantz's five columns with no second page.
   - Layout: the case in three font-1 lines at the top (y 2-37), the table below (rows 29 px from y 62), the reason line (y 181), "Score = 4 of 6, case 7 of 20" (y 193), footer (y 205).
   - Tap a cell (or move the red frame with the arrows and press Enter). Right → the cell flashes green three times, the reason shows in green, then the details page opens. Wrong → the tapped cell flashes red, the right cell is outlined in green (4 px), the reason shows in red ("The same examiners measured twice: PAIRED"); tap the green cell for its details, or Enter / any other tap for the next case.
   - Order: Fisher-Yates with `RANDOM`, no repeats in a round; the round (order, place, score) survives leaving for the Guide or Table. After 20 cases a "Round over" page with the score and four usual traps; Enter/tap = new round.
9. **Details page** (`tcDetails` 455-480 → 845): a "Check:" line (dodger blue, y 93) under the assumptions where the Prime helps (`tcCheck` 407): Stats 1Var normal probability plot (tests 1-4), NormExplorer's data module for residuals (5), single samples (21) and symmetry (13, 23), ChiTable's expected counts (6, 7, 10); blank elsewhere. Frame ends at y 214; footer "tap or any key = back, Quit = leave" at 197. Returns the soft-key action.
10. **Help** (671-692 → `tcHelp1` 1652, `tcHelp2` 1672, `tcHelp` 1693): two pages; page 1 the two questions (and "with a one-sample column", now true again); page 2 every gesture: the flowchart, Back, the two-stage tap, row/column lighting with + and −, the corner key, hatching, the quiz.
11. **Menu** (712-716 → 1757-1762): "Guide me: the flowchart", "Browse the table (Glantz)", "Quiz: which test fits the case?", "Help", "Quit" — unnumbered. The main loop is a mode machine (0 menu, 1-4 screens, 9 quit).
12. **Return** unchanged: `RETURN "TestChooser: " + TC_TEST` (or "no test looked at"). TC_TEST is set when a leaf appears and when any details page opens (guide, table, quiz).
13. Palette: `tcRED` #FF0000, `tcLRED` #FFEBEB, `tcHATCH` #B4B4B4, `tcPALE` #A0A0A0 (greyed nodes) added in `tcInit`; all others as beta 1b.

## Gate (check.sh, final)

```
kit lint: 0 errors
ppl_check tally NEW: (none)          ORIG (beta 1b): (none)
hard errors (E2 E3 E6 E8 E10 E11) in NEW: none
lint_ppl: 1045 checks, 52 problems -- 47 are "RECT_P/LINE_P/PIXON_P/TEXTOUT_P targets
  'ptG'/'bxG'/'htG'/'cdG', not a GROB" (grob passed as a parameter, ChiTable's csDotV
  form: known noise); the other 5 are the same known-noise lines beta 1b has (426 checks,
  5 problems). Two "concatenates bare tcCY1" false positives were removed by precomputing y.
full parse: PARSE FAIL at "EXPORT TC_TEST" followed by file-level LOCAL (135), exactly as
  beta 1b (85) -- the kit's limit. ppl_run_v1 loads it: 52 functions, 47 file-level LOCALs.
non-ASCII in code: none (the ⇆⇅ glyphs are inside strings, as in beta 1b)
fleet_names_v2 over out/*.txt without beta 1b: no collision, untagged, mixed-tag or built-in
  name involving TestChooser_beta2 (the 231 collisions listed are other programs' old and new
  versions sitting side by side in out/).
```

## Harness runs (ppl_run_v1, `verify_TestChooser.py`, output in `verify_TestChooser_out.txt`)

**230 checks passed, 0 failed.** No statistics are computed, so there is nothing to compare with SciPy; the script checks the program against itself:

- **Quiz bank**: each case's (scale, design) run through the program's own `tcIdFor`/`tcFull` gives the intended test (20/20); the three also-accepted cells give Kruskal-Wallis, RR/OR and chi-square 2×2; all designs in 2-6; every line ≤ 46 characters; the bank covers 18 of 18 testable cells.
- **Hatching**: `tcNotP` equals the "line 3 starts Not on the Prime" rule for all 24 tests; 12 hatched.
- **Strings**: every Check line ≤ 42, node text ≤ 20, row/column summaries ≤ 46.
- **Guide** (taps): menu → tap Nominal → seven animation frames → level 1 (breadcrumb "Nominal", six designs) → tap "two groups" → six path frames with orange LINE_P → leaf "Chi-square 2x2, or Fisher's exact" → tap leaf → details with "Check: expected counts >= 5 in ChiTable." and subtitle "nominal | 2 independent groups" → Enter, Esc, Esc. **Keys only**: Down, Right, Enter (Survival) → Right, Down, Down, Enter (association) → leaf "Cox proportional-hazards regression" with "not on the Prime, tap or Ent = details" → Enter → details. Returns "TestChooser: Cox proportional-hazards regression".
- **Table**: first tap names "Unpaired (two-sample) t test" without opening; second tap opens it ("Check: Stats 1Var normal plot, each group."); tap "Ordinal" → "Ordinal row: rank tests - ranks, not means"; tap a heading → "3+ independent groups: different people"; corner key → "1 group / vs value" column shown; + → "Interval row: ..."; − → "2 independent groups: ..."; Right ×5 slides back to designs 2-6 at "Pearson r and linear regression"; Enter → its details; Table soft key stays; Back → menu. G2 built at most 3 times in the run; 1,339 hatching dots in it.
- **Quiz**: a whole 20-case round with seed 7 (a permutation of 1-20), every third case answered wrong: green cell drawn for right answers and the details page opens; a wrong-answer frame for each wrong case with the case's reason line ("Same officers rated twice, ordinal: paired" etc.); tapping the green cell opens the right test; "Round over" shows "You picked the right test 13 times out of 20." (7 wrong: cases 2, 5, 8, ... 20)
- **Help**: two pages; the Quit soft key leaves with "TestChooser: no test looked at".
- **Soft keys**: Guide → Table → Quiz → Guide → Back → menu, each landing on the right screen.
- **Layout** on every held page (animation frames excluded): no text reaches y 218, no two texts overlap (6.5 / 8 px per char, 11 / 14 px rows), nothing new wider than its box. (The 8-character cell labels — "Friedman", "Kruskal-", "Spearman", "Wilcoxon", "chi-sq./", "k groups" — estimate at 52 px for a 49-px width; they are beta 1b's, unchanged, and only the device can say whether they clip.)

**Harness limit met**: ppl_run_v1 covers `RANDOM` only written as a call; the fleet (CentralLimit, GaltonBoard, CICatcher) and `tcQNew` write it bare. The test subclasses the harness to read a bare `RANDOM` as `RANDOM()`; the program itself is unchanged.

## (b) DEVICE TEST CHECKLIST (least → most risky)

1. Paste into the Connectivity Kit and Check: no syntax error. Run `TestChooser()`: five menu items, numbered 1-5 by the Prime.
2. Help: two pages fit inside the orange frame; footers above the soft-key strip; the strip reads Guide, Table, Quiz, (blank), Back, Quit. Enter goes to page 2, Left back to page 1, Back to the menu.
3. Soft keys on every screen: from the Guide tap Table, from the Table tap Quiz, from the Quiz tap Guide, then Back → menu; Quit leaves from any screen and Home shows `TestChooser: ...`. The blank key does nothing.
4. Guide, level 0: the root box, trunk, four nodes with name + two hint lines readable (font 2 name fits 136 px; hints ≤ 20 chars); arrowheads point into the nodes.
5. Tap Nominal: watch the animation (grey-out, rise, three rows drop in) — smooth enough on the **G1**? (each frame ~60 drawing calls plus a 60-150 ms pause.)
6. Level 1: breadcrumb "Nominal"; six two-line design nodes; tap the breadcrumb → back to level 0.
7. Tap "two groups": the orange path draws in six steps down the trunk, along the branch, round the node, down the left rail and into the leaf; the leaf names the test in white on orange. Try a right-column design too (rail on the right edge, x 316-317 — visible?). Try "Before/after survival" (font-1 name, hatched-test wording).
8. Tap the leaf → details page: frame ends above the strip, "Check:" line in dodger blue under the assumptions (for chi-square: ChiTable). Any key/tap → back to level 2. Back → level 1 → level 0 → menu.
9. Keyboard only, whole guide: arrows move the solid focus, Enter picks, Enter on level 2 opens details, Esc goes up.
10. Table: the corner key, pictograms in the headings and beside the row labels are recognisable at 14 × 12; "Interval"/"Survival" still clear the cells; **cell labels "Friedman", "Kruskal-", "Spearman", "Wilcoxon" not clipped** (unchanged from beta 1b, now with 35-px rows).
11. Hatching: the ten hatched cells on page 1 are clearly grey-dotted and the text on them still readable; the legend swatch matches. First entry into the table builds G2 (1,339 PIXON_P) — how long does it take on the G1? (once per entry / page flip.)
12. Table taps: first tap selects (red frame, name in the status line, no details); second tap on the same cell opens details; a tap on a different cell only selects.
13. Row label / column heading taps light the row / column in the scale colours with the summary in the status line; tap again to clear; + and − do the same. **A lit row redraws ~530 hatch dots per frame — any visible lag on the G1?**
14. Corner key: the one-sample column appears ("1 group / vs value"), the corner reads "show > / assoc."; Left from design 2 also slides there, Right past design 5 slides back.
15. Quiz: the case's three lines fit; tap the right cell → three green flashes, reason in green, details page; Back → next case. Tap a wrong cell → red flashes, the right cell outlined in green, reason in red; tap the green cell → its details; Enter → next case. Score line counts correctly.
16. Quiz order: two rounds in a row give different orders and no case repeats within a round (RANDOM-driven Fisher-Yates). After case 20: the Round over page; Enter starts a new round.
17. Leave the quiz mid-round for the Table and come back via the Quiz soft key: it continues at the next case with the score kept.
18. **G2 as a cache** (`DIMGROB_P(G2, ...)` + `BLIT_P(G1, 0, 0, G2)`): GaltonBoard's form, in 87 corpus programs, but not yet run by us on hardware. If the table shows blank or stale, report it — the fallback is to draw the background straight into G1 each frame (slower).

## (c) Not confirmed / left as is

- **44-px cells**: not used. At ~6.5 px per character the 8-character cell labels need ~52 px; the one-sample column is a second page (corner key / Left) instead, as the brief allowed.
- **Pictograms are in the headers, not the cells**: a 14-px picture beside two 8-character lines does not fit in a 53-px cell.
- **Test 18 is not hatched** although it is not on the Prime either: its detail line 3 begins "Re-think", and the brief defines the twelve by line 3. Hatch it too if you prefer (one `1` in `tcNotP`).
- The quiz uses only designs 2-6, so the one-sample tests are never a quiz answer.
- The Inference-app soft key the review floated (STARTAPP from a leaf) is not in this version: whether the caller continues after STARTAPP is unrecorded.
- Text widths are estimates (6.5 / 8 px per character); every "fits" above is an estimate the device must confirm, especially the font-2 scale names and the leaf name in font 2 (names ≤ 31 characters).
- **The "More" soft-key convention** (BRIEF_TOUCH, 16 Oct): not applied. The screens need exactly the six labels the brief fixed (Guide, Table, Quiz, blank, Back, Quit), and every feature already has a key or soft-key route (corner key = Left past design 2; row/column lighting = + / -; Help = Back to the menu). Adding a "More" key would have displaced Quit from slot 6 for no gain; if Help should be reachable from every screen, the blank slot 4 is the place for it before any "More".
- tcPick and tcShowPath are gone (replaced by the flowchart); nothing else of beta 1b was restructured.
