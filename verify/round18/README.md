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
| `monkey_r18.py`, `monkey_r18.txt` | The monkey, 23 November: 1,000 runs for each of the 30 programs the PC harness can drive, and every run that did not end OK replayed with its own seed on the version before; `monkey_r18.txt` is its summary, one line a program. |
| `monkey_r18_slow.py` | The 44 runs that the monkey called FREEZE at 30 s, replayed with 240 s. |
| `probes/` | Three small probes of what the monkey found, each with its output beside it: `probe_statdist_cas.py`, `probe_dataload_bins.py` and `probe_epistats_mh.py`. |
| `mk/` | The runs: `mk/<Name>.jsonl` (one line a run), `mk/not_ok.json` (the runs that did not end OK, and whether the version before did the same) and `mk/slow_replays.jsonl`. |

## To run again

From the repository's root, with hp-prime-kit at `$HPKIT` (see `CLAUDE.md`):

```
python3 verify/round18/make_round18.py OUTDIR                 # the 31 programs, a few seconds
python3 verify/verify_round18_settings_v1.py                  # about ten minutes
python3 verify/round18/make_changes_r18.py .                  # the change notes
python3 verify/round18/monkey_r18.py                          # the monkey, about three and a half hours on two cores
python3 verify/round18/monkey_r18_slow.py                     # its FREEZE runs again with 240 s, about twenty minutes
```

Both monkey scripts resume where they stopped, because every run is written to `mk/` as it ends.

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

## What the monkey found (23 November 2026)

`monkey_r18.py` ran `tools/monkey_chunks_v1.py` (base 18, `--lists`, 150 events a run) 1,000 times on each of the 30 programs the PC harness can drive, with 30 s a run (GaltonBoard, which is paced by the clock, 120 s) and `--writes` as `docs/dev/monkey-fleet-2026-11-01.md` gives it. CentralLimit is an app and is out of the harness's reach. Every run that did not end OK was then run again, with its own seed, on the version before round 18 (read from git at `3a121b6`).

- **26 programs: 1,000 of 1,000 OK.**
- **Four programs had runs that did not end OK, 46 runs in all, and every one of them did the same on the version before**, so round 18's line made none of them (`monkey_r18.txt`, `mk/not_ok.json`).

| Program | Not OK | What it was |
| --- | --- | --- |
| StudRange beta 15o | 43 FREEZE | Slow pages, not stuck ones. With 240 s each (`monkey_r18_slow.py`), all 43 ended OK, in 30 to 140 s (median 47 s). StudRange's plots are slow in the PC harness, and the fleet's monkey has given it 240 s a run before (`docs/dev/monkey-fleet-2026-11-01.md`); this script gave it 30 s. |
| StatDist v2.7o | 1 FREEZE, seed 18000984 | The Formula page (CAS) for Student's t with a df such as 17.83 or 206.3, which Giac on the PC did not finish in ten minutes. Not known yet whether the calculator waits too; below. |
| DataLoad beta 1h | 1 CRASH, seed 18000713 | The harness's binary arithmetic, not the calculator's; below. Nothing to change. |
| EpiStats v1.7n | 1 CRASH, seed 18000612 | A division by zero that would most likely stop the calculator too, with person-times no study has; below. |

### StatDist: the Formula page (CAS) for Student's t with a df such as 17.83

Seed 18000984 chose Student's t with df = 206.3 and then Plot options, 2, "Formula page (CAS)". With 240 s it still did not end: the harness stops any one CAS call at 60 s, and Giac had not finished E[X²], the integral of x² f(x) from −∞ to ∞ (`st_FmCont` → `st_FmAsk` → `st_Cas`). `probes/probe_statdist_cas.py` asked Giac 1.9.0 on the PC the same integral, written as the program writes it, for seven df:

| df | What Giac gave for E[X²] |
| --- | --- |
| 5, 24 | 5/3 and 12/11, at once |
| 206 | 103/102, in 0.9 s |
| 2.5, 9.5 | the integral back undone, in 0.2 s and 0.1 s, so the page says "no closed form shown" and gives the program's own value |
| 17.83 | nothing in 600 s |
| 206.3 | nothing in 600 s (E[X] came back as 0 in 4.2 s) |

