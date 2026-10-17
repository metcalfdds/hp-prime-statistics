# DNAMixLR beta 2 → beta 3: what changed

*16 October 2026. Built ON TOP OF `/home/claude/work/out/DNAMixLR_beta2.txt` (2432 lines); every beta 2 change is kept.
Output: `/home/claude/work/out/DNAMixLR_beta3.txt` (3015 lines, 126.0 KB, UTF-8, LF). **Not yet run on hardware** (nor were
beta 1, 1a and 2), and **nothing about the CAS has run on a calculator**. "b2" = beta 2 line numbers, "b3" = beta 3.
`dmProb`, `dmKnowns`, `dmTyped` and `dmEval` are byte-for-byte beta 2 (checked by script), and so are `dmCombAt`,
`dmCurves`, `dmInterp`, `dmThX`, `dmThFrame` and the theta drag in `dmPlotTheta`.*

## (a) Every change

1. **The LR as a formula (CAS), on the locus page** (b2 `dmDrawPanel` 1771 / `dmLocusPanel` 1882 → b3 2309 / 2439;
   new `dmFxMake` 2183, `dmFxShow` 2222, `dmDrawFx` 2238).
   - `-` (key 45), or a tap on the footer row (y ≥ 198), switches the lower half of the locus page between the allele
     picture (as in beta 2) and the formula view (`dmFrm`). The `+` key and the picture-band tap act only in picture view.
   - The formula view shows, from y 96: the caption and the badge ("exact (CAS)" / "decimal", dodger blue); the LR with
     theta, wrapped (up to 4 lines, magenta); the LR at theta = 0 (blue); a reading note
     "(p×th-p-th) = -(th+(1-th)p): signs pair off" when the CAS's factors have that form and a line is free; and
     "your p, th = 0.010: LR = 56.793 (the program's value)" — the number is `dmLR`, the PPL engine's, never the CAS's.
   - A formula longer than 4 lines says "With theta: 740 characters, too long to show." and the theta = 0 formula
     gets the lines instead; an input over `dmCasMx` (3000 characters) is not sent: "Too many terms to send to the CAS
     here."; a CAS failure: "The CAS did not answer: no formula here." with the "decimal" badge. An excluded locus
     (LR = 0) and an Hd-impossible locus (no LR) are explained in words and the CAS is not asked.
   - Display: `dmq1 … dmqm` → `p` + allele name (`p14`, `p14.3`), `dmt` → `dmTHG` (= "th" until GfxProbe T14 shows
     that CHAR(952) θ renders; one line in `dmInit`), `*` → × (CHAR 215). `dmWrap` (b3 535) breaks after `)` or ×,
     before a joining `+`/`-`, or after a `/` that precedes a bracket, choosing the place with the fewest brackets
     open, so a factor such as `(p14×th-p14-th)` stays on one line and no number or fraction is split.
   - Footers: picture view "tap here/- = formula, + = Hp/Hd, arrows = locus"; formula view
     "tap here/- = picture, arrows = locus, Esc = menu".
2. **How the formula is built** (new, beside the engine: `dmCasP` b3 970, `dmCasLR` 1065).
   - `dmCasP` is a second, separate copy of `dmProb`'s structure that writes TEXT: the inclusion-exclusion sum over the
     subsets S of U, each term the 2x factors `(t(M\S)+j)*dmt+(1-dmt)*p(M\S)` with p(M\S) a sum of the symbols
     `dmq1 … dmqm`, the common denominator `(1+(nT+j-1)*dmt)` written once. Only whole numbers appear (typed-allele
     counts and indices, via `dmIStr`). `dmCasLR` sends `factor(normal((P(E|Hp))/(P(E|Hd))))`; the theta = 0 version
     drops theta altogether.
   - `dmFxMake` asks the CAS only when the CAS text differs from the one it last answered (`dmFxK`, `dmF0K`): two
     calls for a new locus, none when coming back to the same one, never during the theta drag. It writes
     "asking the CAS ..." on the screen first (G1 speed unknown). An answer containing a decimal point (approximate
     mode) is treated as no answer.
3. **The CAS kit** (b3 471-511): `dmIStr` and `dmCas` copied from BRIEF_CAS, including the coordinator's later
   quote-strip (one surrounding pair of `"` dropped before the undef/error test). `dmCas` is the ONE CAS call.
   Text helpers `dmRepl` (INSTRING/LEFT/MID only) and `dmWrap`.
