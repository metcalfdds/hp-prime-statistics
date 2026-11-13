# DataLoad beta 1g: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in DataLoad beta 1f (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 2/3 writes the Virtual Calculator's folder as Documents > HP Prime > Calculators > Prime.  The doubled backslashes of beta 1f may or may not print as one on the calculator (a backslash in a string is untested, Lessons Learned v7zq); the book printed them doubled.

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of DataLoad beta 1g that differ from DataLoad beta 1f: line 4 (comment); lines 21-25 (comment); lines 1013-1014 (code). Routines whose code changed, with the number of lines: dd_Help 2.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 2, before (beta 1f)

```text
DataLoad help 2/3: Getting data in
VIRTUAL CALCULATOR: the Data Loader web page
(hp-prime-statistics on GitHub) turns columns
pasted from Excel, SPSS or a CSV file into a
matrix file, M1.hpmat.  Close the calculator,
copy the file into Documents\\HP Prime\\
Calculators\\Prime, start it, run DataLoad.
G1 OR G2: in the Connectivity Kit, open the
calculator's matrix M1 and paste the columns,
or drag M1.hpmat onto it (not yet tested).
Or type a few values in the Matrix editor
(Shift 4) for M1.
Open Statistics 1Var once before the first load.
any key or tap = next page
```

### Screen 2, after (beta 1g)

```text
DataLoad help 2/3: Getting data in
VIRTUAL CALCULATOR: the Data Loader web page
(hp-prime-statistics on GitHub) turns columns
pasted from Excel, SPSS or a CSV file into a
matrix file, M1.hpmat.  Close the calculator,
copy the file into Documents > HP Prime >
Calculators > Prime, start it, run DataLoad.
G1 OR G2: in the Connectivity Kit, open the
calculator's matrix M1 and paste the columns,
or drag M1.hpmat onto it (not yet tested).
Or type a few values in the Matrix editor
(Shift 4) for M1.
Open Statistics 1Var once before the first load.
any key or tap = next page
```

## Checks

- `tools/ppl_gate_v1e.py` against DataLoad beta 1f: PASS. lint_ppl 4 problems, as in DataLoad beta 1f; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 3 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0)  PPLError: undefined variable: M1.
- `tools/text_overlap_v1.py --walk`: same report as the old version.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: the help page that changed.

## Unresolved

Whether a backslash in a PPL string prints once or twice on the calculator is still untested; no help page needs one now.
