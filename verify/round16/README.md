# Round 16: six tests added, and the credits of four more programs (15 November 2026)

Six additions to five programs, and one change of wording in four.

- **AnovaLab beta 1i**: Dunnett's test, every group against one control, with the p and the critical value computed for the data's own group sizes; a table page and a plot page. Numbers are no longer cut by the places they are drawn in.
- **RankLab beta 1j**: Page's *L* for an ordered trend, with its exact null distribution, and a runs test for randomness, with its own; four presets and two more kinds of "Use my data".
- **FitCheck beta 1i**: Dixon's outlier test for a sample of 3 to 30 values, its p computed and not read from a table; a preset.
- **CICatcher beta 2l**: a sixth interval, the tolerance interval x̄ ± k s, with the exact factor.
- **BiNorm3D beta 1g**: a third view, the target, with the circle that holds half of all pairs (the CEP), the ellipse that holds half too, and shots to count.
- **StatDist v2.7n, AgreeLab beta 1h, RiskLab beta 1h, BurrLab beta 1r**: their headers say, in plain verbs, what was done with the programs they stand beside.

Roger had a book of tables checked against fresh calculations on 15 November 2026 (Zwillinger & Kokoska, 2000; the report is `docs/dev/crc-table-check-2026-11-15.md`, its scripts in `verify/crc2000/`). The report ended with six suggestions for our programs, each a test whose printed table had been found wanting or missing. Roger, the same day: "Add all please", "Just do a really good job", and, of the credits, "reword as the others---look, be consistent throughout the book". Later that day: "interesting to refer back to the HP-67 programs if possible", which is why the runs test's example is Hewlett-Packard's own, from 1975.

## What is here

