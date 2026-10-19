# SampDist v2.3a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, evening. Built on v2.3; every v2.3 feature is kept. Not yet run on hardware or on the emulator (v2.3 passed the emulator).*

## Why

**No "=" before a relation** (Roger approved the pass, 17 Oct 2026, 21:18). sd_fmtp writes `< 0.000001` below its floor. Mode 1's result panel put that after `= `, on its probability line and again on the z line's percent: `P(x̄ < -6.000) = < 0.000001` and `z = -6.0000   = < 0.001%`. This is reached by any bound 5 σx̄ or more out, in all four tail types.

**A right tail that read 0.** The coordinator asked for this check across the fleet after FDAES's emulator run. "Right tail" was `1 - NORMALD_CDF(μ, σx̄, a)`, and so was the right half of "Outside". That is exactly 0 once the tail is below the CDF's last digit. P(x̄ > 10) read `= 0.000000` and `= 0.000%`, where the same tail on the left read `< 0.000001`. The exported EP_SD_P was 0, and "outside −10 .. 10" held only its left half. The harness shows this in doubles.

## What changed (line numbers: v2.3 → v2.3a)

1. **New `sd_Eq(eqS)`** (→ 256-261, after sd_fmtp). It returns `" = 0.158655"`, or `" < 0.000001"` when sd_fmtp has already written the relation. It reads `LEFT(eqS, 1)` only inside `IF DIM(eqS) > 0`, and it uses no INSTRING.
2. **The result panel** (sd_compose) uses it on its four probability lines (641, 645, 650, 655 → 674, 678, 683, 688) and its percent (658 → 691). The percent is `"  " + sd_Eq(…)`, so an ordinary panel keeps its three spaces: `   = 15.866%`.
3. **The right tail** is `NORMALD_CDF(mu, se, 2*mu - lo)`, the lower tail and the same number by symmetry. The right half of "Outside" is `NORMALD_CDF(mu, se, 2*mu - hi)`. Both are changed in sd_prob (509, 514 → 541, 546), which the live graph uses, and in Mode 1 (1229, 1234 → 1263, 1268), which sets EP_SD_P.
4. **Header:**
   - the tested-on lines (26-28);
   - a "v2.3a" paragraph (→ 30-44);
   - the VERIFIED note (202 → 218).
   - Comments above the changed lines say what each does.

**Before and after** (Mode 1, μ 0, σ 1, n 1; harness):

| Region | v2.3 | v2.3a |
|---|---|---|
| left of −6 | `P(x̄ < -6.000) = < 0.000001`, `z = -6.0000   = < 0.001%` | `P(x̄ < -6.000) < 0.000001`, `z = -6.0000   < 0.001%` |
| right of 6 | `= < 0.000001`, `= < 0.001%` | `< 0.000001`, `< 0.001%` |
| right of 10 | `P(x̄ > 10.000) = 0.000000`, `= 0.000%`; EP_SD_P 0 | `P(x̄ > 10.000) < 0.000001`, `< 0.001%`; EP_SD_P 7.6E-24 |
| between 5 and 6 | `= < 0.000001` | `< 0.000001` |
| outside −10 .. 10 | `= < 0.000001`; EP_SD_P 7.6E-24 (left half only) | `< 0.000001`; EP_SD_P 1.5E-23 |
| right of 1; outside ±1; right of 0.5 at n 30 | `= 0.158655`, `= 0.317311`, `= 0.003085` | the same |

Nothing else changed. Part I5 of the verify checks that the changed code lines are exactly the nine above, plus sd_Eq.

**Seen, not changed:**
- **"Between" far to the right.** It is `NORMALD_CDF(hi) - NORMALD_CDF(lo)`, which also reaches exactly 0 when both bounds are far right of μ (for z 10 to 12 in the calculator's digits), while the same interval on the left keeps its digits. It is a difference of CDFs, not a `1 - CDF` tail. Mirroring the interval when it lies right of μ would fix it; this is Roger's call.
- **The tick label `-5.6ᴇ-17`.** In the harness, a tick label at 0 for σx̄ 0.2 prints this. v2.3 does the same. It is binary doubles' arithmetic, which the Prime's BCD does not share.

## Verification

`verify_SampDist_v2.3a.py`, output in `verify_SampDist_v2.3a_output.txt`: **337 checks, 0 failures.**
- **Parts A-H** are `verify_SampDist_v2.3.py` run on v2.3a with only the file name changed (ppl_harness_v1; v2.2 is still the comparison where they compare): **317 checks, 0 failures**, as on v2.3. They also pass unchanged, so every ordinary display those parts read is unchanged.
- **Part I (new, harness v3e):**
  - **I1.** The table above, before and after, for each tail.
  - **I2.** EP_SD_P against SciPy (P(x̄ > 10) = 7.6E-24; outside ±10, both halves). sd_prob directly: 240 cases (3 normals, 4 tails, z −12 to 14) are within 1E-9 of SciPy, and equal to v2.3 except where its `1 - CDF` had lost the tail.
  - **I3.** 108 panels (4 tails, n 1 / 30 / 400, z −9 to 9) are identical to v2.3, once its `= <` and right-tail zeros are written the v2.3a way; 18 needed it.
  - **I4.** sd_Eq.
  - **I5.**
    - The exact code-line diff.
    - The new names sd_Eq and eqS are not built-ins.
    - The version strings are swept.
    - No comment sits inside an open bracket, and there is no INSTRING.
  - **I6.** No new scientific fixed decimal: only the tick above, the same as v2.3.

## Gate

`python3 ppl_gate_v1b.py SampDist_v2.3a.txt SampDist_v2.3.txt`, in a scratch copy of `gate_r2` with the newest version of every program: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 2 E4, 3 E9, as v2.3. There are no hard errors, E12 included.
- lint_ppl: 18 problems, as v2.3. A first build of v2.3a added a 19th: the new comments spelled x̄ with a combining macron. They now say "x-bar".
- Full parse: OK, 26 functions (v2.3: 25).
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v2.3 (open it in the Kit). Then Program Catalog → Check.
2. **Find probability**, μ 0, σ 1, n 1, Right tail, a = 6: the panel reads `P(x̄ > 6.000) < 0.000001` and `z = 6.0000   < 0.001%`, with no `=`. Then n+ until the bound is far out (or a = 10): still `< 0.000001`, never `0.000000`.
3. An ordinary case (Right tail, a = 1) still reads `P(x̄ > 1.000) = 0.158655` and `   = 15.866%`. After Esc, Home's EP_SD_P for a = 10 is about 7.6E-24, not 0.
