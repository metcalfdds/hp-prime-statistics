# HP Prime statistics

Teaching programs for the HP Prime graphing calculator, written in PPL and MicroPython, and originally intended for upper-level university statistics courses.  

**And a set of notes on what the Prime actually does**, as opposed to what the manual says — hard limits, commands that behave differently than documented, the MicroPython bridge and how it fails. Those notes are not specific to statistics; if you write PPL for anything, [docs/lessons-learned_v7d.md](docs/lessons-learned_v7d.md) is the part worth your time.

Everything here is **free for educational and personal use**. See [LICENSE](LICENSE.txt).

**Tested on** an HP Prime G2 and G1, both running the **2026-09-09** firmware, plus the desktop Virtual Calculator — **except the newer programs listed under [Not yet tested on hardware](#not-yet-tested-on-hardware)**, which have not been run on a calculator yet.

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

*The versions in `programs/` dated 10–11 October 2026 (BayesTree beta 5, NormExplorer beta 40, StudRange beta 13, ChiTable beta 1k, and the beta 1a releases below) carry the helper-name and wait-loop fixes described under* The notes *and have not yet been re-run on hardware; the versions they replace were tested as stated.*

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

### ChiTable — chi-square for a two-way table
Pick 2 × 2, 2 × 3 or 3 × 2, tap the cells to type the observed counts (soft keys: Edit, Values, Clear, Cancel, Run), and get the expected counts, row and column percentages, χ² with df, p and the critical value, the likelihood-ratio G², Cramér's V, each cell's contribution and adjusted residual, and an interpretation in words with an APA-style line. A 2 × 2 table adds Yates, Fisher's exact test, the two-proportion z, risk difference, relative risk and odds ratio with 95% intervals. Three plots: observed beside expected, a mosaic coloured by residual, and the χ² curve with the p-value shaded. Four built-in examples, including the Florida death-penalty tables that show Simpson's paradox.

**Status: beta 1k.** Beta 1j was tested on a G2 and a G1, both on the 2026-09-09 firmware (10 Oct 2026): the entry grid and its soft keys, the Values form, the results pages and all three plots. Beta 1k only changes how it waits and how it quits (below) and has not been re-run yet. The arithmetic is verified against scipy and statsmodels; [docs/chitable-guide.md](docs/chitable-guide.md) is the user's guide.

---

## Not yet tested on hardware

> **These programs are new (October 2026) and have NOT yet been run on an HP Prime.** They were written for the 2026-09-09 firmware and checked off the calculator, but none has been run on one yet. Treat them as betas: expect rough edges, check any result you intend to rely on, and please report what you find. Each file's header says the same thing.
>
> The beta 1a releases (11 October 2026) of GaltonBoard, CentralLimit, TrendTest and TestChooser put a one-second limit on every "wait for the finger to lift" loop and, where the program printed a summary on the way out, return it to Home instead; nothing else changed. DNAMixLR needed no change.

### GaltonBoard — Galton's quincunx *(untested)*
Balls fall through rows of pegs, bouncing right with probability p, and the bins build a Binomial(R, p) histogram. The binomial expected counts and the normal approximation are drawn over it. Tap the pegs to drop a ball, or tap a bar to compare its observed share with the binomial probability. The arrows change p and the number of rows, and the menu sends the bins to D1/D2 for the Statistics 1Var app. After Galton (1873) and the QUINCUNX demo in CDC Epi Info 6.

### CentralLimit — Central Limit Theorem explorer *(untested)*
**This one is an app, not a plain program.** It lives inside a saved copy of the Statistics 1Var app, so it can set up the built-in histograms; the installation steps are in the file's header. Build a population (uniform, normal, exponential, geometric, bimodal, or your own data in D1), draw repeated samples, and watch the sample means pile up into a bell centred on μ with spread σ/√n. Sample sizes are offered only as perfect squares, so σ / SD(means) can be compared with √n at a glance. After Colin Croft's HP 39G aplet (2003).

### TrendTest — chi-square test for linear trend *(untested)*
For a 2 × k table with ordered exposure levels: Mantel's chi-square for trend (1 df), Pearson's chi-square, and the departure from linearity. Each level gets a Wilson interval for its proportion and an odds ratio against level 1 with a Woolf interval. There are two plots, proportions with the weighted trend line and odds ratios on a log scale; tap a dot for its numbers. The arithmetic was checked against SciPy and statsmodels on 300 random tables before the PPL was written. The built-in example (snoring and heart disease, Norton & Dunn 1985) lists its expected results in the header, so the first hardware run can be checked against them.

### TestChooser — which statistical test? *(untested)*
Two tapped questions, the outcome's measurement scale and the study design, lead to a suggested test. Each test page says what it compares, what it assumes, where to find it on the Prime, what to do afterwards, and the alternative when an assumption fails. You can also browse the whole table and tap a cell. The scheme follows Stanton Glantz's *Primer of Biostatistics*.

### DNAMixLR — likelihood ratio for a DNA mixture *(untested)*
The likelihood ratio for a mixed DNA profile under prosecution and defence hypotheses, locus by locus, with the NRC II coancestry (θ) correction, following Weir et al. (1997) and Curran et al. (1999). It offers preset or custom hypotheses, up to 12 loci, the ENFSI verbal scale, and plots of the LR by locus and against θ. The probability engine was checked against brute-force enumeration in Python (400 random cases), and a worked example is built in. **A teaching tool only:** casework needs validated software and a qualified analyst.

---

## Diagnostics

Short throwaway programs for finding out what your own calculator does.

**`PyVer`** is the useful one. It reports your MicroPython version, probes ten modules, and tests two behaviours known to vary. Two minutes, and it tells you more about your firmware's Python than any document can.

`JoinTest` and `GenTest` isolate a specific `str.join` failure — kept because they document a real investigation, including the part where it did not reproduce.

**`PyProbe`** (beta 2b) asks what the Prime's MicroPython can actually do: how values pass from PPL into Python, what the `matplotl` charts really draw, and what each module contains. It has been run on the Virtual Calculator only, **not yet on hardware**. Its findings so far are in the file's header: `argv` text is cut off at about 250 characters in total, and `matplotl` is not usable for teaching charts (`clf()` clears nothing, `axis()` has no visible effect, colour is ignored).

---

## The notes

[**docs/lessons-learned_v7d.md**](docs/lessons-learned_v7d.md) is the substantial document here: everything found the expensive way across roughly forty build iterations on real hardware. Hard limits, command behaviour that contradicts the manual, graphics and input idioms, the MicroPython bridge, numerical methods, and a list of disproved theories recorded as disproved. The lessons learned document can be uploaded to your favorite AI to assist with coding.  

A few things from it that are hard to find elsewhere:

- **The Prime runs MicroPython 1.9.4**, a December 2018 release tracking CPython 3.4. Check *those* docs, not the current ones. This single fact explains most of the surprises.
- **A Python exception does not raise a PPL error.** The traceback goes to the Terminal and PPL carries on with whatever the bridge variable held before. `IFERR` around `PYTHON(...)` catches nothing. In this fleet a sampler failed on every run for eleven consecutive builds with nothing on screen to show it.
- **`FREEZE` is not a pause.** It suppresses the screen refresh at program *end*. Mid-program it does nothing.
- **`STRING(x, 1, digits)` ignores the digits argument.** Mode 1 is Standard. Fixed decimals need mode 2.
- **Built-in names are matched case-insensitively.** `LOCAL csC` is a syntax error because `csC` is `CSC`, the cosecant; a program named `ChiSquare` is `CHISQUARE`. Scan every name, prefix or not.
- **Every program's routines go into one shared pool.** A helper that is not `EXPORT`ed is still visible to every other program on the calculator, and two programs that define the same name (`NiceNum`, `fmtp`...) can run each other's code: a runtime error, the Program Editor open on the *other* program, and a reset to get out. The 10 October 2026 versions in `programs/` give every helper a program tag (`sr_NiceNum`, `bt_fmtp`), and `tools/fleet_names_v1.py` checks a folder of programs for duplicates.
- **A finger lift can arrive from `WAIT(-1)` as a one-element list.** Read `kk(2)` from it and the program stops with an error. Check `SIZE` first, and give any "wait for the finger to lift" loop a time limit.
- **Data columns are reachable from a standalone program; app settings are not.** `D1`, `C1`, `C2` can be read and written. `H1Type` and `SetSample` are a syntax error at paste time.
- **The desktop emulator runs the real ROM**, so any difference you see on hardware is necessarily timing, memory or display — and no amount of further emulator testing will find it.

---

## Credit

Concept, direction, classroom judgement and all hardware testing: **Roger Metcalf**, 2026.

Dozens of community PPL programs from various HP-related forums were read as reference while working out how the Prime actually behaves — several entries in the notes exist because a corpus program showed a construct working that the manual does not describe. None of those programs are reproduced here.

Implementation, numerical work and documentation: written, expanded, and vastly improved with incredible and amazing AI assistance from Anthropic Claude--mostly Opus 5 and Fable 5.1.  Much of the notes and the user's guides were essentially written by Claude.

The studentized range algorithm is after Dunlap, Powell & Konnerth (1977). Accuracy figures were verified against SciPy, and several were also cross-checked against historical sources: Harter's 1960 tables of the studentized range, and the worked examples HP printed in the manuals for its own 1970s statistics programs on the HP-41, HP-55, HP-65 and HP-67/97 ([docs/historical-cross-checks.md](docs/historical-cross-checks.md)). Several MicroPython findings credited in the notes come from [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit), measured independently on a different G2.

Corrections and reproductions are welcome. Where a claim here is unverified, it says so.
