# HP Prime statistics

Teaching programs for the HP Prime graphing calculator, written in PPL and MicroPython, and originally intended for upper-level university statistics courses.  

**And a set of notes on what the Prime actually does**, as opposed to what the manual says — hard limits, commands that behave differently than documented, the MicroPython bridge and how it fails. Those notes are not specific to statistics; if you write PPL for anything, [docs/lessons-learned.md](docs/lessons-learned.md) is the part worth your time.

Everything here is **free for educational and personal use**. See [LICENSE](LICENSE).

**Tested on** an HP Prime G2 and G1, both running the **2026-09-09** firmware, plus the desktop Virtual Calculator.

---

## Installing

Every program is a plain `.txt` file, on purpose.

1. Open the **HP Connectivity Kit** and connect your calculator.
2. Create a new program in the Program Catalog.
3. Open this repository's `.txt` file in any text editor, select all, copy.
4. Paste into the Connectivity Kit's program editor, and sync.

**Do not rename the file to `.hpprgm`.** That format is binary — UTF-16LE with a header — and a `.txt` renamed to it will not import. Pasting is the reliable route.

The MicroPython inside `StudRangePy` and `NormExplorer` lives in a `#PYTHON … #END` block inside the program file. There is **no separate `.py` file**, and nothing goes into the Python app. If you have Python firmware (2.1.14567, April 2021, or later) it runs; if not, the programs fall back to pure PPL automatically.

---

## The programs

### NormExplorer — normal distribution workbench
A ten-item menu covering the normal distribution: set any μ and σ, four kinds of probability question, three kinds of inverse question, a z-formula solver, a live explorer you can drag with your finger, Cohen's d, a standardize animation, and a diagnostics page.

It also reads **your own data**. It will take a list from the Statistics 1Var app and fit a curve to it, take two groups from Statistics 2Var and give you a pooled-s Cohen's d, run regression residuals through the normality view, and write z-scores back where other apps can reach them.

### StudRange — studentized range (Tukey's q), in PPL
P-value from q, critical value from α, Tukey HSD, and an interactive distribution plot with a five-rung α ladder. Tap or drag the plot to move the observed q.

Descends from a 1977 FORTRAN IV subroutine (Dunlap, Powell & Konnerth, *Behavior Research Methods & Instrumentation* 9(4):373–375), with native distribution functions replacing their polynomial approximations and a u² substitution added for low degrees of freedom — a case the original paper explicitly excluded.

Requires df ≥ 3.

### StudRangePy — the same thing in MicroPython
Same algorithm, same answers, roughly forty times faster on critical values: about 1.5 seconds against about a minute. Handles df ≥ 1. Requires Python firmware.

Accuracy against `scipy.stats.studentized_range`: p-values under 1×10⁻⁷ relative, critical values under 1×10⁻⁶.

### BayesTree — natural-frequency Bayes tree
A diagnostic-testing tree: N people split by prevalence, then by the test. PPV read off the tree rather than computed from a formula. ROC view, PPV-versus-prevalence curve, 2×2 table, and a diagnostics panel with Youden's J, NND, diagnostic odds ratio, F1, MCC and Cohen's κ.

**Tap any node** for an explanation of that count — what it is, the formula behind it, and which pair it belongs to.

---

## Diagnostics

Short throwaway programs for finding out what your own calculator does.

**`PyVer`** is the useful one. It reports your MicroPython version, probes ten modules, and tests two behaviours known to vary. Two minutes, and it tells you more about your firmware's Python than any document can.

`JoinTest` and `GenTest` isolate a specific `str.join` failure — kept because they document a real investigation, including the part where it did not reproduce.

---

## The notes

[**docs/lessons-learned.md**](docs/lessons-learned.md) is the substantial document here: everything found the expensive way across roughly forty build iterations on real hardware. Hard limits, command behaviour that contradicts the manual, graphics and input idioms, the MicroPython bridge, numerical methods, and a list of disproved theories recorded as disproved. The lessons learned document can be uploaded to your favorite AI to assist with coding.  

A few things from it that are hard to find elsewhere:

- **The Prime runs MicroPython 1.9.4**, a December 2018 release tracking CPython 3.4. Check *those* docs, not the current ones. This single fact explains most of the surprises.
- **A Python exception does not raise a PPL error.** The traceback goes to the Terminal and PPL carries on with whatever the bridge variable held before. `IFERR` around `PYTHON(...)` catches nothing. In this fleet a sampler failed on every run for eleven consecutive builds with nothing on screen to show it.
- **`FREEZE` is not a pause.** It suppresses the screen refresh at program *end*. Mid-program it does nothing.
- **`STRING(x, 1, digits)` ignores the digits argument.** Mode 1 is Standard. Fixed decimals need mode 2.
- **Data columns are reachable from a standalone program; app settings are not.** `D1`, `C1`, `C2` can be read and written. `H1Type` and `SetSample` are a syntax error at paste time.
- **The desktop emulator runs the real ROM**, so any difference you see on hardware is necessarily timing, memory or display — and no amount of further emulator testing will find it.

---

## Credit

Concept, direction, classroom judgement and all hardware testing: **Roger Metcalf**, 2026.

Dozens of community PPL programs from various HP-related forums were read as reference while working out how the Prime actually behaves — several entries in the notes exist because a corpus program showed a construct working that the manual does not describe. None of those programs are reproduced here.

Implementation, numerical work and documentation: written, expanded, and vastly improved with incredible and amazing AI assistance from Anthropic Claude--mostly Opus 5 and Fable 5.1.  Much of the notes and the user's guides were essentially written by Claude.

The studentized range algorithm is after Dunlap, Powell & Konnerth (1977). Accuracy figures were verified against SciPy. Several MicroPython findings credited in the notes come from [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit), measured independently on a different G2.

Corrections and reproductions are welcome. Where a claim here is unverified, it says so.
