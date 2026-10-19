# ppl_run_v3e -- run a fleet program on the PC, scripted

`ppl_run_v3a.py` runs an HP Prime PPL program's real source on the PC, with the student's key presses, taps, menu picks and form entries supplied by a script, and records everything the student would have seen: every TEXTOUT_P (text, position, font, colour), every screen shown, every MSGBOX, CHOOSE and INPUT, and the Terminal. It is built on hp-prime-kit's interpreter (`hpkit/interp.py`; found through the `HPKIT` environment variable, else unpacked from `Community_Library/github/JordiRigau__hp-prime-kit.zip` beside this file or one folder up, as `ppl_gate_v1b.py` does) and does not modify it.

It is a test bench for **logic and layout**, not a substitute for the calculator. Nothing here is device evidence. See *Limits*.

**This is the v3e README** (17 October 2026). The tool is `ppl_run_v3e.py`. Everything below up to the v3c section is v3b's text and still holds, except where the sections at the end say otherwise: v3c models two findings of the first emulator round -- how a tap reaches `WAIT(-1)` (F1) and which statistics built-ins refuse a fractional df (F3) -- and the drawing warnings follow GfxProbe beta 1's results; v3d models the second round's string findings (`INSTRING("")`, small fixed decimals; v3d had no README of its own, so its section is taken from its docstring); v3e puts Home's minus before a scientific exponent.

Files: `ppl_run_v2.py` (the tool, CLI and module), `test_statdist_example.py` (example tests), this README. It needs Python 3.8+ and SciPy for the statistics built-ins.

## Quick start

```
python3 ppl_run_v2.py StatDist_v2.5.txt --call "st_calc_normal()" \
    --choose 1 --input "mean=100,stdev=15,x_val=130" --key Enter
```
prints the CHOOSE and INPUT it answered, then the result page line by line (`y=114 x=6 f2 #C800C8  P(X <= 130.0000) = 0.977250`), the key it took, any warnings, and any script left unused.

```python
from ppl_run_v2 import Harness, KEY, ACCEPT, CANCEL
h = Harness('StatDist_v2.5.txt', strict=True)
h.choose('Lower tail')                         # by label (substring) or index; 0 = cancel
h.answer({'mean': 100, 'stdev': 15, 'x_val': 130})
h.press('Enter')                               # or KEY['Enter'], or a number
h.call('st_calc_normal')                       # or h.execute('st_calc_normal()')
page = h.pages[-1]
assert page.find('P(X <=').hex == '#C800C8'
```
CLI options: `--call EXPR` (repeatable), `--choose N|LABEL`, `--input "a=1,b=2" | "1,2" | ok | cancel`, `--key K` (a code or Esc/Enter/Left/Right/Up/Down/Plus/Minus/Zero), `--tap X,Y`, `--timeout`, `--idle-key K`, `--strict`, `--stale-keys`, `--seed N`, `--show timeline|screens|texts|all`, `--coverage`. `--coverage` lists every built-in or outside name the program uses that the harness does not cover. All 20 fleet programs load, and their only uncovered names are CentralLimit's Statistics-app settings.

## What the pre-pass and parser accept

The fleet's source loads as written. All rewriting happens **in code only, never in strings or comments**, and line numbers are kept.

| Construct | Handling |
| --- | --- |
| `#pragma ...` | blanked |
| `#PYTHON ... #END` | blanked. `PYTHON(name, ...)` is recorded and does nothing, so the program's PPL fallback runs, as it does on the device when the Python side fails (Lessons Learned s9). A warning names the call. |
| `#RRGGBBh`, `#RRGGBB:24h` | converted to decimal. **The kit could not read these; worked around.** |
| root sign `√(x)`, `√x` | becomes `SQRT(x)`. **The kit could not read it; worked around.** |
| `π`, `e` | defined as globals, so the source keeps its pi sign |
| `≤ ≥ ≠ −` | `<= >= <> -` |
| file-level `LOCAL`, before or **after an EXPORT list** | read as program globals, shared by every routine as on the device. **The kit could not read this; worked around** (ChiTable, PowerViz, TrendTest and others). |
| forward declarations `name();` | skipped; a warning if the routine is never defined. **The kit could not read these; worked around** (NormExplorer, StudRange). |
| `LOCAL name(...)` routine heads | read as routines (PowerViz) |
| `VIEW "label", name()` | read as routines and listed in `h.views` (CentralLimit, an app program) |
| `x₀`-style names | already legal in the kit's lexer |

