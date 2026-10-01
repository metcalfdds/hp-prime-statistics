# MicroPython on the HP Prime

## What actually breaks, and what to do about it

*Field notes to accompany the Norm Explorer program and user's guide*

## Why these notes exist

The HP Prime has run MicroPython since firmware 2.1, and almost nobody writes about it.

That is measurable rather than impressionistic. In a working library of 83 HP Prime programs collected from the community, exactly **one** uses the Python bridge. Of 54 reference documents — the User Guide, a 46-page programming tutorial, a 24-page advanced workshop, a 14-page PPL guide, 64 pages of AP statistics materials — exactly **one** covers Python, and it is a 7-page personal page whose author opens by saying that official documentation for Python programming on the Prime is yet to be written, and that what follows was learned through googling and a good bit of trial and error. The User Guide bundled with most installations predates the feature entirely.

So the failure modes below were found the expensive way, on hardware, while building a statistics teaching program. They are written down here because none of them announces itself, several are silent, and one of them hid for eleven successive builds.

Everything that follows was observed on a physical G1 and G2. Where something is inferred rather than observed, it says so.

## Getting Python code onto the calculator

The question asked most often is not about any of the failures below. It is how to get a Python program running at all, and nothing HP ships answers it.

**Check the firmware first.** Python arrived in firmware **2.1.14567**, April 2021, for both the G1 and the G2 — worth stating precisely, because 2.1.14181 is sometimes quoted and that build is from November 2018 and has no Python at all. It was the last major update *before* Python, during the stretch when the Prime had fallen out of step with the French curriculum's move to Python. Check Help → Tree → About, or press **Apps** and look for a Python icon. If it is not there, the fix is a firmware update, not a setting. Both calculators behind these notes run Python, and the sampler described below runs on each.

There are then **two entirely different routes**, and confusing them is the support question.

### Route A — Python inside a PPL program

This is the route to use for anything you share. The whole program is one text file, with the Python sitting in a `#PYTHON name … #END` block and a short PPL wrapper underneath:

```
#PYTHON pyname
print("hello from Python")
#END

EXPORT Hello()
BEGIN
  PYTHON(pyname);
END;
```

It installs exactly as any PPL program does — paste it into a new program in the Connectivity Kit and sync — and it then appears in the Program Catalog (**Shift 1**) under its EXPORT name. That is `Hello`, not `pyname`: the name after `#PYTHON` is internal. **There is never a separate `.py` file**, and the user need never open the Python app. If you import the `.txt` file instead of pasting it, the Kit can leave a few stray CJK characters at the very end; delete them.

Every Python program distributed with these notes, `PyVer.txt` included, is built this way, and it is the reason "how do I install a Python program" has not come up once with them — Route A makes the question disappear. For anything classroom-facing, or anything you hand to someone else, use it.

### Route B — a standalone script in the Python app

For a script that is Python from top to bottom. Press **Apps**, open Python, press **Save** and give the copy a name. On the calculator, **Symb** opens the editor and **Num** runs the scripts and shows the Terminal; from the Shell, `import filename` runs one too.

`.py` files do **not** appear in the Program Catalog. They live in the Python app's own file list. This is the single biggest source of confusion: people sync a `.py`, look in the Program Catalog, find nothing, and conclude the transfer failed.

To load a `.py` file from a computer, open the Connectivity Kit, expand the calculator's Application Library, find your app, right-click its Files folder and choose **Add file**. The app then launches from the Apps screen like any other. *(That loading step is the standard documented route rather than something verified here — nothing in this bundle ships that way.)*

### Which to choose

Route A is one file and one paste, launches like every other program, and lets PPL keep the interface and graphics while Python does the arithmetic — the arrangement the rest of these notes are about. It is also the honest answer to "how do I give a Python program to someone who has never opened the Python app": you hand them one `.txt`, and it behaves like a normal Prime program. Route B suits stand-alone scripts.

### Before the first run

**`print()` and `input()` use the Terminal**, and `input()` echoes nothing — no characters, no newline — so print the user's entry back yourself. Output and tracebacks both land there: Shift-View.

