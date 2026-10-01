# HP Prime Lessons Learned
*Roger Metcalf & Claude · rewritten 28 September 2026*

Working notes for writing PPL and MicroPython on the HP Prime. Everything here was found on hardware, not read in a manual — where a claim is inferred rather than observed, it says so.

**Verified on:** HP Prime G2 and G1, both running the **2026-09-09** firmware, plus the desktop Virtual Calculator. Firmware matters more than it looks: glyph rendering and app-variable reachability have both proved version-dependent, so a "device-verified" claim is only verified on a stated build.

---

> ## Read this before writing code
>
> Not after. In one September session, four bugs were rediscovered the expensive way — the `STRING` mode, the FREEZE pause, the x-bar glyph, and the LOCAL limit — and all four were already written down here.
>
> Then: **grep the uploaded `.txt` corpus** for anything this file does not cover. `<>` was avoided for a whole session as "unverified" when five corpus programs use it.
>
> Then: **read the uploaded reference PDFs.** Note that `HPPrimeProgrammingUDelaware.pdf` is actually a ZIP of page images with a broken text layer — it will not turn up in a text search and has to be unzipped and read as images. It is the only document in the library that covers Python.

---

## 1 · Which language, and why

**PPL by default.** It is good at calculating, and the native `_P` graphics have no Python equivalent worth reimplementing. Anything that redraws on a keypress stays pure PPL.

**Python (MicroPython) when the arithmetic earns it.** Compute-heavy engines — quadrature, root-finding, simulation — get a real speed-up because the math primitives are compiled C while PPL loops are interpreted. A measured case: StudRange's critical value takes about a minute in PPL (60-step bisection) and about 1.5 seconds in Python (secant, ~9 evaluations).

The counter-example matters as much. A live power visualiser with held-key stepping and four reshaded regions per frame gains nothing — its arithmetic is a handful of CDFs per redraw, and the bridge crossing would cost more than the computation. **Of nine programs in this fleet, one was worth converting.**

**CAS only for genuinely symbolic work.** Prefer deriving closed forms off-device, verified against SciPy, and shipping clean numerics. Home capitals A–Z are built-in global reals; CAS lowercase are symbolic; case matters. Keep each program on one side of the fence.

State *why* in one line before splitting any project across languages.

## 2 · Hard limits

- **16 arguments** maximum on user function definitions *and* built-in calls. Pack into lists, unpack inside.
- **`CHOOSE` simple syntax caps at 14 options**; the list form `CHOOSE(var,"title",{...})` is unlimited.
- **Never test `CHOOSE`'s return value for a specific number.** Initialise the index variable to 0, call `CHOOSE`, then test the index variable itself. Cancel leaves it 0.
- **`INPUT`'s first argument must be a list of variable NAMES**, written back in place. Value lists give "Invalid Input".
- **Never `INPUT` into a function parameter.** Copy to a `LOCAL`, `INPUT` that, assign back. Parameters as targets fail silently.
- **`LOCAL` statement size: 7 is known to work; 6 is the house habit.** BayesTree ships with three 7-variable `LOCAL` lines and runs fine on device, so the earlier "maximum 6" was over-cautious and whatever failure prompted it had another cause. The true ceiling has not been established — the documented figure was 8. Keep to 6 by habit, do not go rewriting working code that uses 7. **`LOCAL` inside `IF`/`CASE` is genuinely rejected** — hoist to the top of the function, splitting across several lines.
- **A PPL function cannot modify its caller's variables.** Parameters pass by value. Shared state therefore lives in exported globals, which means every write path to that state must be audited together.
- **Parameter names must not collide with built-in FUNCTION names** (`FP`, `IP`, `LN`, `RE`, `IM`, `SIGN`…). `fp` as a parameter is a syntax error even though `LOCAL fp` parses fine — the parameter parser is stricter.
- **Programs with parameters get an auto-generated argument form** from the catalog. Menu-driven tools take zero arguments and hold defaults internally; plot explorers launched from Home with values keep theirs.
- **`.hpprgm` is binary** (UTF-16LE plus header). Distribute as `.txt` and paste into the Connectivity Kit editor. UTF-8 import can append stray CJK characters at the end — harmless, delete them.

