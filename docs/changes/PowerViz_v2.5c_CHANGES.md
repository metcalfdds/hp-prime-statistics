# PowerViz v2.5c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, evening. Built on v2.5b; every v2.5b feature is kept, and PW, the plot and every exported value are unchanged. Not yet run on hardware or on the emulator.*

## Why

**No "=" before a relation** (Roger approved the pass, 17 Oct 2026, 21:18). pv_FMTP writes `< 0.001` below its floor. Eleven displays put that after `= `:
- **A typed α below 0.001** (the edit form accepts any α between 0 and 1; only the ladder and the drag keep it at 0.001 or more). It read `α = < 0.001` on the panel, in the tails hint (`2-sided: α = < 0.001 is split, < 0.0001 in each tail,`), in both curve views' titles and in the exit box.
- **A small power** read `power = < 0.001` in the curve views, and `POWER = < 0.0001` in the exit box.
- **A large n** read `β = < 0.001` on the panel, and `(β = < 0.0001)` in the exit box.

**A β that read 0.** The coordinator asked for this check across the fleet after FDAES's emulator run. The panel and the exit box printed β as `1 - PW`, which is exactly 0 once PW rounds to 1. n = 5000 at d = 0.67 read `β = 0.000` and `(β = 0.0000)`, where n = 200 read `< 0.001`. The harness shows this in doubles; the calculator's 12 digits reach it at a smaller n.

## What changed (line numbers: v2.5b → v2.5c)

1. **New `pv_Rel(rlS)`** (→ 891-897, after pv_FMTP). It returns `" = 0.050"`, or `" < 0.001"` when pv_FMTP has already written the relation. It reads `LEFT(rlS, 1)` only inside `IF DIM(rlS) > 0`, and it uses no INSTRING.
2. **New `pv_BetaS(bsD)`** (→ 908-918). It computes β as a probability of its own, P(XCL < X < XCU) with X ~ N(M1v, SE1), from the critical values pv_Model set for PW.
   - When the interval lies right of M1v it is mirrored about M1v, so both CDFs are lower tails and a tiny β keeps its digits.
   - β is never 0 under a normal model, so an exact 0 (a tail below what NORMALD_CDF can hold; at n = 5000 the harness's doubles underflow) is shown as the floor.
   - It returns the text, with pv_FMTP's floor.
3. **The eleven displays:**
   - pv_Tails's hint (1161, 1164 → 1219, 1223);
   - the panel's α and β (1421, 1424 → 1482, 1485);
   - pv_PCDraw's two titles (1486, 1489 → 1548, 1552);
   - its power readouts (1607, 1609, 1613 → 1671, 1674, 1679);
   - the exit box (2445, 2447 → 2512, 2514).

   β comes from `pv_BetaS(3)` and `pv_BetaS(4)`.
4. **Header:**
   - the banner (4);
   - the tested-on lines (19, 24);
   - a "v2.5c" paragraph (→ 29-52).
   - Comments above the changed statements say what each does.

**Before and after** (harness, one-sample mean, μ₀ 100, σ 15):

| Case | v2.5b | v2.5c |
|---|---|---|
| typed α 0.0001, μ₁ 100.5, n 30 | panel `α = < 0.001`; exit box `n = 30/group  α = < 0.001  1-sided` | `α < 0.001`; `n = 30/group  α < 0.001  1-sided` |
| the same, 2-sided | `2-sided: α = < 0.001 is split, < 0.0001 in each tail,` | `2-sided: α < 0.001 is split, …` |
| typed α 0.00001, no effect | `POWER = < 0.0001   (β = 1.0000)` | `POWER < 0.0001   (β = 1.0000)` |
| Pow-n view, typed α 0.0001 | `…, α = < 0.001, 1-sided`; `at n = 30: power = < 0.001, …` | `…, α < 0.001, 1-sided`; `at n = 30: power < 0.001, …` |
| Pow-d view, typed α 0.0001 | `n = 30/grp, α = < 0.001, 1-sided`; `at d = 0.03: power = < 0.001, …` | `n = 30/grp, α < 0.001, 1-sided`; `at d = 0.03: power < 0.001, …` |
| μ₁ 110, n 200 | `β = < 0.001`; `(β = < 0.0001)` | `β < 0.001`; `(β < 0.0001)` |
| μ₁ 110, n 5000 | `β = 0.000`; `(β = 0.0000)` | `β < 0.001`; `(β < 0.0001)` |
| defaults (μ₁ 105, n 30, α 0.05) | `α = 0.050`, `β = 0.428`; `POWER = 0.5718   (β = 0.4282)` | the same |

**Left alone (checked):**
- **The drag and snap hints** (1119, 1121, 1133, 1136). The drag clamps α to 0.001-0.5 (`na:=MIN(0.5,MAX(0.001,na*TL));`) and the ladder starts at 0.001, so α never reaches the floor there.
- **The plot's β and power labels** (1382, 1395; 2 decimals). A label is drawn only when its region is wide and tall enough to hold it. A sweep of 960 states of v2.5b, and 120 of v2.5c in the verify, never drew one below 0.01.
- **PW itself** is still `1 - NORMALD_CDF(…)` for the upper tail. Power is at least α in the direction the test follows, so it reaches 0 only for a typed α below about 5E-13.

## Verification

`verify_PowerViz_v2.5c.py` was built from the v2.5b script, and every check is kept. It runs on harness **ppl_run_v3e**, with v3d's results. Output is in `verify_PowerViz_v2.5c_output.txt`: **134 PASS, 0 FAIL** (v2.5b's script: 106).

