# FitCheck beta 1g: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in FitCheck beta 1f (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 4/8: a comma after "In the two-digit test".

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of FitCheck beta 1g that differ from FitCheck beta 1f: lines 17-19 (comment); line 3132 (code); line 3161 (code). Routines whose code changed, with the number of lines: fc_Help 1, fc_Opening 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 4, before (beta 1f)

```text
FitCheck help 4/8: Benford, Poisson, binomial
BENFORD'S LAW.  In many collections of amounts 
spread over several powers of ten the leading 
digit d turns up with probability log₁₀(1 + 
1/d): a 1 about 30.1% of the time, a 9 only 
4.6%.  The first two digits: log₁₀(1 + 1/(10a 
+ b)).  In the two-digit test numbers below 10 
are left out (they have no second digit).  
Nigrini's MAD is the average gap between the 
actual and Benford's proportions.  The orange 
curve on the bars is Benford's law.
POISSON: λ is estimated as the mean count; the 
last cell is the tail (K or more), so the E 
add up to N; df = k - 2.  BINOMIAL: p 
estimated (df = k - 2) or typed (df = k - 1).
page 4 of 8, any key or tap = next, Esc = menu
```

### Screen 4, after (beta 1g)

```text
FitCheck help 4/8: Benford, Poisson, binomial
BENFORD'S LAW.  In many collections of amounts 
spread over several powers of ten the leading 
digit d turns up with probability log₁₀(1 + 
1/d): a 1 about 30.1% of the time, a 9 only 
4.6%.  The first two digits: log₁₀(1 + 1/(10a 
+ b)).  In the two-digit test, numbers below 
10 are left out (they have no second digit).  
Nigrini's MAD is the average gap between the 
actual and Benford's proportions.  The orange 
curve on the bars is Benford's law.
POISSON: λ is estimated as the mean count; the 
last cell is the tail (K or more), so the E 
add up to N; df = k - 2.  BINOMIAL: p 
estimated (df = k - 2) or typed (df = k - 1).
page 4 of 8, any key or tap = next, Esc = menu
```

## Checks

- `tools/ppl_gate_v1e.py` against FitCheck beta 1f: PASS. lint_ppl 9 problems, as in FitCheck beta 1f; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 8 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 97/352 collisions 0 (firm 0) straddles 0 overruns 0 ghosts 0.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: the help page that changed.