4. **Theta at the ladder edge** (new `dmBand` b3 1079, `dmEdge` 1102; drawn in `dmThStatic` b3 1735, b2 1356).
   - The first theta above the session theta at which the combined LR leaves its ENFSI band (edges LR 10⁻⁶ … 10⁶ as
     in `dmVerbal`, both sides). PPL only: the 21 cached curve points bracket it, then 0.06, 0.08, 0.1, 0.15, 0.2,
     0.25 via `dmCombAt`; then bisection on log10 LR(θ) − log10(edge) with `dmCombAt` to a width below 1E-8.
   - On the theta plot, in orange, composed once into G2 with the rest of the static picture: a dotted vertical line
     at that theta, a dotted horizontal line at the edge's height from the axis, a dot where they meet, and
     "band edge LR 1,000" / "at theta 0.0136" at the top right of the box. Past 0.05: only the text,
     "at theta 0.0891 (off plot)". No crossing up to 0.25: "no band edge" / "up to theta 0.25". An exclusion: nothing.
   - Cached (`dmEdOK`): `dmRecalc` and `dmClearLoci` gain one line each to clear it (b3 816, 1280). Adopting a new
     theta (Enter on the plot, or the menu) therefore recomputes it.
   - Worked example (θ 0.01, LR 3,981.5, "strong"): the edge LR 1,000 is reached at **θ = 0.0891** — far past the
     conservative 0.03, so the verbal conclusion survives any usual theta.
5. **Help page 4** (b3 2793): the formula view and the band edge in teaching terms. The pager now runs to 4 pages
   ("(n of 4)"); help page 3's locus-page line now says "arrows: loci, -: formula."
6. **State** (b3 313-332): `dmFrm dmFxK dmFxT dmFxS dmF0K dmF0T` / `dmF0S dmCasOK dmTHG dmCasMx dmEdT dmEdV` / `dmEdOK`,
   initialised in `dmInit`. Header: "What changed in beta 3", firmware line, HOW TO USE step 4, file map.
7. **"More" soft-key page: not needed.** The six soft keys are unchanged; the new view has a hardware key (`-`) and a
   tap target (the footer row), and the band edge is part of the existing theta plot.

## Which presets give a formula that fits (desktop Giac 1.9; labels 10, 11 …; 4 lines × 48 characters)

| Preset | alleles | theta formula | theta = 0 |
|---|---|---|---|
| 1 V+S vs V+1U | 2, 3, 4 (all genotype patterns tried) | shown, 2 lines | shown (1/(2 p14 p15), 1/(p16+p17)^2 …) |
| 2 S+1U vs 2U | 4; 3 | shown, 2 lines; 4 lines | shown |
| 2 S+1U vs 2U | 2 | **too long** (268-318 chars) | shown (54-59 chars, 2 lines) |
| 3 S vs 1U | 2 | shown, 2 lines | shown (1/(2 p16 p17)) |
| 4 V+S+1U vs V+2U | 6; 4 with a homozygous victim | shown, 2 lines; 4 lines | shown |
| 4 V+S+1U vs V+2U | 3, 4, 5 (distinct alleles) | **too long** (244-740 chars) | shown, 2-5 lines |
| custom V+S+T vs V+T+1U | 5, 6 | shown, 2-3 lines | shown |
| custom S+2U vs 3U (general case) | 4 | **not sent**: input 3,315 > 3,000 | shown, 5 lines |

The longest CAS input any preset can produce (every allele count 2-8, every genotype pattern) is 2,875 characters
(preset 4, 6 alleles), under `dmCasMx` = 3000.

## Gate (final file)

```
=================== DNAMixLR_beta3.txt ===================  (bash check.sh NEW DNAMixLR_beta2.txt)
--- 1. kit lint (errors) ---               kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW / ORIG) --- (empty) / (empty)
--- 2b. HARD errors (E2 E3 E6 E8 E10 E11)  none
--- 3. lint_ppl structural ---             2072 checks, 15 problems (beta 2: 1690, 7). The 8 new ones are known
     false positives: "STRING() with 1 args" is the kit's STRING(CAS(dmS)); "STRING() with 2 args" x 7 are INSTRING(...)
     calls read as STRING(. The other 7 are beta 2's (entry-point/EXPORT noise, 'lgG' not a GROB).
--- 4. full parse ---  PARSE FAIL <ppl>:246 expected KW, found OP ';'   (the forward declaration)
                ORIG:  PARSE FAIL <ppl>:202 (same construct).  Masked (forward declaration, EXPORT and file-level
                LOCAL lines commented out): PARSE OK (71 functions; beta 2 60 + 11 new).
--- 5. ---  3015 lines, 126016 bytes; no non-ASCII in code
ppl_gate_v1.py NEW ORIG: ppl_check_v3 clean (orig clean), hard errors none, lint 2072/15 as above.
fleet_names_v2 over the newest version of every program in out/ (27 files, incl. CASProbe_beta1, ChiTable_beta3,
  BayesTree_beta8, ErrorRate_beta1, TrendTest_beta3, ScatterLab_beta2): 1233 routine names, 0 collisions, 0 untagged,
  0 mixed-tag, 0 built-in matches.  (Over every *.txt in out/ it lists DNAMixLR_beta1a/beta2 vs beta3 pairs only.)
```