## 3 · Command truths

- **`STRING(value, mode, digits)`: mode 1 is Standard and IGNORES the digits argument.** `0.6826894921` stays full length no matter what you ask for. **Fixed decimals need mode 2.** Easy to miss because most values still look right; only long decimals expose it, and it silently disables computed decimal counts on axis labels. Sweep every `STRING` call before delivery.
- **`CHISQUARE(n,x)` is the DENSITY.** P-values need `1 - CHISQUARE_CDF(n,x)`.
- **`<>` is valid for not-equal** — corpus-confirmed in CHOOSE_R, Hammurabi and PONG. No need to restructure around it.
- **Confirmed working:** `NORMALD` / `NORMALD_CDF` / `NORMALD_ICDF`, `STUDENT(_CDF)`, `FISHER(_CDF)`, `BINOMIAL(_CDF)` including the 4-argument form, `POISSON(_CDF)`, `COMB`, `IFTE`, `MAKELIST`, `CONCAT`, `RANDOM`, `PIXON_P`, `TYPE` (6 = list), `SIZE`, `CHAR`, `ROUND(v, places)`, `MOUSE`, `VIEW`, `mean`, `stddev`, `variance`.
- **Do not exist:** `GEOMETRIC*` — compute p(1−p)^(k−1) by hand. `LNGAMMA` outside the CAS — carry a Lanczos helper, or use Python's `lgamma` and delete it.
- Prefer native `NORMALD_ICDF` to any hand-rolled inverse normal.

## 4 · Input fields

- **There is no blank input field, and the string workaround fails.** A PPL real always holds a value, so a numeric `INPUT` always shows one. A string variable initialised to `""` does *not* give an empty box — the Prime renders the quotation marks as editable text, and deleting them to type a number is a syntax error. *(Device-verified.)*
- **House default is 0**, unless 0 is illegal for that field — areas, α, confidence levels — where the conventional value goes in: 0.90, 0.05, 0.95.
- **Defaults are pedagogy, not placeholders.** A prefill computed from other session values reads as a stray number and generates a bug report. This happened: `x := μ + σ` with μ=22, σ=4 opened a solver at 26 and looked broken. Use flat constants, or state the rule in the field's help line.
- **Guards should teach.** "σ must be positive" is adequate. "These values give σ = −9.18; the sign of z must match the sign of x − μ" is better, because that *is* the student's error.

## 5 · Reserved words and characters

- **Scan every new name** against PPL keywords: `STEP` (use `stp`), `TO`, `FROM`, `DO`, `OR`, `AND`, `MOD`, `e`, `Re`. The syntax error lands at the usage line.
- **Write exponent literals with a capital E.** Corpus code uses `1E10` and `-1E10`; lowercase `1e-9` is unverified, and lowercase `e` is a reserved name. Or just write the decimal out.
- **Avoid bare single-letter lowercase identifiers.** `x` is the CAS's symbolic variable, `i` the imaginary unit, `e` already listed. *Honesty note: a suspected stale-CAS-`x` leak was tested and DISPROVED — CAS `x` was 0. This is cheap insurance, not a diagnosed cause; do not cite it as one.*
- **House convention: prefix every local with a routine tag** — `zsX`, `ndPY`, `pcA`, `awlo`. Makes greps and renames tractable.
- **x-bar is `CHAR(57344)`** (U+E000); **p-hat is `CHAR(57345)`** (U+E001). Single precomposed glyphs in HP's private-use area — they position themselves and scale with the font. **The combining macron U+0304 does NOT stack**; it renders as its own character to the *right* of the x. A hand-drawn `LINE_P` bar also works but needs per-font pixel tuning. Use the glyph.
- **Subscript digits render:** `CHAR(8322)` = subscript 2, paired with `CHAR(956)` = μ for labels like μ₂.
- Characters taken from the on-device **Shift-Chars menu are pre-verified by construction**.
- **`EXPORT` on a helper publishes it in the catalog.** Keep helpers non-`EXPORT`.

