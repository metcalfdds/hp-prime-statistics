# StudRange beta 15c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, evening. Built on beta 15b; every beta 15b feature is kept, and the #PYTHON srq block is byte-identical. Not yet run on hardware or on the emulator.*

## Why

**No "=" before a relation** (Roger approved the pass, 17 Oct 2026, 21:18). sr_FmtP writes `< 0.00001` below its floor. Beta 15b had stopped the Quit summary from saying `p = < 0.00001`, by testing p twice. The P-value page itself still printed the relation after `= `:
- `P(Q ≥ q) = < 0.00001` (q 12, k 3, df 12)
- `F(q) = < 0.00001` (q 0.001; beta 15b's own CHANGES file lists that text)

**A p of exactly 0.** The coordinator asked for this check across the fleet after FDAES's emulator run. The PPL engine's p is `MAX(0, 1 - F)`, and F reaches 1 in the calculator's digits for a large q. So q 40 (k 3, df 12) printed `P(Q ≥ q) = 0.00000`, and the Quit summary `p = 0.00000`, where q 12 printed `< 0.00001`. P(Q ≥ q) is never 0 for a finite q; SciPy gives 6.7E-12 at q 40. The harness shows this in doubles, without a 12-digit model.

## What changed (line numbers: beta 15b → beta 15c)

1. **New `sr_Eq(eqS)`** (→ 1084-1089, after sr_FmtP; its prototype is at → 335). It returns `" = 0.07000"`, or `" < 0.00001"` when sr_FmtP has already written the relation. It reads `LEFT(eqS,1)` only inside `IF DIM(eqS)>0`, so it never reads from an empty string, and it uses no INSTRING.
2. **sr_PvMode** (the P-value page):
   - **The p as text, once** (1422-1423 → 1462-1464).
     - `pvS:=sr_FmtP(pv,5)`.
     - An exact 0 reads `"< 0.00001"`.
     - `srPS:="p"+sr_Eq(pvS)`.
     - It replaces beta 15b's two-step `srPS` test; the summary and the page now read the same text.
   - The new LOCAL `pvS` is on the routine's one LOCAL line (1386 → 1421): six names.
   - **The page's two lines** (1429-1430 → 1471-1472): `"P(Q ≥ q)"+sr_Eq(pvS)` and `"F(q)"+sr_Eq(sr_FmtP(fv,5))`.
   - **EP_QPVAL still holds the computed value** (0 at q 40 with the PPL engine).
3. **Header:**
   - both banners (2, 272 → 293);
   - the tested-on lines (20-21, 25);
   - a "What changed in beta 15c" paragraph (→ 57-76).
   - Comments above the changed lines say what each does.

**Displays, before and after** (harness, PPL engine):

| q, k, df | beta 15b | beta 15c |
|---|---|---|
| 3.5, 3, 12 | `P(Q ≥ q) = 0.07000`, `F(q) = 0.93000`; summary `p = 0.07000` | the same |
| 12, 3, 12 | `P(Q ≥ q) = < 0.00001`; summary `p < 0.00001` | `P(Q ≥ q) < 0.00001`; `p < 0.00001` |
| 40, 3, 12 | `P(Q ≥ q) = 0.00000`; summary `p = 0.00000` | `P(Q ≥ q) < 0.00001`; `p < 0.00001` |
| 0.001, 3, 12 | `F(q) = < 0.00001` | `F(q) < 0.00001` |
| 0, 3, 12 | `P(Q ≥ q) = 1.00000`, `F(q) = 0.00000` | the same (F(0) = 0 is true) |

**Left alone:**
- The plot's p (sr_PlotMode, 1965-1966). Beta 15b already writes it without `=`. It can never be exactly 0, because it is floored at 1E-12 before its log interpolation.
- The Python engine's p (`SR_OUT`) goes through the same pvS line, so an exact 0 from it would also read `< 0.00001`. The harness does not run the Python engine on the P-value page, so this path is untested.

Nothing else changed. Section 9c of the verify checks that the routines differing from beta 15b are exactly sr_PvMode and the new sr_Eq. The changed code lines are exactly those above, and the #PYTHON srq block is byte-identical.

## Verification

`verify_StudRange_beta15c.py` was built from the beta 15b script, and every check is kept. It runs on harness **ppl_run_v3e**, which gives v3d's results; this script took 7 min. Output is in `verify_StudRange_beta15c_output.txt`: **130 ok, 0 failures** (beta 15b's script: 100).

**Adjusted only where 15c changes the screen on purpose:**
- 7g (15b against 15a) also expects sr_Eq and its prototype line.
- 8c expects `F(q) < 0.00001`. Beta 15b's own check expected `F(q) = < 0.00001`, the very form this pass removes.
- 8d allows the two `LEFT` calls of sr_Eq, inside `IF DIM(eqS)>0`. There is still no INSTRING, RIGHT or MID in the PPL code.

**Section 9 (new):**
- **9a.** The P-value page and the Quit summary, beta 15b and 15c, for the table above plus two ordinary cases (q 5, k 4, df 20: `= 0.01029`; q 8, k 6, df 30: `= 0.00005`). These are identical. EP_QPVAL is the same in both, and the summary after q 40 reads `p < 0.00001`.
- **9b.** sr_Eq, including `""` → `" = "` with no error.
- **9c.** The routine diff and the exact code-line diff, and the #PYTHON block byte-identical.
- **9d.**
  - The new names sr_Eq, eqS and pvS are not built-ins, and sr_Eq carries the sr_ tag.
  - The version strings are swept.
  - No comment sits inside an open bracket.
- **8c (all runs).** No scientific fixed decimal in any beta 15c run.

## Gate

`python3 ppl_gate_v1b.py StudRange_beta15c.txt StudRange_beta15b.txt`, in a scratch copy of `gate_r2` with the newest version of every program: **RESULT: PASS**.
- hp-prime-kit lint: 1 error, the #PYTHON block's "unbalanced", as beta 15b.
- ppl_check_v4: 1 E7, as beta 15b. There are no hard errors, E12 included.
- lint_ppl: 18 problems, as beta 15b.
- Parse: it stops at the prototypes, as beta 15b's does (the tool's limit).
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. Paste over beta 15b (open it in the Kit; do not add a second copy). Then Program Catalog → Check.
2. **P-value from q** with q 12, k 3, df 12: the page reads `P(Q ≥ q) < 0.00001`, with no `=`. Then q 40, k 3, df 12: still `< 0.00001`, not `0.00000`; note which engine the badge names. Then q 0.001: `F(q) < 0.00001`.
3. Quit after the q-40 page: Home shows `… p < 0.00001, …`. An ordinary case (q 3.5) still reads `p = 0.07000`.
