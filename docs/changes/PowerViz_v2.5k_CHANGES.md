# PowerViz v2.5k: changes

*31 October 2026, late afternoon. Built from v2.5j by `make_v25k.py` (9 exact replacements, each required to match once). 3,845 lines: 2,400 of code and 1,278 of comments. v2.5j was filed but not committed; this version carries it (see `PowerViz_v2.5j_CHANGES.md`).*

## Why

Roger compared PowerViz with his SPSS output, where Levene's F is 6.847 with p = .009, and asked whether ours was different.

**The answer:**
- It is the same test. The two-samples page works out Levene's F from the absolute deviations from the group means, as SPSS does, and verify F2 checks it against SciPy on 203 data sets.
- But a Levene F needs every score. The main screen and the power page have only the means, SDs and n's, so neither can give SPSS's 6.847.

Roger: "we're not putting all that raw data in a calculator -- so maybe we either need to delete our Levene's section or give a really good explanation as to what is going on". Asked which, he chose to **keep both pages and explain**.

## What changed (line numbers are v2.5k's)

### The power page opens with what it is, and is not (`pv_LvPage`, 2893; the new screen at 2904)

With Roger's numbers, the screen reads:

```
Would Levene's test notice?
A Levene F, as SPSS or R prints it, comes from
every score (here 416): how far each one sits
from its group's mean. PowerViz has only the
means, SDs and n's, so it cannot work out that
F, and it does not try.
This page asks a planning question instead:
if the population SDs really are 3.288 and
3.749, how often would Levene's test notice
with samples of 270 and 146?
To see a Levene F worked out from data, use
Menu > Two samples: data (built-in examples,
or a short list of your own in D1 and D2).
any key or tap = go on
```

- The number of scores, the two SDs and the two n's are those on screen.
- After it come the page's two screens, as before. With Roger's numbers the power is 0.40 by the large-sample formula (a 20,000-pair simulation gives 0.39) and 0.45 for the exact F test.

### The menu item and the texts that name it

- **The menu item** is "Would Levene notice?" (3519), the page's own title. It was "Levene's test: power".
  - The comment about it sits above the `CHOOSE`, not inside the list. The gate's first run caught a `//` comment inside the braces, which is a syntax error on the Prime (E12).
- **The data page's reading** points to it: "they are equal (Menu, Would Levene notice?)" (3347).
- **Help page 5** (3486) now says what the page answers and why it gives no Levene F:
  - "if σ₁ and σ₂ are as typed, how often would Levene's test notice at your n? (A plan.)"
  - "It cannot give SPSS's Levene F: that F needs every score; PowerViz has means, SDs and n."

## Not changed

Everything else of v2.5j: the engine, the readout box, the statistic obtained, the data page's arithmetic, and the simulation.

## Verification

`verify_PowerViz_v2.5k.py`, output `verify_PowerViz_v2.5k_output.txt`: **98 PASS, 0 FAIL**.

- **E7, new:**
  - the first screen, line for line, with Roger's numbers (416 scores; 3.288 and 3.749; 270 and 146);
  - after it, the large-sample page;
  - the menu item;
  - help page 5's lines.
- **E5:** reopening the page shows the first screen again, then the cached result with no new simulation.
- **Everything else:** every other check of v2.5j's script.

## Gate

`ppl_gate_v1c.py PowerViz_v2.5k.txt PowerViz_v2.5j.txt`: **RESULT: PASS**. Before the fix above, it failed on E12, a comment inside the menu list's braces.

## Device checklist

Items 1–27 of the earlier change notes still apply, with "Levene's test: power" now read as "Would Levene notice?". Then:

28. **Menu → Would Levene notice?** with Roger's numbers:
    - the first screen, with nothing off the right edge;
    - any key, then the page: "Levene (large-sample formula): 0.40".
29. **Help page 5:** the four new lines fit.

## Unresolved

The same as v2.5j.
