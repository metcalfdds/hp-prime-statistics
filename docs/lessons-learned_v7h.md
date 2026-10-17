# HP Prime Lessons Learned
*Roger Metcalf & Claude · v7h · 17 October 2026 (v7g 16 October 2026, evening; v7f 16 October 2026; v7e 12 October 2026; v7d 11 October 2026; v7c, v7b, v7a and v7 on 10 October 2026; v6 6 October 2026; v5 3 October 2026; v4 1 October 2026; v3 rewritten 28 September 2026)*

**What changed in v7h** (the first run on the Prime's firmware: the HP Prime Virtual Calculator 2.4.2, build 2026-09-09, 17 Oct 2026; Emulator_Round1_Results_2026-10-17_v1.md has every observation):

- **The CAS call form was wrong, and the right one is known** (§9b). `CAS(s)` with `s` a string *variable* hands the text back **unevaluated**. The fleet's `xxCas` therefore returned its own input, and ErrorRate beta 1's "Why 3" page showed its question as the answer, badged "exact (CAS)". The form that works is `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))`, then drop the quotes (CASProbe beta 1b: 42 pass, 8 fail, 19 values). All twelve CAS programs carry it now (BRIEF_CAS_v2), and ErrorRate beta 1a shows a real `ln(20)` on the emulator.
- **The Prime prints CAS answers its own way** (§9b, new table): `e^(…)` for exp, `√` for sqrt, braces from `solve`, `∞` and `±∞`. Never parse for `exp(`, `sqrt(` or `list[`; check by value. **CAS variables persist** into the student's CAS until `purge`.
- **Soft keys under `WAIT(-1)`** (§7). A tap on the DRAWMENU strip reaches `WAIT(-1)` **only** as `{3, x, y}`, a click with no press and no lift (MenuTapProbe beta 1; WaitLab's 2014 note holds on 2026-09-09). BayesTree and StudRange looked for a type-0 press there and their soft keys did nothing. Read a strip tap from type 3 with y ≥ 218, and ignore type 3 above the strip, because a screen tap sends 0, 2 and then 3. `GETKEY` + `MOUSE` polling (ChiTable's pattern) sees strip taps as before.
- **Chi-square and F reject a fractional df** (§3). `CHISQUARE_CDF`, `CHISQUARE_ICDF`, `FISHER_CDF` and `FISHER_ICDF` raise "Invalid input" for df = 2.5. The densities `CHISQUARE` and `STUDENT`, and `STUDENT_CDF` / `STUDENT_ICDF`, take any df (Welch is safe). `POISSON_CDF(λ, k < 0)` raises too. StatDist v2.6 stopped on a chi-square df of 2.5.
- **ARC_P discs have holes** (§6). Concentric `ARC_P` rings at r = 3, 2, 1 plus the centre pixel leave the diagonals white (GfxProbe T09), so GaltonBoard's pegs and balls looked like ⊕. Use `FILLPOLY_P`.
- **GfxProbe's answers** (§6 table, §3): `FILLPOLY_P` (both list forms, with alpha), `TRIANGLE_P` (one colour, a three-colour blend, alpha), the ten-argument scaled `BLIT_P`, `MAX`/`SORT` on a list and a LOCAL `MAKELIST` counter (Home's K untouched) all work. MSGBOX shows 5 lines. All nine glyph lines render. `WAIT(−1)` types 0, 1, 2, 3 and 7 arrive as the manual says; their numbers are integers, which `STRING()` prints in hex. `BINOMIAL` takes (n, p, k) only. The 3-D `TRIANGLE_P` mesh drew nothing with our arguments.
- **`LOCAL name(args)` is a legal routine head** (§5; LocalHeadProbe).
- **Testing on the Virtual Calculator** (new §16): what it can and can't settle, and how to drive it.

**What changed in v7g** (the touch and graphics versions, the "More" key, and the CAS let in behind a fence; 16 Oct 2026, evening):

- **The CAS is allowed in fleet programs, behind a fence** (§1, new §9b). Roger, 21:15: "yes, change the rule". The old rule ("CAS only for genuinely symbolic work … keep each program on one side of the fence") stands for the *engine* of a program; the CAS may now add exact and symbolic *answers* — fractions, huge integers, closed forms, derivations, limits — through one call routine per program, on events only, with a decimal fallback and a badge. **Nothing about the CAS has run on our calculators**; CASProbe beta 1 settles the call form, the text it hands back, its error behaviour and its G1 speed.
- **The "More" soft key** (§13). When a screen needs more than six soft-key actions, slot 6 reads "More" on every page and steps to the next page of labels, wrapping to page 1 — the HP 48's NXT key (NEXT on the HP-28) in software (Roger, 16 Oct 2026). A screen whose actions fit in six gets no "More". Used by StatDist v2.6 (plot), BayesTree beta 7 (three pages) and NormExplorer beta 42 (page 2 chooses what the arrows move); the TouchKit template v2 carries the shape.
- **The PC run harness** (§14 rule 15): `ppl_run_v2.py` copies a list or matrix on assignment, as the calculator does (v1 shared the Python list, which could hide or invent aliasing bugs), and accepts a bare `RANDOM`; `ppl_run_v3.py` answers `CAS("...")` with desktop **Giac** — the engine inside the Prime's CAS — so a program's CAS text is tested end to end, and `cas='fail'` tests the fallback.
- **The touch and graphics versions** (§15) — nineteen programs and three new ones (ScatterLab, BiNorm3D, CICatcher), each gated and run in the harness against SciPy/statsmodels; none on hardware yet. ConTable2 and FEP are retired: EpiStats v1.6 module 1 and `EpiStats2x2(a,b,c,d)` replace them.
- **`CHOOSE`'s simple form takes 14 items** (§2, unchanged) — EpiStats v1.6's help menu sits exactly at it; BayesTree, ChiTable, StatDist, GaltonBoard and NormExplorer use the list form for their longer menus.

