# Round 18: every program sets the book's four Home settings when it starts, and leaves them set (22 November 2026)

All 31 programs, and in each of them one line of code. No arithmetic, no page, no menu and no word on the screen changed, apart from the version where a page shows it.

## Why

The book may have readers in Europe, where most languages write the decimal point as a comma, and a Prime can be set that way (Home Settings, Digit Grouping, 123.456,789). On 22 November the Virtual Calculator was set so, and four programs were run ([the record](../../docs/dev/comma-decimal-mark-2026-11-22.md)):

- `STRING` writes Home's decimal mark, inside a running program too, pragma line or not. Every program's comma routine takes a run of four or more digits for a whole number unless a period stands before it, so it put commas into the decimals: Norm3 showed 0.9772 as 0,9,772, and StatDist showed 0.758036 as 0,758,036.
- NormExplorer beta 42j and StudRange beta 15n, the two programs with no `#pragma mode` line, stopped the calculator at Run.

Roger asked, "Can a HP Prime program change the settings?" Three probes showed that it can, and that a setting stays as the program leaves it (`diagnostics/SetProbe_beta1.txt`, `SetOdd_beta1.txt`, `SetBook_beta1.txt`). Asked whether each program should put the reader's own settings back when it ends, or leave the book's on, he chose: "I agree that we should leave the calculator the way Statisticles sets it--and that also helps avoid any potential mis-settings in subsequent Statisticles--we keep putting the calculator in the mode we need it to be in".

## What changed

One line, at the head of every routine a person can start a program by:

```
HSeparator := 0; HFormat := 0; HAngle := 0; Entry := 0;   // Round 18: the book's four Home settings, left on
```

| Variable | Home Settings | 0 is |
| --- | --- | --- |
| `HSeparator` | Digit Grouping | 123,456.789: the period is the decimal point |
| `HFormat` | Number Format | Standard |
| `HAngle` | Angle Measure | Radians |
| `Entry` | Entry | Textbook |

