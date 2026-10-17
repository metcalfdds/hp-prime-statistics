# CICatcher beta 1 — notes

*16 October 2026. A new program, not yet run on hardware. Pure PPL, 1,535 lines, tag `cq` (glued style: `cqDraw`, `cqLimits` …).*

From the fleet review of 16 Oct 2026, §7 item 4: the confidence-interval coverage simulation that answers **"95 % of WHAT?"**. Files:

- `CICatcher_beta1.txt` — the program (`EXPORT CICatcher()`, zero arguments)
- `verify_CICatcher.py` — every formula and every quoted number checked against scipy/statsmodels, and the program's own routines run in the `ppl_run_v1` harness
- `cicatcher-guide_beta1.md` — the user's guide

## 1 · What it does

1. **Welcome page**, then **setup**: `CHOOSE` the interval — mean σ known (z), mean σ unknown (t), proportion Wald, proportion Wilson — then one `INPUT` form: μ, σ, n, level (means) or p, n, level (proportions). Defaults are pedagogy: μ = 100, σ = 15, n = 10; p = 0.10, n = 20 (where Wald visibly falls short); level 0.95. The level may be typed as 0.95 or 95. Bad values get a teaching message and the form comes back.
2. **The main screen** (one G1 frame, one blit, then `DRAWMENU`): the truth as a 2-px green vertical line; the most recent 50 intervals as 1-px horizontal lines at a 3-px pitch, newest on top, each with a 3 × 3 dot at its estimate — **blue if it caught the truth, red if it missed**; header line 1 "caught 47 of 50 (94.0 %), all 237: 95.4 %", line 2 "target 95 %" (magenta) and "t, μ = 100, σ = 15, n = 10" (green); an x-axis with Heckbert ticks and light grid lines; for proportions, light grey "impossible" zones below 0 and above 1 (only Wald lines reach them). The window is frozen per run at the truth ± 6.5 standard errors, so a higher level visibly *lengthens* the lines; a line that runs off the window is cut and notched.
3. **Soft keys** `{"+1","+10","+50","Conf","n","Menu"}`: +1 animates one sample (the stack slides down 1 px a frame for 3 frames, the new sample's values appear in the bottom panel, its interval grows grey out of its estimate over 5 frames, and only then turns blue or red; the header leaves it out of the counts until then); +10 / +50 add at once behind a "Sampling k of N ..." box; Conf = `CHOOSE` 80/90/95/99 %; n = `INPUT` (a fresh run); Menu = `CHOOSE` new setup / reset the counts / Help / Quit.
4. **The showcase — drag the level.** The strip x ≥ 298 is a slider from 50 % (bottom) to 99.9 % (top), spaced by z* rather than by percent (equal finger travel = equal change in length; 80 % sits a quarter of the way up), with grey ticks at 50/80/90/95/99 and a magenta knob; it snaps to 80/90/95/99 % within 0.3 %. While the finger is down, every MOUSE sample sets the level and **every visible interval is recomputed from its stored estimate and SD — no resampling** — so lines lengthen, red turns blue, and both header counts update live. Up/Down step the level (whole percents; 99 → 99.5 → 99.9).
5. **Tap a line** (or slide up and down the stack; Left/Right step one line): the line is drawn 3 px thick on a light orange band, and the bottom panel shows that sample — for a mean, its n raw values as black dots on the plot's own axis (off-window values pulled to the edge in grey), the green truth tick, the interval and x̄ under them; for a proportion, n yes/no tiles (black = yes); then one line: "x̄ = 103.2, s = 14.1: 93.1 to 113.3, missed by 1.3" or "p̂ = 3/20 = 0.15: -0.01 to 0.31, caught". A tap on the picked line again, or on the panel, closes it.
6. **Help** (five drawn pages): what the 95 % refers to (the method's long-run catch rate, not one interval's probability); level vs width, z vs t (t(9) = 2.262 vs 1.960; z-with-s would catch only 91.8 % at n = 10) and the **engine note** ("t critical value: STUDENT_ICDF (built-in)" / "bisection on STUDENT_CDF" / "not needed yet"); Wald vs Wilson (87.6 % vs 95.7 % at p = 0.10, n = 20; 12.2 % of samples have p̂ = 0 and a zero-width Wald interval; Wald reaches 93.2 % at n = 100); a CJ example (fear of walking alone at night, 38 of 100 residents, 28.5 % to 47.5 %, the right and wrong sentences); keys and touch.
7. **Quit** returns "CICatcher: 226 of 237 caught the truth (95.4 %) at 95 %, t, μ = 100, σ = 15, n = 10; see CQ_COVER" and leaves `CQ_TOTAL`, `CQ_HITS`, `CQ_COVER` in Home.

### How the counts follow the slider without resampling

Each interval contains the truth at level L exactly when one pivot q is at most the critical value: z: |x̄ − μ|/(σ/√n); t: |x̄ − μ|/(s/√n); Wald: |p̂ − p|/√(p̂(1 − p̂)/n) (∞ when p̂ = 0 or 1); Wilson: |p̂ − p|/√(p(1 − p)/n) (the Wilson interval is by construction the set of p passing that score test). So `cqCatch` stores each interval's **catch level** — the lowest level on the 0.1 % grid (500 … 999 thousandths; 1000 = never) at which it catches, `CEILING(1000 (2 CDF(q) − 1))` — and a 501-bin histogram of catch levels over every interval ever drawn. A colour is `cat ≤ L`; the visible count is a loop over 50; the long-run count moves with the level by adding the histogram bins between the old and new level (`cqSetLevel`). The level itself is always a whole number of thousandths, so this is exact for all intervals, not just the 50 on screen, and costs a few additions per drag step.

### Critical values

- z*: `NORMALD_ICDF(0, 1, 0.5 + L/2000)` (verified), cached per level.
- t*: `STUDENT_ICDF(df, q)` inside `IFERR`, and **used before it is trusted**: the answer must be positive and give `STUDENT_CDF(df, t*)` within 1E-6 of q. Otherwise bisection on `STUDENT_CDF` (verified): bracket by doubling from 4 (df = 1 at 99.9 % needs 636.6), then 60 halvings. `cqEng` records which ran; the help page shows it. Cached per level (`cqCVc`, 500 entries), so a drag over levels already visited costs nothing even on the fallback.

## 2 · Verification (verify_CICatcher.py — PASS, 0 failures, 88 s)

```
A. formulas vs scipy/statsmodels, 4,000 random cases each
   z vs norm.interval 2.2e-14 (/σ) · t vs t.interval 1.1e-13 (/half-width)
   Wald vs proportion_confint 'normal' 5.6e-15 (statsmodels clips to [0,1]; the PPL shows raw limits)
   Wilson vs proportion_confint 'wilson' 4.8e-15
B. the PPL routines in the harness
   t* via STUDENT_ICDF: exact; via the bisection fallback: worst relative error 1.1e-13 (df 1-99, 50-99.9 %)
   a wrong STUDENT_ICDF answer (arguments swapped) is rejected by the CDF check -> bisection
   cqLimits on 1,500 PPL samples x 8 levels, 7 settings (incl. t n = 2, Wald n = 5, Wilson n = 100):
     worst 5e-13 of the half-width; colour-from-catch-level == contains-the-truth: 0 mismatches;
     long-run tally after cqSetLevel == direct recount at every level
C. coverage at the defaults           exact     100,000 replicates
   z  (mu 100, sigma 15, n 10)        0.9500    0.9496
   t  (same)                          0.9500    0.9501
   Wald  (p 0.10, n 20)               0.8760    0.8760
   Wilson (p 0.10, n 20)              0.9568    0.9571
   z with s at n 10: 0.9184 · Wald p 0.10 n 100: 0.9324 · P(phat = 0) at n 20: 0.1216
   by level, p 0.10 n 20: 80 % Wald 0.835 Wilson 0.746 · 90 % 0.867 / 0.957 · 99 % 0.878 / 0.989
   every number on the help pages checked against these (87.6, 95.7, 93.2, 12.2, 91.8, 2.262,
   1.960, 0.095, 28.5 to 47.5)
D. the PPL's own sampler, 20,000 intervals per type: z 0.9476, t 0.9479, Wald 0.8755, Wilson 0.9570
   (all within 4 SE of exact); mean of xbar 100.03 / 99.94, mean of s^2 225.3 / 224.1 (225)
E. scripted session (t: +1, +50, slider to 99.9 and back to 80, tap a line, arrows, Conf 99, n 25,
   +, Help 5 pages, new Wald setup, +50, tap, Quit): runs to Quit, every scripted event used,
   no MSGBOX, engine note "STUDENT_ICDF (built-in)", exports CQ_TOTAL 50 CQ_HITS 44 CQ_COVER 0.880
F. keyboard-only session (Up to 99.9, Down to 50, Left/Right, -, reset, cancelled setup, Esc);
   Wilson n = 100, Wald n = 5, t n = 2 sessions with drags; a whole session with STUDENT_ICDF
   raising: help says "bisection on STUDENT_CDF", t* still 2.262157.
   One full frame (50 t intervals + a picked sample): 142 shapes, 17 texts.
```

The harness routes bare `GETKEY`, `MOUSE` and `TICKS` but not a bare `RANDOM`; the script adds that one line (the bare form is what NormExplorer's device-run sampler uses). Layouts were also rendered off-device from the harness records and inspected (main screen, slider at 99.9 %, picked sample, +1 animation, Wald with grey zones, help pages, welcome).

## 3 · Gate

```
kit lint: 0 errors
ppl_check_v3: 0 errors, 0 warnings (no codes at all); hard E2/E3/E6/E8/E10/E11: none
lint_ppl: 911 checks, 5 problems -- all known noise ('no function named CICatcher_beta1',
  three EXPORT-discipline lines, 'entry point not EXPORTed')
full parse: fails at line 131, the file-level LOCAL after the EXPORT list -- the kit's limit;
  ChiTable beta 1k and GaltonBoard beta 1b fail on the same construct.  The harness's parser
  reads the whole file and ran it (sections B-F).
fleet_names_v2 over out/*.txt (42 files): 0 untagged, 0 mixed-tag, 0 built-in matches; no
  collision involves a cq name (the 274 listed are between parallel versions of OTHER programs
  now in the folder, e.g. NormExplorer beta 41 / 42)
```

Tag `cq` chosen (not `ci`, which is the built-in Ci). All 51 routines and every LOCAL / parameter passed E11; one clash was caught on the way (`suB` = `SUB`, renamed `suSD`).

## 4 · Device test checklist (least to most risky)

1. **Paste and compile.** If the paste stops at `STUDENT_ICDF` (line ~353), the name is unknown to this firmware: tell Claude; the bisection path alone can replace that line. (hp-prime-kit saw `STUDENT_ICDF(3, 0.5) = 0` on the emulator, so this is not expected.)
2. **Welcome page** draws, any key or tap moves on; **setup** CHOOSE shows four items (with σ glyph), the INPUT form shows μ:, σ:, n:, Level: with 100, 15, 10, 0.95. Try Level = 95 (accepted as 0.95) and σ = 0 (message, form returns).
3. **Main screen, empty**: "no intervals yet ...", axis 70 … 130, green line at 100, slider ticks 50/80/90/95/99 with the magenta knob beside 95, the two-line blue legend above the soft keys; the soft-key labels survive.
4. **+50**: the orange "Sampling k of 50 ..." box, then 50 lines. Note the time on the G1 (expected a few seconds) and that the header reads about "caught 47 of 50".
5. **Header text widths**: "caught 50 of 50 (100.0 %)," must not run into "all 237: 95.4 %" at x = 172; "target 99.9 %" must not run into the green description at x = 92. The longest font-1 lines are 48 characters (the legend; help lines 46-48) — ChiTable's 48-character help lines fit, so these should; look.
6. **+1**: the stack slides, the new sample's dots appear in the panel, a grey line grows, then blue or red, and the panel gets its verdict. Watch the speed on the G1 (8 full frames + 40 ms pauses).
7. **Tap a line**: band and thick line; panel dots, green tick, interval; the text "x̄ = …, s = …: … to …, missed by …" (t, the longest form, ~48 characters: check it is not cut on the right). Slide the finger up and down the stack: the panel follows. Tap the same line again: the panel closes. Left/Right step the picked line.
8. **Up/Down**: 95 → 96 … 99 → 99.5 → 99.9; Down to 50 and it stops. Lines lengthen/shrink, colours and both counts follow.
9. **The drag (the showcase)**: put a finger on the right edge and slide slowly from bottom to top and back. Every line must follow live; the counts update; the knob snaps at 80/90/95/99. **Measure the frame rate on the G1** (one frame is ~142 shapes + 17 texts and 50 `cqLimits` calls). Lift: the program must not freeze (capped drain); a key press during the drag ends it.
10. **Conf** (CHOOSE 80/90/95/99) and **n** (INPUT, a fresh run; n = 1 or 101 refused).
11. **Menu → Help**: five pages; the engine line on page 2 should read "STUDENT_ICDF (built-in)" after a t run. **This is the device test of `STUDENT_ICDF`** — if it says "bisection", the built-in failed or disagreed with `STUDENT_CDF` (tell Claude). Esc leaves help early.
12. **Proportions**: Menu → New setup → Wald, defaults. +50: grey zone left of 0, red dots stuck at 0 (p̂ = 0, zero width), the all-count drifting toward ~88 %. Drag to 99.9 %: the 0-dots stay red. Then Wilson: ~96 %, no line enters the grey. Tap a line: the yes/no tiles. Try n = 100 (tiles 2 px apart).
13. **t with n = 2** at 99.9 %: most lines run off both edges (t* = 636.6) — notches at the edges, no error.
14. **Quit**: Home shows the summary line; `CQ_TOTAL`, `CQ_HITS`, `CQ_COVER` hold the run. `K` holds the last MAKELIST count (expected, house rule until GfxProbe T19).

### The "More" soft-key convention (Roger, 16 Oct 2026)

Considered and **not applied**: the main screen's actions fit in six soft keys, `{"+1","+10","+50","Conf","n","Menu"}`, and every feature already has a soft-key or key route (new setup, reset, Help and Quit through Menu, slot 6; the level through the slider and Up/Down; picking a line through a tap and Left/Right). Paging would only hide +50 or Conf behind a page turn. If a later version adds a seventh action (for example a z/t toggle or a "drop 1,000" item), slot 6 becomes "More" with Menu moved onto page 2, in the BRIEF_TOUCH shape. The help pages say nothing about "More" because the key does not exist in this version.

## 5 · Not verified, stated plainly

- **Nothing has run on a Prime.** The constructs are all fleet-verified (file-level LOCAL, `DRAWMENU` + taps at y ≥ 218, `MOUSE` polled each frame while a finger is down as NormExplorer's x₀ drag, the capped `TICKS` drain, `IFERR`, `RECT_P` with fill, `TEXTOUT_P` with width, `NORMALD_CDF/ICDF`, `STUDENT_CDF`, `LN`, bare `RANDOM`, `MAKELIST` with `K`, `CHAR()` glyphs including 57344/57345, 956, 963, 215, 8645, 8646) **except `STUDENT_ICDF`**, which is wrapped and checked as described.
- **The 5,000-value raw list** (50 samples × n ≤ 100): within the Prime's documented 10,000-element list limit; n is capped at 100 for that reason (proportions too, so the CJ example uses n = 100, not 400).
- **Drag frame rate on the G1** is not known; the arithmetic per frame was kept small (inline row arithmetic, one `cqLimits` call per line, critical values cached), but this is the program's heaviest frame.
- **Font widths**: the harness estimates font 1 at 5.5 px a character, ChiTable's notes at 6.5; the longest lines (48 characters) are at ChiTable's verified maximum.
- **The `TICKS` pause** (`cqPause`, 40 ms) is used instead of `WAIT(0.02)`, whose effect on keys is still a GfxProbe question.
- **Wilson at 80 %** catches only 74.6 % at p = 0.10, n = 20 (discreteness: coverage of any interval for a count oscillates with n and p). It is true and worth showing, but it is not on the help pages — the guide mentions it.
- Display limits: a Wald lower limit just below 0 prints as e.g. "-0.01" (true to the formula; the help page calls such values impossible).