**What changed in v7f** (the fleet review of 16 October 2026 and the fix versions it produced; two new rules, one checker fix, one probe):

- **A fleet review** (`Fleet_Review_2026-10-16_v1.md`) read all nineteen programs against this file. The fix versions listed in §15 clear its section 2 (runtime errors, wrong numbers, output cut off by MSGBOX, missing drains) and section 3 (the sweeps). None of them has run on hardware yet; every one carries a device-test checklist in its `_CHANGES.md`.
- **`fleet_names_v2.py` requires each helper to carry ITS OWN FILE's tag** (§5). v1 accepted any two-to-four-character prefix as a tag, so StatDist's ten `calc_*` stubs passed as tagged and v7d's "0 untagged" was a false pass. v2 also reports a file that mixes two tags.
- **The MOUSE and WAIT(-1) type tables are different tables** (§7). In a `MOUSE` list the type is 0 New · 1 Completed · 2 Drag · 3 Stretch · 4 Rotate · 5 LongClick; in a `WAIT(-1)` list it is 0 Down · 1 Move · 2 Up · 3 Click · 5 Stretch · 6 Rotate · 7 Long click. Drag is 2 in one and 1 in the other. A handler must say which call it is reading.
- **A GETKEY drain does not drain touch** (§7). BayesTree's node page bracketed `WAIT(-1)` with key drains; the finger lift that opened the page could close it. The capped `MOUSE(1) == -1` drain goes before any wait that touch can satisfy.
- **`WAIT(-1)` gives up after about a minute** and returns −1 (Commands reference). It is the wrong hold for a page that must stay up through a lecture; `xxWaitAny()` is the right one.
- **`ans` is `Ans`** (§5): the lint found it in GfxProbe before the paste did. `K` used as the `MAKELIST` counter writes Home's K on every call. A LOCAL counter appears in 51 corpus programs, almost always with a constant expression; whether the expression can USE a LOCAL counter is untested, so **keep `K` until GfxProbe T19 passes**, then sweep. `G1`…`G6` are the graphics variables — do not use them as LOCAL names even in lowercase.
- **Self-numbered menus were in seven programs, not six** (TrendTest had been missed); all seven are fixed in the versions below. Version strings, companion-file names and file maps inside a program are references too and go stale with every rename — seven were stale.
- **What the Prime can draw that the fleet never used** (§6, new table): translucent `FILLPOLY_P`, blended and translucent `TRIANGLE_P`, the 3-D `TRIANGLE_P` mesh, the ten-argument scaled `BLIT_P`, a second finger in `MOUSE`, the `WAIT(-1)` gesture events. Documented and corpus-used, none verified by us. **GfxProbe beta 1** tests each one and writes the answers to `GP_LOG`; §6's table says what to fill in from it. Until then no fleet program uses them.
- **Open questions that GfxProbe also settles**: how many lines a MSGBOX shows (T13), whether `CHISQUARE_CDF` and `FISHER_CDF` take non-integer df (T11, the door to Gamma and Beta in StatDist), what `POISSON_CDF(λ, −1)` returns (T12), nine unverified glyphs (T14), and whether keys survive `WAIT(0.02)` (T15). A ten-line **LocalHeadProbe** settles whether PowerViz's `LOCAL pv_Name()` routine heads are legal.
- **The canonical footer** is CentralLimit's form (§13): comma-separated, spaces round `=`, dodger blue. Four other forms were in use.
- §8: a `from random import …` guard is a guaranteed fallback on this firmware, not a precaution — `random` is absent, `urandom` present. The `hpprime` drawing argument orders StudRangePy uses ran on the G2 and are recorded as observed.
- §14: rules 13 and 14 (version strings are references; the gate before any paste, `ppl_gate_v1.py`, with `ppl_check_v3.py`).

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

**Verified on:** HP Prime G2 and G1, both running the **2026-09-09** firmware, plus the desktop Virtual Calculator (2.4.2, the same build; the whole fleet ran there on 16–17 Oct 2026, §16). Firmware matters more than it looks: glyph rendering and app-variable reachability have both proved version-dependent, so a "device-verified" claim is only verified on a stated build.

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

