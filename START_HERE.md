# Start here

*HP Prime statistics: a one-page guide for first-time visitors. Version 1, 19 October 2026. Prepared for the HHC 2026 conference drive.*

This repository holds **19 teaching programs** for the HP Prime, written in PPL with MicroPython where it helps. It also holds **a set of notes on how the Prime actually behaves**, found by testing and not by reading the manual. The programs were written for university statistics and forensic science courses. The notes are useful to anyone who writes PPL.

Everything here is free for educational and personal use ([LICENSE](LICENSE.txt)).

## If you have five minutes: read the notes

[**docs/lessons-learned_v7q.md**](docs/lessons-learned_v7q.md) is the most useful file here, even if you never run a statistics program. It covers hard limits, commands that behave differently from the manual, touch and graphics idioms, `WAIT(-1)` and soft keys, the MicroPython bridge and how it fails silently, how to call the CAS from a program safely, numerical methods for 12-digit reals, and testing on the Virtual Calculator. Theories that turned out wrong are kept, marked as disproved.

Three findings that save the most time:

- **The Prime runs MicroPython 1.9.4**, a December 2018 release tracking CPython 3.4. Read *those* docs.
- **A Python exception does not raise a PPL error.** `IFERR` around `PYTHON(...)` catches nothing, and the program carries on with stale values.
- **Every program's routines share one name pool.** Two programs that both define a helper with the same name can run each other's code. `tools/fleet_names_v2.py` checks for this.

The notes are written so they can also be given to an AI coding assistant as background before it writes PPL for you.

## If you have a calculator: try these first

Install by pasting the `.txt` file into a new program in the HP Connectivity Kit ([full steps](README.md#installing)). Do not rename a `.txt` to `.hpprgm`. Each of these five shows off the touch screen:

| Program | Try this |
| --- | --- |
| **CICatcher** | Drag the confidence level up and down: fifty intervals stretch or shrink, and the count of hits and misses updates. |
| **GaltonBoard** | Hold a finger on the funnel and pour balls through the pegs; drag sideways to change p. |
| **BayesTree** | Slide the prevalence down and watch a 95 %-accurate test's positive predictive value collapse. |
| **PowerViz** | Drag the H₁ curve; the α, β and power regions reshade as you move. |
| **ScatterLab** | Fit a line by eye in Guess mode, then see least squares beat it. |

The full list of programs, with what each one does, is in the [README](README.md#the-programs).

## What has been tested, and what has not

- Every program passes a four-tool lint gate and runs in a PC harness that presses keys and taps like a student. Its numbers are checked against SciPy, statsmodels and exact arithmetic. A review on 19 October 2026 made about 82,000 such checks and found no wrong formula.
- Earlier versions ran in two rounds on the **HP Prime Virtual Calculator**. Its reports are in [docs/dev/](docs/dev/).
- **The current versions have had only a quick, cursory try on a G1 and a G2**, not a systematic run of their checklists; the two 22 October versions (StudRange beta 15e, TrendTest beta 3f) have not yet run on a calculator. Earlier versions of ChiTable, NormExplorer, StudRange and BayesTree were tested on both.
- Each version has a device-test checklist in [docs/changes/](docs/changes/), ordered from least to most risky.

## If you would like to help

- **Run a checklist on real hardware.** Pick any program, follow its checklist in `docs/changes/`, and report what you see. A G1 result is especially welcome.
- **Run the diagnostics on your own calculator.** `GfxProbe` and `CASProbe` (in [diagnostics/](diagnostics/)) test features the manuals describe but that have not been confirmed here. Each writes its results to a variable you can send back.
- **Correct the notes.** If a finding in the Lessons Learned is wrong on your firmware, or you know something it does not, that is the most valuable report of all.
- **Build on the code.** [templates/TouchKit_template_v3.txt](templates/TouchKit_template_v3.txt) is a starting point for a new touch program, and [tools/](tools/) has the checks every program here passes, in plain Python 3.

Reports and corrections are welcome through [GitHub issues](https://github.com/metcalfdds/hp-prime-statistics/issues). Where a claim here is unverified, it says so.

**DISCLAIMER: these programs are teaching and demonstration aids. They are not validated for forensic, clinical or legal use; do not rely on their results for legal purposes.**

---

*Roger D. Metcalf, DDS, JD, DFSc, 2026. Written with AI assistance: the concept, direction, decisions and all hardware testing are the author's; the code, drafting and source-checking were done with Claude Opus 5.5 and Claude Fable 5.1 (Anthropic), October 2026.*