**A Python error never raises a PPL error.** Its traceback goes to the Terminal and the program carries on. A Route A program needs the clear-then-validate pattern below; in Route B the Shell prompt simply returns as though nothing happened. If something appears to do nothing, the reason is in the Terminal.

**Paste, do not retype.** Indentation survives a paste into the Connectivity Kit; hand entry on the device invites a tab-and-space mismatch that is miserable to find on a 320×240 screen.

**The desktop emulator hides hardware differences.** Any new Python path gets tested on real hardware with the Terminal open — see the join episode further down for what that costs when skipped.

The quickest way to confirm a calculator is ready is `PyVer.txt`: paste it in, run it, and it reports the interpreter version and module list on the Terminal.

## Two shapes for an embedded program

Both appear in the wild, and they suit different jobs.

**Python as the whole program.** The PPL side is a three-line launcher; everything happens in Python, with `print()` and `input()` to the terminal. The one community program found using the bridge takes this route:

```
#PYTHON main
import hpprime
...
main()
#END

START()
BEGIN
  PYTHON(main);
END;
```

**Python as a compute kernel.** PPL owns the program, the interface and the graphics; Python is called for one expensive loop and hands back a small result. This is the better fit when the program is interactive, because PPL's `_P` graphics and key handling have no Python equivalent worth reimplementing.

The kernel pattern needs a bridge. There is only one mechanism: named PPL globals, read and written from Python through `hpprime.eval`.

```
EXPORT NEpmu, NEpsg, NEpn, NEpout;   // PPL side: declared globals

// PPL writes the inputs, calls Python, reads the output
NEpmu := 100; NEpsg := 15; NEpn := 5000;
PYTHON(SAMPBINSPY);
result := NEpout;
```

```
from hpprime import eval as ppl        # Python side
mu = float(ppl("NEpmu"))
n  = int(ppl("NEpn"))
...
ppl("NEpout:={" + out + "}")           # assignment, as a string
```

**If you have read that this cannot work.** The 7-page write-up mentioned at the start reports that PPL's `EXPORT` variables do not seem reachable through `hpprime.eval()`, and that only variables belonging to an app can be exchanged. On the calculators behind these notes they are reachable: the bridge above uses nothing but exported globals, and it has run on both a G1 and a G2. That write-up was based on firmware from 2023, so the difference may be version-dependent. If the bridge fails on your calculator, record the firmware you are running.

Two rules that matter more than they look:

**Never cross the bridge inside a loop.** Each `hpprime.eval` is expensive. Pass the inputs once, return a fixed-size result once. A sampler returning 34 numbers costs the same whether n is 200 or 5000; one returning n values does not.

**The return trip is a string you build.** Python assembles PPL source text and has PPL execute it. That is where most of the trouble lives.

## When it is worth crossing the bridge

The hazards below are only worth accepting when the speed-up is real. Here is a measured case.

**StudRange** computes the studentized range distribution — Tukey's q, and the HSD post-hoc test that depends on it. It began as a 1977 FORTRAN IV subroutine (Dunlap, Powell & Konnerth, *Behavior Research Methods & Instrumentation* 9(4):373–375), which hand-rolled the normal CDF with Abramowitz & Stegun 26.2.17 polynomials because that is what you did before native distribution functions existed. It was ported to PPL, then given a MicroPython twin running the same algorithm.

On G2 hardware, same math, same accuracy:

| Computation | PPL | MicroPython |
| --- | --- | --- |
| p-value (q=5, k=5, df=15; double Simpson, \~6300 nodes) | ≈ 1 s | near-instant |
| critical value (secant, \~9 chained CDF evaluations) | \~1 minute (60-step bisection) | \~1.5 s |

Accuracy was verified against `scipy.stats.studentized_range` before either version went near the calculator: relative error 8×10⁻⁸ on the p-value, under 10⁻⁶ on the critical value.

