# HP Prime Lessons Learned
*Roger Metcalf & Claude · v7e · 12 October 2026 (v7d 11 October 2026; v7c, v7b, v7a and v7 on 10 October 2026; v6 6 October 2026; v5 3 October 2026; v4 1 October 2026; v3 rewritten 28 September 2026)*

**What changed in v7e** (a search index for the library; no PPL rule changed):

- **The whole of `D:\HP-Prime` is now searchable in about a second** (box below, §14.11). `Library_Index.db` holds the text of every program and text file in all ~1,650 zips and the loose folders, every `.hpprgm`/`.hpappprgm` decoded (1,658 sources; 100 are compiled objects with no source, indexed by their strings), the text layer of every PDF (628 of 1,051 have one; the rest are scans), and the names of all ~67,000 files. `libsearch_v1.py` searches it; `library_index_build_v1.py` refreshes it incrementally. Build and search instructions are in `CLAUDE.md`.
- Three `.hpprgm` variants turned up while building it: the usual binary header + UTF-16LE source; plain UTF-8 text that merely has the extension (our own September device pulls); and objects with the `7C 61 8A B2` header but no UTF-16 source at all. `Decode-HPPrime.ps1` handles only the first.

**What changed in v7d** (fleet table completed; the exit review extended to the five programs that arrived on 9 October):

- §15 now lists GaltonBoard, TrendTest, TestChooser and DNAMixLR, which were committed to the repository on 9 October 2026 but had never been entered here, and marks CentralLimit as the app it is. All five are still untested on hardware.
- GaltonBoard beta 1a, TrendTest beta 1a and TestChooser beta 1a: every finger-lift drain goes through a capped `xxDrain()` (§7), and GaltonBoard and TrendTest return their summary line instead of printing it. DNAMixLR needed nothing (key-only waits, no trailing `PRINT`). All four already carried tagged helpers (`gb`, `tr`, `tc`, `dm`); `fleet_names_v1.py` over the whole fleet of 20 files: 0 collisions, 0 untagged.
- The masters of these four now live in `D:\HP-Prime` alongside the rest (until 11 October they existed only in the Project and the repository).

**What changed in v7c** (one new rule, device-found, and three loop rules from the fleet exit review, 10 Oct 2026):

- **All programs share ONE pool of routine names** (§5). Roger ran StudRange, hit a runtime error that opened the Program Editor, could not leave it, and ended up looking at a Burr3 screen; only a reset got him out. Five fleet programs defined `NiceNum`, nine defined `fmtp`/`FMTP`/`FmtP`, three `lngamma`, two `Drain`, `FMT` and `ShowHelp`. A call to a helper can land in another program's copy of the same name, whichever was compiled last. The User Guide's "a function without EXPORT is visible only inside its program" does not hold on the device; the library says the same (hummingbird1986: "the global namespace is flat and shared across every program on the device — name collisions between .hpprgm files are the main failure mode"; hp-prime-kit `ppl.global-namespace`, `ppl.compilation-order`). **Rule: every non-EXPORT routine carries the program's tag** (`sr_NiceNum`, `b3_fmtp`, or the `csName` / `cltName` style). `fleet_names_v1.py` checks every program against every other, ignoring case; it found 6 collisions in the fleet and 0 after the rename.
- **Read x and y from a touch list only after checking `SIZE`** (§7). `WAIT(-1)` hands back a list for a touch, and a finger lift can be a one-element list; `kk(2)` on it is a runtime error, which opens the Program Editor at the failing line — the "screen that listed the program". StudRange and BayesTree both did this.
- **A finger-lift drain gets a time limit** (§7). `REPEAT UNTIL MOUSE(1) == -1;` with no limit holds the program for ever if the touch reading sticks; `csDrain()` / `cltDrain()` give up after one second via `TICKS`.
- **Finish with `RETURN`, not `PRINT`** (§7), unless the program really has Terminal output to scroll. ChiTable now returns its summary line; Home shows it and no Terminal screen is left open.
- §14 rule 12 (run the fleet check before every paste); §15 lists the renamed versions, none of which has been re-run on hardware yet.