## Verification (`verify_DNAMixLR_beta3.py`, output in `verify_DNAMixLR_beta3_output.txt`: 0 failures)

```
Part A: every CAS template in desktop Giac (icas), against the Python engine
PASS Giac formula = Python engine, 20 loci x 6 frequency sets x 6 thetas   worst relative difference 2.66e-13
PASS Giac theta = 0 formula = Python engine at theta 0   worst 5.81e-14
PASS the longest CAS input any preset (1-4) can produce fits dmCasMx = 3000   2875 characters, preset 4, 6 alleles
PASS custom, 3 unknowns: 3315 characters > 3000, so the program does not send it ("too many terms")
  worked example as Giac simplifies it:
    locus 12,13,14,15: (3×th+1)×(4×th+1)/(2×(th×p15-th-p15)×(p14×th-p14-th))      theta 0: 1/(2×p15×p14)
    locus 8,9,11:      (3×th+1)×(4×th+1)/(2×(th×p11-th-p11)×(p9×th-p9-th))        theta 0: 1/(2×p11×p9)
    locus 16,17:       (3×th+1)×(4×th+1)/((th×p16+th×p17-5×th-p16-p17)×(th×p16+th×p17-4×th-p16-p17))
                                                                                   theta 0: 1/(p16+p17)^2
Part B: the PPL program in the harness (ppl_run_v3, Giac and cas='fail')
PASS the PPL dmCasLR text = the Python builder, every case (theta and theta = 0)
PASS CAS formula (Giac, from the PPL text) = the PPL engine dmEval, 240 comparisons   worst relative difference 8.47e-13
PASS band edge: worked example, theta 0.01 / 0.03 / 0     program 0.08914508 (LR 1000) = brentq 0.08914508
PASS band edge: locus 1 alone; "just above 10"             no edge up to 0.25 (both)
PASS band edge: rare alleles p14 = p15 = 0.01              program 0.01355674 (LR 1000) = brentq
PASS band edge: preset 2, two loci                         program 0.10885597 (LR 10) = brentq
PASS formula view (Giac): badge, formula, theta = 0 line, value line; two CAS calls, both answered; footer
PASS the same locus again: no new CAS call (cached); a tap on the footer row switches back to the picture
PASS three loci visited in the formula view, then back: 2 calls per new formula (8)
PASS cas=fail: decimal badge, "did not answer", the value line, no error
PASS preset 4, 4 alleles: "too long to show" for theta, theta = 0 formula shown instead
PASS custom, 3 unknowns: "Too many terms to send to the CAS here.", only the theta = 0 call
PASS exclusion: LR = 0 explained, no CAS call; no band edge to look for (dmEdT = -2)
PASS theta plot: "band edge LR 1,000 / at theta 0.0891 (off plot)"; theta drag: no CAS call at all
PASS an edge inside the plot (theta 0.0136): text, and the orange dot at x 90
PASS stale-key run: menu -> example -> bar -> locus page -> formula -> quit, no skipped page
PASS dmProb / dmKnowns / dmTyped / dmEval byte-for-byte beta 2
```
A width sweep of the formula views, theta plot and help pages (harness estimates) found no new text past the screen
edge; one beta 2 picture line ("1 unknown must supply nothing new (any of M): P = 0.272") is clipped by its own width
argument, as in beta 2.

## (b) DEVICE TEST CHECKLIST (least → most risky)

1. **Run CASProbe beta 1 first**, on the G2 and the G1. If it reports a call form other than `STRING(CAS(s))`
   (T07), change the IFERR line in `dmCas` (b3 494) and nothing else. Note T14 (exact or approximate mode: the formula
   view needs exact mode, otherwise it shows "decimal"), T20 (diff/simplify), T26 (IFERR catches a CAS syntax error).
2. **Paste and compile.** 71 routines; new file-level LOCAL lines b3 314-330. If the paste stops, note the cursor line.
3. **Everything beta 2 did** (its checklist, items 2-15) should be unchanged: menu, table, drop a locus, locus plot,
   waterfall, picture, fallacy, ladder, theta plot and drag, exclusion, twelve loci, preset 3.
4. **Help (item B):** four pages; page 4 in magenta/blue/orange lines, nothing past the frame.
5. **Theta plot, band edge in the plot.** Clear, Enter a locus: 4 alleles 12/13/14/15, p 0.1/0.2/0.01/0.01, victim
   1/2, suspect 3/4 (θ 0.010). Theta plot: an orange dotted vertical line at θ ≈ 0.0136, an orange dotted horizontal
   line from the axis at log10 LR = 3, an orange dot where they meet the blue curve, and "band edge LR 1,000" /
   "at theta 0.0136" at the top right of the plot box. Drag across it: the drag behaves as in beta 2 (no CAS involved).
