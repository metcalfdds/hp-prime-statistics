# HP Prime statistics

Teaching programs for the HP Prime graphing calculator, written in PPL and MicroPython. They were originally intended for upper-level university statistics courses, and also to show off some of the capabilities of the HP Prime calculator: the colour screen, the touch screen, and the MicroPython engine running alongside PPL.

**And a set of notes on what the Prime actually does**, as opposed to what the manual says: hard limits, commands that behave differently than documented, the MicroPython bridge and how it fails. Those notes are not specific to statistics. If you write PPL for anything, [docs/lessons-learned_v7h.md](docs/lessons-learned_v7h.md) is the part worth your time, I hope.

Everything here is **free for educational and personal use**. See [LICENSE](LICENSE.txt).

> **Test status, 17 October 2026.**
> - **The emulator run.** The touch-and-graphics versions of 16 October ran on the **HP Prime Virtual Calculator** (2.4.2, the same 2026-09-09 firmware as the calculators). Most passed. Every number checked matched SciPy.
> - **What it found, and what is fixed.** The emulator found six real bugs, and the versions here fix them:
>   - the way programs called the CAS;
>   - soft keys in BayesTree and StudRange;
>   - GaltonBoard's hollow pegs;
>   - StatDist's fractional degrees of freedom;
>   - a rounding slip in BayesTree.
> - **Not yet re-run on the emulator:** most of the CAS versions. ErrorRate is the exception; it shows a real CAS answer there.
> - **Not yet on hardware:** none of these versions has been run on a G1 or G2. Earlier versions of ChiTable, NormExplorer, StudRange and BayesTree were tested on both.
> - **How each program was checked:** every program here passed a four-tool lint gate. It was also run on a PC in a test harness that drives it like a student at the keys, with its numbers checked against SciPy and statsmodels.
> - **Checklists:** each one has a device-test checklist in [docs/changes/](docs/changes/). The emulator's full report is in [docs/dev/](docs/dev/).

These programs are works in progress and have not been extensively tested, and they are provided as is--you should not rely on the results from these programs for anything. Use at your own risk. Your mileage may vary.

---

## Installing

Every program is a plain `.txt` file, on purpose.

1. Open the **HP Connectivity Kit** and connect your calculator.
2. Create a new program in the Program Catalog.
3. Open this repository's `.txt` file in any text editor, select all, copy.
4. Paste into the Connectivity Kit's program editor, and sync.

**Do not rename the file to `.hpprgm`.** That format is binary (UTF-16LE with a header), and a `.txt` renamed to it will not import. Pasting is the reliable route.

**Install one version of each program.** Every program on a Prime shares one pool of routine names, so two versions of the same program on one calculator can run each other's code. Delete the old one first.

**Upgrading from an earlier version?** ConTable2 and FEP are now part of EpiStats, and StudRangePy is now part of StudRange. Delete those three from the calculator.

**CentralLimit is an app, not a plain program.** The installation steps are in its header.

**MicroPython.** StudRange, NormExplorer, GaltonBoard, CentralLimit and ErrorRate carry a `#PYTHON … #END` block inside the program file. There is **no separate `.py` file**, and nothing goes into the Python app. With Python firmware (2.1.14566, April 2021, or later) the Python part runs, and a badge on screen says so. Without it, the programs fall back to pure PPL automatically.

---

## The programs

**Exact answers from the CAS.** Twelve programs can now show an exact or symbolic answer beside their decimal one: Fisher's p as a fraction, a binomial probability as C(n, k)·pᵏ…, the limit that turns into the rule of three, a least-squares line as exact fractions. The calculator's CAS works it out on demand, the program checks it against its own number, and a badge says "exact (CAS)" or "decimal". If the CAS is busy or fails, the decimal answer stands.

Almost every program now responds to a finger: drag a bound, a bar, a curve or a dot and watch the numbers follow. Where a screen needs more than six soft-key actions, the right-hand key reads **More** and pages to the next set, as the NXT key did on the HP 48. Every touch action also has a key route.

### Distributions

**NormExplorer** (beta 42): a normal-distribution workbench.
- Any μ and σ, four kinds of probability question and three inverse ones, a z-formula solver, Cohen's d, and a standardize animation.
- A live explorer: drag either bound of a shaded interval. "More" brings up a second page, so the arrow keys can move a bound, μ or σ.
- Reads your own data from the Statistics apps.