## 6 · Graphics

- Screen is 320×240, origin top-left, y increases **down**. The y-flip: `py := BOT - IP(y/ymax*H)`, then clamp.
- **Compose off-screen and blit once.** `DIMGROB_P(G1,...)`, draw every pass to `G1`, then one `BLIT_P(G0,0,0,G1)`. Drawing straight to `G0` tears visibly. Miss one `G1` argument and that element flickers alone — a useful diagnostic.
- **Shading must iterate pixel columns**, not math samples. Sample loops leave white gap columns; this bit two programs before the rule stuck. Iterate pixels, solve for x.
- **Cache the density — for EVERY curve, not just the first.** If three passes need the same pdf, evaluate it once per pixel column into a list. The trap is doing this for the main curve and forgetting the comparison curve: a second curve read by both an overlap fill and a trace costs two `NORMALD` calls per pixel per frame — 544 on a 272-pixel plot, on top of the main curve's 273. That is the one per-frame cost a G1 can actually feel during a live drag.
- **Precompute anything needed twice in the same frame.** Histogram bar heights were computed once to widen the y-scale and again to draw. Build the array first, then use it in both places.
- **Verified GETKEY codes, the only ones to trust:** Esc=4, Left=7, Right=8, Up=2, Down=12, Enter=30, +=50, −=45, 0=42. Route anything else through Enter → `CHOOSE`.
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

## 8 · MicroPython: getting it running

**The interpreter is MicroPython 1.9.4** — confirmed by `sys.implementation` on a G2 with the 2026-09-09 firmware. That release's documentation was last updated December 2018 and tracks CPython 3.4. **Check the 1.9.4 docs, not the current ones.** Most of the quirks below follow from this one fact.

**Python arrived in firmware 2.1.14567, April 2021.** Not 2.1.14181 — that build is from November 2018 and has no Python at all, though it is sometimes quoted.

**Module inventory on this firmware:** `math`, `cmath`, `urandom`, `hpprime`, `arit`, `linalg`, `matplotl` and `gc` all present. **`random` and `time` are absent.** `urandom.getrandbits()` is the natural random source here.

The missing `time` is independently confirmed by hp-prime-kit on a different G2, and they give the workaround: build your own on **`eval('ticks()')`**, which returns milliseconds. Worth knowing that `ticks()` exists — it is the only timing source on the Python side.

**`hpprime` has more than `eval`.** In confirmed use: `fillrect(gr,x,y,w,h,edge,fill)` with `gr=0` meaning the screen, `keyboard()` for any-key-down, and `dimgrob(n,w,h,colour)` for an off-screen grob (used to measure text). Colours are 24-bit `0xRRGGBB` integers. A longer list — `arc`, `blit`, `circle`, `line`, `mouse`, `pixon`, `rect`, `textout` and `_c` variants — is documented by the community but unverified; nearly all have a PPL equivalent reachable through `eval` anyway.

**Two installation routes, and confusing them is the support question.**

*Route A — embedded in a PPL program.* The Python lives in a `#PYTHON name … #END` block with a PPL wrapper `EXPORT f() BEGIN PYTHON(name); END;`. Install like any PPL program: paste the `.txt`, sync. **There is never a separate `.py` file.** It launches from the Program Catalog and the user need never open the Python app. This is the house method and the right answer for anything you hand to someone else.

*Route B — a standalone `.py` in the Python app.* These do **not** appear in the Program Catalog; they live under Apps → Python → Files. People sync a `.py`, look in the Program Catalog, find nothing, and conclude it failed.