**The CAS for exact and symbolic answers, behind a fence** (v7g; Roger, 16 Oct 2026). A program's *engine* stays PPL (or Python) numerics, derived and verified off-device against SciPy. The CAS may add what only it can: exact fractions, integers of any size, closed forms, a derivation done live on the student's numbers, a limit. It is reached through ONE call routine per program, only on events, with the decimal answer as the fallback (§9b). Home capitals A–Z are built-in global reals; CAS lowercase names are symbolic; case matters.

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
- **`MSGBOX` shows 5 lines.** A 6th line was lost (PyProbe beta 1, 1 Oct 2026); ten lines showed lines 1–5 (GfxProbe T13, emulator, 17 Oct 2026). Keep message boxes to 5 lines; put longer output on a screen of your own.
- **Whole-number df only, for chi-square and F CDFs and quantiles** (GfxProbe T11 and Home checks, emulator, 17 Oct 2026). `CHISQUARE_CDF(2.5, 3)`, `CHISQUARE_ICDF(2.5, 0.5)`, `FISHER_CDF(2.5, 7.5, 2)` and `FISHER_ICDF(2.5, 7.5, 0.5)` are "Invalid input". The densities `CHISQUARE(2.5, 1)` (0.281348225763) and `STUDENT(2.5, 1)` take any df, and so do `STUDENT_CDF(2.5, 1)` (0.797969486361) and `STUDENT_ICDF(2.5, 0.9)` (1.7302509288); all match SciPy to 12 digits. For a fractional chi-square or F df use your own incomplete gamma or beta (StatDist v2.7b's `st_gammaP` / `st_betaI`).
- **`POISSON_CDF(λ, k)` with k < 0 is "Invalid input"** (T12), not 0. Guard the lower bound of a "between" sum.
- **`BINOMIAL` and `BINOMIAL_CDF` take (n, p, k) only** (GfxProbe T20, CASProbe T42): `BINOMIAL(10, 0.3, 2)` = 0.233474 = SciPy; (n, k, p) is an error. HP's Commands.pdf prints (n, k, p); it is wrong for this firmware.
- **Also confirmed on the emulator, 17 Oct 2026:** `MAX` and `SORT` on a list (T10); `MAKELIST` with a LOCAL counter, in both the constant and the counter-reading forms, leaving Home's `K` untouched (T19); `TICKS` (a `WAIT(0.1)` read 107 ms, T18); `IFTE`; a `LOCAL name(args)` routine head (LocalHeadProbe).

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
- **`ans` is `Ans`, `ci` is `Ci` (the cosine integral), `G1`…`G6` are the graphics variables.** All three were caught by the checkers in October 2026 before a paste; the first two are the case-insensitive rule above biting on ordinary English words, the third would shadow a GROB. Run `ppl_check_v3.py` (or the whole gate, `ppl_gate_v1.py`) on every file; it reads `HP_Prime_Builtin_Names.txt`.
- **`K` as the `MAKELIST` counter writes Home's K** on every call (ChiTable, GaltonBoard, CentralLimit, DNAMixLR, NormExplorer). A LOCAL counter (`MAKELIST(0, ib, 1, n)`) appears 162 times in 51 corpus programs, nearly always with a constant expression; the fleet also writes `MAKELIST(K*0.5, K, …)`, where the expression reads the counter. GfxProbe T19 (emulator, 17 Oct 2026) showed a LOCAL counter works in both forms and leaves Home's K alone: **new code uses a LOCAL counter**; the older programs' `K` is harmless and changes only when a program is touched for another reason.
- **Non-`EXPORT` does not make a helper private.** Device-found 10 Oct 2026: all programs' routines live in one pool, matched ignoring case, so StudRange's `NiceNum` and Burr3's `NiceNum` were the same name to the calculator, and a call from one program ran the other's code (a runtime error, the Program Editor opening on the other program, a reset). **Every non-`EXPORT` routine carries the program's tag**: `sr_NiceNum`, `b3_fmtp`, `es_Module_Table2x2`, or the glued style `csGrid`, `cltSample`. Before any paste, run `python3 fleet_names_v2.py *.txt` in `D:\HP-Prime`: it lists every routine name defined in more than one program (COLLISION), every helper that does not carry its own file's tag (UNTAGGED), any file mixing two tags (MIXEDTAG) and every name that matches a built-in when case is ignored. (v1 accepted any short prefix as a tag and passed StatDist's `calc_*` stubs; v2 works out each file's tag from its helpers.) The app hooks `START`, `Plot`, `Symb`, `Num`, `Reset`, `Info` keep their fixed names.

## 6 · Graphics

- Screen is 320×240, origin top-left, y increases **down**. The y-flip: `py := BOT - IP(y/ymax*H)`, then clamp.
- **Compose off-screen and blit once.** `DIMGROB_P(G1,...)`, draw every pass to `G1`, then one `BLIT_P(G0,0,0,G1)`. Drawing straight to `G0` tears visibly. Miss one `G1` argument and that element flickers alone — a useful diagnostic.
- **Shading must iterate pixel columns**, not math samples. Sample loops leave white gap columns; this bit two programs before the rule stuck. Iterate pixels, solve for x.
- **Cache the density — for EVERY curve, not just the first.** If three passes need the same pdf, evaluate it once per pixel column into a list. The trap is doing this for the main curve and forgetting the comparison curve: a second curve read by both an overlap fill and a trace costs two `NORMALD` calls per pixel per frame — 544 on a 272-pixel plot, on top of the main curve's 273. That is the one per-frame cost a G1 can actually feel during a live drag.
- **Precompute anything needed twice in the same frame.** Histogram bar heights were computed once to widen the y-scale and again to draw. Build the array first, then use it in both places.
- **Verified GETKEY codes, the only ones to trust:** Esc=4, Left=7, Right=8, Up=2, Down=12, Enter=30, +=50, −=45, 0=42. Route anything else through Enter → `CHOOSE`.
- **Soft keys, device-verified (ChiTable, G2 and G1, 10 Oct 2026):** compose the frame in `G1`, `BLIT_P(G0, 0, 0, G1)`, then `DRAWMENU({"Edit", "Values", "Clear", "", "Cancel", "Run"})` — it paints the screen, so it goes after the blit and is repeated every frame. A tap with `y >= 218` is a soft key; the slot is `MIN(6, IP(x / 53.4) + 1)` (CHOOSE_R's and LibMenu's geometry). The labels never produce a `GETKEY` code, so keep hardware keys as shortcuts for keyboard-only use. **This is for a `GETKEY` + `MOUSE` polling loop.** Under `WAIT(-1)` a strip tap arrives only as a type-3 click (§7).
- **Touch works alongside keys.** Poll both: `REPEAT exK := GETKEY; exM := MOUSE; UNTIL exK > -1 OR SIZE(exM(1)) > 0;`. `m(1)` is the first finger; elements 1 and 2 are x and y. Put the plot box coordinates in shared constants so the touch handler and the drawing code cannot disagree.
- **`BLIT_P(G0, G1)` with two arguments** copies the whole GROB; StudRange used it through beta 11 on hardware. The four-argument `BLIT_P(G0, 0, 0, G1)` is the fleet idiom; both work.
- **Dotted and dashed lines do not exist in `LINE_P`.** Draw them: `FOR i FROM a TO b STEP 4 DO PIXON_P(i,y,color); END;`. The one legitimate home of the `STEP` keyword.
- **`ARC_P` rings do not make a solid disc.** Concentric rings at r = 3, 2, 1 plus the centre pixel leave the diagonals white; each dot reads as ⊕ (GfxProbe T09, emulator, 17 Oct 2026; GaltonBoard's pegs and balls). Draw a small disc as overlapping `RECT_P` bars (GaltonBoard beta 3b: three bars for r = 3, two for r = 2, pixel-exact) or one `FILLPOLY_P` polygon.
- **Nice axis ticks** (Heckbert): step 1/2/5×10^e, decimals `MAX(0,-FLOOR(LOG(stp)))`, start `CEILING(xmin/stp)*stp`.
- **`NiceNum` belongs on interactive step sizes too.** Arrows that add σ/4 give 3.75 on N(100,15); `NiceNum(σ/4)` gives 5. Snap to the grid — `(FLOOR(v/stp + 1e-9) + 1) * stp` — so an odd starting value like 847 is pulled onto 850 rather than carrying its oddness forever.
- **Auto-scale the window, and check BOTH axes before drawing a reference curve.** Horizontal fit is not enough: N(0,1) peaks at 0.3989 and a σ=7 curve at 0.057, so the reference clips flat and reads as a grey artefact box. Suppress what cannot be drawn interpretably — **and say on screen that you have**, or the toggle appears broken.
- **Freeze the window inside a live explorer.** If it tracks μ, the bell sits centred forever and moving the mean looks like nothing happening. Lock on entry, offer a re-centre key.
- **Freeze the x-window, but NOT the y-scale.** σ changes the peak height, so a frozen y-scale either clips a grown curve or leaves a shrunk one floating low. Refit the height on σ changes only — μ does not affect a normal's peak height.
- **Corner readouts collide with plot annotations.** A label at a curve feature lands wherever that feature is; a fixed text block does not move aside, and at 320×240 there is nowhere to slide either. Suppress whichever matters less in that mode.
- **Check vertical gaps when adding a line to an existing text block.** 14 px spacing tolerates one insert; 6 px overlaps.
- Hand-placed layouts: audit box edges against line endpoints numerically, and expect one or two pixel-nudge rounds on device.


**Documented and corpus-used; the Status column is GfxProbe beta 1 on the Virtual Calculator, 17 Oct 2026** (the same firmware as the calculators; a held key and two fingers need the hardware).

| Capability | Call | Documented behaviour | Corpus | Status |
| --- | --- | --- | --- | --- |
| Translucent fills | `FILLPOLY_P([G], {{x,y},…}, color, alpha)`, alpha 0–255; a flat `{x1,y1,x2,y2,…}` list also appears in two programs | fills a polygon with transparency | 91 files | **works**, both list forms, alpha 110 (T01–T03) |
| Translucent / gradient triangles | `TRIANGLE_P([G], x1,y1,x2,y2,x3,y3, c1,[c2,c3],[alpha])` | three colours blend between the vertices; alpha | 90 files | **works**: one colour, a smooth three-colour blend, alpha 128 (T04–T06) |
| 3-D surfaces | `TRIANGLE_P([G], points, triangles, {rotmat or −1, "N", eye or −1, {xmin…zmax}}, [zstring])`, points a matrix `[x y z colour]`, triangles a matrix of point indices; `TRIANGLE_P(G)` returns the z-buffer string | a whole mesh in one call with rotation, perspective and depth clipping | Advanced Graph 3D, 3ddrawing | **drew nothing** with our control list (T07); unresolved, unused (BiNorm3D draws with LINE_P) |
| Zoom by copying | `BLIT_P(G0, dx1,dy1,dx2,dy2, G1, sx1,sy1,sx2,sy2)` | stretches the source rectangle into the target rectangle | 180 files | **works**, exactly 2× (T08) |
| Two fingers | `MOUSE` → `{ {x,y,x0,y0,type}, {x,y,x0,y0,type} }`, one list per finger, empty when up | non-blocking | 427 files | `MOUSE` returns 2 lists (T16); the second finger needs hardware |
| Gesture events | `WAIT(-1)` → `{type, x, y, [dx, dy]}` | 0 Down · 1 Move · 2 Up (no x,y) · 3 Click · 5 Stretch · 6 Rotate (angles in 1/32 circle) · 7 Long click (1 s) | WaitLab (hpcalc) | **0, 1, 2, 3 and 7 seen** (T17); 2 is `{2}`; values are integers. 5 and 6 need two fingers |

WaitLab's observed sequences (firmware 5447/6030, 2014; **the strip and tap sequences re-confirmed on 2026-09-09 by MenuTapProbe, 17 Oct 2026**): a tap on the menu strip (y ≥ 219) arrives as `{3,x,y}` only; a tap elsewhere as `{0,x,y} {2} {3,x,y}`; a drag as `{0,x0,y0} {1,x1,y1}… {2}`; a long touch inserts `{7,x,y}` after the press; a flick ends `{1,65535,y}`; a stretch is `{0,a} {0,b} {5,…,dx,dy}… {2}`; a rotate `{0,a} {0,b} {6,angles…} {2}`.

What these unlock once probed: a shaded region as one translucent polygon instead of 272 vertical `LINE_P` fills (and α/β/power regions that visibly overlap), a bivariate normal surface rotated with a finger, pinch-to-zoom on any plot, long-press as "what is this?", a two-finger spread to set an interval width on the axis.

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

**Soft keys under `WAIT(-1)` arrive as type 3, and only as type 3** (MenuTapProbe beta 1, emulator, 17 Oct 2026). With `DRAWMENU` on screen, a tap on the strip gives one event, `{3, 78, 230}`: no press and no lift. A tap above the strip gives `{0, x, y}`, `{2}`, `{3, x, y}`. BayesTree beta 7 and StudRange beta 15 read the strip from a type-0 press, so their soft keys did nothing. The shape (BayesTree beta 8b):

```
IF kk(1) == 3 AND SIZE(kk) >= 3 THEN
  IF kk(3) >= 218 THEN slot := MIN(6, IP(kk(2)/53.4) + 1); ... END;   // a soft key
  // type 3 above the strip is the tail of a press already handled: ignore it
END;
```

When a view closes on a type-0 press, that tap's `{2}` and `{3}` are still queued for the next `WAIT(-1)` loop. If the tap was on the footer, the next loop sees a soft-key click. Remember the closing tap and skip one matching type 3 (BayesTree 8b's `btTL…`, StudRange 15a's `srTL…`).

**`WAIT(-1)` hands back integers.** `STRING()` prints them in hex (`#3C:-16h` for 60). Arithmetic and comparisons are unaffected; add `0.0` before printing.

**A GETKEY drain does not drain touch, and `WAIT(-1)` times out.** BayesTree beta 5 held its node page with `WAIT(-1)` between two `GETKEY` drains; the finger lift from the tap that opened the page is a touch event, so it could satisfy the wait at once, and after about a minute with no event `WAIT(-1)` returns −1 and the page closes by itself. Hold pages with `xxWaitAny()` — drain keys AND the capped `MOUSE` drain, poll `GETKEY` and `MOUSE` together, drain again.

**`MOUSE` and `WAIT(-1)` number their event types differently** (Commands reference, 16 Oct 2026). `MOUSE` list, fifth element: 0 New · 1 Completed · 2 Drag · 3 Stretch · 4 Rotate · 5 LongClick. `WAIT(-1)` list, first element: 0 Down · 1 Move · 2 Up · 3 Click · 5 Stretch · 6 Rotate · 7 Long click. A pinch is 3 in one and 5 in the other; a drag 2 and 1. Say in the comment which table a handler reads.

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

**`random` is absent, so `try: from random import random` is a guaranteed fallback, not a precaution.** NormExplorer's sampler carried that guard for eleven builds; the xorshift fallback ran on every call. Import from `urandom` first (beta 41 does).

**`hpprime` has more than `eval`.** In confirmed use:

- `fillrect(gr,x,y,w,h,edge,fill)`, with `gr=0` meaning the screen.
- `keyboard()` for any-key-down.
- `dimgrob(n,w,h,colour)` for an off-screen grob (used to measure text).

Colours are 24-bit `0xRRGGBB` integers.

**Argument orders that ran on the G2** (StudRangePy's plot, header line 16; recorded as observed, 16 Oct 2026): `fillrect(gr, x, y, w, h, edge, fill)`, `line(gr, x1, y1, x2, y2, c)`, `pixon(gr, x, y, c)`, `textout(gr, x, y, text, c)` with `gr = 0` the screen.

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

## 9b · The CAS behind the fence (v7h: CASProbe beta 1b ran on the Prime's firmware)

**What we know, from the emulator** (HP Prime Virtual Calculator 2.4.2, build 2026-09-09, 17 Oct 2026; CASProbe beta 1a, then beta 1b):

| Call | What happens |
|---|---|
| `CAS(comb(100,50))` written in the program | evaluated, but a CAS integer too big for Home crosses back as a 12-digit real |
| `CAS(s)`, `s` a string variable or parameter | **the text comes back unevaluated** |
| `EXPR("CAS(" + q + s + q + ")")`, q = CHAR(34) | evaluated; big integers still become reals |
| `EXPR("CAS(" + q + "string(" + s + ")" + q + ")")` | **evaluated, and the answer arrives as a PPL string**: all 30 digits of C(100,50), all 300 of C(1000,500), `35/128`, `(2*cxt+1)*(3*cxt+2)` |
| `STRING()` of that answer | adds a pair of quotes; `"" + answer` does not |
| a syntax error in the text | a run-time error that IFERR catches |
| an unknown function | handed back unevaluated, e.g. `cxnosuch(3)` |
| 6,005 characters of CAS text in one call | fine |
| Python `cas.caseval` | no crash, but returns a decimal for C(100,50); stays outside the fence |

**How the Prime prints CAS answers** (it is not desktop Giac's printing, which the harness used until v3b):

| What | The Prime | Desktop Giac 1.9 |
|---|---|---|
| exp | `e^(cxt^2/2)`, `1/2*cxl^2*e^(-cxl)` | `exp(…)` |
| sqrt | `√2`, `erf(49*√2/50)/2+1/2` (U+221A) | `sqrt(2)` |
| solve | `{1/20}`, `{-2,2}`, a system `{[2,1]}` | `list[…]` |
| fsolve | `[0.0950338528553]` | |
| a limit to infinity | `∞` (U+221E) | `+infinity` |
| 1/0 | `±∞` | `infinity` |
| 0/0 | `undef` | `undef` |
| series | `…+cxt^4*order_size(cxt)`; `convert(…,polynom)` drops it | same |
| evalf | 12 significant digits | |
| negative numbers, products | ASCII `-`, `*` | same |

**CAS variables persist.** `cxq:=7` survives into the next call, and so into the student's CAS view, until `purge(cxq)`. Never assign a CAS variable in a fleet program; solve for it or leave it a symbol.

**The fence** (BRIEF_CAS_v2.md has the code):

1. **One call routine, `xxCas(s)`**:
   ```
   IFERR cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")")); THEN cR := ""; END;
   ```
   Drop one pair of surrounding quotes. An answer containing `undef`, `rror` or `∞` (CHAR(8734)) counts as a failure. `s` must never contain a double quote.
2. **CAS text is built from integers only, by `xxIStr(n)`.** Home's `STRING(-2.5)` gives the U+2212 minus. The CAS happens to read it, but the rule stands: write 0.95 as `95/100`.
3. **Events, never frames.** Call the CAS when a page opens, a tap lands or a finger lifts, and only when the inputs changed; cache the text. Speed on the emulator: 8 ms at most per call; on the G1, unknown.
4. **Text for display; numbers from PPL.** A CAS number is used only through `EXPR(text)` inside IFERR, with the PPL value as the fallback.
5. **Tagged CAS variable names** (`ctq`, `erpz`), never x, n, p, k, t. Never assign them.
6. **A badge**, "exact (CAS)" or "decimal", wherever a CAS answer appears.
7. **Check every answer by value**, against the program's own number. Never by its text: `exp(`, `sqrt(` and `list[` never appear on the Prime. A failed check shows "no closed form shown".
8. **No** `#cas` blocks, `CAS.name()` calls, cross-program calls or Python `cas.caseval`.
9. **The CAS's job must be visible.** A purely numeric answer (a Clopper–Pearson bound with k > 0, a conditional MLE) is computed in PPL.

**Desktop Giac traps** (still worth knowing; the harness uses desktop Giac with a Prime-printing layer since v3b):
- A plain `sum` over an index makes Giac try to solve Gamma equations, even with numeric bounds; `sum(seq(…))` avoids it.
- `fsolve` around a `sum` fails; expand first, or bisect in PPL.
- The binomial→Poisson limit needs a numeric k.
- `factor()` on symbolic square-root forms can be wrong; send the plain expression.
- A full `factor` of a long binomial sum took over 60 s at n = 10,000.
- The Logistic's E[X²] came back with the wrong sign, hence rule 7.

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

**Soft-key pages: the "More" key** (Roger, 16 Oct 2026). When a screen needs more than six soft-key actions, slot 6 reads "More" on EVERY page and steps to the next page of labels, wrapping to page 1 — the job the NXT key did on the HP 48 (NEXT on the HP-28). The most-used actions go on page 1; a destructive action never sits where the finger lands after a page turn; a screen whose actions fit in six gets no "More". Shape: `TouchKit_template_v2.txt`; DRAWMENU is verified, the paging is only program state.

**CAS badge** (v7g): "exact (CAS)" when the line came from the CAS, "decimal" when it fell back — dodger blue, beside the value.

Panels: coloured border, light fill, matching text. **The canonical footer is CentralLimit's**: comma-separated, spaces round `=`, dodger blue — `+/- = n, tap top = redraw, Ent = menu, Esc = quit`. Four other forms were in use on 16 Oct 2026 (colons, no spaces, space-separated, grey); the fix versions adopt this one. Arrow glyphs: `⇆`/`⇅` (CHAR(8646)/CHAR(8645)) or the `CHAR(8592)+CHAR(8594)` pair — both render; Roger to pick one. Subscripts: `CHAR(8320)`-style builds or the literal ₀ ₁ ₂ from the Chars menu — both render; same decision.

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
12. **Check the whole fleet for duplicate routine names before every paste** (`python3 fleet_names_v2.py *.txt` in `D:\HP-Prime`), as well as the single-file checks (`ppl_check_v3.py`, `lint_ppl.py` — `ppl_gate_v1.py` runs all of them). One program is never the whole picture on a calculator that pools every program's routines (§5).
13. **Version strings inside a file are references too.** The banner, the help page, the companion-file name in a header, the file map's line count — seven were stale on 16 Oct 2026 (StatDist said v2.3 twice in v2.4; StudRange and its twin named beta 12a; NormExplorer's map was 12 lines short). Sweep them with every rename, as rule 6 says for menu numbers.
14. **The gate, before any paste**: `python3 ppl_gate_v1a.py NEW.txt [ORIGINAL.txt]` (v1a, 16 Oct 2026: paths made absolute — `lint_ppl.py` used to read a relative path from its own folder, fail, and the gate's filter hid the failure; a lint that prints no summary now fails the gate; the fleet check compares against the newest version of each program only) in `D:\HP-Prime`. It runs `hpprime lint` from hp-prime-kit (0 errors on every device-tested program in the fleet, so an error is real), `ppl_check_v3.py` (E2/E3/E6/E8/E10/E11 must be zero; v3 matches built-ins ignoring case, as the device does — v2 reported `TYPE` and `LEFT` as unknown because the list spells them in lowercase — and no longer mistakes `!=` for `=`), `lint_ppl.py` (block balance, LOCAL sizes, CHOOSE and INPUT shapes), a full parse with the kit's PPL interpreter where it can read the file (it does not read file-level LOCAL after an EXPORT list, forward declarations, `√`, or `#RRGGBB:24h`; a parse failure on those lines is the tool's limit, not an error), and `fleet_names_v2.py` over every program in the folder.

15. **The run harness before the device** (`ppl_run_v3c.py`, README beside it): the kit's interpreter with SciPy-backed built-ins and scripted keys, taps and drags; lists copied on assignment as on the calculator (v2); `CAS("...")` answered by desktop Giac and logged (v3); since v3b the Prime's way: `CAS(variable)` unevaluated, `EXPR("CAS(...)")` evaluated, Giac's printing translated to the Prime's (`e^(`, `√`, braces, `∞`), big integers turned to reals unless they are strings; since v3c, soft-key taps under `WAIT(-1)` as type 3 only, and the integer-df built-ins raising on a fractional df. Every program with a CAS feature is run once with `cas='giac'` and once with `cas='fail'`; every CAS template it can build is also run through `icas` in its verify script. Harness agreement is not device agreement — the checklist still decides — but it has caught a wrong BINOMIAL argument order (GaltonBoard), a clamp that never fired (ChiTable) and a crossed-bounds negative probability (StatDist) before any paste. It caught none of the emulator's findings before v3b/v3c modelled them — which is why the emulator run comes before the hardware run.

## 15 · Current fleet

**One current set, 17 October 2026** (in `D:\HP-Prime` and `FIXED_FOR_DEVICE`). The round-1 touch-and-graphics versions ran on the Virtual Calculator on 16–17 Oct 2026 (§16; Emulator_Round1_Results_2026-10-17_v1.md). The round-2 CAS versions were then fixed for the Prime's CAS (call form and printing) and for what round 1 found, and became current. Round 1 and the round-2 originals are in `_superseded_2026-10-17`, so either can be restored.

Each program has `_CHANGES.md` files with device checklists (the "a" ones: the CAS call form; the "b" ones: the round-1 emulator fixes) and a `verify_*.py` run in harness v3c. **"Emulator" below means its round-1 predecessor ran there**, except where stated; none has run on a G1 or G2 since 10 Oct.

| Program | Version | State |
| --- | --- | --- |
| **ChiTable** | beta 3b | Emulator: the full checklist passed (beta 2). Beta 3 adds the exact CAS pages; 3a the call form; 3b shortens two clipped menu items. |
| **GaltonBoard** | beta 3b | Emulator (beta 2): passed, including the MicroPython 100,000-ball drop. 3a: the Poisson-limit reader accepts `e^(`; 3b: solid pegs and balls (RECT_P), labels clear of the binomial line. |
| **BayesTree** | beta 8b | Emulator (beta 7): passed except soft keys. 8b reads soft keys from WAIT(−1) type 3 (§7), guards a stale click after a view closes, and makes every rounded pair add up. |
| **StudRange** | beta 15a | Emulator (beta 15): the Python bridge, HSD and the plot passed; soft keys on the plot failed. 15a: type-3 soft keys; Quit says "p not computed". |
| **StatDist** | v2.7b | Emulator (v2.6): gallery and plots passed; a fractional chi-square df stopped it. 2.7a: call form; 2.7b: fractional df through `st_gammaP` / `st_betaI`, short INPUT labels. |
| **TrendTest** | beta 3b | Emulator (beta 2): passed. 3b: shorter example names, solid dots. |
| **PowerViz** | v2.5a | Emulator (v2.4): passed (LocalHeadProbe confirms its `LOCAL pv_Name()` heads). |
| **EpiStats** | v1.7a | Emulator (v1.6): the 2×2 path passed, every number = SciPy. |
| **CICatcher** | beta 2a | Emulator (beta 1): passed. |
| **CentralLimit** (app) | beta 3a | **Not run** (the app install through the Kit did not take). |
| **DNAMixLR** | beta 3a | Emulator (beta 2): passed. |
| **ScatterLab** | beta 2a | Emulator (beta 1): passed. |
| **ErrorRate Lab** | beta 1a | **Emulator: beta 1a passed**, with a real CAS limit `ln(20)` on the "Why 3" page. Beta 1 showed its question as the answer. |
| **NormExplorer** | beta 42 | Emulator: most of the checklist passed. |
| **Norm3 / Burr3** | v2.4 / v2.4 | Emulator: passed. They take arguments; the Catalog asks. |
| **SampDist** | v2.3 | Emulator: passed. Next: v2.4, the candy lab (CandyLab_Design v6). |
| **TestChooser** | beta 2 | Emulator: passed. |
| **BiNorm3D** | beta 1 | Emulator: passed. |
| **FDAES** | v3.6 | Emulator: passed. Held back from this repository until two reference values are re-checked against their sources. |
| **TouchKit template** | v3 | The F1 note added; the code is unchanged. |
| **GfxProbe** | beta 1 | Ran on the emulator; rerun on the G1 and G2 for T15 (held key), T16 (two fingers) and timing. |
| **CASProbe** | beta 1b | Ran on the emulator (§9b). Rerun on the G1 for speed. |
| **LocalHeadProbe** | beta 1 | Passed on the emulator. |
| **MenuTapProbe** | beta 1 | NEW, 40 lines: records raw WAIT(−1) events with DRAWMENU shown (§7). |
| **Retired** | | ConTable2 and FEP (in EpiStats), StudRangePy (in StudRange). Delete them from the calculators. |
| **PyProbe beta 2b / PyDirect beta 1 / PyVer / JoinTest / GenTest** | | Diagnostics, unchanged. |

**Still to settle on the calculators:** G1 speed (CAS calls, drags, the morph), a light finger tap on soft keys in polling loops (§16), held keys (GfxProbe T15), two fingers (T16), CentralLimit as an app, and whether an INPUT or CHOOSE OK tap leaves a click for the next `WAIT(−1)`.

## 16 · Testing on the Virtual Calculator (v7h)

**What it settles.** The HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) runs the calculators' firmware, so these behave as on the G1 and G2:
- commands and what they accept or reject;
- the CAS and how it prints;
- MicroPython and the bridge;
- drawing and glyphs;
- what `WAIT(-1)` and `MOUSE` report for a tap or a drag.

Round 1 of the fleet ran there on 16–17 Oct 2026 (Emulator_Round1_Results_2026-10-17_v1.md).

**What it cannot settle:**
- G1 speed (the PC is far faster: 100,000 Galton balls in 7 ms);
- a key held down;
- two fingers;
- how a real finger tap compares with a mouse click.

A mouse click shorter than a polling loop's pass can be **missed** by a `GETKEY` + `MOUSE` loop (the StatDist gallery, PowerViz's α+, CICatcher's welcome page). A press of about 0.3 s always registered. Check on the calculator that a light tap works.

**How to drive it** (computer use, from the cloud):
- **Load:**
  1. Open the program's file from `FIXED_FOR_DEVICE` in Notepad and copy all of it.
  2. In the Connectivity Kit, right-click Programs, choose New, and type the name.
  3. Paste the text into the editor and click Save. The Kit gives no syntax check. The calculator's own editor does: Program Catalog (Shift 1) → Edit → Check.
- **Replace a program by opening it in the Kit, never by adding a second copy.** Two copies share one pool of routine names (§5).
- **Run:** paste the program's name into Home **without parentheses**, or use the Catalog's Run. `Name()` with empty parentheses in Home is a "Syntax Error"; it is not a fault in the program.
- **Read a log:** evaluate it in Home, select the result, then Edit ▸ Copy (Ctrl+C) in the emulator's menu. The Windows clipboard then holds the calculator's own text.
- **Typing:** letters typed from the PC keyboard leave the emulator in ALPHA lock, so digits typed after them come out as letters (2 → Z). Paste from the clipboard instead. Shift on the skin followed by the PC's 1 opens the Program Catalog.
- **PC Esc after the skin's Shift is Shift+Esc**, which clears the Home history.
- **Apps:** installing an app program by saving from the Kit's app editor did not reach the calculator (CentralLimit). Use the calculator's own Program Catalog.

*Shelved: a three-level Bayes tree for desktop — R/Shiny favoured for the classroom.*

---

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