| File | What it is |
| --- | --- |
| `make_anovalab_1i.py`, `make_ranklab_1j.py`, `make_fitcheck_1i.py`, `make_cicatcher_2l.py`, `make_binorm3d_1g.py` | The five builds. Each change is an exact replacement in the version before, read from git (`BASE`, the commit before this round); a replacement that does not match exactly once stops the build. Tables a program needs (Gauss–Legendre nodes, the one-block counts of Page's *L*) and the header's file map are written by the build from Python. |
| `make_wording_r16.py` | The build of the four programs whose only change is their header's words: the replacements, then each program's next version. It stops if an old label is left at the head of a line. |
| `records_r16.py` | Gathers the round's other records for all nine: `gates/` (`tools/ppl_gate_v1e.py` on each new version against its old one), `helppages_before_r16.json` and `helppages_r16.json` (every help screen of the old and the new versions as the PC harness draws them), `helpcheck_r16.json` (every new help screen laid out at the glyph widths GlyphProbe_v1 measured), and `checks_r16.txt`: S, the harness smoke test beside the old version's; T, `tools/text_overlap_v1.py --walk` on both versions, the two reports kept in `overlap_<Name>.txt`; F, `tools/fleet_names_v2.py` over the fleet. |
| `make_changes_r16.py` | Writes `docs/changes/<Name>_<version>_CHANGES.md` for the four wording versions from those records. (The other five notes are written by hand.) |
| `linemap_r16.py` | `python3 linemap_r16.py NEW OLD`: the routines of NEW that are new or changed, with their line numbers. The change notes' tables come from it. |
| `help_AnovaLab_beta1i.txt`, `help_RankLab_beta1j.txt` | The two programs' help pages as their verify scripts drew them (`--save`), for the book. |
| `mk/` | The monkey's runs (`tools/monkey_chunks_v1.py`, base 16, `--lists`; FitCheck with `--writes D`): 1,000 of 1,000 OK for AnovaLab, RankLab, FitCheck, CICatcher and BiNorm3D. The four wording programs were not run again: only a version string differs among the lines the calculator runs. |
| `mk/reach_r16.txt` | How often the monkey's first 300 sessions of each program found the new pages by themselves (`tools/monkey_reach_v1.py`). Dunnett's table: 3; its plot: 0; a tolerance run: 0; the Outlier page's verdict: 19; Page's picture: 61; the runs test's picture: 56; the target view: 69. |
| `directed_r16.py`, `mk/directed/`, `mk/directed_r16.txt` | The answer to that: fourteen sets of 200 sessions, each started on one of the new pages by a scripted lead and then handed to the monkey (`tools/monkey_directed_v1.py`). 2,800 sessions, all OK. In ten sets the page was on the screen in all 200; in the four that go in through "Use my data" with the monkey's own lists, the program rightly refused many of the lists (the page in 84, 82, 68 and 111). |
| `vc_checks.txt` | The Checks and the runs on the Virtual Calculator, with every number read from the screen, and what the runs found. |
| `keyprobe_r16.txt` | The count of key presses that programs lost on the Virtual Calculator (`diagnostics/KeyProbe_beta1.txt`). |
| `screens/` | 161 captures from the Virtual Calculator, each 320 × 240 as the calculator drew it: every new page with its presets, every help page of the five programs, the closing lines, the two faults as first seen. The book's pictures are these, enlarged three times. |
| `../verify_AnovaLab_beta1i.py`, `../verify_RankLab_beta1j.py`, `../verify_FitCheck_beta1i.py`, `../verify_CICatcher_beta2l.py`, `../verify_BiNorm3D_beta1g.py`, `../verify_round16_wording_v1.py` | The six verify scripts (51, 57, 66, 37, 44 and 25 checks, 0 failed); their saved output is beside them. |

## To run again

From the repository's root, with hp-prime-kit at `$HPKIT` (see `CLAUDE.md`):

```
python3 verify/round16/make_anovalab_1i.py OUTDIR      # and the other four builds, and make_wording_r16.py
python3 verify/verify_AnovaLab_beta1i.py --save        # about 7 minutes; FitCheck's and RankLab's about 3 each, CICatcher's 2, BiNorm3D's under 1
python3 verify/round16/records_r16.py                  # about ten minutes
python3 verify/round16/directed_r16.py 200             # about three quarters of an hour; it resumes where it stopped
python3 verify/round16/make_changes_r16.py .           # after records_r16.py
```

## What the Virtual Calculator found that the harness could not

All nine programs were Checked and run on the HP Prime Virtual Calculator 2.4.2 (`vc_checks.txt`). Three things came of it.

1. **A `CHOOSE` title shows 31 characters and no more.** AnovaLab's box that asks before a long computation carries its estimate in the title, and "Dunnett d crit: about 14-41 s on a G1" lost its end. So had beta 1h's Tukey box, since it was written. The four titles now give the time without "about". The fact is in `tools/prime_facts_v1.py` (fact 4), and this round's five verify scripts check every title they meet.
2. **What a program returns is shown in a box of five lines of about 26 characters** after a run from the Program Catalog. CICatcher's first closing line for a tolerance run was longer and lost its end. It was shortened, and its verify script now lays the line out in a model of that box.
3. **Key presses that do nothing.** About one press in eight did nothing on the programs' pages. `KeyProbe` counted it: a loop that polls `GETKEY` loses presses on that calculator, and `WAIT(-1)` loses none. Whether a G1 or a G2 loses presses is not known, and nothing was changed for it in this round.

## What was read, and what the library in `D:\HP-Prime` holds

Searched on 15 November 2026 with `libsearch_v1.py` over `Library_Index.db`.

- **No HP Prime program in the library does any of the six.** "Dunnett" and "Jonckheere" appear only as names in our own TestChooser.
- **The runs test on HP calculators.** HP-65 Stat Pac 2 (© Hewlett-Packard Company 1975, part 00065-90275), program Stat 2-22A, "The Run Test for Randomness", with its example on p. 86; the HP-67/HP-97 Users' Library Solutions book *Test Statistics* (part 00097-90163; no date in its text), pp. 27 to 31, which calls its program a translation of the HP-65's and cites Freund and Williams, *Dictionary/Outline of Basic Statistics* (McGraw-Hill, 1966); the HP-41C's RUNTEST. They take n₁, n₂ and the number of runs, keyed in by the user, and return the mean, the standard deviation and z; for small samples they send the user to tables. Their example: a statistician at a roulette table, RRRR B RRR BBBBB RR BBB RR BB RRR with 0 and 00 left out, 14 red, 11 black and 9 runs, giving 13.32, 2.41 and −1.79. Those three numbers were checked by hand, and RankLab's preset shows them. The pages were read to see what the programs compute; none of their code is in RankLab.
- **Dunnett.** HP-41C Users' Library Solutions, *Applied Statistics I*, program STAT.08: after an ANOVA it gives the t of each group against the control, which the user compares with Dunnett's printed table (it cites Dunnett, 1964). No probability is computed. Read to see what it computes; none of its code is in AnovaLab.
- **Dixon.** Every "Dixon" in the HP statistics books is the textbook of Dixon and Massey, not the outlier test. The TI program STATLITE's "Outlier test" is the 1.5 × IQR fences. Nothing was read as code.
- **Page's *L*, tolerance factors, the CEP.** Nothing in the library. No TI program there does a runs test or Page's *L* either (searched by name and by text).
- **Page's *L*, on paper**: Page (1963), *Journal of the American Statistical Association*, 58(301), 216–230; Odeh (1977), *Communications in Statistics: Simulation and Computation*, 6(1), 49–61; Hollander, Wolfe & Chicken, *Nonparametric Statistical Methods* (3rd ed., 2014), section 7.2 with Comments 19 and 21; the notes of SciPy's `page_trend_test`.
- **The ozone data** of RankLab's preset are Table 7.2 of Hollander, Wolfe & Chicken (p. 301), a subset of Goldsmith and Nadel (1969), *Journal of the Air Pollution Control Association*, 19, 329–330: the change in airway resistance of four subjects after 0.1, 0.6 and 1.0 ppm of ozone. Roger's own 2021 homework used them.
- **Dixon's test, on the web**: which ratio for which n, from NIST's Dataplot reference manual ("DIXON TEST") and the manual of the R package `dixonTest`, which agree (3 to 7: r₁₀; 8 to 10: r₁₁; 11 to 13: r₂₁; 14 to 30: r₂₂). Dixon (1950), *Annals of Mathematical Statistics*, 21, 488–506; Dixon (1951), the same journal, 22(1), 68–78; Dean & Dixon (1951), *Analytical Chemistry*, 23, 636–638; McBane (2006), *Journal of Statistical Software*, 16(3), 1–9, for the distribution of the ratios as a double integral and the errors of the printed tables. Rorabacher (1991), *Analytical Chemistry*, 63(2), 139–146, was seen by title only; its volume and pages are still to be confirmed before the book cites it.

## Numbers worth keeping

Each is in a verify script, against exact arithmetic, SciPy or a second integral.

- **Dunnett, two-sided 5 % points** (three groups, the control among them; df 10, 20, 60): 2.5683, 2.3787, 2.2653. Insect sprays against Spray A: d crit 2.576. Mock jury against Average: 2.241. The 1970 lottery against December: 2.759.
- **Page's *L***: for 3 treatments and 4 blocks the 5 % point is 54; the ozone data give L = 48 with an exact p of 14/27 = 0.5185 conditional on its tie, where the untied null gives 83/144 = 0.5764 (what R and SciPy print). The 1970 lottery's months in order: L = 13,440, z = −3.314, p = 0.0005.
- **Runs test**: the roulette example's exact lower tail is 409/7,429 = 0.0551 and its two-sided p 0.1101, where the normal z of the HP book gives 0.0731. The 1970 lottery by day: 172 runs, exact two-sided p 0.2286.
- **Dixon**: Darwin's 15 differences, r₂₂ = 0.5935, one-end p 0.0161. The exact one-sided 5 % points of r₁₀ for n = 3 to 10: 0.9413, 0.7655, 0.6424, 0.5624, 0.5073, 0.4671, 0.4363, 0.4119. The printed Q table's 0.926 (n = 4, 99 %) cuts off 0.43 % where the exact point is 0.9207, and its 0.740 (n = 6, 99 %) stands for 0.7427: the two entries McBane names. Its 0.560 (n = 6, 90 %) cuts off 5.12 %; the exact point is 0.5624.
- **Tolerance factor** at 95 % confidence, n = 10: 2.8563, 3.3934 and 4.4369 for 90, 95 and 99 % of the population; Howe's approximation gives 2.8382, 3.3819 and 4.4446.
- **CEP**, in standard deviations: 1.1774 at ρ = 0, 1.1597 at 0.3, 1.1010 at 0.6, 0.9879 at 0.9.

## What the book needs from this round

The companion book prints the help pages word for word and names some menu items by number, so Draft 37 changes with the programs:

- the help pages of the five programs (AnovaLab 10, RankLab 10, FitCheck 12, CICatcher 7, BiNorm3D 6);
- menu numbers that moved: RankLab's Help and Quit (11 and 12); the six items after Dunnett's in AnovaLab's one-way menu; in FitCheck, the draft lottery and the illustrative binomial among the presets (8 and 9) and "My values in D1" in the Normality menu (4, or 5 once a sample is loaded);
- the program table's versions and line counts;
- the new tests, each with a worked example, in the appendix of advanced programs, and a sentence in their chapters that points there;
- that RankLab's exact p for Page's *L* with ties is conditional on the ties, where other software prints the untied one.

## A note on reading `checks_r16.txt`

The T lines give `text_overlap_v1.py`'s one-line summary. For a program with new pages the walk meets more screens than its old version's walk, so the two reports differ in their counts; what matters is that neither has a collision the other lacks. AnovaLab's "collisions 57" are in beta 1h's report too: rows of small text 11 px apart, which the tool's full report lists as tight rows (Round 15's README). The walk does not reach Dunnett's pages; AnovaLab's verify script lays those out itself (D1, 258 screens).

## Not done

Nothing in this round has run on a G1 or a G2.