**Norm3 and Burr3** (v2.4, they take arguments; the Program Catalog asks for them): drag x₀ and watch the area and the S-curve together. Tap the S-curve for the inverse. Burr3 shows its mode, median and mean sliding apart, and announces the moment cases.

**StatDist** (v2.7b): 27 distributions, each result a plot you can touch. Drag x or k, the shading follows, and the window snaps to round values. Overlays show the normal approximation, N(0, 1) behind t, and the CDF as an S-curve. A Gallery opens six examples with one tap.

**StudRange** (beta 15a): the studentized range (Tukey's q).
- p from q, the critical value from α, Tukey HSD, and an interactive plot.
- **MicroPython does the arithmetic, PPL is the fallback**, and a badge says which engine ran.
- Python adds an H₀ simulation that shows why q, and not t, is the right yardstick.
- Descends from a 1977 FORTRAN IV subroutine (Dunlap, Powell & Konnerth, *Behavior Research Methods & Instrumentation* 9(4):373–375).
- Accuracy against SciPy: within 5×10⁻⁶ for k 2–20 and df 1–20,000. This version also fixes wrong values at df = 1 and at very large df in the earlier versions.

### Sampling, estimation and power

**CentralLimit** (beta 3a, an app): watch one sample happen, its members lighting up and their mean dropping into the pile. Then drag along the top panel to choose n, and see the square-root law on its own page. After Colin Croft's HP 39G aplet (2003).

**SampDist** (v2.3): the sampling distribution of x̄, with the population drawn faintly behind it.
- **n×4** halves the width.
- The nearer bound follows your finger.
- "Watch sample means" drops forty of them onto the axis.

**CICatcher** (beta 2a): fifty confidence intervals stack up, blue if it catches the truth (the green line) and red if it misses. **Drag the confidence level**: every interval stretches or shrinks, and the catch count updates exactly without new samples. Covers z, t, Wald and Wilson.

**GaltonBoard** (beta 3b): Galton's quincunx.
- **Pour mode:** hold a finger on the funnel and a stream of balls cascades through the pegs.
- **Drag sideways** to change p.
- **Drop 100,000** runs in MicroPython.
- Tap a bar for its binomial probability and the normal area.

**PowerViz** (v2.5a): **drag the H₁ curve**, and the α, β and power regions reshade live. Drag the critical line to set α, and drag up or down for n. n₈₀ appears in the panel and on the power-versus-n curve.

### Tables and tests

**ChiTable** (beta 3b): chi-square for a 2 × 2, 2 × 3 or 3 × 2 table.
- The full statistics: expected counts, G², Cramér's V, adjusted residuals, and for a 2 × 2 Fisher, RR and OR.
- **Drag an observed bar**, and every expected bar moves with χ² and p.
- **Drag the critical line** on the χ² curve.
- An independence morph, a Fisher bar plot, and the Florida death-penalty tables as a Simpson's-paradox page.
- [docs/chitable-guide.md](docs/chitable-guide.md) is the user's guide.

**TrendTest** (beta 3b): chi-square for linear trend in a 2 × k table. **Drag a dot** to change a level's proportion and watch the trend test respond. Includes a confidence band and Wilson intervals.

**TestChooser** (beta 2): which statistical test? It is a tappable flowchart: tap the outcome's scale and the design, and the path draws itself to a test. There is also a tappable table, and a 20-case criminal-justice and forensic quiz. After Glantz's *Primer of Biostatistics*.

**EpiStats** (v1.7a): epidemiology.
- **2 × 2 tables** in cohort, diagnostic and paired layouts: McNemar, Yule's Q, and a bar for every possible table behind Fisher's test. Call `EpiStats2x2(a,b,c,d)` from Home.
- **Risk and odds** with Wilson intervals, plus an NNT icon array.
- **Incidence rates and sample size.**
- **Stratified Mantel–Haenszel analysis** with Breslow–Day, and a forest plot where a tap drops a stratum.

### Correlation and regression

**ScatterLab** (beta 2a): build a scatterplot with your finger. Add, drag or delete points, and the least-squares line, r, r², SSE and the residuals follow. Guess mode lets you fit a line by eye first, then shows that least squares really does have the smallest SSE.

**BiNorm3D** (beta 1): the bivariate normal as a wireframe you turn with a finger. It adds a contour view, and a slice that shows regression to the mean.

### Bayes and forensic science

**BayesTree** (beta 8b): a natural-frequency Bayes tree.
- **Slide the prevalence** and the tree and a mosaic re-flow: watch a 95 %-accurate test's PPV collapse at low prevalence.
- Sensitivity and specificity can be dragged on the branches.
- A Fagan nomogram, a second test, and forensic labels.

**DNAMixLR** (beta 3a): the likelihood ratio for a mixed DNA profile, locus by locus, with the NRC II θ correction (Weir et al. 1997; Curran et al. 1999).
- **Drag θ** and watch the LR fall down an ENFSI verbal ladder.
- Tap a locus for its numbers, and drop loci from the table.
- A prosecutor's-fallacy page.
- **A teaching tool only:** casework needs validated software and a qualified analyst.

**ErrorRate Lab** (beta 1a): "Zero errors in 30 proficiency tests: how good is the examiner?"
- The **upper 95 % confidence bound** on the error rate, the convention PCAST (2016) asked forensic disciplines to report. The rule of three appears as the limit it is.
- A Bayesian view.
- A MicroPython simulation of 10,000 proficiency programmes.
- The chance of a coincidental match in a database search.

*FDAES (forensic dental age estimation) is held back from this repository until two reference values are re-checked against their sources.*

---

## Diagnostics

Short programs for finding out what your own calculator does.

- **`GfxProbe`** tests the graphics and touch features the manuals document but that we have not confirmed:
  - translucent and blended fills;
  - the 3-D triangle mesh;
  - scaled blits;
  - a second finger;
  - the WAIT(−1) gesture events;
  - plus how many lines a message box really shows.
  It writes its answers to `GP_LOG`.
- **`CASProbe`** (beta 1b) finds out how a program can use the CAS safely:
  - the call form;
  - what text comes back;
  - how errors look;
  - how fast it is on a G1;
  - and, last, behind a warning page, whether Python's `cas.caseval` is stable.
  It writes `CX_LOG`. On the 2026-09-09 firmware it found that `CAS(s)` hands a string variable's text back unevaluated; the working form is in the notes, §9b.
- **`MenuTapProbe`** (new, 40 lines) shows what `WAIT(-1)` reports for a tap on the soft-key strip: a click, and nothing else.
- **`LocalHeadProbe`** is ten lines: is `LOCAL name(a, b)` a legal routine head?
- **`PyVer`** reports your MicroPython version and probes ten modules. It takes two minutes.
- **`PyProbe`** (beta 2b) asks what the Prime's MicroPython can actually do: how values pass from PPL into Python, what the `matplotl` charts really draw, and what each module contains. Run on the Virtual Calculator only.
- `JoinTest` and `GenTest` isolate a specific `str.join` failure. They are kept because they document a real investigation, including the part where it did not reproduce.

`templates/TouchKit_template_v3.txt` is the house touch kit as a starting point for a new program: drain, wait-for-key-or-tap, soft keys with "More" pages, hit boxes, and a draggable bar chart.

---

## The notes

[**docs/lessons-learned_v7h.md**](docs/lessons-learned_v7h.md) is the substantial document here: everything found the expensive way across roughly forty build iterations on real hardware. It covers:
- hard limits;
- command behaviour that contradicts the manual;
- graphics and input idioms;
- the MicroPython bridge;
- how to let the CAS into a program without letting it break one;
- numerical methods;
- testing on the HP Prime Virtual Calculator;
- a list of disproved theories, recorded as disproved.

The lessons learned document can be uploaded to your favorite AI to assist with coding.

A few things from it that are hard to find elsewhere:

- **The Prime runs MicroPython 1.9.4**, a December 2018 release tracking CPython 3.4. Check *those* docs, not the current ones. This single fact explains most of the surprises.
- **A Python exception does not raise a PPL error.** The traceback goes to the Terminal, and PPL carries on with whatever the bridge variable held before. `IFERR` around `PYTHON(...)` catches nothing. In this fleet a sampler failed on every run for eleven consecutive builds with nothing on screen to show it.
- **`FREEZE` is not a pause.** It suppresses the screen refresh at program *end*. Mid-program it does nothing.
- **`STRING(x, 1, digits)` ignores the digits argument.** Mode 1 is Standard. Fixed decimals need mode 2.
- **Built-in names are matched case-insensitively.** `LOCAL csC` is a syntax error because `csC` is `CSC`, the cosecant. A program named `ChiSquare` is `CHISQUARE`. Scan every name, prefix or not.
- **Every program's routines go into one shared pool.** A helper that is not `EXPORT`ed is still visible to every other program on the calculator. Two programs that define the same name (`NiceNum`, `fmtp`...) can run each other's code: a runtime error, the Program Editor open on the *other* program, and a reset to get out. Every helper here carries its program's tag, and `tools/fleet_names_v2.py` checks a folder of programs for duplicates.
- **`MOUSE` and `WAIT(-1)` number their touch events differently.** In `MOUSE`, drag is 2; in `WAIT(-1)`, drag is 1. A handler has to say which table it reads.
- **Soft keys under `WAIT(-1)` arrive only as a click.** A tap on the `DRAWMENU` strip is `{3, x, y}`: no press, no lift. A loop that waits for a press there never sees the key.
- **A program cannot hand the CAS a string variable.** `CAS(s)` gives the text back unevaluated; `EXPR("CAS(\"string(" + s + ")\")")` works. The Prime prints `e^(`, `√` and `{…}`, not desktop Giac's `exp(`, `sqrt(` and `list[…]`.
- **Chi-square and F CDFs take whole-number df only**; the t distribution takes any.
- **A finger lift can arrive from `WAIT(-1)` as a one-element list.** Read `kk(2)` from it and the program stops with an error. Check `SIZE` first, and give any "wait for the finger to lift" loop a time limit.
- **`STRING()` of a number follows the Home number format,** which can include digit-grouping marks and a special minus sign. Text built for the CAS or for Python should not come from it.
- **Data columns are reachable from a standalone program; app settings are not.** `D1`, `C1` and `C2` can be read and written. `H1Type` and `SetSample` are a syntax error at paste time.
- **The desktop emulator runs the real ROM**, so any difference you see on hardware is necessarily timing, memory or display. No amount of further emulator testing will find it.

[docs/changes/](docs/changes/) has one file per program version: what changed, the lint and verification output, and the device-test checklist. [docs/dev/](docs/dev/) has the fleet review and the CAS plan that drove the 16 October versions, and the emulator report of 17 October.

---

## Tools

[tools/](tools/) has the checks every program here passes before it is pasted, in plain Python 3:
- the fleet-wide name-collision check;
- the built-in-name and structure checks;
- the gate that runs them all;
- a PC run harness that drives a program with scripted keys, taps and drags, with SciPy behind the statistics built-ins and desktop Giac behind `CAS(...)`, made to behave as the Prime's firmware does where the emulator showed a difference.

[verify/](verify/) has the scripts that checked each program's numbers.

---

## Credit

Concept, direction, classroom judgement and all hardware testing: **Roger Metcalf**, 2026.

Dozens of community PPL programs from various HP-related forums were read as reference while working out how the Prime actually behaves. Several entries in the notes exist because a corpus program showed a construct working that the manual does not describe. None of those programs are reproduced here.

Implementation, numerical work and documentation: written, expanded, and vastly improved with incredible and amazing AI assistance from Anthropic Claude--mostly Opus 5 and Fable 5.1.  Much of the notes and the user's guides were essentially written by Claude.

The studentized range algorithm is after Dunlap, Powell & Konnerth (1977). Accuracy figures were verified against SciPy, and several were also cross-checked against historical sources: Harter's 1960 tables of the studentized range, and the worked examples HP printed in the manuals for its own 1970s statistics programs on the HP-41, HP-55, HP-65 and HP-67/97 ([docs/historical-cross-checks.md](docs/historical-cross-checks.md)). Several MicroPython findings credited in the notes come from [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit), measured independently on a different G2.

Corrections and reproductions are welcome. Where a claim here is unverified, it says so.