The reason is straightforward. Python's `math` primitives are compiled C; PPL loops are fully interpreted. The gap widens with the number of function evaluations, which is why quadrature and root-finding benefit most.

There is a second gain that is easy to overlook: **native `erf` and `lgamma`**. PPL has no `LNGAMMA` outside the CAS, so the PPL version carried a hand-written Lanczos approximation that the Python version simply deletes. Less code, and one fewer thing to get subtly wrong.

The counter-example matters as much. A live power visualiser in the same fleet — four tests, held-key stepping through `ISKEYDOWN`, α, β and power regions reshaded on every frame — gains nothing from Python and was deliberately left in PPL. Its arithmetic is a handful of normal CDFs per redraw; the bridge crossing would cost more than the computation. The same held for every other interactive tool reviewed: the explorers, the tree, the 2×2 calculators.

One program in that fleet was worth converting. Eight were not.

**The resulting rule:** compute-heavy engines — quadrature, root-finding, simulation — default to Python. PPL keeps the live `_P` graphics and keypress redraw loops, where crossing the bridge per frame would cost more than the computation saves.

Worth noting what this means in practice: a 1977 FORTRAN subroutine now runs, unrecognisably faster, on a MicroPython interpreter inside a pocket calculator.

## The one that matters: Python failures are silent

**A Python exception does not raise a PPL error.**

The traceback prints to the Terminal — which nobody is looking at — and PPL carries straight on with whatever value the bridge variable happened to hold. `IFERR` around `PYTHON(...)` catches nothing, because from PPL's point of view nothing went wrong.

The consequence in practice: if the program has any fallback, the fallback runs, the result looks correct, and the only symptom is that it took longer. That is indistinguishable from success.

In the program these notes come from, the Python sampler failed on every single run for **eleven consecutive builds**. Every histogram was drawn by the slow PPL fallback. The output was correct each time. The statistics were correct. Nothing on screen suggested a problem. It surfaced only when the author happened to open the Terminal on a physical calculator and saw a traceback scroll past under a feature that appeared to be working perfectly.

The lesson is not "be careful". It is that this class of bug cannot be found by testing whether the program works, because it does work. It has to be found by checking the Terminal deliberately, or by building the check into the program.

## Three things that break

All three are consequences of the interpreter's age. The Prime reports MicroPython **1.9.4**, a December 2018 release tracking CPython 3.4 — so the reference to check is the 1.9.4 documentation, not the current one.

### `random` may not exist

`import random` raises `ImportError` on the calculator, and a module probe pins down the scope. Of `math`, `cmath`, `random`, `urandom`, `hpprime`, `arit`, `linalg`, `matplotl`, `time` and `gc`, only **`random` and `time` are absent**.

Note that **`urandom` is present**. `urandom.getrandbits()` is the natural random source on this firmware; the fallback below matters only if you want code that also runs on builds lacking both.

The workaround is a self-contained generator seeded from PPL's own `RANDOM`:

```
try:
    from random import random as _rand
except ImportError:
    _state = [0]
    def _seed():
        sd = 0
        for _ in range(3):
            sd = (sd * 65536 + int(float(ppl("RANDOM")) * 65536)) & 0xFFFFFFFF
        _state[0] = sd or 2463534242
    def _rand():
        st = _state[0]
        st ^= (st << 13) & 0xFFFFFFFF
        st ^= st >> 17
        st ^= (st << 5) & 0xFFFFFFFF
        _state[0] = st
        return st / 4294967296.0
    _seed()
```

This xorshift32 is ample for classroom simulation — a 5000-draw normal sample built on it returned a mean of 100.03 and an SD of 14.85 against a target of N(100, 15).

### A `join` failure that will not reproduce

This one is recorded as unexplained, because that is what it is.

During development the bridge line raised `TypeError: join expects a list of str/bytes objects consistent with self object` on a G2 — on every run, for eleven consecutive builds, while the PPL fallback quietly produced correct histograms. Replacing `join` with plain concatenation fixed it, and the MicroPython sampler has run correctly on both a G1 and a G2 ever since.

