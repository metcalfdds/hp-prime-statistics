# PowerViz v2.5j: changes

*Superseded the same afternoon by v2.5k (the Levene power page's first screen: why SPSS's Levene F cannot be worked out here; see `PowerViz_v2.5k_CHANGES.md`). v2.5j was filed but not committed. Its verify script, `verify_PowerViz_v2.5j.py`, is in the author's folder; `verify_PowerViz_v2.5k.py` runs its checks on v2.5k.*

*31 October 2026, late afternoon. Built from v2.5i by `make_v25j.py` (20 exact replacements, generated from the line diff and each required to match once). 3,802 lines: 2,382 of code and 1,253 of comments. v2.5i was filed but not committed; this version carries it (see `PowerViz_v2.5i_CHANGES.md`).*

## Why

Roger, 31 Oct 2026, minutes after v2.5i: "Oh, crap--we didn't put in t obtained!"

## What changed (line numbers are v2.5j's)

### The test statistic obtained, under POWER (`pv_TObt`, 1634)

It is the t (or z) a sample would give if its means (or proportions), SDs and n's were exactly the ones typed. It is printed in APA form with its df, and it replaces v2.5i's "df = …" line, whose df it carries:

| Test | Statistic | Example |
| --- | --- | --- |
| 1, one mean | t, df = n − 1 | t(29) = 1.83 |
| 2, two means, equal σ & n | pooled t, df = 2n − 2 | t(58) = 1.29 |
| 3, one proportion | z | z = 2.00 |
| 4, two proportions | z (pooled p̄) | z = 1.42 |
| 5, two means, unequal σ & n | Welch's t, Welch–Satterthwaite df, one decimal | t(265.9) = 4.35 |

- **The formula:** in every test it is (M1v − M0v)/SE0, the H₁ centre in SE₀ units. SE₀ is the very standard error that test divides by:
  - σ/√n in test 1;
  - σ√(2/n) in test 2;
  - √(p₀q₀/n) in test 3;
  - the pooled √(2p̄q̄/n) in test 4;
  - √(σ₁²/n₁ + σ₂²/n₂), Welch's, in test 5.
- **`pv_DF`** (1609) gains test 1 (n − 1).
- **Roger's SPSS numbers:** t(265.9) = 4.35. SPSS printed −4.351 on 265.924 df; the sign is turned because PowerViz takes group 2 minus group 1.
- **The text is pulled left** as far as it needs to end at x 316.

### The new box in every test (`pv_Panel`, 1663; was `pv_PanelG`)

- **The one-sample tests (1 and 3)** now get v2.5i's box too:
  - n, μ₀, μ₁ and σ (or p₀ and p₁), one value each;
  - then the same middle column (d or h, zcrit, α, β) and right column (POWER, the statistic obtained).
- **Taps:**
  - μ₀, p₀ or σ opens the Edit form;
  - μ₁ or p₁ edits the effect;
  - n edits n.
- **The plot:** every test's plot ends at y 133. PYB is a file-level constant now (506), and v2.5i's per-test line in `pv_Setup` is gone.
- **pv_Draw** draws the box with one call (2019). Tests 1 and 3's old box is gone.

### Help

- **Page 1:** "SE₀ = the H₀ curve's SE, from σ (or p) and n" and "t(df) = t obtained if a sample had these values" (3363) replace the two SE lines.
- **Page 2:** "α, zcrit = the α ladder;  σ, μ₀, p₀ = Edit form".

## Not changed

- The engine: every number of every test. Verify A1 checks the eight engine values against v2.5f in 512 states.
- Everything else of v2.5i, v2.5h and v2.5g.

## Verification

`verify_PowerViz_v2.5j.py`, output `verify_PowerViz_v2.5j_output.txt`: **95 PASS, 0 FAIL**.

- **A, against v2.5f, 512 states of tests 1–4:**
  - the new box shows every text of v2.5f's box except its n and μ/p cells;
  - its table holds the values typed (n; both means or p's, to the decimals shown; σ);
  - the plot shows the same texts, except the labels inside the regions, which are drawn only where they fit and the plot is 13 px shorter;
  - the curve views and the formula page;
  - help pages 1–3, each allowed difference checked.
- **H5, the statistic obtained:**
  - "t(265.9) = 4.35" for Roger's data, equal to SciPy's Welch t from his SPSS numbers (4.351);
  - "t(58) = 1.29" (test 2), "t(29) = 1.83" (test 1), "z = 1.42" (test 4), "z = 2.00" (test 3);
  - `pv_DF` equals the Welch–Satterthwaite formula in 7 cases.
- **H1–H4:** v2.5i's checks:
  - a finger left on OK, with a control copy that reproduces Roger's report;
  - no `!=`, and the floor;
  - Roger's data cell by cell;
  - every plot ends at 133.
- **B, C, E, F, G and D:** as for v2.5i.

## Gate

`ppl_gate_v1c.py PowerViz_v2.5j.txt PowerViz_v2.5i.txt`: **RESULT: PASS**.
- No new E1 note.
- The full-parse step stops at the bare `EXPORT EP_…;` lines, as before.
- lint_ppl's four problems are the version number in the file name, as before.

## Device checklist (G2 first, then G1)

Items 1–12 (`PowerViz_v2.5g_CHANGES.md`), 13–18 (`PowerViz_v2.5h_CHANGES.md`) and 19–23 (`PowerViz_v2.5i_CHANGES.md`) still apply, except that 20 and 22 now read a t line, not "df = …", under POWER. Then:

24. **Test 5 with Roger's numbers:** "t(265.9) = 4.35" under POWER, ending inside the box.
25. **Test 1** (defaults, n = 30):
    - the box reads n 30, μ₀ 100, μ₁ 105, σ 15, and "t(29) = 1.83" under POWER;
    - a tap on μ₀ opens the Edit form, a tap on μ₁ the effect form.
26. **Test 3** (defaults): n, p₀, p₁ and "z = 2.00".
27. **Help page 1:** the two new lines, with nothing off the right edge.

## Unresolved

The same as v2.5i:
- whether `!=` was the cause of the β display;
- the same `!=` floor in BayesTree, Norm3 and StatDist;
- the fleet sweep for the finger-on-OK fault.
