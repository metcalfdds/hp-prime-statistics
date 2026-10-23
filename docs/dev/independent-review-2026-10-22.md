# Independent review, 22 October 2026

*A second look at the 20 October fleet, in a fresh environment, with the author's verify scripts rerun from his working folders. Written with AI assistance (Anthropic Claude, Claude Code cloud session); the decisions and the merges are the author's.*

## Setting

A clean Linux container with nothing of the author's development environment in it: Python 3.13, SciPy 1.18.1, statsmodels 0.15, SymPy 1.14, Giac 1.9.0.93 (`icas`, from the Ubuntu package), and hp-prime-kit cloned fresh from GitHub. The repository as of commit 98b8e39 (the 20 October symbol versions). The author's working folders arrived later as a 21.7 MB zip of every `.py`, `.txt`, `.md` and `.json` file under `D:\HP-Prime`.

## 1. The gate and the fleet

`tools/ppl_gate_v1c.py` on all 19 programs, with the kit present (the repository's own notes had skipped the two kit steps where the zip was absent): **19 PASS**. hp-prime-kit's linter: 0 errors on every file. Full-parse failures only on the documented tool limits (the √ character, `#RRGGBB:24h` colours, forward declarations, a file-level LOCAL after an EXPORT list). `fleet_names_v2.py`: 19 files, 1,132 routine names, 0 collisions, 0 built-in matches.

`verify/check_glyph_sweep2.py`, rerun on the 19 October versions pulled from git history: the same line counts and the same "0 failures" as the saved output, pair for pair (FDAES and NormExplorer beta 42b are not in the repository, so those two pairs could not be run).

## 2. Harness smoke test

Every program loaded in `ppl_run_v3e` with zero warnings and ran its main routine to the end with Esc pressed whenever it idled: no `PPLError` anywhere. Burr3 and Norm3 stop at once because they take arguments, by design.

## 3. The programs' own routines against SciPy and statsmodels

281 comparisons, calling the routines through the harness with arguments or with the program's state set directly:

| Program | Routines | Reference | Result |
| --- | --- | --- | --- |
| EpiStats | es_WilsonCI, es_FisherExact, es_CondOR, es_McNemar, es_CPInt (exact and mid-p) | statsmodels, SciPy, a root-finder | all agree |
| ChiTable | csWils, csFisher, csCompute (X², G², adjusted residuals, V, Yates, Newcombe, Woolf OR and RR) | SciPy, statsmodels | all agree |
| TrendTest | trCompute (trend, Pearson, slope) | own implementation of Mantel's form | all agree |
| DNAMixLR | dmProb with θ, known contributors and typed alleles | brute-force enumeration of every allele sequence | all agree to 1E-9 |
| ErrorRate | erlBound, erlBetaCdf, erlBetaQ | SciPy beta | all agree |
| Burr3 | b3_bcdf, b3_bpdf | SciPy burr12 | all agree |
| StatDist | st_betaI, st_gammaP, st_gammaQ, st_lngamma | SciPy special | all agree |
| StudRange | sr_SRCDF, sr_SRCrit (PPL engine) | SciPy studentized_range | see below |

Two differences are conventions, not errors: `es_McNemar` returns 0 and p = 1 when the discordant cells are equal, as R's `mcnemar.test` does (statsmodels applies the correction anyway); `trCompute` uses Mantel's N - 1 variance, which is the larger variance, so its statistic is the smaller: R's `prop.trend.test` prints Armitage's form, larger by N/(N - 1), as the program's own comments say.

## 4. The one wrong number: StudRange's PPL plot cache

`sr_Cache` passed a 32-node outer Simpson grid over s for df 8 and above. The density of s narrows as df grows, and from df about 50 to 100 the grid steps over it: `sr_SRCDF` at SciPy's 95th percentile returned 0.968 at df 90 (true 0.950), 0.943 at df 70. The cached CDF behind the Plot page was off by up to 2 percentage points; the Critical value and P-value pages, which pass 64 nodes, were exact. Only the PPL fallback is affected. **Fixed as StudRange beta 15e** (64 nodes at every df; `docs/changes/StudRange_beta15e_CHANGES.md`, `verify/verify_StudRange_beta15e.py`), merged the same day.

## 5. The author's verify scripts, rerun

The 19 October verify scripts hard-code the author's folders (`/home/claude/work/out`, `fix19`, `review`, `harness`) and need his review check scripts and earlier program versions. Those came in the zip; the layout was rebuilt from it and from git history, and every script was run unchanged except where noted.

| Result | Scripts |
| --- | --- |
| **Same result as the saved output** (13) | BiNorm3D, ScatterLab, TestChooser, Norm3, Burr3, CentralLimit, CICatcher, DNAMixLR, ErrorRate, NormExplorer, PowerViz, StudRange, TrendTest (3 checks fewer: they compare harness v3d, not in the zip) |
| **Pass except the checks against a version missing from both the zip and git** (3) | ChiTable 6,929 of 6,931 (beta 3a); GaltonBoard 4,195 of 4,203 (beta 3a); StatDist all but 3 (v2.7a). The next version was substituted so the rest could run, and only the comparisons with the missing one fail. |
| **Partly run** (2) | EpiStats 300 of 302 (the v1.6 suite needs harness v3d); BayesTree 86 of 285 (83 pass, 3 are beta 8a comparisons), then a stall in a section that needs harness v3d |
| **Could not run** (2) | SampDist (needs `ppl_harness_v1.py`); CASProbe (needs CASProbe beta 1c) |

No check that could run against the real files failed. The files the zip lacks: `ppl_run_v3d.py`, `ppl_harness_v1.py`, ChiTable beta 3a, GaltonBoard beta 3a, StatDist v2.7a, BayesTree beta 8a, CASProbe beta 1c.

## 6. A nit, fixed as TrendTest beta 3f

TrendTest's Pearson and departure p-values were `1 - CHISQUARE_CDF`, exactly 0 on the Prime once the tail is below about 5E-13. Beta 3f computes them as a finite sum of positive terms (`docs/changes/TrendTest_beta3f_CHANGES.md`).

## What was not done

Nothing here ran on the HP Prime Virtual Calculator or on a G1 or G2. Both new versions have device checklists in `docs/changes/`.