## Built-ins

**From the kit, unchanged:** SIZE, DIM, EXPR, ROUND, ABS, MIN, MAX, IP, FP, FLOOR, CEILING, SIGN, SQRT, LOG, LN, EXP, MOD, RGB, CONCAT, LEFT, RIGHT, MID, INSTRING, SORT, RREF, TRN, IDENMAT, DET, INVERSE, and the lazy IFTE, MAKELIST, MAKEMAT.

**Statistics (SciPy), with HP's argument orders and forms:**
- `NORMALD([μ,σ,]x)`, `NORMALD_CDF(x)`, `(x1,x2)`, `(μ,σ,x)` and `(μ,σ,x1,x2)`, `NORMALD_ICDF([μ,σ,]p)`.
- `STUDENT(n,x)`, `STUDENT_CDF(n,x[,x2])`, `STUDENT_ICDF(n,p)`.
- `CHISQUARE`, `CHISQUARE_CDF` and `CHISQUARE_ICDF` likewise.
- `FISHER(n,d,x)`, `FISHER_CDF(n,d,x[,x2])`, `FISHER_ICDF(n,d,p)`.
- `BINOMIAL(n,p,k)`, `BINOMIAL_CDF(n,p,k)` and `(n,p,k1,k2)` (inclusive), `BINOMIAL_ICDF(n,p,q)`.
- `POISSON(μ,k)`, `POISSON_CDF(μ,k)` and `(μ,k1,k2)` (inclusive), `POISSON_ICDF(μ,p)`.
- `COMB` and `PERM`: exact integers. A result above the Prime's range (1E500) is a runtime error, as on the device (the ConTable2/FEP overflow). One above a double's range but inside the Prime's raises Unsupported.
- Every call is logged in `h.stat_calls`.

