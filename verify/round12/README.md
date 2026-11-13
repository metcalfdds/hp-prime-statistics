# Round 12: help-page fixes from the book's pre-submission read (13 November 2026)

The book *Statisticles* prints every program's help pages exactly as the programs show them. Reading Draft 27 line by line for submission found wording faults in the help pages of twelve programs, and places where Round 11's re-wrap had run a list's items together: a label and its first item on one line, two keys in one sentence with nothing between them, three drags in one sentence, a hyphenated name split by a space. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case".

## What is here

| File | What it is |
| --- | --- |
| `make_round12.py` | The build. Each change is an exact replacement in the version before, read from git (`BASE`, the commit before this round); a replacement that does not match exactly once stops it. Then each program gets its next version: the header line, a history note, and every version string in a literal (with its date), as Round 11's bump did. |
| `checks_r12.py`, `checks_r12.txt` | The harness smoke test (main routine, idle key Esc) of each new version beside its old one; `tools/text_overlap_v1.py --walk` on both; `tools/fleet_names_v2.py` over the fleet with the new versions. |
| `helppages_before_r12.json`, `helppages_r12.json` | Every help screen of the old and the new versions, as the PC harness draws them (`verify/round11/helpdump_r11.py`). |
| `helpcheck_r12.json` | Every help screen of the new versions laid out at the glyph widths GlyphProbe_v1 measured (`verify/round11/helpcheck_r11.py`). |
| `gates/` | `tools/ppl_gate_v1e.py` on each new version against its old one. |
| `mk/` | The monkey's runs (`tools/monkey_chunks_v1.py`, base 12, `--lists`) for the four programs whose help pages were laid out again: SampDist, PowerViz, RankLab and BayesTree. |
| `vc_checks.txt` | The Checks on the Virtual Calculator. |
| `screens/` | Help pages as the Virtual Calculator showed them (320 × 240, enlarged three times), and RankLab's Check after the fix. |
| `../verify_round12_v1.py` | The round's verify script; its saved output is beside it. |

## The changes

| Program | Version | Help page | Change |
| --- | --- | --- | --- |
| AnovaLab | beta 1g | 4/9 | "Scheffé" with its accent (CHAR(233)); the menus keep "Scheffe" |
| BayesTree | beta 8k | 2/5 | the three sets of soft keys on lines of their own, each key as its label reads ("Test 2"); "Esc quits BayesTree." in one piece |
| CICatcher | beta 2j | 2/6 | two sentences where "so ... so" ran together |
| DataLoad | beta 1g | 2/3 | the folder as Documents > HP Prime > Calculators > Prime, with no backslashes |
| EpiStats | v1.7l | 1/15, 11/15 | "Mantel-Haenszel" in one piece; the NPV formula and the next sentence on separate lines |
| FitCheck | beta 1g | 4/8 | a comma after "In the two-digit test" |
| PowerViz | v2.5s | 3/7 | the three drags on three lines; "the nearest of the seven α values (0.001 to 0.2)" for "the nearest of those values" |
| RankLab | beta 1h | 2/7, 5/7 | one key per line; the halo preset is "the first 8 of those judges"; and the fault the monkey found (below) |
| RiskLab | beta 1g | 2/8 | "penalized" |
| SampDist | v2.3k | 1/2, 2/2 | lists again: each label on a line of its own, its items indented below |
| StatDist | v2.7m | 1/4 | "then", not "Then", after a comma |
| TTestLab | beta 1j | (menu, flowchart, a note) | no figure number of the lecture note: the menu item "Choose the test (flowchart)", as in TTestLabG; the flowchart's title "Which t-test?"; "separate if not." |

## The monkey's finding

The first 1,000 runs on RankLab (base 12) ended in 3 crashes, all "index out of range in cgN" in `rk_ChooseG`, called by Mann-Whitney's `rk_PickTwo`. The cause was older than this round: Your data > Groups emptied the groups (values, group numbers, names) before it found that fewer than two columns were filled, refused, and kept the old group count, so a Mann-Whitney afterwards asked for names that were not there. RankLab beta 1h reads the columns into locals first, and the groups change only when there are two or more. `monkey_v1b.py --replay` on the three seeds did not repeat the crashes, so the fault was confirmed by a scripted harness check instead: `verify_round12_v1.py`'s X1 shows it on beta 1g, every time, and its absence on beta 1h; `mk/RankLab_beta1h_before_fix.jsonl` holds the runs that found it, `mk/RankLab.jsonl` the 1,000 runs of the fixed version.

## Results

- `make_round12.py`: twelve new versions, every replacement matched once. `verify_round12_v1.py`: 74 of 74 checks PASS (T1 the build makes each file byte for byte; T2 nothing else differs; T3 the help dumps; T4 the layout; T5 the gate; X1 the RankLab fault on beta 1g and not on beta 1h).
- Gate: PASS for all twelve; lint_ppl's problem counts are the old versions' counts. `tools/fleet_names_v2.py` over the 31 newest files: 0 collisions, 0 untagged; `tools/case_scan_v1.py`: clean.
- The help dumps: the only screens that changed are the ones listed above, and they changed only as listed; no help page gained or lost a page.
- `helpcheck_r12.json`, at the measured glyph widths: no reports, apart from StatDist's known one (the harness cannot call `st_ABHelp` without its argument).
- The harness smoke test: the same as the old versions (no warnings; DataLoad's "undefined variable: M1" with no matrix loaded, as before).
- `tools/text_overlap_v1.py --walk`: the same report as the old version for eleven programs. SampDist's help pages, whose rows are 11 px apart as before, gained four "rows too close" reports and lost two straddles and two overruns; the tool's model of font 1 is about 40 % wider than the calculator draws it, and the layout check at the measured widths reports nothing.
- The monkey: 1,000 of 1,000 runs OK for SampDist v2.3k, PowerViz v2.5s, BayesTree beta 8k and the fixed RankLab beta 1h (base 12, `--lists`).
- Virtual Calculator 2.4.2 (build 2026-09-09): "No errors in the program" for all twelve (`vc_checks.txt`); AnovaLab's "Scheffé" and SampDist's two list pages read on its screen (`screens/`). Starter pack v17 carries the calculator's checked files; the Prime Loader v1o is built from it (59 PASS, 0 FAIL).
- Not yet run on a G1 or a G2.

## To run it again

`python3 verify/verify_round12_v1.py` from the repository's root, with hp-prime-kit in `HPKIT` (CLAUDE.md, "Setting up a fresh session"). The build alone: `python3 verify/round12/make_round12.py OUTDIR`.