A df like 17.83 is what Welch's *t*-test gives, so a student may well type one, and the page's own words are "it can take a few seconds". What a calculator does is not known: the program asks the CAS inside `IFERR`, so it would not stop with an error, but it may wait. Whether the Prime's own CAS takes as long, and whether the ON key ends the wait, has not been tried on the Virtual Calculator, a G1 or a G2. That is the next step, and if it waits there, how to change the page is the author's choice (for one, ask the CAS for E[X²] only when df is a whole number or a half, and otherwise go straight to "no closed form shown" and the program's own value, ν/(ν − 2)).

### DataLoad: a histogram of a column with one value, or all its values the same

Seed 18000713 left a list of one value in D1 (the monkey's "one" lists) and chose to look at the data, and `dd_DrawHisto` stopped at "index 0 out of range in hc (1..0)". With one value, or every value v the same, the routine takes hw := MAX(1, |v|/10) as the bin width, hs := FLOOR(v/hw)·hw as the first bin's start and FLOOR((v − hs)/hw) + 1 bins. The harness counts in binary doubles, in which |v|/10 is rounded, so FLOOR(v/hw)·hw can come out a hair above v, and then there are no bins. The Prime counts in 12-digit decimals, in which dividing by 10 only moves the decimal point, so FLOOR(v/hw)·hw is v and there is one bin. `probes/probe_dataload_bins.py`: of 437 such columns, the harness stopped on 28 (the smallest |v| among them 1,004.18169); the same three lines of arithmetic in binary doubles give no bin for the same 28, and in 12-digit decimals for none. So nothing is changed.

### EpiStats: the stratified rate ratio with a person-time of 1E−300

Seed 18000612 typed a person-time of 1E−300 into one stratum of the stratified analysis, and `es_MHCalc` divided by zero in the Mantel–Haenszel rate ratio's variance (`mcV := mcPR / (mcR * mcSS)`). `probes/probe_epistats_mh.py` shows how, with two strata, each with 1 case in 100,000 person-time on one side and 0 cases in 1E−300 on the other, the other way round in the second: the two sums mcR and mcSS are each 1E−305, and their product, 1E−610, is far below the smallest number the harness keeps (about 5E−324), so it becomes 0. The Prime overflows at 1E499 (Lessons Learned v7zy §3); if its smallest number is 1E−499, as that suggests, the product is 0 there too, but the small end has not been checked. A division by zero stops a program on the Prime with "Error: X/0" (§3), so this would most likely stop the calculator too; it has not been tried there. With 0.001 in place of 1E−300 the variance is 200,000,000, and the interval's EXP overflows: in the harness that is an error, and on the Prime an overflow is ∞ with no error (§3), so the interval's upper end would be ∞. The same line is in v1.7e, the oldest EpiStats in the repository's history, so it is not new.

A person-time of 1E−300 or of 0.001 next to 100,000 is no study's, and the program's range for a person-time is 0 to 100,000. Lessons Learned already has the rule that fits ("Check a ratio before anything is squared or divided", §11, from EpiStats v1.7h's sample sizes). Two ways to keep to it, which are the author's choice: refuse a person-time below some smallest value, with a sentence that says the range; or keep every value, compute the variance as (mcPR / mcR) / mcSS, and show the interval as "cannot be computed" when its ends would overflow. Either one is a new version of EpiStats (v1.7o) with its own round.

## What was not done

- **No G1 and no G2.** Everything about a calculator in this round was seen on the Virtual Calculator under Wine. Each change note has the two-minute check for a real one.
- **No help page says that the program changes the calculator's settings.** The book says it. Adding a sentence to a help page changes a page the book prints word for word, and that is the author's choice.
- **A form that opens before the program's first line.** Norm3 takes three numbers, and the Program Catalog asks for them in a form of its own before `Norm3` runs, so that form is filled with the calculator's settings as they were. A line typed in Home, such as `Norm3(100, 15, 130)`, is read by Home before the program runs: in RPN entry Home refuses it, and with a comma as the decimal point it is typed `Norm3(100;15;130)`.
- **An app's own settings.** CentralLimit is an app, and an app has an Angle Measure and a Number Format of its own (Symbolic Setup). The line sets Home's. Whether an app setting that is not "System" overrides it inside the app's program was not tried.
- **The comma routine itself is unchanged.** It still takes a period for the decimal point. With the line in place a program never draws a number while Home's mark is a comma, so the routine is never asked to.
- The text-overlap walks were not made again, because nothing a page draws differs but the version. The monkey's runs were made again on 23 November, and what they found is above.
