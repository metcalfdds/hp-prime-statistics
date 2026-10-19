# Norm3 v2.4a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, evening. Built on v2.4; every v2.4 feature is kept. Not yet run on hardware or on the emulator (v2.4 passed the emulator).*

## Why

**No "=" before a relation** (Roger approved the pass, 17 Oct 2026, 21:18). n3_fmtp writes `< 0.0001` below its floor. Four displays put that after `= `, all reached with the program's ordinary inputs:
- `pdf = < 0.0001 (a height)`: x₀ at z = ±5, or any x₀ when σ is large (N(0, 20000) at its mean);
- `P(X ≤ x₀) = < 0.0001`: x₀ = −5 σ;
- `P(X > x₀) = < 0.0001`: x₀ = +5 σ;
- the summary returned to Home, `… P(X ≤ -5.00) = < 0.0001; …`.

**A right tail that read 0.** The coordinator asked for this check across the fleet after FDAES's emulator run. P(X > x₀) was `1 - cdf0`, which is exactly 0 once the tail is below the CDF's last digit. x₀ is typed and the window widens to hold it, so x₀ ten σ to the right printed `P(X > x₀) = 0.0000`, while ten σ to the left printed `P(X ≤ x₀) = < 0.0001`. The harness shows this in doubles, without a 12-digit model.

## What changed (line numbers: v2.4 → v2.4a)

1. **New `n3_Eq(eqS)`** (→ 226-231, after n3_fmtp). It returns `" = 0.8413"`, or `" < 0.0001"` / `" > -0.0001"` when n3_fmtp has already written the relation. It reads `LEFT(eqS, 1)` only inside `IF DIM(eqS) > 0`, and it uses no INSTRING.
2. **The four displays use it:**
   - the pdf readout (610 → 641);
   - the two area keys (614 → 648, 616 → 650);
   - the summary (815 → 850).
3. **P(X > x₀)** (616 → 650) is `NORMALD_CDF(mu, sd, 2*mu - n3X0)`, the lower tail and the same number by symmetry. A tail too small for the CDF's last digit is kept, and reads `< 0.0001`.
4. **Header and help:**
   - the banner (4);
   - a "What changed in v2.4a" paragraph (→ 19-32);
   - a line in VERIFIED (→ 195-196);
   - the help page's title, `Norm3 v2.4a  -  touch and keys` (270 → 300).
   - Comments above the changed lines say what each does.

**Before and after** (harness):

| Call | v2.4 | v2.4a |
|---|---|---|
| `Norm3(0,1,-5)` | `pdf = < 0.0001 (a height)`, `P(X ≤ x₀) = < 0.0001`; Home: `P(X ≤ -5.00) = < 0.0001` | `pdf < 0.0001 (a height)`, `P(X ≤ x₀) < 0.0001`; `P(X ≤ -5.00) < 0.0001` |
| `Norm3(0,1,5)` | `P(X > x₀) = < 0.0001` | `P(X > x₀) < 0.0001` |
| `Norm3(0,1,10)` | `P(X > x₀) = 0.0000` | `P(X > x₀) < 0.0001` |
| `Norm3(0,20000,0)` | `pdf = < 0.0001 (a height)` | `pdf < 0.0001 (a height)` |
| `Norm3(0,1,1)` | `pdf = 0.2420 (a height)`, `P(X ≤ x₀) = 0.8413`, `P(X > x₀) = 0.1587` | the same |

Nothing else changed. The verify's C5 checks that the changed code lines are exactly the five above, plus n3_Eq.

**Seen, not changed:** in the harness the axis tick at 0 for σ = 0.2 prints `-5.6ᴇ-17`. v2.4 does the same. It is binary doubles' −0.8 + 4 × 0.2, a number the Prime's BCD holds exactly, so it is the harness's arithmetic and not a program fault.

## Verification

`verify_Norm3_v2.4a.py`, output in `verify_Norm3_v2.4a_output.txt`: **ALL CHECKS PASSED.**
- **A. harness_Norm3_v24.py**, v2.4's harness run (ppl_run_v1: every touch and key path, numbers against SciPy), on v2.4a with only the file name changed: **45 / 45**.
- **B. verify_Norm3.py**, v2.4's formula mirror (it reads no program file), run as it is: **276 passed, 0 failed**.
- **C. v2.4a**, harness v3e:
  - **C1.** Each display in the table, v2.4 and v2.4a.
  - **C2.** The right tail beside the left one: `NORMALD_CDF(μ, σ, 2μ − x₀)` equals SciPy's `norm.sf` to 12 digits at four points, including 7.6E-24 at z = 10.
  - **C3.** 224 calls (μ 0, 22, −12.5, 500; σ 1, 4, 0.2, 100; 14 values of z from −6 to 9). Every readout row and summary is identical to v2.4, once v2.4's `= <` and its right-tail `0.0000` are written the v2.4a way; 104 calls needed it.
  - **C4.** n3_Eq, including `""` → `" = "`.
  - **C5.**
    - The exact code-line diff.
    - The new names n3_Eq and eqS are not built-ins, and n3_Eq carries the n3_ tag.
    - The version strings are swept.
    - No comment sits inside an open bracket, and there is no INSTRING.
  - **C6.** No new scientific fixed decimal: the 230 v2.4a runs print exactly what v2.4 prints, only the `-5.6ᴇ-17` tick above.

## Gate

`python3 ppl_gate_v1b.py Norm3_v2.4a.txt Norm3_v2.4.txt`, in a scratch copy of `gate_r2` with the newest version of every program: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 2 E5, 1 E7, as v2.4. There are no hard errors, E12 included.
- lint_ppl: 4 problems, as v2.4.
- Full parse: OK, 7 functions (v2.4: 6).
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v2.4 (open it in the Kit). Then Program Catalog → Check.
2. Run Norm3 with μ 0, σ 1, x₀ 5 (the Catalog asks for the three arguments; or `Norm3(0,1,5)` in Home): the keys read `P(X ≤ x₀) = 1.0000` and `P(X > x₀) < 0.0001`, and the readout reads `pdf < 0.0001 (a height)`. Quit.
3. `Norm3(0,1,10)`: `P(X > x₀) < 0.0001`, not `0.0000`. `Norm3(0,1,-5)`, then Quit: Home shows `… P(X ≤ -5.00) < 0.0001; values in EP_NORM_*`.
