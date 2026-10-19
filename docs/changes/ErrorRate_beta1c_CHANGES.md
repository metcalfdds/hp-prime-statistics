# ErrorRate Lab beta 1c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, evening. Built on beta 1b; every beta 1b feature is kept, and the MicroPython block is byte-identical. Not yet run on hardware or on the emulator.*

## Why

**No "=" before a relation** (Roger approved the pass, 17 Oct 2026, 21:18). erlPctS writes `< 0.0001 %` below one in a million and `> 99.9999 %` just under certainty. Eight displays put that after `= `. The trawl read:
- `P(at least one chance match) = < 0.0001 %`
- `At N = 1: P = < 0.0001 % exactly,`

The right form drops the `=`: `P(at least one chance match) < 0.0001 %`. The same trawl panel said `N = 1 profiles searched`.

**A "1 − CDF" tail that read 0.** The coordinator asked for this check across the fleet after FDAES's emulator run. The Bayes page's `P(true rate > x)` was `1 - erlBetaCdf(…)`, a FISHER_CDF. That is exactly 0 once the tail is below the CDF's last digit, so it printed `0 %` where a slightly larger tail printed `< 0.0001 %`. With 0 errors in 1000 tests and a true rate of 30 %, beta 1b printed `P(true rate > 30.0 %) = 0 %`; the tail is 8.8E-156. The harness's doubles reproduce this, so a 12-digit model is not needed to see it.

## What changed (line numbers: beta 1b → beta 1c)

1. **New `erlEq(eqS)`** (→ 399-404, after erlPctS). It returns `" = 2.15 %"`, or `" < 0.0001 %"` / `" > 99.9999 %"` when erlPctS has already written the relation.
   - It reads `LEFT(eqS, 1)` only inside `IF DIM(eqS) > 0`, so it never reads from an empty string, and it uses no INSTRING.
   - Eight displays use it:

   | Display | beta 1b | beta 1c |
   |---|---|---|
   | "No closed form" page, p (erlCasDraw, 1321 → 1356) | `p = 1.00000 = > 99.9999 %` (9999 errors in 10000, α 0.001) | `p = 1.00000 > 99.9999 %` |
   | Bayes page (erlBayesDraw, 1516 → 1555) | `P(true rate > 50.0 %) = < 0.0001 %` | `P(true rate > 50.0 %) < 0.0001 %` |
   | Simulation, k = 0 (erlSimDraw, 1846 → 1886) | `exact chance (1 - p)^30 = < 0.0001 %` | `exact chance (1 - p)^30 < 0.0001 %` |
   | Simulation, k > 0 (erlSimDraw, 1850 → 1891) | `exact chance (BINOMIAL_CDF) = > 99.9999 %` | `exact chance (BINOMIAL_CDF) > 99.9999 %` |
   | Trawl panel (erlTrDraw, 1991 → 2033) | `P(at least one chance match) = < 0.0001 %` | `P(at least one chance match) < 0.0001 %` |
   | Trawl Exact page (erlTrExact, 2062 → 2105) | `At N = 1: P = < 0.0001 % exactly,` | `At N = 1: P < 0.0001 % exactly,` |
   | Trawl Exact page (erlTrExact, 2063 → 2106) | `1-e^(-μ) = < 0.0001 %, μ = 0.000.` | `1-e^(-μ) < 0.0001 %, μ = 0.000.` |

2. **The Bayes page's tail** (erlBayesDraw, 1515 → 1554) is `erlBetaCdf(bwB2, bwA2, 1 - erlP0)`, the mirrored Beta's lower tail P(Beta(b, a) < 1 − x).
   - It is the same number as `1 - erlBetaCdf(bwA2, bwB2, erlP0)`, but a tiny tail is kept: 0 of 1000 at 30 % now reads `< 0.0001 %`.
   - The ends are unchanged: x = 0 gives 1 and x = 1 gives 0.
   - The F degrees of freedom are still whole numbers (2a + 2k, 2b + 2(n − k)), so FISHER_CDF's whole-df rule holds.
3. **"N = 1 profile searched"** (erlTrDraw, 1990 → 2032), with `IFTE(erlTN == 1, " profile searched", " profiles searched")`.
4. **Header:**
   - the banner (4);
   - the tested-on line, "Beta 1b and 1c have not run there yet" (23);
   - the harness and verify names (32);
   - the companion files (34-35);
   - a dated "beta 1c" paragraph (→ 42-61).
   - A comment above each changed line says what it does.

Nothing else changed. The verify's T6 checks that the routines differing from beta 1b are exactly erlBayesDraw, erlCasDraw, erlSimDraw, erlTrDraw and erlTrExact, plus the new erlEq. The changed code lines are exactly the nine above, and the #PYTHON block is byte-identical.

### Checked and left alone