- **A, B, G, R (kept).**
  - B12, v2.4's script run on v2.5c, still gives 64 PASS with only the intended help-page count failing.
  - R5's list of routines that differ from v2.5a now includes v2.5c's, and its count of untouched routines leaves out the two new ones.
- **T1.** Every row of the table, reached in the harness, before and after.
- **T2.** pv_BetaS over 1,152 states (4 tests, 2 tails, 4 αs, n 2-5000, 6 effects), at 3 and 4 decimals.
  - It gives v2.5b's text wherever `1 - PW` still had its digits, and the floor where SciPy's β is below it.
  - The β it computes is SciPy's to 3.4E-13 relative, down to 1E-290.
- **T3.** pv_Rel, including `""` → `" = "`.
- **T4.** The sites left alone, as above.
- **T5.**
  - The routines that differ from v2.5b are exactly POWERVIZ, pv_Draw, pv_PCDraw and pv_Tails, plus the new pv_BetaS and pv_Rel.
  - The changed code lines are exactly the eleven above.
  - The new names are not built-ins and carry the pv_ tag.
  - The version strings are swept.
  - No comment sits inside an open bracket.
  - INSTRING is as v2.5b.
- **T6.** No scientific fixed decimal in any of the 165 v2.5c runs.

## Gate

`python3 ppl_gate_v1b.py PowerViz_v2.5c.txt PowerViz_v2.5b.txt`, in a scratch copy of `gate_r2` with the newest version of every program: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 5 E1, 175 E7, 14 E9 (v2.5b: 174 E7). There are no hard errors, E12 included. The one new E7 is `bsV`, pv_BetaS's LOCAL. ppl_check_v4 reads a `LOCAL pv_Name()` head as a file-level LOCAL line, so it reports every routine's own LOCAL in PowerViz this way (thr, lbs, abi, cix …).
- lint_ppl: 22 problems, as v2.5b.
- Parse: it stops at the EXPORT list, as v2.5b's does.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v2.5b (open it in the Kit). Then Program Catalog → Check.
2. **Typed α.** Choose the one-sample mean, set α to 0.0001 in the form, and keep μ₁ 100.5:
   - the panel reads `α < 0.001`;
   - Enter → Toggle 1/2-sided: the hint reads `2-sided: α < 0.001 is split, < 0.0001 in each tail,`;
   - the Pow-n soft key: the title ends `α < 0.001, 1-sided` and the readout says `power < 0.001`;
   - Esc: the box reads `α < 0.001`.
3. **Large n.** μ₁ 110, n 200, then n 5000: the panel reads `β < 0.001` both times, never `0.000`. Esc: `(β < 0.0001)`.