**Refusing to guess.** A call whose device answer has never been observed raises `Unverified`. Examples: a negative or fractional k (v2.4's `POISSON_CDF(5,-1)`), σ ≤ 0, df ≤ 0, p outside [0,1], an ICDF at p = 0 or 1, SUB out of range. Pass `on_unverified='warn'` to continue with SciPy's value and a warning. A NaN always raises. A non-integer df is only a warning.

**Added here:**
- STRING with display modes: 1 Standard ignores the digits argument; 2 fixed decimals (the kit's STRING ignored the mode); 3 scientific. A string comes back quoted, as the kit measured.
- `"text" + number` uses Standard format, 12 significant digits (the kit used Python's repr).
- CHAR, ASC, TYPE (0 real, 2 string, 4 matrix, 6 list), TRUNCATE, SUB, ALOG, `mean`.
- SIN, COS, TAN, ASIN, ACOS and ATAN, which honour `HAngle`: 0 radians (kit, measured; the default), 1 degrees, 2 grads. Choose with `Harness(angle='deg')`.
- RANDOM (no argument, or `(a,b)`) and RANDINT(a,b), seeded by `seed=`.
- TICKS: a virtual clock, 1 ms per reading; `WAIT(n)` advances it.

**Input** (the model is described below): GETKEY, MOUSE, MOUSE(1), ISKEYDOWN, WAIT(-1), WAIT(n > 0), CHOOSE (both forms), INPUT (list form, the single-variable form, and `{var, types, pos}` items), MSGBOX (with the OK/Cancel flag via `msgbox_answer`), PRINT.

**Drawing (recorded, not rendered):**
- Recorded with their arguments: DIMGROB_P, BLIT_P (2-, 4- and 1-argument forms), RECT_P and RECT (no coordinates = clear), TEXTOUT_P and TEXTOUT (returning x + an estimated width), LINE_P, PIXON_P, ARC_P, INVERT_P, SUBGROB_P, DRAWMENU, FREEZE, and the Cartesian LINE, PIXON, ARC.
- GROBW_P and GROBH_P return the grob's size; GETPIX_P returns its background colour.
- STARTAPP, STARTVIEW, CHECK and UNCHECK are recorded and do nothing.
- FILLPOLY_P, TRIANGLE_P, the scaled BLIT_P and MOUSE(2) work but add a "not device-verified" warning, matching the brief's ban.

**Home and apps:**
- A-Z are 0, as Home's reals.
- G0-G9 are graphics objects.
- `D0-D9` and `C0-C9` raise a PPL runtime error, which IFERR catches, as before the Statistics app is first opened. Preset them with `Harness(app_data={'D1': [...]})`.
- App settings (H1, Xmin, Hwidth ...) are not covered.

## The input model

**One ordered event queue holds keys and touches.** Keys and touches share the queue because a page that waits on both (`UNTIL k > -1 OR SIZE(m(1)) > 0`) must know which came first. Add events with:
- `press(code, hold=0, anytime=False)`
- `tap(x, y, lift=False, hold=0)`
- `drag([(x, y), ...], lift=True)`
- `timeout()`
- `event(Key(..), Tap(..), ...)`

CHOOSE answers (`choose(...)`) and INPUT answers (`answer(...)`) have queues of their own; dialogs take their answers in program order.

**When a key or tap is taken.** A non-blocking read (GETKEY, MOUSE, ISKEYDOWN) is handed the next event only when the program is *waiting*. That means two things. First, the same call site, in the same running loop, already answered "nothing" on an earlier pass. Second, nothing has been drawn since that pass. This has three consequences:
- A **drain** (`REPEAT k := GETKEY; UNTIL k == -1;`) leaves after its first "nothing", so it can never eat a scripted key. On the device the key is pressed after the drain.
- A **wait loop** always gets it, on its second pass.
- An **animation** that polls for Esc between frames draws on every pass, so it is not handed the key meant for the page after it. Use `anytime=True` to press during an animation. If the event has waited for `anim_patience` (default 2000) frames, it is handed over anyway.

`WAIT(-1)` blocks, so it takes the next event at once: a key code, `{0,x,y}` for a tap, `{0,..}` then `{1,..}` per drag point, `{2}` after a tap with `lift=True` or at the end of a drag, and -1 for `timeout()`. MOUSE readings are `{x,y,x0,y0,type}`: type 0 on the press and 2 for later drag readings (HP's MOUSE table). `MOUSE(1)` is that list, or -1 with no finger. Bare `MOUSE` is `{{...},{}}`. ISKEYDOWN(k) is 1 in the loop pass where key k arrived, and for `hold` more passes.

**When the script runs out:**
- An empty CHOOSE queue cancels and an empty INPUT queue accepts the form as shown. With `strict=True`, either raises `HarnessStall` instead.
- A wait loop with no event raises `HarnessStall` after `stall_limit` (10,000) idle passes, under a second. The message names the waiting routine and says what is queued.
- `idle_key=4` instead presses Esc whenever the program waits idle.
- `h.leftover()` lists script that was never used.

**Stale-key mode, a drain checker.** With `stale_keys=True`, each dialog's own press stays in the key buffer when the dialog closes: Enter for OK, Esc for Cancel. On the device this skips a page whose wait loop has no drain (Lessons Learned s7). In this mode:
- The next GETKEY takes the left-over key. A drain eats it harmlessly.
- A wait loop that *ends* on it is logged in `h.stale_skips` as a skipped page, and the glimpsed page is captured with reason `'skipped?'`.
- A `WAIT(-1)` that answers it is logged the same way.

**INPUT into a routine's own parameter** is not written back; the device fails the same way, silently (Lessons Learned s2). A warning says so.

## The records

| Attribute | Contents |
| --- | --- |
| `h.screens` | each `Screen` the student saw. G0 is captured at every `BLIT_P` to G0 (`reason='blit'`). It is also captured when the program waits or opens a dialog after drawing on G0 directly (`'wait'`, `'dialog'`), and at the end of the call (`'end'`). `h.pages` holds only the blits, one per composed page. |
| `Screen` | `.texts` (`Text` items), `.shapes`, `.menu` (DRAWMENU labels), `.lines()` (strings sorted top to bottom), `.find(sub)`, `.has(sub)`, `.text_at(y)`, `.func` (the routine that showed it) |
| `Text` | `.text .x .y .font .color .hex .width .grob .func`, `.est_width` and `.clipped`. The last two are estimates from average glyph widths, so treat them as hints. |
| `h.texts` | every TEXTOUT_P on any grob, in order |
| `h.msgboxes` | `MsgBox` with `.lines` and `.over_five` (MSGBOX shows about 5 lines) |
| `h.dialogs`, `h.chooses`, `h.inputs` | `Choose(title, items, index, label)` and `Input(title, names, labels, helps, before, after, accepted)` |
| `h.timeline` | everything in order. The CLI prints it. |
| `h.terminal` | PRINT output |
| `h.warnings` | warnings from the run |
| `h.stat_calls` | every statistics call |
| `h.stale_skips` | pages skipped in stale-key mode |
| `h.log` | the raw drawing calls |
| `h.result` / `h.error` | the outcome of the last top-level call |

`reset_records()` clears the records between calls. Globals, including file-level LOCALs, persist, as on the device.

A failure raises with `e.ppl_stack`, the routine chain at the point of failure. `PPLError` is a runtime error: the device would open the Program Editor there.

## Limits (read before trusting a result)

- **Arithmetic is IEEE double:** 15-17 digits and a range of 1.8E308. The Prime uses 12-digit BCD with a range of 1E500. Compare at the displayed precision, as the example tests do.
- **Number display is approximate.** Standard format (`%.12g` with E notation) and fixed mode are modelled. The switch-over points to E notation and the minus glyph the device uses are not measured.
- **Nothing is rendered.** Text positions, fonts and colours are recorded exactly as the program passed them. Widths are estimated and pixels are not drawn. GETPIX_P returns only the grob's background. A layout bug that depends on real glyph widths needs the device.
- **Unmodelled input:**
  - a second finger, MOUSE types other than 0 and 2, and WAIT(-1) types 3/5/6/7;
  - `WAIT()` and `WAIT(0)`, which raise Unsupported;
  - key auto-repeat;
  - a touch and a key at the same instant (key polls answer nothing while a finger is down).
- **The delivery rule is a model of a patient student.** It cannot reproduce a key pressed *during* drawing unless the event says `anytime=True`. Stale-key mode is the only model of keys arriving early.
- **Name matching.** User routine names are matched case-sensitively here, while the device ignores case. Loading several files into one `Harness([...])` pools their routines, last file wins, like the device's shared pool, but case-sensitively. `fleet_names_v2.py` remains the check for collisions.
- **Not checked here; that is the gate's job (`check.sh`):** the 6-names-per-LOCAL rule, reserved and built-in names, the 16-argument limit, CHOOSE numbering, INPUT label counts.
- **Not covered:**
  - CAS commands;
  - `stddev` and `variance` (which divisor the device uses is not confirmed);
  - app settings (H1, Xmin ...: CentralLimit's Plot setup);
  - `STARTAPP` actually starting an app;
  - Python.
- Anything else the kit does not cover raises `Unsupported` rather than inventing a value.

## What it found on its first runs (16 Oct 2026)

- **StatDist v2.4**: Poisson Between with the default bounds calls `POISSON_CDF(5, -1)` (`Unverified`, in st_calc_poisson). v2.5 answers `P(0 <= X <= 9) = 0.968172`.
- **GaltonBoard beta 1a, lines 233 and 481** call `BINOMIAL(gbR, K - 1, gbP)`, which is (n, k, p). HP's help, the kit's entry and StatDist all use (n, p, k). The harness stops on `BINOMIAL(8, 0, 0.5)`, read as k = 0.5. Either the theory overlay and the tap-a-bar box are wrong on the device, or the device accepts both orders. A one-line device check settles it: `BINOMIAL(10, 0.3, 2)` should give 0.233474, and `BINOMIAL(10, 2, 0.3)` shows which reading the device takes.
- **BayesTree beta 5**: a tap with `lift=True` on a leaf opens `bt_NodeInfo`, and the lift `{2}` closes it at once. This reproduces the review's §2.A finding mechanically.
- **EpiStats v1.3**: with `stale_keys=True`, `es_WaitKey` skips page 1 of the 2×2 module on the form's left-over Enter (review §2.D). StatDist v2.5's `st_Page` holds.
- **ChiTable beta 1k**: the Examples item already opens the results, so a script for it must page through the results first. That was a scripting lesson, not a bug: the stall message named `csResults` waiting.

## Example tests

`python3 test_statdist_example.py` runs six tests on StatDist (pytest-style functions; the file also runs as a plain script):
- the Normal page, line by line, with its colours;
- Poisson Between on v2.5 and v2.4;
- the Binomial "rounded down" boxes;
- Cancel drawing nothing;
- all 17 distributions × 3 tails ending in the magenta P(...) line;
- the page surviving the form's left-over Enter.

Point `STATDIST_V25` / `STATDIST_V24` elsewhere to test other copies. It only reads the program files.

*v1, 16 October 2026. Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*

## v3 (16 Oct 2026): CAS calls answered by Giac

`ppl_run_v3a.py` answers `CAS("expression text")` with the desktop Giac (`icas`, from the
Ubuntu `xcas` package: `apt-get install xcas`). Giac is the engine inside the Prime's CAS, but
the desktop build (1.9) is newer than the Prime's, so CASProbe on the calculator still decides.

- `h.cas_calls` logs every call as `(expression, Giac's answer, ms)`.
- `STRING(CAS(s))` and `"text" + CAS(s)` give Giac's answer as text; a Giac string
  (`string(...)`) comes back without its quotes.
- A Giac answer containing `Error:` raises a runtime error, so the program's `IFERR` runs.
  `undef` comes back as the text "undef" -- the program's call routine must reject it.
- `Harness(path, cas='fail')` makes every CAS call fail, to test the decimal fallback.
  `Harness(path, cas={'expr': 'answer'})` gives canned answers.
- A CAS result used in arithmetic is not covered: programs keep CAS answers as text.

## v3b (17 Oct 2026): the CAS as the calculator answers it

`ppl_run_v3b.py` replaces v3a's CAS model with the one CASProbe beta 1a and 1b measured on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09, 17 Oct 2026; `Emulator_Round1_Results_2026-10-17_v1.md`). Under v3a a program's `STRING(CAS(s))` worked from a variable and big integers stayed exact, so a harness pass on CAS code proved less than it seemed. Everything else is v3a's.

**What the harness now does with CAS:**

| The program writes | v3b hands back | Emulator evidence |
|---|---|---|
| `CAS(s)`, s a variable, a parameter or a concatenation | the PPL string `s` itself, **unevaluated** (logged as such, plus one warning naming the fix) | T06, T07 |
| `CAS("literal")` in the source, or `EXPR("CAS(" + CHAR(34) + s + CHAR(34) + ")")` | Giac's answer | T04, T08 |
| `EXPR("CAS.eval(" + q + s + q + ")")`, `EXPR("CAS.name(args)")` | Giac's answer (the kit's parser cannot read these; EXPR does it) | T09, T10 |
| an answer that is a CAS string (`string(...)`) | a **PPL string** (TYPE 2): `STRING()` of it adds quotes, `"" +` does not | T12 |
| a non-string integer of more than 12 digits | a **real**: `1.00891344546E29` | T04, T08 (beta 1a) |
| any other answer | a CAS object (`CasResult`, TYPE 8), printed as the Prime prints it | T05 |
| a syntax error | a run-time error (`PPLError`), which IFERR catches. Desktop Giac says "syntax error" on stderr; v3b reads stderr | T26 |
| `name := value` inside CAS text | evaluated, **kept** (replayed before every later call) until `purge(name)`; listed in `h.cas_vars`, with a warning | T25 |

**The Prime's printing** (`prime_print`, applied to every answer, inside strings too):

| Desktop Giac 1.9 | v3b (the Prime) | Evidence |
|---|---|---|
| `exp(u)` | `e^(u)`; `(e^(u))` when a `^` follows (`exp(1)^4` → `(e^(1))^4`), so the text reads back with the same meaning | T17, T40 |
| `sqrt(2)`, `sqrt(u+1)` | `√2` (an atom), `√(u+1)`; bracketed when a `^` follows | T14b, T21a |
| `list[1/20]`, `list[[2,1]]` | `{1/20}`, `{[2,1]}` | T18, T36 |
| `+infinity`, `-infinity` | `∞`, `-∞` | T41 |
| `infinity` (unsigned, 1/0) | `±∞` | T27 |

Measured to print alike, and left alone: seq and matrices in `[]`, products with `*`, `undef`, evalf to 12 significant digits, an unknown function handed back unevaluated, `order_size` in a series.

Not measured, and modelled as above only to keep the text re-readable: `(e^(1))^4`. The Prime may print `e^4`. Programs check CAS answers by value, so this does not matter to them.

**New options and records:**
- `Harness(..., home_minus=True)`: `STRING()` of a negative real starts with U+2212, as on the calculator (T01). Off by default, because fleet verify scripts read screen text with hyphens. The CAS reads U+2212 as a minus (T31b), and v3b translates it before Giac sees it.
- `h.cas_calls` holds `(expression, Prime-printed answer, ms)`. `h.cas_desktop` holds `(expression, desktop Giac's raw answer)`. `h.cas_vars` lists CAS variables assigned and not purged.
- `prime_eval(expr)` is `giac_eval` with the Prime's printing. Verify scripts use it to read a template as the calculator would.
- `cas='fail'` and canned answers (`cas={'string(...)': '"answer"'}`) work as in v3. A canned answer is taken as the Prime prints it. The key is the text the program sends, which is `string(...)` under the BRIEF_CAS_v2 kit.

**CASProbe beta 1b in v3b.** `out/run_CASProbe_beta1b_v3b.py` runs the probe exactly as on the emulator, with the Python blocks in CPython and `cas.caseval` modelled on its emulator answer.
- With `home_minus=True` (`--minus`), it gives the emulator's summary exactly: **CAS available yes, form 2, 42 pass, 8 fail, 19 values, 0 errors**. The fails are T01, T04, T05, T06, T07, T10, T32 and T34a.
- Without `--minus`, T01 passes (43 / 7 / 19).
- The emulator log gave only the totals, so the per-test list is the harness's reading. It agrees with every per-test fact in the results file.

**The fleet on v3b.** The twelve round-2a programs (the BRIEF_CAS_v2 kit) pass their verify scripts in v3b with the CAS on and with `cas='fail'`. Each round-2 file run in v3b reproduces the emulator's finding: no exact line anywhere, or its own text shown as an answer.

*v3b, 17 October 2026. Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*

## v3c (17 Oct 2026): WAIT(-1) taps and the whole-number-df built-ins, as the emulator answered

`ppl_run_v3c.py` is v3b plus what the first emulator round measured (HP Prime Virtual Calculator 2.4.2, build 2026-09-09, the fleet's firmware; `Emulator_Round1_Results_2026-10-17_v1.md`). Under v3b, BayesTree beta 7/8a's and StudRange beta 15's soft keys passed and StatDist v2.7a's fractional chi-square ran; on the emulator all three failed. Under v3c they fail here too, and their fixed versions pass.

### F1: how a tap reaches WAIT(-1) (MenuTapProbe beta 1)

| What the script does | v3c, `wait_model='device'` (the default) | v3b (`wait_model='v3b'`) |
|---|---|---|
| `tap(x, y)` with y >= 218 while a DRAWMENU strip is on the screen | **only** `{3, x, y}` (type 3, a click): no press, no lift | `{0, x, y}` (then `{2}` with `lift=True`) |
| `tap(x, y)` anywhere else | `{0, x, y}`, then `{2}`, then `{3, x, y}` | `{0, x, y}` (then `{2}` with `lift=True`) |
| `tap(x, y)` with y >= 218 and **no** strip on the screen | `{0}`, `{2}`, `{3}` like any tap, plus one warning: **not measured** | as above |
| `drag(points)` | `{0, x0, y0}`, `{1, x, y}` per point, `{2}` (no click; WaitLab) | the same |
| a key | its code | the same |

- "A strip on the screen" means DRAWMENU was the last thing drawn on G0: a `BLIT_P` to G0, `DIMGROB_P(G0, ...)` or a clear of G0 paints over it.
- In device mode a `Tap` always lifts: `lift` and `hold` no longer change what WAIT(-1) sees. A finger that stays down is `Drag([(x, y)], lift=False)`.
- `MOUSE`, `MOUSE(1)` and `GETKEY` are unchanged: a program that polls them sees a soft-key tap like any other tap (ChiTable, G2 and G1).
- `mouse_tail=True` (off by default): a tap that a program read through `MOUSE` **also** leaves its `{2}`, `{3, x, y}` (or just `{3, x, y}` on the strip) for the next `WAIT(-1)`. This is **not measured**; it is a worst case for testing a program's guard against stale clicks (BayesTree beta 8b and StudRange beta 15a keep a list of taps whose click may still come).
- **Run against MenuTapProbe beta 1** (tap on soft key 2, a tap on the screen, Esc): v3c gives `{3,78,230}`, `{0,161,115}`, `{2}`, `{3,161,115}`, key 4 -- the emulator's record exactly. v3b gave `{0,78,230}`, `{0,161,115}`, key 4.
- Not modelled: WAIT(-1)'s values are whole numbers on the calculator (`#3C:-16h`), so `STRING()` of one prints hex; here they are reals.

### F3: the built-ins that take whole-number df only (GfxProbe beta 1 T11, T12 and the Home checks)

| Call | v3c | Emulator |
|---|---|---|
| `CHISQUARE_CDF`, `CHISQUARE_ICDF`, `FISHER_CDF`, `FISHER_ICDF` with a non-integer df | a run-time error, `PPLError("... Invalid input ...")`; IFERR catches it, as on the calculator | "Invalid input" (`CHISQUARE_CDF(2.5, 3)`, `FISHER_CDF(2.5, 7.5, 2)`, both ICDFs) |
| `POISSON_CDF(mu, k)` with k < 0 | `PPLError` "Invalid input" | "Invalid input" for k = -1 and -0.5 |
| `CHISQUARE(df, x)`, `STUDENT`, `STUDENT_CDF`, `STUDENT_ICDF` with a non-integer df | SciPy's value, **no warning** now | matched SciPy to 12 digits at df 2.5 |
| `FISHER(d1, d2, x)` (the density) with a non-integer df | SciPy's value and a warning: not measured | not among the checks |
| `POISSON_CDF(mu, k)` with a fractional k >= 0, the 3-argument form with k < 0 | `Unverified`, as in v3b | not measured |

The values the harness gives match the emulator's table: `CHISQUARE_CDF(3, 3)` 0.608374823729, `CHISQUARE(2.5, 1)` 0.281348225763, `STUDENT_CDF(2.5, 1)` 0.797969486361, `STUDENT_ICDF(2.5, 0.9)` 1.7302509288, `STUDENT(2.5, 1)` 0.200795960671.

### Drawing (GfxProbe beta 1)

- `FILLPOLY_P` (both point-list forms, with or without alpha), the one-colour, three-colour and alpha `TRIANGLE_P`, and the 10-argument scaled `BLIT_P` passed T01-T06 and T08 on the emulator: **no warning** now. (Still emulator-only: they have not run on a G1 or G2.)
- `TRIANGLE_P` with a matrix argument (the 3-D mesh form) warns: T07 drew nothing.
- `ARC_P` with r <= 3 gives **one warning per run**: T09 showed that ARC_P at r = 3, 2, 1 plus the centre pixel, drawn as a solid dot, leaves white holes on the diagonals. Fill a dot with `RECT_P` bars or `FILLPOLY_P` instead (GaltonBoard beta 3b, TrendTest beta 3b).

### Which programs this changes

- Fail in v3c as they failed on the emulator: BayesTree beta 8a (soft keys do nothing), StudRange beta 15 (plot soft keys do nothing), StatDist v2.7a (Chi-square or F with df 2.5 stops with "Invalid input").
- Pass in v3c: BayesTree beta 8b, StudRange beta 15a, StatDist v2.7b (their `verify_*.py` run in v3c and include these checks).
- Unchanged: programs that poll `GETKEY` + `MOUSE` (every other fleet program) and programs whose df are whole.

### Using it

`from ppl_run_v3c import Harness` (it sits in `out/` beside this README). Options added: `Harness(..., wait_model='device' | 'v3b', mouse_tail=False)`. Everything else is v3b's.

*v3c, 17 October 2026. Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*

## v3d (17 Oct 2026): the string findings of the second emulator round

`ppl_run_v3d.py` is v3c plus what was typed in Home on the emulator in round 2 (`Emulator_Round2_Results_2026-10-17_v1.md`):

- `INSTRING("", sub)` is a run-time error, "Invalid input" (a `PPLError`, which IFERR catches). v3a-v3c returned 0, so a replace loop that searched what was left of a string, and every `xxCas` that tested `INSTRING(cR, "undef")` after a failed call, passed here and stopped TrendTest's and ScatterLab's CAS pages on the emulator. `INSTRING("abc", "")` = 1, `INSTRING("abc", "z")` = 0.
- `STRING(x, 2, d)` (fixed decimals) prints the **scientific** form when 0 < |x| < 10^-d, with U+1D07 (the small capital E) for the E: `STRING(0.096, 2, 1)` = `9.6ᴇ-2`, `STRING(0.0004, 2, 3)` = `4.000ᴇ-4`. 0.1 with d = 1 and 0.001 with d = 3 stay fixed; `STRING(0, 2, 3)` = `0.000`. From 1E12 it is scientific too, and fixed output holds at most 12 significant digits. Each scientific result is logged in `h.sci_strings` as (value, digits, text), with one warning per run, so a verify script can list every such display. `STRING(ROUND(x, d), 2, d)` is the safe form.
- Measured again, already in the kit: `LEFT(s, 0)` and `RIGHT(s, 0)` are the whole string; `MID(s, 0, n)` is "Bad argument type"; `MID("", 1, 1)` and `MID(s, past the end)` are `""`.

## v3e (17 Oct 2026): Home's minus before a scientific exponent

**17 Oct 2026, v3e:** with `home_minus=True`, the scientific form of `STRING(x, 2, d)` now has U+2212 (Home's minus, code 8722) before a negative exponent, not the ASCII hyphen: `STRING(0.096, 2, 1)` = `9.6ᴇ−2`, codes 57 46 54 7431 8722 50. That is what CASProbe beta 1c's T43b logged on the emulator (build 2026-09-09); v3d printed 45 there, so beta 1c's T43b passed here and failed on the emulator. A negative mantissa already had U+2212 under `home_minus` (v3b, CASProbe T01's `STRING(-2.5)`).

- `home_minus` still defaults to **False**: the fleet's verify scripts read screen text with hyphens, and only `verify_CASProbe_*` turns it on. With it off, v3e prints exactly what v3d printed.
- `h.sci_strings` and the run's one warning keep the hyphen form, as in v3d, so a list of scientific sites reads the same with `home_minus` on or off.
- Not changed, and not measured on the emulator: `STRING`'s Standard (mode 1) and Scientific (mode 3) forms still write an ASCII `E` and hyphen.
- **Regression.** Of the 15 verify scripts that import v3d, 14 give the same results when pointed at v3e; only PC timings differ. The 15th, `verify_CASProbe_beta1c.py`, now sees beta 1c fail T43b, as the emulator did, so 5 of its checks fail. `verify_CASProbe_beta1d.py` replaces it. `CASProbe_beta1d_CHANGES.md` has the run.

`from ppl_run_v3e import Harness` (it sits in `out/` beside this README). No option was added; everything else is v3d's.

*v3e, 17 October 2026. Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
