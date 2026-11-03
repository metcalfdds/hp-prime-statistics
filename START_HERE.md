# Start here

*HP Prime statistics: a one-page guide for first-time visitors. Version 2, 27 October 2026. Prepared for HHC 2026: welcome!*

This repository holds **30 teaching programs** for the HP Prime, written in PPL with MicroPython where it helps. It also holds **a set of notes on how the Prime actually behaves**, found by testing and not by reading the manual. The programs were written for university statistics and forensic science courses. The notes are useful to anyone who writes PPL.

Everything here is free for educational and personal use ([LICENSE](LICENSE.txt)).

## If you have five minutes: read the notes

[**docs/lessons-learned_v7zl.md**](docs/lessons-learned_v7zl.md) is the most useful file here, even if you never run a statistics program. It covers hard limits, commands that behave differently from the manual, touch and graphics idioms, `WAIT(-1)` and soft keys, the MicroPython bridge and how it fails silently, how to call the CAS from a program safely, numerical methods for 12-digit reals, and testing on the Virtual Calculator. Theories that turned out wrong are kept, marked as disproved.

Three findings that save the most time:

- **The Prime runs MicroPython 1.9.4**, a December 2018 release tracking CPython 3.4. Read *those* docs.
- **A Python exception does not raise a PPL error.** `IFERR` around `PYTHON(...)` catches nothing, and the program carries on with stale values.
- **Every program's routines share one name pool.** Two programs that both define a helper with the same name can run each other's code. `tools/fleet_names_v2.py` checks for this.

The notes are written so they can also be given to an AI coding assistant as background before it writes PPL for you. They were written with and for Claude Code and read best there; they are meant to help any assistant, but have not been tried with another. `CLAUDE.md` at the top of the repository is the working brief a Claude Code session reads on its own. For a model with a small context window, [docs/ppl-rules-for-any-assistant.md](docs/ppl-rules-for-any-assistant.md) is the same knowledge as about 3,000 words of flat rules, ending in a small program that passes the gate.

## If you have a calculator: try these first

No calculator? The [starter pack](starter-pack/README.md) puts all 30 on HP's free Virtual Calculator for Windows in one copy, with no Connectivity Kit. Your own data goes in through the [Data Loader](data-loader/README.md) page and DataLoad, not by typing. Neither shortcut is in HP's manuals: [docs/two-shortcuts.md](docs/two-shortcuts.md) says how they work and who found them. Newest: the [Prime Loader](https://metcalfdds.github.io/hp-prime-statistics/prime-loader/) page ([how it works](prime-loader/README.md)) puts one chapter's programs on the Virtual Calculator: one click in Edge or Chrome, a few in Firefox, and nothing to check afterwards.

Install by pasting the `.txt` file into a new program in the HP Connectivity Kit ([full steps](README.md#installing)). Do not rename a `.txt` to `.hpprgm`. Each of these shows off the touch screen:

| Program | Try this |
| --- | --- |
| **CICatcher** | Drag the confidence level up and down: fifty intervals stretch or shrink, and the count of hits and misses updates. |
| **GaltonBoard** | Hold a finger on the funnel and pour balls through the pegs; drag sideways to change p. |
| **BayesTree** | Slide the prevalence down and watch a 95 %-accurate test's positive predictive value collapse. |
| **PowerViz** | Drag the H₁ curve; the α, β and power regions reshade as you move. |
| **ScatterLab** | Fit a line by eye in Guess mode, then see least squares beat it. |
| **BiNorm3D** | Turn the bivariate normal in 3-D with a finger, then slice it to see regression to the mean. |
| **AgreeLab** | Drag a count off the diagonal of the two neurologists' table and watch kappa fall. |
| **RiskLab** | Drag the cut-off along the ROC curve and watch who gets flagged "high risk", group by group. |

The full list of programs, with what each one does, is in the [README](README.md#the-programs).

## What has been tested, and what has not

- Every program passes a four-tool lint gate and runs in a PC harness that presses keys and taps like a student. Its numbers are checked against SciPy, statsmodels and exact arithmetic. A review on 19 October 2026 made about 82,000 such checks and found no wrong formula.
- Earlier versions ran in two rounds on the **HP Prime Virtual Calculator**. Its reports are in [docs/dev/](docs/dev/).
- **The current versions have had only a quick, cursory try on a G1 and a G2**, not a systematic run of their checklists. That includes the eight programs added in October 2026 (RankLab, AnovaLab, SeizureLab, SurvLab, FitCheck, ResampLab, AgreeLab and RiskLab), which also each had an independent second review before release; the two 22 October versions (StudRange beta 15e, TrendTest beta 3f) have not yet run on a calculator. Earlier versions of ChiTable, NormExplorer, StudRange and BayesTree were tested on both.
- **31 October 2026: all 28 current versions load and compile on the Virtual Calculator** from the starter pack (Check: "No errors in the program"), and TTestLab, BurrLab (its MicroPython fit) and CentralLimit started there. That is a load test, not a run of their checklists ([the notes](docs/changes/StarterPack_v1_NOTES.md)).
- **31 October 2026: DataLoad (new) ran on the Virtual Calculator** in three versions: both kinds of load on the Rossi data and on a text-coded matrix with blanks, its summaries equal to Python's, and TTestLab reading the lists it filled ([the notes](docs/changes/DataLoad_beta1_NOTES.md)). Not yet on a G1 or G2.
- **31 October 2026, night: TTestLab had its independent review** ([docs/dev/review2-TTestLab-beta1a.md](docs/dev/review2-TTestLab-beta1a.md)): the arithmetic was right throughout, and ten faults in its dialogs and wording (a cancelled α list leaving a one-tailed label on two-tailed numbers, a crash after a refused D1/D2 read, "p = 0.000") were fixed in beta 1b, which ran on the Virtual Calculator.
- **31 October 2026, night: TTestLabG (new), the general version of TTestLab**, built from it for an intro course in any subject: separate variances by default, t critical exact for the df with the printed table as a note, Darwin's plants and the 1970 draft lottery among its examples. 93 checks; **ran on the Virtual Calculator** beside TTestLab ([the notes](docs/changes/TTestLabG_beta1_NOTES.md)). Not yet on a G1 or G2, and not yet reviewed as a program of its own.
- **2 November 2026, night: commas in big numbers, all 30 programs** (round 5; Lessons Learned v7zk). Every number of 1,000 or more on the screen now shows its commas, never a year; AgreeLab and ResampLab write d̄. Each new version passes its verify script against the one before (the same path under random use, the same texts handed to the CAS, every big number grouped, no new overlap), and **all 30 were Checked on the Virtual Calculator with no error**; not yet run on a G1 or G2 ([how it was done](docs/dev/commas-2026-11-02.md)).
- **2 November 2026, night: sensible ranges for what a student types, and menus that fit, in 11 programs** (round 6; Lessons Learned v7zl). Alpha is from 0.001 to 0.2 everywhere; a value outside a range is refused with a sentence, never changed without a word (StudRange made an alpha of 5 into 0.5); counts, StudRange's k, df and m, and DNAMixLR's answers keep to ranges the program can show and compute; every menu item fits its box; BurrLab draws a y axis on every plot. Each new version passes its verify script against the one before, and **all 11 were Checked on the Virtual Calculator with no error**; not yet run on a G1 or G2 ([how it was done](docs/dev/caps-2026-11-02.md)).
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
