# Verification scripts

One script per program version, named `verify_<Program>_<version>.py`. Each one does two things:

- **It checks the program's formulas against an independent implementation:** SciPy, statsmodels, SymPy, exact fractions, or brute-force enumeration.
- **It runs the program itself in the PC harness** (`tools/ppl_run_v3c.py`; older scripts name v3a or v3b), scripted, to check that it produces those numbers on its own pages.

**Scripts that import `ppl_run_v3b`** (CICatcher beta 2a, CentralLimit beta 3a, DNAMixLR beta 3a, EpiStats v1.7a, ErrorRate beta 1a, PowerViz v2.5a, ScatterLab beta 2a) run unchanged on `ppl_run_v3c`: change `v3b` to `v3c` in the import. All seven were re-run that way on 17 October 2026 with the same results; only the timings differed.

Where a script's output was saved, it sits beside the script as `*_output.txt`. The same output is quoted in the program's file in `docs/changes/`.

**These scripts ran in the development environment, and most of them name its folders at the top:**
- the program file;
- the harness;
- hp-prime-kit.

To rerun one, edit those paths to point at this repository's `programs/` and `tools/` and your copy of hp-prime-kit. They need Python 3 with SciPy (and statsmodels or SymPy where they import them), and Giac's `icas` for the CAS checks.