Each of these puts erlPctS after `= `, but its value cannot reach erlPctS's ends with the inputs the program accepts (n 1-10000, k 0-n, α 0.001-0.5, a and b 0.5-100 in halves, the simulation's M ≤ 10,000):
- **The rule, n bound and k = 0 bound** (970, 1288, 1289 and the summary returned to Home, 2631).
  - Over every α on the menu and n from 1 to 10000, the rule's n / bound runs from 6.9E-5 to 0.9868 (or past 1), and the k = 0 bound from 6.9E-5 to 0.999. Both stay inside the ends (verify T4).
  - The summary's "upper bound" has no `=` before it.
- **The Bayes mean** (1509, 1513): (a + k)/(a + b + n) runs from 5.0E-5 to 0.99995.
- **The simulation's shares** (1844, 1848): 0, 1 or a multiple of 1/10000.

### Seen, not changed (outside this pass)

- **`P(true rate > < 0.0001 %)`.** A typed rate below one in a million goes through erlRateS into the Bayes page's own label. That is a relation inside a bracket, not after `=`.
- **`at most 1 errors`** on the simulation page (k = 1).
- **The trawl's top end reads `100.0 %`.** At RMP 1 in 1000 and N = 100,000,000 the panel shows `P(at least one chance match) = 100.0 %`, where N = 20,000 shows `> 99.9999 %`. Here 1 − (1 − r)^N is 1 in the calculator's digits, and in doubles too. It is the top-end form of the 0 vs `<` question. For FDAES, Roger's rule is that a model's exact 1 prints as the floor. Whether ErrorRate should do the same is for Roger: here an exact 1 is sometimes true (a rate of 0 gives P(rate > 0) = 100 %).

## Verification

`verify_ErrorRate_beta1c.py` was built from the beta 1b script, and every check is kept. It runs on harness **ppl_run_v3e**, which gives the same results as v3d for this script. Output is in `verify_ErrorRate_beta1c_output.txt`: **250 PASS, 0 FAIL** (beta 1b's script: 211).

- **A-E, G and R (kept).** R5's list of routines that differ from beta 1a now includes beta 1c's five and erlEq.
- **T1, each display before and after,** reached in the harness: the table above, plus ordinary values unchanged.
  - The Bayes page at 5 % and 4 %: `= 20.4 %`, `= 66.6 %`.
  - The simulation: `= 21.5 %`, `= 81.2 %`.
  - The trawl at RMP 10⁻⁶, N = 10⁶: `= 63.2 %`.
  - The "No closed form" page at three ordinary records.
  - `P(true rate > 0.0 %) = 100.0 %` (true, and kept).
- **T2.** The mirrored tail equals `1 - erlBetaCdf` and SciPy's `beta.sf` in 42 cases (worst 9.5E-15). At 0 of 1000 and 30 % it is 8.77E-156, where `1 - erlBetaCdf` is exactly 0 even in doubles.
- **T3.** erlEq, including `""` → `" = "` with no error.
- **T4.** The sites left alone cannot reach the ends (above).
- **T5.** Two whole lecture sessions (1,379 texts each) are identical in beta 1b and 1c. None of their texts needed rewriting, so every ordinary display is unchanged.
- **T6.** The routine diff and the exact line diff.
- **T7.**
  - The new names erlEq and eqS are not built-ins, and erlEq carries the erl tag.
  - The same three guarded INSTRING lines as beta 1b.
  - The version strings are swept.
  - No comment sits inside an open bracket.
- **T8.** No scientific fixed decimal in any of the 56 beta 1c runs.

## Gate

`python3 ppl_gate_v1b.py ErrorRate_beta1c.txt ErrorRate_beta1b.txt`, in a scratch copy of `gate_r2` with the newest version of every program: **RESULT: PASS**.
- hp-prime-kit lint: 1 error, the #PYTHON block's "unbalanced", as beta 1b.
- ppl_check_v4: clean. There are no hard errors, E12 included.
- lint_ppl: 17 problems, as beta 1b.
- Parse: it stops at the EXPORT list, as beta 1b's does.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. Paste over beta 1b (open it in the Kit; do not add a second copy). Then Program Catalog → Check.
2. **The trawl.** More → Trawl → RMP "1 in 1 billion" → N, type 1. The panel reads:
   - `N = 1 profile searched`
   - `P(at least one chance match) < 0.0001 %`

   Exact: `At N = 1: P < 0.0001 % exactly,` and `1-e^(-μ) < 0.0001 %, …`. Then RMP 1 in 1000 and N = 20000: `> 99.9999 %`, with no `=` before it.
3. **The Bayes tail.** Menu → "Set n, k and α": 1000, 0, 0.05. Menu → "Set the true rate": 0.3. Bayes: `P(true rate > 30.0 %) < 0.0001 %` (beta 1b: `= 0 %`). Drag back towards 0: the value rises through ordinary `= x %` readings.
