# EpiStats v1.7l: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in EpiStats v1.7k (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 1/15: "Mantel-Haenszel" in one piece (Round 11's re-wrap had left a space after the hyphen).  Help page 11/15: the NPV formula ends its line, and "A rare disease makes most positives false." starts the next.

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of EpiStats v1.7l that differ from EpiStats v1.7k: line 3 (comment); lines 31-34 (comment); line 747 (code); line 5933 (code); line 5938 (code); lines 6103-6104 (code). Routines whose code changed, with the number of lines: EpiStats 1, es_Help_About 2, es_Help_Prev 2.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 1, before (v1.7k)

```text
EpiStats help 1/15: About EpiStats
EpiStats v1.7k
Comprehensive biostatistics and epidemiology calculator.
Modules: 2×2 tables, risk analysis, diagnostic tests, incidence
rates, stratified (Mantel- Haenszel) analysis, and sample size.
From Home: EpiStats2x2(a,b,c,d) opens the 2×2 results at once
and returns Fisher's p.
Results are kept in Home as EP_ variables (help page 8).  Touch
and keys: help pages 9 to 13; exact answers: pages 14 and 15.
any key or tap = back
```

### Screen 1, after (v1.7l)

```text
EpiStats help 1/15: About EpiStats
EpiStats v1.7l
Comprehensive biostatistics and epidemiology calculator.
Modules: 2×2 tables, risk analysis, diagnostic tests, incidence
rates, stratified (Mantel-Haenszel) analysis, and sample size.
From Home: EpiStats2x2(a,b,c,d) opens the 2×2 results at once
and returns Fisher's p.
Results are kept in Home as EP_ variables (help page 8).  Touch
and keys: help pages 9 to 13; exact answers: pages 14 and 15.
any key or tap = back
```

### Screen 11, before (v1.7k)

```text
EpiStats help 11/15: PPV vs prevalence, ROC
Diagnostic module, page 4: PPV (magenta) and NPV (blue) for
THIS test at every prevalence.
Drag along the plot or the slider, or use the arrows (1 %;
Up/Down 10 %); 0 = your sample's prevalence, the red marker.
+/- turn the page.
PPV = sens×p / (sens×p + (1-spec)(1-p))
NPV = spec(1-p) / (spec(1-p) + (1-sens)p) A rare disease makes
most positives false.
Page 5: the test as a point on the ROC square:
LR+ = slope of the line from (0,0), LR- = slope of the line from
(1,1); dotted = chance.
any key or tap = back
```

### Screen 11, after (v1.7l)

```text
EpiStats help 11/15: PPV vs prevalence, ROC
Diagnostic module, page 4: PPV (magenta) and NPV (blue) for
THIS test at every prevalence.
Drag along the plot or the slider, or use the arrows (1 %;
Up/Down 10 %); 0 = your sample's prevalence, the red marker.
+/- turn the page.
PPV = sens×p / (sens×p + (1-spec)(1-p))
NPV = spec(1-p) / (spec(1-p) + (1-sens)p)
A rare disease makes most positives false.
Page 5: the test as a point on the ROC square:
LR+ = slope of the line from (0,0), LR- = slope of the line from
(1,1); dotted = chance.
any key or tap = back
```

## Checks

- `tools/ppl_gate_v1e.py` against EpiStats v1.7k: PASS. lint_ppl 8 problems, as in EpiStats v1.7k; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 15 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 18/912 collisions 0 (firm 0) straddles 0 overruns 0 ghosts 0.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: Help pages 1/15 and 11/15.