**What changed in v7b** (device confirmations from ChiTable's first runs, G2 and G1, 10 Oct 2026):

- **Soft keys work this way** (§6): draw the frame to G1, `BLIT_P`, then `DRAWMENU({...})` on the screen; read a tap with y >= 218 as key `MIN(6, IP(x / 53.4) + 1)`. The labels never produce a key code. Verified on both calculators.
- **Now in the confirmed-working list** (§3): file-level `LOCAL` state in a standalone program; `INPUT` with its label list taken from a string variable; `MAKEMAT` followed by element assignment into an `EXPORT`ed matrix; `CHISQUARE` (density), `CHISQUARE_CDF` and `CHISQUARE_ICDF` together; `CHAR(967)+CHAR(178)` for the chi-square glyph, `CHAR(8320)`/`CHAR(8321)` for subscript 0 and 1, `CHAR(215)` for the multiplication sign.
- §15: ChiTable beta 1j is tested on the G2 and the G1.

**What changed in v7a** (one observation added to §2):

- **CHOOSE numbers its items itself, and past 9 it uses letters:** items 10, 11 and 12 are labelled A, B and C on the Prime (Roger, 10 Oct 2026, ChiTable's menu). So menu strings should not carry their own numbers, and any on-screen reference to a late item should say "(A)", not "(10)".

**What changed in v7** (one new rule, device-found):

- **Built-in names are matched case-INsensitively** (§5). `LOCAL csR, csC, ...` at the top of ChiSquare beta 1a was rejected at paste time on the G2 with the cursor after `csC` — the parser read it as `CSC`, the cosecant. The program's own name, `ChiSquare`, was `CHISQUARE` (the density) and would have failed next. A routine prefix does not make a name safe: `csC`, `csR`-style names must be scanned against the command list ignoring case, and so must function names and EXPORT variables. `lint_ppl.py` and `ppl_check_v2.py` now do this for file-level LOCALs, EXPORT variables and function names (10 Oct 2026).
- §5's earlier note that `LOCAL fp` parses fine stands as observed, but it is now the odd one out; do not rely on it.
- §15: ChiTable beta 1b (the renamed ChiSquare) joins the fleet.

**What changed in v6** (paths only; no rule changed):

- The master folder is now **`D:\HP-Prime` on Rogers-HP**. The EliteOne died in early October 2026; its files were copied to D: on Rogers-HP, Roger's new main computer, and kept there for space (Roger, 6 Oct 2026). Every `C:\HP-Prime` below is now `D:\HP-Prime` (box above §1, §9a, §14.11).
- The count of zips at the top of the folder is corrected from "about 400" to **about 940** (938 on 3 Oct 2026, mostly from hpcalc.org).

**What changed in v5** (corrections only; no rule changed):

- The University of Delaware Python pages are **Mike Markowski's**. v4 wrongly credited them to "Mark Mitchell" (§9a).
- The box above §1 no longer calls `HPPrimeProgrammingUDelaware.pdf` the only Python document in the library. Streeter's book and a saved copy of Markowski's pages are both in `Community_Library\docs`.
- That PDF is not a ZIP of page images, as v4 said. The copy on Roger's computer is an ordinary 7-page PDF, printed from Markowski's page in January 2024, whose text layer is garbled.
- §9a now says where each Python source is saved in the library.

**What changed in v4:**

- The `LOCAL` rule is now 6 per line (§2).
- Every update gets a new version number, and stale copies are archived (§14.7).
- Search the whole library, not just the Project's 83 programs (box above §1, §14.11).
- Today's PyProbe findings are folded in: argv, matplotl, the module contents, MSGBOX, Terminal scrolling (§3, §7, §8, §9).
- Python's arrival date is corrected from HP's release notes (§8).

Working notes for writing PPL and MicroPython on the HP Prime. Everything here was found on hardware, not read in a manual — where a claim is inferred rather than observed, it says so.

**Verified on:** HP Prime G2 and G1, both running the **2026-09-09** firmware, plus the desktop Virtual Calculator. Firmware matters more than it looks: glyph rendering and app-variable reachability have both proved version-dependent, so a "device-verified" claim is only verified on a stated build.

---

> ## Read this before writing code
>
> Not after. In one September session, four bugs were rediscovered the expensive way — the `STRING` mode, the FREEZE pause, the x-bar glyph, and the LOCAL limit — and all four were already written down here.
>
> Then: **search the whole library** for anything this file does not cover — with the index, not by unzipping: `python3 libsearch_v1.py WORDS` (or `-s "exact text"`, `-r REGEX`, `-n filename`) in `D:\HP-Prime` answers in about a second across every zip, program, decoded `.hpprgm` and PDF there. That means the `.txt` programs uploaded to the Project, plus everything in `D:\HP-Prime` on Roger's computer (Rogers-HP): the fleet, about 940 zips (mostly hpcalc.org), and `Community_Library` (see its `INDEX.md`). `<>` was avoided for a whole session as "unverified" when five corpus programs use it.
>
> Then: **read the uploaded reference PDFs.** Note that `HPPrimeProgrammingUDelaware.pdf` (Mike Markowski's University of Delaware page, printed to PDF in January 2024) has a garbled text layer — it will not turn up in a text search and has to be read as page images. It is not the only Python document in the library: Markowski's pages are also saved as HTML in `Community_Library\docs\markowski_udel\`, and Neil Streeter's *HP Prime Python Activities Book* is `Community_Library\docs\hpprime-python-activities.pdf`. §9a lists every Python source and where it is.

---

## 1 · Which language, and why

**PPL by default.** It is good at calculating, and the native `_P` graphics have no Python equivalent worth reimplementing. Anything that redraws on a keypress stays pure PPL.

**Python (MicroPython) when it makes a program faster, or supplies a needed feature PPL lacks** (Roger's rule, 1 Oct 2026). Compute-heavy engines get a real speed-up, because the math primitives are compiled C while PPL loops are interpreted. Examples are quadrature, root-finding and simulation. A measured case: StudRange's critical value takes about a minute in PPL (60-step bisection) and about 1.5 seconds in Python (secant, ~9 evaluations).

The counter-example matters as much. A live power visualiser with held-key stepping and four reshaded regions per frame gains nothing — its arithmetic is a handful of CDFs per redraw, and the bridge crossing would cost more than the computation. **Of nine programs in this fleet, one was worth converting.**

**CAS only for genuinely symbolic work.** Prefer deriving closed forms off-device, verified against SciPy, and shipping clean numerics. Home capitals A–Z are built-in global reals; CAS lowercase are symbolic; case matters. Keep each program on one side of the fence.

State *why* in one line before splitting any project across languages.

## 2 · Hard limits

- **16 arguments** maximum on user function definitions *and* built-in calls. Pack into lists, unpack inside.
- **`CHOOSE` simple syntax caps at 14 options**; the list form `CHOOSE(var,"title",{...})` is unlimited.
- **`CHOOSE` numbers the items itself**, 1-9 and then A, B, C ... for items 10 and up (device, 10 Oct 2026). Do not number them in the strings, and refer to item 10 as (A) in messages and help text.
- **Never test `CHOOSE`'s return value for a specific number.** Initialise the index variable to 0, call `CHOOSE`, then test the index variable itself. Cancel leaves it 0.
- **`INPUT`'s first argument must be a list of variable NAMES**, written back in place. Value lists give "Invalid Input".
- **Never `INPUT` into a function parameter.** Copy to a `LOCAL`, `INPUT` that, assign back. Parameters as targets fail silently.
- **`LOCAL` statement size: 6 per line. That is the rule** (Roger, 1 Oct 2026). For the record:
  - 7 has been seen to work: BayesTree ships three 7-variable lines.
  - The documented figure was 8.
  - The true ceiling has never been established.
  - New code uses at most 6. Split longer lists across several `LOCAL` lines.
- **`LOCAL` inside `IF`/`CASE` is genuinely rejected.** Hoist it to the top of the function, splitting across several lines.
- **A PPL function cannot modify its caller's variables.** Parameters pass by value. Shared state therefore lives in exported globals, which means every write path to that state must be audited together.
- **Parameter names must not collide with built-in FUNCTION names** (`FP`, `IP`, `LN`, `RE`, `IM`, `SIGN`…). `fp` as a parameter is a syntax error even though `LOCAL fp` parses fine — the parameter parser is stricter.
- **Programs with parameters get an auto-generated argument form** from the catalog. Menu-driven tools take zero arguments and hold defaults internally; plot explorers launched from Home with values keep theirs.
- **`.hpprgm` is binary** (UTF-16LE plus header). Distribute as `.txt` and paste into the Connectivity Kit editor. UTF-8 import can append stray CJK characters at the end — harmless, delete them.

## 3 · Command truths

- **`STRING(value, mode, digits)`: mode 1 is Standard and IGNORES the digits argument.** `0.6826894921` stays full length no matter what you ask for. **Fixed decimals need mode 2.** Easy to miss because most values still look right; only long decimals expose it, and it silently disables computed decimal counts on axis labels. Sweep every `STRING` call before delivery.
- **`CHISQUARE(n,x)` is the DENSITY.** P-values need `1 - CHISQUARE_CDF(n,x)`.
- **`<>` is valid for not-equal** — corpus-confirmed in CHOOSE_R, Hammurabi and PONG. No need to restructure around it.
- **Confirmed working:** `NORMALD` / `NORMALD_CDF` / `NORMALD_ICDF`, `STUDENT(_CDF)`, `FISHER(_CDF)`, `BINOMIAL(_CDF)` including the 4-argument form, `POISSON(_CDF)`, `COMB`, `IFTE`, `MAKELIST`, `CONCAT`, `RANDOM`, `PIXON_P`, `TYPE` (6 = list), `SIZE`, `CHAR`, `ROUND(v, places)`, `MOUSE`, `VIEW`, `mean`, `stddev`, `variance`.
- **Also confirmed (ChiTable, G2 and G1, 10 Oct 2026):** `CHISQUARE` (the density) with `CHISQUARE_CDF` and `CHISQUARE_ICDF`; `MAKEMAT(0, r, c)` followed by `M(r, c) := v` on an `EXPORT`ed matrix; `DRAWMENU({...})` for soft keys (§6); `INPUT({v}, "title", {lbl}, {help})` where `lbl` is a string variable built by concatenation; file-level `LOCAL` variables shared by every routine in a standalone program; `DIM`, `LEFT`, `MID` on strings.
- **Do not exist:** `GEOMETRIC*` — compute p(1−p)^(k−1) by hand. `LNGAMMA` outside the CAS — carry a Lanczos helper, or use Python's `lgamma` and delete it.
- Prefer native `NORMALD_ICDF` to any hand-rolled inverse normal.
- **`MSGBOX` shows about 5 lines.** A 6th line was simply lost (PyProbe beta 1, emulator, 1 Oct 2026). Keep message boxes to 5 lines; put longer output on a screen of your own.

## 4 · Input fields

- **There is no blank input field, and the string workaround fails.** A PPL real always holds a value, so a numeric `INPUT` always shows one. A string variable initialised to `""` does *not* give an empty box — the Prime renders the quotation marks as editable text, and deleting them to type a number is a syntax error. *(Device-verified.)*
- **House default is 0**, unless 0 is illegal for that field — areas, α, confidence levels — where the conventional value goes in: 0.90, 0.05, 0.95.
- **Defaults are pedagogy, not placeholders.** A prefill computed from other session values reads as a stray number and generates a bug report. This happened: `x := μ + σ` with μ=22, σ=4 opened a solver at 26 and looked broken. Use flat constants, or state the rule in the field's help line.
- **Guards should teach.** "σ must be positive" is adequate. "These values give σ = −9.18; the sign of z must match the sign of x − μ" is better, because that *is* the student's error.

## 5 · Reserved words and characters

- **Scan every new name** against PPL keywords: `STEP` (use `stp`), `TO`, `FROM`, `DO`, `OR`, `AND`, `MOD`, `e`, `Re`. The syntax error lands at the usage line.
- **Scan every new name against the BUILT-IN COMMANDS too, ignoring case.** Device-found 10 Oct 2026 (G2, 2026-09-09 firmware): `LOCAL csC` is a syntax error at paste time because `csC` is `CSC`, the cosecant — the editor's cursor lands right after the offending name. A program named `ChiSquare` is `CHISQUARE`, the density function. This applies to LOCALs at file level and in functions, to EXPORT variables and to function names. The routine-prefix convention (`cs…`, `tr…`) is no protection when the prefix plus one letter spells a command: `csC`, `csR` (fine today, but rename on sight), `tcE`… The lint tools check this now; run them before every paste. (`LOCAL fp` was once seen to parse, which contradicts this; treat that as the exception and never rely on it.)
- **Write exponent literals with a capital E.** Corpus code uses `1E10` and `-1E10`; lowercase `1e-9` is unverified, and lowercase `e` is a reserved name. Or just write the decimal out.
- **Avoid bare single-letter lowercase identifiers.** `x` is the CAS's symbolic variable, `i` the imaginary unit, `e` already listed. *Honesty note: a suspected stale-CAS-`x` leak was tested and DISPROVED — CAS `x` was 0. This is cheap insurance, not a diagnosed cause; do not cite it as one.*
- **House convention: prefix every local with a routine tag** — `zsX`, `ndPY`, `pcA`, `awlo`. Makes greps and renames tractable.
- **x-bar is `CHAR(57344)`** (U+E000); **p-hat is `CHAR(57345)`** (U+E001). Single precomposed glyphs in HP's private-use area — they position themselves and scale with the font. **The combining macron U+0304 does NOT stack**; it renders as its own character to the *right* of the x. A hand-drawn `LINE_P` bar also works but needs per-font pixel tuning. Use the glyph.
- **Subscript digits render:** `CHAR(8322)` = subscript 2, paired with `CHAR(956)` = μ for labels like μ₂.
- Characters taken from the on-device **Shift-Chars menu are pre-verified by construction**.
- **`EXPORT` on a helper publishes it in the catalog.** Keep helpers non-`EXPORT`.
- **Non-`EXPORT` does not make a helper private.** Device-found 10 Oct 2026: all programs' routines live in one pool, matched ignoring case, so StudRange's `NiceNum` and Burr3's `NiceNum` were the same name to the calculator, and a call from one program ran the other's code (a runtime error, the Program Editor opening on the other program, a reset). **Every non-`EXPORT` routine carries the program's tag**: `sr_NiceNum`, `b3_fmtp`, `es_Module_Table2x2`, or the glued style `csGrid`, `cltSample`. Before any paste, run `python3 fleet_names_v1.py *.txt` in `D:\HP-Prime`: it lists every routine name defined in more than one program (COLLISION), every untagged helper and every name that matches a built-in when case is ignored. The app hooks `START`, `Plot`, `Symb`, `Num`, `Reset`, `Info` keep their fixed names.

## 6 · Graphics

- Screen is 320×240, origin top-left, y increases **down**. The y-flip: `py := BOT - IP(y/ymax*H)`, then clamp.
- **Compose off-screen and blit once.** `DIMGROB_P(G1,...)`, draw every pass to `G1`, then one `BLIT_P(G0,0,0,G1)`. Drawing straight to `G0` tears visibly. Miss one `G1` argument and that element flickers alone — a useful diagnostic.
- **Shading must iterate pixel columns**, not math samples. Sample loops leave white gap columns; this bit two programs before the rule stuck. Iterate pixels, solve for x.
- **Cache the density — for EVERY curve, not just the first.** If three passes need the same pdf, evaluate it once per pixel column into a list. The trap is doing this for the main curve and forgetting the comparison curve: a second curve read by both an overlap fill and a trace costs two `NORMALD` calls per pixel per frame — 544 on a 272-pixel plot, on top of the main curve's 273. That is the one per-frame cost a G1 can actually feel during a live drag.
- **Precompute anything needed twice in the same frame.** Histogram bar heights were computed once to widen the y-scale and again to draw. Build the array first, then use it in both places.
- **Verified GETKEY codes, the only ones to trust:** Esc=4, Left=7, Right=8, Up=2, Down=12, Enter=30, +=50, −=45, 0=42. Route anything else through Enter → `CHOOSE`.
- **Soft keys, device-verified (ChiTable, G2 and G1, 10 Oct 2026):** compose the frame in `G1`, `BLIT_P(G0, 0, 0, G1)`, then `DRAWMENU({"Edit", "Values", "Clear", "", "Cancel", "Run"})` — it paints the screen, so it goes after the blit and is repeated every frame. A tap with `y >= 218` is a soft key; the slot is `MIN(6, IP(x / 53.4) + 1)` (CHOOSE_R's and LibMenu's geometry). The labels never produce a `GETKEY` code, so keep hardware keys as shortcuts for keyboard-only use.
- **Touch works alongside keys.** Poll both: `REPEAT exK := GETKEY; exM := MOUSE; UNTIL exK > -1 OR SIZE(exM(1)) > 0;`. `m(1)` is the first finger; elements 1 and 2 are x and y. Put the plot box coordinates in shared constants so the touch handler and the drawing code cannot disagree.
- **Dotted and dashed lines do not exist in `LINE_P`.** Draw them: `FOR i FROM a TO b STEP 4 DO PIXON_P(i,y,color); END;`. The one legitimate home of the `STEP` keyword.
- **Nice axis ticks** (Heckbert): step 1/2/5×10^e, decimals `MAX(0,-FLOOR(LOG(stp)))`, start `CEILING(xmin/stp)*stp`.
- **`NiceNum` belongs on interactive step sizes too.** Arrows that add σ/4 give 3.75 on N(100,15); `NiceNum(σ/4)` gives 5. Snap to the grid — `(FLOOR(v/stp + 1e-9) + 1) * stp` — so an odd starting value like 847 is pulled onto 850 rather than carrying its oddness forever.
- **Auto-scale the window, and check BOTH axes before drawing a reference curve.** Horizontal fit is not enough: N(0,1) peaks at 0.3989 and a σ=7 curve at 0.057, so the reference clips flat and reads as a grey artefact box. Suppress what cannot be drawn interpretably — **and say on screen that you have**, or the toggle appears broken.
- **Freeze the window inside a live explorer.** If it tracks μ, the bell sits centred forever and moving the mean looks like nothing happening. Lock on entry, offer a re-centre key.
- **Freeze the x-window, but NOT the y-scale.** σ changes the peak height, so a frozen y-scale either clips a grown curve or leaves a shrunk one floating low. Refit the height on σ changes only — μ does not affect a normal's peak height.
- **Corner readouts collide with plot annotations.** A label at a curve feature lands wherever that feature is; a fixed text block does not move aside, and at 320×240 there is nowhere to slide either. Suppress whichever matters less in that mode.
- **Check vertical gaps when adding a line to an existing text block.** 14 px spacing tolerates one insert; 6 px overlaps.
- Hand-placed layouts: audit box edges against line endpoints numerically, and expect one or two pixel-nudge rounds on device.

## 7 · Waiting for a keypress

**`FREEZE` is not a pause.** It only suppresses the screen refresh when the *program terminates*. Mid-program it does nothing: a result panel followed by `FREEZE` draws and is instantly repainted by the next `CHOOSE`, and the user reports "it goes straight back to the menu."

**`UNTIL k == -1` and `UNTIL k > -1` look alike and do opposite things.** The first drains and falls through instantly; the second blocks. A wait loop written with the wrong one is a silent no-op.

**Drain, wait, drain.** A keypress left behind by `INPUT` or `CHOOSE` satisfies the next wait loop and skips the screen you just drew:

```
REPEAT k := GETKEY; UNTIL k == -1;   // drain stale
REPEAT k := GETKEY; UNTIL k > -1;    // wait for real
REPEAT k := GETKEY; UNTIL k == -1;   // drain that one
```

**The key-help footer must match what the keys actually do.** Live arrows exist only in an explorer; on a result view any key returns. Advertising arrows there invites a press that loses the plot. Drive the footer from a state flag.

**The Terminal can only be scrolled after the program ends.** While a program waits in a `GETKEY` loop, it takes every key, the arrows included, so arrows only move the program on.

- End the program with a `PRINT`. The Terminal then stays open, and Up/Down scroll it (User Guide, PRINT entry).
- Del erases the Terminal, so warn the user.
- Its scroll bar does not respond to touch.

Verified with PyProbe beta 2a, 1 Oct 2026. For output the user must read while the program is still running, draw your own scrolling screen, as PyProbe beta 2b does.

**But a program with nothing to scroll should end with `RETURN`, not `PRINT`.** A trailing `PRINT` leaves the Terminal on screen after Quit, and the user has to press a key to get back to Home — it reads as "the program did not exit cleanly" (Roger, 10 Oct 2026). Return the summary as a string instead (`RETURN "ChiTable: " + ...`): Home shows it in the history and nothing is left open. StatDist and EpiStats already end this way.

**Touch lists from `WAIT(-1)`: check `SIZE` before reading x and y.** `WAIT(-1)` returns a key code, or a list for a touch. The list is `{type, x, y}` for a press (type 0) or a drag (type 1), but a finger LIFT can arrive as a one-element list, and `kk(2)` on that is a runtime error. The error dialog opens the Program Editor at the failing line, and from there the only way back was a reset (StudRange, 10 Oct 2026). The safe shape:

```
kk := WAIT(-1);
IF TYPE(kk) == 6 THEN                 // a touch
  tx := -1; ty := -1;
  IF SIZE(kk) >= 3 THEN
    IF kk(1) == 0 THEN tx := kk(2); ty := kk(3); END;   // a new press only
  END;
  ...hit-test tx, ty; -1 matches nothing...
END;
```

**Give a finger-lift drain a time limit.** `REPEAT UNTIL MOUSE(1) == -1;` waits for the finger to leave the screen. If the touch reading sticks (PrimeSUD measured a phantom touch at (2147483647, 0) after a `GETKEY` landed on a finger lift, on the Python side), that loop never ends and the program is frozen with no way out but a reset. Put the drain in one helper and cap it:

```
csDrain()
BEGIN
  LOCAL drT;
  drT := TICKS;                                  // milliseconds
  REPEAT UNTIL MOUSE(1) == -1 OR TICKS - drT > 1000;
END;
```

`TICKS` (no parentheses) is the millisecond clock; TowerOfHanoi and Solitaire in the library use it the same way. ChiTable beta 1k, CentralLimit beta 1a and NormExplorer beta 40 drain this way. The key-only waits (`UNTIL kk > -1`) in the older programs are not a hang — any key leaves them — so they were left alone.

## 8 · MicroPython: getting it running

**The interpreter is MicroPython 1.9.4** — confirmed by `sys.implementation` on a G2 with the 2026-09-09 firmware. That release's documentation was last updated December 2018 and tracks CPython 3.4. **Check the 1.9.4 docs, not the current ones.** Most of the quirks below follow from this one fact.

**Python arrived in firmware build 2.1.14566, released 2021/04/28** (HP's release notes, "Add Python app").

- It did not arrive in 2.1.14181. That build is dated 2018/10/16 in the same notes, and it has no Python at all, though it is sometimes quoted.
- v3 had the build as 14567 and that date as November 2018. Both are corrected here.

**What is in each module.** PyProbe beta 2, `dir()` on the 2026-09-09 emulator, 1 Oct 2026. `sys.implementation` = micropython (1, 9, 4).

- **Present:** `math`, `cmath`, `urandom`, `hpprime`, `arit`, `linalg`, `matplotl`, `graphic`, `cas`, `gc`.
- **Absent:** `random` and `time`. Also **`os`**: `import os` fails in a `#PYTHON` block. HP's 2.4.2 notes mention `os.read` fixes; perhaps `os` exists only inside the Python app. That is untested.
- **`urandom`:** `random()`, `uniform()`, `randint()`, `randrange()`, `choice()`, `getrandbits()`, `seed()`.
- **`math` extras:**
  - Present: `erf`, `erfc`, `lgamma`, `gamma`, `log2`, `log10`, `expm1`. `erf` gives the normal CDF directly.
  - Missing: `fsum`, `isclose`, `factorial`, `comb`.
- **`linalg`:** `det`, `inv`, `solve`, `rref`, `eig`, `eigenvects`, `transpose`, `mul`, `dot`, `cross`, `fft`, `ifft`, `linspace`, `arange`, `matrix`, `zeros`, `ones`, `eye`, `identity`, and polynomial helpers. That is enough for regression and ANOVA without hand-written matrix code.
- **`graphic`:**
  - Drawing: `draw_line`, `draw_rectangle`, `draw_filled_rectangle`, `draw_circle`, `draw_filled_circle`, `draw_arc`, `draw_filled_arc`, `draw_polygon`, `draw_filled_polygon`, `draw_string`, `draw_pixel`, `fill_rect`, `get_pixel`, `set_pixel`.
  - Screen: `clear_screen`, `show`, `show_screen`.
  - Named colours: black, white, red, green, blue, cyan, magenta, yellow.
  - Argument orders are not yet tested.
- **`cas`:** `caseval`, `eval_expr`, `get_key`, `xcas`.
- **`arit`:** `gcd`, `lcm`, `iegcd`, `ifactor`, `isprime`, `nextprime`, `prevprime`, `nprimes`, `euler`, `asc`, `char`.

**Do not use `matplotl` for teaching charts** (PyProbe beta 2). Every function is accepted, but the module is unusable:

- `clf()` clears nothing.
- Pictures pile up, even across separate `PYTHON()` runs.
- `axis()` has no visible effect, so the Prime picks the window.
- `text()` draws only a small square, never the letters.
- A colour argument is accepted but ignored.
- Everything is blue or black outline.

Only the shapes are right: `histogram` counts in width-1 classes from the minimum, and `barplot` bars are centred at x = 0, 1, 2…. Draw charts yourself, with PPL `_P` commands or with Python's `hpprime` or `graphic`.

The missing `time` is independently confirmed by hp-prime-kit on a different G2, and they give the workaround: build your own on **`eval('ticks()')`**, which returns milliseconds. Worth knowing that `ticks()` exists — it is the only timing source on the Python side.

**`hpprime` has more than `eval`.** In confirmed use:

- `fillrect(gr,x,y,w,h,edge,fill)`, with `gr=0` meaning the screen.
- `keyboard()` for any-key-down.
- `dimgrob(n,w,h,colour)` for an off-screen grob (used to measure text).

Colours are 24-bit `0xRRGGBB` integers.

The full list is now confirmed present (PyProbe): `arc`, `blit`, `circle`, `dimgrob`, `eval`, `fillpoly`, `fillrect`, `get_cartesian`, `getpix`, `grobh`, `grobw`, `invert`, `keyboard`, `line`, `mouse`, `pixon`, `rect`, `set_cartesian`, `strblit`, `strblit2`, `textout`, `ticks`, most with `_c` (Cartesian-coordinate) variants. Their argument orders are not yet verified; test before relying on them. Nearly all have a PPL equivalent reachable through `eval` anyway.

**Two installation routes, and confusing them is the support question.**

*Route A — embedded in a PPL program.* The Python lives in a `#PYTHON name … #END` block with a PPL wrapper `EXPORT f() BEGIN PYTHON(name); END;`. Install like any PPL program: paste the `.txt`, sync. **There is never a separate `.py` file.** It launches from the Program Catalog and the user need never open the Python app. This is the house method and the right answer for anything you hand to someone else.

*Route B — a standalone `.py` in the Python app.* These do **not** appear in the Program Catalog; they live under Apps → Python → Files. People sync a `.py`, look in the Program Catalog, find nothing, and conclude it failed.

**Paste, do not retype.** Indentation survives a paste into the Connectivity Kit; hand entry invites a tab-and-space mismatch that is miserable to find on a small screen.

## 9 · MicroPython: the bridge

**The pattern.** PPL writes named globals, Python reads them with `hpprime.eval`, and writes back by assembling a PPL assignment as text. `eval` also writes and reads PPL globals directly (`ev('CX:=3.5')`, `ev('CX')`) and calls your own PPL functions (`ev('MYFUNC(1.0)')`).

**`PYTHON(name, a, b, …)` passes values in `sys.argv`, but only use it for small whole numbers and plain text.** PyProbe, 1 Oct 2026, emulator.

- Every value arrives as text, and `argv[0]` is the first value; there is no script name in front.
- Numbers arrive formatted as the Home screen would display them:
  - −2.5 came as `'−2.5'`, with U+2212 as the minus sign.
  - 1E20 came as `'1ᴇ20'`, with U+1D07 as the E.
  - 123456789012 came as `'123﹐456﹐789﹐012'`, with U+FE50 digit-group marks.
  - `float()` rejects all three.
- A 200-value list arrived cut off at 214 characters, which was 47 values. All seven arguments together came to 257 characters.
- So pass a test number or a mode this way. Have Python read real numbers and data lists directly from PPL variables with `hpprime.eval`; they arrive as true floats.
- A different Home number format, such as Fixed 2, would presumably change what arrives. That is untested.

**Cost of a crossing: about 0.2 ms.** *(Measured by hp-prime-kit on a G2 at firmware 2.4.15515 — not by us.)* Thirty to forty lookups cost around 8 ms, which is nothing. This **corrects an earlier blanket rule here** that said never to cross inside a loop: that is too strong. The real limit is per-pixel work — 272 columns × 2 crossings a frame is about 109 ms, which a live redraw will feel. So: cross freely for tens of lookups, keep it out of per-pixel loops, and keep a returned payload fixed-size so 5000 draws cost the same as 200.

**A Python exception does not raise a PPL error.** This is the one that matters. The traceback prints to the Terminal and PPL carries straight on with whatever the bridge variable held before; `IFERR` around `PYTHON(...)` catches nothing. If the program has a fallback, the fallback runs, the result is correct, and the only symptom is that it took longer. In this fleet the Python sampler failed on every run **for eleven consecutive builds** with nothing on screen to show it.

**So the guard does three things, all necessary:**

1. **Clear the output variable first**, so no stale value survives a failure.
2. **Validate by USING the result**, not by asking its type — read the last element inside `IFERR`. Testing `TYPE(...) == 6` also works but adds a firmware assumption, and if that were ever wrong the program would silently take the slow path forever.
3. **Always write the pure-PPL fallback.** It is slower, and it is the difference between degrading and failing in front of a class.

**Then report which one ran.** A diagnostics page naming the sampler that actually produced the last result — plus a live probe that runs a trivial call and checks the answer comes back — turns an invisible failure into a visible one. Any bridged program should carry one.

**Three ways a Python app closes with no message at all.** *(All measured by hp-prime-kit on a G2; we have not reproduced them, but they match the silent-failure character of this bridge.)*
- **A PPL list containing a string, returned raw to Python.** A function returning eight numbers and a text warning closes the app — no exception, no trace. Wrap the call in PPL and let only numbers out: `ev('LOCAL zr:=' + call + '; {zr(1),...,zr(8)}')`. The same applies to `MOUSE`, which returns lists inside lists. **Design any PPL function that Python will call to return a flat list of numbers, or one number.**
- **A top-level import of a module MicroPython does not have.** Imports inside a function do not count. Delete `__pycache__` before packaging too — those are CPython files MicroPython cannot read.
- **A quote inside a string you are concatenating into an `eval` expression.** Clean it first: `s = str(s).replace('"', "'")`.

**When an app closes silently, leave marks in a PPL global.** The screen is gone and there is no trace, but a PPL global survives:
```
def mark(t):
    try: ev('PZ:="' + t + '"')
    except Exception: pass
```
Then go to Home and type `PZ` to see how far it got. *(hp-prime-kit's technique; it is how they isolated the list-with-string crash in a single pass, by probing in order of increasing risk.)*

**Do not use `repr()` on floats crossing the bridge.** It can emit exponent notation PPL will not parse. Use `"%.6f" % x`.

**On `join`:** it works on this firmware in every form tested — string literals, `str(int)`, list comprehensions, `%`-formatted floats, `repr(float)`, `str(float)`, a mixed list, a bare generator expression, and a tuple. A real, repeated `join` TypeError *did* occur during development and was cured by switching to concatenation, but it has never reproduced; cause unknown, a stale build left on the calculator being the least unlikely guess. **Keep building hand-off strings by concatenation** — it is free and immune to whatever that was.

**The emulator cannot catch these.** It runs the real ROM, so the language behaves identically — which makes it excellent for syntax and logic and useless for this class of bug. The desktop simply ran the fallback fast enough that nothing looked wrong. Any new Python path gets tested on hardware with the Terminal open.

## 9a · Where the Python knowledge actually lives

HP's own Python documentation is thin, though the 2.4.2 firmware (2026-09-09) substantially improved the built-in Python help: press Help in each Python app view. Four outside sources are worth knowing, in rough order of value:

- **`JordiRigau/hp-prime-kit`** on GitHub — `docs/topics/micropython.md` in particular. Every claim is labelled measured or unverified, and measured ones name the firmware. Also ships a PPL linter, an interpreter, and a `.hpprgm` builder. The best single source found. *Saved copy:* `Community_Library\github\JordiRigau__hp-prime-kit.zip`.
- **Mike Markowski's HP Prime Programming page** (udel.edu/~mm/hp/primePython/) — the `hpprime.eval` bridge, calling `CHOOSE` and `DRAWMENU` from Python, `AVars()` for typed values, touch via `mouse`. *Saved copies:* the HTML pages, with his `upython.html` module inventory and the `hat.py` and `spiro.ppl` examples, are in `Community_Library\docs\markowski_udel\`. Roger's January 2024 printout is `HPPrimeProgrammingUDelaware.pdf` (in the Project and in `D:\HP-Prime`); its text layer is garbled, so read the HTML copy instead.
- **Neil Streeter's HP Prime Python Activities** (hpcalc literature, June 2025) — HP-adjacent introduction, the `#PYTHON` wrapper, writing in VS Code and pasting. *Saved copy:* `Community_Library\docs\hpprime-python-activities.pdf` (22 pages).
- **Cemetech and the HP Museum forums** — scattered, but where the version information and most failure reports surface.

Note that hp-prime-kit lists the PPL→Python direction (`PYTHON(name)` with `#PYTHON … #END`, our Route A) as **unverified — "here to put the door on record rather than because it was tried."** That is the direction this fleet has shipped three programs on. If anything here gets published, that is the gap worth filling.

## 10 · Reaching the built-in apps

**Data columns are global and reachable.** `D1` (Statistics 1Var) and `C1`, `C2` (Statistics 2Var) can be read and written from a standalone program. Wrap the first read in `IFERR` — the variable does not exist until the app has been opened once. Writing works too: `D2 := MAKELIST(...)` puts results where every other app can reach them. `STARTAPP("Statistics 1Var")` then launches the app with the data in place.

**App settings are not reachable.** `H1Type` and `SetSample` are Statistics 1Var app variables. Referencing either from a standalone program is a **syntax error at paste time** — not a runtime error, so `IFERR` cannot help. The User Guide documents qualifying as `Function.Xmin`; both `Statistics1Var.H1Type` and `Statistics 1Var.H1Type` were tried on a G2 at 2026-09-09 and both error.

The confusing part: HP's own DiceSimulation example uses `SetSample` and `H1Type` freely — but that example *is* a Statistics-derived app, where those names are in scope.

**So: data is reachable, configuration is not.** Instruct the user for the rest, or write your program *as* a customised app.

**`VIEW "name", Func()`** registers a function in the Prime's own Views menu (Shift-View), which HP's apps use and custom programs rarely do.

## 11 · Numerical methods

- **Normal sampling: Marsaglia polar.** No trig, so it is immune to angle mode.
- **Substitute to cluster quadrature nodes where the mass is.** StudRange's outer integral over s = √(χ²ᵥ/v) is sharply peaked at low v; the 1977 original excluded low df for exactly this reason. Substituting s = u² (Jacobian 2u) fixes it: k=4, v=3, α=.005 returns 15.4499 against a true 15.4503, where the unsubstituted version was 0.34 off.
- **Secant beats bisection when each evaluation is expensive.** 60 bisection steps versus ~9 secant iterations, with a warm start worth the two lines it costs.
- **The computational variance formula is acceptable here, with a guard.** Accumulating Σx and Σx² keeps the bridge payload fixed-size, and it agrees with a two-pass calculation to 14 decimal places at classroom scales. Wrap it in `MAX(0, ...)` before the square root — cancellation driving the result slightly negative is the one failure mode that matters.
- **Guard moment existence** (Burr XII: mean needs K·C>1, variance K·C>2). "No mean" is a teaching feature.
- Verify every formula against SciPy before it goes near the calculator.

## 12 · Statistical wording

- **μ and σ are correct when the program computes from a DECLARED distribution.** Entering N(100,15) declares a population, and every `NORMALD_CDF` result is an exact area under it. x̄ and s belong only where a sample is actually summarised — switching to them in a distribution explorer introduces the error rather than fixing it.
- **"Confidence level" is wrong for a central probability interval.** The middle 95% of N(μ,σ) is where a single observation falls 95% of the time; a confidence interval is built from a sample to estimate a parameter and uses a standard error, not σ. Both give ±1.96, which is exactly why students merge them. Say "central proportion."
- **Cohen's d from two real groups uses the pooled s.** That is both the standard denominator and the only thing a one-σ plot can honestly draw — say so rather than letting the reader assume the statistics were chosen to suit the graphics.
- Showing a sample's own x̄ and s beside the μ and σ that generated it is the cheapest sampling-variability lesson available: they differ on every draw.

## 13 · House style

Blue `RGB(0,60,200)` the distribution curve · Magenta `RGB(200,0,200)` derived quantities (CDF, posteriors, odds) · Red `RGB(255,0,0)` "you are here" markers, T− cells · Green `RGB(0,140,60)` T+/detected, mean marker; help lines `RGB(0,128,0)` · Orange `RGB(255,69,0)` frames, panels, totals · Dodger blue `RGB(30,144,255)` LR lines, footers · Gray `RGB(90,90,90)` tick labels · Grid `RGB(225,228,235)` · Shade fill `RGB(170,205,255)`. Light fills: green `232,246,235`, red `255,235,235`, blue `235,242,255`, orange `255,240,220`.

Panels: coloured border, light fill, matching text. Legends comma-separated — `⇆ = C, ⇅ = K, +/- = x₀, Ent = menu, Esc = quit`.

**Distribution terms.** Programs go out as `.txt` with a header block carrying the author, year, AI-assistance note, licence — free for educational and personal use, keep the header, credit the author, not for sale — and the firmware tested on. Guides carry the same paragraph after their Credit section.

## 14 · Working rules

1. **Verify before delivering.** Formulas against SciPy; layouts audited numerically; structure balance, reserved words, builtin-name parameters, `LOCAL` sizes, `INPUT` counts, `CHOOSE` arguments — all checked programmatically.
2. **Never guess Prime specifics.** This file, then the corpus, then the reference PDFs, then the web. The device's CMDS and Chars menus are ground truth.
3. **Test before theorising.** When a value appears from nowhere, ask for the observed value of the suspect variable *before* proposing a mechanism. A confident wrong diagnosis (a stale CAS `x`) cost several exchanges and sent Roger to `purge(x)` for nothing; the one-line check should have come first.
4. **Ask how it was installed before theorising about the code.** A duplicate paste into the Connectivity Kit gives duplicate `EXPORT` declarations and an error deep in the file, which looks exactly like a firmware or capacity limit. Environment before code.
5. **Never parse PPL block structure by counting `END;`.** `IF`, `FOR`, `WHILE`, `CASE` and function bodies all close with the same token, so a depth counter terminates at the first inner `IF`. A rename script built this way silently mangled a working file. Track the opening keyword; regenerate rather than patch. Identifier rewrites must also skip string literals, or `"x = "` gets renamed along with `x`.
6. **Sweep every reference when something is renamed.** Menu numbers, key assignments and variable names appear in more places than the obvious one — two menu numbers in a user's guide stayed wrong for several builds after a swap.
7. **Version the filename with every update**, for programs and documents alike, Lessons Learned included (v5 → v6).
   - When unsure of the next number, add a letter: beta14 → beta14a.
   - Always work from the most recent version.
   - **Archive** stale copies: move them to a `_superseded…` folder rather than deleting them, so there is never ambiguity about which file is current.
   - The exceptions are files whose names tools depend on, such as `CLAUDE.md` and `INDEX.md`. Those are edited in place.
8. **An outside code review is worth having, but not worth pasting.** A reviewer with only the source text can spot real problems — two genuine per-frame costs were found this way, both verified against the file. But a full-file rewrite produced without the actual file silently drops things: one such rewrite omitted a `LOCAL` declaration that existed in the original, introduced a lowercase exponent literal, and downgraded 81 working Greek glyphs to ASCII on a speculative "paste fidelity" argument against device evidence. **Take the findings, implement them on the verified file.**
9. **Record disproved theories AS disproved.** A note that reads like a diagnosed cause will send the next session down the same dead end. Two confident explanations of the `join` failure were tested and failed; both are now labelled.
10. **When Roger pastes his edited version, sync to his edits first.** His device copy is the source of truth.
11. **Search the whole library, every time.** It persists, and all of it is reachable:
    - the 83 `.txt` programs uploaded to the Project;
    - on Roger's computer (Rogers-HP), `D:\HP-Prime`: the fleet, about 940 zips (mostly hpcalc.org) at the top level, and `Community_Library`. That folder holds hpcalc, GitHub and cnCalc material plus docs; its `INDEX.md` lists everything.

    Reach it through the link to his computer, or a Claude Code session on Rogers-HP. Search it with `libsearch_v1.py` (the index, `Library_Index.db`, covers all of `D:\HP-Prime`; refresh it with `library_index_build_v1.py` after adding files). For anything the index cannot answer, read archives in place with Python's `zipfile` rather than uploading them. (This corrects v3, which said the corpus zips do not persist between sessions.)
12. **Check the whole fleet for duplicate routine names before every paste** (`python3 fleet_names_v1.py *.txt` in `D:\HP-Prime`), as well as the single-file checks (`ppl_check_v2.py`, `lint_ppl.py`). One program is never the whole picture on a calculator that pools every program's routines (§5).

## 15 · Current fleet

| Program | State |
| --- | --- |
| **Norm Explorer beta 40** | Menu-first normal workbench: auto-scaling window for any μ and σ, four probability directions, inverse calculations, z-formula solver, touch input, data module reading D1 / C1 / C2, simulated sampling, Cohen's d, standardize animation, diagnostics page. Guide written. Data module emulator-tested only. Beta 40 = beta 39a with every helper tagged `ne_` and a capped finger-lift drain; not yet re-run on hardware. |
| **StudRange beta 13** | Studentized range in PPL: p-value, critical value, Tukey HSD, interactive plot with α ladder; tap or drag the plot to move q (touch emulator-tested only). df ≥ 3. Beta 13 = beta 12a with every helper tagged `sr_` and a `SIZE` check on the touch list; not yet re-run on hardware. |
| **StudRangePy beta 14b** | The MicroPython twin. Handles df ≥ 1, far faster on critical values, static plot. |
| **EpiStats v1.3** | Seven-module epi suite. *Pending: M-H confidence intervals, Breslow-Day.* |
| **FEP v1.3** | Fisher exact plus chi-square, corrected p-values. |
| *EpiStats v1.3, FEP v1.3, ConTable2 v1.2, StatDist v2.4, SampDist v2.1, Burr3 v2.2, Norm3 v2.2, PowerViz v2.2* | Each is the previous version with every helper routine tagged (`es_`, `fe_`, `ct_`, `st_`, `sd_`, `b3_`, `n3_`, `pv_`) and nothing else changed (10 Oct 2026); none re-run on hardware yet. FDAES v3.4 (`fdPct`) and StudRangePy beta 14b (no helpers) needed no change. |
| **ConTable2 v1.2** | Contingency battery, row-based RR/RD, Haldane-Anscombe, McNemar. |
| **StatDist v2.4** | 17 distributions live, 10 stubbed. |
| **SampDist v2.1** | Sampling-distribution explorer. |
| **Burr3 / Norm3 v2.2** | Parameter explorers with CDF overlay and mean marker. |
| **BayesTree beta 5** | Natural-frequency tree, ROC view, PPV-vs-prevalence, 2×2 view. Beta 5 = beta 4 with every helper tagged `bt_` and a `SIZE`/type check on the tap list; not yet re-run on hardware. *Pending: sequential evidence, Fagan nomogram.* |
| **ChiTable beta 1k** | Chi-square for a 2 x 2, 2 x 3 or 3 x 2 table (PPL): touch-grid entry, expected counts, row/column %, X2/df/p/critical value, G2, V, adjusted residuals, interpretation page, 2 x 2 extras (Yates, Fisher, z, RD, RR, OR), bar, mosaic and chi-square-curve plots. Was ChiSquare beta 1/1a — renamed because `ChiSquare` is `CHISQUARE`. Tested on the G2 and the G1 (10 Oct 2026): entry grid with soft keys, Values form, results pages, all three plots. Beta 1k adds the capped `csDrain()` and returns the summary instead of printing it; not yet re-run on hardware. |
| **CentralLimit beta 1a** | Central Limit Theorem explorer, built as an APP on Statistics 1Var (after Colin Croft's HP 39G aplet); its program is pasted into the app's own program, not the catalog. Beta 1a adds the capped `cltDrain()`. Awaiting a device test. |
| **GaltonBoard beta 1a** | Galton's quincunx: animated balls through R rows of pegs, bins build a Binomial(R, p) histogram with binomial and normal overlays; tap the pegs to drop a ball, tap a bar for its numbers; bins to D1/D2. Beta 1a: capped `gbDrain()`, `RETURN` instead of `PRINT`. Untested on hardware. |
| **TrendTest beta 1a** | Chi-square for linear trend in a 2 × k table (Mantel, 1 df), Pearson's chi-square and the departure from linearity; Wilson intervals, odds ratios with Woolf intervals; two plots. Checked against SciPy/statsmodels on 300 tables. Beta 1a: capped `trDrain()`, `RETURN` instead of `PRINT`. Untested on hardware. |
| **TestChooser beta 1a** | "Which statistical test?" — two tapped questions (scale, design) lead to a test page: what it compares, assumes, where it is on the Prime, what follows, and the fallback; browse the whole table by tapping. After Glantz. Beta 1a: capped `tcDrain()`. Untested on hardware. |
| **DNAMixLR beta 1** | Likelihood ratio for a DNA mixture, locus by locus, with the NRC II coancestry (θ) correction (Weir et al. 1997; Curran et al. 1999); preset or custom hypotheses, up to 12 loci, ENFSI verbal scale, LR-by-locus and LR-against-θ plots. Engine checked against brute-force enumeration (400 cases). Teaching tool only. Untested on hardware. |
| **PyProbe beta 2b / PyDirect beta 1** | MicroPython probes: argv, matplotl, module inventory. Beta 2b shows its output on its own scrolling screen. PyDirect tests the direct-call `#PYTHON name(args)` form. |
| **PyVer / JoinTest / GenTest** | Throwaway diagnostics. `PyVer` reports interpreter version and module list. |

*Shelved: a three-level Bayes tree for desktop — R/Shiny favoured for the classroom.*

---

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
