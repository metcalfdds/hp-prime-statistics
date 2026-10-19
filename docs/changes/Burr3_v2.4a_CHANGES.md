# Burr3 v2.4a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, evening. Built on v2.4; every v2.4 feature is kept. Not yet run on hardware or on the emulator (v2.4 passed the emulator).*

## Why

**No "=" before a relation** (Roger approved the pass, 17 Oct 2026, 21:18). b3_fmtp writes `< 0.0001` below its floor. Three displays put that after `= `, all with ordinary inputs:
- the status row, `pdf = < 0.0001 (a height), P(X ≤ x₀) = < 0.0001` (x₀ 0.005, or x₀ 30, for Burr(2, 1, 1));
- view 4, `its P(X < 0) = < 0.0001` (C 10, K 1);
- the summary returned to Home.

**A P that read 0.** The coordinator asked for this check across the fleet after FDAES's emulator run. P(X ≤ x₀) is `1 - (1 + (x₀/S)^C)^(-K)`. For a small x₀ with a large C, `1 + u` is 1 in the last digit, and the difference is exactly 0. C 25, x₀ 0.3 printed `< 0.0001`, but x₀ 0.2 printed `P(X ≤ x₀) = 0.0000`; SciPy gives 3.4E-18. The harness shows this in doubles, without a 12-digit model.

Here x₀ is always above 0: it must be typed above 0, and the keys and the snap keep it at 0.05 or more. The Burr's CDF is never 0 there, so an exact 0 is always this cancellation.

## What changed (line numbers: v2.4 → v2.4a)

1. **New `b3_Eq(eqS)`** (→ 240-245, after b3_fmtp). It returns `" = 0.5000"`, or `" < 0.0001"` / `" > -0.0001"` when b3_fmtp has already written the relation. It reads `LEFT(eqS, 1)` only inside `IF DIM(eqS) > 0`, and it uses no INSTRING.
2. **The three displays use it:**
   - view 4's line (596 → 628);
   - the status row (726-727 → 761-762);
   - the summary (984-985 → 1020-1021).
3. **An exact-0 P(X ≤ x₀)** reads `< 0.0001`, on the status row (`IFTE(cdf0 > 0, b3_fmtp(cdf0,4), "< 0.0001")`) and in the summary. **EP_BURR_CDF still holds the computed value.** The CDF formula itself is unchanged: computing the small-x₀ tail exactly needs LNP1/EXPM1, which the fleet has never verified on the Prime.
4. **Header and help:**
   - the banner (4);
   - a "What changed in v2.4a" paragraph (→ 19-35);
   - the help page's title, `Burr3 v2.4a  -  touch and keys` (290 → 321).
   - Comments above the changed lines say what each does.

**Before and after** (harness):

| Call | v2.4 | v2.4a |
|---|---|---|
| `Burr3(2,1,1,0.005)` | `pdf = 0.0100 (a height), P(X ≤ x₀) = < 0.0001` | `… P(X ≤ x₀) < 0.0001` |
| `Burr3(2,1,1,30)` | `pdf = < 0.0001 (a height), P(X ≤ x₀) = 0.9989` | `pdf < 0.0001 (a height), …` |
| `Burr3(25,1,1,0.3)` | `pdf = < 0.0001 …, P(X ≤ x₀) = < 0.0001`; Home `P(X ≤ 0.30) = < 0.0001` | `pdf < 0.0001 …, P(X ≤ x₀) < 0.0001`; `P(X ≤ 0.30) < 0.0001` |
| `Burr3(25,1,1,0.2)` | `P(X ≤ x₀) = 0.0000`; Home `P(X ≤ 0.20) = 0.0000` | `P(X ≤ x₀) < 0.0001`; `P(X ≤ 0.20) < 0.0001` |
| view 4, `Burr3(10,1,1,1)` | `its P(X < 0) = < 0.0001` | `its P(X < 0) < 0.0001` |
| `Burr3(2,1,1,1)`; view 4 `Burr3(3,2,1,1)` | `= 0.5000`; `its P(X < 0) = 0.0207` | the same |

Nothing else changed. The verify's C5 checks that the changed code lines are exactly the six above, plus b3_Eq.

**Seen, not changed:** the summary prints x₀ with `STRING(x₀, 2, 2)`, so an x₀ below 0.01 reads `P(X ≤ 5.00ᴇ-3)`. That is a scientific fixed decimal, as in v2.4, and outside this pass.

## Verification

`verify_Burr3_v2.4a.py`, output in `verify_Burr3_v2.4a_output.txt`: **ALL CHECKS PASSED.**
- **A. harness_Burr3_v24.py**, v2.4's harness run (ppl_run_v1), on v2.4a: **50 / 50**. Only the file name changed, and check 10b's alternative form is written without the `=`; its case, Burr3(3,2,1,1), prints 0.0207 either way.
- **B. verify_Burr3.py**, v2.4's formula mirror (it reads no program file), run as it is: **4,972 passed, 0 failed**.
- **C. v2.4a**, harness v3e:
  - **C1.** Each display in the table, before and after.
  - **C2.** The exact 0: EP_BURR_CDF is 0, and SciPy's 3.4E-18 is positive.
  - **C3.** 224 calls (C 0.5 to 25, K 0.25 to 2, S 1 and 3.5, x₀ 0.05 to 40). Every readout row and summary is identical to v2.4, once v2.4's `= <` and exact-0 CDF are written the v2.4a way; 84 calls needed it.
  - **C4.** b3_Eq.
  - **C5.**
    - The exact code-line diff.
    - The new names b3_Eq and eqS are not built-ins, and b3_Eq carries the b3_ tag.
    - The version strings are swept.
    - No comment sits inside an open bracket, and there is no INSTRING.
  - **C6.** No new scientific fixed decimal: only the summary's x₀ = 0.005, the same as v2.4.

## Gate

`python3 ppl_gate_v1b.py Burr3_v2.4a.txt Burr3_v2.4.txt`, in a scratch copy of `gate_r2` with the newest version of every program: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 4 E5, 2 E7, as v2.4. There are no hard errors, E12 included.
- lint_ppl: 4 problems, as v2.4.
- Parse: it stops at `√`, as v2.4's does (the tool's limit).
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v2.4 (open it in the Kit). Then Program Catalog → Check.
2. Burr3 with C 25, K 1, S 1, x₀ 0.3, then x₀ 0.2: the status row reads `P(X ≤ x₀) < 0.0001` both times (v2.4: `= < 0.0001`, then `= 0.0000`). Quit: Home shows `… P(X ≤ 0.20) < 0.0001; …`.
3. Burr3 with C 10, K 1, S 1, x₀ 1, View four times: `its P(X < 0) < 0.0001`.