Afterwards, with the calculator to hand, the failure would not reproduce. `join` was tested directly on that same G2 with string literals, `str(int)` results, a list comprehension, `%`-formatted floats, `repr(float)`, `str(float)`, the exact mixed list the sampler had built, a generator expression without brackets, and a tuple. **Every one passed.**

So the honest state of it: something in that code path genuinely failed, repeatedly, and nothing tried since has reproduced it. A stale copy of an earlier build still resident on the calculator is the least unlikely explanation — duplicate program copies had already caused one confusing error in the same project — but that is a guess, not a finding.

What survives is practical rather than diagnostic. Build hand-off strings by concatenation:

```
out = ""
for c in cnt:
    out += str(c) + ","
```

It costs nothing, and it is immune to whatever this was.

### `repr()` on floats can produce unparseable text

The return trip is PPL source code, so anything Python emits must be text PPL can read back. `repr()` may produce exponent notation. Use fixed-point formatting:

```
out += "%.6f" % total          # not repr(total)
```

`%`-formatting works. So does `math`, and `cmath`. One community program imports `gcd` from a module called `arit`, which is not standard MicroPython — the Python app's CMDS menu is the authoritative list of what a given firmware actually provides.

## The defensive pattern

Three habits follow from the silent-failure problem. Together they turn an invisible fault into a visible one.

**Clear the output variable before calling Python.** Otherwise a failed run leaves the previous run's value in place, and the program happily uses stale data.

**Validate by using the result, not by asking its type.** Reading the last element inside `IFERR` proves the value came back, is a list, and is long enough — in one step, with no assumption about type codes:

```
NEpout := 0;                       // nothing carried over
IFERR
  PYTHON(SAMPBINSPY);
THEN
END;
ok := 0;
IFERR
  chk := NEpout(NBINS+2) + 0;      // if this reads, the bridge worked
  ok := 1;
THEN
  ok := 0;
END;
IF ok == 1 THEN
  bins := NEpout;
ELSE
  bins := SampBins(...);           // pure-PPL fallback
END;
```

The earlier version of this checked `TYPE(NEpout) == 6` for a list. That works, but it adds an assumption about firmware type codes, and if the assumption is ever wrong the program silently uses the slow path forever. Reading the value is both simpler and self-proving.

**Always write the fallback.** Every bridged routine should have a pure-PPL twin. It is slower, and it is the difference between a program that degrades and a program that fails in front of a class.

**Then report which one ran.** A one-screen diagnostics page naming the sampler that actually produced the last result — and probing the bridge live with a trivial call — would have caught the eleven-build bug the first time anyone looked at it. Any program that crosses the bridge should carry one.

## Three more ways an app dies without saying anything

These come from JordiRigau/hp-prime-kit, measured on a different G2 at firmware 2.4.15515. They are not our findings and we have not reproduced them — but they share the character of everything above, so they belong here.

**A PPL list containing a string, returned raw to Python, closes the app.** No exception, no message, no trace. A function returning eight numbers and a text warning at the end was enough. Never let the raw list out: wrap the call in PPL and allow only numbers through, taking the elements one by one into a fresh list. The same applies to MOUSE, which returns lists inside lists. If a PPL function will be called from Python, design it from the start to return a flat list of numbers, or a single number.

**A top-level import of a module MicroPython lacks closes the app on startup.** Imports inside a function do not count. Delete **pycache** before packaging too — CPython bytecode MicroPython cannot read.

**A quote inside a string concatenated into an eval expression breaks it.** Clean before building: replace any double quote with a single one.

### The answer to a silent close

When the app vanishes the screen is gone and nothing is logged — but a PPL global survives it. Write progress markers from Python into a global, wrapped in try/except so the marking itself cannot fail. Then go to Home, type that variable's name, press Enter: it says how far execution got.

hp-prime-kit used this to isolate the list-with-string crash in a single pass, probing in order of increasing risk, so that the point of death named the cause with no further experiments.

That is the same instinct as the diagnostics page described earlier, applied to a harder failure: when the system cannot tell you what went wrong, arrange for it to leave something behind that outlives the crash.

