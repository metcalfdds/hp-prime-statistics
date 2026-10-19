# Norm3 v2.4b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on v2.4a; every v2.4a feature is kept, and every ordinary display is unchanged. Run only in the PC harness (ppl_run_v3e); not yet run on hardware or on the emulator (v2.4 passed the emulator; v2.4a never ran there).*

## Why

**N1** (fleet review, 19 Oct 2026, findings_A §2): "μ, σ, x₀ and z are printed with `STRING(x, 2, d)` and no `ROUND`, so the Prime prints its scientific form for 0 < |x| < 10⁻ᵈ." The review reached it four ways, all with ordinary controls:
- *keys alone:* σ− 31 times from σ = 1 read `σ = 9.904ᴇ-4` in the title; at the σ floor (0.0001), `σ = 1.000ᴇ-4`, and the animation frames `1.016ᴇ-4`, `1.032ᴇ-4`;
- *a tap:* a press on the S-curve at p = 0.51 with σ = 0.1 read `p = 0.510 → x₀ = 2.51ᴇ-3, z = 0.03`;
- *a drag:* σ = 0.03, 8 px right of the mean line, read `x₀ = 6.91ᴇ-3` while the finger was down;
- *Home:* `Norm3(0, 1, 0.004)` read `x₀ = 4.00ᴇ-3, z = 4.00ᴇ-3`, and the summary `P(X ≤ 4.00ᴇ-3)`.

**The rule for small values** (brief §2, D14 still open, honest minimum): ROUND before STRING so `ᴇ` never shows; a value that is not 0 but would round to 0 at the shown decimals reads in the program's `< 0.001` style, never `0.000` and never in scientific form.

**The K counter** (findings_A, Norm3 improvement 3: "when the file is touched for N1"): `MAKELIST(0, K, 1, N, 1)` writes Home's K on the Prime; Lessons Learned v7i §5 says new code uses a LOCAL counter (GfxProbe T19).

**Roger's disclaimer** (19 Oct 2026, 12:48): a DISCLAIMER line beside the distribution terms.

## What changed (line numbers: v2.4a → v2.4b)

1. **New `n3_Fx(fxV, fxD)`** (→ 283-291, after `n3_Eq`): `STRING(ROUND(x, d), 2, d)`; a value that is not 0 but rounds to 0 goes through `n3_fmtp` instead, which writes `< 0.001` / `> -0.001` (or `< 0.01` at two decimals). Exactly 0 still reads `0.000`.
2. **New `n3_Nm(nmS, nmV, nmD)`** (→ 298-304): for a slot the text already names, as in the summary's `N(μ, σ)`: the number, or the name with the relation, `σ < 0.001`.
3. **The N1 sites:**
   - the title row (624-625 → 701-702): `Normal  μ = 0.000, σ < 0.001`;
   - row 2, the inverse form (636-637 → 716-717) and the readout form (640-641 → 720-721): `x₀ < 0.01, z < 0.01, pdf = …`;
   - the summary to Home (849-850 → 928-939): μ and σ through `n3_Nm`; x₀ through `n3_Fx`, and a tiny x₀ keeps its name inside P( ): `Norm3: N(0.000, 1.000), P(X ≤ x₀) = 0.5016 with x₀ < 0.01; …`. Two LOCALs for it, `n3XS`, `n3XT` (→ 413).
   - Left as they were (each cannot reach the scientific form): p on the inverse row (clamped to 0.005 or more), the tick labels (multiples of their 1-2-5 step), `n3_fmtp`'s own STRINGs, and the z-ruler's whole numbers.
4. **The caches** (388-389 → 462-463): `MAKELIST(0, n3I, 1, N, 1)`, the routine's own LOCAL counter, not Home's K.
5. **Header:** the banner (4); the DISCLAIMER line (→ 14-16); the firmware lines (→ 18-23: harness only); a "What changed in v2.4b" paragraph (→ 25-55); a VERIFIED line (→ 235-237). The help page's title says `Norm3 v2.4b  -  touch and keys` (300 → 372). Comments above each changed statement say what it does and why.

**Before and after** (harness v3e; every one is a check in part D of the verify):

| How it is reached | v2.4a | v2.4b |
|---|---|---|
| σ− 31 times from σ = 1 | `Normal  μ = 0.000, σ = 9.904ᴇ-4` | `Normal  μ = 0.000, σ = 0.001` |
| σ− 60 times (floor 0.0001) | `σ = 1.000ᴇ-4`; Home `N(0.000, 1.000ᴇ-4)` | `σ < 0.001`; Home `N(0.000, σ < 0.001)` |
| S-curve press at p = 0.51, σ = 0.1 | `p = 0.510 → x₀ = 2.51ᴇ-3, z = 0.03` | `p = 0.510 → x₀ < 0.01, z = 0.03` |
| drag 8 px right of the mean, σ = 0.03 | `x₀ = 6.91ᴇ-3, z = 0.23, …` | `x₀ = 0.01, z = 0.23, …` |
| `Norm3(0, 1, 0.004)` | `x₀ = 4.00ᴇ-3, z = 4.00ᴇ-3, …`; Home `P(X ≤ 4.00ᴇ-3) = 0.5016` | `x₀ < 0.01, z < 0.01, …`; Home `P(X ≤ x₀) = 0.5016 with x₀ < 0.01` |
| `Norm3(0.0005, 1, 0.005)` | `Normal  μ = 5.000ᴇ-4, …` | `Normal  μ = 0.001, …`, `x₀ = 0.01, z < 0.01` |
| `Norm3(-0.0004, 1, -0.003)` | `μ = -4.000ᴇ-4`, `x₀ = -3.00ᴇ-3` | `μ > -0.001`, `x₀ > -0.01, z > -0.01`; Home `N(μ > -0.001, 1.000), P(X ≤ x₀) = 0.4990 with x₀ > -0.01` |
| 224 ordinary calls | | identical, character for character |

