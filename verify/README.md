# Verification scripts

One script per program version, named `verify_<Program>_<version>.py`. Each one does two things:

- **It checks the program's formulas against an independent implementation:** SciPy, statsmodels, SymPy, exact fractions, or brute-force enumeration.
- **It runs the program itself in the PC harness** (`tools/ppl_run_v3e.py`; older scripts name v3a to v3d), scripted, to check that it produces those numbers on its own pages.

**Scripts that import `ppl_run_v3d`** (BayesTree beta 8c, CICatcher beta 2b, CentralLimit beta 3b, ChiTable beta 3c, DNAMixLR beta 3b, EpiStats v1.7b, ErrorRate beta 1b, GaltonBoard beta 3c, PowerViz v2.5b, ScatterLab beta 2b, StatDist v2.7c, StudRange beta 15b, TrendTest beta 3c) run unchanged on `ppl_run_v3e`: change `v3d` to `v3e` in the import. All fourteen of the fleet's scripts that import v3d, these thirteen and one for a program held back from this repository, were re-run that way on 17 October 2026 with the same results; only the PC timings and the order of one printed set differed.

**`verify_CASProbe_beta1d.py`** imports `ppl_run_v3e` itself and reads every file from its own folder: the probe, the harness, and the two versions it compares, CASProbe beta 1c (the one the emulator ran, never in this repository) and beta 1b (in this repository's history). Its one comparison with `ppl_run_v3d` is skipped, with a note, when v3d is not there.

**The 19 October 2026 versions** (BayesTree beta 8e, BiNorm3D beta 1a, Burr3 v2.4b, CICatcher beta 2c, CentralLimit beta 3c, ChiTable beta 3d, DNAMixLR beta 3c, EpiStats v1.7d, ErrorRate beta 1d, Norm3 v2.4b, NormExplorer beta 42a, PowerViz v2.5d, SampDist v2.3b, ScatterLab beta 2c, StatDist v2.7e, StudRange beta 15d, TestChooser beta 2a, TrendTest beta 3d) import `ppl_run_v3e`. Each also runs, as a regression test, the independent check script written for that program by the fleet review of 19 October 2026: the checks that failed on the old version pass on the new one, and the script shows the old version failing them. Every one of these scripts was re-run in a separate folder after it was written, with the same result. GaltonBoard beta 3d changes only its header, so beta 3c's script stands.

Where a script's output was saved, it sits beside the script as `*_output.txt`. The same output is quoted in the program's file in `docs/changes/`.

**These scripts ran in the development environment, and most of them name its folders at the top:**
- the program file;
- the harness;
- hp-prime-kit.

To rerun one, edit those paths to point at this repository's `programs/` and `tools/` and your copy of hp-prime-kit. They need Python 3 with SciPy (and statsmodels or SymPy where they import them), and Giac's `icas` for the CAS checks.

**`verify_TrendTest_beta3f.py`** (22 October 2026) likewise runs from `verify/` by relative path and reads beta 3e from git history: `trUpper` against SciPy at df 1 to 12, and `trCompute` on six tables in beta 3e and 3f, three of them extreme enough that beta 3e prints p = 0. Output beside it.

**`verify_StudRange_beta15e.py`** (22 October 2026) imports `ppl_run_v3e` from this repository's `tools/` folder by relative path, so it runs from `verify/` as is, given hp-prime-kit (`HPKIT`, or the Community_Library zip) and SciPy. It reads beta 15d from git history when `programs/StudRange_beta15d.txt` is absent. Section A shows where the PPL engine's 32-node outer grid loses the density of s (df about 50 to 100); section B builds the plot cache on the PPL path with beta 15d and beta 15e and checks each against SciPy. Its output is beside it.

**The 20 October 2026 symbol versions** (BiNorm3D beta 1b, Burr3 v2.4c, CICatcher beta 2d, CentralLimit beta 3d, ChiTable beta 3e, DNAMixLR beta 3d, EpiStats v1.7e, ErrorRate beta 1e, GaltonBoard beta 3e, NormExplorer beta 42c, PowerViz v2.5e, SampDist v2.3c, ScatterLab beta 2d, StatDist v2.7f, TestChooser beta 2b, TrendTest beta 3e) change only the text on screen: symbols instead of spelled-out names. They have no verify scripts of their own. `check_glyph_sweep.py` and `check_glyph_sweep2.py` (outputs beside them) show that, with every `CHAR()` build folded back into its string and every string and comment blanked, each file's code is line for line its 19 October version's, apart from five listed display lines; that no line building CAS text changed; and that no literal used in a comparison changed. Each program's 19 October script was then run on the new text: `Glyph_Sweep_2026-10-20_harness.txt` says, program by program, which checks fail and why. They fail by design wherever they look for the old wording, the old version string or "exactly these lines changed"; none reports a wrong number, an error or a stall.


**The eight October 2026 programs** (RankLab, AnovaLab, SeizureLab, SurvLab, FitCheck, AgreeLab and RiskLab beta 1a; ResampLab beta 1b, with its beta 1a script): `verify_<Name>_beta1a.py` and its saved output. These were written and run in the build workspace, not in this repository's layout: they expect the programs, `tools/` and the harness `ppl_run_v3e.py` beside them, `HPKIT` set to hp-prime-kit, and the preset data files named in `docs/data/`. The independent second reviews they answer are `docs/dev/review2-<Name>-beta1.md`.