**Paste, do not retype.** Indentation survives a paste into the Connectivity Kit; hand entry invites a tab-and-space mismatch that is miserable to find on a small screen.

## 9 · MicroPython: the bridge

**The pattern.** PPL writes named globals, Python reads them with `hpprime.eval`, and writes back by assembling a PPL assignment as text. `eval` also writes and reads PPL globals directly (`ev('CX:=3.5')`, `ev('CX')`) and calls your own PPL functions (`ev('MYFUNC(1.0)')`).

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

There is no official HP documentation for the Python side. Four sources are worth knowing, in rough order of value:

- **`JordiRigau/hp-prime-kit`** on GitHub — `docs/topics/micropython.md` in particular. Every claim is labelled measured or unverified, and measured ones name the firmware. Also ships a PPL linter, an interpreter, and a `.hpprgm` builder. The best single source found.
- **Mark Mitchell's HP Prime Programming page** (udel.edu/~mm/hp/primePython/) — the `hpprime.eval` bridge, calling `CHOOSE` and `DRAWMENU` from Python, `AVars()` for typed values, touch via `mouse`. Also in this project as a PDF, though that file is a ZIP of page images with a broken text layer.
- **Neil Streeter's HP Prime Python Activities** (hpcalc literature, June 2025) — HP-adjacent introduction, the `#PYTHON` wrapper, writing in VS Code and pasting.
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
7. **Version the filename with the build**, and delete stale copies so there is never ambiguity about which file is current.
8. **An outside code review is worth having, but not worth pasting.** A reviewer with only the source text can spot real problems — two genuine per-frame costs were found this way, both verified against the file. But a full-file rewrite produced without the actual file silently drops things: one such rewrite omitted a `LOCAL` declaration that existed in the original, introduced a lowercase exponent literal, and downgraded 81 working Greek glyphs to ASCII on a speculative "paste fidelity" argument against device evidence. **Take the findings, implement them on the verified file.**
9. **Record disproved theories AS disproved.** A note that reads like a diagnosed cause will send the next session down the same dead end. Two confident explanations of the `join` failure were tested and failed; both are now labelled.
10. **When Roger pastes his edited version, sync to his edits first.** His device copy is the source of truth.
11. The ~600-program corpus zips do **not** persist between sessions. The 83 individual `.txt` files in the project do. For the full corpus, grep a local folder from Claude Code rather than uploading.

## 15 · Current fleet

| Program | State |
| --- | --- |
| **Norm Explorer beta 39** | Menu-first normal workbench: auto-scaling window for any μ and σ, four probability directions, inverse calculations, z-formula solver, touch input, data module reading D1 / C1 / C2, simulated sampling, Cohen's d, standardize animation, diagnostics page. Guide written. Data module emulator-tested only. |
| **StudRange beta 11** | Studentized range in PPL: p-value, critical value, Tukey HSD, interactive plot with α ladder. df ≥ 3. |
| **StudRangePy beta 14** | The MicroPython twin. Handles df ≥ 1, far faster on critical values, static plot. |
| **EpiStats v1.1** | Seven-module epi suite. *Pending: M-H confidence intervals, Breslow-Day.* |
| **FEP** | Fisher exact plus chi-square, corrected p-values. |
| **ConTable2** | Contingency battery, row-based RR/RD, Haldane-Anscombe, McNemar. |
| **StatDist** | 17 distributions live, 10 stubbed. |
| **SampDist** | Sampling-distribution explorer. |
| **Burr3 / Norm3** | Parameter explorers with CDF overlay and mean marker. |
| **BayesTree** | Natural-frequency tree, ROC view, PPV-vs-prevalence, 2×2 view. *Pending: sequential evidence, Fagan nomogram.* |
| **PyVer / JoinTest / GenTest** | Throwaway diagnostics. `PyVer` reports interpreter version and module list. |

*Shelved: a three-level Bayes tree for desktop — R/Shiny favoured for the classroom.*

---

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