EP_NORM_* keep the computed values (EP_NORM_X0 = 0.004 above).

## Verification

`verify_Norm3_v2.4b.py`, built from `verify_Norm3_v2.4a.py`; output in `verify_Norm3_v2.4b_output.txt`: **ALL CHECKS PASSED, 93 checks** (A 45, C 21, B 1, D 26).
- **A.** v2.4's harness run (ppl_run_v1, every touch and key path, numbers against SciPy), now on v2.4b: 45 / 45.
- **B.** verify_Norm3.py, the formula mirror: 276 / 0.
- **C.** v2.4a's own checks of its change set (v2.4 against v2.4a), kept as they were and pointed at the v2.4a file in `out/`. Their runs now keep only the scientific strings C6 reads, not the whole harness: with the fleet's other verify runs on the same machine, 460 kept harnesses ran it out of memory once.
- **D. (new)**
  - **D1 regression.** The review's `check_Norm3.py`, run on v2.4b: **172 checks, 0 failed**. The same script on v2.4a fails its 5 N1 checks (C3 × 4, C6), exactly the review's, plus the two expectations that name the version (moved from v2.4a to v2.4b: the help page's title, the version string on screen). Nothing else in it was touched.
  - **D2.** Each reproduction above, v2.4a against v2.4b, and the three summaries.
  - **D3.** `n3_Fx` (12 values, halves away from 0, negatives) and `n3_Nm`.
  - **D4.** 224 ordinary calls (μ 0, 22, −12.5, 500; σ 1, 4, 0.2, 100; 14 values of z): every title, row 2, area key and summary is v2.4a's.
  - **D5.** The caches count with `n3I`, not K (a code check: the harness binds a MAKELIST counter locally, so it cannot show the Prime's write to K).
  - **D6.** The routine diff: `Norm3` and `n3_Help` (its title only) changed, `n3_Fx` and `n3_Nm` added; `n3_fmtp`, `n3_Eq`, `n3_NiceNum`, `n3_Drain` and `n3_WaitAny` byte-identical. Inside `Norm3` the changed code lines are exactly the N1 sites, the summary's x₀ slot and the two MAKELIST lines.
  - **D7.** The new names are not built-ins, ignoring case; version strings and the disclaimer; no comment inside a bracket; LOCAL lines ≤ 6; no INSTRING, no root sign; every bare `STRING(x, 2, d)` left has its reason.
  - **D8. Scientific STRING results** over the 234 v2.4b runs of part D: two, `-5.6ᴇ-17` and `-2.8ᴇ-17`, the axis tick at 0 for σ 0.2 in binary doubles (−0.8 + 4 × 0.2). The Prime's BCD makes that tick exactly 0: the harness's arithmetic, as v2.4a's C6 found. None from μ, σ, x₀, z or the summary.

## Gate

`python3 ppl_gate_v1b.py Norm3_v2.4b.txt _old/Norm3_v2.4a.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 2 E5, 1 E7, as v2.4a (the `x₀` parameter); no hard errors, E12 included.
- lint_ppl: 4 problems, as v2.4a.
- Full parse: OK, 9 functions (v2.4a: 7).
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`check.sh` (against `out/Norm3_v2.4a.txt`): kit lint 0 errors; the same tally; parse OK.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v2.4a (open it in the Kit). Program Catalog → Check.
2. `Norm3(0,1,1)`: `Normal  μ = 0.000, σ = 1.000`, `x₀ = 1.00, z = 1.00, pdf = 0.2420 (a height)` — unchanged.
3. Press σ− (Down) 35 times or more (σ stops at 0.0001 after 42): the title reads `σ < 0.001`, never `…ᴇ−4`; after 31 presses it reads `σ = 0.001`. Esc: Home shows `Norm3: N(0.000, σ < 0.001), …`.
4. `Norm3(0,0.1,0.05)`, press the magenta S-curve just above its middle (p = 0.51): row 2 reads `p = 0.510 → x₀ < 0.01, z = 0.03`.
5. `Norm3(0,1,0.004)`: row 2 `x₀ < 0.01, z < 0.01, …`; Esc: `… P(X ≤ x₀) = 0.5016 with x₀ < 0.01; …`.
6. Before running, type `7▶K` in Home; after a run and Esc, `K` still reads 7 (v2.4a left 278).

## Unresolved (for Roger)

- **D14** (fleet review §3): the σ floor (0.0001) below the title's three decimals, or three significant figures for small values (one answer for Norm3 and Burr3). v2.4b applies the honest minimum: rounded, or `σ < 0.001`.
- **N3** (findings_A): a press where the S-curve crosses the μ line grabs the mean; unchanged.
