# Burr3 v2.4b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on v2.4a; every v2.4a feature is kept, and every ordinary display is unchanged. Run only in the PC harness (ppl_run_v3e); not yet run on hardware or on the emulator (v2.4 passed the emulator; v2.4a never ran there).*

## Why

**B1, a probable crash** (fleet review, 19 Oct 2026, findings_A §3): "The pdf's denominator overflows the Prime's 1E500 for large shapes inside the drawn window." `b3_bpdf` formed `(1 + (x/S)^C)^(K+1)` at every pixel column up to the window's right edge: `Burr3(30, 30, 1, 5)` reaches about 1E706 there, `Burr3(20, 25, 1, 10)` 1E552, `Burr3(100, 100, 1, 1)` 1E613, `Burr3(3, 400, 1, 10)` 1E1276. C and K rise without limit by the arrows (0.25 a press) and drags (0.01 a pixel). The one overflow the fleet has seen on a calculator was a run-time error, which here would open the Program Editor inside the cache loop. The CDF's `(x/S)^C` alone overflows once C is above about 294 at 50·S.

**B2** (findings_A): "Mode, median, mean, S, x₀, C, K and the summary use `STRING(x, 2, 2)` without `ROUND`; a value below 0.01 prints the scientific form": S at its 0.01 floor by the keys drew `mode 5.77ᴇ-3`; `Burr3(1.01, 1, 1, 1)` `mode 5.24ᴇ-3`; `Burr3(1, 100, 1, 1)` `median 6.96ᴇ-3`; `Burr3(2, 1, 1, 0.005)` `x₀ = 5.00ᴇ-3` and `P(X ≤ 5.00ᴇ-3)` in the summary. The moments on the status row (3 decimals) had the same exposure.

**B3**: "A root sign in executable code" (`msd := √(mvar);`), against the house rule; it also stopped the gate's full parse.

**B4**: "`MAKELIST(0, X, 1, N, 1)` at 427-430 writes Home's X."

**The rule for small values** (brief §2, D14 still open, honest minimum): ROUND before STRING so `ᴇ` never shows; a value that is not 0 but would round to 0 at the shown decimals reads in the program's `< 0.01` style, never `0.00` and never in scientific form.

**Roger's disclaimer** (19 Oct 2026, 12:48): a DISCLAIMER line beside the distribution terms.

## What changed (line numbers: v2.4a → v2.4b)