### Correcting the cost model

hp-prime-kit measured a bridge crossing at about 0.2 ms, thirty to forty lookups at around 8 ms, and concludes there is nothing to optimise — cross as often as the clear code wants.

That is a fair correction to the rule stated more absolutely above. The real constraint is per-pixel work: 272 columns times two crossings a frame is roughly 109 ms, which a live redraw will feel. Cross freely for tens of lookups; keep crossings out of pixel loops; keep a returned payload fixed-size.

## The emulator will not catch these

The desktop Virtual Calculator runs the real ROM, so the language behaves identically. That makes it excellent for syntax, structure and logic — and useless for this particular class of bug.

The reason is speed. When the Python path failed and the PPL fallback took over, the desktop machine completed the fallback fast enough that nothing looked wrong. On the G2 the same failure was visible as a delay. The emulator did not behave *differently*; it was simply too fast for the symptom to register.

The same applies to two other things it cannot tell you: whether a program is stable under a real memory ceiling — one unexplained reboot occurred on a G2 after a Python run and has not reproduced since — and how anything actually looks at device scale.

A practical consequence: since the ROM is identical, *any* difference you observe between emulator and hardware is necessarily a timing, memory or display effect, and therefore something no amount of further emulator testing will find.

## What is still unknown

Three things I could not settle at first. The first has since been answered; the other two are offered in case someone reading this can.

**~~Which MicroPython version.~~ Answered.** `sys.implementation` on a G2 running the 2026-09-09 firmware reports **MicroPython 1.9.4**. The documentation for that release was last updated in December 2018, and the MicroPython of that era tracks CPython 3.4 — a language version from 2014.

That single fact explains most of this document. The missing `random`, the `join` that rejects a list of plain strings, the absence of f-strings: none of these are HP peculiarities. They are the behaviour of an eight-year-old interpreter, and several were fixed upstream years ago. The practical rule that follows is simpler than a list of workarounds — **write for MicroPython 1.9.4 and check its documentation, not the current one.**

**The reboot.** One G2 rebooted after a Python sampler run, once, and has not reproduced across many subsequent runs. Cause unknown. Recorded here as unresolved rather than fixed, because an intermittent fault that has been seen once is not the same as one that has gone away.

**App variables from outside their app.** `D1`, `C1` and `C2` are global and readable from any program. `H1Type` and `SetSample` are not: referencing them from a standalone program is a syntax error at paste time, not a run-time error `IFERR` can catch. HP's own DiceSimulation example in the User Guide uses both, but that example lives inside a Statistics-derived app where the names are in scope. The User Guide documents qualifying a variable as `Function.Xmin`; whether an equivalent form exists for a two-word app name, I could not determine.

## Basis

Everything above was observed while building a normal-distribution teaching program, over roughly forty build iterations, on a physical HP Prime G2 and G1 plus the desktop Virtual Calculator. Both calculators now run the **2026-09-09 firmware**; the G1 observations recorded here were made before it was updated to that build. Findings marked as observed were reproduced on hardware. Findings marked as inferred are labelled as such in the text.

The firmware matters more than it might appear. Two of the findings here — which characters render, and which app variables a standalone program can reach — have turned out to be firmware-dependent, and the missing `random` module may well be too. Anyone reproducing this should record their own version alongside their results.

**Credit.** The programs these notes came out of are Roger Metcalf's — his concept, his direction, and his testing on real calculators, which is where every finding above was actually caught. Claude did the implementation and wrote this up. Corrections are welcome, and the reproducible one-line tests matter more than the anecdotes: anyone with a Prime can check the module list and the `join` behaviour in about two minutes.

`PyVer.txt`, distributed alongside these notes, does exactly that — paste it in, run it, read the Terminal. It reports the interpreter version, the module list, and two behaviour tests.

**Free for educational and personal use.** Share these notes, teach from them, quote them with attribution. Not for sale or commercial redistribution. Provided as is — everything here is one person's findings on two calculators, not a specification.

© 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).