6. **Theta plot, band edge off the plot.** Load the worked example: "band edge LR 1,000" / "at theta 0.0891 (off plot)",
   no orange lines. Adopt θ = 0.03 (drag, Enter): the text stays 0.0891 (recomputed from the new θ, same edge).
   Exclusion (beta 2 item 13): no orange text at all.
7. **Formula view, worked example — the CAS steps.** Results → Locus soft key → tap bar 1 twice (locus page), press `-`.
   You should see "asking the CAS ..." briefly (**time it on the G1**), then:
   `LR as a formula in p and th (theta):` and **exact (CAS)** at the right;
   `LR = (3×th+1)×(4×th+1)/(2×(th×p15-th-p15)×` / `(p14×th-p14-th))` (magenta; the Prime's Giac may order the
   factors differently — any order is right if the theta = 0 line matches);
   `theta = 0: LR = 1/(2×p15×p14)` (blue); `(p×th-p-th) = -(th+(1-th)p): signs pair off` (grey);
   `your p, th = 0.010: LR = 56.793 (the program's value)`. Footer "tap here/- = picture, …".
8. **Right/Left in the formula view.** Locus 2: `…/(2×(th×p11-th-p11)×(p9×th-p9-th))`, theta 0 `1/(2×p11×p9)`,
   LR 19.083. Locus 3: two `(th×p16+th×p17-…)` factors, theta 0 `1/(p16+p17)^2`, LR 3.674. Back to locus 1:
   "asking the CAS ..." appears again (the cache holds one locus — expected).
9. **Toggle back.** Tap the footer row: the picture returns; `-` again: the formula, with no new "asking" (cached).
10. **Preset 3** (beta 2 item 15 data, θ 0.010): `LR = (th+1)×(2×th+1)/(2×(th×p17-th-p17)×` /
    `(p16×th-p16-th))`, theta 0 `1/(2×p17×p16)`, value 8.067, and the green "single source: LR = 1/RMP,
    theta-corrected" under it.
11. **A long formula.** Hypotheses 4 (V+S+1U vs V+2U), a locus 10/11/12/13, p 0.1/0.2/0.15/0.05, V 1/2, S 3/4:
    "With theta: 740 characters, too long to show." and the theta = 0 formula on 4 lines starting
    `theta = 0: LR = (p10+p11+p12+p13)^2/`; value 14.569. (The Prime's character count may differ.)
12. **The CAS switched to approximate mode** (CAS settings, uncheck Exact), then step 7 again: expect "decimal", no
    formula, the value line, and no error. Restore Exact afterwards.
13. **Home's number format Fixed 2** (Home settings), step 7 again: the formula must be unchanged (no decimal
    points or digit-group marks can reach the CAS: all CAS text is built by `dmIStr`). Restore Standard.

## (c) Not confirmed, left as it was

- **Nothing about the CAS has run on a Prime.** The call form, `factor`, `normal` and the answer's text form are
  desktop Giac 1.9's; the Prime's Giac is older and may order factors or print signs differently (display only — the
  numbers shown come from the PPL engine). CASProbe does not test `factor` or `normal`, nor inputs of 300-2,900
  characters (preset 2 with 4 alleles sends 2,123; preset 4 with 6 alleles 2,875). If long inputs fail on the
  device, lower `dmCasMx` in `dmInit`.
- **Speed on a G1:** desktop Giac takes 30-50 ms per formula; the Prime's time is unknown ("asking the CAS ..." is shown).
- **θ glyph:** `dmTHG = "th"`; switch to `CHAR(952)` only after GfxProbe T14 says it renders.
- **Font-1 widths** are estimates (48 characters a line is assumed); the tightest are the 48-character formula lines
  and the value line.
- **The formula cache holds one locus** (and one theta = 0 formula); revisiting a locus asks again. Intentional
  (small state), not a bug.
- **The sign note** is a reading hint for the CAS's normalised factors (−(θ + (1−θ)p) written as (pθ − p − θ)); it is
  shown whenever the CAS answer has that shape.
- **Band edges beyond θ 0.25** are not searched ("no band edge up to theta 0.25"); the session θ can be up to 0.5.
- Everything in beta 2's "not confirmed" list still stands (G2 scene buffer, drag loop, TEXTOUT_P into a grob
  parameter, CHAR(8594), MAKELIST's Home K in dmProb, NRC II citation numbers, LR = −1 loci, DM_LR with drops).