1. **B1, `b3_bpdf` in logarithms** (210-217 → 269-291). `ln pdf = ln(K C) − ln x + ln z − (K+1) ln(1 + z)`, with `ln z = C ln(x/S)`; only the final EXP is taken, so nothing large is ever formed. Past `ln z > 100` (z > 2.7E43), `ln(1 + z)` is `ln z` to far more than 12 digits and the pdf is `K C / (x z^K)`, again in logs (findings_A's proposed routine, word for word). A pdf below the machine's smallest real comes back 0, as before.
2. **B1, new `b3_bcdf`** (→ 293-305): `1 − (1 + z)^(−K)` through the same `ln z`; past `ln z > 100`, `1 − EXP(−K ln z)`. It replaces the three CDF sites: the S-curve cache (505 → 616), `cdf0` (529 → 640) and `EP_BURR_CDF` (1015 → 1141).
3. **The pdf readout** (761 → 883): where v2.4a stopped, the pdf at x₀ can now be smaller than the Prime's smallest real (`Burr3(30, 30, 1, 5)`: about 1E−628) and come back as 0. The Burr pdf is never 0 above 0, so an exact 0 reads `pdf < 0.0001`, as v2.4a already did for an exact-0 CDF. EP_BURR_PDF keeps the computed value.
4. **B2, new `b3_Fx(fxV, fxD)`** (→ 336-352, after `b3_Eq`): `STRING(ROUND(x, d), 2, d)`; a value that is not 0 but rounds to 0 goes through `b3_fmtp`, which writes `< 0.01` (or `< 0.001`). Exactly 0 (the mode when C ≤ 1) still reads `0.00`. Sites:
   - the moments on the status row (468, 477 → 577, 587): `μ = 1.571` or `μ < 0.001`;
   - the three marker labels (666-683 → 780-797): `mode 0.01`, `mode < 0.01`;
   - the title row (744-747 → 860-863): `S = 0.01`, `x₀ < 0.01`;
   - the inverse row (752 → 870);
   - the summary to Home (1019-1021 → 1144-1156): C, K, S through `b3_Fx` and `b3_Eq`; a tiny x₀ keeps its name inside P( ): `P(X ≤ x₀) = 0.1379 with x₀ < 0.01`. Two LOCALs for it, `b3XS`, `b3XT` (→ 471).
   - Left as they were (each cannot reach the scientific form): K×C (0.5 or more), p on the inverse row (0.005 or more), the tick labels and `b3_fmtp`'s own STRINGs.
5. **The status row's K×C** (780 → 906): it starts left of x 248 when it has 13 or more characters (K×C of 1,000 or more), so it ends by x 320 at 6 px a character. `Burr3(123.25, 456.5, 1, 1)` drew `K×C = 56263.62` past the edge; v2.4a mostly stopped in `b3_bpdf` before drawing it, so the review's own C7 passed on v2.4a only for that reason and failed on v2.4b until this line moved. Every K×C below 1,000 still starts at 248.
6. **B3** (476 → 586): `msd := mvar^0.5;`.
7. **B4** (427-430 → 534-537): `MAKELIST(0, b3I, 1, N, 1)`, the routine's own LOCAL counter.
8. **Header:** the banner (4); the DISCLAIMER line (→ 14-16); the firmware lines (→ 18-23: harness only); a "What changed in v2.4b" paragraph (→ 25-73); a MATH VERIFIED line (→ 242-244). The help page's title says `Burr3 v2.4b  -  touch and keys` (321 → 427). Comments above each changed statement say what it does and why.

**Before and after** (harness v3e; each is a check in part D of the verify):

| How it is reached | v2.4a | v2.4b |
|---|---|---|
| `Burr3(30, 30, 1, 5)`, `(100, 100, 1, 1)`, `(20, 25, 1, 10)`, `(3, 400, 1, 10)` | stops in `b3_bpdf` (the harness's doubles end at 1.8E308; the Prime's reals at 1E500) | runs; EP_BURR_PDF, EP_BURR_CDF and the mean = mpmath / burr12; at (30, 30, 1, 5) `pdf < 0.0001 (a height)` |
| S soft key, Down × 25 (S = 0.01), x₀, a tap | `mode 5.77ᴇ-3`, `6.66ᴇ-3`, `8.32ᴇ-3` | `mode 0.01`, `S = 0.01` |
| `Burr3(1.01, 1, 1, 1)` | `mode 5.24ᴇ-3` | `mode 0.01` |
| `Burr3(1, 100, 1, 1)` | `median 6.96ᴇ-3` | `median 0.01`, `mean 0.01` |
| `Burr3(2, 1, 1, 0.005)` | `x₀ = 5.00ᴇ-3`; Home `P(X ≤ 5.00ᴇ-3) < 0.0001` | `x₀ = 0.01`; Home `P(X ≤ 0.01) < 0.0001` |
| `Burr3(2, 1, 0.001, 0.0004)` | `S = 1.00ᴇ-3`, `x₀ = 4.00ᴇ-4`, … | `S < 0.01`, `x₀ < 0.01`, `mode < 0.01`, `median < 0.01`, `mean < 0.01`; Home `… S < 0.01, P(X ≤ x₀) = 0.1379 with x₀ < 0.01` |
| `Burr3(3, 2, 0.0001, 0.0001)` | `μ = 8.061ᴇ-5, σ = 3.953ᴇ-5` | `μ < 0.001, σ < 0.001` |
| 210 ordinary calls; the five views and seven keys | | identical, character for character |

## Verification

`verify_Burr3_v2.4b.py`, built from `verify_Burr3_v2.4a.py`; output in `verify_Burr3_v2.4b_output.txt`: **ALL CHECKS PASSED, 105 checks** (A 50, C 21, B 1, D 33).
- **A.** v2.4's harness run (ppl_run_v1, every touch and key path, numbers against SciPy), now on v2.4b: 50 / 50.
- **B.** verify_Burr3.py, the formula mirror: 4,972 / 0.
- **C.** v2.4a's own checks of its change set (v2.4 against v2.4a), kept as they were and pointed at the v2.4a file in `out/`. Their runs now keep only the scientific strings C6 reads, not the whole harness: with the fleet's other verify runs on the same machine, 460 kept harnesses ran it out of memory once.
- **D. (new)**
  - **D1 regression.** The review's `check_Burr3.py`, run on v2.4b: **290 checks, 0 failed**. On v2.4a the same script fails its 9 checks (C4 × 4: B1; C5 and C6 × 3: B2; D4: B3), plus the two that name the version (help title, D2), which moved to v2.4b. Its C4 sized `(1 + z)^(K+1)` from the inputs alone, so it could never pass whatever the program did; it is restated about the program: the run completes in the harness and EP_BURR_PDF = burr12.pdf. Its three marker-label checks accepted the Prime's scientific form for a value below 0.01; they now also accept B2's `< 0.01` for a value below 0.005 (Burr3(0.25, 4, 1, 1)'s median, 0.0013). Its C7 (text past x 320) passed on v2.4a only because `Burr3(123.25, 456.5, 1, 1)` stopped in `b3_bpdf` before drawing; it passes on v2.4b because the K×C text moved (item 5).
  - **D2.** Each B2 reproduction above, v2.4a against v2.4b, and two summaries.
  - **D3. B1.** `b3_bpdf` against 40-digit mpmath at 1,402 points (C 0.5 to 400, K 0.01 to 400, S 0.01 to 7, x from 1E−6·S to 1000·S), 327 of them in the tail branch: worst relative error 4.3E−13; against `scipy.stats.burr12.pdf` wherever SciPy gives a finite nonzero value (1,380 points, 104 in the tail branch): worst 1.3E−13. `b3_bcdf` against mpmath on the same grid: worst absolute 3.7E−14. The four calls that stopped v2.4a, and (20, 20, 1, 1), (50, 50, 1, 1), end to end.
  - **D4.** 210 ordinary calls, and the five views with seven keys on two distributions: every text v2.4b draws, and its summary, is v2.4a's.
  - **D5. B4.** The four caches count with `b3I`, not X (a code check: the harness binds a MAKELIST counter locally).
  - **D6.** The routine diff: `Burr3`, `b3_bpdf` and `b3_Help` (its title only) changed; `b3_bcdf` and `b3_Fx` added; `b3_lngamma`, `b3_fmtp`, `b3_Eq`, `b3_NiceNum`, `b3_Drain`, `b3_WaitAny` and `b3_Label` byte-identical. Inside `Burr3` every changed code line is a B1, B2, B3 or B4 site, the pdf readout's IFTE or the summary's x₀ slot.
  - **D7.** The new names are not built-ins, ignoring case; version strings and the disclaimer; no comment inside a bracket; LOCAL lines ≤ 6; no root sign, no INSTRING, no MAKELIST counting with K or X; every bare `STRING(x, 2, d)` left has its reason.
  - **D8. Scientific STRING results** over the 245 v2.4b runs of part D: none.