- It is the first statement after the routine's `LOCAL` lines, so every `LOCAL` still stands at the routine's head.
- It is in 31 of the fleet's 32 `EXPORT` routines (EpiStats has two, `EpiStats` and `EpiStats2x2`). The thirty-second is CentralLimit's, which is empty: CentralLimit is an app, and an app is started by its hooks, so there the line is in `START` and in `Plot`. That is 33 lines in the 31 programs.
- NormExplorer and StudRange also get `#pragma mode( separator(.,;) integer(h32) )` as their first line, word for word the first line of 28 of the other 29 (StatDist's has no spaces inside its outer parentheses).
- Nothing puts the reader's own settings back. A reader who prefers a comma, RPN entry, Fixed or Degrees finds the calculator changed after a program has run; the book asks for these four settings anyway.

| Program | Version | Program | Version | Program | Version |
| --- | --- | --- | --- | --- | --- |
| AgreeLab | beta 1j | ErrorRate | beta 1k | ScatterLab | beta 2n |
| AnovaLab | beta 1k | ExhibitLab | beta 1j | StatDist | v2.7o |
| BayesTree | beta 8l | FitCheck | beta 1k | StudRange | beta 15o |
| BiNorm3D | beta 1h | GaltonBoard | beta 3j | SurvLab | beta 1h |
| BurrLab | beta 1s | Norm3 | v2.4h | TDist3D | beta 1c |
| CICatcher | beta 2n | NormExplorer | beta 42k | TTestLab | beta 1m |
| CentralLimit | beta 3h | PowerViz | v2.5u | TTestLabG | beta 1j |
| ChiTable | beta 3n | RankLab | beta 1l | TestChooser | beta 2i |
| DNAMixLR | beta 3k | ResampLab | beta 1k | TrendTest | beta 3o |
| DataLoad | beta 1h | RiskLab | beta 1i | | |
| EpiStats | v1.7n | SampDist | v2.3l | | |

Each program's change note (`docs/changes/<Name>_<version>_CHANGES.md`) has its line numbers.

## What is here

| File | What it is |
| --- | --- |
| `make_round18.py` | The build of thirty programs, each from the version before, read from git (`BASE`, the commit before this round): the line, the pragma line for two, and Round 11's bump (the header, a history note, the version in every quoted string that holds it). It then runs `tools/make_tlg1_v5.py`, which builds TTestLabG beta 1j from TTestLab beta 1m. |
| `../verify_round18_settings_v1.py` | The verify script for all 31, with its saved output beside it. It also writes `gates/`. |
| `gates/` | `tools/ppl_gate_v1e.py` on each new version against its old one. |
| `vc_checks.txt` | What the Virtual Calculator did: the 31 Checks, and each program started on a calculator that had just been left in RPN entry, with a comma as the decimal point, Fixed 2 and Degrees. |
| `vc_checks_run.py`, `vc_runs_b.py`, `vc_runs_c.py`, `t69.py` | The scripts that drove the calculator for those, as they were run: the Checks, the plain runs, the runs that need a chooser or a form answered, and the small steps they share (they use `tools/vc_cloud_v1/vcdrive.py`). |
| `screens/` | Captures from the Virtual Calculator, each 320 × 240 as the calculator drew it. |
| `make_changes_r18.py` | Writes the 31 change notes from the programs, the verify script's output and `vc_checks.txt`. |

## To run again

From the repository's root, with hp-prime-kit at `$HPKIT` (see `CLAUDE.md`):

```
python3 verify/round18/make_round18.py OUTDIR                 # the 31 programs, a few seconds
python3 verify/verify_round18_settings_v1.py                  # about ten minutes
python3 verify/round18/make_changes_r18.py .                  # the change notes
```

## What the checks found

- **`verify/verify_round18_settings_v1.py`: 225 checks, 0 failed** (its output is beside it). B, the build makes each of the 31 filed programs byte for byte. T1, with the settings line, the history note and (for two) the new first line taken out, each new version differs from the old one only in the header's version line and in quoted strings that hold the version or its date: 33 settings lines in all. T2, the line is the first statement after the `LOCAL` lines of each start routine. T3, the first line of every program is the pragma line. T4, the line is ASCII. G, the gate passes each new version against its old one (`gates/`). S, the harness smoke test of each start routine (33 calls) ends as the old version's did, with no more warnings. H, started with HSeparator 4, HFormat 1, HAngle 1 and Entry 2, the harness holds 0, 0, 0 and 0 after each call. N, `fleet_names_v2.py` and `screen_text_v1.py` on the 31 programs: no collisions, no place against the rules.
- **The harness cannot show what the line does to a calculator.** It has no Home settings of its own and always writes a period (`tools/prime_facts_v1.py`, facts 5 and 6). H shows that the line runs.
- **The Virtual Calculator 2.4.2, 22 November, 17:36 to 18:59** (`vc_checks.txt`, `screens/`):
  - The Check said "No errors in the program" for all 31, NormExplorer and StudRange with their new first line among them.
  - Each of the 31 was then started with the calculator just left in RPN entry, with a comma as the decimal point, Fixed 2 and Degrees (`diagnostics/SetOdd_beta1.txt`, and Home Settings read to see it). Each showed its own opening page or menu, the calculator kept running, and Home Settings afterwards read Radians, Standard, 123,456.789 and Textbook, 31 times of 31.
  - NormExplorer beta 42k and StudRange beta 15o started. Their versions before had stopped the calculator at this step.
  - StatDist v2.7o, from the same four wrong settings, with 1234.5, 2.5 and 1236.25 typed: μ = 1,234.5, σ = 2.5, f(x) = 0.1249, P(X ≤ 1,236.25) = 0.758036. v2.7n had shown 0,758,036.
  - Norm3 v2.4h by the book's own line, with only the comma set: the same keys read `Norm3(100;15;130)` in Home, and the page read P(X ≤ x₀) = 0.9772, P(X > x₀) = 0.0228 and pdf = 0.0036. v2.4g had shown 0,9,772.
- **Starter pack v24** holds the 31 checked files (`docs/changes/StarterPack_v24_NOTES.md`), and the Prime Loader v2n is built from it.

## What was not done

- **No G1 and no G2.** Everything about a calculator in this round was seen on the Virtual Calculator under Wine. Each change note has the two-minute check for a real one.
- **No help page says that the program changes the calculator's settings.** The book says it. Adding a sentence to a help page changes a page the book prints word for word, and that is the author's choice.
- **A form that opens before the program's first line.** Norm3 takes three numbers, and the Program Catalog asks for them in a form of its own before `Norm3` runs, so that form is filled with the calculator's settings as they were. A line typed in Home, such as `Norm3(100, 15, 130)`, is read by Home before the program runs: in RPN entry Home refuses it, and with a comma as the decimal point it is typed `Norm3(100;15;130)`.
- **An app's own settings.** CentralLimit is an app, and an app has an Angle Measure and a Number Format of its own (Symbolic Setup). The line sets Home's. Whether an app setting that is not "System" overrides it inside the app's program was not tried.
- **The comma routine itself is unchanged.** It still takes a period for the decimal point. With the line in place a program never draws a number while Home's mark is a comma, so the routine is never asked to.
- The text-overlap walks and the monkey's runs were not made again: nothing a page draws differs but the version.