## Gate

`python3 ppl_gate_v1b.py Burr3_v2.4b.txt _old/Burr3_v2.4a.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 3 E5, 1 E7 (v2.4a: 4 E5, 2 E7; the root sign was one of each); no hard errors, E12 included.
- lint_ppl: 4 problems, as v2.4a.
- Full parse: **OK, 12 functions** (v2.4a stopped at the root sign on 476).
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`check.sh` (against `out/Burr3_v2.4a.txt`): kit lint 0 errors; parse OK where v2.4a's failed at `√`.

## Device checklist (emulator first, then G2 and G1)

1. In Home first: `EXP(-2000)` → 0 and `(1.17E6)^(-101)` → 0 (an underflow must give 0, not an error: b3_bpdf and b3_bcdf rely on it far in the tail, as v2.4a's CDF already did). Then `(1.17E6)^101` → an error or ∞ (the overflow v2.4b no longer forms).
2. Paste over v2.4a (open it in the Kit). Program Catalog → Check.
3. `Burr3(2,1,1,1)`: `C = 2.00 … x₀ = 1.00`, `mode 0.58`, `median 1.00`, `mean 1.57`, `pdf = 0.5000 (a height), P(X ≤ x₀) = 0.5000` — unchanged.
4. `Burr3(30,30,1,5)`: the plot draws (v2.4a would have stopped in b3_bpdf), the row reads `pdf < 0.0001 (a height), P(X ≤ x₀) = 1.0000`. Then K chosen, hold Up (or drag right) to K = 60: no error.
5. `Burr3(2,1,1,1)`, S soft key, Down 25 times, x₀ soft key, tap the plot: the labels read `mode 0.01`, `S = 0.01`, never `…ᴇ−3`.
6. `Burr3(2,1,0.001,0.0004)`: `S < 0.01`, `x₀ < 0.01`, `mode < 0.01`; Esc: `… S < 0.01, P(X ≤ x₀) = 0.1379 with x₀ < 0.01; …`.
7. G1: drag C sideways on `Burr3(2,1,1,1)` and judge the redraw (each pixel column now takes about two more LN/EXP than v2.4a's two powers).
8. Before running, `7▶X` in Home; after a run and Esc, `X` still reads 7.

## Unresolved (for Roger)

- **D14** (fleet review §3): the S floor, or three significant figures for small values (one answer for Norm3 and Burr3). v2.4b applies the honest minimum: rounded, or `< 0.01`.
- **B1's alternative** (findings_A): cap C and K at 50 instead of the log-space pdf. Not taken: the log form forbids nothing and changes no ordinary number.
- **Seen, not changed:** a Home call with a tiny K and K·C = 0.5 (`Burr3(500, 0.001, 1, 1)`) makes the window's 0.995 quantile, `0.005^(−1/K)`, pass 1E500 (line 450 → 557); keys and drags keep K ≥ 0.01, where it is at most 1E230. Not in the review's fix list; noted for the next pass.
